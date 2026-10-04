"""Project Grounded: Liberty Garden, het eilandje van Victini (post-game, Victory-gauntlet).
Layout = Southern Island (buitenkant) met de bosgrot dicht en de open plek verbreed tot een tuin:
een geplaveid plein (Rustboro) met fontein, lantaarns en bloemen.
De veerboot legt aan bij de steiger (13,22), net als bij Southern Island.
Gauntlet: het kronkelpad van de steiger naar het plein heeft vier knelpunten van 2 breed; op elk staat een
uitdager (zicht 1) die de ene helft blokkeert en de andere ziet, dus je moet ze op volgorde verslaan.
V wacht bij de fontein (aanspreken). Na de vijfde springt Victini van de rechterlantaarn naar de fontein.
Idempotent; controleert de bereikbaarheid. Gebruik: python3 tools/grounded/maptools/liberty_garden.py"""
import json, os, shutil, struct
from collections import deque

NAME, CONST = 'LibertyGarden', 'LIBERTY_GARDEN'
SRC = 'SouthernIsland_Exterior'
W, H = 33, 30
os.makedirs('data/layouts/' + NAME, exist_ok=True)
shutil.copy('data/layouts/%s/border.bin' % SRC, 'data/layouts/%s/border.bin' % NAME)
b = open('data/layouts/%s/map.bin' % SRC, 'rb').read()
v = [[struct.unpack_from('<H', b, (y * W + x) * 2)[0] for x in range(W)] for y in range(H)]

ELEV3 = 3 << 12
BLOCK = 1 << 10
GRASS, FLOWERS, TRUNK, CANOPY, FOREST = 0x001, 0x004, 0x016, 0x00E, 0x0C6
PAVE, LAMP_TOP, LAMP_POST = 0x2BB, 0x212, 0x21A
FOUNTAIN = [[0x338, 0x339, 0x33A], [0x340, 0x341, 0x342], [0x348, 0x349, 0x34A]]


def put(x, y, mt, blocked=False):
    v[y][x] = mt | ELEV3 | (BLOCK if blocked else 0)


# 1. open plek: rechthoek x 7-22, y 5-10 (de grot bovenaan verdwijnt; rij 4 = stammen onder het bos)
X0, X1, Y0, Y1 = 7, 22, 5, 10
for y in range(Y0, Y1 + 1):
    for x in range(X0, X1 + 1):
        put(x, y, GRASS)
for x in range(X0, X1 + 1):
    put(x, Y0 - 1, TRUNK, True)
    if v[Y1 + 1][x] & 0x3FF == FOREST:
        put(x, Y1 + 1, CANOPY, True)
# de grotopening (14-15, 4) en de bomen erboven: gewoon bos
for x in (14, 15):
    for y in range(0, Y0 - 1):
        v[y][x] = v[0][13]

# 2. plein van 7 x 5 met de fontein in het midden (x 11-17, y 6-10)
PX0, PY0 = 11, 6
for y in range(PY0, PY0 + 5):
    for x in range(PX0, PX0 + 7):
        put(x, y, PAVE)
for j in range(3):
    for i in range(3):
        put(PX0 + 2 + i, PY0 + 2 + j, FOUNTAIN[j][i], True)
# lantaarns op de hoeken boven en onder
for lx in (PX0, PX0 + 6):
    put(lx, PY0, LAMP_TOP)
    put(lx, PY0 + 1, LAMP_POST, True)
# 3. bloemperken links en rechts van het plein
for (fx, fy) in [(8, 6), (9, 6), (8, 7), (9, 9), (8, 9), (9, 10), (19, 6), (20, 6), (20, 7), (19, 9), (20, 9), (21, 10),
                 (7, 8), (22, 8)]:
    put(fx, fy, FLOWERS)

SIGN = (10, 6)
put(SIGN[0], SIGN[1], 0x003, True)
DOCK_SIGN = (11, 21)
put(DOCK_SIGN[0], DOCK_SIGN[1], 0x003, True)

open('data/layouts/%s/map.bin' % NAME, 'wb').write(b''.join(struct.pack('<H', v[y][x]) for y in range(H) for x in range(W)))

VICTINI = (14, 7)          # eindplek bij de fontein (setobjectxyperm in de scripts)
VICTINI_LAMP = (17, 6)     # startplek: de kop van de rechterlantaarn
SAILOR, DOCK = (13, 23), (13, 22)
# (naam, gfx, plek, kijkrichting, gezien vakje of None = aanspreken)
GAUNTLET = [
    ('VANCE', 'OBJ_EVENT_GFX_BLACK_BELT', (15, 19), 'RIGHT', (16, 19)),
    ('VERNON', 'OBJ_EVENT_GFX_RICH_BOY', (21, 15), 'DOWN', (21, 16)),
    ('VEGA', 'OBJ_EVENT_GFX_LASS', (24, 13), 'RIGHT', (25, 13)),
    ('VESNA', 'OBJ_EVENT_GFX_HEX_MANIAC', (23, 9), 'UP', (23, 8)),
    ('V', 'OBJ_EVENT_GFX_EXPERT_M', (16, 9), 'LEFT', None),
]
OBJS = {VICTINI, SAILOR} | {g[2] for g in GAUNTLET}

# bereikbaarheid: van de steiger naar Victini, de borden en elke uitdager
def walkable(x, y):
    return 0 <= x < W and 0 <= y < H and not (v[y][x] >> 10) & 3 and (v[y][x] >> 12) == 3 and (x, y) not in OBJS
def flood(extra_block=()):
    seen = {DOCK}; q = deque([DOCK])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in seen and walkable(*n) and n not in extra_block:
                seen.add(n); q.append(n)
    return seen
def near(seen, p, dirs=((0, 1), (0, -1), (1, 0), (-1, 0))):
    return any((p[0] + dx, p[1] + dy) in seen for dx, dy in dirs)
seen = flood()
assert near(seen, VICTINI), 'Victini onbereikbaar'
assert near(seen, SIGN, ((0, 1),)) and near(seen, DOCK_SIGN, ((0, 1), (1, 0))), 'bord onbereikbaar'
for name, gfx, pos, face, sight in GAUNTLET:
    assert pos in {(x, y) for y in range(H) for x in range(W) if not (v[y][x] >> 10) & 3}, name + ' staat op een muur'
    assert near(seen, pos), name + ' onbereikbaar'
    if sight:
        # gauntlet: wie het geziene vakje vermijdt, komt niet bij het plein (dus niet langs deze uitdager)
        assert not near(flood({sight}), VICTINI), name + ' kan omzeild worden'
        assert sight in seen and sight == (pos[0] + {'RIGHT': 1, 'LEFT': -1}.get(face, 0), pos[1] + {'DOWN': 1, 'UP': -1}.get(face, 0))

lj = open('data/layouts/layouts.json').read()
if '"LAYOUT_%s"' % CONST not in lj:
    i = lj.index('"id": "LAYOUT_SOUTHERN_ISLAND_INTERIOR"'); j = lj.index('},', i) + 2
    lj = lj[:j] + '''
    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_General",
      "secondary_tileset": "gTileset_Rustboro",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    },''' % (CONST, NAME, W, H, NAME, NAME) + lj[j:]
    open('data/layouts/layouts.json', 'w').write(lj)

def obj(lid, gfx, pos, mv, script, flag='0', elev=3, sight=0):
    return {'local_id': lid, 'graphics_id': gfx, 'x': pos[0], 'y': pos[1], 'elevation': elev, 'movement_type': mv,
            'movement_range_x': 0, 'movement_range_y': 0,
            'trainer_type': 'TRAINER_TYPE_NORMAL' if sight else 'TRAINER_TYPE_NONE',
            'trainer_sight_or_berry_tree_id': str(sight), 'script': script, 'flag': flag}

m = json.load(open('data/maps/%s/map.json' % SRC))
m.update({'id': 'MAP_' + CONST, 'name': NAME, 'layout': 'LAYOUT_' + CONST, 'region_map_section': 'MAPSEC_LIBERTY_GARDEN',
          'music': 'MUS_SOOTOPOLIS', 'show_map_name': True})
m['object_events'] = [
    obj('LOCALID_LIBERTY_GARDEN_SAILOR', 'OBJ_EVENT_GFX_SAILOR', SAILOR, 'MOVEMENT_TYPE_FACE_UP', NAME + '_EventScript_Sailor'),
    obj('LOCALID_LIBERTY_GARDEN_SS_TIDAL', 'OBJ_EVENT_GFX_SS_TIDAL', (13, 25), 'MOVEMENT_TYPE_FACE_RIGHT', '0x0', elev=1),
    obj('LOCALID_LIBERTY_GARDEN_VICTINI', 'OBJ_EVENT_GFX_SPECIES(VICTINI)', VICTINI_LAMP, 'MOVEMENT_TYPE_FACE_DOWN',
        NAME + '_EventScript_Victini', 'FLAG_HIDE_LIBERTY_GARDEN_VICTINI'),
] + [obj('LOCALID_LIBERTY_GARDEN_' + name, gfx, pos, 'MOVEMENT_TYPE_FACE_' + face,
         NAME + '_EventScript_' + name.capitalize(), sight=1 if sight else 0) for name, gfx, pos, face, sight in GAUNTLET]
m['warp_events'] = []
m['coord_events'] = []
m['bg_events'] = [{'type': 'sign', 'x': SIGN[0], 'y': SIGN[1], 'elevation': 3, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
                   'script': NAME + '_EventScript_Sign'},
                  {'type': 'sign', 'x': DOCK_SIGN[0], 'y': DOCK_SIGN[1], 'elevation': 3, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
                   'script': NAME + '_EventScript_DockSign'}]
os.makedirs('data/maps/' + NAME, exist_ok=True)
open('data/maps/%s/map.json' % NAME, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')

g = open('data/maps/map_groups.json').read()
if '"%s"' % NAME not in g:
    g = g.replace('    "BattleFrontier_StadiumArena"', '    "BattleFrontier_StadiumArena",\n    "%s"' % NAME, 1)
    open('data/maps/map_groups.json', 'w').write(g)
es = open('data/event_scripts.s').read()
inc = '\t.include "data/maps/%s/scripts.inc"\n' % NAME
if inc not in es:
    es = es.replace('\t.include "data/maps/MeteorSpace/scripts.inc"\n', '\t.include "data/maps/MeteorSpace/scripts.inc"\n' + inc, 1)
    open('data/event_scripts.s', 'w').write(es)
print('klaar,', len(seen), 'bereikbare tegels')
