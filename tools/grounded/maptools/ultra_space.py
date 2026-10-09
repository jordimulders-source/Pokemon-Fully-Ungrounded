"""Project Grounded: Ultra Space (post-game), achterin Altering Cave (Route 103).

Een Ultra Wormhole (object, OBJ_EVENT_GFX_ULTRA_WORMHOLE) achterin Altering Cave leidt naar de hub
(UltraSpace_Hub): een zwevend eiland met het grote portaal. Het portaal kiest via special Ultra_PickPortal
(src/ultra_space.c) een willekeurige Ultra Beast-plek waarvan de UB nog niet gevangen is; Necrozma pas als alle
tien de anderen gehad zijn, daarna willekeurig uit alle elf. Op elke plek staat de UB als object (eenmalig,
FLAG_ULTRA_*) en een wormgat terug naar de hub. Poipole is geen gevecht: de aliens (Elgyem/Beheeyem) geven hem.

Plekken (elk één kaart: gang + arena, abstract en bizar; tiles van bestaande tilesets met eigen paletten, zie
TINTS: een palet-tileset kost 512 bytes, de tiles/metatiles komen van de basistileset):
- Nihilego: glazen droomwereld (Sootopolis Gym, pastel glas, kwallen die door de lucht zweven)
- Buzzwole: sportschool (Dewford Gym, rood; Machamp & co. die gewichten heffen)
- Pheromosa: catwalk (Lilycove Contest Hall, wit; publiek en een jury)
- Xurkitree: woud van stroomkabels (New Mauville, nachtblauw met neon)
- Celesteela: lanceerveld in het niets (Meteor Space; rijen Celesteela die zichzelf afvuren, Koffing als rook)
- Kartana: wereld van papier (Trick House, papierwit)
- Guzzlord: eindeloze afvalvlakte (Meteor Space, bruin; Trubbish/Garbodor, puin)
- Poipole: gifkristallen met aliens (Granite Cave, paars/gifgroen)
- Stakataka: een muur die naar je kijkt (Desert Ruins, grijs; een muur van Stakataka)
- Blacephalon: circus (Battle Dome, rood/geel; clowns)
- Necrozma: donkere prismagrot (Meteor Space, zwart met prismakleuren)

Meteor Space-kaarten worden uit een masker (vloer/leegte) opgebouwd met een autotiler die per cel een metatile
kiest uit MeteorSpace met dezelfde omgeving (3 breed, 2 boven en 1 onder), zodat randen en klifwanden kloppen.

Schrijft: palet-tilesets (data/tilesets/*/ultra_*), blokken in src/data/tilesets/graphics.h en headers.h,
layouts (data/layouts/UltraSpace_*), layouts.json, map.json's, map_groups.json (gMapGroup_UltraSpace),
event_scripts.s, de wormhole in Altering Cave (map.json + scripts.inc) en scripts.inc per kaart (alleen als hij
nog niet bestaat: Jordi bewerkt teksten in de Dialoogstudio; --scripts schrijft ze opnieuw).
Controleert de bereikbaarheid van UB's, portalen, NPC's en items.

Gebruik: python3 tools/grounded/maptools/ultra_space.py [--scripts] [--render <map>]"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
_sys.path.append(_os.path.dirname(_os.path.abspath(__file__)))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
import json, os, random, re, struct, subprocess, sys  # noqa: E401,E402
from collections import deque, Counter  # noqa: E402
import nieuwe_items as ni  # noqa: E402
import importlib.util  # noqa: E402

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
os.chdir(REPO)
FORCE_SCRIPTS = '--scripts' in sys.argv
_spec = importlib.util.spec_from_file_location('dialogen_import', 'tools/dialogen/import.py')
dimp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dimp)
LAYOUTS = {l['name']: l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if 'name' in l}
GROUP = 'gMapGroup_UltraSpace'
MAPSEC = 'MAPSEC_ALTERING_CAVE'


def ts_dir(sym):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', sym.replace('gTileset_', '')).lower()


def load(n):
    l = LAYOUTS[n + '_Layout']
    W = l['width']
    v = list(struct.unpack('<%dH' % (W * l['height']), open(l['blockdata_filepath'], 'rb').read()))
    return [v[y * W:(y + 1) * W] for y in range(l['height'])], l


def write_json(path, d):
    open(path, 'w').write(json.dumps(d, indent=2, ensure_ascii=False) + '\n')


# ====================================================================== paletten (tint)
def lum(c):
    r, g, b = c
    return (0.30 * r + 0.59 * g + 0.11 * b) / 248.0


def grad(stops, t):
    t = min(1.0, max(0.0, t)) * (len(stops) - 1)
    i = min(int(t), len(stops) - 2)
    f = t - i
    a, b = stops[i], stops[i + 1]
    return tuple(a[k] + (b[k] - a[k]) * f for k in range(3))


def make_tint(stops, keep=0.2, gamma=1.0):
    def fn(c):
        g = grad(stops, lum(c) ** gamma)
        return tuple(max(0, min(248, int(g[k] * (1 - keep) + c[k] * keep)) // 8 * 8) for k in range(3))
    return fn


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().split('\n')[3:19]]


TILESETS = []   # (symbool, basissymbool, isSecondary, map)


def pal_tileset(base_sym, key, fn):
    """Palet-tileset gTileset_Ultra<key> met de tiles/metatiles van base_sym en eigen (getinte) paletten."""
    secondary = base_sym not in ('gTileset_General', 'gTileset_Building')
    sym = 'gTileset_Ultra' + key
    kind = 'secondary' if secondary else 'primary'
    src = 'data/tilesets/%s/%s' % (kind, ts_dir(base_sym))
    dst = 'data/tilesets/%s/%s' % (kind, ts_dir(sym))
    os.makedirs(dst + '/palettes', exist_ok=True)
    open(dst + '/BASE', 'w').write(ts_dir(base_sym) + '\n')
    for i in range(16):
        cols = [fn(c) for c in read_pal('%s/palettes/%02d.pal' % (src, i))]
        with open('%s/palettes/%02d.pal' % (dst, i), 'w', newline='\r\n') as fp:
            fp.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % c for c in cols))
    if not any(t[0] == sym for t in TILESETS):
        TILESETS.append((sym, base_sym, secondary, dst))
    return sym


def write_tileset_blocks():
    hdr = open('src/data/tilesets/headers.h').read()
    gfx_blk = ['// ultra_space { (tools/grounded/maptools/ultra_space.py: palet-tilesets van Ultra Space)']
    hdr_blk = ['// ultra_space { (tools/grounded/maptools/ultra_space.py: Ultra Space, tiles/metatiles van de basistileset met eigen paletten)']
    for sym, base, secondary, dst in TILESETS:
        pal = 'gTilesetPalettes_' + sym.replace('gTileset_', '')
        gfx_blk.append('const u16 %s[][16] =\n{' % pal)
        gfx_blk += ['    INCBIN_U16("%s/palettes/%02d.gbapal"),' % (dst, i) for i in range(16)]
        gfx_blk.append('};\n')
        body = re.search(r'const struct Tileset ' + base + r' =[^{]*\{(.*?)\};', hdr, re.S).group(1)
        body = re.sub(r'\.palettes = \w+', '.palettes = ' + pal, body)
        hdr_blk.append('const struct Tileset %s =\n{%s};\n' % (sym, body))
    gfx_blk.append('// }')
    hdr_blk.append('// }')
    for path, blk in (('src/data/tilesets/graphics.h', gfx_blk), ('src/data/tilesets/headers.h', hdr_blk)):
        s = open(path).read()
        if '// ultra_space {' in s:
            i = s.index('// ultra_space {')
            j = s.index('// }', i) + 4
            s = s[:i] + '\n'.join(blk) + s[j:]
        else:
            s = s.rstrip('\n') + '\n\n' + '\n'.join(blk) + '\n'
        open(path, 'w').write(s)


# ====================================================================== autotiler voor Meteor Space-kaarten
MS, _ = load('MeteorSpace')
MSH, MSW = len(MS), len(MS[0])


def ms_ground(x, y):
    return 0 <= x < MSW and 0 <= y < MSH and not (MS[y][x] >> 10) & 3


WIN = [(dx, dy) for dy in (-2, -1, 0, 1) for dx in (-1, 0, 1)]


def sig(gr, x, y):
    return tuple(1 if gr(x + dx, y + dy) else 0 for dx, dy in WIN)


EXAMPLES = {}
_cnt = Counter(v & 0x3ff for r in MS for v in r)
for y in range(MSH):
    for x in range(MSW):
        EXAMPLES.setdefault(sig(ms_ground, x, y), []).append(MS[y][x])
STARS = [v for v in EXAMPLES[(0,) * len(WIN)] if _cnt[v & 0x3ff] >= 20]
WEIGHT = [1, 1, 1, 2, 3, 2, 3, 6, 3, 1, 2, 1]   # center telt het zwaarst, dan de rij erboven


def autotile(mask, seed):
    """mask: lijst van strings, '#'/' ' = leegte, al het andere = vloer."""
    H, W = len(mask), len(mask[0])
    rnd = random.Random(seed)

    def gr(x, y):
        return 0 <= x < W and 0 <= y < H and mask[y][x] not in '# '
    out = [[0] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            s = sig(gr, x, y)
            if s == (0,) * len(WIN):
                out[y][x] = rnd.choice(STARS)
                continue
            cands = EXAMPLES.get(s)
            if not cands:
                best = max(EXAMPLES, key=lambda k: sum(w for a, b, w in zip(k, s, WEIGHT) if a == b) if k[7] == s[7] else -1)
                cands = EXAMPLES[best]
            c = Counter(cands)
            top = c.most_common(1)[0][0]
            out[y][x] = top if rnd.random() < 0.8 or not gr(x, y) else rnd.choice(cands)
            if gr(x, y):
                out[y][x] = (out[y][x] & 0x3ff) | (3 << 12)        # vloer: altijd begaanbaar, hoogte 3
            else:
                out[y][x] = (out[y][x] & 0x3ff) | (1 << 10) | (3 << 12)
    return out


# ====================================================================== bereikbaarheid
def reachable(g, start, blocked=()):
    H, W = len(g), len(g[0])
    seen = {start}
    q = deque([start])
    while q:
        x, y = q.popleft()
        e0 = g[y][x] >> 12
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < W and 0 <= ny < H) or (nx, ny) in seen or (nx, ny) in blocked:
                continue
            v = g[ny][nx]
            e = v >> 12
            if (v >> 10) & 3 or not (e == e0 or e in (0, 15) or e0 in (0, 15)):
                continue
            seen.add((nx, ny))
            q.append((nx, ny))
    return seen


def next_to(r, x, y):
    return any((x + dx, y + dy) in r for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))


# ====================================================================== registratie
def save_layout(name, g, border, prim, sec):
    os.makedirs('data/layouts/' + name, exist_ok=True)
    open('data/layouts/%s/map.bin' % name, 'wb').write(b''.join(struct.pack('<H', t) for r in g for t in r))
    open('data/layouts/%s/border.bin' % name, 'wb').write(struct.pack('<4H', *border))
    lj = open('data/layouts/layouts.json').read()
    const = 'LAYOUT_' + re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', name).upper()
    entry = '''    {
      "id": "%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "%s",
      "secondary_tileset": "%s",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    }''' % (const, name, len(g[0]), len(g), prim, sec, name, name)
    m = re.search(r'    \{\n      "id": "%s",.*?\n    \}' % const, lj, re.S)
    if m:
        lj = lj[:m.start()] + entry + lj[m.end():]
    else:
        i = lj.rindex('    }\n  ]')
        lj = lj[:i + 5] + ',\n' + entry + lj[i + 5:]
    open('data/layouts/layouts.json', 'w').write(lj)
    return const


def add_to_group(name):
    g = open('data/maps/map_groups.json').read()
    if '"%s"' % GROUP not in g:
        last = re.findall(r'\n    "(gMapGroup_\w+)"\n  \],', g)[0]
        g = g.replace('\n    "%s"\n  ],' % last, '\n    "%s",\n    "%s"\n  ],' % (last, GROUP), 1)
        i = g.rindex('\n  ]\n}')
        g = g[:i] + '\n  ],\n  "%s": [\n  ]\n}' % GROUP + g[i + 6:]
    if '"%s"' % name not in g:
        i = g.index('"%s": [' % GROUP)
        j = g.index('\n  ]', i)
        body = g[i:j]
        if body.endswith('['):
            g = g[:j] + '\n    "%s"' % name + g[j:]
        else:
            g = g[:j] + ',\n    "%s"' % name + g[j:]
    open('data/maps/map_groups.json', 'w').write(g)
    json.loads(g)


def add_include(name):
    es = open('data/event_scripts.s').read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        a = '\t.include "data/maps/AlteringCave/scripts.inc"\n'
        last = re.findall(r'\t\.include "data/maps/UltraSpace_\w+/scripts\.inc"\n', es)
        a = last[-1] if last else a
        es = es.replace(a, a + inc, 1)
        open('data/event_scripts.s', 'w').write(es)


def map_const(name):
    return 'MAP_' + re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', name).upper()


def obj(lid, gfx, x, y, script, flag='0', move='MOVEMENT_TYPE_FACE_DOWN', sight='0', rx=0, elev=3):
    o = {'graphics_id': gfx, 'x': x, 'y': y, 'elevation': elev, 'movement_type': move,
         'movement_range_x': rx, 'movement_range_y': 0, 'trainer_type': 'TRAINER_TYPE_NONE',
         'trainer_sight_or_berry_tree_id': sight, 'script': script, 'flag': flag}
    if lid:
        o = dict(local_id=lid, **o)
    return o


def map_json(name, layout_const, music, objs, bgs, weather='WEATHER_NONE', mtype='MAP_TYPE_UNDERGROUND'):
    return {'id': map_const(name), 'name': name, 'layout': layout_const, 'music': music,
            'region_map_section': MAPSEC, 'requires_flash': False, 'weather': weather,
            'map_type': mtype, 'allow_cycling': False, 'allow_escaping': False,
            'allow_running': True, 'show_map_name': False, 'battle_scene': 'MAP_BATTLE_SCENE_NORMAL',
            'connections': None, 'object_events': objs, 'warp_events': [], 'coord_events': [], 'bg_events': bgs}


# ====================================================================== Ultra Beast-plekken
# key, soort, level, transitie (battle_setup.c), basis, tint, ...
WORM = 'OBJ_EVENT_GFX_ULTRA_WORMHOLE'
GFX = 'OBJ_EVENT_GFX_SPECIES(%s)'


def mon(sp):
    return GFX % sp


SPOTS = []   # volgorde = index in src/ultra_space.c (sUltraFlags)
# Opnieuw gebouwd in een eigen script met een eigen tileset (Jordi, 9 okt: "schrap alles"): deze plekken worden hier
# overgeslagen (alleen de hub-warp blijft); kaart, tileset en scripts maakt tools/grounded/maptools/ultra_worlds_a.py.
REBUILT = {'Nihilego', 'Buzzwole', 'Pheromosa', 'Xurkitree', 'Celesteela', 'Kartana'}


def spot(**k):
    SPOTS.append(k)


# Hub en Meteor Space-maskers ('.' vloer, '#' leegte, letters = plekken die het script gebruikt)
HUB_MASK = [
    '##########################',
    '##########################',
    '##########################',
    '##########.....###########',
    '#########.......##########',
    '#########...P...##########',
    '#########.......##########',
    '##########.....###########',
    '###########...############',
    '###########...######...###',
    '####...####...#####.....##',
    '###.....##.....###......##',
    '###.....#.......#.......##',
    '####....................##',
    '#####.................####',
    '##########.......#########',
    '##########...R...#########',
    '##########...A...#########',
    '###########.....##########',
    '##########################',
    '##########################',
    '##########################',
]

CELESTEELA_MASK = [
    '##################################',
    '##################################',
    '##################################',
    '####...........................###',
    '###.............................##',
    '###.............................##',
    '###.............................##',
    '###.............................##',
    '###.............................##',
    '###..............U..............##',
    '###.............................##',
    '####...........................###',
    '##############.....###############',
    '###############...################',
    '###############...################',
    '###############...################',
    '##############.....###############',
    '##############..R..###############',
    '##############..A..###############',
    '###############...################',
    '##################################',
    '##################################',
]

GUZZLORD_MASK = [
    '####################################',
    '####################################',
    '####################################',
    '#####.........######################',
    '####............####......##########',
    '###..............####.......########',
    '###...............##.........#######',
    '###.......U..................#######',
    '####........................########',
    '#####.....................##########',
    '#######.......####......############',
    '#########....######....#############',
    '#########...########...#############',
    '########....#######.....############',
    '#######......#####.......###########',
    '######..R.....###.........##########',
    '######..A.......###......###########',
    '#######......###########.###########',
    '####################################',
    '####################################',
    '####################################',
]

NECROZMA_MASK = [
    '############################',
    '############################',
    '############################',
    '#########..........#########',
    '#######..............#######',
    '######................######',
    '#####..................#####',
    '#####........U.........#####',
    '#####..................#####',
    '######................######',
    '#######..............#######',
    '#########..........#########',
    '############....############',
    '#############..#############',
    '#############..#############',
    '############....############',
    '############.R..############',
    '############.A..############',
    '#############..#############',
    '############################',
    '############################',
    '############################',
]


def find(mask, ch):
    for y, r in enumerate(mask):
        if ch in r:
            return r.index(ch), y
    raise KeyError(ch)


def crop(name, x0, y0, w, h):
    g, l = load(name)
    return [r[x0:x0 + w] for r in g[y0:y0 + h]], l


spot(key='Nihilego', species='NIHILEGO', level=88, trans='B_TRANSITION_RIPPLE',
     src=('SootopolisCity_Gym_1F', 0, 0, 17, 26), arrive=(10, 23), ret=(10, 22), ub=(8, 2),
     tint=dict(prim=[(40, 20, 64), (150, 112, 200), (240, 192, 232), (224, 248, 255)], keep=0.3),
     music='MUS_RG_SEVII_CAVE',
     decor=[('FRILLISH', 3, 16, 'MOVEMENT_TYPE_WANDER_AROUND', 'Jelly'), ('JELLICENT', 14, 16, 'MOVEMENT_TYPE_WANDER_AROUND', 'Jelly'),
            ('NIHILEGO', 4, 7, 'MOVEMENT_TYPE_FACE_DOWN', 'Echo'), ('NIHILEGO', 12, 8, 'MOVEMENT_TYPE_FACE_DOWN', 'Echo')])
spot(key='Buzzwole', species='BUZZWOLE', level=88, trans='B_TRANSITION_ANGLED_WIPES',
     src=('DewfordTown_Gym', 0, 0, 18, 28), arrive=(6, 26), ret=(6, 25), ub=(10, 4),
     tint=dict(prim=[(32, 8, 8), (152, 32, 24), (240, 144, 64), (255, 232, 184)], keep=0.25),
     music='MUS_GYM',
     decor=[('MACHAMP', 9, 13, 'MOVEMENT_TYPE_WALK_IN_PLACE_DOWN', 'Lifter'),
            ('CONKELDURR', 12, 21, 'MOVEMENT_TYPE_WALK_IN_PLACE_DOWN', 'Lifter'),
            ('HARIYAMA', 2, 16, 'MOVEMENT_TYPE_WALK_IN_PLACE_DOWN', 'Lifter')])
spot(key='Pheromosa', species='PHEROMOSA', level=88, trans='B_TRANSITION_WHITE_BARS_FADE',
     src=('LilycoveCity_ContestHall', 5, 4, 42, 29), arrive=(21, 26), ret=(21, 25), ub=(19, 7),
     tint=dict(prim=[(48, 40, 64), (176, 168, 192), (248, 240, 248), (255, 255, 255)], keep=0.3),
     music='MUS_CONTEST_LOBBY',
     decor=[('GARDEVOIR', 12, 9, 'MOVEMENT_TYPE_FACE_RIGHT', 'Judge'), ('DELCATTY', 28, 9, 'MOVEMENT_TYPE_FACE_LEFT', 'Judge'),
            ('MR_MIME', 3, 20, 'MOVEMENT_TYPE_FACE_UP', 'Crowd'), ('KIRLIA', 37, 20, 'MOVEMENT_TYPE_FACE_UP', 'Crowd'),
            ('LOPUNNY', 20, 14, 'MOVEMENT_TYPE_FACE_UP', 'Crowd')])
spot(key='Xurkitree', species='XURKITREE', level=89, trans='B_TRANSITION_SHRED_SPLIT',
     src=('NewMauville_Inside', 0, 0, 41, 22), arrive=(2, 8), ret=(2, 7), ub=(33, 5),
     tint=dict(prim=[(4, 4, 24), (16, 24, 80), (48, 160, 216), (248, 248, 120)], keep=0.1, gamma=1.8),
     music='MUS_ABANDONED_SHIP',
     decor=[('JOLTIK', 6, 11, 'MOVEMENT_TYPE_WANDER_AROUND', 'Spark'), ('TYNAMO', 16, 17, 'MOVEMENT_TYPE_WANDER_AROUND', 'Spark'),
            ('XURKITREE', 18, 15, 'MOVEMENT_TYPE_FACE_DOWN', 'Cable')])
spot(key='Celesteela', species='CELESTEELA', level=90, trans='B_TRANSITION_SLICE',
     mask=CELESTEELA_MASK, seed=797,
     tint=dict(sec=[(8, 16, 32), (64, 104, 96), (200, 200, 184), (255, 232, 176)], keep=0.15, gamma=0.6),
     music='MUS_RG_SPACE_DOOR' if False else 'MUS_ROUTE104',
     decor=[('CELESTEELA', x, y, mv, 'Rocket') for x, y, mv in (
         (6, 5, 'MOVEMENT_TYPE_RUN_IN_PLACE_UP'), (11, 5, 'MOVEMENT_TYPE_FACE_DOWN'), (16, 5, 'MOVEMENT_TYPE_RUN_IN_PLACE_UP'),
         (22, 5, 'MOVEMENT_TYPE_FACE_DOWN'), (27, 5, 'MOVEMENT_TYPE_RUN_IN_PLACE_UP'), (6, 9, 'MOVEMENT_TYPE_FACE_DOWN'),
         (27, 9, 'MOVEMENT_TYPE_RUN_IN_PLACE_UP'), (11, 9, 'MOVEMENT_TYPE_RUN_IN_PLACE_UP'), (22, 9, 'MOVEMENT_TYPE_FACE_DOWN'))]
     + [('KOFFING', 6, 6, 'MOVEMENT_TYPE_FACE_DOWN', 'Smoke'), ('KOFFING', 16, 6, 'MOVEMENT_TYPE_FACE_DOWN', 'Smoke'),
        ('WEEZING', 27, 6, 'MOVEMENT_TYPE_FACE_DOWN', 'Smoke')])
spot(key='Kartana', species='KARTANA', level=89, trans='B_TRANSITION_GRID_SQUARES',
     src=('Route110_TrickHousePuzzle1', 0, 0, 15, 22), arrive=(1, 20), ret=(1, 19), ub=None,
     tint=dict(prim=[(64, 56, 48), (184, 176, 168), (248, 240, 224), (255, 255, 248)], keep=0.05),
     music='MUS_RG_TRAINER_TOWER' if False else 'MUS_TRICK_HOUSE',
     decor=[('KARTANA', 7, 4, 'MOVEMENT_TYPE_FACE_DOWN', 'Fold'), ('KARTANA', 3, 12, 'MOVEMENT_TYPE_FACE_RIGHT', 'Fold')])
spot(key='Guzzlord', species='GUZZLORD', level=90, trans='B_TRANSITION_BLACKHOLE',
     mask=GUZZLORD_MASK, seed=799,
     tint=dict(sec=[(16, 8, 16), (72, 40, 40), (144, 112, 64), (216, 200, 136)], keep=0.15, gamma=0.7),
     music='MUS_RG_POKE_MANSION' if False else 'MUS_ABANDONED_SHIP',
     decor=[('TRUBBISH', 5, 5, 'MOVEMENT_TYPE_WANDER_AROUND', 'Trash'), ('GARBODOR', 23, 6, 'MOVEMENT_TYPE_FACE_DOWN', 'Trash'),
            ('MUK', 20, 15, 'MOVEMENT_TYPE_WANDER_AROUND', 'Trash'),
            (None, 13, 5, 'OBJ_EVENT_GFX_BREAKABLE_ROCK', 'Junk'), (None, 25, 8, 'OBJ_EVENT_GFX_BREAKABLE_ROCK', 'Junk'),
            (None, 10, 13, 'OBJ_EVENT_GFX_CUTTABLE_TREE', 'Junk')])
spot(key='Poipole', species='POIPOLE', level=85, trans=None,
     src=('GraniteCave_B2F', 0, 9, 32, 15), arrive=(8, 12), ret=(8, 11), ub=(25, 3),
     tint=dict(prim=[(16, 0, 24), (96, 24, 128), (184, 64, 224), (184, 255, 120)], keep=0.15),
     music='MUS_RG_SEVII_DUNGEON',
     decor=[])
spot(key='Stakataka', species='STAKATAKA', level=90, trans='B_TRANSITION_FRONTIER_SQUARES',
     src=('DesertRuins', 0, 2, 17, 11), arrive=(8, 9), ret=(8, 8), ub=(8, 1),
     tint=dict(prim=[(16, 16, 24), (80, 88, 96), (160, 168, 176), (232, 232, 224)], keep=0.2),
     music='MUS_SEALED_CHAMBER',
     decor=[('STAKATAKA', x, 1, 'MOVEMENT_TYPE_FACE_DOWN', 'Wall') for x in (4, 5, 6, 7, 9, 10, 11, 12)])
spot(key='Blacephalon', species='BLACEPHALON', level=90, trans='B_TRANSITION_FRONTIER_CIRCLES_SYMMETRIC_SPIRAL',
     src=('BattleFrontier_BattleDomeBattleRoom', 0, 0, 20, 10), arrive=(2, 8), ret=(2, 7), ub=(9, 6),
     tint=dict(prim=[(40, 0, 24), (184, 24, 48), (248, 184, 48), (255, 248, 224)], keep=0.35),
     music='MUS_GAME_CORNER',
     decor=[('MR_MIME', 6, 5, 'MOVEMENT_TYPE_WANDER_AROUND', 'Clown'), ('MIME_JR', 14, 7, 'MOVEMENT_TYPE_WANDER_AROUND', 'Clown'),
            ('SPOINK', 12, 4, 'MOVEMENT_TYPE_JOG_IN_PLACE_DOWN', 'Clown'), ('GRUMPIG', 16, 5, 'MOVEMENT_TYPE_FACE_LEFT', 'Clown')])
spot(key='Necrozma', species='NECROZMA', level=95, trans='B_TRANSITION_BLACKHOLE_PULSATE',
     mask=NECROZMA_MASK, seed=800,
     tint=dict(sec=[(0, 0, 0), (40, 16, 72), (136, 80, 216), (255, 240, 144)], keep=0.25, gamma=0.9),
     music='MUS_RG_SEVII_DUNGEON',
     decor=[])
# Werelden die een eigen script bouwt (kaart, layout, tileset, map.json, scripts.inc, wilde Pokémon): hier alleen
# de plek in het portaal (SPOTS-volgorde) en de aankomstplek voor de hub (uit het warpblok in de hub-scripts.inc,
# dat het andere script bijwerkt). Zie ultra_worlds_b.py.
EXTERNAL_B = ('Guzzlord', 'Poipole', 'Stakataka', 'Blacephalon', 'Necrozma')   # tools/grounded/maptools/ultra_worlds_b.py
EXTERNAL = set(EXTERNAL_B)


def external_arrive(key):
    s = open('data/maps/UltraSpace_Hub/scripts.inc').read()
    m = re.search(r'UltraSpace_Hub_EventScript_To%s::\n\twarp MAP_ULTRA_SPACE_\w+, (\d+), (\d+)' % key, s)
    return int(m.group(1)), int(m.group(2))


HUB_TINT = dict(sec=[(16, 16, 56), (120, 104, 200), (232, 224, 248), (255, 255, 240)], keep=0.15, gamma=0.55)
LOCAL = {'Poipole': 'aliens'}


# ====================================================================== bouwen
def build_tints(key, base_prim, base_sec, t):
    keep, gamma = t.get('keep', 0.2), t.get('gamma', 1.0)
    prim, sec = base_prim, base_sec
    if 'prim' in t:
        fn = make_tint(t['prim'], keep, gamma)
        prim = pal_tileset(base_prim, key + 'Base', fn)
        sec = pal_tileset(base_sec, key, fn)
    if 'sec' in t:
        sec = pal_tileset(base_sec, key, make_tint(t['sec'], keep, gamma))
    return prim, sec


SUMMARY = {}


def build_spot(i, s):
    key = s['key']
    name = 'UltraSpace_' + key
    if key in REBUILT:      # kaart, tileset en scripts komen uit ultra_worlds_a.py; hier alleen de aankomstplek (hub-warp)
        hs = open('data/maps/UltraSpace_Hub/scripts.inc').read()
        m = re.search(r'warp %s, (\d+), (\d+)' % map_const(name), hs)
        SUMMARY[key] = dict(name=name, arrive=(int(m.group(1)), int(m.group(2))), ub=None, ret=None, kinds=[], items=[])
        add_to_group(name)
        add_include(name)
        return name
    if 'mask' in s:
        mask = s['mask']
        g = autotile(mask, s['seed'])
        arrive = find(mask, 'A')
        ret = find(mask, 'R')
        ub = find(mask, 'U') if 'U' in ''.join(mask) else None
        base_prim, base_sec = 'gTileset_General', 'gTileset_MeteorSpace'
        border = [STARS[0], STARS[1], STARS[2], STARS[0]]
    else:
        src, x0, y0, w, h = s['src']
        g, l = crop(src, x0, y0, w, h)
        arrive, ret, ub = s['arrive'], s['ret'], s.get('ub')
        base_prim, base_sec = l['primary_tileset'], l['secondary_tileset']
        border = list(struct.unpack('<4H', open(l['border_filepath'], 'rb').read()))
    edit = globals().get('edit_' + key)
    if edit:
        edit(g)
    prim, sec = build_tints(key, base_prim, base_sec, s['tint'])
    decor = s.get('decor', [])
    blocked = {ret} | {(x, y) for _, x, y, *_ in decor if not str(_[1]).startswith('MOVEMENT_TYPE_WANDER')}
    blocked = {ret} | {(d[1], d[2]) for d in decor}
    for d in decor:
        assert not (g[d[2]][d[1]] >> 10) & 3, (key, 'decor op een muur', d)
    items = ni.items(name)
    r = reachable(g, arrive, blocked)
    if ub is None:      # verst bereikbare vak (BFS-afstand) dat een buur heeft
        dist = {arrive: 0}
        q = deque([arrive])
        while q:
            c = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (c[0] + dx, c[1] + dy)
                if n in r and n not in dist:
                    dist[n] = dist[c] + 1
                    q.append(n)
        ub = max(dist, key=lambda c: (dist[c], -c[1]))
    blocked |= {ub}
    r = reachable(g, arrive, blocked)
    assert next_to(r, *ub), (key, 'UB onbereikbaar', ub)
    assert next_to(r, *ret), (key, 'terugweg onbereikbaar', ret)
    for d in decor:
        if d[3] and 'WANDER' not in str(d[3]):
            pass
    # items op een bereikbare plek, ver van de aankomst, niet op de looproute naar de UB
    item_spots = s.get('items') or []
    if items and not item_spots:
        rr = sorted(r - {arrive}, key=lambda c: (-abs(c[0] - arrive[0]) - abs(c[1] - arrive[1]), c))
        for c in rr:
            if len(item_spots) == len(items):
                break
            if c in blocked or any(abs(c[0] - o[0]) + abs(c[1] - o[1]) < 3 for o in item_spots + [ub]):
                continue
            r2 = reachable(g, arrive, blocked | {c} | set(item_spots))
            if next_to(r2, *ub) and next_to(r2, *ret) and next_to(r2, *c):
                item_spots.append(c)
    assert len(item_spots) == len(items), (key, 'te weinig plek voor items')
    layout_const = save_layout(name, g, border, prim, sec)
    flag = 'FLAG_ULTRA_' + s['species']
    objs = [obj('LOCALID_ULTRA_%s_RETURN' % key.upper(), WORM, ret[0], ret[1], 'UltraSpace_EventScript_ReturnToHub')]
    if key == 'Poipole':
        objs.append(obj('LOCALID_ULTRA_POIPOLE_MON', mon('POIPOLE'), ub[0], ub[1], name + '_EventScript_Poipole', flag,
                        'MOVEMENT_TYPE_JOG_IN_PLACE_DOWN'))
        for j, (sp, x, y) in enumerate((('BEHEEYEM', ub[0] - 1, ub[1] + 1), ('ELGYEM', ub[0] + 1, ub[1] + 1),
                                        ('ELGYEM', ub[0] + 3, ub[1]))):
            objs.append(obj(None, mon(sp), x, y, name + '_EventScript_Alien%d' % j, '0', 'MOVEMENT_TYPE_FACE_DOWN'))
            blocked.add((x, y))
        r = reachable(g, arrive, blocked)
        assert next_to(r, ub[0] - 1, ub[1] + 1), 'Beheeyem onbereikbaar'
    else:
        objs.append(obj('LOCALID_ULTRA_%s_UB' % key.upper(), mon(s['species']), ub[0], ub[1], name + '_EventScript_UB', flag))
    kinds = []
    for sp, x, y, mv, kind in decor:
        if kind not in kinds:
            kinds.append(kind)
        gfx = mon(sp) if sp else mv
        move = mv if sp else 'MOVEMENT_TYPE_FACE_DOWN'
        dflag = flag if kind in ('Wall', 'Echo', 'Rocket', 'Cable', 'Fold') else '0'
        objs.append(obj(None, gfx, x, y, '%s_EventScript_%s' % (name, kind), dflag, move,
                        rx=1 if 'WANDER' in move else 0))
    bgs = []
    for (fl, it, q, hid), (x, y) in zip(items, item_spots):
        if hid:
            bgs.append({'type': 'hidden_item', 'x': x, 'y': y, 'elevation': g[y][x] >> 12, 'item': it, 'flag': fl})
        else:
            objs.append(obj(None, 'OBJ_EVENT_GFX_ITEM_BALL', x, y, 'Common_EventScript_FindItem', fl,
                            'MOVEMENT_TYPE_LOOK_AROUND', it, rx=q))
    assert len(objs) <= 15, (key, len(objs))
    os.makedirs('data/maps/' + name, exist_ok=True)
    write_json('data/maps/%s/map.json' % name, map_json(name, layout_const, s['music'], objs, bgs))
    add_to_group(name)
    add_include(name)
    SUMMARY[key] = dict(name=name, arrive=arrive, ub=ub, ret=ret, kinds=kinds, items=list(zip(items, item_spots)))
    return name


# ---------------------------------------------------------------- kaartaanpassingen per bron
def edit_Blacephalon(g):
    """Battle Dome: tribunes dicht (rij 0-3), de BATTLE FRONTIER-banner (rij 3) wordt nog een rij publiek."""
    for x in range(len(g[0])):
        g[3][x] = g[1][x]
        for y in range(4):
            g[y][x] |= 1 << 10


def edit_Xurkitree(g):
    """New Mauville: alle groene/blauwe slagbomen open (zoals de knoppen ze openzetten)."""
    OPEN = {0x2B6: (0x269, 1), 0x2B7: (0x269, 1), 0x2BE: (0x271, 1), 0x2BF: (0x271, 1),
            0x2C6: (0x26D, 0), 0x2C7: (0x26D, 0), 0x2CE: (0x281, 0), 0x2CF: (0x281, 0)}
    for y in range(len(g)):
        for x in range(len(g[0])):
            m = g[y][x] & 0x3ff
            if m in OPEN:
                mt, col = OPEN[m]
                g[y][x] = mt | (col << 10) | (3 << 12)


def edit_Poipole(g):
    """Gifkristallen (Cave 0x3A5-0x3A7) op de lichte grotvloer 0x211; alleen waar ze niets afsluiten."""
    rnd = random.Random(803)
    spots = [(x, y) for y in range(len(g)) for x in range(len(g[0])) if g[y][x] & 0x3ff == 0x211
             and abs(x - 25) + abs(y - 3) > 4 and abs(x - 8) + abs(y - 12) > 2]
    rnd.shuffle(spots)
    n, size = 0, len(reachable(g, (8, 12)))
    for (x, y) in spots:
        if n == 14:
            break
        old = g[y][x]
        g[y][x] = (old & ~0x3ff) | rnd.choice((0x3A5, 0x3A6, 0x3A7)) | (1 << 10)
        if len(reachable(g, (8, 12))) != size - 1:
            g[y][x] = old
            continue
        size -= 1
        n += 1


def main():
    names = [build_spot(i, s) for i, s in enumerate(SPOTS) if s['key'] not in EXTERNAL]
    for s in SPOTS:
        if s['key'] in EXTERNAL:
            SUMMARY[s['key']] = dict(name='UltraSpace_' + s['key'], arrive=external_arrive(s['key']), external=True)
    # hub
    hub = 'UltraSpace_Hub'
    g = autotile(HUB_MASK, 777)
    prim, sec = build_tints('Hub', 'gTileset_General', 'gTileset_MeteorSpace', HUB_TINT)
    portal, arrive, ret = find(HUB_MASK, 'P'), find(HUB_MASK, 'A'), find(HUB_MASK, 'R')
    r = reachable(g, arrive, {portal, ret})
    assert next_to(r, *portal) and next_to(r, *ret), 'hub'
    lc = save_layout(hub, g, [STARS[0], STARS[1], STARS[2], STARS[0]], prim, sec)
    write_json('data/maps/%s/map.json' % hub if os.path.isdir('data/maps/' + hub) else
               (os.makedirs('data/maps/' + hub) or 'data/maps/%s/map.json' % hub),
               map_json(hub, lc, 'MUS_RG_SEVII_CAVE',
                        [obj('LOCALID_ULTRA_HUB_PORTAL', WORM, portal[0], portal[1], hub + '_EventScript_Portal'),
                         obj('LOCALID_ULTRA_HUB_RETURN', WORM, ret[0], ret[1], hub + '_EventScript_ToAlteringCave'),
                         obj(None, mon('COSMOG'), portal[0] + 3, portal[1] + 1, hub + '_EventScript_Cosmog', '0',
                             'MOVEMENT_TYPE_FACE_LEFT')],
                        [{'type': 'sign', 'x': arrive[0] + 2, 'y': arrive[1] - 1, 'elevation': 0,
                          'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY', 'script': hub + '_EventScript_Sign'}]))
    add_to_group(hub)
    add_include(hub)
    SUMMARY['Hub'] = dict(arrive=arrive, portal=portal, ret=ret)
    write_tileset_blocks()
    altering_cave(arrive)
    write_scripts(arrive)
    for k, v in SUMMARY.items():
        print(k, {a: b for a, b in v.items() if a != 'kinds'})


# ====================================================================== Altering Cave
def altering_cave(hub_arrive):
    g, _ = load('AlteringCave')
    start = (18, 21)
    r = reachable(g, start)
    dist = {start: 0}
    q = deque([start])
    while q:
        c = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (c[0] + dx, c[1] + dy)
            if n in r and n not in dist:
                dist[n] = dist[c] + 1
                q.append(n)
    # wormgat: het verste doodlopende vak, met een vrij vak eronder om op te staan
    cands = [c for c in dist if (c[0], c[1] + 1) in dist and c != start]
    cands.sort(key=lambda c: -dist[c])
    worm = next(c for c in cands if len(reachable(g, start, {c})) == len(r) - 1)
    stand = (worm[0], worm[1] + 1)
    d = json.load(open('data/maps/AlteringCave/map.json'))
    d['object_events'] = [o for o in d['object_events'] if o.get('local_id') != 'LOCALID_ALTERING_CAVE_WORMHOLE']
    d['object_events'].append(obj('LOCALID_ALTERING_CAVE_WORMHOLE', WORM, worm[0], worm[1],
                                  'AlteringCave_EventScript_UltraWormhole', 'FLAG_TEMP_1', elev=g[worm[1]][worm[0]] >> 12))
    write_json('data/maps/AlteringCave/map.json', d)
    s = open('data/maps/AlteringCave/scripts.inc').read()
    if 'UltraWormhole' not in s:
        s = s.replace('''AlteringCave_OnTransition:
	setflag FLAG_LANDMARK_ALTERING_CAVE
	end
''', '''AlteringCave_OnTransition:
	setflag FLAG_LANDMARK_ALTERING_CAVE
	call_if_unset FLAG_SYS_GAME_CLEAR, AlteringCave_EventScript_HideWormhole
	end

@ Project Grounded: Ultra Wormhole naar Ultra Space (post-game; tools/grounded/maptools/ultra_space.py)
AlteringCave_EventScript_HideWormhole::
	setflag FLAG_TEMP_1
	return

AlteringCave_EventScript_UltraWormhole::
	lock
	playse SE_M_TELEPORT
	waitse
	warp MAP_ULTRA_SPACE_HUB, %d, %d
	waitstate
	release
	end
''' % hub_arrive)
        open('data/maps/AlteringCave/scripts.inc', 'w').write(s)
    else:
        s = re.sub(r'warp MAP_ULTRA_SPACE_HUB, \d+, \d+', 'warp MAP_ULTRA_SPACE_HUB, %d, %d' % hub_arrive, s)
        open('data/maps/AlteringCave/scripts.inc', 'w').write(s)
    SUMMARY['AlteringCave'] = dict(worm=worm, stand=stand)


# ====================================================================== scripts
TEXTS = {
    'Poipole': ('',),   # gift van de aliens: teksten in POIPOLE_TEXTS
    'Nihilego': ('A translucent POKéMON drifts through the\nglass. It looks exactly like a thought\nyou had once and regretted.',
                 'Jelly', 'It floats through the air as if the air\nwere water. Nobody told it otherwise.',
                 'Echo', 'A reflection of NIHILEGO. Or NIHILEGO is\na reflection of this. The glass won\'t say.'),
    'Buzzwole': ('BUZZWOLE flexes. The floor flexes back.\\pIt has never skipped leg day. It has\nnever skipped any day.',
                 'Lifter', 'Counting reps. It lost count at 4,000\nand started over out of spite.'),
    'Pheromosa': ('PHEROMOSA strikes a pose at the end of\nthe catwalk.\\pIt refuses to look at you. You are not\nin its tax bracket.',
                  'Judge', 'The judge holds up a scorecard.\nIt says “ew”.',
                  'Crowd', 'The audience claps politely, then stops\nwhen it realizes it has no idea why.'),
    'Xurkitree': ('XURKITREE is plugged into nothing and\nstill pulling 40,000 volts.\\pYour hair is standing up. So is your\nBIKE, somewhere in your BAG.',
                  'Spark', 'It is chewing on a cable. The cable\nis chewing back.',
                  'Cable', 'A tangle of cables shaped like XURKITREE.\nOr a XURKITREE shaped like cables.'),
    'Celesteela': ('CELESTEELA is counting down.\\p3… 2… 1…\\pIt reconsiders. It counts down again.\nThis has been going on for a century.',
                   'Rocket', '3… 2… 1… nothing.\nThis one has been “about to launch”\\lsince the last ice age.',
                   'Smoke', 'It insists it is exhaust.\nIt is clearly just a KOFFING.'),
    'Kartana': ('A POKéMON made of paper, folded into a\nsword, folded into a POKéMON.\\pIt could cut you. Mostly it just gives\nyou papercuts and an attitude.',
                'Fold', 'A folded paper KARTANA. It is not alive.\nProbably. Do not unfold it.'),
    'Guzzlord': ('GUZZLORD is eating the horizon.\\pIt has been eating it for a while. The\nhorizon is getting nervous.',
                 'Trash', 'It lives here. It likes it here.\nPlease stop looking at it like that.',
                 'Junk', 'A pile of things GUZZLORD didn\'t finish.\nThere is a sock. There is always a sock.'),
    'Stakataka': ('The wall is looking at you.\\pOne brick in particular is looking at you\nreally hard.',
                  'Wall', 'The wall looks at you. You look at the\nwall. Nobody blinks. Bricks can\'t blink.'),
    'Blacephalon': ('BLACEPHALON juggles its own head.\\pIt drops it, on purpose, and it explodes.\nThe crowd goes wild. Your eyebrows go home.',
                    'Clown', 'A clown. Its makeup is real. Its smile\nis not. Welcome to the circus.'),
    'Necrozma': ('A POKéMON made of hungry darkness,\nsucking the light out of the prisms.\\pIt wants your light. You only have a\nflashlight app and a bad attitude.',),
}


def write_scripts(hub_arrive):
    for s in SPOTS:
        key = s['key']
        if key in EXTERNAL:
            continue
        info = SUMMARY[key]
        name = info['name']
        path = 'data/maps/%s/scripts.inc' % name
        if key in REBUILT or (os.path.exists(path) and not FORCE_SCRIPTS):
            continue
        t = TEXTS[key]
        out = ['%s_MapScripts::' % name, '\t.byte 0', '']
        sp = 'SPECIES_' + s['species']
        flag = 'FLAG_ULTRA_' + s['species']
        if key == 'Poipole':
            out += poipole_script(name)
        else:
            out += ['%s_EventScript_UB::' % name, '\tlock', '\tfaceplayer',
                    '\tplaymoncry %s, CRY_MODE_ENCOUNTER' % sp,
                    '\tmsgbox %s_Text_UB, MSGBOX_DEFAULT' % name, '\twaitmoncry', '\tclosemessage',
                    '\tsetwildbattle %s, %d' % (sp, s['level']), '\tspecial BattleSetup_StartLegendaryBattle',
                    '\twaitstate', '\tspecialvar VAR_RESULT, GetBattleOutcome',
                    '\tgoto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, %s_EventScript_UBCaught' % name,
                    '\tgoto_if_eq VAR_RESULT, B_OUTCOME_WON, %s_EventScript_UBBack' % name,
                    '\trelease', '\tend', '',
                    '%s_EventScript_UBBack::' % name, '\tmsgbox %s_Text_UBBack, MSGBOX_DEFAULT' % name,
                    '\trelease', '\tend', '',
                    '%s_EventScript_UBCaught::' % name, '\tsetflag %s' % flag, '\tgoto UltraSpace_EventScript_CaughtFade', '']
        for j in range(1, len(t), 2):
            out += ['%s_EventScript_%s::' % (name, t[j]), '\tmsgbox %s_Text_%s, MSGBOX_NPC' % (name, t[j]), '\tend', '']
        out += ['@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)']
        if key != 'Poipole':
            out += text_block('%s_Text_UB' % name, t[0])
            out += text_block('%s_Text_UBBack' % name, UB_BACK[key])
        else:
            out += [l for l in POIPOLE_TEXTS(name)]
        for j in range(1, len(t), 2):
            out += text_block('%s_Text_%s' % (name, t[j]), t[j + 1])
        open(path, 'w').write('\n'.join(out) + '\n')
    hub_script(hub_arrive)


UB_BACK = {
    'Nihilego': 'NIHILEGO wobbles back into the glass.\nIt will be back. Thoughts always are.',
    'Buzzwole': 'BUZZWOLE shakes it off and starts another\nset. You are now part of its warm-up.',
    'Pheromosa': 'PHEROMOSA walks back to the start of the\ncatwalk. Again. Forever. Fashion is pain.',
    'Xurkitree': 'XURKITREE reboots. Have you tried\nturning it off and on again? It did.',
    'Celesteela': 'CELESTEELA aborts the launch and resets\nthe countdown. 100… 99…',
    'Kartana': 'KARTANA refolds itself. Origami is\nmostly about not giving up.',
    'Guzzlord': 'GUZZLORD burps and keeps eating.\nYou were a snack. Barely.',
    'Stakataka': 'The bricks reshuffle. The wall is still\nlooking at you. Harder now.',
    'Blacephalon': 'BLACEPHALON grows a new head and takes\na bow. The crowd demands an encore.',
    'Necrozma': 'NECROZMA folds back into the dark.\nThe prisms dim. They\'re waiting for you.',
}


def text_block(label, txt):
    """Tekst met \\p (nieuw vak) -> .string-regels; regels breekt de Dialoogstudio-importer af (zelfde regels)."""
    plain = txt.replace('\\p', '\n\n').replace('\\l', ' ')
    plain = '\n\n'.join(re.sub(r'\s*\n\s*', ' ', b).strip() for b in plain.split('\n\n'))
    return ['%s:' % label] + ['\t.string "%s"' % l for l in dimp.to_strings(plain)] + ['']


def poipole_script(name):
    return ['%s_EventScript_Poipole::' % name, '\tlock', '\tfaceplayer', '\tplaymoncry SPECIES_POIPOLE, CRY_MODE_NORMAL',
            '\tmsgbox %s_Text_PoipoleMon, MSGBOX_DEFAULT' % name, '\twaitmoncry', '\trelease', '\tend', '',
            '%s_EventScript_Alien0::' % name, '\tlock', '\tfaceplayer',
            '\tgoto_if_set FLAG_ULTRA_POIPOLE, %s_EventScript_AlienAfter' % name,
            '\tmsgbox %s_Text_AlienGift, MSGBOX_DEFAULT' % name,
            '\tsetvar VAR_0x8004, SPECIES_POIPOLE', '\tsetvar VAR_0x8005, 85', '\tsetvar VAR_0x8006, ITEM_NONE',
            '\tcall Grounded_EventScript_GiveGiftMon',
            '\tgoto_if_eq VAR_RESULT, FALSE, %s_EventScript_AlienNoRoom' % name,
            '\tsetflag FLAG_ULTRA_POIPOLE', '\tremoveobject LOCALID_ULTRA_POIPOLE_MON',
            '\tmsgbox %s_Text_AlienBye, MSGBOX_DEFAULT' % name, '\trelease', '\tend', '',
            '%s_EventScript_AlienNoRoom::' % name, '\tmsgbox %s_Text_AlienNoRoom, MSGBOX_DEFAULT' % name,
            '\trelease', '\tend', '',
            '%s_EventScript_AlienAfter::' % name, '\tmsgbox %s_Text_AlienAfter, MSGBOX_DEFAULT' % name,
            '\trelease', '\tend', '',
            '%s_EventScript_Alien1::' % name, '\tmsgbox %s_Text_Alien1, MSGBOX_NPC' % name, '\tend', '',
            '%s_EventScript_Alien2::' % name, '\tmsgbox %s_Text_Alien2, MSGBOX_NPC' % name, '\tend', '']


def POIPOLE_TEXTS(name):
    t = []
    t += text_block(name + '_Text_PoipoleMon', 'POIPOLE: Beepu?\\pIt is wearing a tiny backpack. Someone\nloves this thing very much.')
    t += text_block(name + '_Text_AlienGift',
                    'GREETINGS, FLESH-NOODLE.\\pWE HAVE OBSERVED YOUR PLANET FOR\nSEVENTEEN (17) TELEVISION SEASONS.\\p'
                    'WE ARE DISAPPOINTED BY THE FINALE.\\pTAKE THIS SMALL PURPLE ONE. IT EATS\nNOTHING AND SAYS “BEEPU”.\\p'
                    'WE CANNOT TAKE IT HOME. IT IS\nALLERGIC TO HOME.')
    t += text_block(name + '_Text_AlienBye', 'GOODBYE, FLESH-NOODLE. PLEASE RATE\nYOUR ABDUCTION FIVE STARS.')
    t += text_block(name + '_Text_AlienNoRoom', 'YOUR POCKET-DIMENSIONS ARE FULL.\nWE WILL WAIT. WE ARE GOOD AT WAITING.\\p'
                                                'WE HAVE BEEN WAITING SINCE THE\nDINOSAURS. THEY ALSO HAD NO ROOM.')
    t += text_block(name + '_Text_AlienAfter', 'DOES THE PURPLE ONE STILL SAY “BEEPU”?\nGOOD. THAT MEANS IT IS WORKING.')
    t += text_block(name + '_Text_Alien1', 'BLEEP. WE COME IN PEACE.\nWE LEAVE IN PIECES. LONG STORY.')
    t += text_block(name + '_Text_Alien2', 'YOUR CRYSTALS ARE DELICIOUS.\nDO NOT LICK THE CRYSTALS.\\pWE ARE ALLOWED. WE HAVE THE PAPERWORK.')
    return t


def hub_script(hub_arrive):
    hub = 'UltraSpace_Hub'
    path = 'data/maps/%s/scripts.inc' % hub
    # het warpblok wordt altijd opnieuw geschreven (gegenereerd), de rest alleen de eerste keer
    warps = ['@ ultra_space { gegenereerd door tools/grounded/maptools/ultra_space.py; niet met de hand bewerken',
             'UltraSpace_Hub_EventScript_PortalWarp::', '\tspecial Ultra_PickPortal', '\tswitch VAR_RESULT']
    for i, s in enumerate(SPOTS):
        warps.append('\tcase %d, UltraSpace_Hub_EventScript_To%s' % (i, s['key']))
    warps.append('\tend')
    for s in SPOTS:
        a = SUMMARY[s['key']]['arrive']
        warps += ['UltraSpace_Hub_EventScript_To%s::' % s['key'], '\twarp %s, %d, %d' % (map_const('UltraSpace_' + s['key']), a[0], a[1]),
                  '\twaitstate', '\tend']
    ret = SUMMARY['Hub']['ret']
    warps += ['', 'UltraSpace_EventScript_ReturnToHub::', '\tlock', '\tplayse SE_M_TELEPORT', '\twaitse',
              '\twarp MAP_ULTRA_SPACE_HUB, %d, %d' % hub_arrive, '\twaitstate', '\trelease', '\tend', '',
              'UltraSpace_Hub_EventScript_ToAlteringCave::', '\tlock', '\tplayse SE_M_TELEPORT', '\twaitse',
              '\twarp MAP_ALTERING_CAVE, %d, %d' % SUMMARY['AlteringCave']['stand'], '\twaitstate', '\trelease', '\tend',
              '@ }']
    if os.path.exists(path) and not FORCE_SCRIPTS:
        s = open(path).read()
        i = s.index('@ ultra_space {')
        j = s.index('@ }', i) + 3
        open(path, 'w').write(s[:i] + '\n'.join(warps) + s[j:])
        return
    out = ['%s_MapScripts::' % hub, '\t.byte 0', '',
           '%s_EventScript_Portal::' % hub, '\tlock',
           '\tgoto_if_set FLAG_ULTRA_HUB_VISITED, %s_EventScript_PortalGo' % hub,
           '\tsetflag FLAG_ULTRA_HUB_VISITED', '\tmsgbox %s_Text_PortalFirst, MSGBOX_DEFAULT' % hub,
           '%s_EventScript_PortalGo::' % hub,
           '\tspecial Ultra_CountOpen', '\tgoto_if_ne VAR_RESULT, 0, %s_EventScript_PortalJump' % hub,
           '\tmsgbox %s_Text_PortalAllDone, MSGBOX_DEFAULT' % hub, '\tcloseMessage' if False else '\tclosemessage',
           '%s_EventScript_PortalJump::' % hub, '\tplayse SE_M_TELEPORT', '\twaitse',
           '\tgoto UltraSpace_Hub_EventScript_PortalWarp', '',
           '@ Na het vangen van een Ultra Beast: even stil, dan verder (gedeeld door alle plekken)',
           'UltraSpace_EventScript_CaughtFade::', '\tremoveobject VAR_LAST_TALKED', '\trelease', '\tend', '',
           '%s_EventScript_Cosmog::' % hub, '\tlock', '\tfaceplayer', '\tplaymoncry SPECIES_COSMOG, CRY_MODE_NORMAL',
           '\tmsgbox %s_Text_Cosmog, MSGBOX_DEFAULT' % hub, '\twaitmoncry', '\trelease', '\tend', '',
           '%s_EventScript_Sign::' % hub, '\tmsgbox %s_Text_Sign, MSGBOX_SIGN' % hub, '\tend', ''] + warps + [
           '', '@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)']
    out += text_block(hub + '_Text_PortalFirst',
                      'A hole in reality, humming like a fridge\nat 3 AM.\\pSomething on the other side is thinking\nabout you. '
                      'It is not thinking nice\\lthings.\\pThe hole picks where you go. You do not\nget a vote. Welcome to democracy.')
    out += text_block(hub + '_Text_PortalAllDone',
                      'The portal has run out of strangers.\nIt sends you somewhere anyway, for old\\ltimes\' sake.')
    out += text_block(hub + '_Text_Cosmog', 'COSMOG: Pew!\\pIt seems to be lost. Or it is exactly\nwhere it wants to be, and you are lost.')
    out += text_block(hub + '_Text_Sign', 'ULTRA SPACE\nPlease do not feed the beasts.\\pThe beasts will feed themselves.')
    open(path, 'w').write('\n'.join(out) + '\n')


if __name__ == '__main__':
    main()
    if '--render' in sys.argv:
        n = sys.argv[sys.argv.index('--render') + 1]
        subprocess.run([sys.executable, 'tools/grounded/maptools/render_map.py', n, sys.argv[sys.argv.index('--render') + 2], '0', '999'])
