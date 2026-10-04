"""Project Grounded: tileset fortree_jungle voor Fortree Jungle (gebruikt door fortree_jungle.py).

Kopie van Fortree; alle nieuwe tiles en metatiles komen ACHTERAAN (vrije, lege tile-plekken en metatiles vanaf 0x318),
zodat Fortree City via de connection ongewijzigd getekend wordt. Vrije paletten van Fortree: 6, 7 en 12.
- palet 12: kopie van General-palet 2 met diepere, blauwgroene jungle-bomen + lianen en epifytenbloemen.
- palet 6: mangrove en wortelboog (Ekat99, ekat99_moeras.png), omgevallen bemoste stammen, varens, monstera,
  bananenplant, bosbodem.
- palet 7: tropische bloemen (hibiscus, heliconia, orchideeen, rode bloemetjes) en waterlelies.
Alles behalve de mangrove en de wortelboog (Ekat99) is hier getekend: procedureel of als ASCII-raster (MONSTERA,
BANANA, HELICONIA, BROMELIAD).

Gebruik: ts = JungleTileset(); ts.forest(mt, variant) ... ts.save(); of los: python3 jungle_tileset.py voorbeeld.png
(toont alle nieuwe metatiles vergroot)."""
import math, os, shutil, struct, sys
from PIL import Image

SRC, TS = 'data/tilesets/secondary/fortree', 'data/tilesets/secondary/fortree_jungle'
GEN = 'data/tilesets/primary/general'
EKAT = 'graphics/grounded/tilesets/ekat99_moeras.png'
P_TREE, P_JUNGLE, P_FLOWER = 12, 6, 7

# ---------------------------------------------------------------- paletten (GBA 5-bit, x8)
PAL12 = {  # General palet 2 als basis; 1-4 bomen, 5/7/9 liaan, 10-12 bloemen, 14 donkere mint
    1: (112, 216, 96), 2: (48, 168, 72), 3: (16, 112, 64), 4: (8, 64, 40),
    5: (72, 48, 32), 7: (128, 88, 48), 9: (152, 216, 64), 10: (232, 48, 56), 11: (248, 200, 56),
    12: (240, 112, 184), 14: (40, 144, 72),
}
PAL6 = [(0, 0, 0),
        (16, 56, 40), (32, 104, 56), (64, 152, 64), (120, 200, 80), (184, 232, 104),   # 1-5 bladgroen
        (48, 32, 24), (96, 64, 40), (144, 104, 64), (192, 160, 112),                   # 6-9 hout
        (72, 160, 120), (64, 104, 168),                                                  # 10 mintschaduw, 11 donker water
        (136, 64, 48), (224, 208, 168), (96, 120, 48), (160, 200, 72)]                 # 12 hartrood, 13 jaarring, 14-15 mos
PAL7 = [(0, 0, 0),
        (40, 32, 40), (24, 96, 48), (56, 152, 64), (128, 208, 88),                     # 1 omlijning, 2-4 blad
        (160, 24, 48), (232, 56, 56), (248, 144, 48), (248, 224, 80),                  # 5-8 rood/oranje/geel
        (248, 152, 200), (208, 72, 160), (96, 48, 160), (168, 104, 224), (216, 176, 248),  # 9-13 roze/paars
        (248, 248, 240), (56, 152, 112)]                                                # 14 wit, 15 mintschaduw


def q(c):
    return tuple((v // 8) * 8 for v in c)


def read_pal(path):
    lines = open(path).read().split('\n')[3:19]
    return [tuple(map(int, l.split())) for l in lines if l.strip()]


def write_pal(path, cols):
    with open(path, 'w', newline='\r\n') as fp:
        fp.write('JASC-PAL\n0100\n16\n')
        for c in cols:
            fp.write('%d %d %d\n' % q(c))


def png_tiles(path):
    im = Image.open(path)
    px = im.load()
    w = im.width // 8
    return [[[px[(t % w) * 8 + x, (t // w) * 8 + y] & 15 for x in range(8)] for y in range(8)]
            for t in range((im.width // 8) * (im.height // 8))], im.getpalette()


# ---------------------------------------------------------------- tekenen
class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.p = [[0] * w for _ in range(h)]

    def get(self, x, y):
        return self.p[y][x] if 0 <= x < self.w and 0 <= y < self.h else 0

    def set(self, x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < self.w and 0 <= y < self.h:
            self.p[y][x] = c

    def outline(self, c, only=None):
        """Omlijn alle gevulde pixels die aan leegte grenzen (alleen randpixels van de vulling zelf)."""
        edge = []
        for y in range(self.h):
            for x in range(self.w):
                if self.p[y][x] and (only is None or self.p[y][x] in only):
                    if any(not (0 <= x + dx < self.w and 0 <= y + dy < self.h) or not self.p[y + dy][x + dx]
                           for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                        edge.append((x, y))
        for x, y in edge:
            self.p[y][x] = c

    def paste(self, other, ox, oy):
        for y in range(other.h):
            for x in range(other.w):
                if other.p[y][x]:
                    self.set(ox + x, oy + y, other.p[y][x])


def grow(cv, c, only=None):
    """Omlijning buitenom: lege pixels naast de vulling krijgen kleur c."""
    add = []
    for y in range(cv.h):
        for x in range(cv.w):
            if not cv.p[y][x] and any(cv.get(x + dx, y + dy) and (only is None or cv.get(x + dx, y + dy) in only)
                                      for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                add.append((x, y))
    for x, y in add:
        cv.p[y][x] = c


def polyline(pts):
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(abs(x1 - x0), abs(y1 - y0))
        for i in range(n + (1 if (x1, y1) == pts[-1] else 0)):
            p = (round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n))
            if not out or out[-1] != p:
                out.append(p)
    return out


def frond(cv, pts, size=2, light=5, mid=4, rib=3):
    """Varenblad als visgraat langs een polylijn: middennerf met om de pixel een paar blaadjes."""
    line = polyline(pts)
    n = len(line)
    for i, (x, y) in enumerate(line):
        cv.set(x, y, rib)
        if i % 2 == 1 and i < n - 1:
            nx, ny = line[min(i + 1, n - 1)]
            px, py = line[i - 1]
            dx, dy = nx - px, ny - py
            ll = max(1, round(size * (1 - i / n) + 0.4))
            for side in (-1, 1):
                ox, oy = (-dy, dx) if side < 0 else (dy, -dx)
                ox, oy = (ox > 0) - (ox < 0), (oy > 0) - (oy < 0)
                for k in range(1, ll + 1):
                    if not cv.get(x + ox * k, y + oy * k):
                        cv.set(x + ox * k, y + oy * k, light if (oy < 0 or (oy == 0 and ox < 0)) else mid)


def fern(variant):
    cv = Canvas(16, 16)
    if variant == 0:
        fr = [[(7, 14), (5, 10), (3, 7), (1, 6)], [(8, 14), (10, 10), (12, 7), (14, 6)],
              [(7, 14), (6, 9), (5, 5), (4, 3)], [(8, 14), (9, 9), (10, 5), (11, 3)],
              [(7, 14), (4, 13), (1, 13)], [(8, 14), (11, 13), (14, 13)], [(8, 14), (8, 8), (7, 2)]]
    else:
        fr = [[(7, 14), (4, 11), (1, 10)], [(8, 14), (11, 11), (14, 10)], [(7, 14), (5, 8), (3, 4), (2, 3)],
              [(8, 14), (10, 8), (12, 4), (13, 3)], [(8, 14), (8, 7), (8, 2)]]
    for pts in fr:
        frond(cv, pts)
    grow(cv, 2)
    return cv


def ascii(rows, cmap):
    cv = Canvas(len(rows[0]), len(rows))
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            cv.p[y][x] = cmap.get(ch, 0)
    return cv


C6 = {'o': 1, 'd': 2, 'm': 3, 'l': 4, 'h': 5, 'b': 6, 'B': 7, 'w': 8, 's': 10}
C7 = {'o': 1, 'd': 2, 'm': 3, 'l': 4, 'R': 5, 'r': 6, 'y': 7, 'Y': 8, 'p': 9, 'P': 10, 'v': 11, 'V': 12,
      'L': 13, 'W': 14, 's': 15}

MONSTERA = [
    '................',
    '.....ooo...ooo..',
    '....ollmo.ohllo.',
    '...ohl.mmohl.mmo',
    '..ohlmm.dolmm.do',
    '..olm.mmdolm.mdo',
    '.ohlmm.ddoomdddo',
    '.olm.mddo.oooo..',
    '.oomddddooooo...',
    'ohlloooooohlllo.',
    'olm.mmolloml.mmo',
    'ohlmm.olm.mmd.do',
    '.olm.mdlmm.mdddo',
    '..oodddooddddoo.',
    '....oossbsooo...',
    '.....ss.b.......',
]

BANANA = [
    '................',
    '......oo........',
    '.....ohlo...oo..',
    '..oo.olmo..ohlo.',
    '.ohlooldmo.olmo.',
    '.olmlolmdooldmo.',
    'ohlmdoolmdoldmo.',
    'olmdo.olmdlmdo..',
    'olmd.ooolmmdooo.',
    'oldo.ohlolmdhllo',
    '.oo.ohlmmolmlmmo',
    '...ohlmmdolmdmdo',
    '..ohlmdoo.odo.do',
    '.ohlmdo.oBbooo.o',
    'ohlmdo..oBwbo...',
    'olmdo...oBwbo..o',
    'oddo.....owbo.od',
    '.oo......oBwbood',
    '.........oBwbdo.',
    '.........oBwbo..',
    '........omBwbo..',
    '........oBwbbo..',
    '........oBwbbo..',
    '........oBwwbo..',
    '.......oBwwbbo..',
    '.......oBwwbbo..',
    '......odBwwbbmo.',
    '.....odmBwwbbmdo',
    '.....odlBwwbbdmo',
    '......sooooooos.',
    '.......ssssss...',
    '................',
]


def monstera():
    return ascii(MONSTERA, C6)


def banana():
    return ascii(BANANA, C6)


def log(length):
    """Omgevallen bemoste stam, length vakken breed (2 of 3): rond geschaduwd, schorsstrepen, mosplakken
    bovenop en rechts het zaagvlak met jaarringen. Links afgebroken."""
    import random
    r = random.Random(length * 7 + 1)
    W = 16 * length
    cv = Canvas(W, 16)
    top, bot = 4, 13
    shade = {5: 9, 6: 9, 7: 8, 8: 8, 9: 8, 10: 7, 11: 7, 12: 7}
    darker = {9: 8, 8: 7, 7: 6, 6: 6}
    for x in range(1, W - 1):
        for y in range(top + 1, bot):
            cv.set(x, y, shade[y])
    for y in range(top + 2, bot - 1):          # schorsstrepen
        x = r.randrange(2, 6)
        while x < W - 6:
            ln = r.randrange(2, 5)
            for k in range(ln):
                cv.set(x + k, y, darker[shade[y]])
            x += ln + r.randrange(3, 8)
    x = 2                                       # mosplakken
    while x < W - 7:
        w = r.randrange(4, 8)
        for k in range(w):
            h = 2 + (1 if 0 < k < w - 1 else 0) + (1 if r.random() < 0.3 else 0)
            for y in range(top - 1, top - 1 + h):
                cv.set(x + k, y, 5 if y == top - 1 and k % 2 else 4 if y <= top else 3)
            if r.random() < 0.25:
                cv.set(x + k, top - 1 + h, 3)
        x += w + r.randrange(2, 6)
    ex = W - 4                                  # zaagvlak
    for y in range(top, bot + 1):
        for x in range(ex - 2, W):
            dy = (y - (top + bot) / 2) / ((bot - top) / 2 + 0.6)
            dx = (x - ex) / 2.4
            d = math.hypot(dx, dy)
            if d <= 1.0:
                cv.set(x, y, 7 if d > 0.82 else 13 if d > 0.6 else 9 if d > 0.38 else 13 if d > 0.15 else 12)
    for y in range(top + 1, bot):              # afgebroken linkerkant
        if y % 3 == 1:
            cv.set(1, y, 0)
        if y % 4 == 2:
            cv.set(2, y, 0)
    for y in range(top, bot + 1):
        for x in range(1, W - 1):
            if y in (top, bot) and cv.get(x, y) == 0 and cv.get(x, top + 1 if y == top else bot - 1) in (6, 7, 8, 9):
                cv.set(x, y, 6)
    grow(cv, 6, only=(6, 7, 8, 9, 12, 13))
    grow(cv, 1, only=(3, 4, 5))
    for x in range(3, W - 2):                   # schaduw op de grond
        for y in (bot + 1, bot + 2):
            if not cv.get(x, y) and (y == bot + 1 or 4 < x < W - 4):
                cv.set(x, y, 10)
    return cv


# ---- palet 7: bloemen
HELICONIA = [
    '................',
    '................',
    '................',
    '................',
    '.........oo.....',
    '........oYyo....',
    '.......orrYo....',
    '.......oRro.....',
    '...oo..oRo......',
    '..oYyo.oRo......',
    '..oYrroodo......',
    '...oRrrodo......',
    '....ooRodoo.....',
    '......odoYyo....',
    '......odorrYo...',
    '......odoRrro...',
    '..oo..odoRro....',
    '.oYyo.odooo.....',
    '.oYrroodo.......',
    '..oRrrodo..oo...',
    '...ooRodo.olmo..',
    '.oo..odo.olmmo..',
    'olmo.odoolmmdo..',
    'oldmoodolmmdo...',
    '.olmmodolmddo.oo',
    '.oldmmdolmdo.olo',
    '..oldmdmmddoolmo',
    '...oldmmmddolmdo',
    '....odmmmdddmdo.',
    '.....oddmdddoo..',
    '......ssooos....',
    '................',
]


def heliconia():
    return ascii(HELICONIA, C7)


def blossom(cv, cx, cy, petal, dark, heart):
    for y in range(cy - 4, cy + 5):
        for x in range(cx - 4, cx + 5):
            dx, dy = x - cx, y - cy
            d = math.hypot(dx, dy)
            a = math.atan2(dy, dx)
            r = 2.4 + 1.2 * abs(math.cos(2.5 * (a + 0.3)))
            if d <= r:
                cv.set(x, y, dark if d > r - 1.0 or d < 1.2 else petal)
    cv.set(cx, cy, heart); cv.set(cx + 1, cy - 1, heart); cv.set(cx + 2, cy - 2, heart)


def hibiscus(variant):
    """Hibiscusstruikje: bladeren met twee of drie grote bloemen (rood of roze)."""
    cv = Canvas(16, 16)
    for cx, cy, rx, ry in ((4, 10, 4, 3), (11, 10, 4, 3), (8, 7, 5, 4), (8, 12, 5, 3)):
        for y in range(16):
            for x in range(16):
                e = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if e <= 1:
                    cv.set(x, y, 4 if (x - cx) + (y - cy) * 1.5 < -2.5 else 3 if e < 0.75 else 2)
    if variant == 0:
        blossom(cv, 5, 6, 6, 5, 8); blossom(cv, 11, 10, 6, 5, 8)
    else:
        blossom(cv, 9, 5, 9, 10, 8); blossom(cv, 4, 11, 9, 10, 8)
    grow(cv, 1)
    for x in range(4, 12):
        if not cv.get(x, 15):
            cv.set(x, 15, 15)
    return cv


def groundflowers(variant):
    """Lage bloemetjes om doorheen te lopen (zoals de bloemen van General): paarse orchideeen of rood-gele."""
    cv = Canvas(16, 16)
    spots = [(4, 5), (11, 4), (7, 11), (13, 12)] if variant == 0 else [(3, 10), (9, 6), (12, 12)]
    for i, (cx, cy) in enumerate(spots):
        for dx, dy in ((-1, 1), (1, 2)):
            cv.set(cx + dx * 2, cy + dy, 3)
            cv.set(cx + dx * 2 + dx, cy + dy, 2)
        if variant == 0:
            for dx, dy, c in ((0, -1, 12), (-1, 0, 12), (1, 0, 12), (0, 1, 11), (0, 0, 14), (-1, -1, 13), (1, -1, 13)):
                cv.set(cx + dx, cy + dy, c)
        else:
            col, dark = ((6, 5), (7, 6), (6, 5))[i % 3]
            for dx, dy, c in ((0, -1, col), (-1, 0, col), (1, 0, col), (0, 1, col), (0, 0, 8)):
                cv.set(cx + dx, cy + dy, c)
            cv.set(cx + 1, cy + 1, dark)
    grow(cv, 1, only=(5, 6, 7, 8, 11, 12, 13, 14))
    return cv


def lotus(variant):
    """Waterlelieblad (en soms een roze bloem) op het water; doorzichtige achtergrond."""
    cv = Canvas(16, 16)
    pads = [(5, 10, 3.6), (11, 5, 2.8)] if variant == 0 else [(9, 9, 4.0)]
    for cx, cy, r in pads:
        for y in range(16):
            for x in range(16):
                d = math.hypot(x - cx, (y - cy) * 1.25)
                a = math.atan2(y - cy, x - cx)
                if d <= r and not (abs(a - 0.6) < 0.35 and d > 0.8):
                    cv.set(x, y, 4 if (x - cx) + (y - cy) < -1 else 3)
    cv.outline(2)
    if variant == 1:
        for dx, dy, c in ((0, -2, 9), (-1, -1, 9), (1, -1, 9), (-2, 0, 10), (2, 0, 10), (0, -1, 14), (-1, 0, 9),
                          (1, 0, 9), (0, 0, 8)):
            cv.set(9 + dx, 7 + dy, c)
    return cv


# ---- palet 12: lianen en epifyten op de jungle-bomen (in de boomtile gebakken)
LEAF_R = ['.99.', '9999', '.ee9', '..e.']      # liaanblad rechts van de stengel (9 licht, e = 14 schaduw)


def vine(cv, x, y0, y1, phase, tip=False):
    """Liaan: houtige stengel (7 met schaduw 5) met om de drie pixels een hartvormig blad links of rechts."""
    for y in range(y0, y1):
        xx = x + (1 if math.sin(y * 0.45 + phase) > 0.5 else 0)
        cv.set(xx, y, 7)
        cv.set(xx + 1, y, 5)
    for y in range(y0 + int(phase) % 4, y1 - 2, 4):
        xx = x + (1 if math.sin(y * 0.45 + phase) > 0.5 else 0)
        right = (y // 4 + int(phase)) % 2 == 0
        for j, row in enumerate(LEAF_R):
            for i, ch in enumerate(row):
                if ch != '.':
                    c = 9 if ch == '9' else 14
                    cv.set(xx + 2 + i if right else xx - 1 - i, y + j, c)
    if tip:
        for dx, dy, c in ((-1, 0, 9), (0, 0, 9), (1, 0, 9), (2, 0, 9), (-1, 1, 14), (0, 1, 9), (1, 1, 9),
                          (2, 1, 14), (0, 2, 14), (1, 2, 9), (0, 3, 9)):
            cv.set(x + dx, y1 + dy, c)


BROMELIAD = [
    '....r.....',
    '...rYr....',
    '..rrYrr...',
    '.9.rrr.9..',
    '9e9.r.9e9.',
    '.9e999e9..',
    '..9eee9...',
]


def bromeliad(cv, cx, cy, col):
    """Epifyt (bromelia) in de kruin: rozet van bladeren met een felle bloeiaar (rood of roze, geel hart)."""
    cmap = {'r': col, 'Y': 11, '9': 9, 'e': 14}
    for j, row in enumerate(BROMELIAD):
        for i, ch in enumerate(row):
            if ch in cmap:
                cv.set(cx - 4 + i, cy - 3 + j, cmap[ch])


def litter(variant):
    """Bosbodem: gevallen bladeren en mosplukjes (begaanbaar); geeft de mintgrond van Fortree een jungle-tint."""
    cv = Canvas(16, 16)
    spots = ([(3, 4, 'b'), (11, 2, 'm'), (8, 9, 'y'), (2, 12, 'm'), (13, 12, 'b')],
             [(5, 3, 'm'), (12, 7, 'y'), (3, 10, 'b'), (9, 13, 'm')],
             [(7, 5, 'b'), (2, 8, 'm'), (12, 11, 'b'), (6, 13, 'y')])[variant]
    for x, y, k in spots:
        if k == 'm':      # mosplukje
            for dx, dy, c in ((0, 0, 4), (1, 0, 3), (-1, 1, 3), (0, 1, 3), (1, 1, 2), (2, 1, 2)):
                cv.set(x + dx, y + dy, c)
        else:             # blad: bruin (b) of geel (y)
            c1, c2 = (8, 7) if k == 'b' else (9, 8)
            for dx, dy, c in ((0, 0, c1), (1, 0, c1), (2, 1, c2), (1, 1, c1), (0, 1, c2)):
                cv.set(x + dx, y + dy, c)
            cv.set(x + 3, y + 1, 6)
    return cv


# ---------------------------------------------------------------- Ekat99-mangrove
EKAT_MAP = {
    (40, 60, 42): 1, (64, 96, 67): 2, (82, 119, 96): 3, (107, 154, 125): 4,
    (54, 49, 44): 6, (104, 96, 88): 7, (136, 120, 104): 8, (160, 144, 120): 9, (96, 68, 64): 7,
    (120, 160, 104): 0, (122, 172, 130): 0, (140, 178, 131): 0, (149, 190, 157): 0, (110, 146, 100): 0,
    (96, 128, 88): 10,                                  # schaduw op gras -> donkere mint
    (96, 136, 136): 0, (72, 112, 112): 0, (80, 80, 80): 11,   # water -> doorzichtig, schaduw -> donker water
}


def ekat(box):
    im = Image.open(EKAT).convert('RGBA').crop(box)
    cv = Canvas(im.width, im.height)
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = im.getpixel((x, y))
            if a < 128:
                continue
            c = EKAT_MAP.get((r, g, b))
            if c is None:
                c = min(EKAT_MAP, key=lambda k: sum((k[i] - (r, g, b)[i]) ** 2 for i in range(3)))
                c = EKAT_MAP[c]
            cv.p[y][x] = c
    return cv


def mangrove(big, water):
    """Grote (3x3) of kleine (2x3) mangrove uit ekat99_moeras.png; wortels op gras of in het water."""
    if big:
        top = ekat((80, 32, 128, 64))
        rootrow = ekat((80, 192, 128, 208) if water else (80, 64, 128, 80))
    else:
        top = ekat((80, 80, 112, 112))
        rootrow = ekat((80, 208, 112, 224) if water else (80, 112, 112, 128))
    cv = Canvas(top.w, 48)
    cv.paste(top, 0, 0)
    cv.paste(rootrow, 0, 32)
    return cv


def root_arch(water):
    """Wortelboog (2x1) uit ekat99_moeras.png: een wortel die uit de grond (of het water) omhoog boogt."""
    return ekat((80, 224, 112, 240) if water else (80, 128, 112, 144))


# ---------------------------------------------------------------- tileset
class JungleTileset:
    def __init__(self):
        os.makedirs(TS + '/palettes', exist_ok=True)
        self.tiles, self.pngpal = png_tiles(SRC + '/tiles.png')
        self.tiles += [[[0] * 8 for _ in range(8)] for _ in range(512 - len(self.tiles))]
        self.gtiles, _ = png_tiles(GEN + '/tiles.png')
        self.gmts = open(GEN + '/metatiles.bin', 'rb').read()
        self.gattr = open(GEN + '/metatile_attributes.bin', 'rb').read()
        self.mts = bytearray(open(SRC + '/metatiles.bin', 'rb').read())
        self.attrs = bytearray(open(SRC + '/metatile_attributes.bin', 'rb').read())
        self.first = 512 + len(self.mts) // 16
        ref = set()
        for e in struct.unpack('<%dH' % (len(self.mts) // 2), self.mts):
            if e & 0x3FF >= 512:
                ref.add((e & 0x3FF) - 512)
        self.free = [t for t in range(1, 512) if t not in ref and not any(any(r) for r in self.tiles[t])]
        self.nfree = len(self.free)
        self.tidx = {}
        self.midx = {}
        self.pals = [read_pal('%s/palettes/%02d.pal' % (SRC, i)) for i in range(16)]
        p2 = read_pal(GEN + '/palettes/02.pal')
        self.pals[P_TREE] = [q(PAL12.get(i, p2[i])) for i in range(16)]
        self.pals[P_JUNGLE] = [q(c) for c in PAL6]
        self.pals[P_FLOWER] = [q(c) for c in PAL7]

    # -- tiles
    def tile(self, pix):
        """Voegt een 8x8-tile toe (ontdubbeld, ook gespiegeld); geeft tile-veld zonder palet terug."""
        t = tuple(tuple(r) for r in pix)
        if not any(any(r) for r in t):
            return 0                # lege tile: tile 0 van General is leeg
        for hf in (0, 1):
            for vf in (0, 1):
                v = tuple(tuple(r[::-1] if hf else r) for r in (t[::-1] if vf else t))
                if v in self.tidx:
                    return self.tidx[v] | (hf << 10) | (vf << 11)
        assert self.free, 'geen vrije tiles meer in fortree_jungle'
        slot = self.free.pop(0)
        self.tiles[slot] = [list(r) for r in t]
        self.tidx[t] = 512 + slot
        return 512 + slot

    def cut(self, cv, ox, oy, pal):
        """Vier tile-entries (linksboven, rechtsboven, linksonder, rechtsonder) uit een 16x16-vak van een canvas."""
        ent = []
        for k in range(4):
            x0, y0 = ox + (k % 2) * 8, oy + (k // 2) * 8
            pix = [[cv.get(x0 + x, y0 + y) for x in range(8)] for y in range(8)]
            t = self.tile(pix)
            ent.append(0 if t == 0 else t | (pal << 12))
        return ent

    # -- metatiles
    def base(self, mt):
        """(bottom-entries, top-entries, attr) van een bestaande metatile (General of Fortree)."""
        if mt < 512:
            ent = list(struct.unpack_from('<8H', self.gmts, mt * 16))
            at = struct.unpack_from('<H', self.gattr, mt * 2)[0]
        else:
            ent = list(struct.unpack_from('<8H', self.mts, (mt - 512) * 16))
            at = struct.unpack_from('<H', self.attrs, (mt - 512) * 2)[0]
        return ent[:4], ent[4:], at

    def metatile(self, bottom, top, attr):
        key = (tuple(bottom), tuple(top), attr)
        if key not in self.midx:
            self.mts += struct.pack('<8H', *(list(bottom) + list(top)))
            self.attrs += struct.pack('<H', attr)
            self.midx[key] = self.first + len(self.midx)
            assert self.midx[key] < 1024, 'te veel metatiles'
        return self.midx[key]

    def overlay(self, basemt, cv, ox, oy, pal, layer=None, behavior=None):
        """Nieuwe metatile: onderlaag van basemt, bovenlaag = 16x16-vak (ox, oy) van cv in palet pal.
        layer: None = zoals basemt, anders 0 (normaal, boven de speler) of 1 (covered, onder de speler)."""
        b, t, at = self.base(basemt)
        assert not any(t), ('basis heeft al een bovenlaag', hex(basemt))
        if layer is not None:
            at = (at & 0x0FFF) | (layer << 12)
        if behavior is not None:
            at = (at & 0xF000) | behavior
        return self.metatile(b, self.cut(cv, ox, oy, pal), at)

    TREE_TILES = (0x4, 0x14, 0x6, 0x7, 0x16, 0xE, 0x1E)

    def jungle_entries(self, ents):
        """Zet elke General-boomtile (palet 2) om naar een kopie in de secondary met het jungle-palet 12."""
        out = []
        for e in ents:
            ti, pn = e & 0x3FF, e >> 12
            if ti in self.TREE_TILES and pn == 2:
                t = self.tile(self.gtiles[ti])
                fl = ((e >> 10) & 3) ^ ((t >> 10) & 3)
                e = (t & 0x3FF) | (fl << 10) | (P_TREE << 12)
            out.append(e)
        return out

    def jungle(self, basemt):
        """Dezelfde metatile met jungle-groene bomen (ook palmkruinen die over bos liggen)."""
        b, t, at = self.base(basemt)
        return self.metatile(self.jungle_entries(b), self.jungle_entries(t), at)

    def recolor(self, basemt, pal=P_TREE, draw=None, layer=None):
        """Kopie van een General-boommetatile met de boomtiles in palet pal (jungle-groen); draw(canvas) mag lianen
        of bloemen op de 16x16 bovenlaag (of onderlaag bij een stam zonder bovenlaag) tekenen."""
        b, t, at = self.base(basemt)
        uses_top = any(t)
        ent = t if uses_top else b
        cv = Canvas(16, 16)
        for k, e in enumerate(ent):
            ti, hf, vf = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1
            src = self.gtiles[ti]
            for y in range(8):
                for x in range(8):
                    cv.p[(k // 2) * 8 + y][(k % 2) * 8 + x] = src[7 - y if vf else y][7 - x if hf else x]
        if draw:
            draw(cv)
        new = self.cut(cv, 0, 0, pal)
        if layer is not None:
            at = (at & 0x0FFF) | (layer << 12)
        return self.metatile(b, new, at) if uses_top else self.metatile(new, t, at)

    def save(self):
        w = 16
        out = Image.new('P', (128, 256), 0)
        out.putpalette(self.pngpal)
        for n, t in enumerate(self.tiles):
            for y in range(8):
                for x in range(8):
                    out.putpixel(((n % w) * 8 + x, (n // w) * 8 + y), t[y][x])
        out.save(TS + '/tiles.png')
        for i in range(16):
            write_pal('%s/palettes/%02d.pal' % (TS, i), self.pals[i])
        open(TS + '/metatiles.bin', 'wb').write(self.mts)
        open(TS + '/metatile_attributes.bin', 'wb').write(self.attrs)
        register()
        return self.nfree - len(self.free), len(self.midx)


def register():
    hdr = open('src/data/tilesets/headers.h').read()
    if 'gTileset_FortreeJungle' not in hdr:
        hdr += '''
const struct Tileset gTileset_FortreeJungle = // Project Grounded: Fortree Jungle, Fortree + tropische tiles achteraan, jungle_tileset.py
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_FortreeJungle,
    .palettes = gTilesetPalettes_FortreeJungle,
    .metatiles = gMetatiles_FortreeJungle,
    .metatileAttributes = gMetatileAttributes_FortreeJungle,
    .callback = InitTilesetAnim_Fortree,
};
'''
        open('src/data/tilesets/headers.h', 'w').write(hdr)
    gfx = open('src/data/tilesets/graphics.h').read()
    if 'gTilesetTiles_FortreeJungle' not in gfx:
        gfx += '\nconst u32 gTilesetTiles_FortreeJungle[] = INCBIN_U32("%s/tiles.4bpp.fastSmol");\n\n' % TS
        gfx += 'const u16 gTilesetPalettes_FortreeJungle[][16] =\n{\n'
        gfx += ''.join('    INCBIN_U16("%s/palettes/%02d.gbapal"),\n' % (TS, i) for i in range(16)) + '};\n'
        open('src/data/tilesets/graphics.h', 'w').write(gfx)
    mh = open('src/data/tilesets/metatiles.h').read()
    if 'gMetatiles_FortreeJungle' not in mh:
        mh += '\nconst u16 gMetatiles_FortreeJungle[] = INCBIN_U16("%s/metatiles.bin");\n' % TS
        mh += 'const u16 gMetatileAttributes_FortreeJungle[] = INCBIN_U16("%s/metatile_attributes.bin");\n' % TS
        open('src/data/tilesets/metatiles.h', 'w').write(mh)


def preview(path, scale=4):
    """Alle tekeningen naast elkaar op mintgras, vergroot (om te beoordelen vóór ze in de kaart gaan)."""
    ts = JungleTileset()
    grass = (164, 213, 197)
    items = [('fern0', fern(0), P_JUNGLE), ('fern1', fern(1), P_JUNGLE), ('monstera', monstera(), P_JUNGLE),
             ('banana', banana(), P_JUNGLE), ('log3', log(3), P_JUNGLE), ('log2', log(2), P_JUNGLE),
             ('arch', root_arch(False), P_JUNGLE), ('litter', litter(0), P_JUNGLE),
             ('hibiscus0', hibiscus(0), P_FLOWER), ('hibiscus1', hibiscus(1), P_FLOWER), ('heliconia', heliconia(), P_FLOWER),
             ('gflow0', groundflowers(0), P_FLOWER), ('gflow1', groundflowers(1), P_FLOWER), ('lotus0', lotus(0), P_FLOWER), ('lotus1', lotus(1), P_FLOWER),
             ('mangrove', mangrove(True, False), P_JUNGLE), ('mangrove_w', mangrove(True, True), P_JUNGLE),
             ('mangrove_s', mangrove(False, False), P_JUNGLE), ('mangrove_sw', mangrove(False, True), P_JUNGLE)]
    W = sum(cv.w + 4 for _, cv, _ in items)
    img = Image.new('RGB', (W, 52), grass)
    x = 0
    for name, cv, pal in items:
        bg = (115, 189, 246) if name.endswith('w') or name.startswith('lotus') else grass
        for y in range(cv.h):
            for xx in range(cv.w):
                c = cv.p[y][xx]
                img.putpixel((x + xx, y), ts.pals[pal][c] if c else bg)
        x += cv.w + 4
    img.resize((W * scale, 52 * scale), Image.NEAREST).save(path)


if __name__ == '__main__':
    preview(sys.argv[1] if len(sys.argv) > 1 else 'jungle_preview.png')
