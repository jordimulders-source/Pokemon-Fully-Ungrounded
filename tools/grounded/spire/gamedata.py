"""Leest soorten, moves en de typetabel uit de broncode (voor de Spire-rekenscripts)."""
import glob, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
TYPES = ['NONE', 'NORMAL', 'FIGHTING', 'FLYING', 'POISON', 'GROUND', 'ROCK', 'BUG', 'GHOST', 'STEEL',
         'MYSTERY', 'FIRE', 'WATER', 'GRASS', 'ELECTRIC', 'PSYCHIC', 'ICE', 'DRAGON', 'DARK', 'FAIRY', 'STELLAR']


def _read(p):
    with open(os.path.join(ROOT, p), encoding='utf-8') as f:
        return f.read()


def _macros(txt):
    out = {}
    for m in re.finditer(r'#define\s+(\w+)\s+\((?:P_UPDATED_\w+\s*>=\s*GEN_\d+\s*\?\s*)?(\w+)', txt):
        out[m.group(1)] = m.group(2)
    return out


def load_species():
    out = {}
    allsrc = ''.join(open(p, encoding='utf-8').read() for p in glob.glob(os.path.join(ROOT, 'src/data/pokemon/species_info/*.h')))
    macros = _macros(allsrc)
    for path in sorted(glob.glob(os.path.join(ROOT, 'src/data/pokemon/species_info/gen_*_families.h'))):
        txt = open(path, encoding='utf-8').read()
        txt = re.sub(r'\b[A-Z][A-Z0-9_]+\b', lambda m: macros.get(m.group(0), m.group(0)), txt)
        for m in re.finditer(r'\[SPECIES_(\w+)\]\s*=\s*\{', txt):
            body = txt[m.end():m.end() + 2500]
            nxt = re.search(r'\n    \[SPECIES_', body)
            if nxt:
                body = body[:nxt.start()]
            d = {}
            for key, field in (('hp', 'baseHP'), ('atk', 'baseAttack'), ('def', 'baseDefense'),
                               ('spe', 'baseSpeed'), ('spa', 'baseSpAttack'), ('spd', 'baseSpDefense')):
                f = re.search(r'\.%s\s*=\s*(?:P_UPDATED_\w+\s*>=\s*GEN_\d+\s*\?\s*)?(\d+)' % field, body)
                if not f:
                    break
                d[key] = int(f.group(1))
            else:
                t = re.search(r'MON_TYPES\(TYPE_(\w+)(?:,\s*TYPE_(\w+))?\)', body)
                if t:
                    d['types'] = [t.group(1)] + ([t.group(2)] if t.group(2) and t.group(2) != t.group(1) else [])
                    out[m.group(1)] = d
    return out


def load_moves():
    txt = _read('src/data/moves_info.h')
    out = {}
    for m in re.finditer(r'\[MOVE_(\w+)\]\s*=\s*\{', txt):
        body = txt[m.end():m.end() + 3000]
        nxt = re.search(r'\n    \[MOVE_', body)
        if nxt:
            body = body[:nxt.start()]
        p = re.search(r'\.power\s*=\s*(?:B_UPDATED_\w+\s*>=\s*GEN_\d+\s*\?\s*)?(\d+)', body)
        t = re.search(r'\.type\s*=\s*TYPE_(\w+)', body)
        c = re.search(r'\.category\s*=\s*DAMAGE_CATEGORY_(\w+)', body)
        tg = re.search(r'\.target\s*=\s*MOVE_TARGET_(\w+)', body)
        pp = re.search(r'\.pp\s*=\s*(\d+)', body)
        acc = re.search(r'\.accuracy\s*=\s*(\d+)', body)
        if p and t and c:
            out[m.group(1)] = dict(power=int(p.group(1)), type=t.group(1), cat=c.group(1),
                                   target=tg.group(1) if tg else 'SELECTED',
                                   pp=int(pp.group(1)) if pp else 0, acc=int(acc.group(1)) if acc else 100)
    return out


def load_typechart():
    txt = _read('src/data/types_info.h')
    macros = {'______': 1.0, 'STL_RS': 1.0, 'PSN_RS': 0.5, 'BUG_RS': 1.0, 'PSY_RS': 2.0, 'FIR_RS': 0.5}
    chart = {}
    for m in re.finditer(r'\[TYPE_(\w+)\]\s*=\s*\{([^}]*)\}', txt.split('gTypeEffectivenessTable')[1].split('};')[0]):
        vals = []
        for tok in [x.strip() for x in m.group(2).split(',') if x.strip()]:
            x = re.match(r'X\(([\d.]+)\)', tok)
            vals.append(float(x.group(1)) if x else macros[tok])
        chart[m.group(1)] = dict(zip(TYPES, vals))
    return chart
