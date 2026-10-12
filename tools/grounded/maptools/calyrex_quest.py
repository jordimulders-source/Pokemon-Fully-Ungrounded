"""Project Grounded: de Calyrex-quest met Glastrier en Spectrier (post-game, na het National Park).

- CrownTundra (40x34, General + snow): een verborgen sneeuwvallei achter Route 136. Bovenin een bergwand met de
  grotmond waar je binnenkomt (warp 0 = terug naar Route 136). Een spoor van platgetrapte sneeuw loopt naar het
  vervallen kroonheiligdom rechtsboven (stenen plein, een rotsblok als altaar, gebroken ijspilaren). Links een
  ijsveld (GLASTRIER), rechtsonder een donker dennenbos (SPECTRIER), daartussen hoog sneeuwgras.
- Ingang: een grotopening in de zuidwand van het heuveltje rechtsonder op Route 136 (deur op (45,33)). De opening
  staat dicht in map.bin en gaat open (setmetatile in Route136_OnLoad) zodra FLAG_NATIONAL_PARK_DONE gezet is.
- Quest: Calyrex staat bij het heiligdom en vraagt je zijn paard terug te halen. Dan verschijnen beide paarden; je
  kiest er één door het aan te spreken (ja/nee), het andere verdwijnt voorgoed. Gevangen paard -> terug naar Calyrex:
  hij geeft de REINS OF UNITY en daagt je uit (Calyrex lv 88). Verslagen paard/Calyrex komt terug bij het volgende
  bezoek; alleen vangen rondt af.
- Registratie: layouts.json, map_groups.json (achteraan gMapGroup_Grounded), event_scripts.s, mapsec + popups +
  region_map (speciale plek bij Route 136), wilde Pokemon, flags (FLAG_GROUNDED 1280-1319, blok 'calyrex'), items via
  nieuwe_items.py (1300-1309), eigen case in BattleSetup_StartLegendaryBattle.
Idempotent, vaste seed. Controleert de bereikbaarheid van de warp, het heiligdom, de paarden en de items.
Gebruik: python3 tools/grounded/maptools/calyrex_quest.py [renderdir]   (render: na make, de tiles.4bpp zijn nodig)"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
# Levels: de levelcurve (v0.9.192) is leidend; check_levels zet bestaande levels bij het afsluiten terug.
import check_levels  # noqa: E402
check_levels.protect()
import importlib.util, json, os, random, re, struct, sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
os.chdir(REPO)
sys.path.insert(0, HERE)
import snowlib as sl
import nieuwe_items as ni

_spec = importlib.util.spec_from_file_location('dialogen_import', 'tools/dialogen/import.py')
dimp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dimp)

NAME, CONST = 'CrownTundra', 'CROWN_TUNDRA'
GROUP = 'gMapGroup_Grounded'
W, H = 40, 34
STEED_LEVEL, CALYREX_LEVEL = 86, 88
R136_DOOR = (45, 33)                 # grotopening in het heuveltje rechtsonder op Route 136
R136_GROTTO_MOUTH = (50, 24)         # bestaande grotmond (Route136_Grotto): bron van de tegels

# ====================================================================== flags (FLAG_GROUNDED 1280-1319)
FLAGS = [
    (1280, 'FLAG_CROWN_QUEST_STARTED', 'Crown Tundra: Calyrex heeft gevraagd zijn paard terug te halen (paarden verschijnen)'),
    (1281, 'FLAG_CROWN_CHOSE_GLASTRIER', 'Crown Tundra: GLASTRIER gevangen (naam historisch; beide paarden zijn te vangen)'),
    (1282, 'FLAG_CROWN_CHOSE_SPECTRIER', 'Crown Tundra: SPECTRIER gevangen (naam historisch; beide paarden zijn te vangen)'),
    (1283, 'FLAG_CROWN_STEED_DONE', 'Crown Tundra: minstens één paard gevangen (Calyrex geeft de Reins)'),
    (1284, 'FLAG_RECEIVED_REINS_OF_UNITY', 'Crown Tundra: REINS OF UNITY gekregen van Calyrex'),
    (1285, 'FLAG_CROWN_CALYREX_DONE', 'Crown Tundra: CALYREX gevangen (quest klaar)'),
]
FLAG_RANGE = (1280, 1319)


def flags():
    p = 'include/constants/flags.h'
    s = open(p).read()
    blk = '// calyrex { (tools/grounded/maptools/calyrex_quest.py; FLAG_GROUNDED 1280-1319: 1280-1285 quest, ' \
          '1300-1309 nieuwe items (nieuwe_items.py), 1286-1299 en 1310-1319 nog vrij)\n'
    for n, name, why in FLAGS:
        assert FLAG_RANGE[0] <= n <= FLAG_RANGE[1]
        blk += '#define %-48s FLAG_GROUNDED(%d) // Project Grounded: %s\n' % (name, n, why)
    blk += '// }'
    if '// calyrex {' in s:
        i = s.index('// calyrex {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        anchor = s.index('// national_park {')
        s = s[:anchor] + blk + '\n' + s[anchor:]
    for n, *_ in FLAGS:
        assert len(re.findall(r'FLAG_GROUNDED\(%d\)' % n, s)) == 1, ('flag dubbel', n)
    open(p, 'w').write(s)
    ni.flags()


# ====================================================================== de kaart
TOP = set(sl.rect(-1, -1, W, 2)) | set(sl.rect(4, -1, 15, 5)) | set(sl.rect(25, -1, W, 3))
AX = 9                                   # grotmond (deur op (AX,5)), aankomst op (AX,6)
PLAZA = set(sl.rect(27, 8, 34, 13))      # stenen plein van het heiligdom
ALTAR = (30, 6)                          # rotsblok 2x2 (30-31, 6-7)
CALYREX = (30, 10)
SIGN = (31, 7)                           # het altaar (aanspreken vanaf (31,8))
GLASTRIER = (7, 21)
SPECTRIER = (33, 23)
TRAIL = set(sl.rect(AX, 6, AX + 1, 15)) | set(sl.rect(AX, 14, 31, 15))


def build(items):
    """items: dict met 'ice' (bal), 'ghost' (bal), 'hidden' (verborgen) -> (x,y)."""
    m = sl.M(W, H)
    rnd = random.Random(898)                       # dexnummer Calyrex
    for y in range(H):
        for x in range(W):
            if rnd.random() < 0.05:
                m.put(x, y, rnd.choice(['snow_dots', 'snow_light', 'tuft0', 'tuft1', 'tuft3']))
    # bergwand met de grotmond
    sl.terrace(m, TOP)
    for x, n in zip((AX - 1, AX, AX + 1), ('cliff_front_a', 'cliff_front_b', 'cliff_front_c')):
        m.put(x, 4, n, 1)
    for x, n in zip((AX - 1, AX, AX + 1), ('cave_l', 'cave_door', 'cave_r')):
        m.put(x, 5, n, 1)
    m.put(AX, 5, 'cave_door', 0, 0)
    topc = lambda x, y: 0 <= x < W and 0 <= y < H and m.g[y][x] == sl.N['cliff_c']
    for (px, py) in [(5, 0), (12, 2), (27, 0), (33, 0), (37, 0)]:
        if all(topc(px + i, py + j) for i in (0, 1) for j in (0, 1)):
            for i in (0, 1):
                for j in (0, 1):
                    m.put(px + i, py + j, 'peak_%d%d' % (i, j), 1)
    for (px, py) in [(10, 0), (6, 1)]:
        if all(topc(px + i, py + j) for i in (0, 1) for j in (0, 1, 2)):
            m.pine(px, py, green=px % 2 == 0)
    # spoor van platgetrapte sneeuw en het stenen plein
    sl.autopath(m, TRAIL, 'deep')
    sl.autopath(m, PLAZA, 'path_stone')
    for i in (0, 1):
        for j in (0, 1):
            m.put(ALTAR[0] + i, ALTAR[1] + j, 'boulder_%d%d' % (i, j), 1)
    for (x, y), n in [((26, 7), 'ice_crystal'), ((35, 7), 'ice_crystal2'), ((26, 13), 'rock_snow4'),
                      ((35, 13), 'ice_rock2'), ((28, 6), 'rock_snow3'), ((33, 6), 'ice_chunks')]:
        m.put(x, y, n, 0 if n == 'ice_chunks' else 1)
    events = {GLASTRIER, SPECTRIER, CALYREX, SIGN, items['ice'], items['ghost']}
    solid_events = events - {SIGN}
    keep = set(TRAIL) | set(PLAZA) | {(AX, 6)}
    for (x, y) in events | {items['hidden']}:
        keep |= {(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)}

    def free(x, y):
        return 0 <= x < W and 0 <= y < H and m.col[y][x] == 0 and m.elev[y][x] == 3 and (x, y) not in keep

    def reach_ok():
        start = (AX, 6)
        seen, q = {start}, deque([start])
        while q:
            x, y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                if not (0 <= n[0] < W and 0 <= n[1] < H) or n in seen:
                    continue
                if m.col[n[1]][n[0]] or n in solid_events:
                    continue
                seen.add(n); q.append(n)
        adj = lambda p: any((p[0] + dx, p[1] + dy) in seen for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        return all(adj(e) for e in events) and items['hidden'] in seen and (31, 8) in seen

    # Hoenn-randbomen links, rechts en onder; het dennenbos van Spectrier rechtsonder
    BAND = set(sl.rect(0, 3, 3, H - 1)) | set(sl.rect(W - 4, 4, W - 1, H - 1)) | set(sl.rect(0, H - 4, W - 1, H - 1))
    BAND |= set(sl.rect(4, H - 6, 7, H - 5)) | set(sl.rect(16, 3, 19, 4))
    sl.hforest(m, BAND, free)
    HT = {sl.N[k] for k in sl.N if k.startswith('htree')}
    near_tree = lambda x, y: any(0 <= x + dx < W and 0 <= y + dy < H and m.g[y + dy][x + dx] in HT
                                 for dx in (-1, 0, 1) for dy in (-1, 0, 1))

    def pine(x, y, green):
        cells = [(x + dx, y + dy) for dx in range(2) for dy in range(3)]
        if not all(free(*c) and m.g[c[1]][c[0]] != sl.N['grass_snow'] for c in cells):
            return
        old = [(c, m.g[c[1]][c[0]], m.col[c[1]][c[0]]) for c in cells]
        m.pine(x, y, green=green)
        if not reach_ok():
            for (cx, cy), g, c in old:
                m.g[cy][cx] = g; m.col[cy][cx] = c
    # Spectriers bos: dicht, donkergroen, met een open plek in het midden
    grove = [(29, 17), (31, 16), (35, 17), (28, 21), (36, 20), (30, 26), (34, 26), (27, 25), (32, 19),
             (25, 19), (25, 23), (36, 24)]
    for (x, y) in grove:
        pine(x, y, True)
    for (x, y) in [(31, 21), (35, 22)]:
        if free(x, y) and free(x, y + 1):
            m.put(x, y, 'thinpine_0', 1); m.put(x, y + 1, 'thinpine_1', 1)
            if not reach_ok():
                m.put(x, y, 'snow', 0); m.put(x, y + 1, 'snow', 0)
    # ijsveld van Glastrier
    for (x, y) in sl.blob(8, 22, 4.5, 3.5, seed=8961, rough=0.25):
        if free(x, y) and rnd.random() < 0.5:
            m.put(x, y, rnd.choice(['snow_deep', 'snow_deep2', 'snow_light']), 0)
    for (x, y), n in [((4, 19), 'ice_rock'), ((11, 19), 'ice_crystal'), ((5, 24), 'ice_crystal2'),
                      ((11, 24), 'ice_rock2'), ((9, 18), 'ice_chunks'), ((6, 18), 'rock_cluster')]:
        if free(x, y):
            m.put(x, y, n, 0 if n == 'ice_chunks' else 1)
            if not reach_ok():
                m.put(x, y, 'snow', 0)
    # hoog sneeuwgras (wilde Pokemon)
    for c, seed in [((19, 20, 4, 3), 1), ((15, 27, 4.5, 2.5), 2), ((22, 9, 3, 2), 3), ((28, 30, 3, 1.5), 4),
                    ((13, 10, 2.5, 2), 5)]:
        for (x, y) in sl.blob(*c, seed=seed):
            if free(x, y) and not near_tree(x, y):
                m.put(x, y, 'grass_snow', 0)
    # losse dennen en decor (nooit iets afsluiten)
    for (x, y) in [(5, 8), (22, 15), (13, 16), (20, 24), (8, 27), (23, 29)]:
        pine(x, y, rnd.random() < 0.4)
    BLOCK = ['rock_snow', 'rock_snow2', 'rock_cluster', 'ice_rock', 'snowball', 'stump', 'log', 'bush_snow']
    SOFT = ['flowers_blue', 'tuft2', 'tuft4', 'tuft6', 'tuft7', 'snow_deep', 'snow_deep2']
    cands = [(x, y) for y in range(6, H) for x in range(W) if free(x, y)]
    rnd.shuffle(cands)
    for (x, y) in cands:
        if not free(x, y) or m.g[y][x] == sl.N['grass_snow']:
            continue
        r = rnd.random()
        if r < 0.04:
            old = m.g[y][x]
            m.put(x, y, rnd.choice(BLOCK), 1)
            if not reach_ok():
                m.put(x, y, old, 0)
        elif r < 0.10:
            m.put(x, y, rnd.choice(SOFT), 0)
    assert reach_ok(), 'Crown Tundra: iets onbereikbaar'
    for e in events | {items['hidden']}:
        assert m.col[e[1]][e[0]] == 0 or e == SIGN, ('event op een blokkerende tegel', e)
    return m


# ====================================================================== registratie
def read_layout(name):
    L = {l['name']: l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if 'name' in l}[name + '_Layout']
    w, h = L['width'], L['height']
    v = struct.unpack('<%dH' % (w * h), open(L['blockdata_filepath'], 'rb').read())
    return [list(v[y * w:(y + 1) * w]) for y in range(h)]


def register_layout(name, const, w, h, secondary):
    lj = open('data/layouts/layouts.json').read()
    entry = '''    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_General",
      "secondary_tileset": "%s",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    }''' % (const, name, w, h, secondary, name, name)
    if '"LAYOUT_%s"' % const in lj:
        i = lj.index('"id": "LAYOUT_%s"' % const); s = lj.rindex('    {', 0, i); e = lj.index('    }', i) + 5
        lj = lj[:s] + entry + lj[e:]
    else:
        i = lj.rindex('    }\n  ]')
        lj = lj[:i + 5] + ',\n' + entry + lj[i + 5:]
    json.loads(lj)
    open('data/layouts/layouts.json', 'w').write(lj)


def save_layout(m):
    os.makedirs('data/layouts/' + NAME, exist_ok=True)
    open('data/layouts/%s/map.bin' % NAME, 'wb').write(b''.join(struct.pack('<H', v) for v in m.bin()))
    open('data/layouts/%s/border.bin' % NAME, 'wb').write(open('data/layouts/Route136/border.bin', 'rb').read())
    register_layout(NAME, CONST, W, H, 'gTileset_Snow')


def register_map():
    g = open('data/maps/map_groups.json').read()
    i = g.index('"%s": [' % GROUP); j = g.index(']', i)
    if '"%s"' % NAME not in g[i:j]:
        k = g.rindex('"', i, j) + 1
        g = g[:k] + ',\n    "%s"' % NAME + g[k:]
        j = g.index(']', i)
    assert len(re.findall(r'"([^"]+)"', g[g.index('[', i):j])) <= 128
    json.loads(g)
    open('data/maps/map_groups.json', 'w').write(g)
    es = open('data/event_scripts.s').read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % NAME
    if inc not in es:
        a = '\t.include "data/maps/MangroveMire/scripts.inc"\n'
        assert a in es
        es = es.replace(a, a + inc, 1)
    open('data/event_scripts.s', 'w').write(es)


def mapsec():
    mid, nm = 'MAPSEC_CROWN_TUNDRA', 'CROWN TUNDRA'
    p = 'src/data/region_map/region_map_sections.json'
    s = open(p).read()
    if '"%s"' % mid not in s:
        i = s.rindex('    }\n  ]')
        s = s[:i + 5] + ',\n    {\n      "id": "%s",\n      "name": "%s"\n    }' % (mid, nm) + s[i + 5:]
    json.loads(s)
    open(p, 'w').write(s)
    p = 'src/map_name_popup.c'
    s = open(p).read()
    a = '    [MAPSEC_CRYSTAL_CAVITY - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_STONE, // Project Grounded\n'
    b = '    [MAPSEC_CRYSTAL_CAVITY - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_BW_DEFAULT, // Project Grounded\n'
    assert a in s and b in s
    if '[%s - KANTO' % mid not in s:
        s = s.replace(a, a + '    [%s - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_MARBLE, // Project Grounded: Calyrex-quest\n' % mid, 1)
        s = s.replace(b, b + '    [%s - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_BW_DEFAULT, // Project Grounded: Calyrex-quest\n' % mid, 1)
    open(p, 'w').write(s)
    p = 'src/region_map.c'
    s = open(p).read()
    a = '    {MAPSEC_CRYSTAL_CAVITY,              MAPSEC_ROUTE_136}, // Project Grounded\n'
    assert a in s
    if '{%s,' % mid not in s:
        s = s.replace(a, a + '    {%s,               MAPSEC_ROUTE_136}, // Project Grounded: Calyrex-quest\n' % mid, 1)
    open(p, 'w').write(s)


def battle_setup():
    p = 'src/battle_setup.c'
    s = open(p).read()
    if 'case SPECIES_GLASTRIER:' in s:
        return
    a = '    case SPECIES_ETERNATUS: // Project Grounded: National Park'
    i = s.index(a); j = s.index('break;\n', i) + len('break;\n')
    s = s[:j] + ('    case SPECIES_GLASTRIER: // Project Grounded: Crown Tundra, Calyrex-quest (placeholder: Kanto-legendary-thema, ijs dat splijt)\n'
                 '        CreateBattleStartTask(B_TRANSITION_SHRED_SPLIT, MUS_RG_VS_LEGEND);\n        break;\n'
                 '    case SPECIES_SPECTRIER: // Project Grounded: Crown Tundra, Calyrex-quest (placeholder: Kanto-legendary-thema, zwart gat)\n'
                 '        CreateBattleStartTask(B_TRANSITION_BLACKHOLE, MUS_RG_VS_LEGEND);\n        break;\n'
                 '    case SPECIES_CALYREX: // Project Grounded: Crown Tundra, de koning zelf (placeholder: Kanto-legendary-thema)\n'
                 '    case SPECIES_CALYREX_ICE:\n    case SPECIES_CALYREX_SHADOW:\n'
                 '        CreateBattleStartTask(B_TRANSITION_FRONTIER_CIRCLES_MEET, MUS_RG_VS_LEGEND);\n        break;\n') + s[j:]
    open(p, 'w').write(s)


# ---------------------------------------------------------------- wilde Pokemon (post-game: baby 55-60, basis 60-70,
# midden 70-80, eind 80-90; 12 unieke soorten)
WILD = (20, [('CUBCHOO', 62, 66), ('SNOVER', 62, 66), ('SNOM', 60, 64), ('PHANTUMP', 62, 66), ('DEERLING', 64, 68),
             ('PILOSWINE', 72, 76), ('WYRDEER', 82, 85), ('CETITAN', 82, 85), ('TREVENANT', 83, 86),
             ('FROSMOTH', 83, 86), ('SMOOCHUM', 55, 58), ('SPIRITOMB', 86, 88)])


def wild():
    p = 'src/data/wild_encounters.json'
    s = open(p).read()
    rate, spec = WILD
    assert len(spec) == 12 and len({x[0] for x in spec}) == 12
    e = {'map': 'MAP_' + CONST, 'base_label': 'gCrownTundra',
         'land_mons': {'encounter_rate': rate,
                       'mons': [{'min_level': a, 'max_level': b, 'species': 'SPECIES_' + sp} for sp, a, b in spec]}}
    blob = '\n'.join('        ' + ln for ln in json.dumps(e, indent=2).split('\n'))
    key = '"map": "MAP_%s"' % CONST
    if key in s:
        i = s.index(key); a = s.rindex('{', 0, i)
    else:
        i = s.rindex('"map": "MAP_'); a = s.rindex('{', 0, i)
    depth, j = 0, a
    while True:
        if s[j] == '{': depth += 1
        elif s[j] == '}':
            depth -= 1
            if depth == 0: break
        j += 1
    if key in s:
        s = s[:a] + blob.lstrip() + s[j + 1:]
    else:
        s = s[:j + 1] + ',\n' + blob + s[j + 1:]
    d = json.loads(s)
    assert any(x.get('map') == 'MAP_' + CONST for x in d['wild_encounter_groups'][0]['encounters'])
    open(p, 'w').write(s)


# ---------------------------------------------------------------- Route 136: de ingang
def route136():
    g = read_layout('Route136')
    gx, gy = R136_GROTTO_MOUTH
    src = [[g[gy + j][gx + i] for i in range(3)] for j in range(2)]     # front a/b/c + cave l/door/r
    x0, y0 = R136_DOOR[0] - 1, R136_DOOR[1] - 1
    N = sl.N
    assert all((g[y0 + j][x0 + i] & 0x3ff) == N['cliff_b'] for i in range(3) for j in range(2)), \
        'Route 136: de plek voor de grotopening is geen rechte klifwand meer'
    assert (g[R136_DOOR[1] + 1][R136_DOOR[0]] >> 10) & 3 == 0, 'Route 136: onder de opening ligt geen vrije tegel'
    p = 'data/maps/Route136/map.json'
    mj = json.load(open(p))
    dest = 'MAP_' + CONST
    idx = [i for i, w in enumerate(mj['warp_events']) if w['dest_map'] == dest]
    wd = {'x': R136_DOOR[0], 'y': R136_DOOR[1], 'elevation': 0, 'dest_map': dest, 'dest_warp_id': '0'}
    if idx:
        mj['warp_events'][idx[0]] = wd; widx = idx[0]
    else:
        mj['warp_events'].append(wd); widx = len(mj['warp_events']) - 1
    open(p, 'w').write(json.dumps(mj, indent=2, ensure_ascii=False) + '\n')
    # ON_LOAD: de opening openen na het National Park
    p = 'data/maps/Route136/scripts.inc'
    s = open(p).read()
    line = '\tmap_script MAP_SCRIPT_ON_LOAD, Route136_OnLoad\n'
    if line not in s:
        a = '\tmap_script MAP_SCRIPT_ON_TRANSITION, Route136_OnTransition\n'
        assert a in s
        s = s.replace(a, a + line, 1)
    code = '@ calyrex { (gegenereerd door tools/grounded/maptools/calyrex_quest.py)\n' \
           'Route136_OnLoad:\n\tgoto_if_unset FLAG_NATIONAL_PARK_DONE, Route136_OnLoadEnd\n'
    for j in range(2):
        for i in range(3):
            v = src[j][i]
            code += '\tsetmetatile %d, %d, 0x%03X, %s\n' % (x0 + i, y0 + j, v & 0x3ff, 'TRUE' if (v >> 10) & 3 else 'FALSE')
    code += 'Route136_OnLoadEnd:\n\tend\n@ }\n'
    if '@ calyrex {' in s:
        i = s.index('@ calyrex {'); j = s.index('@ }\n', i) + 4
        s = s[:i] + code + s[j:]
    else:
        s = s.rstrip('\n') + '\n\n' + code
    open(p, 'w').write(s)
    return widx


# ---------------------------------------------------------------- map.json + scripts
def obj(gfx, x, y, script, flag='0', move='MOVEMENT_TYPE_FACE_DOWN', lid=None, item=None, elev=3):
    o = {'graphics_id': gfx, 'x': x, 'y': y, 'elevation': elev, 'movement_type': move, 'movement_range_x': 0,
         'movement_range_y': 0, 'trainer_type': 'TRAINER_TYPE_NONE', 'trainer_sight_or_berry_tree_id': item or '0',
         'script': script, 'flag': flag}
    return dict(local_id=lid, **o) if lid else o


def text(label, s):
    out = '%s:\n' % label
    for part in dimp.to_strings(s):
        out += '\t.string "%s"\n' % part
    return out + '\n'


P = NAME + '_EventScript_'
T = NAME + '_Text_'
LID = {k: 'LOCALID_CROWN_TUNDRA_' + k for k in ('CALYREX', 'GLASTRIER', 'SPECTRIER')}


def steed_script(sp, flag_me):
    """Jordi: alle Pokémon zijn beschikbaar, dus beide paarden zijn te vangen (geen keuze zoals in Crown Tundra)."""
    s = sp.title()
    return f'''{P}{s}::
	lock
	faceplayer
	playmoncry SPECIES_{sp}, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox {T}{s}Look, MSGBOX_DEFAULT
	msgbox {T}{s}Battle, MSGBOX_DEFAULT
	closemessage
	setwildbattle SPECIES_{sp}, {STEED_LEVEL}
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {P}{s}Later
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {P}{s}Later
	removeobject {LID[sp]}
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, {P}{s}Caught
	msgbox {T}{s}Fled, MSGBOX_DEFAULT
	release
	end

{P}{s}Caught:
	setflag {flag_me}
	setflag FLAG_CROWN_STEED_DONE
	msgbox {T}{s}Caught, MSGBOX_DEFAULT
	release
	end

{P}{s}Later:
	release
	end
'''


CODE = f'''{P}OnTransition:
	setflag FLAG_TEMP_1
	setflag FLAG_TEMP_2
	setflag FLAG_TEMP_3
	goto_if_unset FLAG_NATIONAL_PARK_DONE, {P}OnTransitionEnd
	call_if_unset FLAG_CROWN_CALYREX_DONE, {P}ShowCalyrex
	goto_if_unset FLAG_CROWN_QUEST_STARTED, {P}OnTransitionEnd
	call_if_unset FLAG_CROWN_CHOSE_GLASTRIER, {P}ShowGlastrier
	call_if_unset FLAG_CROWN_CHOSE_SPECTRIER, {P}ShowSpectrier
{P}OnTransitionEnd:
	end

{P}ShowCalyrex:
	clearflag FLAG_TEMP_1
	return

{P}ShowGlastrier:
	clearflag FLAG_TEMP_2
	return

{P}ShowSpectrier:
	clearflag FLAG_TEMP_3
	return

{P}Calyrex::
	lock
	faceplayer
	playmoncry SPECIES_CALYREX, CRY_MODE_NORMAL
	waitmoncry
	goto_if_set FLAG_CROWN_STEED_DONE, {P}CalyrexReins
	goto_if_set FLAG_CROWN_QUEST_STARTED, {P}CalyrexWaiting
	msgbox {T}CalyrexIntro, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_CROWN_QUEST_STARTED
	clearflag FLAG_TEMP_2
	clearflag FLAG_TEMP_3
	addobject {LID['GLASTRIER']}
	addobject {LID['SPECTRIER']}
	playmoncry SPECIES_GLASTRIER, CRY_MODE_NORMAL
	waitmoncry
	playmoncry SPECIES_SPECTRIER, CRY_MODE_NORMAL
	waitmoncry
	msgbox {T}CalyrexTask, MSGBOX_DEFAULT
	release
	end

{P}CalyrexWaiting:
	msgbox {T}CalyrexWaiting, MSGBOX_DEFAULT
	release
	end

{P}CalyrexReins:
	goto_if_set FLAG_RECEIVED_REINS_OF_UNITY, {P}CalyrexBattle
	msgbox {T}CalyrexReunited, MSGBOX_DEFAULT
	giveitem ITEM_REINS_OF_UNITY
	setflag FLAG_RECEIVED_REINS_OF_UNITY
{P}CalyrexBattle:
	msgbox {T}CalyrexChallenge, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_CALYREX, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_CALYREX, {CALYREX_LEVEL}
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, {P}CalyrexCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, {P}CalyrexDefeated
	release
	end

{P}CalyrexDefeated:
	msgbox {T}CalyrexDefeated, MSGBOX_DEFAULT
	release
	end

{P}CalyrexCaught:
	removeobject {LID['CALYREX']}
	setflag FLAG_CROWN_CALYREX_DONE
	msgbox {T}CalyrexCaught, MSGBOX_DEFAULT
	release
	end

{P}Altar::
	msgbox {T}Altar, MSGBOX_SIGN
	end

''' + steed_script('GLASTRIER', 'FLAG_CROWN_CHOSE_GLASTRIER') + '\n' + steed_script('SPECTRIER', 'FLAG_CROWN_CHOSE_SPECTRIER')

TEXTS = [
    ('Altar', "A crumbling shrine, half buried in snow. Carved into the stone: a crowned head and two horses, one of "
              "which is clearly being difficult.\n\nSomeone left a carrot on the altar. It is frozen solid. It has "
              "been here longer than you have been alive."),
    ('CalyrexIntro', "CALYREX: Ah. The trainer from the park. You found my shrine. It used to be grander. It used to "
                     "have a roof.\n\nI have a task for you, which you will accept, because I am a king and you are "
                     "a person holding a bicycle.\n\nMy steeds have wandered off. GLASTRIER, who is strong and "
                     "stubborn, and SPECTRIER, who is fast and afraid of everything. Including me. Especially me."),
    ('CalyrexTask', "CALYREX: A king rides one horse at a time. That is a rule. Owning two is not against the "
                    "rule. I checked. I wrote it.\n\nGo into the field and bring me my steeds. One will do for "
                    "the REINS. Both would be greedy. You look greedy."),
    ('CalyrexWaiting', "CALYREX: The big one sulks on the ice to the west. The nervous one hides between the dark "
                       "trees. I would fetch them myself, but I am very small and very royal."),
    ('CalyrexReunited', "CALYREX: You caught my steed. In a ball. With my steed inside it. I see.\n\nNo matter. Take "
                        "these REINS OF UNITY. With them, my steed and I become one. It is very majestic and only "
                        "slightly uncomfortable for the horse."),
    ('CalyrexChallenge', "CALYREX: Reins are useless without a king attached. Show me you are worthy of carrying "
                         "one around in your pocket.\n\nI will not go easy on you. I have been in a ball before, "
                         "in another dimension. It was humbling. I did not enjoy being humbled."),
    ('CalyrexDefeated', "CALYREX picks itself up and straightens its crown.\n\nCALYREX: That did not happen. We will "
                        "do it again, whenever you are ready. I can wait. Waiting is mostly what kings do."),
    ('CalyrexCaught', "You caught CALYREX! Use the REINS OF UNITY from your bag while CALYREX and its steed are both "
                      "in your party.\n\nFrom inside the ball, faintly: “This is beneath me. Literally. You put the "
                      "ball on the floor.”"),
    ('GlastrierLook', "A massive white horse made mostly of muscle and ice stares you down. It snorts. Somewhere, a "
                      "small avalanche happens.\n\nCALYREX (in your head): That is GLASTRIER. Strong. Stubborn. Has "
                      "never once listened to me."),
    ('GlastrierBattle', "GLASTRIER lowers its head. That is not a bow."),
    ('GlastrierCaught', "You caught GLASTRIER!\n\nCALYREX: Bring it to the shrine. Gently. It bites."),
    ('GlastrierFled', "GLASTRIER stomps off into the snow, humiliated. It will be back: it left its dignity here and "
                      "it wants it back."),
    ('SpectrierLook', "A thin black horse flickers between the trees, half here and half somewhere worse. It looks "
                      "at you as if YOU are the ghost.\n\nCALYREX (in your head): That is SPECTRIER. Fast. Shy. Once "
                      "fled from its own shadow, and then from the shadow of its shadow."),
    ('SpectrierBattle', "SPECTRIER panics. Panicking is how it fights."),
    ('SpectrierCaught', "You caught SPECTRIER!\n\nCALYREX: Bring it to the shrine. Quietly. Loud noises make it phase "
                        "through the floor."),
    ('SpectrierFled', "SPECTRIER dissolves in fright. It will come back. It always comes back. Usually right behind "
                      "you."),
]


def write_map_files(r136_idx):
    its = ni.items(NAME)
    balls = [(fl, it) for fl, it, q, h in its if not h]
    hids = [(fl, it) for fl, it, q, h in its if h]
    assert len(balls) == 2 and len(hids) == 1, its
    objs = [
        obj('OBJ_EVENT_GFX_SPECIES(CALYREX)', CALYREX[0], CALYREX[1], P + 'Calyrex', 'FLAG_TEMP_1', lid=LID['CALYREX']),
        obj('OBJ_EVENT_GFX_SPECIES(GLASTRIER)', GLASTRIER[0], GLASTRIER[1], P + 'Glastrier', 'FLAG_TEMP_2',
            lid=LID['GLASTRIER'], move='MOVEMENT_TYPE_FACE_RIGHT'),
        obj('OBJ_EVENT_GFX_SPECIES(SPECTRIER)', SPECTRIER[0], SPECTRIER[1], P + 'Spectrier', 'FLAG_TEMP_3',
            lid=LID['SPECTRIER'], move='MOVEMENT_TYPE_LOOK_AROUND'),
        obj('OBJ_EVENT_GFX_ITEM_BALL', ITEMS_XY['ice'][0], ITEMS_XY['ice'][1], 'Common_EventScript_FindItem', balls[0][0],
            'MOVEMENT_TYPE_LOOK_AROUND', item=balls[0][1]),
        obj('OBJ_EVENT_GFX_ITEM_BALL', ITEMS_XY['ghost'][0], ITEMS_XY['ghost'][1], 'Common_EventScript_FindItem',
            balls[1][0], 'MOVEMENT_TYPE_LOOK_AROUND', item=balls[1][1]),
    ]
    warps = [{'x': AX, 'y': 5, 'elevation': 0, 'dest_map': 'MAP_ROUTE136', 'dest_warp_id': str(r136_idx)}]
    bgs = [{'type': 'sign', 'x': SIGN[0], 'y': SIGN[1], 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_NORTH',
            'script': P + 'Altar'},
           {'type': 'hidden_item', 'x': ITEMS_XY['hidden'][0], 'y': ITEMS_XY['hidden'][1], 'elevation': 3,
            'item': hids[0][1], 'flag': hids[0][0]}]
    mj = {'id': 'MAP_' + CONST, 'name': NAME, 'layout': 'LAYOUT_' + CONST, 'music': 'MUS_RG_SEVII_ROUTE',
          'region_map_section': 'MAPSEC_CROWN_TUNDRA', 'requires_flash': False, 'weather': 'WEATHER_SNOW',
          'map_type': 'MAP_TYPE_ROUTE', 'allow_cycling': True, 'allow_escaping': False, 'allow_running': True,
          'show_map_name': True, 'battle_scene': 'MAP_BATTLE_SCENE_NORMAL', 'connections': None,
          'object_events': objs, 'warp_events': warps, 'coord_events': [], 'bg_events': bgs}
    os.makedirs('data/maps/' + NAME, exist_ok=True)
    open('data/maps/%s/map.json' % NAME, 'w').write(json.dumps(mj, indent=2, ensure_ascii=False) + '\n')
    s = ('@ Project Grounded: %s (gegenereerd door tools/grounded/maptools/calyrex_quest.py; niet met de hand bewerken, '
         'teksten via de Dialoogstudio)\n%s_MapScripts::\n\tmap_script MAP_SCRIPT_ON_TRANSITION, %sOnTransition\n'
         '\t.byte 0\n\n' % (NAME, NAME, P)) + CODE.strip('\n') + '\n\n@ ' + '-' * 64 + \
        ' teksten (placeholders, Jordi herschrijft ze)\n' + ''.join(text(T + k, v) for k, v in TEXTS)
    open('data/maps/%s/scripts.inc' % NAME, 'w').write(s.rstrip('\n') + '\n')


ITEMS_XY = {'ice': (4, 22), 'ghost': (34, 28), 'hidden': (21, 6)}


def main():
    flags()
    mapsec()
    battle_setup()
    wild()
    m = build(ITEMS_XY)
    save_layout(m)
    widx = route136()
    write_map_files(widx)
    register_map()
    print('%s: aankomst/terugweg = warp 0 (%d,5) -> Route 136 warp %d op %s' % (NAME, AX, widx, R136_DOOR))
    return m


def render(outdir):
    from gridrender import render as grender
    os.makedirs(outdir, exist_ok=True)
    grender(read_layout(NAME), 'general', 'snow', 1).save(os.path.join(outdir, NAME + '.png'))
    print('render:', outdir)


if __name__ == '__main__':
    main()
    if len(sys.argv) > 1:
        render(sys.argv[1])
