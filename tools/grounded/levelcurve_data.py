"""Project Grounded: parsers voor de levelcurve-simulatie (soorten, trainers, kaarten, wild)."""
import glob
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def species_const(name):
    """'Graveler_Alola' -> 'SPECIES_GRAVELER_ALOLA'."""
    n = name.strip().replace('♀', '_F').replace('♂', '_M').replace('é', 'e').replace("'", '').replace('’', '')
    n = re.sub(r'[^A-Za-z0-9]+', '_', n).strip('_').upper()
    return 'SPECIES_' + n


def species_name(const):
    """'SPECIES_GRAVELER_ALOLA' -> 'Graveler_Alola' (zoals trainers.party)."""
    return '_'.join(w.capitalize() for w in const[len('SPECIES_'):].split('_'))


def parse_species():
    """SPECIES_X -> {'yield', 'growth', 'evos': [(level, target)]}."""
    out = {}
    for path in sorted(glob.glob(os.path.join(ROOT, 'src/data/pokemon/species_info/gen_*_families.h'))):
        text = open(path, encoding='utf-8').read()
        macros = {}
        for m in re.finditer(r'#define\s+(\w+_EXP_YIELD)\s+(\d+)', text):
            macros.setdefault(m.group(1), int(m.group(2)))  # eerste = nieuwste gen
        parts = re.split(r'\n\s*\[(SPECIES_\w+)\]\s*=', text)
        for i in range(1, len(parts), 2):
            name, body = parts[i], parts[i + 1]
            d = {'yield': 100, 'growth': 'GROWTH_MEDIUM_FAST', 'evos': [], 'abilities': [], 'evo_other': False}
            m = re.search(r'\.expYield\s*=\s*([^,\n]+(?:\?[^,\n]+)?),', body)
            if m:
                e = m.group(1).strip()
                if '?' in e:
                    e = e.split('?')[1].split(':')[0].strip()
                if e in macros:
                    d['yield'] = macros[e]
                elif e.isdigit():
                    d['yield'] = int(e)
            m = re.search(r'\.growthRate\s*=\s*(GROWTH_\w+)', body)
            if m:
                d['growth'] = m.group(1)
            m = re.search(r'\.abilities\s*=\s*\{([^}]*)\}', body)
            if m:
                d['abilities'] = [a.strip() for a in m.group(1).split(',') if a.strip()]
            m = re.search(r'\.evolutions\s*=\s*EVOLUTION\((.*?)\)\s*,\s*$', body, re.S | re.M)
            if m:
                for e in re.finditer(r'\{(EVO_\w+),\s*(\d+),\s*(SPECIES_\w+)([^{}]*(?:\{[^}]*\}[^{}]*)*)\}', m.group(1)):
                    if e.group(1) == 'EVO_LEVEL' and 'CONDITIONS' not in e.group(4) and int(e.group(2)) > 0:
                        d['evos'].append((int(e.group(2)), e.group(3)))
                    else:
                        d['evo_other'] = True
            out[name] = d
    return out


def parse_party():
    """TRAINER_X -> {'mons': [{'species','level','lineno','raw'}], 'double', 'class', 'start', 'end'}."""
    path = os.path.join(ROOT, 'src/data/trainers.party')
    lines = open(path, encoding='utf-8').read().split('\n')
    trainers = {}
    cur = None
    expect_species = False
    for i, line in enumerate(lines):
        m = re.match(r'^=== (TRAINER_\w+) ===', line)
        if m:
            if cur:
                cur['end'] = i
            cur = {'name': m.group(1), 'mons': [], 'double': False, 'class': '', 'start': i}
            trainers[m.group(1)] = cur
            expect_species = False
            continue
        if cur is None:
            continue
        s = line.strip()
        if not s:
            expect_species = True
            continue
        if s.startswith('Double Battle:'):
            cur['double'] = 'Yes' in s
        elif s.startswith('Class:'):
            cur['class'] = s.split(':', 1)[1].strip()
        if expect_species and not s.startswith('-') and not s.startswith('/*') and ':' not in s.split('@')[0]:
            sp = s.split('@')[0].strip()
            sp = re.sub(r'\((M|F)\)', '', sp).strip()
            m2 = re.match(r'^.*\(([^)]+)\)$', sp)
            if m2:
                sp = m2.group(1)
            cur['mons'].append({'species': species_const(sp), 'raw': sp, 'level': None, 'lineno': None, 'spline': i})
        if s.startswith('Level:') and cur['mons']:
            cur['mons'][-1]['level'] = int(s.split(':')[1].split('/')[0].strip())
            cur['mons'][-1]['lineno'] = i
        expect_species = False
    if cur:
        cur['end'] = len(lines)
    return trainers, lines


TB = re.compile(r'^\s*(trainerbattle\w*|multi_2_vs_2|multi_2_vs_1|multi_fixed_2_vs_2)\s+(.*)$')


def map_trainers(mapname):
    """Trainers in een kaartscript, in volgorde (geen rematches)."""
    path = os.path.join(ROOT, 'data/maps', mapname, 'scripts.inc')
    if not os.path.exists(path):
        return []
    out = []
    for line in open(path, encoding='utf-8'):
        m = TB.match(line)
        if not m or 'rematch' in m.group(1):
            continue
        for t in re.findall(r'\bTRAINER_\w+', m.group(2)):
            if t.startswith('TRAINER_BATTLE_') or t.startswith('TRAINER_FLAGS'):
                continue
            if t not in out:
                out.append(t)
    return out


def dedup_rival(trainers):
    """Van rivaal-varianten (May/Brendan × starter) één houden."""
    out, seen = [], set()
    for t in trainers:
        key = re.sub(r'_(TREECKO|TORCHIC|MUDKIP)$', '', t)
        key = key.replace('TRAINER_MAY_', 'TRAINER_RIVAL_').replace('TRAINER_BRENDAN_', 'TRAINER_RIVAL_')
        if key in seen:
            continue
        seen.add(key)
        out.append(t)
    return out


def parse_wild():
    """map-constante -> {'land': [(min,max,species)], 'water': ...}."""
    data = json.load(open(os.path.join(ROOT, 'src/data/wild_encounters.json'), encoding='utf-8'))
    out = {}
    for group in data['wild_encounter_groups']:
        if not group.get('for_maps'):
            continue
        for enc in group['encounters']:
            if 'map' not in enc:
                continue
            if enc.get('base_label', '').endswith(('_Night', '_Morning', '_Evening')):
                continue
            d = out.setdefault(enc['map'], {})
            for kind in ('land_mons', 'water_mons', 'rock_smash_mons', 'fishing_mons'):
                if kind in enc and kind not in d:
                    d[kind] = [(m['min_level'], m.get('max_level', m['min_level']), m['species']) for m in enc[kind]['mons']]
    return out


def map_const(mapname):
    """'Route102' -> 'MAP_ROUTE102' (via map.json)."""
    path = os.path.join(ROOT, 'data/maps', mapname, 'map.json')
    try:
        return json.load(open(path, encoding='utf-8'))['id']
    except Exception:
        return None
