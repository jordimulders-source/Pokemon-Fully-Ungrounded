"""Project Grounded: Glimwood Tangle + Ballonlea (Spacetime Cave, post-game): Xerneas en Yveltal.

Galar in een andere tijd: een donker sprookjesbos vol lichtgevende paddenstoelen, waarvan het licht afsterft.

  GlimwoodTangle            48x60. Kronkelende, zacht gloeiende lila paden (eigen tiles, per 8x8-tegel uit een
                            hoekveld: organische randen, geen rechte stukken), bos op een 2x2-raster rond de paden en
                            open plekken, losse boompjes langs de randen, twee terrassen met klifwanden en stenen
                            trappen, grote wortels die uit het bos komen, reuzenpaddenstoelen, hoge gloeiende
                            klokjes (groen/cyaan, zoals in de anime), een heksenkring in het midden, hoog gras.
                            Ingang onderaan (scheur uit de hub), uitgang bovenaan naar Ballonlea.
  GlimwoodTangle_Ballonlea  36x34. Het dorp: paddenstoelhuisjes (eigen tekening, twee hoedkleuren via het palet),
                            pleintje, bovenaan een terras met de heksenkring waar Xerneas slaapt.

Twee toestanden (zelfde map.bin, andere paletten; keuze in ON_TRANSITION, zie CLAUDE.md "Kaart met twee toestanden"):
  *_Dying   glimwood_general_dying + glimwood_dying: grauw, het licht is uit (tot Xerneas gevangen is).
  normaal   glimwood_general + glimwood: nachtbos met felle gloed.

Tilesets: primary glimwood_general(_dying) = General met eigen paletten (BASE general); secondary glimwood = eigen
tiles (tekenfuncties uit mushroom_forest.py hergebruikt), glimwood_dying = dezelfde tiles met dode paletten.

Quest (SPACETIME_PLAN): oude Ballonlea-heks (Expert F) met quizjes -> Impidimp-bende (wilde dubbelgevechten,
de laatste blokkeert de weg naar Ballonlea, de baas de trap naar Xerneas) -> Xerneas (lv 70) vangen -> het bos
licht weer op -> Yveltal (lv 70) in de heksenkring van het bos -> FLAG_SPACETIME_GLIMWOOD_DONE.
Flags FLAG_GROUNDED 880-919 (blok 'glimwood' in flags.h), trainers 1098, 1099, 1107, 1108.
Idempotent; controleert de bereikbaarheid. Gebruik: python3 tools/grounded/maptools/glimwood.py [rendermap]"""
import json, math, os, random, re, struct, subprocess, sys, zlib
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import beacon_dragon as bd          # zet de werkmap op de repo-root
from PIL import Image

HUB_DEST = ('SPACETIME_CAVE', 9)    # terugweg: de Glimwood-scheur in de hub (warps 9-10, spacetime_cave.py)
GROUP = 'gMapGroup_Spacetime'
SEED = 716                          # nationaal dexnummer van Xerneas
TS = 'data/tilesets/secondary/glimwood'
GEN = 'data/tilesets/primary/general'
COVERED, NORMAL = 0x1000, 0x0000
MB_NORTH_ARROW, MB_SOUTH_ARROW = 0x64, 0x65
GRASS_MT, TALL_MT = 0x001, 0x00D
STAIRS = (0x0AF, 0x0CF)             # stenen Hoenn-trap (2 breed)
WALL = dict(W=0x070, E=0x072, FACE=0x07C, FOOT=0x079, FOOT_W=0x078, FOOT_E=0x07A)
SMALL_TREE = ((0x00E, 0x016), (0x00F, 0x017))   # Hoenn-boompjes van 1 breed (top, voet)
FLOWERS = 0x004


def val(mt, coll=0, elev=3):
    return mt | (coll << 10) | (elev << 12)


def const(name):
    return re.sub(r'(?<=[a-z])(?=[A-Z])', '_', name).upper()


# ====================================================================== tekenen (uit mushroom_forest.py)
_src = open(os.path.join(HERE, 'mushroom_forest.py')).read()
_a, _b = _src.index('class Canvas:'), _src.index("\ngm = open(GEN + '/metatiles.bin'")
MF = {'math': math, 'random': random, 'Image': Image, 'MUSH': [(0, 0, 0)] * 16, '__name__': 'mf'}
exec(_src[_a:_b], MF)
Canvas, mushroom, spores, small, moss, glowdots = (MF[k] for k in ('Canvas', 'mushroom', 'spores', 'small', 'moss',
                                                                     'glowdots'))
log_, fairy_ring, giant_small, Tiles, hflip = (MF[k] for k in ('log', 'fairy_ring', 'giant_small', 'Tiles', 'hflip'))
KINDS = MF['KINDS']
# eigen soorten op palet GLOW2 (roze 1-4, cyaan 5-8, groen 9-12, wit 13): steel in de tint van de hoed (zoals de anime)
KINDS['pink'] = dict(cap=(1, 2, 3, 4), spot=(13, 4, 3), stem=(4, 3, 2, 1), gill=(2, 1), ground=(14, 15, 15, 15))
KINDS['cyan'] = dict(cap=(5, 6, 7, 8), spot=(13, 8, 7), stem=(8, 7, 6, 5), gill=(6, 5), ground=(14, 15, 15, 15))
KINDS['green'] = dict(cap=(9, 10, 11, 12), spot=(13, 12, 11), stem=(12, 11, 10, 9), gill=(10, 9), ground=(14, 15, 15, 15))
# paddenstoelhuisje (palet HOUSE): hoed 1-4, room 5-7, hout 8-11
KINDS['house'] = dict(cap=(1, 2, 3, 4), spot=(5, 6, 7), stem=(8, 9, 10, 11), gill=(10, 11), ground=(14, 15, 15, 15))


# ====================================================================== paletten
def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().split('\n')[3:19]]


def jasc(path, cols):
    with open(path, 'w', newline='\r\n') as fp:
        fp.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % tuple(c) for c in cols))


G2 = read_pal(GEN + '/palettes/02.pal')
SHADOW = (16, 100, 92)
P_GLOW1, P_MUSH, P_GLOW2, P_PATH, P_HOUSE, P_HOUSE2 = 6, 7, 8, 9, 10, 11
BASEPAL = {
    # paars/blauw gloeiend (layout van GLOW uit mushroom_forest), 14 slagschaduw, 15 gras
    P_GLOW1: [(0, 0, 0), (42, 20, 72), (88, 46, 142), (140, 86, 204), (198, 150, 242), (18, 36, 88), (36, 84, 168),
              (66, 140, 222), (140, 212, 248), (232, 248, 255), (204, 200, 224), (148, 144, 182), (70, 64, 104),
              (186, 250, 160), SHADOW, G2[15]],
    # rood/bruin/room + schors (wortels, stam), 12 slagschaduw, 13-15 gras
    P_MUSH: [(0, 0, 0), (74, 18, 44), (134, 34, 60), (186, 56, 66), (228, 108, 98), (234, 226, 204), (192, 182, 166),
             (138, 130, 140), (60, 42, 56), (96, 62, 58), (140, 98, 72), (186, 144, 100), SHADOW, G2[13], G2[12], G2[15]],
    # roze, cyaan, groen gloeiend (klokjes zoals in de anime)
    P_GLOW2: [(0, 0, 0), (96, 24, 80), (176, 64, 150), (232, 124, 206), (255, 196, 244), (12, 64, 96), (32, 150, 184),
              (96, 224, 232), (196, 255, 250), (36, 84, 32), (96, 184, 64), (176, 240, 104), (232, 255, 184),
              (250, 255, 240), SHADOW, G2[15]],
    # gloeiend lila pad; 12-15 = de grastinten van General (rand van het pad)
    P_PATH: [(0, 0, 0), (70, 48, 98), (104, 76, 136), (134, 102, 164), (170, 136, 198), (214, 190, 236),
             (250, 236, 255), (150, 230, 250), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)] + G2[12:16],
    # paddenstoelhuisje: magenta hoed, room, hout, raam, deur
    P_HOUSE: [(0, 0, 0), (76, 22, 66), (146, 52, 126), (204, 96, 176), (244, 166, 226), (250, 240, 222), (212, 196, 182),
              (150, 134, 142), (226, 196, 150), (186, 146, 100), (136, 98, 70), (66, 42, 40), (255, 222, 120),
              (112, 60, 50), SHADOW, G2[15]],
}
BASEPAL[P_HOUSE2] = list(BASEPAL[P_HOUSE])
BASEPAL[P_HOUSE2][1:5] = [(10, 52, 74), (28, 118, 142), (76, 188, 204), (168, 240, 244)]   # blauwgroene hoed
GLOWMASK = {P_GLOW1: set(range(1, 14)), P_MUSH: set(), P_GLOW2: set(range(1, 14)), P_PATH: set(range(1, 8)),
            P_HOUSE: set(range(1, 8)) | {12}, P_HOUSE2: set(range(1, 8)) | {12}}


def q8(c):
    return tuple(max(0, min(248, int(v) // 8 * 8)) for v in c)


def lum(c):
    return 0.30 * c[0] + 0.59 * c[1] + 0.11 * c[2]


def night(c):
    """Nachtbos: groen wordt diep blauwgroen, een vleugje violet."""
    r, g, b = c
    return q8((r * 0.30 + 10, g * 0.47 + 6, b * 0.60 + 24))


def dying(c):
    """Stervend bos: grauw, kleurloos, een zieke paarsgrijze waas."""
    L = lum(c)
    n = night(c)
    gray = (L * 0.30 + 24, L * 0.27 + 20, L * 0.31 + 28)
    return q8(tuple(0.25 * a + 0.75 * b for a, b in zip(n, gray)))


def dying_glow(c):
    """Uitgedoofde gloed: dof grijs."""
    L = lum(c)
    return q8((L * 0.24 + 34, L * 0.22 + 30, L * 0.26 + 38))


def soft(c):
    """Minder donker dan night(): schors, rode paddenstoelen en de heksenkring blijven zichtbaar."""
    r, g, b = c
    return q8((r * 0.56 + 12, g * 0.56 + 12, b * 0.62 + 26))


SOFTMASK = {P_MUSH: set(range(1, 12))}


def state_pal(pal, mask, state, softm=()):
    out = [pal[0]]
    for i, c in enumerate(pal[1:], 1):
        if state == 'bright':
            out.append(q8(c) if i in mask else soft(c) if i in softm else night(c))
        else:
            out.append(dying_glow(c) if i in mask else dying(c))
    return out


# ====================================================================== decor tekenen
def glow_pool(cv, cx, cy, rx, ry, col, seed, dense=True):
    """Lichtschijnsel op de grond onder een gloeiende paddenstoel: geditherde ellips."""
    r = random.Random(seed)
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            d = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
            if d <= 1 and not cv.get(x, y):
                if (dense and d < 0.35 and (x + y) % 2 == 0) or (d < 1 and (x * 3 + y * 5) % 7 == 0 and r.random() < 0.8):
                    cv.set(x, y, col)


def small2(kind):
    """Klein groepje (16x16) in roze/cyaan/groen."""
    cv = Canvas(16, 16)
    k = KINDS[kind]
    glow_pool(cv, 8, 14, 7, 2.2, k['cap'][1], 40)
    if kind == 'pink':
        mushroom(cv, 6.5, 13, 3.6, 3.0, 1, 6, 'pink', [(-0.3, -0.6, 0.6)], gills=0, shadow=False, seed=41)
        mushroom(cv, 12.0, 14, 2.4, 2.0, 1, 3, 'pink', gills=0, shadow=False, seed=42)
        spores(cv, [(2, 2), (13, 3), (9, 1), (1, 9)], [13, 4, 13, 4])
    elif kind == 'cyan':
        mushroom(cv, 9.5, 13, 3.4, 3.6, 1, 7, 'cyan', gills=0, shadow=False, seed=43)
        mushroom(cv, 3.5, 14, 2.4, 2.4, 1, 4, 'cyan', gills=0, shadow=False, seed=44)
        spores(cv, [(1, 3), (14, 2), (6, 1), (13, 9)], [13, 8, 13, 8])
    else:
        mushroom(cv, 5.5, 14, 3.2, 3.4, 1, 8, 'green', gills=0, shadow=False, seed=45)
        mushroom(cv, 11.5, 13, 2.8, 2.8, 1, 5, 'green', gills=0, shadow=False, seed=46)
        spores(cv, [(2, 1), (14, 4), (9, 2), (15, 10)], [13, 12, 13, 12])
    return cv


def tall(kind, seed):
    """Hoge gloeiende klokjes (32x48), zoals de paddenstoelen in Glimwood: lange stelen, klokvormige hoeden."""
    cv = Canvas(32, 48)
    k = KINDS[kind]
    glow_pool(cv, 16, 44, 15, 3.6, k['cap'][1], seed, dense=False)
    mushroom(cv, 11.5, 45, 7.2, 7.5, 2, 26, kind, [(-0.4, -0.6, 1.0), (0.3, -0.75, 0.8)], lip=2, gills=1,
             shadow=False, seed=seed + 1)
    mushroom(cv, 23.5, 46, 5.4, 5.6, 2, 15, kind, [(-0.3, -0.6, 0.8)], lip=1, gills=1, shadow=False, seed=seed + 2)
    mushroom(cv, 4.5, 46, 3.0, 3.0, 1, 6, kind, gills=0, shadow=False, seed=seed + 3)
    spores(cv, [(2, 8), (28, 12), (20, 3), (30, 26), (1, 24), (26, 36), (8, 2)], [13, k['cap'][3]] * 4)
    return cv


def root(w, h, pts, seed):
    """Grote wortel (schors met licht van boven, mos erop) langs een bezierkromme door pts, dikte van r0 naar r1."""
    cv = Canvas(w * 16, h * 16)
    r = random.Random(seed)
    (x0, y0, r0), (x1, y1, _), (x2, y2, _), (x3, y3, r3) = pts
    samples = []
    for i in range(121):
        t = i / 120
        a, b, c, d = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
        samples.append((a * x0 + b * x1 + c * x2 + d * x3, a * y0 + b * y1 + c * y2 + d * y3, r0 + (r3 - r0) * t))
    # slagschaduw rechtsonder
    for sx, sy, rr in samples:
        for y in range(int(sy - rr), int(sy + rr + 4)):
            for x in range(int(sx - rr), int(sx + rr + 3)):
                if ((x + 0.5 - sx - 1.5) / (rr + 0.5)) ** 2 + ((y + 0.5 - sy - 2.5) / (rr * 0.8 + 0.5)) ** 2 <= 1:
                    cv.set(x, y, 12)
    best = {}
    for sx, sy, rr in samples:
        for y in range(int(sy - rr) - 1, int(sy + rr) + 2):
            for x in range(int(sx - rr) - 1, int(sx + rr) + 2):
                d = math.hypot(x + 0.5 - sx, y + 0.5 - sy) / rr
                if d <= 1 and (x, y) not in best or (d <= 1 and d < best[(x, y)][0]):
                    best[(x, y)] = (d, (y + 0.5 - sy) / rr)
    for (x, y), (d, ny) in best.items():
        c = 11 if ny < -0.45 else (10 if ny < 0.25 else 9)
        if (x * 7 + y * 3) % 11 < 3 and -0.3 < ny < 0.8:
            c = 9 if c == 10 else (8 if c == 9 else c)            # schorsgroeven
        if d > 0.86:
            c = 8
        cv.set(x, y, c)
    for (x, y), (d, ny) in best.items():                          # mos bovenop
        if ny < -0.6 and d > 0.55 and r.random() < 0.55:
            cv.set(x, y, 14 if r.random() < 0.5 else 13)
            if r.random() < 0.3 and (x, y - 1) not in best:
                cv.set(x, y - 1, 13)
    # grassprieten tegen de voet
    for sx, sy, rr in samples[::6]:
        if r.random() < 0.5:
            x, y = int(sx + rr * 0.6), int(sy + rr) + 1
            for j in range(r.choice((1, 2))):
                cv.set(x, y - j, 15 if j == 0 else 13)
    return cv


def glow_ring(seed):
    """Heksenkring (80x80) van gloeiende paarse en blauwe paddenstoeltjes rond een ring donkere grond."""
    r = random.Random(seed)
    cv = Canvas(80, 80)
    for i in range(160):
        a = r.uniform(0, 2 * math.pi)
        rad = 30 + r.gauss(0, 1.6)
        x, y = int(40 + rad * math.cos(a)), int(42 + rad * math.sin(a) * 0.92)
        cv.set(x, y, 14 if r.random() < 0.7 else 12)
    glow_pool(cv, 40, 42, 24, 22, 2, seed, dense=False)
    pts = []
    for i in range(16):
        a = 2 * math.pi * i / 16 + r.uniform(-0.06, 0.06)
        rad = 29 + r.uniform(-1.5, 1.5)
        pts.append((40 + rad * math.cos(a), 42 + rad * math.sin(a) * 0.92, i))
    for cx, by, i in sorted(pts, key=lambda p: p[1]):
        big = r.random() < 0.45
        mushroom(cv, cx, int(by), 3.0 if big else 2.3, 2.6 if big else 2.0, 1, 4 if big else 3,
                 'purple' if i % 2 else 'blue', gills=0, shadow=False, seed=200 + i)
    spores(cv, [(40, 20), (22, 36), (58, 48), (36, 60), (50, 30), (28, 52), (44, 44), (34, 34)], [9, 13] * 4)
    return cv


def pale_ring(seed):
    """Heksenkring (80x80) van bleke en bruine paddenstoelen: het doodse tegenstuk van glow_ring (hier landt Yveltal)."""
    r = random.Random(seed)
    cv = Canvas(80, 80)
    for i in range(170):
        a = r.uniform(0, 2 * math.pi)
        rad = 30 + r.gauss(0, 1.8)
        x, y = int(40 + rad * math.cos(a)), int(42 + rad * math.sin(a) * 0.92)
        cv.set(x, y, 15 if r.random() < 0.6 else 12)
    pts = []
    for i in range(15):
        a = 2 * math.pi * i / 15 + r.uniform(-0.07, 0.07)
        rad = 29 + r.uniform(-1.5, 1.5)
        pts.append((40 + rad * math.cos(a), 42 + rad * math.sin(a) * 0.92, i))
    for cx, by, i in sorted(pts, key=lambda p: p[1]):
        big = r.random() < 0.5
        mushroom(cv, cx, int(by), 3.4 if big else 2.6, 2.8 if big else 2.1, 2 if big else 1, 4 if big else 3,
                 'tan' if i % 3 else 'brown', gills=1 if big else 0, seed=300 + i)
    return cv


def house():
    """Paddenstoelhuisje (64x64): grote hoed met stippen, de steel is het huis (planken, ronde deur, rond raam)."""
    cv = Canvas(64, 64)
    mushroom(cv, 32, 61, 30.0, 21.0, 30, 31, 'house',
             [(-0.6, -0.55, 3.2), (-0.05, -0.85, 3.0), (0.5, -0.6, 3.0), (0.86, -0.2, 2.2), (-0.88, -0.12, 2.0),
              (0.15, -0.3, 2.4), (-0.35, -0.2, 1.6)], lip=2, gills=2, seed=60, grain=True, shadow=False)
    # deur: rond bovenaan, x 27-36, y 47-61
    for y in range(46, 62):
        for x in range(26, 38):
            dx, dy = (x + 0.5 - 32) / 6.0, (y + 0.5 - 52) / 6.0
            inside = (y >= 52 and 26 <= x < 38) or (dy < 0 and dx * dx + dy * dy <= 1)
            if not inside:
                continue
            edge = x in (26, 37) or (y < 52 and dx * dx + dy * dy > 0.7) or y == 61
            cv.set(x, y, 11 if edge else (13 if (x - 26) % 4 else 10))
    cv.set(35, 55, 12)                                            # deurknop
    # rond raam met warm licht
    for y in range(34, 45):
        for x in range(40, 51):
            d = math.hypot(x + 0.5 - 45.5, y + 0.5 - 39.5)
            if d <= 5.2:
                c = 11 if d > 4.2 else (12 if (x != 45 and y != 39) else 11)
                cv.set(x, y, c)
    # klein raampje links
    for y in range(38, 43):
        for x in range(13, 18):
            cv.set(x, y, 11 if x in (13, 17) or y in (38, 42) else 12)
    return cv


def path_noise():
    r = random.Random(SEED)
    return [[r.uniform(-0.10, 0.10) for _ in range(16)] for _ in range(16)]


PNZ = path_noise()

_gen_tiles = Image.open(GEN + '/tiles.png')


def gen_tile(n):
    sx, sy = (n % (_gen_tiles.width // 8)) * 8, (n // (_gen_tiles.width // 8)) * 8
    return [_gen_tiles.getpixel((sx + i % 8, sy + i // 8)) & 15 for i in range(64)]


GT = {2: gen_tile(2), 3: gen_tile(3)}


def path_tile(c, px, py):
    """8x8-tegel van het pad. c = (linksboven, rechtsboven, linksonder, rechtsonder) in 0/1; px/py = pariteit van de
    tegel (gras eronder: General-tile 2 of 3, textuur met periode 16 px)."""
    base = GT[2 if (px + py) % 2 == 0 else 3]
    out = []
    for y in range(8):
        for x in range(8):
            u, v = (x + 0.5) / 8, (y + 0.5) / 8
            f = c[0] * (1 - u) * (1 - v) + c[1] * u * (1 - v) + c[2] * (1 - u) * v + c[3] * u * v
            f += PNZ[py * 8 + y][px * 8 + x]
            ax, ay = px * 8 + x, py * 8 + y
            h = (ax * 73 + ay * 151 + ax * ay * 7) % 97
            if f > 0.5:
                if f < 0.56:
                    col = 1
                elif f < 0.66:
                    col = 2
                else:
                    col = 3                                     # fijne korrel, geen herkenbaar patroon
                    if h % 11 == 0:
                        col = 2
                    elif h % 13 == 0 and f > 0.8:
                        col = 4
                    elif h == 5 and f > 0.95:
                        col = 5
            else:
                col = base[y * 8 + x]
                if f > 0.36 and (ax + ay) % 2 == 0 and h % 3 == 0:
                    col = 12                                    # gloed op het gras naast het pad
            out.append(col)
    return tuple(out)


# ====================================================================== tileset bouwen
tt = Tiles(512, 1)                  # tile 512 blijft leeg
MT, ATTR, NAMES = [], [], {}
GRASS = [0x2002, 0x2003, 0x2003, 0x2002]


def addmt(name, lower, upper, attr):
    if name in NAMES:
        return NAMES[name]
    NAMES[name] = 0x200 + len(MT)
    MT.append(list(lower) + list(upper))
    ATTR.append(attr)
    return NAMES[name]


def deco(name, cv, pal, w=1, h=1, layer=COVERED):
    for cy in range(h):
        for cx in range(w):
            addmt('%s_%d_%d' % (name, cx, cy) if (w, h) != (1, 1) else name, GRASS, tt.cell(cv, cx, cy, pal), layer)


def path_mt(corners, x, y, beh=0):
    """Metatile van het pad op kaartcel (x, y); corners = 3x3 hoekwaarden. Hergebruikt identieke metatiles."""
    ents = []
    for k in range(4):
        i, j = k % 2, k // 2
        c = (corners[j][i], corners[j][i + 1], corners[j + 1][i], corners[j + 1][i + 1])
        px, py = (2 * x + i) % 2, (2 * y + j) % 2
        if not any(c):
            ents.append(0x2002 if (px + py) % 2 == 0 else 0x2003)
        else:
            ents.append(tt.add(path_tile(c, px, py), P_PATH))
    key = ('path', tuple(ents), beh)
    if key not in NAMES:
        addmt(key, ents, [0] * 4, NORMAL | beh)
    return NAMES[key]


def build_decor():
    deco('m_purple', small('purple'), P_GLOW1)
    deco('m_blue', small('blue'), P_GLOW1)
    deco('m_red', small('red'), P_MUSH)
    deco('m_brown', small('brown'), P_MUSH)
    deco('m_pink', small2('pink'), P_GLOW2)
    deco('m_cyan', small2('cyan'), P_GLOW2)
    deco('m_green', small2('green'), P_GLOW2)
    deco('moss1', moss(1), P_MUSH)
    deco('moss2', moss(7), P_MUSH)
    deco('glow', glowdots(), P_GLOW1)
    deco('log', log_(), P_MUSH, 3, 1)
    deco('ring', pale_ring(SEED), P_MUSH, 5, 5)
    deco('gring', glow_ring(SEED), P_GLOW1, 5, 5)
    deco('gpur', giant_small('purple'), P_GLOW1, 2, 2)
    deco('gblue', giant_small('blue'), P_GLOW1, 2, 2)
    deco('tallg', tall('green', 70), P_GLOW2, 2, 3)
    deco('tallc', tall('cyan', 80), P_GLOW2, 2, 3)
    deco('tallp', tall('pink', 90), P_GLOW2, 2, 3)
    # wortels: uit het bos (boven) naar beneden/opzij; de gespiegelde versie kost weinig extra tiles
    ra = root(5, 2, [(5, 27, 7.0), (18, 0, 0), (52, -2, 0), (75, 26, 4.5)], 101)          # boog over de grond
    deco('rootR', ra, P_MUSH, 5, 2)
    rb = Canvas(80, 32)
    for y in range(32):
        for x in range(80):
            rb.p[y][79 - x] = ra.p[y][x]
    deco('rootL', rb, P_MUSH, 5, 2)
    rc = root(3, 2, [(5, 26, 5.5), (12, 2, 0), (30, 2, 0), (44, 25, 3.5)], 103)
    deco('rootS', rc, P_MUSH, 3, 2)
    deco('house', house(), P_HOUSE, 4, 4)
    deco('house2', house(), P_HOUSE2, 4, 4)
    print('decor:', len(MT), 'metatiles,', len(tt.list) + 1, 'tiles')


STAMPS = {  # naam: (breedte, hoogte, massief(dx, dy))
    'log': (3, 1, lambda dx, dy: True),
    'ring': (5, 5, lambda dx, dy: False), 'gring': (5, 5, lambda dx, dy: False),
    'gpur': (2, 2, lambda dx, dy: True), 'gblue': (2, 2, lambda dx, dy: True),
    'tallg': (2, 3, lambda dx, dy: True), 'tallc': (2, 3, lambda dx, dy: True), 'tallp': (2, 3, lambda dx, dy: True),
    'rootR': (5, 2, lambda dx, dy: True), 'rootL': (5, 2, lambda dx, dy: True), 'rootS': (3, 2, lambda dx, dy: True),
    'house': (4, 4, lambda dx, dy: True), 'house2': (4, 4, lambda dx, dy: True),
}
SMALLS = ['m_purple', 'm_blue', 'm_red', 'm_brown', 'm_pink', 'm_cyan', 'm_green', 'moss1', 'moss2', 'glow']


def save_tileset():
    assert len(tt.list) + 1 <= 512, ('te veel tiles', len(tt.list) + 1)
    assert len(MT) <= 512, ('te veel metatiles', len(MT))
    os.makedirs(TS + '/palettes', exist_ok=True)
    out = Image.new('P', (128, ((len(tt.list) + 1 + 15) // 16) * 8), 0)
    out.putpalette([v for c in BASEPAL[P_GLOW2] for v in c] + [0] * (768 - 48))
    for i, t in enumerate(tt.list):
        n = 1 + i
        for p, v in enumerate(t):
            out.putpixel(((n % 16) * 8 + p % 8, (n // 16) * 8 + p // 8), v)
    out.save(TS + '/tiles.png')
    open(TS + '/metatiles.bin', 'wb').write(b''.join(struct.pack('<8H', *e) for e in MT))
    open(TS + '/metatile_attributes.bin', 'wb').write(b''.join(struct.pack('<H', a) for a in ATTR))
    subprocess.run(['tools/gbagfx/gbagfx', TS + '/tiles.png', TS + '/tiles.4bpp'], check=True)
    # paletten: glimwood (fel) en glimwood_dying (zelfde tiles, uitgedoofd)
    rust = 'data/tilesets/secondary/rustboro/palettes/%02d.pal'
    for d, state in ((TS, 'bright'), (TS + '_dying', 'dying')):
        os.makedirs(d + '/palettes', exist_ok=True)
        for i in range(16):
            p = BASEPAL.get(i)
            if p is None:
                p = read_pal(rust % i)
                p = state_pal(p, set(), state) if 6 <= i <= 12 else p
            else:
                p = state_pal(p, GLOWMASK[i], state, SOFTMASK.get(i, ()))
            jasc('%s/palettes/%02d.pal' % (d, i), p)
    open(TS + '_dying/BASE', 'w').write('glimwood\n')
    for name, state in (('glimwood_general', 'bright'), ('glimwood_general_dying', 'dying')):
        d = 'data/tilesets/primary/' + name
        os.makedirs(d + '/palettes', exist_ok=True)
        open(d + '/BASE', 'w').write('general\n')
        for i in range(16):
            p = read_pal(GEN + '/palettes/%02d.pal' % i)
            jasc('%s/palettes/%02d.pal' % (d, i), state_pal(p, set(), state) if i < 6 else p)


def register_tilesets():
    gh = open('src/data/tilesets/graphics.h').read()
    hh = open('src/data/tilesets/headers.h').read()
    mh = open('src/data/tilesets/metatiles.h').read()
    tag = '// Project Grounded: Glimwood Tangle (tools/grounded/maptools/glimwood.py)\n'
    if 'gTilesetTiles_Glimwood[]' not in gh:
        gh = gh.rstrip('\n') + '\n\n' + tag + 'const u32 gTilesetTiles_Glimwood[] = INCBIN_U32("%s/tiles.4bpp.fastSmol");\n' % TS
    for sym, d in (('Glimwood', TS), ('GlimwoodDying', TS + '_dying'),
                   ('GlimwoodGeneral', 'data/tilesets/primary/glimwood_general'),
                   ('GlimwoodGeneralDying', 'data/tilesets/primary/glimwood_general_dying')):
        if 'gTilesetPalettes_%s[]' % sym not in gh:
            gh = gh.rstrip('\n') + '\n\n' + tag + 'const u16 gTilesetPalettes_%s[][16] =\n{\n' % sym + \
                 ''.join('    INCBIN_U16("%s/palettes/%02d.gbapal"),\n' % (d, i) for i in range(16)) + '};\n'
    if 'gMetatiles_Glimwood[]' not in mh:
        mh = mh.rstrip('\n') + '\n\n' + tag + \
             'const u16 gMetatiles_Glimwood[] = INCBIN_U16("%s/metatiles.bin");\n' % TS + \
             'const u16 gMetatileAttributes_Glimwood[] = INCBIN_U16("%s/metatile_attributes.bin");\n' % TS
    for sym, tiles, mts, sec, cb in (('Glimwood', 'Glimwood', 'Glimwood', True, 'NULL'),
                                     ('GlimwoodDying', 'Glimwood', 'Glimwood', True, 'NULL'),
                                     ('GlimwoodGeneral', 'General', 'General', False, 'InitTilesetAnim_General'),
                                     ('GlimwoodGeneralDying', 'General', 'General', False, 'InitTilesetAnim_General')):
        if 'gTileset_%s =' % sym not in hh:
            hh = hh.rstrip('\n') + '\n\n' + tag + 'const struct Tileset gTileset_%s =\n{\n' \
                 '    .isCompressed = TRUE,\n    .isSecondary = %s,\n    .tiles = gTilesetTiles_%s,\n' \
                 '    .palettes = gTilesetPalettes_%s,\n    .metatiles = gMetatiles_%s,\n' \
                 '    .metatileAttributes = gMetatileAttributes_%s,\n    .callback = %s,\n};\n' % (
                     sym, 'TRUE' if sec else 'FALSE', tiles, sym, mts, mts, cb)
    open('src/data/tilesets/graphics.h', 'w').write(gh)
    open('src/data/tilesets/headers.h', 'w').write(hh)
    open('src/data/tilesets/metatiles.h', 'w').write(mh)


# ====================================================================== kaart-bouwer
def vnoise(seed, scale):
    """Gladde waardenruis (bilineair tussen roosterpunten met afstand `scale`)."""
    r = random.Random(seed)
    cache = {}

    def g(i, j):
        if (i, j) not in cache:
            cache[(i, j)] = random.Random(zlib.crc32(b'%d,%d,%d' % (seed, i, j))).uniform(-1, 1)
        return cache[(i, j)]

    def f(x, y):
        x, y = x / scale, y / scale
        i, j = math.floor(x), math.floor(y)
        u, v = x - i, y - j
        u, v = u * u * (3 - 2 * u), v * v * (3 - 2 * v)
        return (g(i, j) * (1 - u) * (1 - v) + g(i + 1, j) * u * (1 - v) + g(i, j + 1) * (1 - u) * v +
                g(i + 1, j + 1) * u * v)
    return f


def catmull(pts, step=0.2):
    out = []
    P = [pts[0]] + list(pts) + [pts[-1]]
    for k in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[k - 1], P[k], P[k + 1], P[k + 2]
        n = max(2, int(math.hypot(p2[0] - p1[0], p2[1] - p1[1]) / step))
        for s in range(n):
            t = s / n
            out.append(tuple(0.5 * ((2 * p1[i]) + (-p0[i] + p2[i]) * t + (2 * p0[i] - 5 * p1[i] + 4 * p2[i] - p3[i]) * t * t +
                                    (-p0[i] + 3 * p1[i] - 3 * p2[i] + p3[i]) * t ** 3) for i in (0, 1)))
    out.append(tuple(pts[-1]))
    return out


class Map:
    def __init__(self, name, W, H, seed):
        self.name, self.W, self.H = name, W, H
        self.rng = random.Random(seed)
        self.n1, self.n2 = vnoise(seed, 2.5), vnoise(seed + 1, 4.0)
        self.M = [[None] * W for _ in range(H)]
        self.kind = [['?'] * W for _ in range(H)]          # T boom, g gras, p pad, w wand, s trap, d decor
        self.keep = set()                                   # vrij te houden (events en hun aanloop)
        self.paths = []                                     # (gesamplede lijn, straal)
        self.rings = []                                     # (midden x, y, straal, halve breedte): rond pleintje
        self.clearings = []
        self.terraces = []
        self.forced_open = set()
        self.forced_closed = set()
        self.nopath = set()                                 # geen pad (bijv. onder een huis)

    # ---------------------------------------------------------------- plan
    def path(self, pts, r=1.05):
        self.paths.append((catmull(pts), r))

    def dist_path(self, x, y):
        best = 99
        for (cx, cy, R, r) in self.rings:
            best = min(best, abs(math.hypot(x - cx, y - cy) - R) - r)
        for line, r in self.paths:
            for (px, py) in line:
                d = math.hypot(x - px, y - py) - r
                if d < best:
                    best = d
        return best

    def plan(self):
        W, H = self.W, self.H
        # hoekveld van het pad (halve metatile-resolutie)
        self.C = [[0] * (2 * W + 1) for _ in range(2 * H + 1)]
        for j in range(2 * H + 1):
            for i in range(2 * W + 1):
                x, y = i / 2, j / 2
                if self.dist_path(x, y) + 0.22 * self.n1(x * 1.7, y * 1.7) <= 0:
                    self.C[j][i] = 1
        for (x, y) in self.forced_closed | self.nopath:
            for j in range(3):
                for i in range(3):
                    self.C[2 * y + j][2 * x + i] = 0
        self.pathcell = set()
        for y in range(H):
            for x in range(W):
                if any(self.C[2 * y + j][2 * x + i] for j in range(3) for i in range(3)):
                    self.pathcell.add((x, y))
        must = set(self.pathcell) | self.keep | self.forced_open
        for (x0, y0, x1, y1, sx) in self.terraces:
            for y in range(y0, y1 + 1):
                for x in range(x0, x1 + 1):
                    must.add((x, y))
        self.must = must
        openm = set()
        for y in range(H):
            for x in range(W):
                cx, cy = x + 0.5, y + 0.5
                d = self.dist_path(cx, cy) - 1.9 - 1.4 * (self.n2(cx, cy) + 0.45)
                ok = d <= 0
                for (ex, ey, rx, ry) in self.clearings:
                    if ((cx - ex) / rx) ** 2 + ((cy - ey) / ry) ** 2 <= 1 + 0.25 * self.n1(cx * 2, cy * 2):
                        ok = True
                if ok:
                    openm.add((x, y))
        # bomen op een raster van 2x2-cellen
        CW, CH = (W + 1) // 2, (H + 1) // 2
        self.tree = set()
        for cy in range(CH):
            for cx in range(CW):
                cells = [(2 * cx + i, 2 * cy + j) for j in (0, 1) for i in (0, 1)]
                if any(c in must for c in cells):
                    assert not any(c in self.forced_closed for c in cells), ('dicht en open', cx, cy)
                    continue
                border = cx == 0 or cy == 0 or cx == CW - 1 or cy == CH - 1
                n_open = sum(1 for c in cells if c in openm)
                if border or n_open <= 1 or any(c in self.forced_closed for c in cells):
                    self.tree.add((cx, cy))
        for y in range(H):
            for x in range(W):
                self.kind[y][x] = 'T' if (x // 2, y // 2) in self.tree else 'g'
                if self.kind[y][x] == 'g':
                    self.M[y][x] = val(GRASS_MT)

    def is_tree(self, cx, cy):
        CW, CH = (self.W + 1) // 2, (self.H + 1) // 2
        return not (0 <= cx < CW and 0 <= cy < CH) or (cx, cy) in self.tree

    def draw_trees(self):
        for (cx, cy) in self.tree:
            x, y = cx * 2, cy * 2
            L, R, B = self.is_tree(cx - 1, cy), self.is_tree(cx + 1, cy), self.is_tree(cx, cy + 1)
            self.M[y][x] = val(0x1D4 if L else 0x1D6, 1, 0)
            self.M[y][x + 1] = val(0x1D5 if R else 0x1D7, 1, 0)
            if y + 1 < self.H:
                if B:
                    self.M[y + 1][x] = val(0x1DC, 1, 0); self.M[y + 1][x + 1] = val(0x1DD, 1, 0)
                else:
                    self.M[y + 1][x] = val(0x1E4 if L else 0x1E6, 1, 0)
                    self.M[y + 1][x + 1] = val(0x1E5 if R else 0x1E7, 1, 0)

    def crowns(self):
        """Kruin van een boom in de onderste rij van een open cel erboven (alleen op gewoon gras)."""
        for (cx, cy) in self.tree:
            x, y = cx * 2, cy * 2
            if y == 0 or self.is_tree(cx, cy - 1):
                continue
            for i, m in ((0, 0x1CE), (1, 0x1CF)):
                if self.kind[y - 1][x + i] == 'g' and (x + i, y - 1) not in self.keep:
                    self.M[y - 1][x + i] = val(m)
                    self.kind[y - 1][x + i] = 'c'

    def draw_terraces(self):
        for (x0, y0, x1, y1, sx) in self.terraces:
            for y in range(y0, y1 + 1):
                for x in range(x0, x1 + 1):
                    side = 'W' if x == x0 else 'E' if x == x1 else ''
                    if y == y1:
                        m = WALL['FOOT_' + side] if side else WALL['FOOT']
                    elif y == y1 - 1:
                        m = WALL[side] if side else WALL['FACE']
                    elif side:
                        m = WALL[side]
                    else:
                        m = None
                    if m is not None:
                        self.M[y][x] = val(m, 1, 0)
                        self.kind[y][x] = 'w'
                    elif self.kind[y][x] == 'T':
                        raise AssertionError(('boom op terras', x, y))
            for y in (y1 - 1, y1):
                for i in (0, 1):
                    self.M[y][sx + i] = val(STAIRS[i])
                    self.kind[y][sx + i] = 's'

    def draw_paths(self):
        for (x, y) in self.pathcell:
            if self.kind[y][x] != 'g':
                continue
            corners = [[self.C[2 * y + j][2 * x + i] for i in range(3)] for j in range(3)]
            self.M[y][x] = val(path_mt(corners, x, y))
            self.kind[y][x] = 'p'

    def arrow(self, x, y, beh):
        """Pijl-warp op een pad- of grascel."""
        if self.kind[y][x] == 'p':
            corners = [[self.C[2 * y + j][2 * x + i] for i in range(3)] for j in range(3)]
            self.M[y][x] = val(path_mt(corners, x, y, beh))
        else:
            self.M[y][x] = val(addmt(('grassarrow', beh), GRASS, [0] * 4, NORMAL | beh))

    # ---------------------------------------------------------------- decor
    def free(self, x, y, w, h, kinds='g'):
        return all(0 <= x + dx < self.W and 0 <= y + dy < self.H and self.kind[y + dy][x + dx] in kinds and
                   (x + dx, y + dy) not in self.keep for dx in range(w) for dy in range(h))

    def stamp(self, name, x, y, check=None, force=False):
        w, h, solid = STAMPS[name]
        if force:
            assert all(self.kind[y + dy][x + dx] in 'gp' for dy in range(h) for dx in range(w)), (name, x, y)
        elif not self.free(x, y, w, h):
            return False
        old = [(x + dx, y + dy, self.M[y + dy][x + dx], self.kind[y + dy][x + dx]) for dy in range(h) for dx in range(w)]
        for dy in range(h):
            for dx in range(w):
                s = solid(dx, dy)
                mt = NAMES['%s_%d_%d' % (name, dx, dy)]
                if self.kind[y + dy][x + dx] == 'p':          # op het pad: onderlaag van het pad houden
                    low = MT[(self.M[y + dy][x + dx] & 0x3FF) - 0x200][:4]
                    mt = addmt(('over', mt, tuple(low)), low, MT[mt - 0x200][4:], ATTR[mt - 0x200])
                self.M[y + dy][x + dx] = val(mt, 1 if s else 0, 0 if s else 3)
                self.kind[y + dy][x + dx] = 'd'
        if check and not check():
            for (a, b, m, k) in old:
                self.M[b][a], self.kind[b][a] = m, k
            return False
        return True

    def near_tree(self, x, y, r=1):
        return any(0 <= x + dx < self.W and 0 <= y + dy < self.H and self.kind[y + dy][x + dx] == 'T'
                   for dx in range(-r, r + 1) for dy in range(-r, r + 1))

    def scatter(self, names, n, edge_bias=0.75, sep=1):
        cells = [(x, y) for y in range(self.H) for x in range(self.W) if self.free(x, y, 1, 1)]
        self.rng.shuffle(cells)
        cells.sort(key=lambda c: 0 if (self.near_tree(c[0], c[1]) and self.rng.random() < edge_bias) else 1)
        used = 0
        for (x, y) in cells:
            if used >= n:
                break
            if any(0 <= x + a < self.W and 0 <= y + b < self.H and self.kind[y + b][x + a] == 'd' and
                   (self.M[y + b][x + a] & 0x3FF) in SMALL_IDS for a in range(-sep, sep + 1) for b in range(-sep, sep + 1)):
                continue
            nm = names[used % len(names)] if isinstance(names, list) else names
            self.M[y][x] = val(NAMES[nm])
            self.kind[y][x] = 'd'
            used += 1
        return used

    def tall_grass(self, cx, cy, rx, ry):
        for y in range(self.H):
            for x in range(self.W):
                if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1 + 0.3 * self.n1(x * 2.3, y * 2.3) and \
                        self.free(x, y, 1, 1):
                    self.M[y][x] = val(TALL_MT)
                    self.kind[y][x] = 't'

    def small_trees(self, p=0.45, check=None):
        """Losse boompjes van 1 breed tegen de bosrand: maakt de rand van het 2x2-raster rommeliger."""
        for y in range(self.H - 1):
            for x in range(self.W):
                if not (self.free(x, y, 1, 2) and self.kind[y + 1][x] == 'g'):
                    continue
                side = any(0 <= x + dx < self.W and self.kind[y][x + dx] == 'T' and self.kind[y + 1][x + dx] == 'T'
                           for dx in (-1, 1))
                above = y > 0 and self.kind[y - 1][x] == 'T'
                if (side or above) and self.rng.random() < p:
                    if any(self.kind[y + b][x + a] == 'b' for a in (-1, 0, 1) for b in (-1, 0, 1, 2)
                           if 0 <= x + a < self.W and 0 <= y + b < self.H):
                        continue
                    top, foot = SMALL_TREE[self.rng.randrange(2)]
                    old = (self.M[y][x], self.M[y + 1][x])
                    self.M[y][x] = val(top, 1, 0)
                    self.M[y + 1][x] = val(foot, 1, 0)
                    if check and not check():
                        self.M[y][x], self.M[y + 1][x] = old
                        continue
                    self.kind[y][x] = self.kind[y + 1][x] = 'b'

    # ---------------------------------------------------------------- controle
    def walk(self, x, y, blocked=()):
        v = self.M[y][x]
        return (x, y) not in blocked and not (v & 0xC00) and (v >> 12) in (0, 3)

    def reach(self, start, blocked=()):
        seen, q = {start}, deque([start])
        while q:
            x, y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                p = (x + dx, y + dy)
                if p in seen or not (0 <= p[0] < self.W and 0 <= p[1] < self.H) or not self.walk(*p, blocked=blocked):
                    continue
                seen.add(p)
                q.append(p)
        return seen

    def save(self, layout_name, prim, sec, layout_dir=None):
        d = layout_dir or layout_name
        os.makedirs('data/layouts/' + d, exist_ok=True)
        if layout_dir is None:
            for row in self.M:
                assert all(v is not None for v in row)
            open('data/layouts/%s/map.bin' % d, 'wb').write(
                struct.pack('<%dH' % (self.W * self.H), *[v for r in self.M for v in r]))
            open('data/layouts/%s/border.bin' % d, 'wb').write(
                struct.pack('<4H', val(0x1D4, 1, 0), val(0x1D5, 1, 0), val(0x1DC, 1, 0), val(0x1DD, 1, 0)))
        return save_layout(layout_name, self.W, self.H, prim, sec, d)


SMALL_IDS = set()


def save_layout(name, W, H, prim, sec, d):
    lj = open('data/layouts/layouts.json').read()
    c = const(name)
    entry = '''    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "%s",
      "secondary_tileset": "%s",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    }''' % (c, name, W, H, prim, sec, d, d)
    if '"LAYOUT_%s"' % c in lj:
        i = lj.index('"id": "LAYOUT_%s"' % c); s = lj.rindex('    {', 0, i); e = lj.index('    }', i) + 5
        lj = lj[:s] + entry + lj[e:]
    else:
        i = lj.rindex('    }\n  ]')
        lj = lj[:i + 5] + ',\n' + entry + lj[i + 5:]
    json.loads(lj)
    open('data/layouts/layouts.json', 'w').write(lj)
    return 'LAYOUT_' + c


def register_map(name):
    g = open('data/maps/map_groups.json').read()
    if '"%s"' % name not in g:
        i = g.index('"%s": [' % GROUP); j = g.index('\n  ]', i)
        g = g[:j] + ',\n    "%s"' % name + g[j:]
    d = json.loads(g)
    assert len(d[GROUP]) <= 128
    open('data/maps/map_groups.json', 'w').write(g)
    es = open('data/event_scripts.s').read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        anchor = '\t.include "data/maps/SpacetimeCave/scripts.inc"\n'
        assert anchor in es
        es = es.replace(anchor, anchor + inc, 1)
        open('data/event_scripts.s', 'w').write(es)


def write_map(name, layout, objs, warps, bgs, coords=(), **kw):
    m = {'id': 'MAP_' + const(name), 'name': name, 'layout': layout, 'music': 'MUS_RG_VIRIDIAN_FOREST',
         'region_map_section': 'MAPSEC_GLIMWOOD_TANGLE', 'requires_flash': False, 'weather': 'WEATHER_NONE',
         'map_type': 'MAP_TYPE_UNDERGROUND', 'allow_cycling': False, 'allow_escaping': False, 'allow_running': True,
         'show_map_name': True, 'battle_scene': 'MAP_BATTLE_SCENE_NORMAL', 'connections': None,
         'object_events': objs, 'warp_events': warps, 'coord_events': list(coords), 'bg_events': bgs}
    m.update(kw)
    os.makedirs('data/maps/' + name, exist_ok=True)
    open('data/maps/%s/map.json' % name, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    register_map(name)


def lid(o, name):
    o['local_id'] = name
    return o


# ====================================================================== flags (FLAG_GROUNDED 880-919)
FLAGS = [
    (880, 'FLAG_GLIMWOOD_MET_WITCH', 'Glimwood: de heks heeft zich voorgesteld'),
    (881, 'FLAG_GLIMWOOD_GANG_1', 'Glimwood: Impidimp-bende 1 (west) verslagen'),
    (882, 'FLAG_GLIMWOOD_GANG_2', 'Glimwood: Impidimp-bende 2 (oost) verslagen'),
    (883, 'FLAG_GLIMWOOD_GANG_3', 'Glimwood: Impidimp-bende 3 (blokkeert de weg naar Ballonlea) verslagen'),
    (884, 'FLAG_GLIMWOOD_GANG_BOSS', 'Ballonlea: Grimmsnarl (baas van de bende, blokkeert de trap) verslagen'),
    (885, 'FLAG_GLIMWOOD_XERNEAS_DONE', 'Ballonlea: Xerneas gevangen, het bos licht weer op'),
    (886, 'FLAG_SPACETIME_GLIMWOOD_DONE', 'Spacetime-sidequest klaar: Yveltal gevangen'),
    (887, 'FLAG_GLIMWOOD_SCENE_PENDING', 'Ballonlea: tekst na het oplichten nog tonen (eenmalig)'),
    (888, 'FLAG_GLIMWOOD_YVELTAL_SEEN', 'Glimwood: Yveltal-scene gezien (eenmalig)'),
    (889, 'FLAG_ITEM_GLIMWOOD_EXP_CANDY_XL', 'Glimwood: Exp. Candy XL (westterras)'),
    (890, 'FLAG_ITEM_GLIMWOOD_EJECT_PACK', 'Glimwood: Eject Pack (doodlopend pad oost)'),
    (891, 'FLAG_ITEM_GLIMWOOD_DREAM_BALL', 'Glimwood: Dream Ball (oostterras)'),
    (892, 'FLAG_HIDDEN_ITEM_GLIMWOOD_GALARICA_CUFF', 'Glimwood: verborgen Galarica Cuff (heksenkring)'),
    (893, 'FLAG_ITEM_BALLONLEA_GALARICA_WREATH', 'Ballonlea: Galarica Wreath'),
    (894, 'FLAG_HIDDEN_ITEM_BALLONLEA_EXP_CANDY_L', 'Ballonlea: verborgen Exp. Candy L'),
]


def flags():
    p = 'include/constants/flags.h'
    s = open(p).read()
    blk = '// glimwood { (tools/grounded/maptools/glimwood.py; FLAG_GROUNDED 880-919, %d-919 nog vrij)\n' % (
        max(n for n, *_ in FLAGS) + 1)
    for n, name, why in FLAGS:
        assert 880 <= n <= 919
        blk += '#define %-48s FLAG_GROUNDED(%d) // Project Grounded: %s\n' % (name, n, why)
    blk += '// }'
    if '// glimwood {' in s:
        i = s.index('// glimwood {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        anchor = s.index('// national_park {')
        s = s[:anchor] + blk + '\n' + s[anchor:]
    for n, *_ in FLAGS:
        assert len(re.findall(r'FLAG_GROUNDED\(%d\)' % n, s)) == 1, ('flag dubbel', n)
    open(p, 'w').write(s)


# ====================================================================== mapsecs
MAPSECS = [('MAPSEC_GLIMWOOD_TANGLE', 'GLIMWOOD TANGLE', 'MAPPOPUP_THEME_WOOD', 'Glimwood Tangle (Spacetime Cave)'),
           ('MAPSEC_BALLONLEA', 'BALLONLEA', 'MAPPOPUP_THEME_WOOD', 'Ballonlea (Spacetime Cave)')]


def mapsecs():
    p = 'src/data/region_map/region_map_sections.json'
    s = open(p).read()
    for mid, nm, theme, why in MAPSECS:
        if '"%s"' % mid not in s:
            i = s.rindex('    }\n  ]')
            s = s[:i + 5] + ',\n    {\n      "id": "%s",\n      "name": "%s"\n    }' % (mid, nm) + s[i + 5:]
    json.loads(s)
    open(p, 'w').write(s)
    p = 'src/map_name_popup.c'
    s = open(p).read()
    a = '    [MAPSEC_SPACETIME_CAVE - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_STONE, // Project Grounded: Spacetime Cave\n'
    b = '    [MAPSEC_SPACETIME_CAVE - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_BW_DEFAULT, // Project Grounded: Spacetime Cave\n'
    assert a in s and b in s
    for mid, nm, theme, why in reversed(MAPSECS):
        if '[%s - KANTO' % mid in s:
            continue
        s = s.replace(a, a + '    [%s - KANTO_MAPSEC_COUNT] = %s, // Project Grounded: %s\n' % (mid, theme, why), 1)
        s = s.replace(b, b + '    [%s - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_BW_DEFAULT, // Project Grounded: %s\n' % (mid, why), 1)
    open(p, 'w').write(s)


# ====================================================================== wilde Pokemon
WILD = {
    'GLIMWOOD_TANGLE': dict(land=(15, [
        ('SHIINOTIC', 60, 64), ('POLTEAGEIST', 60, 64), ('RAPIDASH_GALAR', 61, 65), ('ORBEETLE', 61, 65),
        ('ALCREMIE', 61, 65), ('DUBWOOL', 61, 65), ('GRIMMSNARL', 62, 66), ('HATTERENE', 62, 66),
        ('ELDEGOSS', 63, 67), ('OBSTAGOON', 63, 67), ('MIMIKYU', 64, 68), ('SLOWKING_GALAR', 64, 68)])),
}


# ====================================================================== trainers
IV, AI, mon = bd.IV, bd.AI, bd.mon
TRAINERS = [
    ('GLIMWOOD_HEX_MANIAC_MORWEN', 1098, 'MORWEN', 'Hex Maniac', 'Hex Maniac', 'Female', 'Suspicious', AI, [
        mon('Hatterene', 67, ['Dazzling Gleam', 'Psychic', 'Mystical Fire', 'Trick Room']),
        mon('Polteageist', 67, ['Shell Smash', 'Shadow Ball', 'Giga Drain', 'Strength Sap']),
        mon('Mismagius', 67, ['Shadow Ball', 'Dazzling Gleam', 'Nasty Plot', 'Mystical Fire']),
        mon('Gothitelle', 68, ['Psychic', 'Thunderbolt', 'Calm Mind', 'Shadow Ball'])], 'Glimwood, verzamelt vervloekte theekopjes'),
    ('GLIMWOOD_PSYCHIC_SILAS', 1099, 'SILAS', 'Psychic', 'Psychic M', 'Male', 'Intense', AI, [
        mon('Orbeetle', 67, ['Bug Buzz', 'Psychic', 'Sticky Web', 'Calm Mind']),
        mon('Mr. Rime', 67, ['Freeze-Dry', 'Psychic', 'Rapid Spin', 'Focus Blast']),
        mon('Slowking-Galar', 67, ['Sludge Bomb', 'Psychic', 'Flamethrower', 'Trick Room']),
        mon('Indeedee', 68, ['Psychic', 'Hyper Voice', 'Calm Mind', 'Mystical Fire'])], 'Glimwood, pelgrim die al eeuwen rondjes loopt'),
    ('GLIMWOOD_BEAUTY_ODETTE', 1107, 'ODETTE', 'Beauty', 'Beauty', 'Female', 'Female', AI, [
        mon('Alcremie', 67, ['Dazzling Gleam', 'Recover', 'Calm Mind', 'Mystical Fire']),
        mon('Sylveon', 67, ['Hyper Voice', 'Shadow Ball', 'Wish', 'Calm Mind']),
        mon('Togekiss', 67, ['Air Slash', 'Dazzling Gleam', 'Aura Sphere', 'Roost']),
        mon('Rapidash-Galar', 68, ['Play Rough', 'Psycho Cut', 'High Horsepower', 'Swords Dance'])], 'Glimwood, feeën-cosplay'),
    ('BALLONLEA_GENTLEMAN_ARTHUR', 1108, 'ARTHUR', 'Gentleman', 'Gentleman', 'Male', 'Rich', AI, [
        mon('Dubwool', 67, ['Cotton Guard', 'Body Press', 'Double-Edge', 'Wild Charge']),
        mon('Corviknight', 67, ['Brave Bird', 'Iron Head', 'Bulk Up', 'Roost']),
        mon('Obstagoon', 67, ['Obstruct', 'Knock Off', 'Close Combat', 'Gunk Shot']),
        mon("Sirfetch'd", 68, ['Leaf Blade', 'Close Combat', 'Brave Bird', 'Knock Off'])], 'Ballonlea, theatercriticus'),
]


def trainers():
    p = 'include/constants/opponents.h'
    s = open(p).read()
    blk = '// glimwood { (tools/grounded/maptools/glimwood.py; id 1098, 1099, 1107, 1108)\n'
    for key, n, *_, why in TRAINERS:
        blk += '#define TRAINER_%-28s%d // Project Grounded: %s\n' % (key, n, why)
    blk += '// }'
    if '// glimwood {' in s:
        i = s.index('// glimwood {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        s = s.replace('\n#define TRAINERS_COUNT', '\n' + blk + '\n\n#define TRAINERS_COUNT', 1)
    for key, n, *_ in TRAINERS:
        hits = re.findall(r'^#define TRAINER_\w+\s+%d\b' % n, s, re.M)
        assert len(hits) == 1, ('trainer-id dubbel', n, hits)
        assert n < 1200
    open(p, 'w').write(s)
    p = 'src/data/trainers.party'
    s = open(p).read()
    blk = '/* --- glimwood (tools/grounded/maptools/glimwood.py) --- */\n\n'
    for key, n, nm, cls, pic, gender, music, ai, team, why in TRAINERS:
        hdr = ['Name: ' + nm, 'Class: ' + cls, 'Pic: ' + pic, 'Gender: ' + gender, 'Music: ' + music,
               'Double Battle: No', ai]
        blk += '=== TRAINER_%s ===\n%s\n\n%s\n\n' % (key, '\n'.join(hdr), '\n\n'.join(team))
    blk = blk.rstrip('\n') + '\n\n/* --- einde glimwood --- */'
    s = bd.replace_block(s, '/* --- glimwood', '/* --- einde glimwood --- */', blk)
    open(p, 'w').write(s)


# ====================================================================== kaarten: Glimwood Tangle
FW, FH = 48, 60
F_ENTRY = (22, 23)                  # x van de twee zuidpijl-warps (rij FH-1), de scheur uit de hub komt hier aan
F_EXIT = (30, 31)                   # x van de twee noordpijl-warps (rij 0) naar Ballonlea
F_RING = (20, 26)                   # heksenkring 5x5 (linksboven); Yveltal in het midden
F_WITCH = (19, 53)
F_GANGS = {1: [(8, 29)], 2: [(41, 38)], 3: [(30, 7), (31, 7)]}
F_TRAINERS = [('GLIMWOOD_HEX_MANIAC_MORWEN', 'OBJ_EVENT_GFX_HEX_MANIAC', 26, 36, 'LEFT', 4, 'Morwen'),
              ('GLIMWOOD_PSYCHIC_SILAS', 'OBJ_EVENT_GFX_PSYCHIC_M', 12, 17, 'DOWN', 3, 'Silas'),
              ('GLIMWOOD_BEAUTY_ODETTE', 'OBJ_EVENT_GFX_BEAUTY', 37, 22, 'LEFT', 3, 'Odette')]
F_TERRACES = [(3, 4, 14, 12, 8), (36, 8, 46, 16, 40)]      # (x0, y0, x1, y1, trap-x), y1 = onderste wandrij
F_ITEMS = [(5, 6, 'ITEM_EXP_CANDY_XL', 'FLAG_ITEM_GLIMWOOD_EXP_CANDY_XL'),
           (35, 49, 'ITEM_EJECT_PACK', 'FLAG_ITEM_GLIMWOOD_EJECT_PACK'),
           (44, 10, 'ITEM_DREAM_BALL', 'FLAG_ITEM_GLIMWOOD_DREAM_BALL')]
F_HIDDEN = [(20, 26, 'ITEM_GALARICA_CUFF', 'FLAG_HIDDEN_ITEM_GLIMWOOD_GALARICA_CUFF')]
F_YVELTAL = (F_RING[0] + 2, F_RING[1] + 2)


def build_forest():
    m = Map('GlimwoodTangle', FW, FH, SEED)
    # hoofdpad: van de scheur onderaan, kronkelend naar het noorden
    m.path([(23.0, 61), (22.6, 56), (20.0, 52), (16.5, 48.5), (14.5, 44), (15.5, 39.5), (19.5, 36.5), (24.5, 35.5),
            (29.0, 34.0), (32.5, 30.5), (34.0, 26.0), (32.0, 21.5), (29.0, 18.5), (29.5, 14.0), (31.5, 10.5),
            (31.0, 6.0), (31.0, -1)])
    # westlus langs de heksenkring en het westterras
    m.path([(14.5, 44), (10.0, 40.5), (8.5, 35.0), (8.5, 29.5), (10.5, 24.0), (14.5, 20.5), (19.0, 21.5),
            (22.5, 24.0)], r=1.0)
    m.path([(22.5, 32.5), (23.5, 35.5)], r=1.0)
    m.path([(12.5, 21.5), (9.0, 16.5), (9.0, 13.0)], r=1.0)                 # naar de trap van het westterras
    m.path([(29.0, 18.5), (25.5, 21.0), (24.5, 24.5)], r=0.95)             # dwarspad naar de kring
    # doodlopend pad naar het zuidoosten (Eject Pack) en naar het oostterras
    m.path([(32.5, 30.5), (38.0, 33.5), (41.5, 38.5), (40.5, 44.0), (36.5, 48.5)], r=1.0)
    m.path([(34.0, 22.0), (37.5, 21.0), (41.0, 18.5), (41.0, 17.0)], r=1.0)
    m.clearings = [(19.5, 51, 5.5, 4.0), (22.5, 28.5, 6.0, 5.0), (8.0, 30.0, 3.5, 5.0), (40.0, 39.0, 4.0, 4.0),
                   (36.0, 48.0, 3.5, 2.5), (15.0, 41.0, 3.5, 3.0), (28.0, 14.5, 3.5, 3.0)]
    m.terraces = F_TERRACES
    events = [F_WITCH, F_YVELTAL] + [p for v in F_GANGS.values() for p in v] + [(x, y) for _, _, x, y, *_ in F_TRAINERS] + \
             [(x, y) for x, y, *_ in F_ITEMS]
    for (x, y) in events:
        m.keep.add((x, y))
    for x in F_ENTRY:
        m.keep |= {(x, FH - 1), (x, FH - 2)}
    for x in F_EXIT:
        m.keep |= {(x, 0), (x, 1)}
    for x0, y0, x1, y1, sx in F_TERRACES:
        m.keep |= {(sx, y1 + 1), (sx + 1, y1 + 1)}
    m.forced_open |= {(F_RING[0] + i, F_RING[1] + j) for i in range(5) for j in range(5)}
    m.keep |= {(x, y) for x, y, *_ in F_HIDDEN}
    # de weg naar Ballonlea is op rij 6-7 precies 2 breed: bende 3 staat erin
    m.forced_closed |= {(28, 6), (29, 6), (28, 7), (29, 7), (32, 6), (33, 6), (32, 7), (33, 7)}
    m.plan()
    m.draw_trees()
    m.draw_terraces()
    m.draw_paths()
    for x in F_ENTRY:
        m.arrow(x, FH - 1, MB_SOUTH_ARROW)
    for x in F_EXIT:
        m.arrow(x, 0, MB_NORTH_ARROW)
    m.stamp('ring', *F_RING, force=True)
    m.crowns()
    return m


def decorate(m, start, targets, plan, gate=()):
    """Decor plaatsen; elke massieve stempel mag geen doel onbereikbaar maken (poortwachters tellen niet mee)."""
    objs = set(targets) - set(gate)

    def ok():
        r = m.reach(start, objs)
        return all(any((p[0] + dx, p[1] + dy) in r for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) or p in r
                   for p in targets)
    rng = m.rng
    for name, n in plan:
        w, h, _ = STAMPS[name]
        cands = [(x, y) for y in range(1, m.H - h) for x in range(1, m.W - w) if m.free(x, y, w, h)]
        if name.startswith('root'):
            # wortels groeien uit het bos: de rij erboven moet bos zijn
            cands = [(x, y) for (x, y) in cands if any(m.near_tree(x + i, y + j, 1) for i in range(w) for j in range(h))]
        elif name.startswith('tall'):
            cands = [(x, y) for (x, y) in cands if m.near_tree(x, y, 1) or m.near_tree(x + 1, y + 2, 1)]
        rng.shuffle(cands)
        placed = 0
        for (x, y) in cands:
            if placed >= n:
                break
            if m.stamp(name, x, y, ok):
                placed += 1
        print('  %-7s %d/%d' % (name, placed, n))
    return ok


def forest_map():
    m = build_forest()
    start = (F_ENTRY[0], FH - 1)
    gang_cells = {p for v in F_GANGS.values() for p in v}
    targets = [F_WITCH, F_YVELTAL, (F_EXIT[0], 0)] + list(gang_cells) + \
              [(x, y) for _, _, x, y, *_ in F_TRAINERS] + [(x, y) for x, y, *_ in F_ITEMS]
    m.tall_grass(10.0, 40.5, 3.2, 2.4)
    m.tall_grass(8.0, 26.0, 2.2, 3.4)
    m.tall_grass(38.5, 35.5, 3.0, 2.0)
    m.tall_grass(26.5, 39.0, 3.4, 1.8)
    m.tall_grass(33.5, 15.5, 2.4, 2.2)
    m.tall_grass(17.5, 46.0, 2.2, 1.6)
    ok = decorate(m, start, targets, [('rootR', 3), ('rootL', 3), ('rootS', 3), ('tallg', 5), ('tallc', 5), ('tallp', 4),
                                 ('gpur', 4), ('gblue', 4), ('log', 4)], gate=F_GANGS[3])
    m.small_trees(check=ok)
    n = m.scatter(['m_cyan', 'm_purple', 'm_green', 'moss1', 'm_blue', 'm_pink', 'glow', 'm_brown', 'moss2', 'm_red'],
                  210)
    print('  klein decor', n)
    for p in [(x, y) for y in range(FH) for x in range(FW) if m.M[y][x] is None]:
        raise AssertionError(('lege cel', p))
    return m


# ====================================================================== kaarten: Ballonlea
BW, BH = 36, 34
B_ENTRY = (17, 18)                  # noordpijl-warps van het bos komen hier aan (rij BH-1, zuidpijl terug)
B_TERRACE = (9, 2, 26, 10, 17)      # terras met de heksenkring van Xerneas, trap op x 17-18
B_RING = (15, 3)
PLAZA = (18.0, 21.5, 3.6)           # middelpunt en straal van het ronde pleintje
B_XERNEAS = (B_RING[0] + 2, B_RING[1] + 2)
B_HOUSES = [('house', 4, 13), ('house2', 25, 15), ('house2', 5, 21), ('house', 26, 24)]   # (stempel, x, y)
B_WITCH = (9, 17)                   # voor haar huis (het eerste)
B_BOSS = [(17, 11), (18, 11)]       # Grimmsnarl + Morgrem op de trap
B_TRAINER = ('BALLONLEA_GENTLEMAN_ARTHUR', 'OBJ_EVENT_GFX_GENTLEMAN', 22, 21, 'LEFT', 3, 'Arthur')
B_ITEMS = [(31, 12, 'ITEM_GALARICA_WREATH', 'FLAG_ITEM_BALLONLEA_GALARICA_WREATH')]
B_HIDDEN = [(24, 4, 'ITEM_EXP_CANDY_L', 'FLAG_HIDDEN_ITEM_BALLONLEA_EXP_CANDY_L')]


def ballonlea_map():
    m = Map('GlimwoodTangle_Ballonlea', BW, BH, SEED + 1)
    cx, cy, rr = PLAZA
    m.rings.append((cx, cy, rr - 1.0, 1.05))                               # rond pleintje met een eilandje
    m.path([(18.0, 35), (18.2, 30.0), (17.4, 27.5), (cx, cy + rr - 0.5)])
    m.path([(cx, cy - rr + 0.5), (18.0, 14.5), (18.0, 11.5)], r=1.0)      # naar de trap
    m.path([(cx - rr + 0.5, cy - 0.5), (12.5, 21.2), (10.0, 19.0), (7.0, 18.2), (6.0, 17.6)], r=0.95)  # heksenhuis
    m.path([(cx + rr - 0.5, cy - 1.0), (23.0, 20.6), (25.0, 18.7), (27.0, 19.6)], r=0.9)
    m.path([(cx - rr + 0.5, cy + 1.2), (12.5, 24.4), (10.0, 26.4), (6.8, 25.8)], r=0.9)
    m.path([(cx + rr - 0.5, cy + 1.2), (23.5, 24.0), (24.5, 27.4), (27.5, 28.7)], r=0.9)
    m.path([(18.0, 8.6), (18.0, 6.6)], r=0.8)                                # op het terras naar de kring
    m.clearings = [(18.0, 21.5, 13.5, 9.0), (18.0, 6.0, 8.0, 4.0), (31.0, 13.0, 2.5, 2.5), (29.0, 28.0, 4.0, 3.0),
                   (6.0, 28.5, 3.5, 2.5)]
    m.terraces = [B_TERRACE]
    for p in [B_WITCH, B_XERNEAS, B_TRAINER[2:4]] + B_BOSS + [(x, y) for x, y, *_ in B_ITEMS]:
        m.keep.add(tuple(p))
    for x in B_ENTRY:
        m.keep |= {(x, BH - 1), (x, BH - 2)}
    m.keep |= {(x, y) for x, y, *_ in B_HIDDEN}
    for name, x, y in B_HOUSES:
        m.forced_open |= {(x + i, y + j) for i in range(4) for j in range(5)}
        m.nopath |= {(x + i, y + j) for i in range(4) for j in range(4)}
        m.keep |= {(x + 1, y + 4), (x + 2, y + 4)}                          # voor de deur
    m.forced_open |= {(B_RING[0] + i, B_RING[1] + j) for i in range(5) for j in range(5)}
    m.plan()
    m.draw_trees()
    m.draw_terraces()
    m.draw_paths()
    for x in B_ENTRY:
        m.arrow(x, BH - 1, MB_SOUTH_ARROW)
    for name, x, y in B_HOUSES:
        for i in range(4):
            for j in range(4):
                if m.kind[y + j][x + i] == 'p':
                    m.kind[y + j][x + i] = 'g'
                    m.M[y + j][x + i] = val(GRASS_MT)
        assert m.stamp(name, x, y), ('huis', name, x, y)
    m.stamp('gring', *B_RING, force=True)
    m.stamp('tallp', 17, 19, force=True)                                   # middelpunt van het plein
    m.crowns()
    start = (B_ENTRY[0], BH - 1)
    targets = [B_WITCH, B_XERNEAS, B_TRAINER[2:4]] + B_BOSS + [(x, y) for x, y, *_ in B_ITEMS] + \
              [(x + 1, y + 3) for _, x, y in B_HOUSES]
    # bloemen in het dorp (bij de huizen)
    for name, x, y in B_HOUSES:
        for (a, b) in ((x - 1, y + 3), (x + 4, y + 3), (x - 1, y + 2)):
            if m.free(a, b, 1, 1) and m.rng.random() < 0.8:
                m.M[b][a] = val(FLOWERS)
                m.kind[b][a] = 'f'
    ok = decorate(m, start, targets, [('tallg', 2), ('tallc', 2), ('tallp', 2), ('gpur', 1), ('gblue', 1), ('rootR', 1),
                                 ('rootL', 1)], gate=B_BOSS)
    m.small_trees(0.35, check=ok)
    print('  klein decor', m.scatter(['m_pink', 'm_cyan', 'm_purple', 'glow', 'm_green', 'moss1', 'm_blue', 'm_red'], 55))
    return m


# ====================================================================== scripts
def forest_scripts():
    S = bd.Scr('GlimwoodTangle', '@ Project Grounded: GlimwoodTangle (tools/grounded/maptools/glimwood.py)\n'
               '@ Stervend bos (layout GlimwoodTangle_Dying) tot Xerneas gevangen is; daarna licht, en Yveltal.\n'
               'GlimwoodTangle_MapScripts::\n'
               '\tmap_script MAP_SCRIPT_ON_TRANSITION, GlimwoodTangle_OnTransition\n'
               '\tmap_script MAP_SCRIPT_ON_FRAME_TABLE, GlimwoodTangle_OnFrame\n\t.byte 0\n')
    P, X = S.P, S.T
    S.raw(f'''GlimwoodTangle_OnTransition:
	setflag FLAG_TEMP_1
	call_if_unset FLAG_GLIMWOOD_MET_WITCH, {P}SetIntro
	goto_if_set FLAG_GLIMWOOD_XERNEAS_DONE, {P}StateBright
	setmaplayoutindex LAYOUT_GLIMWOOD_TANGLE_DYING
	setweather WEATHER_SHADE
	savebgm MUS_RG_POKE_TOWER
	end

{P}StateBright:
	goto_if_set FLAG_SPACETIME_GLIMWOOD_DONE, {P}StateEnd
	clearflag FLAG_TEMP_1
	call_if_unset FLAG_GLIMWOOD_YVELTAL_SEEN, {P}SetYveltal
{P}StateEnd:
	end

{P}SetIntro:
	setvar VAR_TEMP_1, 1
	return

{P}SetYveltal:
	setvar VAR_TEMP_1, 2
	return

GlimwoodTangle_OnFrame:
	map_script_2 VAR_TEMP_1, 1, {P}Intro
	map_script_2 VAR_TEMP_1, 2, {P}YveltalScene
	.2byte 0

{P}Intro:
	lockall
	setvar VAR_TEMP_1, 0
	delay 20
	msgbox {X}Intro1, MSGBOX_DEFAULT
	msgbox {X}Intro2, MSGBOX_DEFAULT
	setflag FLAG_GLIMWOOD_MET_WITCH
	releaseall
	end

{P}YveltalScene:
	lockall
	setvar VAR_TEMP_1, 0
	setflag FLAG_GLIMWOOD_YVELTAL_SEEN
	delay 20
	playmoncry SPECIES_YVELTAL, CRY_MODE_ENCOUNTER
	fadescreenspeed FADE_TO_BLACK, 2
	fadescreenspeed FADE_FROM_BLACK, 2
	waitmoncry
	msgbox {X}YveltalScene, MSGBOX_DEFAULT
	releaseall
	end

{P}Witch::
	lock
	faceplayer
	goto_if_set FLAG_SPACETIME_GLIMWOOD_DONE, {P}WitchDone
	goto_if_set FLAG_GLIMWOOD_XERNEAS_DONE, {P}WitchLight
	random 3
	switch VAR_RESULT
	case 0, {P}Quiz0
	case 1, {P}Quiz1
	msgbox {X}Quiz2, MSGBOX_DEFAULT
	release
	end

{P}Quiz0:
	msgbox {X}Quiz0, MSGBOX_DEFAULT
	release
	end

{P}Quiz1:
	msgbox {X}Quiz1, MSGBOX_DEFAULT
	release
	end

{P}WitchLight:
	msgbox {X}WitchLight, MSGBOX_DEFAULT
	release
	end

{P}WitchDone:
	msgbox {X}WitchDone, MSGBOX_DEFAULT
	release
	end
''', [('Intro1', "Ah, a visitor. Mind the mushrooms, dearie. Some of them used to be people."),
          ('Intro2', "I'm the witch of BALLONLEA. Retired. An IMPIDIMP gang and a deathly aura are snuffing out "
                     "the forest's light. Only XERNEAS can relight it. It sleeps north of the village. "
                     "Pop quiz later. There's always a pop quiz."),
          ('Quiz0', "Pop quiz! What glows in the dark, has no friends and talks to mushrooms? ...Correct, it's me. "
                    "Ten points to nobody."),
          ('Quiz1', "Pop quiz! How many IMPIDIMP does it take to ruin a forest? ...Trick question. They don't "
                    "count. They can't count. That's the whole problem."),
          ('Quiz2', "Pop quiz! True or false: the mushrooms are watching you. ...You hesitated. Wrong answer. "
                    "They're also judging you."),
          ('WitchLight', "The light's back! Lovely. Now something with big red wings is sulking in the fairy "
                         "ring. Life and death, dearie. You can't have one without the other bothering you."),
          ('WitchDone', "Life and death, both in your bag. Very tidy. Final quiz: was it worth it? ...Don't answer. "
                        "I'm a witch, not a therapist."),
          ('YveltalScene', "The new light flickers. Something vast lands in the fairy ring, wings like a funeral "
                           "nobody was invited to. Where there's life, there's paperwork. And YVELTAL.")])
    for key, gfx, x, y, face, sight, nm in F_TRAINERS:
        txt = {
            'Morwen': ("My teacups are cursed. I collect them. I'm not giving you one.",
                       "Fine. Take the teacup. No? Nobody ever takes the teacup.",
                       "The forest whispers my name. Mispronounces it, but still."),
            'Silas': ("I've walked in circles here since the old Galar kings. The path keeps moving. "
                      "Or I do. Fight me while I figure it out.",
                      "Hm. Lost again. To you, this time.",
                      "If you see the exit, don't tell me. I've grown attached to being lost."),
            'Odette': ("I'm a fairy! Real wings! ...They're cardboard. Don't look at the tape.",
                       "My wings fell off. Very on-brand for this forest.",
                       "The mushrooms think I'm one of them. I haven't told them."),
        }[nm]
        S.trainer(nm, key, *txt)
    for g, (sp, lv, sp2, lv2, objs, txt) in {
        1: ('IMPIDIMP', 64, 'MORGREM', 64, ['GANG_1'], "Two IMPIDIMP-gang members are drawing mustaches on a "
                                                        "glowing mushroom. They'd like to draw one on you."),
        2: ('MORGREM', 65, 'IMPIDIMP', 64, ['GANG_2'], "MORGREM is stealing the light out of the mushrooms and "
                                                        "putting it in a jar. The jar says MINE."),
        3: ('MORGREM', 65, 'MORGREM', 65, ['GANG_3A', 'GANG_3B'], "Two MORGREM block the road to BALLONLEA. "
                                                                   "Their sign says NO ENTRY. It's spelled wrong."),
    }.items():
        rm = ''.join('\tremoveobject LOCALID_GLIMWOOD_%s\n' % o for o in objs)
        S.raw(f'''{P}Gang{g}::
	lock
	faceplayer
	playmoncry SPECIES_{sp2}, CRY_MODE_ENCOUNTER
	msgbox {X}Gang{g}, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_{sp}, {lv}, ITEM_NONE, SPECIES_{sp2}, {lv2}, ITEM_NONE
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, {P}Gang{g}Gone
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, {P}Gang{g}Gone
	release
	end

{P}Gang{g}Gone::
	fadescreen FADE_TO_BLACK
{rm}	setflag FLAG_GLIMWOOD_GANG_{g}
	fadescreen FADE_FROM_BLACK
	msgbox {X}GangGone, MSGBOX_DEFAULT
	release
	end
''', [('Gang%d' % g, txt)])
    S.raw('', [('GangGone', "The gang scatters into the dark, giggling. A little light seeps back into the "
                            "mushrooms. Not much. Like a phone at one percent.")])
    S.raw(f'''{P}Yveltal::
	lock
	faceplayer
	playmoncry SPECIES_YVELTAL, CRY_MODE_ENCOUNTER
	msgbox {X}Yveltal, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_YVELTAL, 70
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, {P}YveltalCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, {P}YveltalCocoon
	release
	end

{P}YveltalCocoon::
	msgbox {X}YveltalCocoon, MSGBOX_DEFAULT
	release
	end

{P}YveltalCaught::
	removeobject LOCALID_GLIMWOOD_YVELTAL
	setflag FLAG_SPACETIME_GLIMWOOD_DONE
	msgbox {X}YveltalCaught, MSGBOX_DEFAULT
	release
	end
''', [('Yveltal', "YVELTAL spreads its wings over the fairy ring. The mushrooms nearest to it go grey. "
                      "It looks at you the way a vulture looks at a long walk."),
          ('YveltalCocoon', "YVELTAL folds into a dark cocoon... and hatches again almost immediately, visibly "
                            "annoyed. Death doesn't do sick days. Try again."),
          ('YveltalCaught', "YVELTAL is yours. The forest keeps its light, and its shadows. Both behave, for "
                            "now. GLIMWOOD TANGLE is at peace.")])
    S.write()


def ballonlea_scripts():
    S = bd.Scr('GlimwoodTangle_Ballonlea', '@ Project Grounded: GlimwoodTangle_Ballonlea (tools/grounded/maptools/glimwood.py)\n'
               'GlimwoodTangle_Ballonlea_MapScripts::\n'
               '\tmap_script MAP_SCRIPT_ON_TRANSITION, GlimwoodTangle_Ballonlea_OnTransition\n'
               '\tmap_script MAP_SCRIPT_ON_FRAME_TABLE, GlimwoodTangle_Ballonlea_OnFrame\n\t.byte 0\n')
    P, X = S.P, S.T
    S.raw(f'''GlimwoodTangle_Ballonlea_OnTransition:
	call_if_set FLAG_GLIMWOOD_SCENE_PENDING, {P}SetScene
	goto_if_set FLAG_GLIMWOOD_XERNEAS_DONE, {P}StateEnd
	setmaplayoutindex LAYOUT_GLIMWOOD_TANGLE_BALLONLEA_DYING
	setweather WEATHER_SHADE
	savebgm MUS_RG_POKE_TOWER
{P}StateEnd:
	end

{P}SetScene:
	setvar VAR_TEMP_1, 1
	return

GlimwoodTangle_Ballonlea_OnFrame:
	map_script_2 VAR_TEMP_1, 1, {P}Scene
	.2byte 0

{P}Scene:
	lockall
	setvar VAR_TEMP_1, 0
	clearflag FLAG_GLIMWOOD_SCENE_PENDING
	delay 30
	playse SE_M_HEAL_BELL
	msgbox {X}Relit, MSGBOX_DEFAULT
	releaseall
	end

{P}Witch::
	lock
	faceplayer
	goto_if_set FLAG_SPACETIME_GLIMWOOD_DONE, {P}WitchDone
	goto_if_set FLAG_GLIMWOOD_XERNEAS_DONE, {P}WitchLight
	goto_if_set FLAG_GLIMWOOD_GANG_BOSS, {P}WitchGo
	msgbox {X}Witch, MSGBOX_DEFAULT
	release
	end

{P}WitchGo:
	msgbox {X}WitchGo, MSGBOX_DEFAULT
	release
	end

{P}WitchLight:
	msgbox {X}WitchLight, MSGBOX_DEFAULT
	release
	end

{P}WitchDone:
	msgbox {X}WitchDone, MSGBOX_DEFAULT
	release
	end

{P}Boss::
	lock
	faceplayer
	playmoncry SPECIES_GRIMMSNARL, CRY_MODE_ENCOUNTER
	msgbox {X}Boss, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_GRIMMSNARL, 67, ITEM_NONE, SPECIES_MORGREM, 66, ITEM_NONE
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, {P}BossGone
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, {P}BossGone
	release
	end

{P}BossGone::
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_BALLONLEA_BOSS_A
	removeobject LOCALID_BALLONLEA_BOSS_B
	setflag FLAG_GLIMWOOD_GANG_BOSS
	fadescreen FADE_FROM_BLACK
	msgbox {X}BossGone, MSGBOX_DEFAULT
	release
	end

{P}Xerneas::
	lock
	playmoncry SPECIES_XERNEAS, CRY_MODE_ENCOUNTER
	msgbox {X}Xerneas, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_XERNEAS, 70
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, {P}XerneasCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, {P}XerneasTree
	release
	end

{P}XerneasTree::
	msgbox {X}XerneasTree, MSGBOX_DEFAULT
	release
	end

{P}XerneasCaught::
	removeobject LOCALID_BALLONLEA_XERNEAS
	setflag FLAG_GLIMWOOD_XERNEAS_DONE
	setflag FLAG_GLIMWOOD_SCENE_PENDING
	playse SE_M_HEAL_BELL
	fadescreenspeed FADE_TO_WHITE, 8
	warpsilent MAP_GLIMWOOD_TANGLE_BALLONLEA, {B_XERNEAS[0]}, {B_XERNEAS[1] + 1}
	waitstate
	release
	end

{P}HouseDoor::
	msgbox {X}HouseDoor, MSGBOX_SIGN
	end

{P}WitchDoor::
	msgbox {X}WitchDoor, MSGBOX_SIGN
	end
''', [('Relit', "Light floods back into BALLONLEA. Every mushroom glows at once, like a village that just "
                    "remembered it left the oven on."),
          ('Witch', "You again! Pop quiz: who's blocking the stairs to XERNEAS? ...A GRIMMSNARL with a "
                    "fringe. Correct. Go and be rude to it."),
          ('WitchGo', "Stairs are free. XERNEAS sleeps in the fairy ring up top. Be gentle. And bring a ball. "
                      "Gentleness alone has never caught anything."),
          ('WitchLight', "Look at it glow! Pop quiz: what comes after life? ...Yes. Exactly. Something just "
                         "landed in the forest. Don't keep it waiting."),
          ('WitchDone', "XERNEAS and YVELTAL. You've got the whole circle of life in your bag, dearie. "
                        "Final quiz: who's cleaning up all these spores? ...Wrong. It's still you."),
          ('Boss', "GRIMMSNARL, the boss of the gang, sits on the stairs with its hair crossed. MORGREM holds "
                   "its coat. Nobody gets past without a fight. Or a very good bribe."),
          ('BossGone', "GRIMMSNARL storms off into the dark, taking its hair with it. The stairs to XERNEAS are "
                       "free."),
          ('Xerneas', "XERNEAS slumbers in the fairy ring, its antlers flickering like a lamp on its last bulb. "
                      "It opens one eye. Then the other. Then the antlers."),
          ('XerneasTree', "XERNEAS turns into a tree to rest. Give it a minute. ...It's back. Trees are "
                          "surprisingly fast at this."),
          ('HouseDoor', "The door is locked. A note: OUT. DO NOT LICK THE WALLS. THEY ARE LOAD-BEARING "
                        "MUSHROOM."),
          ('WitchDoor', "THE WITCH'S HOUSE. Visitors by appointment. Appointments by prophecy.")])
    nm = 'Arthur'
    S.trainer(nm, B_TRAINER[0], "I review the BALLONLEA STADIUM shows. One star. Every one. Let's see what "
                                "you're worth.",
              "Two stars. Don't let it go to your head.",
              "The play tonight is about a mushroom who becomes a stage. I've seen it. Twice. Unwillingly.")
    S.write()


# ====================================================================== kaarten wegschrijven
def maps():
    print('Glimwood Tangle:')
    F = forest_map()
    lay_f = F.save('GlimwoodTangle', 'gTileset_GlimwoodGeneral', 'gTileset_Glimwood')
    F.save('GlimwoodTangle_Dying', 'gTileset_GlimwoodGeneralDying', 'gTileset_GlimwoodDying', layout_dir='GlimwoodTangle')
    P = 'GlimwoodTangle_EventScript_'
    objs = [lid(bd.obj('OBJ_EVENT_GFX_EXPERT_F', F_WITCH[0], F_WITCH[1], P + 'Witch', move='MOVEMENT_TYPE_FACE_DOWN'),
                'LOCALID_GLIMWOOD_WITCH')]
    for key, gfx, x, y, face, sight, nm in F_TRAINERS:
        objs.append(bd.tr(gfx, x, y, P + nm, face, sight))
    gfx_g = {1: ['IMPIDIMP'], 2: ['MORGREM'], 3: ['MORGREM', 'MORGREM']}
    for g, cells in F_GANGS.items():
        for i, (x, y) in enumerate(cells):
            tag = 'GANG_%d' % g + ('' if len(cells) == 1 else 'AB'[i])
            objs.append(lid(bd.obj('OBJ_EVENT_GFX_SPECIES(%s)' % gfx_g[g][i], x, y, P + 'Gang%d' % g,
                                   'FLAG_GLIMWOOD_GANG_%d' % g, 'MOVEMENT_TYPE_LOOK_AROUND'), 'LOCALID_GLIMWOOD_' + tag))
    objs.append(lid(bd.obj('OBJ_EVENT_GFX_SPECIES(YVELTAL)', F_YVELTAL[0], F_YVELTAL[1], P + 'Yveltal', 'FLAG_TEMP_1',
                           'MOVEMENT_TYPE_FACE_DOWN'), 'LOCALID_GLIMWOOD_YVELTAL'))
    for x, y, it, fl in F_ITEMS:
        objs.append(bd.ball(x, y, it, fl))
    warps = [bd.warp(F_ENTRY[0], FH - 1, HUB_DEST[0], HUB_DEST[1]), bd.warp(F_ENTRY[1], FH - 1, HUB_DEST[0], HUB_DEST[1]),
             bd.warp(F_EXIT[0], 0, 'GLIMWOOD_TANGLE_BALLONLEA', 0), bd.warp(F_EXIT[1], 0, 'GLIMWOOD_TANGLE_BALLONLEA', 1)]
    bgs = [bd.hidden(x, y, it, fl) for x, y, it, fl in F_HIDDEN]
    write_map('GlimwoodTangle', lay_f, objs, warps, bgs)

    print('Ballonlea:')
    B = ballonlea_map()
    lay_b = B.save('GlimwoodTangle_Ballonlea', 'gTileset_GlimwoodGeneral', 'gTileset_Glimwood')
    B.save('GlimwoodTangle_Ballonlea_Dying', 'gTileset_GlimwoodGeneralDying', 'gTileset_GlimwoodDying',
           layout_dir='GlimwoodTangle_Ballonlea')
    P = 'GlimwoodTangle_Ballonlea_EventScript_'
    objs = [lid(bd.obj('OBJ_EVENT_GFX_EXPERT_F', B_WITCH[0], B_WITCH[1], P + 'Witch', move='MOVEMENT_TYPE_FACE_DOWN'),
                'LOCALID_BALLONLEA_WITCH')]
    key, gfx, x, y, face, sight, nm = B_TRAINER
    objs.append(bd.tr(gfx, x, y, P + nm, face, sight))
    for i, ((x, y), sp) in enumerate(zip(B_BOSS, ('GRIMMSNARL', 'MORGREM'))):
        objs.append(lid(bd.obj('OBJ_EVENT_GFX_SPECIES(%s)' % sp, x, y, P + 'Boss', 'FLAG_GLIMWOOD_GANG_BOSS',
                               'MOVEMENT_TYPE_FACE_DOWN'), 'LOCALID_BALLONLEA_BOSS_' + 'AB'[i]))
    objs.append(lid(bd.obj('OBJ_EVENT_GFX_SPECIES(XERNEAS)', B_XERNEAS[0], B_XERNEAS[1], P + 'Xerneas',
                           'FLAG_GLIMWOOD_XERNEAS_DONE', 'MOVEMENT_TYPE_FACE_DOWN'), 'LOCALID_BALLONLEA_XERNEAS'))
    for x, y, it, fl in B_ITEMS:
        objs.append(bd.ball(x, y, it, fl))
    warps = [bd.warp(B_ENTRY[0], BH - 1, 'GLIMWOOD_TANGLE', 2), bd.warp(B_ENTRY[1], BH - 1, 'GLIMWOOD_TANGLE', 3)]
    bgs = [bd.hidden(x, y, it, fl) for x, y, it, fl in B_HIDDEN]
    for i, (name, x, y) in enumerate(B_HOUSES):
        door = P + ('WitchDoor' if i == 0 else 'HouseDoor')
        bgs += [bd.sign(x + 1, y + 3, door, 'BG_EVENT_PLAYER_FACING_NORTH'),
                bd.sign(x + 2, y + 3, door, 'BG_EVENT_PLAYER_FACING_NORTH')]
    write_map('GlimwoodTangle_Ballonlea', lay_b, objs, warps, bgs, music='MUS_RG_CELADON',
              region_map_section='MAPSEC_BALLONLEA')
    return F, B


def check(F, B):
    probs = []
    gang = {p for v in F_GANGS.values() for p in v}
    objs = {F_WITCH, F_YVELTAL} | gang | {(x, y) for _, _, x, y, *_ in F_TRAINERS} | {(x, y) for x, y, *_ in F_ITEMS}
    start = (F_ENTRY[0], FH - 1)
    r = F.reach(start, objs - set(F_GANGS[3]))
    for p in objs:
        if not any((p[0] + dx, p[1] + dy) in r for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            probs.append(('bos: onbereikbaar', p))
    for x, y, *_ in F_HIDDEN:
        if (x, y) not in r:
            probs.append(('bos: verborgen item onbereikbaar', (x, y)))
    for x in F_EXIT:
        if (x, 0) not in r:
            probs.append(('bos: uitgang onbereikbaar', x))
    if any((x, 0) in F.reach(start, objs) for x in F_EXIT):
        probs.append(('bos: bende 3 blokkeert de weg niet', None))
    objs_b = {B_WITCH, B_XERNEAS, tuple(B_TRAINER[2:4])} | set(B_BOSS) | {(x, y) for x, y, *_ in B_ITEMS}
    sb = (B_ENTRY[0], BH - 1)
    rb = B.reach(sb, objs_b - set(B_BOSS))
    for p in objs_b:
        if not any((p[0] + dx, p[1] + dy) in rb for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            probs.append(('dorp: onbereikbaar', p))
    for x, y, *_ in B_HIDDEN:
        if (x, y) not in rb:
            probs.append(('dorp: verborgen item onbereikbaar', (x, y)))
    for _, x, y in B_HOUSES:
        if (x + 1, y + 4) not in rb:
            probs.append(('dorp: deur onbereikbaar', (x, y)))
    if any((B_XERNEAS[0] + dx, B_XERNEAS[1] + dy) in B.reach(sb, objs_b) for dx, dy in ((0, 1), (1, 0), (-1, 0))):
        probs.append(('dorp: de baas blokkeert de trap niet', None))
    if (B_XERNEAS[0], B_XERNEAS[1] + 1) not in rb:
        probs.append(('dorp: plek voor Xerneas onbereikbaar', None))
    for p in probs:
        print('PROBLEEM', p)
    assert not probs
    print('bos %d, dorp %d tegels bereikbaar' % (len(r), len(rb)))


def battle_setup():
    p = 'src/battle_setup.c'
    s = open(p).read()
    a = '    case SPECIES_ZERAORA: // Project Grounded: Chargestone Cave'
    if 'SPECIES_XERNEAS' not in s:
        assert a in s
        s = s.replace(a, '''    case SPECIES_XERNEAS: // Project Grounded: Glimwood Tangle (placeholder: Kanto-legendary-thema, bestaande transitie)
    case SPECIES_XERNEAS_ACTIVE:
        CreateBattleStartTask(B_TRANSITION_WHITE_BARS_FADE, MUS_RG_VS_LEGEND);
        break;
    case SPECIES_YVELTAL: // Project Grounded: Glimwood Tangle, leven en dood (placeholder: Kanto-legendary-thema)
        CreateBattleStartTask(B_TRANSITION_BLACKHOLE, MUS_RG_VS_LEGEND);
        break;
''' + a, 1)
    b = '    if (MetatileBehavior_IsTallGrass(tileBehavior))\n        return BATTLE_ENVIRONMENT_GRASS;\n'
    g = '    // Project Grounded: Glimwood Tangle (ondergronds vanwege de eigen verlichting, maar het is een bos)\n'
    if g not in s:
        assert s.count(b) == 1
        s = s.replace(b, b + g + '    if (gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_GLIMWOOD_TANGLE)\n'
                      '     && (gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_GLIMWOOD_TANGLE)\n'
                      '      || gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_GLIMWOOD_TANGLE_BALLONLEA)))\n'
                      '        return BATTLE_ENVIRONMENT_GRASS;\n', 1)
    open(p, 'w').write(s)


def render(F, B, outdir):
    sys.path.insert(0, HERE)
    import gridrender as gr
    os.makedirs(outdir, exist_ok=True)
    imgs = {}
    for m, nm in ((F, 'GlimwoodTangle'), (B, 'Ballonlea')):
        for prim, sec, st in (('glimwood_general', 'glimwood', 'licht'), ('glimwood_general_dying', 'glimwood_dying', 'stervend')):
            im = gr.render([[v for v in row] for row in m.M], prim, sec)
            im.save(os.path.join(outdir, '%s_%s.png' % (nm, st)))
            imgs[(nm, st)] = im
    # overzicht: dorp boven het bos (zoals in de game: uitgang bovenaan), beide toestanden naast elkaar
    w = max(F.W, B.W) * 16
    h = (F.H + B.H) * 16 + 16
    ov = Image.new('RGB', (2 * w + 32, h), (16, 12, 24))
    for k, st in enumerate(('stervend', 'licht')):
        ox = k * (w + 32)
        b, f = imgs[('Ballonlea', st)], imgs[('GlimwoodTangle', st)]
        ov.paste(b, (ox + (F_EXIT[0] - B_ENTRY[0]) * 16, 0))
        ov.paste(f, (ox, B.H * 16 + 16))
    ov.save(os.path.join(outdir, 'overzicht.png'))


def main():
    build_decor()
    for n in SMALLS:
        SMALL_IDS.add(NAMES[n])
    F, B = maps()
    save_tileset()
    register_tilesets()
    flags()
    mapsecs()
    bd.WILD = WILD
    bd.wild()
    trainers()
    battle_setup()
    forest_scripts()
    ballonlea_scripts()
    if len(sys.argv) > 1:
        render(F, B, sys.argv[1])
    check(F, B)
    print('tileset: %d metatiles, %d tiles' % (len(MT), len(tt.list) + 1))


if __name__ == '__main__':
    main()
