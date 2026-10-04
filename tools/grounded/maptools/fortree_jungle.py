"""Project Grounded: Fortree Jungle, een dicht, nat regenwoud onder Fortree City.

Bouwt (idempotent, vaste seed):
- data/layouts/FortreeJungle/map.bin + border.bin (40x68, primary General + secondary Fortree, de bomen van Route 119).
- data/maps/FortreeJungle/map.json (connection omhoog naar Fortree, objecten, bord-events).
- Fortree City: twee openingen in de zuidrand (x 9-12 en x 34-36) + connection omlaag naar de jungle.
- Registratie: layouts.json, map_groups.json (gMapGroup_Grounded), event_scripts.s.
De scripts.inc staat met de hand in data/maps/FortreeJungle.

Opbouw: alles begint als bos; paden (polylijnen met breedte), open plekken (blobs), hoog gras (blobs),
poelen (pond-water met oevers zoals Route 119), plassen, bloemen en reuzenpalmen (stempel uit Fortree).
Daarna autotiling: boomkruin boven een open vak (0x0E/0x0F), stam onderaan het bos (0x16/0x17),
lang gras met de zuidrand (0x15 / Fortree 0x208), pond-oevers (0xB0-0xBA, 0xC0/0xC2) en de oever-grastegel
(0x002) onder het water. Tot slot controleert het script de bereikbaarheid van alle events.

Vrijgehouden voor later: de open plek van Zarude (zuidwest, diep in de jungle) en het heiligdom van Ogerpon
(zuidoost, stenen altaar 0x255 met bloemen, NPC-placeholder).

Gebruik: python3 tools/grounded/maptools/fortree_jungle.py [voorbeeld.png]"""
import json, math, os, random, struct, sys
from collections import deque

W, H = 40, 68
SEED = 893  # nationaal dexnummer van Zarude
rng = random.Random(SEED)

# ---------------------------------------------------------------- terrein
# T bos, g gras, L lang gras, w poelwater, p plas, f bloemen, b struik (blokkeert), a altaar, s bord (blokkeert)
T = [['T'] * W for _ in range(H)]


def inb(x, y):
    return 0 <= x < W and 0 <= y < H


def disc(cx, cy, r, kind='g', only=None, keep_border=True):
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            if not inb(x, y):
                continue
            if keep_border and (x == 0 or x == W - 1 or y == H - 1):
                continue
            if (x - cx) ** 2 + ((y - cy) * 1.15) ** 2 <= r * r:
                if only is None or T[y][x] in only:
                    T[y][x] = kind


def blob(cx, cy, r, kind, only=None, n=5):
    disc(cx, cy, r, kind, only)
    for _ in range(n):
        a = rng.random() * 2 * math.pi
        d = r * (0.4 + 0.5 * rng.random())
        disc(cx + math.cos(a) * d, cy + math.sin(a) * d, r * (0.45 + 0.3 * rng.random()), kind, only)


def path(pts, w=2, kind='g'):
    """Pad door de waypoints; w = breedte. Vierkante kwast zodat de randen recht blijven."""
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(abs(x1 - x0), abs(y1 - y0)) * 3 + 1
        for i in range(n + 1):
            t = i / n
            x = x0 + (x1 - x0) * t
            y = y0 + (y1 - y0) * t
            for dy in range(w):
                for dx in range(w):
                    xx, yy = int(round(x - (w - 1) / 2 + dx)), int(round(y - (w - 1) / 2 + dy))
                    if inb(xx, yy) and 0 < xx < W - 1 and yy < H - 1:
                        T[yy][xx] = kind


def rect(x0, y0, x1, y1, kind):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            T[y][x] = kind


# ingangen vanuit Fortree (bovenrand): west x 9-12, oost x 34-36
ENTR = [(x, 0) for x in range(9, 13)] + [(x, 0) for x in range(34, 37)]
rect(9, 0, 12, 2, 'g')
rect(34, 0, 36, 2, 'g')

# hoofdpaden
path([(10, 1), (10, 6), (6, 10), (5, 16), (8, 23), (13, 29), (16, 32)], 3)          # west
path([(35, 1), (34, 7), (29, 11), (25, 16), (22, 23), (19, 29)], 2)                   # oost
path([(5, 13), (2, 13)], 2)                                                            # zijzak noordwest
path([(30, 11), (36, 15), (37, 21)], 2)                                                # zijzak oost
disc(17, 33, 5)                                                                        # centrale open plek
path([(15, 37), (11, 42), (6, 47), (7, 53), (9, 57)], 2)                               # naar Zarude
path([(20, 37), (25, 41), (31, 45), (32, 50)], 2)                                      # naar Ogerpon
path([(13, 62), (19, 64), (24, 62), (28, 57)], 2)                                      # zuidlus
path([(20, 63), (21, 66)], 2)                                                          # verborgen zakje zuid
path([(31, 45), (36, 43), (37, 39)], 2)                                                # doodlopend oost
path([(11, 42), (16, 45)], 2)                                                          # doodlopend midden
disc(9, 60, 5.2)                                                                       # Zarude
disc(31, 54, 4.2)                                                                      # Ogerpon

# hoog gras (alleen op al open grond of bos aan de rand van een pad)
for cx, cy, r in ((7, 19, 3.2), (24, 19, 2.8), (13, 44, 3), (27, 43, 2.6), (18, 62, 2.6), (32, 9, 2.4),
                  (6, 51, 2.6), (35, 17, 2.2), (11, 7, 2.2), (25, 63, 2.2)):
    blob(cx, cy, r, 'L')

# poel ten oosten van de open plek; het TM-zakje is alleen surfend bereikbaar
for y in range(30, 37):
    x0 = 24 if 31 <= y <= 35 else 25
    x1 = 32 if 31 <= y <= 35 else 31
    for x in range(x0, x1 + 1):
        T[y][x] = 'w'
rect(21, 32, 23, 34, 'g')                # verbinding open plek -> oever (3 hoog, geen inham in de poel)
rect(33, 32, 35, 34, 'g')                # eilandzakje (oost, ingesloten door bos)
for x in range(24, 34):
    if T[36][x] == 'w' and T[37][x] == 'T':
        T[37][x] = 'g'                   # grasrand onder de poel (oevertegel)
for x in range(25, 32):
    T[37][x] = 'g'
# tweede poeltje in de Zarude-open plek
for y in range(58, 61):
    for x in range(3, 7):
        T[y][x] = 'w'
for x in range(3, 7):
    T[61][x] = 'g'

# plassen (regenwater) en bloemen
PUDDLES = [(19, 35, 3, 2), (12, 63, 2, 2), (29, 52, 2, 2), (7, 26, 2, 2)]
for x0, y0, w, h in PUDDLES:
    rect(x0, y0, x0 + w - 1, y0 + h - 1, 'p')
for (x, y) in ((29, 55), (33, 55), (30, 56), (32, 56), (29, 54), (33, 54), (14, 33), (20, 31), (11, 58), (13, 59)):
    T[y][x] = 'f'
ALTAR = (31, 54)
T[ALTAR[1]][ALTAR[0]] = 'a'
T[55][31] = 'g'
ZARUDE_SIGN = (9, 56)
T[ZARUDE_SIGN[1]][ZARUDE_SIGN[0]] = 's'
for (x, y) in ((4, 9), (15, 31), (26, 13), (8, 45), (24, 61)):
    if T[y][x] in 'gL':
        T[y][x] = 'b'

# losse bosvakjes van 1 breed tussen twee open vakken boven/onder zien er rommelig uit: openen
for _ in range(2):
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            if T[y][x] == 'T' and T[y - 1][x] in 'gLf' and T[y + 1][x] in 'gLf':
                T[y][x] = 'g'

# ---------------------------------------------------------------- events
OBJ = []      # (gfx, x, y, movement, trainer_type, sight/item, script, flag)
TRAINERS = [  # x, y, kijkrichting, gfx, script, zicht
    (4, 15, 'RIGHT', 'OBJ_EVENT_GFX_BUG_CATCHER', 'FortreeJungle_EventScript_Bram', 4),
    (23, 21, 'DOWN', 'OBJ_EVENT_GFX_WOMAN_5', 'FortreeJungle_EventScript_Maya', 4),
    (13, 33, 'TREE', 'OBJ_EVENT_GFX_NINJA_BOY', 'FortreeJungle_EventScript_Hanzo', 3),
    (26, 40, 'DOWN', 'OBJ_EVENT_GFX_WOMAN_2', 'FortreeJungle_EventScript_Flora', 3),
    (8, 50, 'LEFT', 'OBJ_EVENT_GFX_HIKER', 'FortreeJungle_EventScript_Dirk', 3),
]
ITEMS = [  # x, y, item, flag
    (2, 13, 'ITEM_BIG_ROOT', 'FLAG_ITEM_FORTREE_JUNGLE_BIG_ROOT'),
    (37, 21, 'ITEM_MAX_REVIVE', 'FLAG_ITEM_FORTREE_JUNGLE_MAX_REVIVE'),
    (34, 33, 'ITEM_TM_U_TURN', 'FLAG_ITEM_FORTREE_JUNGLE_TM_U_TURN'),
    (37, 39, 'ITEM_MIRACLE_SEED', 'FLAG_ITEM_FORTREE_JUNGLE_MIRACLE_SEED'),
]
HIDDEN = [  # x, y, item, flag
    (21, 66, 'ITEM_LEAF_STONE', 'FLAG_HIDDEN_ITEM_FORTREE_JUNGLE_LEAF_STONE'),
    (16, 45, 'ITEM_REVIVAL_HERB', 'FLAG_HIDDEN_ITEM_FORTREE_JUNGLE_REVIVAL_HERB'),
]
NPCS = [(32, 56, 'OBJ_EVENT_GFX_OLD_WOMAN', 'FortreeJungle_EventScript_MaskKeeper')]
SIGNS = [(ALTAR[0], ALTAR[1], 'FortreeJungle_EventScript_MaskAltar'),
         (ZARUDE_SIGN[0], ZARUDE_SIGN[1], 'FortreeJungle_EventScript_ZarudeSign')]
for x, y, *_ in TRAINERS + ITEMS + NPCS:
    assert T[y][x] in 'gLf', ('event niet op open grond', x, y, T[y][x])

# ---------------------------------------------------------------- autotiling
GRASS, LONG, LONG_S, BANK = 0x001, 0x015, 0x208, 0x002
FOREST, TRUNK, CANOPY = (0x0C6, 0x0C7), (0x016, 0x017), (0x00E, 0x00F)
FLOWER, BUSH, ALTAR_MT, SIGN_MT = 0x004, 0x276, 0x255, 0x01B
PUD = {(0, 0): 0xC8, (1, 0): 0xC9, (2, 0): 0xCA, (0, 1): 0xD0, (1, 1): 0xD1, (2, 1): 0xD2,
       (0, 2): 0xD8, (1, 2): 0xD9, (2, 2): 0xDA}
PALM = [[0x248, 0x249, 0x24A], [0x250, 0x251, 0x252], [0x0C7, 0x241, 0x0C7], [0x0C7, 0x273, 0x0C6]]


def kind(x, y):
    if not inb(x, y):
        return 'T'
    return T[y][x]


def val(mt, coll, elev):
    return mt | (coll << 10) | (elev << 12)


M = [[0] * W for _ in range(H)]
for y in range(H):
    for x in range(W):
        k = T[y][x]
        below = kind(x, y + 1) if y + 1 < H else 'T'
        if k == 'T':
            if below != 'T':
                M[y][x] = val(rng.choice(TRUNK), 1, 0)
            else:
                M[y][x] = val(rng.choice(FOREST), 1, 0)
        elif k == 'w':
            up, lf, rt = kind(x, y - 1) != 'w', kind(x - 1, y) != 'w', kind(x + 1, y) != 'w'
            ul, ur = kind(x - 1, y - 1) != 'w', kind(x + 1, y - 1) != 'w'
            if up:
                mt = 0xB0 if lf else 0xB2 if rt else 0xB1
            elif lf:
                mt = 0xB8
            elif rt:
                mt = 0xBA
            elif ul:
                mt = 0xC0
            elif ur:
                mt = 0xC2
            else:
                mt = 0xA1
            M[y][x] = val(mt, 0, 1)
        elif below == 'T':
            M[y][x] = val(rng.choice(CANOPY), 0, 3)          # boomkruin van de boom eronder
        elif k == 'p':
            px = 0 if kind(x - 1, y) != 'p' else 2 if kind(x + 1, y) != 'p' else 1
            py = 0 if kind(x, y - 1) != 'p' else 2 if kind(x, y + 1) != 'p' else 1
            M[y][x] = val(PUD[(px, py)], 0, 3)
        elif k == 'L':
            M[y][x] = val(LONG if below == 'L' else LONG_S, 0, 3)
        elif k == 'f':
            M[y][x] = val(FLOWER, 0, 3)
        elif k == 'b':
            M[y][x] = val(BUSH, 1, 3)
        elif k == 'a':
            M[y][x] = val(ALTAR_MT, 1, 3)
        elif k == 's':
            M[y][x] = val(SIGN_MT, 1, 3)
        else:
            M[y][x] = val(BANK if kind(x, y - 1) == 'w' else GRASS, 0, 3)

# reuzenpalmen in massief bos (stempel van Fortree: kruin 3x2, stam, voet)
palms = 0
cands = [(x, y) for y in range(2, H - 6) for x in range(1, W - 3)]
rng.shuffle(cands)
used = set()
for x, y in cands:
    if palms >= 9:
        break
    if all(kind(x + dx, y + dy) == 'T' and M[y + dy][x + dx] & 0x3FF in FOREST
           for dy in range(-1, 5) for dx in range(3)) and not any((x + dx, y + dy) in used
                                                             for dy in range(-3, 7) for dx in range(-2, 5)):
        for dy in range(4):
            for dx in range(3):
                M[y + dy][x + dx] = val(PALM[dy][dx], 1, 0)
                used.add((x + dx, y + dy))
        palms += 1

# ---------------------------------------------------------------- bereikbaarheid
WALK = set('gLpf')


def bfs(starts, ok):
    seen, q = set(starts), deque(starts)
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if inb(*n) and n not in seen and ok(*n):
                seen.add(n)
                q.append(n)
    return seen


blocked = {(x, y) for x, y, *_ in TRAINERS + ITEMS + NPCS}
walk = bfs([ENTR[0]], lambda x, y: T[y][x] in WALK and (x, y) not in blocked)
assert ENTR[-1] in walk, 'oostingang niet verbonden met de westingang'
surf = bfs(list(walk), lambda x, y: (T[y][x] in WALK or T[y][x] == 'w') and (x, y) not in blocked)


def near(x, y, s):
    return any((x + dx, y + dy) in s for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))


for x, y, *_ in TRAINERS + NPCS:
    assert near(x, y, walk), ('trainer/NPC onbereikbaar', x, y)
for x, y, item, _ in ITEMS:
    s = surf if item == 'ITEM_TM_U_TURN' else walk
    assert near(x, y, s), ('item onbereikbaar', item)
    if item == 'ITEM_TM_U_TURN':
        assert not near(x, y, walk), 'TM-zakje moet alleen surfend bereikbaar zijn'
for x, y, item, _ in HIDDEN:
    assert (x, y) in walk, ('verborgen item onbereikbaar', item)
for x, y, _ in SIGNS:
    assert near(x, y, walk), ('bord onbereikbaar', x, y)
for name, (cx, cy) in (('Zarude', (9, 61)), ('Ogerpon', (31, 52))):
    assert (cx, cy) in walk, name + '-plek onbereikbaar'
print('bereikbaar: %d vakken lopend, %d met Surf; %d palmen' % (len(walk), len(surf), palms))

# ---------------------------------------------------------------- schrijven
os.makedirs('data/layouts/FortreeJungle', exist_ok=True)
open('data/layouts/FortreeJungle/map.bin', 'wb').write(b''.join(struct.pack('<H', v) for r in M for v in r))
open('data/layouts/FortreeJungle/border.bin', 'wb').write(struct.pack('<4H', 0x0C6 | 0x400, 0x0C7 | 0x400,
                                                                       0x0C7 | 0x400, 0x0C6 | 0x400))

# Fortree: openingen in de zuidrand (rij 19 was boomkruin 0x24B boven het niets)
FW, FH = 40, 20
fv = list(struct.unpack('<%dH' % (FW * FH), open('data/layouts/FortreeCity/map.bin', 'rb').read()))
for x in list(range(9, 13)) + list(range(34, 37)):
    fv[19 * FW + x] = val(GRASS, 0, 3)
open('data/layouts/FortreeCity/map.bin', 'wb').write(struct.pack('<%dH' % (FW * FH), *fv))
fj = open('data/maps/FortreeCity/map.json').read()
if 'MAP_FORTREE_JUNGLE' not in fj:
    fj = fj.replace('''      "direction": "right"
    }
  ],''', '''      "direction": "right"
    },
    {
      "map": "MAP_FORTREE_JUNGLE",
      "offset": 0,
      "direction": "down"
    }
  ],''', 1)
    assert 'MAP_FORTREE_JUNGLE' in fj
    open('data/maps/FortreeCity/map.json', 'w').write(fj)


def obj(gfx, x, y, move, ttype, sight, script, flag):
    return {"graphics_id": gfx, "x": x, "y": y, "elevation": 3, "movement_type": move,
            "movement_range_x": 1 if move == 'MOVEMENT_TYPE_TREE_DISGUISE' else 0,
            "movement_range_y": 1 if move == 'MOVEMENT_TYPE_TREE_DISGUISE' else 0,
            "trainer_type": ttype, "trainer_sight_or_berry_tree_id": str(sight), "script": script, "flag": flag}


objs = []
for x, y, face, gfx, script, sight in TRAINERS:
    move = 'MOVEMENT_TYPE_TREE_DISGUISE' if face == 'TREE' else 'MOVEMENT_TYPE_FACE_' + face
    objs.append(obj(gfx, x, y, move, 'TRAINER_TYPE_NORMAL', sight, script, '0'))
for x, y, item, flag in ITEMS:
    objs.append(obj('OBJ_EVENT_GFX_ITEM_BALL', x, y, 'MOVEMENT_TYPE_LOOK_AROUND', 'TRAINER_TYPE_NONE', item,
                    'Common_EventScript_FindItem', flag))
for x, y, gfx, script in NPCS:
    objs.append(obj(gfx, x, y, 'MOVEMENT_TYPE_FACE_UP', 'TRAINER_TYPE_NONE', 0, script, '0'))
mj = {
    "id": "MAP_FORTREE_JUNGLE", "name": "FortreeJungle", "layout": "LAYOUT_FORTREE_JUNGLE",
    "music": "MUS_ROUTE119", "region_map_section": "MAPSEC_FORTREE_JUNGLE", "requires_flash": False,
    "weather": "WEATHER_JUNGLE_CYCLE", "map_type": "MAP_TYPE_ROUTE", "allow_cycling": True,
    "allow_escaping": False, "allow_running": True, "show_map_name": True,
    "battle_scene": "MAP_BATTLE_SCENE_NORMAL",
    "connections": [{"map": "MAP_FORTREE_CITY", "offset": 0, "direction": "up"}],
    "object_events": objs, "warp_events": [], "coord_events": [],
    "bg_events": [{"type": "sign", "x": x, "y": y, "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
                   "script": s} for x, y, s in SIGNS] +
                 [{"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag} for x, y, item, flag in HIDDEN],
}
os.makedirs('data/maps/FortreeJungle', exist_ok=True)
with open('data/maps/FortreeJungle/map.json', 'w') as fp:
    json.dump(mj, fp, indent=2, ensure_ascii=False)
    fp.write('\n')

lj = open('data/layouts/layouts.json').read()
if '"LAYOUT_FORTREE_JUNGLE"' not in lj:
    i = lj.rindex('    }\n  ]')
    j = i + len('    }')
    lj = lj[:j] + ''',
    {
      "id": "LAYOUT_FORTREE_JUNGLE",
      "name": "FortreeJungle_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_General",
      "secondary_tileset": "gTileset_Fortree",
      "border_filepath": "data/layouts/FortreeJungle/border.bin",
      "blockdata_filepath": "data/layouts/FortreeJungle/map.bin"
    }''' % (W, H) + lj[j:]
    open('data/layouts/layouts.json', 'w').write(lj)
g = open('data/maps/map_groups.json').read()
if '"FortreeJungle"' not in g:
    i = g.index('"gMapGroup_Grounded": [')
    j = g.index('\n  ]', i)
    g = g[:j] + ',\n    "FortreeJungle"' + g[j:]
    open('data/maps/map_groups.json', 'w').write(g)
es = open('data/event_scripts.s').read()
inc = '\t.include "data/maps/FortreeJungle/scripts.inc"\n'
if inc not in es:
    anchor = '\t.include "data/maps/FlowerParadise_Meadow/scripts.inc"\n'
    assert anchor in es
    es = es.replace(anchor, anchor + inc, 1)
    open('data/event_scripts.s', 'w').write(es)

if len(sys.argv) > 1:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from gridrender import render
    render(M, 'general', 'fortree').save(sys.argv[1])
print('klaar')
