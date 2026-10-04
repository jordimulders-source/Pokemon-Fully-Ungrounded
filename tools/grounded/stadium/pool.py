#!/usr/bin/env python3
"""Battle Stadium (Project Grounded): toernooipool en compagnons. Zie STADIUM_DESIGN.md.

Genereert:
- src/data/stadium_pool.h: de deelnemers (trainer, sterkte) en de compagnons (partner, vrijspelen)
- de PARTNER_STADIUM_*-blokken onderaan src/data/battle_partners.party (tussen de markeringen)
  en hun constanten in include/constants/battle_partner.h: per personage zijn 3 sterkste Pokémon
  (de ace altijd), op level 50.

Sterkte = gemiddelde BST van de 4 sterkste Pokémon (dezelfde keuze als de C-code maakt: de ace
plus de hoogste BST, in de volgorde van het team). De simulatie van NPC-wedstrijden gebruikt die.

Nieuwe personages (CLAUDE.md): voeg ze toe aan POOL (en eventueel aan COMPANIONS) en draai opnieuw.
Gebruik: python3 tools/grounded/stadium/pool.py
"""
import os, re, sys
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools/grounded/spire'))
from spiredata import load_species

LEVEL = 50
PARTY = os.path.join(ROOT, 'src/data/trainers.party')
PARTNERS = os.path.join(ROOT, 'src/data/battle_partners.party')
PARTNER_H = os.path.join(ROOT, 'include/constants/battle_partner.h')
OUT = os.path.join(ROOT, 'src/data/stadium_pool.h')
BEGIN = '/* --- Battle Stadium (gegenereerd door tools/grounded/stadium/pool.py) --- */'
END = '/* --- einde Battle Stadium --- */'

# Deelnemers: de sterkste versie van elk personage. 'rival' = alleen als de speler het andere geslacht is.
POOL = [
    # Hoenn-gymleiders (laatste rematch)
    'ROXANNE_5', 'BRAWLY_5', 'WATTSON_5', 'FLANNERY_5', 'NORMAN_5', 'WINONA_5', 'TATE_AND_LIZA_5', 'JUAN_5',
    # Elite Four en kampioenen
    'SIDNEY', 'PHOEBE', 'GLACIA', 'DRAKE', 'WALLACE', 'STEVEN',
    # verhaal
    'WALLY_VR_5', 'ARCHIE_SOOTOPOLIS', 'MAXIE_SOOTOPOLIS', 'BIRCH_UNDERWATER', 'KECCLES_3', 'COLRESS_MAGMA',
    'ZINNIA', 'MIMI', 'GABBY_AND_TY_6', 'JOEY',
    # Aqua- en Magma-admins (sterkste versie)
    'MATT', 'SHELLY_SEAFLOOR_CAVERN', 'TABITHA_MOSSDEEP',
    # geïmporteerd voor het Stadium (v0.8.108): Kanto (FRLG), Sinnoh (Platinum), Frontier Brains
    'STADIUM_BROCK', 'STADIUM_MISTY', 'STADIUM_LT_SURGE', 'STADIUM_ERIKA', 'STADIUM_KOGA', 'STADIUM_SABRINA',
    'STADIUM_BLAINE', 'STADIUM_GIOVANNI', 'STADIUM_LORELEI', 'STADIUM_BRUNO', 'STADIUM_AGATHA', 'STADIUM_LANCE',
    'STADIUM_BLUE', 'STADIUM_RED', 'STADIUM_OAK',
    'STADIUM_ROARK', 'STADIUM_GARDENIA', 'STADIUM_MAYLENE', 'STADIUM_WAKE', 'STADIUM_FANTINA', 'STADIUM_BYRON',
    'STADIUM_CANDICE', 'STADIUM_VOLKNER', 'STADIUM_AARON', 'STADIUM_BERTHA', 'STADIUM_FLINT', 'STADIUM_LUCIAN',
    'STADIUM_CYNTHIA', 'STADIUM_CYRUS', 'STADIUM_BARRY', 'STADIUM_MARS', 'STADIUM_JUPITER', 'STADIUM_SATURN',
    'STADIUM_PALMER', 'STADIUM_THORTON', 'STADIUM_ARGENTA', 'STADIUM_DAHLIA', 'STADIUM_RILEY',
    'STADIUM_ANABEL', 'STADIUM_TUCKER', 'STADIUM_SPENSER', 'STADIUM_GRETA', 'STADIUM_NOLAND', 'STADIUM_LUCY', 'STADIUM_BRANDON',
    # Jordi en zijn maten (Ace Trainers in Victory Road)
    'ALBERT', 'SAMUEL', 'OWEN',
]
RIVALS = {'BRENDAN_ROUTE_136_TREECKO': 'FEMALE', 'MAY_ROUTE_136_TORCHIC': 'MALE'}   # speler-geslacht waarvoor dit de rivaal is

# Compagnons: (partnernaam, bron-trainer, vrijspelen). Vrijspelen: 'start', ('beat', TRAINER) of ('points', n).
# Iedereen uit de pool wordt compagnon zodra je hem in het Stadium verslaat (Vampire Survivors-stijl).
COMPANIONS = [('BRENDAN', 'BRENDAN_ROUTE_136_TREECKO', 'start'), ('MAY', 'MAY_ROUTE_136_TORCHIC', 'start'),
              ('KECCLES', 'KECCLES_3', 'start'), ('WALLY', 'WALLY_VR_5', 'start')]
def companion_name(t):
    special = {'TATE_AND_LIZA_5': 'TATE_AND_LIZA', 'GABBY_AND_TY_6': 'GABBY_AND_TY', 'LT_SURGE': 'LT_SURGE'}
    t2 = t[len('STADIUM_'):] if t.startswith('STADIUM_') else t
    return special.get(t, special.get(t2, t2.split('_')[0]))


COMPANIONS += [(companion_name(t), t, ('beat', t)) for t in POOL if t not in ('KECCLES_3', 'WALLY_VR_5')]

# Rugplaatjes die bestaan; de rest staat met zijn voorplaatje naast je (zoals de Frontier-tag battles)
BACK_PICS = {'Brendan': 'Brendan', 'May': 'May', 'Red': 'Red', 'Leaf': 'Leaf', 'Steven': 'Steven', 'Wally': 'Wally', 'Kecleon': 'Kecleon'}

# Overworld-sprite in de arena: eigen sprite waar die bestaat, anders een Pokémon of een passende generieke
GFX = {
    'ROXANNE': 'ROXANNE', 'BRAWLY': 'BRAWLY', 'WATTSON': 'WATTSON', 'FLANNERY': 'FLANNERY', 'NORMAN': 'NORMAN',
    'WINONA': 'WINONA', 'TATE_AND_LIZA': 'TATE', 'JUAN': 'JUAN', 'SIDNEY': 'SIDNEY', 'PHOEBE': 'PHOEBE',
    'GLACIA': 'GLACIA', 'DRAKE': 'DRAKE', 'WALLACE': 'WALLACE', 'STEVEN': 'STEVEN', 'WALLY': 'WALLY',
    'ARCHIE': 'ARCHIE', 'MAXIE': 'MAXIE', 'BIRCH': 'PROF_BIRCH', 'KECCLES': 'KECLEON', 'COLRESS': 'COLRESS',
    'ZINNIA': 'ZINNIA', 'MIMI': 'SPECIES(MIMIKYU)', 'BROCK': 'BROCK', 'OAK': 'PROF_OAK', 'RED': 'RED',
    'LEAF': 'LEAF', 'JOEY': 'YOUNGSTER', 'BRENDAN': 'RIVAL_BRENDAN_NORMAL', 'MAY': 'RIVAL_MAY_NORMAL',
    'GABBY': 'REPORTER_F', 'MATT': 'AQUA_MEMBER_M', 'SHELLY': 'AQUA_MEMBER_F', 'TABITHA': 'MAGMA_MEMBER_M',
    'ANABEL': 'ANABEL', 'TUCKER': 'TUCKER', 'SPENSER': 'SPENSER', 'GRETA': 'GRETA', 'NOLAND': 'NOLAND',
    'LUCY': 'LUCY', 'BRANDON': 'BRANDON', 'BRUNO': 'BLACK_BELT', 'MAYLENE': 'BLACK_BELT', 'MISTY': 'SWIMMER_F',
    'LT_SURGE': 'SAILOR', 'WAKE': 'SAILOR', 'KOGA': 'NINJA_BOY', 'SABRINA': 'HEX_MANIAC', 'BLAINE': 'SCIENTIST_1',
    'GIOVANNI': 'GENTLEMAN', 'CYRUS': 'GENTLEMAN', 'AGATHA': 'OLD_WOMAN', 'BERTHA': 'OLD_WOMAN',
    'LORELEI': 'BEAUTY', 'LANCE': 'MAN_3', 'BLUE': 'BOY_3', 'BARRY': 'BOY_3', 'ROARK': 'HIKER', 'BYRON': 'HIKER',
    'GARDENIA': 'PICNICKER', 'ERIKA': 'LASS', 'FANTINA': 'BEAUTY', 'CANDICE': 'GIRL_3', 'VOLKNER': 'MAN_5',
    'AARON': 'BUG_CATCHER', 'FLINT': 'MAN_5', 'LUCIAN': 'PSYCHIC_M', 'CYNTHIA': 'WOMAN_5', 'MARS': 'WOMAN_2',
    'JUPITER': 'WOMAN_2', 'SATURN': 'MAN_2', 'PALMER': 'MAN_4', 'THORTON': 'SCIENTIST_2', 'ARGENTA': 'WOMAN_3',
    'DAHLIA': 'WOMAN_4', 'RILEY': 'MAN_3', 'ALBERT': 'MAN_3', 'SAMUEL': 'MAN_3', 'OWEN': 'MAN_3', 'WINSTON': 'RICH_BOY',
}


def gfx_for(t, header):
    t2 = t[len('STADIUM_'):] if t.startswith('STADIUM_') else t
    for key, g in GFX.items():
        if t2 == key or t2.startswith(key + '_'):
            return 'OBJ_EVENT_GFX_' + g
    female = (header_field(header, 'Gender') or '').lower() == 'female'
    return 'OBJ_EVENT_GFX_' + ('WOMAN_5' if female else 'MAN_3')


species = load_species()
by_disp = {}
for key, d in species.items():
    by_disp.setdefault(d['dispname'].upper(), key)


def species_key(line):
    s = line.split(' @ ')[0].strip()
    m = re.search(r'\(([^()]+)\)\s*(\((?:M|F)\))?\s*$', s)
    if m and m.group(1) not in ('M', 'F'):
        s = m.group(1)
    s = re.sub(r'\s*\((?:M|F)\)\s*$', '', s).strip()
    k = s.upper().replace(' ', '_').replace('-', '_').replace('.', '').replace("'", '').replace('é', 'E')
    for cand in (k, k + '_STANDARD', k + '_NORMAL', k.replace('_HOENN', '')):
        if cand in species:
            return cand
    return by_disp.get(s.upper())


def bst(key):
    d = species.get(key)
    return sum(d[s] for s in ('hp', 'atk', 'def', 'spa', 'spd', 'spe')) if d else 400


def parse_trainers():
    txt = open(PARTY, encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'^=== TRAINER_(\w+) ===\n(.*?)(?=^=== |\Z)', txt, re.S | re.M):
        name, body = m.group(1), m.group(2)
        parts = re.split(r'\n\s*\n', body.strip('\n'))
        header = parts[0]
        mons = [p for p in parts[1:] if p.strip() and not p.lstrip().startswith('/*')]
        out[name] = dict(header=header, mons=mons)
    return out


# --- synergie (Jordi: "een trainer die met een rain team speelt moet altijd een drizzle mon hebben") ---
# per archetype: zetters (abilities/moves) en wie ervan profiteert (abilities/moves/types)
ARCHETYPES = {
    'regen': dict(set_ab={'DRIZZLE', 'PRIMORDIAL_SEA'}, set_mv={'RAIN_DANCE'},
                  use_ab={'SWIFT_SWIM', 'RAIN_DISH', 'HYDRATION', 'DRY_SKIN'}, use_mv={'THUNDER', 'HURRICANE', 'ELECTRO_SHOT', 'WEATHER_BALL'}, use_type={'WATER'}),
    'zon': dict(set_ab={'DROUGHT', 'DESOLATE_LAND', 'ORICHALCUM_PULSE'}, set_mv={'SUNNY_DAY'},
                use_ab={'CHLOROPHYLL', 'SOLAR_POWER', 'FLOWER_GIFT', 'LEAF_GUARD', 'PROTOSYNTHESIS', 'HARVEST'},
                use_mv={'SOLAR_BEAM', 'SOLAR_BLADE', 'WEATHER_BALL', 'GROWTH'}, use_type={'FIRE'}),
    'zand': dict(set_ab={'SAND_STREAM', 'SAND_SPIT'}, set_mv={'SANDSTORM'},
                 use_ab={'SAND_RUSH', 'SAND_FORCE', 'SAND_VEIL'}, use_mv={'SHORE_UP', 'WEATHER_BALL'}, use_type={'ROCK'}),
    'sneeuw': dict(set_ab={'SNOW_WARNING'}, set_mv={'HAIL', 'SNOWSCAPE', 'CHILLY_RECEPTION'},
                   use_ab={'SLUSH_RUSH', 'ICE_BODY', 'SNOW_CLOAK'}, use_mv={'BLIZZARD', 'AURORA_VEIL', 'WEATHER_BALL'}, use_type={'ICE'}),
    'zure regen': dict(set_ab={'AIR_POLLUTION'}, set_mv={'ACID_RAIN'}, use_ab=set(), use_mv=set(), use_type={'POISON'}),
    'stuifmeel': dict(set_ab={'POLLEN_SEASON'}, set_mv={'POLLEN_HAZE'}, use_ab=set(), use_mv=set(), use_type={'BUG', 'GRASS'}),
    'elektrisch terrein': dict(set_ab={'ELECTRIC_SURGE', 'HADRON_ENGINE'}, set_mv={'ELECTRIC_TERRAIN'},
                               use_ab={'SURGE_SURFER', 'QUARK_DRIVE'}, use_mv={'RISING_VOLTAGE'}, use_type=set()),
    'psychisch terrein': dict(set_ab={'PSYCHIC_SURGE'}, set_mv={'PSYCHIC_TERRAIN'}, use_ab=set(), use_mv={'EXPANDING_FORCE'}, use_type=set()),
    'gras-terrein': dict(set_ab={'GRASSY_SURGE', 'SEED_SOWER'}, set_mv={'GRASSY_TERRAIN'}, use_ab={'GRASS_PELT'}, use_mv={'GRASSY_GLIDE'}, use_type=set()),
    'mist-terrein': dict(set_ab={'MISTY_SURGE'}, set_mv={'MISTY_TERRAIN'}, use_ab=set(), use_mv={'MISTY_EXPLOSION'}, use_type=set()),
}


def mon_info(block):
    first = block.split('\n')[0]
    key = species_key(first)
    d = species.get(key, {})
    ab = re.search(r'^Ability:\s*(.+)$', block, re.M)
    ability = ab.group(1).strip().upper().replace(' ', '_').replace('-', '_') if ab else (d.get('abilities') or ['NONE'])[0]
    moves = {m.strip().upper().replace(' ', '_').replace('-', '_') for m in re.findall(r'^- (.+)$', block, re.M)}
    return dict(key=key, bst=bst(key), ability=ability, moves=moves, types=set(d.get('types', [])), spe=d.get('spe', 80))


def score(sub, infos, notes=None):
    sc = sum(infos[i]['bst'] for i in sub)
    sc += 15 * len(set().union(*(infos[i]['types'] for i in sub)))
    for name, a in ARCHETYPES.items():
        setter = any(infos[i]['ability'] in a['set_ab'] or infos[i]['moves'] & a['set_mv'] for i in sub)
        hard = sum(1 for i in sub if infos[i]['ability'] in a['use_ab'] or infos[i]['moves'] & a['use_mv'])
        soft = sum(1 for i in sub if infos[i]['types'] & a['use_type'])
        if setter and (hard or soft):
            sc += 40 + 60 * hard + 15 * soft
            if notes is not None:
                notes.add(name)
        elif hard and not setter:
            sc -= 60 * hard
    tr = [i for i in sub if 'TRICK_ROOM' in infos[i]['moves']]
    if tr:
        slow = sum(1 for i in sub if infos[i]['spe'] <= 50 and i not in tr)
        if slow:
            sc += 40 * slow
            if notes is not None:
                notes.add('Trick Room')
    return sc


def pick(mons, n, notes=None):
    """Beste n Pokémon met synergie (de ace = laatste altijd mee), in teamvolgorde. De C-code neemt deze keuze over."""
    from itertools import combinations
    infos = [mon_info(m) for m in mons]
    keys = [x['key'] for x in infos]
    if len(mons) <= n:
        if notes is not None:
            score(list(range(len(mons))), infos, notes)
        return list(range(len(mons))), keys
    ace = len(mons) - 1
    best = max((list(c) + [ace] for c in combinations(range(ace), n - 1)), key=lambda sub: score(sub, infos))
    if notes is not None:
        score(best, infos, notes)
    return sorted(best), keys


def header_field(header, field):
    m = re.search(r'^%s:\s*(.*)$' % field, header, re.M)
    return m.group(1).strip() if m else None


trainers = parse_trainers()
errors = []
for t in POOL + list(RIVALS) + [c[1] for c in COMPANIONS]:
    if t not in trainers:
        errors.append(f'onbekende trainer TRAINER_{t}')
if errors:
    print('\n'.join(errors)); sys.exit(1)

rows = []
report = ['# Battle Stadium: teams (gegenereerd door tools/grounded/stadium/pool.py)', '',
          'Per trainer de keuze voor singles (4) en doubles/compagnon (3): de ace (laatste) altijd, verder sterkte +',
          'synergie (weer/terrein met zijn zetter, Trick Room met trage Pokémon, typedekking). Level 50.', '',
          '| Trainer | Sterkte | Singles (4) | Doubles (3) | Synergie |', '|---|---|---|---|---|']
masks = {}
for t in POOL + list(RIVALS):
    notes = set()
    idx, keys = pick(trainers[t]['mons'], 4, notes)
    idx3, _ = pick(trainers[t]['mons'], 3, notes)
    masks[t] = (sum(1 << i for i in idx), sum(1 << i for i in idx3))
    nm = lambda i: species[keys[i]]['dispname'] if keys[i] in species else '?'
    report.append(f'| {t} | {{r}} | {", ".join(nm(i) for i in idx)} | {", ".join(nm(i) for i in idx3)} | {", ".join(sorted(notes)) or "-"} |')
    unknown = [trainers[t]['mons'][i].split('\n')[0] for i in idx if keys[i] is None]
    if unknown:
        print(f'let op: {t}: soort niet herkend: {unknown}')
    rating = round(sum(bst(keys[i]) for i in idx) / len(idx))
    report[-1] = report[-1].replace('{r}', str(rating))
    gender = RIVALS.get(t)
    rows.append((t, rating, {'MALE': 1, 'FEMALE': 2}.get(gender, 0), gfx_for(t, trainers[t]['header'])))

# partners
blocks, consts = [], []
for i, (pname, src, unlock) in enumerate(COMPANIONS):
    tr = trainers[src]
    idx, keys = pick(tr['mons'], 3)
    pic = header_field(tr['header'], 'Pic')
    back = BACK_PICS.get(pic)
    lines = [f'=== PARTNER_STADIUM_{pname} ===']
    for f in ('Name', 'Class'):
        lines.append(f'{f}: {header_field(tr["header"], f)}')
    lines.append(f'Pic: {pic}')
    g = header_field(tr['header'], 'Gender') or 'Male'
    lines += [f'Gender: {g}', f'Music: {header_field(tr["header"], "Music") or g}', f'Back Pic: {back or "Brendan"}']
    ai = header_field(tr['header'], 'AI')
    if ai:
        lines.append(f'AI: {ai}')
    lines.append('')
    for j in idx:
        mon = re.sub(r'^Level:\s*\d+', f'Level: {LEVEL}', tr['mons'][j], flags=re.M)
        lines.append(mon.strip('\n'))
        lines.append('')
    blocks.append('\n'.join(lines))
    consts.append((f'PARTNER_STADIUM_{pname}', back is None))

party = open(PARTNERS, encoding='utf-8').read()
for old in (BEGIN, '# --- Battle Stadium (gegenereerd door tools/grounded/stadium/pool.py) ---'):
    if old in party:
        party = party[:party.index(old)].rstrip('\n') + '\n'
party = party.rstrip('\n') + '\n\n' + BEGIN + '\n\n' + '\n'.join(blocks) + '\n' + END + '\n'
open(PARTNERS, 'w', encoding='utf-8').write(party)

h = open(PARTNER_H, encoding='utf-8').read()
h = re.sub(r'\n// Battle Stadium \(pool\.py\)\n.*?(?=#define PARTNER_COUNT)', '\n', h, flags=re.S)
base = int(re.search(r'#define PARTNER_COUNT (\d+)', h).group(1)) if 'PARTNER_STADIUM' not in h else None
first = max(int(x) for x in re.findall(r'#define PARTNER_\w+ (\d+)', h.split('#define PARTNER_COUNT')[0])) + 1
defs = '// Battle Stadium (pool.py)\n' + ''.join(f'#define {c} {first + i}\n' for i, (c, _) in enumerate(consts))
h = re.sub(r'#define PARTNER_COUNT \d+', defs + f'#define PARTNER_COUNT {first + len(consts)}', h)
open(PARTNER_H, 'w', encoding='utf-8').write(h)

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('// Gegenereerd door tools/grounded/stadium/pool.py; niet met de hand bewerken.\n\n')
    f.write('// {trainer, sterkte (gem. BST van de singles-keuze), rivaal voor speler-geslacht (0 = altijd, 1 = man, 2 = vrouw),\n')
    f.write('//  keuze singles (bitmasker teamplekken), keuze doubles, overworld-sprite in de arena}\n')
    f.write('static const struct StadiumEntrant sStadiumPool[] =\n{\n')
    for t, r, g, gfx in rows:
        f.write(f'    {{TRAINER_{t}, {r}, {g}, 0x{masks[t][0]:02X}, 0x{masks[t][1]:02X}, {gfx}}},\n')
    f.write('};\n\n')
    f.write('// {partner, bron-trainer, voorplaatje i.p.v. rugplaatje, vrijspelen: STADIUM_UNLOCK_*, waarde}\n')
    f.write('static const struct StadiumCompanion sStadiumCompanions[] =\n{\n')
    for (pname, src, unlock), (c, front) in zip(COMPANIONS, consts):
        if unlock == 'start':
            u = 'STADIUM_UNLOCK_START, 0'
        elif unlock[0] == 'beat':
            u = f'STADIUM_UNLOCK_BEAT, TRAINER_{unlock[1]}'
        else:
            u = f'STADIUM_UNLOCK_POINTS, {unlock[1]}'
        f.write(f'    {{{c}, TRAINER_{src}, {"TRUE" if front else "FALSE"}, {u}, {gfx_for(src, trainers[src]["header"])}}},\n')
    f.write('};\n')
open(os.path.join(ROOT, 'STADIUM_TEAMS.md'), 'w', encoding='utf-8').write('\n'.join(report) + '\n')
print(f'{len(rows)} deelnemers, {len(COMPANIONS)} compagnons -> {os.path.relpath(OUT, ROOT)}')
for t, r, g, gfx in sorted(rows, key=lambda x: -x[1]):
    print(f'  {r:4d}  {t}')
