#!/usr/bin/env python3
"""Project Grounded: levels bewaken na het draaien van bouwscripts (levelcurve v0.9.192).

De levelcurve (tools/grounded/levelcurve.py, LEVELCURVE.md) heeft de levels in
  - src/data/trainers.party            (Level: per Pokémon)
  - src/data/wild_encounters.json      (min_level/max_level per slot)
  - data/maps/*/scripts.inc, data/scripts/*.inc   (setwildbattle SPECIES, LEVEL)
direct aangepast. De bouwscripts in tools/grounded/maptools/ bevatten nog hun eigen
(oude) levels. Daarom:

1. Bewaker in de bouwscripts:
       import check_levels; check_levels.protect()
   neemt bij de start een momentopname van alle levels en zet bij het afsluiten
   (atexit, of eerder met check_levels.restore()) de levels van entries die al
   bestonden terug naar de momentopname. Nieuwe entries (nieuwe trainer, nieuwe
   wilde tabel, nieuwe setwildbattle) houden het level uit het script.
   Bewust een level in een script wijzigen: draai met GROUNDED_SCRIPT_LEVELS=1
   (of pas de waarde direct in het databestand aan).
   Sleutels: trainer + volgnummer van de Pokémon; tabel-label + veld + slot;
   kaartbestand + soort + n-de setwildbattle met die soort.

2. Controle achteraf (CLI):
       python3 tools/grounded/check_levels.py           # t.o.v. HEAD: welke levels gingen omlaag?
       python3 tools/grounded/check_levels.py --all     # ook verhogingen tonen
       python3 tools/grounded/check_levels.py --rev X   # t.o.v. een andere commit
       python3 tools/grounded/check_levels.py --fix     # verlaagde levels terugzetten naar REV
   Exitcode 1 als er levels omlaag gingen.
"""
import atexit
import glob
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRAINERS = 'src/data/trainers.party'
WILD = 'src/data/wild_encounters.json'
SKIP = {'data/scripts/debug.inc'}


def script_files():
    fs = glob.glob(os.path.join(ROOT, 'data/maps/*/scripts.inc')) + glob.glob(os.path.join(ROOT, 'data/scripts/*.inc'))
    out = [os.path.relpath(f, ROOT) for f in fs]
    return sorted(f for f in out if f not in SKIP)


# ---------------------------------------------------------------- extractors
# Elk geeft een lijst (sleutel, waarde, (start, eind)) met de tekstpositie van het getal.

HDR = re.compile(r'^=== *(\S+) *===', re.M)
LVL = re.compile(r'^Level:[ \t]*(\d+)', re.M)


def species_in_line(line):
    """Soort uit een soortregel (Soort / Bijnaam (Soort) / ... (M) @ Item): (naam, offset) of None."""
    t = line.split('@')[0].rstrip()
    t = re.sub(r' \([MF]\)$', '', t)
    m = re.search(r'\(([^()]+)\)$', t)
    if m:
        return m.group(1).strip(), m.start(1) + (len(m.group(1)) - len(m.group(1).lstrip()))
    if not t or not t[0].isupper() or ':' in t:
        return None
    return t.strip(), len(t) - len(t.lstrip())


def trainer_levels(text):
    """Level per Pokémon (sleutel T) en de soort (sleutel TS: de levelcurve liet ook evolueren)."""
    out = []
    heads = [(m.start(), m.group(1)) for m in HDR.finditer(text)]
    hi, count, cur = 0, 0, None
    for m in LVL.finditer(text):
        while hi < len(heads) and heads[hi][0] < m.start():
            cur, count = heads[hi][1], 0
            hi += 1
        out.append((('T', cur, count), int(m.group(1)), m.span(1)))
        # soortregel = eerste regel van de alinea met het level
        a = text.rfind('\n\n', 0, m.start()) + 2
        b = text.index('\n', a)
        sp = species_in_line(text[a:b]) if a < m.start() else None
        if sp:
            out.append((('TS', cur, count), sp[0], (a + sp[1], a + sp[1] + len(sp[0]))))
        count += 1
    return out


_evo = None


def species_const(name):
    return 'SPECIES_' + re.sub(r'[^A-Z0-9]+', '_', name.replace("'", '').upper().replace('\u00c9', 'E')).strip('_')


def evolves_into(a, b):
    """True als soort b (naam) een latere evolutie is van soort a (naam)."""
    global _evo
    if _evo is None:
        _evo = {}
        for f in glob.glob(os.path.join(ROOT, 'src/data/pokemon/species_info/*.h')):
            t = open(f, encoding='utf-8').read()
            for blk in re.split(r'\n\s*\[(?=SPECIES_\w+\]\s*=)', t)[1:]:
                sp = blk[:blk.index(']')]
                for ev in re.findall(r'\.evolutions = EVOLUTION\((.*?)\}\),', blk, re.S):
                    _evo.setdefault(sp, set()).update(re.findall(r'\{EVO_\w+,\s*[^,{}]+,\s*(SPECIES_\w+)', ev))
    start, goal = species_const(a), species_const(b)
    todo, seen = [start], set()
    while todo:
        for n in _evo.get(todo.pop(), ()):
            if n == goal:
                return True
            if n not in seen:
                seen.add(n)
                todo.append(n)
    return False


def differs(key, new, ref):
    """Moet de waarde uit ref terug? Levels altijd; soorten alleen als ref een evolutie van new is."""
    if key[0] == 'TS':
        return new != ref and evolves_into(new, ref)
    return new != ref


class _Json:
    """Mini-JSON-parser die van elk getal het pad en de tekstpositie bijhoudt."""
    WS = re.compile(r'\s*')
    NUM = re.compile(r'-?\d+(\.\d+)?([eE][-+]?\d+)?')
    STR = re.compile(r'"(?:[^"\\]|\\.)*"')

    def __init__(self, text):
        self.t, self.i, self.nums = text, 0, []

    def ws(self):
        self.i = self.WS.match(self.t, self.i).end()

    def value(self, path):
        self.ws()
        c = self.t[self.i]
        if c == '{':
            self.i += 1
            obj = {}
            self.ws()
            if self.t[self.i] == '}':
                self.i += 1
                return obj
            while True:
                self.ws()
                m = self.STR.match(self.t, self.i)
                key = json.loads(m.group(0))
                self.i = m.end()
                self.ws()
                assert self.t[self.i] == ':'
                self.i += 1
                obj[key] = self.value(path + (key,))
                self.ws()
                c = self.t[self.i]
                self.i += 1
                if c == '}':
                    return obj
                assert c == ','
        if c == '[':
            self.i += 1
            arr = []
            self.ws()
            if self.t[self.i] == ']':
                self.i += 1
                return arr
            while True:
                arr.append(self.value(path + (len(arr),)))
                self.ws()
                c = self.t[self.i]
                self.i += 1
                if c == ']':
                    return arr
                assert c == ','
        if c == '"':
            m = self.STR.match(self.t, self.i)
            self.i = m.end()
            return json.loads(m.group(0))
        m = self.NUM.match(self.t, self.i)
        if m:
            self.i = m.end()
            self.nums.append((path, m.span()))
            return json.loads(m.group(0))
        for word, val in (('true', True), ('false', False), ('null', None)):
            if self.t.startswith(word, self.i):
                self.i += len(word)
                return val
        raise ValueError('JSON-fout op positie %d' % self.i)


def wild_levels(text):
    p = _Json(text)
    data = p.value(())
    out = []
    for path, span in p.nums:
        # wild_encounter_groups, g, encounters, i, <veld>, mons, j, min_level/max_level
        if len(path) == 8 and path[0] == 'wild_encounter_groups' and path[2] == 'encounters' \
                and path[5] == 'mons' and path[7] in ('min_level', 'max_level'):
            grp = data['wild_encounter_groups'][path[1]]
            enc = grp['encounters'][path[3]]
            lab = enc.get('base_label') or '%s/%s' % (enc.get('map'), path[3])
            key = ('W', grp.get('label'), lab, path[4], path[6], path[7])
            out.append((key, int(text[span[0]:span[1]]), span))
    return out


SWB = re.compile(r'^[ \t]*setwildbattle[ \t]+([^\n@]*)', re.M)
PAIR = re.compile(r'(SPECIES_\w+)\s*,\s*(\d+)\b')


def script_levels(text, name):
    out, seen = [], {}
    for m in SWB.finditer(text):
        base = m.start(1)
        for p in PAIR.finditer(m.group(1)):
            sp = p.group(1)
            n = seen.get(sp, 0)
            seen[sp] = n + 1
            out.append((('S', name, sp, n), int(p.group(2)), (base + p.start(2), base + p.end(2))))
    return out


def extract(name, text):
    if name == TRAINERS:
        return trainer_levels(text)
    if name == WILD:
        return wild_levels(text)
    return script_levels(text, name)


def all_files():
    return [TRAINERS, WILD] + script_files()


def read(name):
    p = os.path.join(ROOT, name)
    if not os.path.exists(p):
        return None
    with open(p, encoding='utf-8') as f:
        return f.read()


# ---------------------------------------------------------------- bewaker

_snap = None


def snapshot():
    snap = {}
    for name in all_files():
        t = read(name)
        if t is None:
            continue
        lv = {k: v for k, v, _ in extract(name, t)}
        if lv:
            snap[name] = lv
    return snap


def apply_levels(name, text, ref, only_down=False):
    """Zet levels van sleutels die in ref staan terug; geeft (nieuwe tekst, wijzigingen)."""
    changes = []
    parts, last = [], 0
    for key, val, (a, b) in sorted(extract(name, text), key=lambda x: x[2][0]):
        if key in ref and differs(key, val, ref[key]) and (not only_down or key[0] == 'TS' or val < ref[key]):
            parts.append(text[last:a])
            parts.append(str(ref[key]))
            last = b
            changes.append((key, val, ref[key]))
    parts.append(text[last:])
    return ''.join(parts), changes


def restore(verbose=True):
    """Levels van bestaande entries terugzetten naar de momentopname van protect()."""
    if not _snap:
        return []
    allc = []
    for name, ref in _snap.items():
        t = read(name)
        if t is None:
            continue
        nt, ch = apply_levels(name, t, ref)
        if ch:
            with open(os.path.join(ROOT, name), 'w', encoding='utf-8') as f:
                f.write(nt)
            allc += ch
    if verbose and allc:
        print('check_levels: %d level(s)/evolutie(s) uit het script teruggezet naar de levelcurve, bijv.:' % len(allc))
        for key, old, new in allc[:8]:
            print('   %s: %s -> %s' % (fmt(key), old, new))
        print('   (bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1)')
    return allc


def protect():
    global _snap
    if _snap is not None or os.environ.get('GROUNDED_SCRIPT_LEVELS') == '1':
        return
    _snap = snapshot()
    atexit.register(restore)


# ---------------------------------------------------------------- CLI

def fmt(key):
    if key[0] in ('T', 'TS'):
        return '%s mon %d' % (key[1], key[2] + 1)
    if key[0] == 'W':
        return '%s %s slot %d %s' % (key[2], key[3], key[4], key[5])
    return '%s %s #%d' % (os.path.basename(os.path.dirname(key[1])) or key[1], key[2], key[3] + 1)


def git_show(rev, name):
    r = subprocess.run(['git', 'show', '%s:%s' % (rev, name)], cwd=ROOT, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--rev', default='HEAD')
    ap.add_argument('--all', action='store_true', help='ook verhogingen tonen')
    ap.add_argument('--fix', action='store_true', help='verlaagde levels terugzetten naar REV')
    a = ap.parse_args()
    names = subprocess.run(['git', 'diff', '--name-only', a.rev, '--', TRAINERS, WILD, 'data/maps', 'data/scripts'],
                           cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    names = [n for n in names if (n in (TRAINERS, WILD) or n.endswith('.inc')) and n not in SKIP]
    down = up = 0
    for name in names:
        old, new = git_show(a.rev, name), read(name)
        if old is None or new is None:
            continue
        ref = {k: v for k, v, _ in extract(name, old)}
        for key, val, _ in extract(name, new):
            if key in ref and key[0] == 'TS':
                if differs(key, val, ref[key]):
                    down += 1
                    print('TERUG-GEËVOLUEERD  %s: %s -> %s' % (fmt(key), ref[key], val))
            elif key in ref and ref[key] != val:
                if val < ref[key]:
                    down += 1
                    print('OMLAAG  %s: %d -> %d' % (fmt(key), ref[key], val))
                elif a.all:
                    up += 1
                    print('omhoog  %s: %d -> %d' % (fmt(key), ref[key], val))
        if a.fix:
            nt, ch = apply_levels(name, new, ref, only_down=True)
            if ch:
                with open(os.path.join(ROOT, name), 'w', encoding='utf-8') as f:
                    f.write(nt)
    print('check_levels: %d level(s) omlaag of terug-geëvolueerd%s t.o.v. %s%s' % (
        down, ', %d omhoog' % up if a.all else '', a.rev, ' (teruggezet)' if a.fix and down else ''))
    return 1 if down and not a.fix else 0


if __name__ == '__main__':
    sys.exit(main())
