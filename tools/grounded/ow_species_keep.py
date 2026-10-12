#!/usr/bin/env python3
"""Verzamelt welke Pokémon-overworldsprites de game echt gebruikt en schrijft
src/data/pokemon/ow_species_keep.h (een #define per sPicTable_* die in de ROM moet blijven).

Gebruikt = elke OBJ_EVENT_GFX_SPECIES(...)/_SHINY/_FEMALE/_SHINY_FEMALE in data/, src/ en include/
(kaarten, scripts, Stadium-pool, C-code) en elke `SPECIES_X + OBJ_EVENT_MON`. Alle andere soorten
krijgen geen overworldData en tonen dus de substitute-placeholder (OW_SUBSTITUTE_PLACEHOLDER);
hun graphics worden niet gelinkt.

Schakelaar: OW_ONLY_USED_SPECIES in include/config/overworld.h (FALSE = alles terug).
De Makefile draait dit script automatisch (AUTO_GEN_TARGETS); het schrijft alleen bij een wijziging.
Handmatig: python3 tools/grounded/ow_species_keep.py [-v]
"""
import os, re, sys

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OUT = os.path.join(REPO, 'src/data/pokemon/ow_species_keep.h')
SPECIES_H = os.path.join(REPO, 'include/constants/species.h')
INFO_DIR = os.path.join(REPO, 'src/data/pokemon/species_info')

# Soorten die altijd mee moeten (bijv. runtime-gebruik dat niet via de macro loopt). Leeg = alleen de scan.
ALWAYS_KEEP = []

GFX_RE = re.compile(r'OBJ_EVENT_GFX_SPECIES(?:_SHINY|_FEMALE|_SHINY_FEMALE)?\(\s*(\w+)\s*\)')
PLUS_RE = re.compile(r'\b(SPECIES_\w+)\s*[+|]\s*OBJ_EVENT_MON\b|\bOBJ_EVENT_MON\s*[+|]\s*(SPECIES_\w+)')
SCAN_EXT = ('.json', '.inc', '.s', '.pory', '.c', '.h', '.party')
SKIP = {os.path.normpath(p) for p in (OUT, os.path.join(REPO, 'include/constants/event_objects.h'))}


def scan_used():
    used = {}
    for top in ('data', 'src', 'include'):
        for root, dirs, files in os.walk(os.path.join(REPO, top)):
            for f in files:
                if not f.endswith(SCAN_EXT):
                    continue
                p = os.path.normpath(os.path.join(root, f))
                if p in SKIP:
                    continue
                try:
                    s = open(p, encoding='utf-8', errors='ignore').read()
                except OSError:
                    continue
                if 'OBJ_EVENT_GFX_SPECIES' not in s and 'OBJ_EVENT_MON' not in s:
                    continue
                rel = os.path.relpath(p, REPO)
                for m in GFX_RE.finditer(s):
                    used.setdefault('SPECIES_' + m.group(1), set()).add(rel)
                for m in PLUS_RE.finditer(s):
                    used.setdefault(m.group(1) or m.group(2), set()).add(rel)
    return used


def load_aliases():
    alias = {}
    for m in re.finditer(r'^#define\s+(SPECIES_\w+)\s+(SPECIES_\w+)\b', open(SPECIES_H).read(), re.M):
        alias[m.group(1)] = m.group(2)
    return alias


def resolve(sp, alias):
    seen = set()
    while sp in alias and sp not in seen:
        seen.add(sp)
        sp = alias[sp]
    return sp


PIC_RE = re.compile(r'\bOVERWORLD(?:_FEMALE)?\(\s*(?:\\\s*)*([\w\s#]+?)\s*,')


def load_pic_tables():
    """species -> set(sPicTable_*), ook voor entries die via een *_INFO(...)-macro gemaakt worden."""
    table, macros = {}, {}
    entries = []
    for f in sorted(os.listdir(INFO_DIR)):
        if not f.endswith('.h'):
            continue
        s = open(os.path.join(INFO_DIR, f)).read()
        joined = s.replace('\\\n', ' ')
        for m in re.finditer(r'^#define\s+(\w+)\(([^)]*)\)(.*)$', joined, re.M):
            pics = PIC_RE.findall(m.group(3))
            if pics:
                macros[m.group(1)] = ([a.strip() for a in m.group(2).split(',')], pics)
        starts = [(m.start(), m.group(1)) for m in re.finditer(r'^\s*\[(SPECIES_\w+)\]\s*=', s, re.M)]
        for i, (pos, sp) in enumerate(starts):
            end = starts[i + 1][0] if i + 1 < len(starts) else len(s)
            body = s[pos:end]
            d = re.search(r'^#define\s', body, re.M)  # macrodefinities na de entry horen er niet bij
            entries.append((sp, body[:d.start()] if d else body))
    for sp, body in entries:
        pics = set(p.replace(' ', '').replace('#', '') for p in PIC_RE.findall(body))
        m = re.search(r'=\s*(\w+)\(([^)]*)\)', body)
        if m and m.group(1) in macros:
            params, mpics = macros[m.group(1)]
            args = [a.strip() for a in m.group(2).split(',')]
            env = dict(zip(params, args))
            for p in mpics:
                toks = [env.get(t, t) for t in re.split(r'\s*##\s*|\s+', p.strip()) if t]
                pics.add(''.join(toks))
        if pics:
            table.setdefault(sp, set()).update(pics)
    return table


def main():
    verbose = '-v' in sys.argv
    alias = load_aliases()
    pics = load_pic_tables()
    used = scan_used()
    for sp in ALWAYS_KEEP:
        used.setdefault(sp, set()).add('ALWAYS_KEEP')
    keep, missing = {}, []
    for sp in sorted(used):
        real = resolve(sp, alias)
        if real in pics:
            for p in pics[real]:
                keep.setdefault(p, set()).add(sp)
        elif re.fullmatch(r'SPECIES_[A-Z0-9_]+', sp) and sp not in ('SPECIES_NONE',):
            missing.append((sp, sorted(used[sp])))
    if missing:
        for sp, where in missing:
            print(f'ow_species_keep.py: geen overworld-sprite gevonden voor {sp} (gebruikt in {", ".join(where)})', file=sys.stderr)
    lines = ['// Gegenereerd door tools/grounded/ow_species_keep.py: niet met de hand bewerken.',
             '// Overworld-sprites die in de ROM blijven als OW_ONLY_USED_SPECIES TRUE is.',
             '#ifndef GUARD_OW_SPECIES_KEEP_H', '#define GUARD_OW_SPECIES_KEEP_H', '']
    for p in sorted(keep):
        lines.append(f'#define OWKEEP_{p} 1 // {", ".join(sorted(keep[p]))}')
    lines += ['', '#endif // GUARD_OW_SPECIES_KEEP_H', '']
    text = '\n'.join(lines)
    old = open(OUT).read() if os.path.exists(OUT) else None
    if old != text:
        open(OUT, 'w').write(text)
        print(f'ow_species_keep.py: {len(keep)} overworld-sprites bewaard ({len(used)} soorten gebruikt) -> {os.path.relpath(OUT, REPO)}')
    elif verbose:
        print(f'ow_species_keep.py: ongewijzigd ({len(keep)} sprites)')
    if verbose:
        for p in sorted(keep):
            print(' ', p, sorted(keep[p]))


if __name__ == '__main__':
    main()
