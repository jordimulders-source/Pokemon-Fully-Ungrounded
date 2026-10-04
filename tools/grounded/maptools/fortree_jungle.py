"""Project Grounded: Fortree Jungle, een dicht, nat regenwoud onder Fortree City.

Bouwt (idempotent, vaste seed):
- data/layouts/FortreeJungle/map.bin + border.bin (40x68, primary General + secondary fortree_jungle: Fortree met
  tropische tiles/metatiles achteraan, gebouwd door jungle_tileset.py).
- data/maps/FortreeJungle/map.json (connection omhoog naar Fortree, objecten, bord-events).
- Fortree City: twee openingen in de zuidrand (x 9-12 en x 34-36) + connection omlaag naar de jungle.
- Registratie: layouts.json, map_groups.json (gMapGroup_Grounded), event_scripts.s.
De scripts.inc staat met de hand in data/maps/FortreeJungle.

Opbouw: alles begint als bos; paden (polylijnen met breedte), open plekken (blobs), hoog gras (blobs),
poelen (pond-water met oevers zoals Route 119), plassen, bloemen en reuzenpalmen (stempel uit Fortree).
Daarna autotiling: boomkruin boven een open vak (0x0E/0x0F), stam onderaan het bos (0x16/0x17),
lang gras met de zuidrand (0x15 / Fortree 0x208), pond-oevers (0xB0-0xBA, 0xC0/0xC2) en de oever-grastegel
(0x002) onder het water. Tot slot controleert het script de bereikbaarheid van alle events.

Tropische laag (v0.9.6): vanaf een golvende grens rond rij 11-16 jungle-groene bomen (palet 12) met lianen en
bromelia's, mangroves (Ekat99) en waterlelies in de grote poel, omgevallen bemoste stammen, wortelbogen (Ekat99),
bananenplanten en heliconia's (1x2, bovenkant over de speler), hibiscus en monstera, varens langs de bosranden,
bosbodem (bladeren/mos) en tropische bloemetjes. Elk blokkerend stuk wordt alleen geplaatst als de bereikbaarheids-
controle slaagt en er geen enkel vak afgesloten raakt. De bovenste SAFE rijen blijven Fortree-metatiles: vanuit Fortree
wordt de jungle met de Fortree-tileset getekend.

Rocket-sidequest: aan de noordrand van de zuidlus staat een reuzenpalm (18, 56-59) met een warp naar de Rocket-hideout
(rocket_hideout.py). De holte (METATILE_FortreeJungle_RocketHollow) zet scripts.inc pas als de quest loopt; daarvoor
een plat stukje zonder lang gras en een wachtpost (object achteraan). Dit gebeurt na de tropische laag, zodat de rest
van de jungle gelijk blijft.

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
    if palms >= 14:
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
blocked = {(x, y) for x, y, *_ in TRAINERS + ITEMS + NPCS}
BLOCK = set()            # vakken die de tropische laag hieronder dichtzet (stammen, mangroves, struiken)


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


def near(x, y, s):
    return any((x + dx, y + dy) in s for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))


def check(extra=()):
    """Alle events bereikbaar met BLOCK (+ extra) dicht? Geeft (lopend, met Surf) terug of AssertionError."""
    shut = blocked | BLOCK | set(extra)
    walk = bfs([ENTR[0]], lambda x, y: T[y][x] in WALK and (x, y) not in shut)
    assert ENTR[-1] in walk, 'oostingang niet verbonden met de westingang'
    surf = bfs(list(walk), lambda x, y: (T[y][x] in WALK or T[y][x] == 'w') and (x, y) not in shut)
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
    return walk, surf


walk0, surf0 = check()

# ---------------------------------------------------------------- tropische laag (tileset fortree_jungle)
# Alles hieronder gebruikt metatiles die alleen in fortree_jungle bestaan (achter de Fortree-metatiles). Vanuit
# Fortree wordt de jungle met de Fortree-tileset getekend: de bovenste SAFE rijen blijven daarom origineel.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jungle_tileset as J
ts = J.JungleTileset()
SAFE = 10
JRNG = random.Random(SEED + 1)
EVENT_CELLS = {(x, y) for x, y, *_ in TRAINERS + ITEMS + NPCS} | {(x, y) for x, y, *_ in HIDDEN} | \
              {(x, y) for x, y, _ in SIGNS}
KEEP = set()             # geen blokkerend decor: rond events, zichtlijnen van trainers, Zarude- en Ogerpon-plek
for x, y in EVENT_CELLS:
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            KEEP.add((x + dx, y + dy))
for x, y, face, *_ in TRAINERS:
    d = {'UP': (0, -1), 'DOWN': (0, 1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}.get(face, (0, 0))
    for k in range(1, 6):
        KEEP.add((x + d[0] * k, y + d[1] * k))
for y in range(H):
    for x in range(W):
        if (x - 9) ** 2 + (y - 60) ** 2 <= 30 or (x - 31) ** 2 + (y - 54) ** 2 <= 22:
            KEEP.add((x, y))


def mid(x, y):
    return M[y][x] & 0x3FF


def put(x, y, mt, coll=None):
    v = M[y][x]
    c = (v >> 10) & 3 if coll is None else coll
    M[y][x] = mt | (c << 10) | (v & 0xF000)


# 1. jungle-groene bomen vanaf een golvende grens (rij SAFE+1 .. SAFE+6), palmkruinen over bos gaan mee
TREEISH = set(FOREST) | set(TRUNK) | set(CANOPY) | {0x248, 0x249, 0x24A, 0x250, 0x251, 0x252, 0x273}
ph1, ph2 = JRNG.random() * 6.28, JRNG.random() * 6.28
EDGE = [SAFE + 1 + round(2.5 + 1.6 * math.sin(x * 0.42 + ph1) + 0.9 * math.sin(x * 1.1 + ph2)) for x in range(W)]
JUNGLE = set()
for y in range(SAFE, H):
    for x in range(W):
        if mid(x, y) in TREEISH and y >= EDGE[x]:
            JUNGLE.add((x, y))
for y in range(SAFE, H):          # boomkruin boven een vrij vak hoort bij de boom eronder
    for x in range(W):
        if mid(x, y) in CANOPY and y + 1 < H:
            (JUNGLE.add if (x, y + 1) in JUNGLE else JUNGLE.discard)((x, y))
VINE_X = (3, 11)
lianas = epis = 0
done = set()
for y in range(H - 1, SAFE - 1, -1):
    for x in range(W):
        if (x, y) not in JUNGLE or (x, y) in done:
            continue
        m = mid(x, y)
        if m in TRUNK and JRNG.random() < 0.45:
            vx, ph = JRNG.choice(VINE_X), JRNG.choice((0.0, 2.0))
            length = JRNG.choice((9, 11, 13))
            put(x, y, ts.recolor(m, draw=lambda cv, vx=vx, ph=ph, l=length: J.vine(cv, vx, 0, l, ph, tip=True)))
            lianas += 1
            yy = y - 1                          # liaan loopt door in de kruinen erboven
            while yy >= SAFE and (x, yy) in JUNGLE and mid(x, yy) in FOREST:
                put(x, yy, ts.recolor(mid(x, yy), draw=lambda cv, vx=vx, ph=ph: J.vine(cv, vx, 0, 16, ph)))
                done.add((x, yy))
                if JRNG.random() < 0.5:
                    break
                yy -= 1
        elif m in FOREST and JRNG.random() < 0.05 and all(kind(x + dx, y + dy) == 'T' for dx in (-1, 0, 1)
                                                          for dy in (-1, 0, 1)):
            cx, cy, col = JRNG.choice(((5, 6, 10), (10, 9, 12), (8, 5, 10), (6, 10, 12)))
            put(x, y, ts.recolor(m, draw=lambda cv, cx=cx, cy=cy, col=col: J.bromeliad(cv, cx, cy, col)))
            epis += 1
        elif m in TREEISH:
            put(x, y, ts.jungle(m))
print('jungle: %d boomvakken groen, %d lianen, %d bromelia\'s' % (len(JUNGLE), lianas, epis))


# 2. decor: stempels die een basis-metatile zonder bovenlaag overschilderen
def stamp(x0, y0, cv, pal, base_ok, block=True, layer=1, top_layer=None):
    """Zet cv (veelvoud van 16) op de kaart vanaf (x0, y0). False als het niet past of iets afsluit.
    layer 1 = onder de speler (covered); top_layer 0 = bovenste rij begaanbaar en over de speler (hoge plant)."""
    w, h = cv.w // 16, cv.h // 16
    cells = [(x0 + i, y0 + j) for j in range(h) for i in range(w)]
    for x, y in cells:
        if not inb(x, y) or y < SAFE or mid(x, y) not in base_ok or (x, y) in BLOCK or (block and (x, y) in KEEP):
            return False
    shut = []
    if block:
        shut = cells if top_layer is None else cells[w:]
        try:
            walk, _ = check(shut)
        except AssertionError:
            return False
        if len(walk) != len(walk0 - BLOCK - set(shut)):
            return False                                           # er raakt een stukje afgesloten
    for j in range(h):
        for i in range(w):
            x, y = x0 + i, y0 + j
            lay = top_layer if (top_layer is not None and j == 0) else layer
            put(x, y, ts.overlay(mid(x, y), cv, i * 16, j * 16, pal, layer=lay), 1 if (x, y) in shut else None)
    BLOCK.update(shut)
    return True


def edge_nook(x, y, need=3, space=12):
    """Open vak aan de bosrand in een ruime plek (niet midden in een smal pad)."""
    t = sum(kind(x + dx, y + dy) == 'T' for dx in (-1, 0, 1) for dy in (-1, 0, 1))
    room = sum(kind(x + dx, y + dy) in 'gLpf' for dx in range(-2, 3) for dy in range(-2, 3))
    return t >= need and room >= space


GR = {GRASS}
WATER_IN = {0xA1}
placed = {}


SPOTS = []


def count(name, x=None, y=None):
    placed[name] = placed.get(name, 0) + 1
    if x is not None:
        SPOTS.append((name, x, y))


def spaced(name, x, y, same=6, other=2):
    """Niet te dicht bij ander blokkerend decor (zelfde soort: same vakken, andere soort: other)."""
    return all(max(abs(x - a), abs(y - b)) >= (same if n == name else other) for n, a, b in SPOTS)


# mangroves in de grote poel (wortels in het water)
for x0, y0, big in ((29, 34, True), (25, 34, False), (28, 33, True), (26, 33, False)):
    if placed.get('mangrove', 0) >= 2:
        break
    if stamp(x0, y0, J.mangrove(big, True), J.P_JUNGLE, WATER_IN):
        count('mangrove')
# waterlelies op de poel (je surft er gewoon overheen)
for _ in range(80):
    x, y = JRNG.randrange(24, 33), JRNG.randrange(31, 37)
    if placed.get('lotus', 0) < 5 and stamp(x, y, J.lotus(JRNG.randrange(2)), J.P_FLOWER, WATER_IN, block=False):
        count('lotus')
cands = [(x, y) for y in range(SAFE, H - 1) for x in range(1, W - 1)]
JRNG.shuffle(cands)


def against_forest(x, y, n, deep=2):
    """n vakken vanaf (x, y) liggen direct onder de bosrand en daaronder blijft het pad nog deep vakken breed."""
    return all(kind(x + i, y - 1) == 'T' and all(kind(x + i, y + k) in 'gLpf' for k in range(1, deep + 1))
               for i in range(n))


# omgevallen stammen tegen de bosrand (natuurlijke barrieres in open plekken)
for x, y in cands:
    if placed.get('log', 0) >= 8:
        break
    n = JRNG.choice((2, 3))
    free = all(kind(x + i, y + k) in 'gLpf' for i in range(-1, n + 1) for k in (-2, -1, 1, 2))   # midden in een open plek
    if (against_forest(x, y, n) or free) and spaced('log', x, y, 6) and stamp(x, y, J.log(n), J.P_JUNGLE, GR):
        count('log', x, y)
# wortelbogen (Ekat99)
for x, y in cands:
    if placed.get('arch', 0) >= 6:
        break
    if against_forest(x, y, 2) and spaced('arch', x, y) and stamp(x, y, J.root_arch(False), J.P_JUNGLE, GR):
        count('arch', x, y)
# hoge planten (1x2): bananenplant en heliconia tegen de bosrand; het bovenste vak is begaanbaar en valt over de
# speler heen
for x, y in cands:
    if placed.get('tall', 0) >= 16:
        break
    if against_forest(x, y, 1, 3) and spaced('tall', x, y, 3):
        cv, pal = (J.banana(), J.P_JUNGLE) if JRNG.random() < 0.5 else (J.heliconia(), J.P_FLOWER)
        if stamp(x, y, cv, pal, GR, top_layer=0):
            count('tall', x, y)
# struiken (1x1): hibiscus en monstera; de oude Fortree-struikjes worden ook tropisch
for y in range(SAFE, H):
    for x in range(W):
        if T[y][x] == 'b':
            BLOCK.add((x, y))
            plant = (J.hibiscus(JRNG.randrange(2)), J.P_FLOWER) if JRNG.random() < 0.6 else (J.monstera(), J.P_JUNGLE)
            put(x, y, ts.overlay(GRASS, plant[0], 0, 0, plant[1], layer=1), 1)
for x, y in cands:
    if placed.get('bush', 0) >= 16:
        break
    if edge_nook(x, y, 3, 11) and spaced('bush', x, y, 4):
        cv, pal = (J.hibiscus(JRNG.randrange(2)), J.P_FLOWER) if JRNG.random() < 0.45 else (J.monstera(), J.P_JUNGLE)
        if stamp(x, y, cv, pal, GR):
            count('bush', x, y)
# varens langs de bosranden en bloemetjes in open plekken (begaanbaar, onder de speler)
for x, y in cands:
    if mid(x, y) != GRASS or (x, y) in EVENT_CELLS:
        continue
    t = sum(kind(x + dx, y + dy) == 'T' for dx in (-1, 0, 1) for dy in (-1, 0, 1))
    if t >= 2 and JRNG.random() < 0.45:
        if stamp(x, y, J.fern(JRNG.randrange(2)), J.P_JUNGLE, GR, block=False):
            count('fern')
    elif t == 0 and JRNG.random() < 0.07:
        if stamp(x, y, J.groundflowers(JRNG.randrange(2)), J.P_FLOWER, GR, block=False):
            count('flowers')
    elif JRNG.random() < 0.3:
        if stamp(x, y, J.litter(JRNG.randrange(3)), J.P_JUNGLE, GR, block=False):
            count('litter')
# de rode General-bloemen in de jungle worden tropische bloemetjes (niet bij het altaar van Ogerpon)
for y in range(SAFE, H):
    for x in range(W):
        if mid(x, y) == FLOWER and (x - 31) ** 2 + (y - 54) ** 2 > 22:
            put(x, y, GRASS)
            stamp(x, y, J.groundflowers(1), J.P_FLOWER, GR, block=False)


# 3. Rocket-hideout (sidequest, v0.9.x): een reuzenpalm aan de noordrand van de zuidlus, met aan zijn voet een holte die
# pas open is als de quest loopt (setmetatile in scripts.inc op METATILE_FortreeJungle_RocketHollow, zie
# include/constants/metatile_labels.h). Komt helemaal aan het eind, zodat de rest van de jungle (rng) gelijk blijft.
ROCKET_DOOR = (18, 59)                  # voet van de palm (warp); de speler loopt er vanuit het zuiden in
ROCKET_GUARD = (19, 60)                 # grunt die de wacht houdt (alleen zichtbaar als de quest loopt)
for dy in range(-4, 1):
    for dx in range(-2, 3):
        x, y = ROCKET_DOOR[0] + dx, ROCKET_DOOR[1] + dy
        assert T[y][x] == 'T' and (x, y) not in KEEP, ('reuzenpalm Rocket past niet', x, y)
for dy in range(4):
    for dx in range(3):
        m = PALM[dy][dx]
        put_mt = ts.jungle(m) if m in TREEISH else m
        M[ROCKET_DOOR[1] - 3 + dy][ROCKET_DOOR[0] - 1 + dx] = val(put_mt, 1, 3 if (dy, dx) == (3, 1) else 0)
# voor de palm een plat stukje (geen lang gras: daarin verdwijnt de grunt met zijn donkere pet helemaal)
for dx in (-1, 0, 1):
    x, y = ROCKET_DOOR[0] + dx, ROCKET_DOOR[1] + 1
    assert T[y][x] in 'gL'
    T[y][x] = 'g'
    M[y][x] = val(GRASS, 0, 3)
    stamp(x, y, J.litter(1 + dx % 2), J.P_JUNGLE, GR, block=False)


def rocket_hollow():
    """Palmvoet (0x273) met een donkere holte onderin de stam; gedrag MB_NON_ANIMATED_DOOR (0x60)."""
    b, t, at = ts.base(0x273)
    cv = J.Canvas(16, 16)
    for k, e in enumerate(b):
        ti, hf, vf = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1
        src = ts.tiles[ti - 512] if ti >= 512 else ts.gtiles[ti]
        for y in range(8):
            for x in range(8):
                cv.p[(k // 2) * 8 + y][(k % 2) * 8 + x] = src[7 - y if vf else y][7 - x if hf else x]
    for y in range(4, 16):                      # boog: 8 breed, bovenkant rond
        half = 4 if y >= 7 else (2, 3, 4)[y - 4]
        for x in range(8 - half, 8 + half):
            edge = x in (8 - half, 7 + half) or y == 4
            cv.p[y][x] = 8 if edge else 9       # palet 9: 8 donkerblauw (rand), 9 zwart (holte)
    for y in range(5, 16):
        cv.p[y][8 - (4 if y >= 7 else (2, 3, 4)[min(y - 4, 2)]) - 1] = 7
    # bovenlaag (boomkruinen naast de voet) in het midden open, anders valt de holte erachter weg
    top = J.Canvas(16, 16)
    tj = ts.jungle_entries(t)
    for k, e in enumerate(tj):
        ti, hf, vf = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1
        src = ts.tiles[ti - 512] if ti >= 512 else ts.gtiles[ti]
        for y in range(8):
            for x in range(8):
                top.p[(k // 2) * 8 + y][(k % 2) * 8 + x] = src[7 - y if vf else y][7 - x if hf else x]
    for y in range(2, 16):
        for x in range(3, 13):
            top.p[y][x] = 0
    return ts.metatile(ts.cut(cv, 0, 0, b[0] >> 12), ts.cut(top, 0, 0, tj[0] >> 12), (at & 0xF000) | 0x60)


ROCKET_HOLLOW = rocket_hollow()
print('Rocket-holte: metatile 0x%X op %s' % (ROCKET_HOLLOW, ROCKET_DOOR))
ml = open('include/constants/metatile_labels.h').read()
LBL = '#define METATILE_FortreeJungle_RocketHollow'
line = '%s                0x%X // Project Grounded: tools/grounded/maptools/fortree_jungle.py\n' % (LBL, ROCKET_HOLLOW)
if LBL in ml:
    i = ml.index(LBL)
    ml = ml[:i] + line + ml[ml.index('\n', i) + 1:]
else:
    i = ml.index('// gTileset_Fortree\n')
    ml = ml[:i] + '// gTileset_FortreeJungle\n' + line + '\n' + ml[i:]
open('include/constants/metatile_labels.h', 'w').write(ml)

for y in range(SAFE):
    for x in range(W):
        assert mid(x, y) < ts.first, ('nieuwe metatile in het vanuit Fortree zichtbare deel', x, y)
ntiles, nmts = ts.save()
walk, surf = check()
assert (ROCKET_DOOR[0], ROCKET_DOOR[1] + 1) in walk and ROCKET_GUARD in walk and \
    (ROCKET_DOOR[0], ROCKET_DOOR[1] + 1) not in BLOCK, 'Rocket-ingang onbereikbaar'
print('tropisch:', placed, '| %d nieuwe tiles (van %d vrij), %d nieuwe metatiles' % (ntiles, ts.nfree, nmts))
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
# Rocket-sidequest: wachtpost bij de holle reuzenpalm (achteraan, zodat de nummers van de andere objecten blijven)
objs.append(obj('OBJ_EVENT_GFX_ROCKET_GRUNT_M', ROCKET_GUARD[0], ROCKET_GUARD[1], 'MOVEMENT_TYPE_FACE_LEFT',
                'TRAINER_TYPE_NORMAL', 2, 'FortreeJungle_EventScript_RocketGuard', 'FLAG_HIDE_JUNGLE_ROCKET_GUARD'))
mj = {
    "id": "MAP_FORTREE_JUNGLE", "name": "FortreeJungle", "layout": "LAYOUT_FORTREE_JUNGLE",
    "music": "MUS_ROUTE119", "region_map_section": "MAPSEC_FORTREE_JUNGLE", "requires_flash": False,
    "weather": "WEATHER_JUNGLE_CYCLE", "map_type": "MAP_TYPE_ROUTE", "allow_cycling": True,
    "allow_escaping": False, "allow_running": True, "show_map_name": True,
    "battle_scene": "MAP_BATTLE_SCENE_NORMAL",
    "connections": [{"map": "MAP_FORTREE_CITY", "offset": 0, "direction": "up"}],
    "object_events": objs,
    "warp_events": [{"x": ROCKET_DOOR[0], "y": ROCKET_DOOR[1], "elevation": 0, "dest_map": "MAP_ROCKET_HIDEOUT_1F",
                     "dest_warp_id": "0"}],
    "coord_events": [],
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
      "secondary_tileset": "gTileset_FortreeJungle",
      "border_filepath": "data/layouts/FortreeJungle/border.bin",
      "blockdata_filepath": "data/layouts/FortreeJungle/map.bin"
    }''' % (W, H) + lj[j:]
    open('data/layouts/layouts.json', 'w').write(lj)
i = lj.index('"LAYOUT_FORTREE_JUNGLE"')
j = lj.index('}', i)
if '"gTileset_Fortree"' in lj[i:j]:                    # oudere versie (v0.9.5) gebruikte Fortree zelf
    lj = lj[:i] + lj[i:j].replace('"gTileset_Fortree"', '"gTileset_FortreeJungle"') + lj[j:]
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
    render(M, 'general', 'fortree_jungle').save(sys.argv[1])
    MR = [row[:] for row in M]                        # zoals tijdens de Rocket-quest: holte open
    MR[ROCKET_DOOR[1]][ROCKET_DOOR[0]] = val(ROCKET_HOLLOW, 0, 3)
    render(MR, 'general', 'fortree_jungle').save(sys.argv[1].replace('.png', '_rocket.png'))
print('klaar')
