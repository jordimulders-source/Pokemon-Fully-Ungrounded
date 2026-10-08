"""Project Grounded: eb en vloed op Route 132 + Juans eiland op Route 129.

1. Pacifidlog-tileset: achteraan 13 kopieen van de General-zandset (midden, randen, binnenhoeken) met gedrag
   MB_DEEP_SAND ("slik": wilde Pokemon, je zakt erin weg). Vanilla-nummers blijven gelijk.
2. Route 132: tweede layout `Route132_LowTide` (eb). Ten noorden van het zandeiland (x 44-58, y 22-35) valt een
   wad droog (x 46-61, y 11-21): ondiep water met slikvlakken, rotsen op het wad, een strandjutter en verborgen
   items. Bij vloed (gewone layout) is daar zee met stroming. Het map-script kiest de layout bij binnenkomst.
3. Route 129: Juans eiland rond (40,9): ondiepe rand, strand met palmen en in het midden een lagune
   ("waterpodium"). De objecten staan in map.json.

Idempotent (bouwt alles opnieuw uit de vloed-layout / zet het vak van Juans eiland eerst terug op zee) en
controleert de bereikbaarheid. Gebruik: python3 tools/grounded/maptools/tides_juan.py [rendermap]"""
import os, re, struct, sys
from collections import deque

BLOCK, E1, E3 = 1 << 10, 1 << 12, 3 << 12

# --- gedrag per metatile (voor elevation en bereikbaarheid) ---
BEH = {}
for l in open('include/constants/metatile_behaviors.h'):
    m = re.match(r'\s*(MB_\w+)', l)
    if m and m.group(1) not in BEH:
        BEH[m.group(1)] = len(BEH)
MB = {v: k for k, v in BEH.items()}


def attrs(path):
    a = open(path, 'rb').read()
    return [struct.unpack_from('<H', a, i * 2)[0] for i in range(len(a) // 2)]


GEN = attrs('data/tilesets/primary/general/metatile_attributes.bin')
SURF = {'MB_OCEAN_WATER', 'MB_DEEP_WATER', 'MB_POND_WATER', 'MB_INTERIOR_DEEP_WATER', 'MB_SOOTOPOLIS_DEEP_WATER',
        'MB_WESTWARD_CURRENT', 'MB_EASTWARD_CURRENT', 'MB_NORTHWARD_CURRENT', 'MB_SOUTHWARD_CURRENT', 'MB_SEAWEED',
        'MB_WATERFALL', 'MB_NO_SURFACING'}

# --- 1. slik-metatiles achteraan Pacifidlog ---
PAC = 'data/tilesets/secondary/pacifidlog/'
PAC_N = 203  # vanilla-aantal
SAND = {'C': 0x124, 'TL': 0x195, 'T': 0x196, 'TR': 0x197, 'L': 0x19D, 'R': 0x19F, 'BL': 0x1A5, 'B': 0x1A6,
        'BR': 0x1A7, 'NW': 0x185, 'NE': 0x186, 'SW': 0x18D, 'SE': 0x18E}
gm = open('data/tilesets/primary/general/metatiles.bin', 'rb').read()
pm = open(PAC + 'metatiles.bin', 'rb').read()[:PAC_N * 16]
pa = open(PAC + 'metatile_attributes.bin', 'rb').read()[:PAC_N * 2]
DEEP = {}
for i, (k, src) in enumerate(SAND.items()):
    DEEP[k] = 0x200 + PAC_N + i
    pm += gm[src * 16:src * 16 + 16]
    pa += struct.pack('<H', (GEN[src] & 0xF000) | BEH['MB_DEEP_SAND'])
open(PAC + 'metatiles.bin', 'wb').write(pm)
open(PAC + 'metatile_attributes.bin', 'wb').write(pa)
PACA = attrs(PAC + 'metatile_attributes.bin')
MOSA = attrs('data/tilesets/secondary/mossdeep/metatile_attributes.bin')


def beh(mt, sec):
    mt &= 0x3FF
    a = GEN[mt] if mt < 0x200 else sec[mt - 0x200]
    return MB.get(a & 0xFF, a & 0xFF)


def cell(mt, sec, blocked=False):
    return mt | (E1 if beh(mt, sec) in SURF else E3) | (BLOCK if blocked else 0)


# --- autotiling (General-rand van ondiep water + zand) ---
RING = {'TL': 0x1AD, 'T': 0x1AE, 'TR': 0x1AF, 'L': 0x1B5, 'R': 0x1B7, 'BL': 0x1BD, 'B': 0x1BE, 'BR': 0x1BF,
        'NW': 0x19B, 'NE': 0x19C, 'SW': 0x1A3, 'SE': 0x1A4, 'C': 0x19E}
ROCK_WATER = [0x150, 0x151, 0x158, 0x159]
ROCK_SHALLOW = [0x15E, 0x15F, 0x16E, 0x16F]
ROCK_SAND = [0x0A3, 0x0A4, 0x0AB, 0x0AC]
PALM = [0x308, 0x309, 0x310, 0x311]


def shape(S, x, y):
    has = lambda dx, dy: (x + dx, y + dy) in S
    n, s, w, e = has(0, -1), has(0, 1), has(-1, 0), has(1, 0)
    if not n and not w: return 'TL'
    if not n and not e: return 'TR'
    if not s and not w: return 'BL'
    if not s and not e: return 'BR'
    if not n: return 'T'
    if not s: return 'B'
    if not w: return 'L'
    if not e: return 'R'
    if not has(-1, -1): return 'NW'
    if not has(1, -1): return 'NE'
    if not has(-1, 1): return 'SW'
    if not has(1, 1): return 'SE'
    return 'C'


def thin(S):
    """Haal 1 breed uit een vorm (de randtiles bestaan alleen voor vormen van minstens 2 breed)."""
    S = set(S)
    while True:
        bad = {(x, y) for (x, y) in S if ((x, y - 1) not in S and (x, y + 1) not in S)
               or ((x - 1, y) not in S and (x + 1, y) not in S)}
        if not bad: return S
        S -= bad


def rows(spec):
    return {(x, y) for y, (a, b) in spec.items() for x in range(a, b + 1)}


def rects(*rs):
    return {(x, y) for (x0, y0, x1, y1) in rs for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}


def load(name, w, h):
    b = open('data/layouts/%s/map.bin' % name, 'rb').read()
    return [[struct.unpack_from('<H', b, (y * w + x) * 2)[0] for x in range(w)] for y in range(h)]


def save(name, v):
    os.makedirs('data/layouts/' + name, exist_ok=True)
    open('data/layouts/%s/map.bin' % name, 'wb').write(b''.join(struct.pack('<H', c) for r in v for c in r))


def reach(v, sec, start, targets, label):
    """Lopen over niet-geblokkeerde, niet-surfbare tegels (bij eb moet alles te voet bereikbaar zijn)."""
    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if p in seen or not (0 <= p[0] < len(v[0]) and 0 <= p[1] < len(v)): continue
            c = v[p[1]][p[0]]
            if c & BLOCK or beh(c, sec) in SURF: continue
            seen.add(p); q.append(p)
    miss = [t for t in targets if t not in seen]
    if miss: print('%s: niet bereikbaar: %s' % (label, miss)); FAIL.append(label)
    return seen


FAIL = []
RING_ALL = set(RING.values()) | {0x246, 0x247, 0x256, 0x257, 0x25E, 0x25F, 0x266, 0x267, 0x23E, 0x23F, 0x24E, 0x24F}

# --- 2. Route 132 bij eb ---
W, H = 80, 40
v = load('Route132', W, H)
ROCKS_ALL = set(ROCK_WATER) | {0x175, 0x176, 0x17D, 0x17E}
OLD = {(x, y) for x in range(40, 62) for y in range(22, 36) if (v[y][x] & 0x3FF) not in ROCKS_ALL
       and (beh(v[y][x], PACA) not in SURF or (v[y][x] & 0x3FF) in RING_ALL)}
FLAT = rows({11: (51, 59), 12: (49, 61), 13: (48, 61), 14: (47, 61), 15: (47, 61), 16: (47, 61), 17: (47, 61),
             18: (46, 60), 19: (46, 60), 20: (46, 59), 21: (46, 58)})
# rotsen: helemaal op het wad (met rand) -> rots op ondiep water, anders blijft de rots in zee en wijkt het wad
rocks = [(x, y) for (x, y) in FLAT if (v[y][x] & 0x3FF) == ROCK_WATER[0]]
keep_rocks = []
SWEEP = {(53, 15), (55, 15)}  # deze rotsen verdwijnen bij eb onder het slik (anders sluiten ze het wad af)
for (x, y) in rocks:
    if (x, y) in SWEEP:
        continue
    blk = rects((x - 1, y - 1, x + 2, y + 2))
    if blk <= FLAT:
        keep_rocks.append((x, y))
    else:
        FLAT -= rects((x, y, x + 1, y + 1))
LAND = thin(FLAT | OLD)
NEW = LAND - OLD
rock_cells = {(x + i % 2, y + i // 2): ROCK_SHALLOW[i] for (x, y) in keep_rocks for i in range(4)}
# slik: het binnenste van het wad, met een ondiepe rand rond de rotsen en een paar getijdenpoelen
INNER = {p for p in NEW if all((p[0] + dx, p[1] + dy) in LAND for dx in (-1, 0, 1) for dy in (-1, 0, 1))}
POOLS = rects((57, 15, 58, 16), (50, 19, 51, 20), (53, 13, 54, 13))
SLIK = INNER - POOLS - rects(*[(x, y, x + 1, y + 1) for (x, y) in keep_rocks])
SLIK = thin(SLIK)
for (x, y) in LAND:
    near_new = any((x + dx, y + dy) in NEW for dx in (-1, 0, 1) for dy in (-1, 0, 1))
    if (x, y) in OLD and not ((v[y][x] & 0x3FF) in RING_ALL and near_new):
        continue
    if (x, y) in rock_cells:
        v[y][x] = cell(rock_cells[(x, y)], PACA, True)
    elif (x, y) in SLIK:
        v[y][x] = cell(DEEP[shape(SLIK, x, y)], PACA)
    else:
        v[y][x] = cell(RING[shape(LAND, x, y)], PACA)
save('Route132_LowTide', v)
R132 = reach(v, PACA, (50, 26), [], 'Route 132 eb')
LOST = sorted(p for p in NEW if p not in R132 and not v[p[1]][p[0]] & BLOCK and beh(v[p[1]][p[0]], PACA) not in SURF)
if LOST: print('niet bereikbaar op het wad:', LOST); FAIL.append('wad')
reach(v, PACA, (50, 26), [(56, 14), (60, 14), (47, 20)], 'Route 132 eb (strandjutter, verborgen items)')
v132 = v

# --- 3. Route 129: Juans eiland ---
W, H = 80, 40
v = load('Route129', W, H)
for y in range(4, 16):
    for x in range(35, 48):
        v[y][x] = 0x170 | E1
ISLAND = thin(rows({4: (39, 44), 5: (37, 46), 6: (35, 47), 7: (35, 47), 8: (35, 47), 9: (35, 47), 10: (35, 47),
                    11: (35, 47), 12: (35, 47), 13: (37, 46), 14: (39, 44)}))
BEACH = rows({5: (40, 43), 6: (38, 45), 7: (36, 46), 8: (36, 46), 9: (36, 46), 10: (36, 46), 11: (36, 46),
              12: (38, 45), 13: (40, 43)}) & ISLAND
LAGOON = rects((40, 8, 42, 10))  # het waterpodium: ondiep water midden in het strand
BEACH = thin(BEACH - LAGOON)
for (x, y) in ISLAND:
    if (x, y) in BEACH:
        v[y][x] = cell(SAND[shape(BEACH, x, y)], MOSA)
    else:
        v[y][x] = cell(RING[shape(ISLAND, x, y)], MOSA)
# palmen (2x2) alleen op vol zand
PALMS = [(37, 8), (44, 9)]
for (px, py) in PALMS:
    for i in range(4):
        cx, cy = px + i % 2, py + i // 2
        assert (v[cy][cx] & 0x3FF) == SAND['C'], 'palm (%d,%d) niet op vol zand' % (px, py)
        v[cy][cx] = cell(PALM[i], MOSA, i >= 2)
save('Route129', v)
reach(v, MOSA, (40, 6), [(41, 7), (36, 9), (46, 9), (40, 12), (41, 9), (43, 7), (39, 11)], 'Juans eiland')

if len(sys.argv) > 1:  # voorbeeld: beide eilanden vergroot, met rasternummers
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from gridrender import render
    from PIL import Image, ImageDraw
    parts = []
    for vv, sec, (x0, y0, x1, y1) in [(v132, 'pacifidlog', (36, 4, 64, 36)), (v, 'mossdeep', (30, 0, 50, 18))]:
        im = render([r[x0:x1] for r in vv[y0:y1]], 'general', sec)
        im = im.resize((im.width * 2, im.height * 2), Image.NEAREST)
        d = ImageDraw.Draw(im)
        for x in range(x0, x1):
            d.text(((x - x0) * 32 + 2, 0), str(x % 100), fill=(255, 0, 0))
        for y in range(y0, y1):
            d.text((0, (y - y0) * 32 + 10), str(y), fill=(255, 0, 0))
        parts.append(im)
    out = Image.new('RGB', (sum(p.width for p in parts), max(p.height for p in parts)))
    ox = 0
    for p in parts:
        out.paste(p, (ox, 0)); ox += p.width
    out.save(sys.argv[1])
assert not FAIL, FAIL
if os.environ.get('DBG'):
    for y in range(9, 24):
        print('%2d ' % y + ''.join('#' if v132[y][x] & BLOCK else '~' if beh(v132[y][x], PACA) in SURF else ('s' if (x, y) in SLIK else 'r' if (x, y) in R132 else '?') for x in range(44, 63)))
