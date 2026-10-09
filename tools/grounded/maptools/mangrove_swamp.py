"""Project Grounded: Mangrove Mire, een vochtig mangrovemoeras tussen Fortree Jungle en Route 120.

Bouwt (idempotent, vaste seed):
- tileset mangrove_mire (secondary, primary General): een LEGE secondary met eigen tiles achteraan. Paletten:
  6/7/12 = dezelfde jungle-paletten als fortree_jungle (mangroves, wortels, varens, bloemen, jungle-groene bomen),
  8 = moeras (gras, modder, troebel water, oeverschaduw). Modder en water zijn per vak getekend uit een veld over de
  3x3 buren (bilineair + vaste ruis), zodat poelen en modderplekken organisch rond lopen zonder vaste autotile-set.
  Plankenpaden (palet 6, hout) liggen als bovenlaag over het water.
- data/layouts/MangroveMire (56x44) + data/maps/MangroveMire/map.json (objecten, coord-triggers, borden).
- Route 120 (alleen de westrand): een bord op (1, 59) en coord-triggers op (0, 60-61) naar het moeras.
- Registratie: layouts.json, map_groups.json (gMapGroup_Grounded), event_scripts.s, tileset-headers.
De scripts.inc staat met de hand in data/maps/MangroveMire.

Verbindingen (andere tileset dan jungle en Route 120, dus warps via coord-triggers zoals Route 136 -> Ashfrost):
west (0, 21-22) <-> Fortree Jungle (39, 39-40); oost (55, 29-30) <-> Route 120 (0, 60-61).
Het script controleert de bereikbaarheid: van west naar oost zonder Surf; trainers, items en borden bereikbaar; het
Mystic Water-eiland alleen surfend.

Gebruik: python3 tools/grounded/maptools/mangrove_swamp.py [voorbeeld.png]"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
import json, math, os, random, struct, sys
from collections import deque
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jungle_tileset as J

W, H = 56, 44
SEED = 453  # Croagunk
rng = random.Random(SEED)
TS = 'data/tilesets/secondary/mangrove_mire'
P_SWAMP = 8

# ---------------------------------------------------------------- terrein
# T bos, g gras, L hoog gras, w troebel water, m modder, k plankenpad, b blokkerend decor (later)
T = [['T'] * W for _ in range(H)]


def inb(x, y):
    return 0 <= x < W and 0 <= y < H


def kind(x, y):
    return T[y][x] if inb(x, y) else 'T'


def disc(cx, cy, r, k, only=None, sy=1.15):
    for y in range(int(cy - r - 2), int(cy + r + 3)):
        for x in range(int(cx - r - 2), int(cx + r + 3)):
            if 1 < x < W - 2 and 1 < y < H - 2 and (x - cx) ** 2 + ((y - cy) * sy) ** 2 <= r * r:
                if only is None or T[y][x] in only:
                    T[y][x] = k


def blob(cx, cy, r, k, only=None, n=5):
    disc(cx, cy, r, k, only)
    for _ in range(n):
        a = rng.random() * 2 * math.pi
        d = r * (0.4 + 0.5 * rng.random())
        disc(cx + math.cos(a) * d, cy + math.sin(a) * d, r * (0.45 + 0.3 * rng.random()), k, only)


def path(pts, w=2, k='g', only=None):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(abs(x1 - x0), abs(y1 - y0)) * 3 + 1
        for i in range(n + 1):
            t = i / n
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            for dy in range(w):
                for dx in range(w):
                    xx, yy = int(round(x - (w - 1) / 2 + dx)), int(round(y - (w - 1) / 2 + dy))
                    if 0 < xx < W - 1 and 0 < yy < H - 1 and (only is None or T[yy][xx] in only):
                        T[yy][xx] = k


def rect(x0, y0, x1, y1, k):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            T[y][x] = k


# de grote lagune (troebel water) in het midden
blob(28, 22, 9.5, 'w', n=7)
blob(37, 17, 6, 'w', n=4)
blob(20, 30, 5, 'w', n=4)
blob(34, 31, 5.5, 'w', n=4)
# land: westweide met de ingang, noordwestelijke open plek, centraal eiland, oostoever met de uitgang
WEST_EXIT = [(0, 21), (0, 22)]
EAST_EXIT = [(W - 1, 29), (W - 1, 30)]
rect(0, 21, 5, 22, 'g')
blob(9, 22, 4.6, 'g', n=4)
path([(9, 19), (10, 13), (15, 9), (20, 8)], 2)
blob(21, 8, 3.6, 'g', n=3)
blob(27, 22, 3.2, 'g', n=3)                         # centraal eiland
blob(46, 29, 4.8, 'g', n=4)                         # oostoever
rect(W - 6, 29, W - 1, 30, 'g')
path([(46, 24), (47, 18), (50, 14)], 2)             # zijpad noordoost (verborgen item)
blob(41, 11, 2.4, 'g', n=2)                         # eilandje noordoost (alleen surfend)
blob(11, 33, 4.2, 'g', n=3)                         # zuidwest: modderplaat
path([(9, 25), (10, 30)], 2)
path([(45, 34), (44, 38), (40, 39)], 2)             # zuidoost: zakje met de TM
blob(40, 39, 2.2, 'g', n=2)
# plankenpaden over de lagune: west -> eiland, eiland -> oost (met een zijsteiger voor de visser)
BOARD = [((13, 22), (25, 22)), ((28, 23), (38, 23)), ((38, 23), (38, 28)), ((38, 28), (41, 28))]
for (x0, y0), (x1, y1) in BOARD:
    for x in range(min(x0, x1), max(x0, x1) + 1):
        for y in range(min(y0, y1), max(y0, y1) + 1):
            if T[y][x] != 'g':
                T[y][x] = 'k'
for y in (23, 24, 25):                              # steiger van de visser naar het zuiden
    T[y][18] = 'k'
# water dat aan de planken grenst moet water blijven (geen eiland-rand onder de planken)
# modder: plekken in de weides (begaanbaar) en de modderplaat
for cx, cy, r in ((8, 24, 1.8), (11, 34, 2.6), (22, 7, 1.4), (47, 31, 1.7), (9, 19, 1.2)):
    blob(cx, cy, r, 'm', only='g', n=2)
# hoog gras
for cx, cy, r in ((7, 20, 2.2), (12, 23, 1.6), (20, 10, 1.8), (27, 21, 1.6), (48, 27, 2.0), (13, 31, 1.6),
                  (43, 31, 1.4)):
    blob(cx, cy, r, 'L', only='g', n=2)

# opruimen: water/modder/hoog gras direct boven bos wordt gras (boomkruin), losse 1-brede bosvakjes openen
for _ in range(2):
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            if T[y][x] == 'T' and T[y - 1][x] in 'gLm' and T[y + 1][x] in 'gLm':
                T[y][x] = 'g'
for y in range(H - 1):
    for x in range(W):
        if T[y][x] in 'wmL' and T[y + 1][x] == 'T':
            T[y][x] = 'g'
for x, y in WEST_EXIT + EAST_EXIT:
    T[y][x] = 'g'

# ---------------------------------------------------------------- events
TRAINERS = [  # x, y, kijkrichting, gfx, script, zicht
    (18, 25, 'UP', 'OBJ_EVENT_GFX_FISHERMAN', 'MangroveMire_EventScript_Otto', 3),
    (21, 8, 'DOWN', 'OBJ_EVENT_GFX_HEX_MANIAC', 'MangroveMire_EventScript_Griselda', 4),
    (27, 21, 'LEFT', 'OBJ_EVENT_GFX_PICNICKER', 'MangroveMire_EventScript_Fern', 3),   # Pokemon Ranger
    (47, 27, 'TREE', 'OBJ_EVENT_GFX_NINJA_BOY', 'MangroveMire_EventScript_Kappa', 3),
]
ITEMS = [  # x, y, item, flag, surf
    (12, 35, 'ITEM_BLACK_SLUDGE', 'FLAG_ITEM_MANGROVE_MIRE_BLACK_SLUDGE', False),
    (41, 11, 'ITEM_MYSTIC_WATER', 'FLAG_ITEM_MANGROVE_MIRE_MYSTIC_WATER', True),
    (23, 7, 'ITEM_ABSORB_BULB', 'FLAG_ITEM_MANGROVE_MIRE_ABSORB_BULB', False),
    (40, 39, 'ITEM_TOXIC_ORB', 'FLAG_ITEM_MANGROVE_MIRE_TOXIC_ORB', False),
]
HIDDEN = [
    (10, 33, 'ITEM_BIG_ROOT', 'FLAG_HIDDEN_ITEM_MANGROVE_MIRE_BIG_ROOT'),
    (50, 14, 'ITEM_ULTRA_BALL', 'FLAG_HIDDEN_ITEM_MANGROVE_MIRE_ULTRA_BALL'),
]
SIGNS = [(4, 23, 'MangroveMire_EventScript_SignWest'), (50, 28, 'MangroveMire_EventScript_SignEast')]
for x, y, *_ in TRAINERS + ITEMS + HIDDEN:
    if T[y][x] not in 'gLmk':
        T[y][x] = 'g'
if os.environ.get('ASCII'):
    for y in range(H):
        print('%2d ' % y + ''.join(T[y]).replace('T', '#').replace('g', '.'))
for x, y, _ in SIGNS:
    assert T[y][x] in 'gLm', ('bord niet op open grond', x, y, T[y][x])
    T[y][x] = 's'

# ---------------------------------------------------------------- bereikbaarheid
WALK = set('gLmk')
blocked = {(x, y) for x, y, *_ in TRAINERS + ITEMS}
BLOCK = set()


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
    shut = blocked | BLOCK | set(extra)
    walk = bfs([WEST_EXIT[0]], lambda x, y: T[y][x] in WALK and (x, y) not in shut)
    for c in WEST_EXIT + EAST_EXIT:
        assert c in walk, ('uitgang niet lopend bereikbaar', c)
    surf = bfs(list(walk), lambda x, y: (T[y][x] in WALK or T[y][x] == 'w') and (x, y) not in shut)
    for x, y, *_ in TRAINERS:
        assert near(x, y, walk), ('trainer onbereikbaar', x, y)
    for x, y, item, _, by_surf in ITEMS:
        assert near(x, y, surf if by_surf else walk), ('item onbereikbaar', item)
        if by_surf:
            assert not near(x, y, walk), ('item hoort alleen surfend bereikbaar', item)
    for x, y, item, _ in HIDDEN:
        assert (x, y) in walk, ('verborgen item onbereikbaar', item)
    for x, y, _ in SIGNS:
        assert near(x, y, walk), ('bord onbereikbaar', x, y)
    return walk, surf


walk0, surf0 = check()


# ---------------------------------------------------------------- tileset
class SwampTileset(J.JungleTileset):
    """Lege secondary: alleen eigen tiles/metatiles (vanaf 0x200), paletten 6/7/12 van de jungle + 8 moeras."""

    def __init__(self):
        os.makedirs(TS + '/palettes', exist_ok=True)
        self.tiles = [[[0] * 8 for _ in range(8)] for _ in range(512)]
        self.pngpal = Image.open(J.GEN + '/tiles.png').getpalette()
        self.gtiles, _ = J.png_tiles(J.GEN + '/tiles.png')
        self.gmts = open(J.GEN + '/metatiles.bin', 'rb').read()
        self.gattr = open(J.GEN + '/metatile_attributes.bin', 'rb').read()
        self.mts, self.attrs = bytearray(), bytearray()
        self.first = 512
        self.free = list(range(1, 512))
        self.nfree = len(self.free)
        self.tidx, self.midx = {}, {}
        gp = J.read_pal(J.GEN + '/palettes/02.pal')
        self.pals = [[(0, 0, 0)] * 16 for _ in range(16)]
        self.pals[J.P_TREE] = [J.q(J.PAL12.get(i, gp[i])) for i in range(16)]
        self.pals[J.P_JUNGLE] = [J.q(c) for c in J.PAL6]
        self.pals[J.P_FLOWER] = [J.q(c) for c in J.PAL7]
        self.pals[P_SWAMP] = [J.q(c) for c in SWAMP_PAL]

    def save(self):
        out = Image.new('P', (128, 256), 0)
        out.putpalette(self.pngpal)
        for n, t in enumerate(self.tiles):
            for y in range(8):
                for x in range(8):
                    out.putpixel(((n % 16) * 8 + x, (n // 16) * 8 + y), t[y][x])
        out.save(TS + '/tiles.png')
        for i in range(16):
            J.write_pal('%s/palettes/%02d.pal' % (TS, i), self.pals[i])
        open(TS + '/metatiles.bin', 'wb').write(self.mts)
        open(TS + '/metatile_attributes.bin', 'wb').write(self.attrs)
        register()
        return self.nfree - len(self.free), len(self.midx)


SWAMP_PAL = [(0, 0, 0),
             (164, 213, 197), (115, 197, 164), (65, 180, 131),      # 1-3 gras (General palet 2: 12, 13, 14)
             (75, 99, 68), (96, 128, 88),                           # 4-5 oeverschaduw
             (96, 68, 64), (119, 86, 82), (146, 107, 100), (166, 132, 125),   # 6-9 modder
             (48, 84, 88), (72, 112, 112), (96, 136, 136), (128, 168, 160),   # 10-13 troebel water
             (40, 56, 44), (200, 224, 208)]                          # 14 donker, 15 glinstering
GRASS_MAP = {12: 1, 13: 2, 14: 3}


def register():
    hdr = open('src/data/tilesets/headers.h').read()
    if 'gTileset_MangroveMire' not in hdr:
        hdr += '''
const struct Tileset gTileset_MangroveMire = // Project Grounded: Mangrove Mire, eigen moerastiles (mangrove_swamp.py)
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_MangroveMire,
    .palettes = gTilesetPalettes_MangroveMire,
    .metatiles = gMetatiles_MangroveMire,
    .metatileAttributes = gMetatileAttributes_MangroveMire,
    .callback = NULL,
};
'''
        open('src/data/tilesets/headers.h', 'w').write(hdr)
    gfx = open('src/data/tilesets/graphics.h').read()
    if 'gTilesetTiles_MangroveMire' not in gfx:
        gfx += '\nconst u32 gTilesetTiles_MangroveMire[] = INCBIN_U32("%s/tiles.4bpp.fastSmol");\n\n' % TS
        gfx += 'const u16 gTilesetPalettes_MangroveMire[][16] =\n{\n'
        gfx += ''.join('    INCBIN_U16("%s/palettes/%02d.gbapal"),\n' % (TS, i) for i in range(16)) + '};\n'
        open('src/data/tilesets/graphics.h', 'w').write(gfx)
    mh = open('src/data/tilesets/metatiles.h').read()
    if 'gMetatiles_MangroveMire' not in mh:
        mh += '\nconst u16 gMetatiles_MangroveMire[] = INCBIN_U16("%s/metatiles.bin");\n' % TS
        mh += 'const u16 gMetatileAttributes_MangroveMire[] = INCBIN_U16("%s/metatile_attributes.bin");\n' % TS
        open('src/data/tilesets/metatiles.h', 'w').write(mh)


ts = SwampTileset()

# grastextuur (General metatile 0x001: tiles 2/3/3/2)
GRASS_CV = J.Canvas(16, 16)
for k, t in enumerate((2, 3, 3, 2)):
    for y in range(8):
        for x in range(8):
            GRASS_CV.p[(k // 2) * 8 + y][(k % 2) * 8 + x] = GRASS_MAP.get(ts.gtiles[t][y][x], 2)

NOISE = [[0.0] * 16 for _ in range(16)]
nr = random.Random(7)
for y in range(16):
    for x in range(16):
        NOISE[y][x] = 0.10 * math.sin(x * 0.9 + y * 0.35) + 0.08 * math.sin(y * 1.3 - x * 0.5) + nr.uniform(-0.03, 0.03)


def field(x, y, mat, px, py):
    """Bilineair veld (1 = materiaal) op pixel (px, py) van vak (x, y), uit de centra van de 2x2 dichtstbijzijnde vakken."""
    fx, fy = (px + 0.5) / 16 - 0.5, (py + 0.5) / 16 - 0.5
    ox, oy = (-1 if fx < 0 else 0), (-1 if fy < 0 else 0)
    tx, ty = fx - ox, fy - oy
    v = [[1.0 if kind(x + ox + i, y + oy + j) in mat else 0.0 for i in (0, 1)] for j in (0, 1)]
    return (v[0][0] * (1 - tx) * (1 - ty) + v[0][1] * tx * (1 - ty) + v[1][0] * (1 - tx) * ty + v[1][1] * tx * ty)


WATERISH = set('wk')


def ground(x, y):
    """16x16-canvas (palet 8) van gras, modder en troebel water voor vak (x, y), of None als het gewoon gras is."""
    mats = {}
    near_any = False
    for j in range(-1, 2):
        for i in range(-1, 2):
            if kind(x + i, y + j) in 'wkm':
                near_any = True
    if not near_any:
        return None
    cv = J.Canvas(16, 16)
    mat = [[0] * 16 for _ in range(16)]                   # 0 gras, 1 modder, 2 water
    for py in range(16):
        for px in range(16):
            n = NOISE[py][px]
            if field(x, y, WATERISH, px, py) + n > 0.5:
                mat[py][px] = 2
            elif field(x, y, 'm', px, py) + n > 0.5:
                mat[py][px] = 1
    if all(v == 0 for r in mat for v in r):
        return None
    for py in range(16):
        for px in range(16):
            m = mat[py][px]
            if m == 2:
                d = min(abs(px - qx) + abs(py - qy) for qx in range(16) for qy in range(16) if mat[qy][qx] != 2) \
                    if any(v != 2 for r in mat for v in r) else 9
                wave = (px + 2 * py + 5 * ((x + y) & 1)) % 11
                c = 12
                if d <= 1:
                    c = 10                                 # donkere rand langs de oever
                elif d <= 2:
                    c = 11
                elif wave == 0 and py % 4 == 1:
                    c = 13                                 # rimpeling
                elif (px * 3 + py * 7) % 23 == 0:
                    c = 11
                cv.p[py][px] = c
            elif m == 1:
                h = (px * 7 + py * 13 + 3 * (x & 1) + 5 * (y & 1)) % 17
                c = 8 if h > 5 else (7 if h > 1 else 9)
                if any(0 <= px + dx < 16 and 0 <= py + dy < 16 and mat[py + dy][px + dx] == 0
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    c = 6
                cv.p[py][px] = c
            else:
                c = GRASS_CV.p[py][px]
                if any(0 <= px + dx < 16 and 0 <= py + dy < 16 and mat[py + dy][px + dx] != 0
                       for dx, dy in ((1, 0), (0, -1), (0, 1), (-1, 0))):
                    c = 4 if any(0 <= px + dx < 16 and 0 <= py + dy < 16 and mat[py + dy][px + dx] == 2
                                 for dx, dy in ((1, 0), (0, -1), (0, 1), (-1, 0))) else 5
                cv.p[py][px] = c
    return cv


def val(mt, coll, elev):
    return mt | (coll << 10) | (elev << 12)


GRASS, TALL = 0x001, 0x00D
FOREST, TRUNK, CANOPY = (0x0C6, 0x0C7), (0x016, 0x017), (0x00E, 0x00F)
SIGN_MT = 0x01B
M = [[0] * W for _ in range(H)]
for y in range(H):
    for x in range(W):
        k = T[y][x]
        below = kind(x, y + 1)
        if k == 'T':
            M[y][x] = val(ts.jungle(rng.choice(TRUNK if below != 'T' else FOREST)), 1, 0)
        elif below == 'T' and k in 'gs':
            M[y][x] = val(ts.jungle(rng.choice(CANOPY)), 0, 3) if k == 'g' else val(SIGN_MT, 1, 3)
        elif k == 'L':
            M[y][x] = val(TALL, 0, 3)
        elif k == 's':
            M[y][x] = val(SIGN_MT, 1, 3)
        else:
            cv = ground(x, y)
            if k in 'wk':
                mt = ts.metatile(ts.cut(cv, 0, 0, P_SWAMP), [0, 0, 0, 0], (1 << 12) | 0x10)
                if k == 'k':
                    horiz = kind(x - 1, y) in 'kg' and kind(x + 1, y) in 'kg' or kind(x, y - 1) != 'k'
                    if kind(x, y - 1) == 'k' or kind(x, y + 1) == 'k':
                        horiz = False
                    M[y][x] = ('plank', mt, horiz)
                    continue
                M[y][x] = val(mt, 0, 1)
            elif cv is None:
                M[y][x] = val(GRASS, 0, 3)
            else:
                M[y][x] = val(ts.metatile(ts.cut(cv, 0, 0, P_SWAMP), [0, 0, 0, 0], 1 << 12), 0, 3)


# plankenpad: houten planken (palet 6, hout 6-9) met donkere naden; palen in de hoeken als het pad ophoudt
def plank(horiz, end_a, end_b):
    cv = J.Canvas(16, 16)
    for py in range(16):
        for px in range(16):
            u, v = (px, py) if horiz else (py, px)          # u langs het pad, v dwars
            if v in (0, 15):
                c = 6
            elif u % 5 == 4:
                c = 6                                        # naad tussen twee planken
            else:
                c = 8 if (v + u // 5) % 4 else 9
                if v == 1:
                    c = 9
                if v == 14:
                    c = 7
            cv.p[py][px] = c
    for end, u0 in ((end_a, 0), (end_b, 13)):
        if end:
            for du in range(3):
                for v in (0, 1, 14, 15):
                    px, py = (u0 + du, v) if horiz else (v, u0 + du)
                    cv.p[py][px] = 7 if du == 1 else 6
    return cv


for y in range(H):
    for x in range(W):
        if isinstance(M[y][x], tuple):
            _, mt, horiz = M[y][x]
            if horiz:
                ea, eb = kind(x - 1, y) != 'k', kind(x + 1, y) != 'k'
            else:
                ea, eb = kind(x, y - 1) != 'k', kind(x, y + 1) != 'k'
            pm = ts.overlay(mt, plank(horiz, ea, eb), 0, 0, J.P_JUNGLE, layer=1, behavior=0x00)
            M[y][x] = val(pm, 0, 3)

# ---------------------------------------------------------------- decor (alleen als de bereikbaarheid blijft)
EVENT_CELLS = {(x, y) for x, y, *_ in TRAINERS + ITEMS + HIDDEN} | {(x, y) for x, y, _ in SIGNS}
KEEP = set()
for x, y in EVENT_CELLS | set(WEST_EXIT) | set(EAST_EXIT):
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            KEEP.add((x + dx, y + dy))
for x, y, face, *_ in TRAINERS:
    d = {'UP': (0, -1), 'DOWN': (0, 1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}.get(face, (0, 0))
    for k in range(1, 6):
        KEEP.add((x + d[0] * k, y + d[1] * k))
for y in range(H):                                   # niets naast de planken (anders lijkt het pad dicht)
    for x in range(W):
        if T[y][x] == 'k':
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    KEEP.add((x + dx, y + dy))
JR = random.Random(SEED + 1)


def mid(x, y):
    return M[y][x] & 0x3FF


def is_water_mt(m):
    if m < 512:
        return False
    at = struct.unpack_from('<H', ts.attrs, (m - 512) * 2)[0]
    b, t, _ = ts.base(m)
    return at & 0xFF == 0x10 and not any(t)


def is_grass_mt(m):
    return m == GRASS


def stamp(x0, y0, cv, pal, ok, block=True, layer=1):
    w, h = cv.w // 16, cv.h // 16
    cells = [(x0 + i, y0 + j) for j in range(h) for i in range(w)]
    for x, y in cells:
        if not inb(x, y) or not ok(mid(x, y)) or (x, y) in BLOCK or (block and (x, y) in KEEP):
            return False
    if block:
        try:
            walk, surf = check(cells)
        except AssertionError:
            return False
        if len(walk) != len(walk0 - BLOCK - set(cells)) or len(surf) < len(surf0 - BLOCK - set(cells)) - 2:
            return False
    for j in range(h):
        for i in range(w):
            x, y = x0 + i, y0 + j
            v = M[y][x]
            M[y][x] = ts.overlay(mid(x, y), cv, i * 16, j * 16, pal, layer=layer) | (((1 if block else (v >> 10) & 3)) << 10) | (v & 0xF000)
    if block:
        BLOCK.update(cells)
    return True


placed = {}
cands = [(x, y) for y in range(2, H - 2) for x in range(2, W - 2)]
JR.shuffle(cands)


def all_water(x0, y0, w, h):
    return all(T[y][x] == 'w' for y in range(y0, y0 + h) for x in range(x0, x0 + w) if inb(x, y))


# mangroves in het water (groot 3x3, klein 2x3), dan op de oever
for x, y in cands:
    if placed.get('mangrove_w', 0) >= 7:
        break
    big = JR.random() < 0.5
    w = 3 if big else 2
    if all_water(x - 1, y - 1, w + 2, 5) and stamp(x, y, J.mangrove(big, True), J.P_JUNGLE, is_water_mt):
        placed['mangrove_w'] = placed.get('mangrove_w', 0) + 1
for x, y in cands:
    if placed.get('mangrove_l', 0) >= 4:
        break
    big = JR.random() < 0.4
    w = 3 if big else 2
    if all(kind(x + i, y + j) == 'g' for i in range(w) for j in range(3)) and \
            all(kind(x + i, y + 3) in 'gLm' for i in range(w)) and \
            stamp(x, y, J.mangrove(big, False), J.P_JUNGLE, is_grass_mt):
        placed['mangrove_l'] = placed.get('mangrove_l', 0) + 1
# wortelbogen in het water en op de oever
for x, y in cands:
    if placed.get('arch', 0) >= 6:
        break
    if all_water(x - 1, y - 1, 4, 3) and stamp(x, y, J.root_arch(True), J.P_JUNGLE, is_water_mt):
        placed['arch'] = placed.get('arch', 0) + 1
# omgevallen stammen op het land
for x, y in cands:
    if placed.get('log', 0) >= 4:
        break
    n = JR.choice((2, 3))
    if all(kind(x + i, y - 1) == 'T' and kind(x + i, y + 1) in 'gLm' and kind(x + i, y + 2) in 'gLm' for i in range(n)) \
            and stamp(x, y, J.log(n), J.P_JUNGLE, is_grass_mt):
        placed['log'] = placed.get('log', 0) + 1
# waterlelies (je surft eroverheen)
for x, y in cands:
    if placed.get('lotus', 0) >= 10:
        break
    if all_water(x - 1, y - 1, 3, 3) and (x, y) not in KEEP and JR.random() < 0.5:
        if stamp(x, y, J.lotus(JR.randrange(2)), J.P_FLOWER, is_water_mt, block=False):
            placed['lotus'] = placed.get('lotus', 0) + 1
# varens langs de bosranden, bosbodem
for x, y in cands:
    if mid(x, y) != GRASS or (x, y) in EVENT_CELLS:
        continue
    t = sum(kind(x + dx, y + dy) == 'T' for dx in (-1, 0, 1) for dy in (-1, 0, 1))
    if t >= 2 and JR.random() < 0.4:
        if stamp(x, y, J.fern(JR.randrange(2)), J.P_JUNGLE, is_grass_mt, block=False):
            placed['fern'] = placed.get('fern', 0) + 1
    elif JR.random() < 0.25:
        if stamp(x, y, J.litter(JR.randrange(3)), J.P_JUNGLE, is_grass_mt, block=False):
            placed['litter'] = placed.get('litter', 0) + 1
# lianen in de boomrand
for y in range(H):
    for x in range(W):
        if mid(x, y) in [ts.jungle(m) for m in TRUNK] and JR.random() < 0.35:
            vx, ph = JR.choice((3, 11)), JR.choice((0.0, 2.0))
            base = TRUNK[[ts.jungle(m) for m in TRUNK].index(mid(x, y))]
            M[y][x] = val(ts.recolor(base, draw=lambda cv, vx=vx, ph=ph: J.vine(cv, vx, 0, 11, ph, tip=True)), 1, 0)
            placed['liana'] = placed.get('liana', 0) + 1

walk, surf = check()
ntiles, nmts = ts.save()
print('moeras:', placed, '| %d tiles (van %d), %d metatiles' % (ntiles, ts.nfree, nmts))
print('bereikbaar: %d vakken lopend, %d met Surf' % (len(walk), len(surf)))

# ---------------------------------------------------------------- schrijven
os.makedirs('data/layouts/MangroveMire', exist_ok=True)
open('data/layouts/MangroveMire/map.bin', 'wb').write(b''.join(struct.pack('<H', v) for r in M for v in r))
BT = [ts.jungle(0x0C6) | 0x400, ts.jungle(0x0C7) | 0x400]
open('data/layouts/MangroveMire/border.bin', 'wb').write(struct.pack('<4H', BT[0], BT[1], BT[1], BT[0]))


def obj(gfx, x, y, move, ttype, sight, script, flag, elev=3):
    return {"graphics_id": gfx, "x": x, "y": y, "elevation": elev, "movement_type": move,
            "movement_range_x": 1 if move == 'MOVEMENT_TYPE_TREE_DISGUISE' else 0,
            "movement_range_y": 1 if move == 'MOVEMENT_TYPE_TREE_DISGUISE' else 0,
            "trainer_type": ttype, "trainer_sight_or_berry_tree_id": str(sight), "script": script, "flag": flag}


objs = []
for x, y, face, gfx, script, sight in TRAINERS:
    move = 'MOVEMENT_TYPE_TREE_DISGUISE' if face == 'TREE' else 'MOVEMENT_TYPE_FACE_' + face
    objs.append(obj(gfx, x, y, move, 'TRAINER_TYPE_NORMAL', sight, script, '0'))
for x, y, item, flag, _ in ITEMS:
    objs.append(obj('OBJ_EVENT_GFX_ITEM_BALL', x, y, 'MOVEMENT_TYPE_LOOK_AROUND', 'TRAINER_TYPE_NONE', item,
                    'Common_EventScript_FindItem', flag))
coords = [{"type": "trigger", "x": x, "y": y, "elevation": 3, "var": "VAR_TEMP_0", "var_value": "0",
           "script": "MangroveMire_EventScript_ToJungle"} for x, y in WEST_EXIT] + \
         [{"type": "trigger", "x": x, "y": y, "elevation": 3, "var": "VAR_TEMP_0", "var_value": "0",
           "script": "MangroveMire_EventScript_ToRoute120"} for x, y in EAST_EXIT]
mj = {
    "id": "MAP_MANGROVE_MIRE", "name": "MangroveMire", "layout": "LAYOUT_MANGROVE_MIRE",
    "music": "MUS_ROUTE119", "region_map_section": "MAPSEC_MANGROVE_MIRE", "requires_flash": False,
    "weather": "WEATHER_JUNGLE_CYCLE", "map_type": "MAP_TYPE_ROUTE", "allow_cycling": True,
    "allow_escaping": False, "allow_running": True, "show_map_name": True,
    "battle_scene": "MAP_BATTLE_SCENE_NORMAL",
    "connections": [],
    "object_events": objs,
    "warp_events": [],
    "coord_events": coords,
    "bg_events": [{"type": "sign", "x": x, "y": y, "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
                   "script": s} for x, y, s in SIGNS] +
                 [{"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag}
                  for x, y, item, flag in HIDDEN],
}
os.makedirs('data/maps/MangroveMire', exist_ok=True)
with open('data/maps/MangroveMire/map.json', 'w') as fp:
    json.dump(mj, fp, indent=2, ensure_ascii=False)
    fp.write('\n')

lj = open('data/layouts/layouts.json').read()
if '"LAYOUT_MANGROVE_MIRE"' not in lj:
    i = lj.rindex('    }\n  ]')
    j = i + len('    }')
    lj = lj[:j] + ''',
    {
      "id": "LAYOUT_MANGROVE_MIRE",
      "name": "MangroveMire_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_General",
      "secondary_tileset": "gTileset_MangroveMire",
      "border_filepath": "data/layouts/MangroveMire/border.bin",
      "blockdata_filepath": "data/layouts/MangroveMire/map.bin"
    }''' % (W, H) + lj[j:]
    open('data/layouts/layouts.json', 'w').write(lj)
g = open('data/maps/map_groups.json').read()
if '"MangroveMire"' not in g:
    i = g.index('"gMapGroup_Grounded": [')
    j = g.index('\n  ]', i)
    g = g[:j] + ',\n    "MangroveMire"' + g[j:]
    open('data/maps/map_groups.json', 'w').write(g)
es = open('data/event_scripts.s').read()
inc = '\t.include "data/maps/MangroveMire/scripts.inc"\n'
if inc not in es:
    anchor = '\t.include "data/maps/FortreeJungle/scripts.inc"\n'
    assert anchor in es
    es = es.replace(anchor, anchor + inc, 1)
    open('data/event_scripts.s', 'w').write(es)

# Route 120 (alleen de westrand): bord op (1, 59), triggers op (0, 60-61)
RW, RH = 40, 100
rv = list(struct.unpack('<%dH' % (RW * RH), open('data/layouts/Route120/map.bin', 'rb').read()))
assert rv[59 * RW + 1] & 0x3FF in (GRASS, SIGN_MT), hex(rv[59 * RW + 1])
rv[59 * RW + 1] = val(SIGN_MT, 1, 3)
open('data/layouts/Route120/map.bin', 'wb').write(struct.pack('<%dH' % (RW * RH), *rv))
rj = json.load(open('data/maps/Route120/map.json'))
if not any(c.get('script') == 'Route120_EventScript_ToMangroveMire' for c in rj['coord_events']):  # VAR_TEMP_0 = speler-x (weer)
    rt = open('data/maps/Route120/map.json').read()
    add_c = ''.join(''',
    {
      "type": "trigger",
      "x": 0,
      "y": %d,
      "elevation": 3,
      "var": "VAR_TEMP_9",
      "var_value": "0",
      "script": "Route120_EventScript_ToMangroveMire"
    }''' % y for y in (60, 61))
    i = rt.index('"coord_events": [')
    j = rt.index('\n  ]', i)
    empty = rt[i:j].strip().endswith('[')
    rt = rt[:j] + (add_c[1:] if empty else add_c) + rt[j:]
    i = rt.index('"bg_events": [')
    j = rt.index('\n  ]', i)
    rt = rt[:j] + ''',
    {
      "type": "sign",
      "x": 1,
      "y": 59,
      "elevation": 0,
      "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
      "script": "Route120_EventScript_MangroveMireSign"
    }''' + rt[j:]
    json.loads(rt)
    open('data/maps/Route120/map.json', 'w').write(rt)

if len(sys.argv) > 1:
    from gridrender import render
    render(M, 'general', 'mangrove_mire').save(sys.argv[1])
print('klaar')
