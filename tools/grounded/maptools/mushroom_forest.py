"""Project Grounded: Toadstool Hollow, het verborgen paddenstoelenbos achter Petalburg Woods.

Bouwt (idempotent, vaste seed):
- Tileset data/tilesets/secondary/toadstool_hollow: eigen secondary.
  * donkere kopieen van de Hoenn-bosbomen/gras van General (zelfde tiles, palet 6 = donker blauwgroen General-palet 2);
  * getekende paddenstoelen (palet 7 rood/bruin/mos/schors, palet 8 paars/blauw gloeiend): kleine groepjes, mos,
    sporen, een omgevallen stam, een heksenkring (5x5), reuzenpaddenstoelen (rood 3x3, paars/blauw 2x2).
- Petalburg Woods: een verborgen doorgang in de oostrand (x 46-47, y 10). De boom is een kopie op de bovenlaag
  (je loopt erachter langs, onzichtbaar); (47,10) is een oostpijl-warp. Twee rode paddenstoeltjes in het gras
  ervoor als hint. Nieuwe tiles/metatiles achteraan Rustboro (die tileset gebruikt Petalburg Woods).
- Gen 3-stijl (v0.9.x): ronde lichtbanden van linksboven, omlijning in de donkerste tint, lamellen, slagschaduw
  rechtsonder en grassprieten over de voet. Bomen, kroontjes en reuzen op COVERED zodat de mist alles bedekt.
- ToadstoolHollow: kaart 44x40 (bos op een 2x2-raster, open plekken uit een grof ASCII-plan), bereikbaarheid.
- Registratie: layouts.json, map_groups.json (gMapGroup_Grounded), event_scripts.s, headers/graphics/metatiles.h.
map.json en scripts.inc van ToadstoolHollow staan met de hand in data/maps/ToadstoolHollow.

Gebruik: python3 tools/grounded/maptools/mushroom_forest.py"""
import math, os, random, shutil, struct
from collections import deque
from PIL import Image

SEED = 285  # nationaal dexnummer van Shroomish
TS = 'data/tilesets/secondary/toadstool_hollow'
GEN = 'data/tilesets/primary/general'
RUST = 'data/tilesets/secondary/rustboro'
RUST_MT, RUST_TILES = 350, 498          # originele omvang van Rustboro (alles daarna is van dit script)

# ================================================================ palettes
def jasc(path, cols):
    with open(path, 'w', newline='\r\n') as fp:
        fp.write('JASC-PAL\n0100\n16\n')
        for c in cols:
            fp.write('%d %d %d\n' % tuple(c))


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().split('\n')[3:19]]


g2 = read_pal(GEN + '/palettes/02.pal')
# donker, blauwgroen bos: rood/groen omlaag, blauw iets omhoog
DARK = [(int(r * 0.42), int(g * 0.55), min(255, int(b * 0.62 + 22))) for r, g, b in g2]
# Palet 7 (MUSH): rood, room (stippen/steel), bruin, grasschaduw/gras. Palet 8 (GLOW): paars, blauw, gloed, steel, gras.
MUSH = [(0, 0, 0),
        (74, 18, 44), (134, 34, 60), (186, 56, 66), (228, 108, 98),        # 1-4 rood: omlijning, donker, midden, licht
        (234, 226, 204), (192, 182, 166), (138, 130, 140),                 # 5-7 room: licht, midden, schaduw
        (60, 42, 56),                                                       # 8 bruine omlijning / lamellen
        (96, 62, 58), (140, 98, 72), (186, 144, 100),                       # 9-11 bruin: donker, midden, licht
        (12, 70, 74), (48, 108, 123), (68, 117, 144), (27, 99, 103)]        # 12 slagschaduw, 13-15 gras (= donker bos)
GLOW = [(0, 0, 0),
        (42, 20, 72), (88, 46, 142), (140, 86, 204), (198, 150, 242),      # 1-4 paars
        (18, 36, 88), (36, 84, 168), (66, 140, 222), (140, 212, 248),      # 5-8 blauw
        (232, 248, 255),                                                    # 9 gloed (wit)
        (204, 200, 224), (148, 144, 182), (70, 64, 104),                    # 10-12 steel: licht, midden, donker/omlijning
        (186, 250, 160),                                                    # 13 gloed (geelgroen)
        (12, 70, 74), (27, 99, 103)]                                        # 14 slagschaduw, 15 gras
P_DARK, P_MUSH, P_GLOW = 6, 7, 8



os.makedirs(TS + '/palettes', exist_ok=True)
for i in range(16):
    if i == P_DARK:
        jasc('%s/palettes/%02d.pal' % (TS, i), DARK)
    elif i == P_MUSH:
        jasc('%s/palettes/%02d.pal' % (TS, i), MUSH)
    elif i == P_GLOW:
        jasc('%s/palettes/%02d.pal' % (TS, i), GLOW)
    else:
        shutil.copy('%s/palettes/%02d.pal' % (RUST, i), '%s/palettes/%02d.pal' % (TS, i))


# ================================================================ tekenen (Gen 3-stijl)
class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.p = [[0] * w for _ in range(h)]

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.p[y][x] = c

    def get(self, x, y):
        return self.p[y][x] if 0 <= x < self.w and 0 <= y < self.h else 0

    def outline(self, col, skip=()):
        add = []
        for y in range(self.h):
            for x in range(self.w):
                if self.p[y][x]:
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    v = self.get(x + dx, y + dy)
                    if v and v != col and v not in skip:
                        add.append((x, y))
                        break
        for x, y in add:
            self.p[y][x] = col

    def paste(self, o):
        for y in range(self.h):
            for x in range(self.w):
                if o.p[y][x]:
                    self.p[y][x] = o.p[y][x]


# hoed: omlijning, donker, midden, licht; stip: licht, midden, schaduw; steel: licht, midden, schaduw, omlijning;
# lamellen: licht, donker; grond: slagschaduw, gras donker, gras, gras licht
KINDS = {
    'red':    dict(cap=(1, 2, 3, 4), spot=(5, 6, 7), stem=(5, 6, 7, 8), gill=(7, 8), ground=(12, 15, 13, 14)),
    'brown':  dict(cap=(8, 9, 10, 11), spot=(11, 10, 9), stem=(5, 6, 7, 8), gill=(7, 8), ground=(12, 15, 13, 14)),
    'tan':    dict(cap=(8, 7, 6, 5), spot=(5, 6, 7), stem=(6, 6, 7, 8), gill=(7, 8), ground=(12, 15, 13, 14)),
    'purple': dict(cap=(1, 2, 3, 4), spot=(9, 4, 3), stem=(10, 11, 12, 12), gill=(11, 12), ground=(14, 15, 15, 15)),
    'blue':   dict(cap=(5, 6, 7, 8), spot=(9, 8, 7), stem=(10, 11, 12, 12), gill=(11, 12), ground=(14, 15, 15, 15)),
}
LIGHT = (-0.55, -0.62, 0.56)        # licht van linksboven (en iets van voren)


def _light(nx, ny):
    nz = math.sqrt(max(0.0, 1 - nx * nx - ny * ny))
    ln = math.sqrt(sum(v * v for v in LIGHT))
    return (nx * LIGHT[0] + ny * LIGHT[1] + nz * LIGHT[2]) / ln


def mushroom(cv, cx, by, rx, ry, sw, sh, kind, spots=(), lip=1, gills=1, tufts=True, shadow=True, seed=0,
             ring=False, grain=False):
    """Paddenstoel met de voet op rij `by`, steel `sw` breed, hoed (koepel rx x ry) met de onderrand op by - sh.
    spots: (u, v, r) met u in [-1, 1] (links-rechts) en v in [-1, 0] (top-onderrand) van de koepel, r in pixels.
    Gen 3-stijl: licht van linksboven in ronde banden (hooglicht, licht, midden, donker), omlijning in de donkerste
    tint (aan de lichte kant de donkere tint), donkere lamellen onder de hoed, slagschaduw rechtsonder op de grond en
    grassprieten die over de voet vallen."""
    k = KINDS[kind]
    co, cd, cm, cl = k['cap']
    sl, sm, ss, so = k['stem']
    rnd = random.Random(seed)
    ccy = by - sh                                     # onderrand van de koepel
    t = Canvas(cv.w, cv.h)
    part = {}                                         # (x, y) -> 'cap' | 'stem' | 'gill'
    # --- slagschaduw op de grond (rechtsonder, licht komt van linksboven)
    if shadow:
        sx0, srx = cx + max(1.0, sw * 0.4), max(sw * 0.8 + 1.5, rx * 0.6)
        sry = max(1.3, srx * 0.26)
        for y in range(by - 3, by + 4):
            for x in range(int(cx - srx - 3), int(cx + srx + 4)):
                if ((x + 0.5 - sx0) / srx) ** 2 + ((y + 0.5 - by) / sry) ** 2 <= 1.0:
                    t.set(x, y, k['ground'][0])
    # --- steel (iets breder aan de voet)
    x0 = int(round(cx - sw / 2))
    top = ccy + lip
    for y in range(top, by + 1):
        flare = 0
        if sw >= 4 and y >= by - 2:
            flare = 1
        if sw >= 8 and y >= by:
            flare = 2
        for x in range(x0 - flare, x0 + sw + flare):
            part[(x, y)] = 'stem'
    fib = set()
    if grain:                                         # korte verticale vezelstreepjes
        for i in range(max(1, (by - top) * sw // 22)):
            fx_, fy_ = rnd.randrange(x0 + 2, x0 + sw - 1), rnd.randrange(top + 3, by - 1)
            for j in range(rnd.choice((2, 3, 3, 4))):
                fib.add((fx_, fy_ + j))
    for (x, y) in [p for p, v in part.items() if v == 'stem']:
        f = (x + 0.5 - x0) / max(1, sw)
        c = sl if f < 0.34 else (sm if f < 0.70 else ss)
        if sw <= 2:
            c = sl if x == x0 else ss
        if y < top + max(1, min(3, sh // 5)):
            c = ss if f < 0.70 else so                # schaduw van de hoed
        elif (x, y) in fib:
            c = ss                                    # vezels
        if ring and sw >= 6 and y in (top + 4, top + 5):
            c = sl if (y == top + 4 and f < 0.7) else ss
        t.set(x, y, c)
    if sw <= 2:                                       # dunne steel: omlijning rechts erbuiten
        for y in range(top, by + 1):
            part[(x0 + sw, y)] = 'stem'
            t.set(x0 + sw, y, so)
    if ring and sw >= 6:
        for x in (x0 - 1, x0 + sw):
            part[(x, top + 4)] = 'stem'
            t.set(x, top + 4, ss)
    # --- lamellen (onderkant van de hoed): donkere halve ellips met lijnen naar de steel
    if gills:
        for i in range(gills):
            y = ccy + lip + i
            hw = (rx - 1.0) * (1 - 0.22 * (i + 1)) if gills > 1 else rx - 1.5
            for x in range(int(math.floor(cx - hw)), int(math.ceil(cx + hw))):
                if part.get((x, y)) == 'stem':
                    continue
                part[(x, y)] = 'gill'
                lam = (x - int(cx)) % 2 == 0
                t.set(x, y, k['gill'][1] if (lam or i == gills - 1 or rx < 4) else k['gill'][0])
    # --- hoed
    capset = set()
    for y in range(int(math.floor(ccy - ry)) - 1, ccy + lip):
        for x in range(int(cx - rx) - 2, int(cx + rx) + 3):
            dx = (x + 0.5 - cx) / rx
            if y < ccy + 0.5:
                dy = (y + 0.5 - ccy) / ry
                if dx * dx + dy * dy <= 1.0:
                    capset.add((x, y))
            elif abs(dx) <= 1.0 - 0.08 * (y - ccy):   # omgekrulde rand
                capset.add((x, y))
    hx, hy = -0.32, -0.46                             # middelpunt van de lichtbanden (genormaliseerd)

    def band(x, y):
        dx = (x + 0.5 - cx) / rx
        dy = (y + 0.5 - ccy) / ry
        d = math.hypot(dx - hx, (dy - hy) * 1.05)
        if y > ccy:                                   # rand onder de middellijn
            return 2 if dx < -0.35 else 3
        th = (0.12, 0.42, 0.80) if rx >= 5 else (0.22, 0.62, 1.0)
        lvl = 0 if d < th[0] else (1 if d < th[1] else (2 if d < th[2] else 3))
        if dy > -0.12 and lvl < 2:                    # onderkant van de koepel ligt in de schaduw
            lvl += 1
        return lvl                                    # 0 hooglicht, 1 licht, 2 midden, 3 donker

    for (x, y) in capset:
        part[(x, y)] = 'cap'
        lvl = band(x, y)
        c = (cl, cl, cm, cd)[lvl]
        if lvl == 0 and rx >= 6 and k['spot'][0] and kind in ('red', 'purple', 'blue') and (x + y) % 2 == 0:
            c = cl
        t.set(x, y, c)
    # --- stippen (schaduwen mee met de hoed, verkort naar de rand toe)
    for (u, v, r) in spots:
        scx, scy = cx + u * rx * 0.96, ccy + v * ry
        fx = max(0.5, math.sqrt(max(0.0, 1 - u * u)))
        fy = max(0.45, math.sqrt(max(0.0, 1 - v * v))) * 0.78
        for y in range(int(scy - r) - 1, int(scy + r) + 2):
            for x in range(int(scx - r) - 1, int(scx + r) + 2):
                if (x, y) not in capset:
                    continue
                ddx, ddy = (x + 0.5 - scx) / (r * fx), (y + 0.5 - scy) / (r * fy)
                if ddx * ddx + ddy * ddy <= 1.15 or (r < 1.0 and x == int(scx) and y == int(scy)):
                    lvl = band(x, y)
                    sl_ = 0 if lvl <= 2 else 1
                    if r >= 1.4 and ddx * 0.5 + ddy * 0.85 > 0.55:    # onderrand van de stip
                        sl_ += 1
                    c = k['spot'][min(2, sl_)]
                    t.set(x, y, c)
    # --- omlijning (binnen het silhouet): donkerste tint, aan de lichte kant de donkere tint
    for (x, y), pt in list(part.items()):
        nb = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        out = [q for q in nb if q not in part]
        if pt == 'cap':
            if not out:
                continue
            dx = (x + 0.5 - cx) / rx
            dy = (y + 0.5 - ccy) / ry
            lit = dx < -0.1 and dy < -0.3 and all(q[0] <= x and q[1] <= y for q in out) and rx > 3
            t.set(x, y, cd if lit else co)
        elif pt == 'stem':
            if sw > 2 and any(q[0] != x for q in out):  # zijkanten
                t.set(x, y, so if (x >= cx or y < top + 2) else ss)
        elif pt == 'gill':
            if any(q[0] != x for q in out) or y == ccy + lip + gills - 1:
                t.set(x, y, co if kind in ('red', 'purple', 'blue') else k['gill'][1])
    # --- graspollen over de voet (donkere sprieten met lichte puntjes)
    if tufts:
        sd, gd, gm_, gl = k['ground']
        span = range(x0 - 2, x0 + sw + 2)
        for x in span:
            inner = x0 - 1 <= x <= x0 + sw
            hgt = rnd.choice((1, 2, 2, 3) if inner else (0, 1, 2, 2))
            if sw >= 6:
                edge = x <= x0 + 1 or x >= x0 + sw - 2
                hgt = rnd.choice((3, 4, 4, 5) if edge else (1, 2, 3, 3)) if inner else rnd.choice((1, 2, 3))
            for j in range(hgt):
                y = by + 1 - j
                c = sd if j == 0 else (gd if j < hgt - 1 else gl)
                t.set(x, y, c)
    cv.paste(t)


def spores(cv, pts, cols):
    for (x, y), c in zip(pts, cols):
        if not cv.get(x, y):
            cv.set(x, y, c)


# ---------------------------------------------------------------- kleine decor (16x16)
def small(kind):
    cv = Canvas(16, 16)
    if kind == 'red':
        mushroom(cv, 5.5, 13, 4.6, 3.6, 2, 4, 'red', [(-0.45, -0.55, 0.6), (0.3, -0.75, 0.6), (0.62, -0.25, 0.5)],
                 seed=1)
        mushroom(cv, 11.5, 14, 2.7, 2.2, 2, 3, 'red', [(-0.2, -0.6, 0.5)], seed=2)
    elif kind == 'brown':
        mushroom(cv, 10.5, 12, 3.8, 3.2, 2, 4, 'brown', seed=3)
        mushroom(cv, 4.5, 14, 3.0, 2.4, 2, 3, 'brown', seed=4)
        mushroom(cv, 13.5, 15, 2.2, 1.8, 1, 2, 'tan', gills=0, seed=5)
    elif kind == 'purple':
        mushroom(cv, 7.5, 13, 4.0, 3.4, 2, 5, 'purple', [(-0.4, -0.6, 0.6), (0.4, -0.5, 0.5)], seed=6)
        mushroom(cv, 12.5, 15, 2.2, 1.9, 1, 3, 'purple', gills=0, seed=7)
        spores(cv, [(2, 3), (13, 4), (10, 1), (3, 9), (14, 10)], [13, 9, 4, 13, 9])
    elif kind == 'blue':
        mushroom(cv, 3.5, 13, 2.4, 2.1, 1, 3, 'blue', gills=0, seed=8)
        mushroom(cv, 9.5, 14, 4.2, 3.2, 2, 4, 'blue', [(-0.4, -0.55, 0.6), (0.35, -0.7, 0.5)], seed=9)
        spores(cv, [(1, 4), (12, 2), (6, 1), (14, 8), (5, 7)], [9, 8, 13, 9, 13])
    return cv


def moss(seed):
    """Mospollen: ronde bultjes in de grastinten, licht linksboven, schaduw rechtsonder."""
    r = random.Random(seed)
    cv = Canvas(16, 16)
    blobs = [(r.uniform(4, 12), r.uniform(5, 12), r.uniform(1.8, 3.0)) for _ in range(3)]
    for cx, cy, rr in sorted(blobs, key=lambda b: b[1]):
        for y in range(16):                          # schaduw
            for x in range(16):
                if ((x + 0.5 - cx - 1) / (rr + 0.6)) ** 2 + ((y + 0.5 - cy - rr * 0.7) / (rr * 0.45 + 0.6)) ** 2 <= 1:
                    if not cv.get(x, y):
                        cv.set(x, y, 12)
        for y in range(16):
            for x in range(16):
                dx, dy = (x + 0.5 - cx) / rr, (y + 0.5 - cy) / (rr * 0.8)
                d = dx * dx + dy * dy
                if d <= 1.0:
                    I = _light(dx, min(0.0, dy) if dy < 0 else dy * 0.5)
                    c = 14 if I > 0.78 else (13 if I > 0.35 else 15)
                    if d > 0.72 and (dx > 0 or dy > 0):
                        c = 12
                    cv.set(x, y, c)
    for _ in range(5):                                # sprietjes
        x, y = r.randrange(2, 14), r.randrange(4, 14)
        if cv.get(x, y) in (13, 15):
            cv.set(x, y - 1, 14 if not cv.get(x, y - 1) else cv.get(x, y - 1))
    return cv


def glowdots():
    cv = Canvas(16, 16)
    for (x, y), c in zip([(3, 2), (11, 4), (6, 9), (13, 12), (1, 13), (9, 14), (8, 3)], [13, 9, 13, 13, 8, 9, 13]):
        cv.set(x, y, c)
    for (x, y) in [(6, 8), (6, 10), (5, 9), (7, 9)]:
        cv.set(x, y, 8)
    return cv


def log():
    """Omgevallen stam, 48x16: schors met licht van boven, mos, zaagvlak rechts, slagschaduw eronder."""
    r = random.Random(11)
    cv = Canvas(48, 16)
    y0, y1 = 4, 13                                    # boven- en onderkant van de stam
    for x in range(3, 47):                            # slagschaduw
        for y in (y1 + 1, y1 + 2):
            if not (y == y1 + 2 and (x < 6 or x > 44)):
                cv.set(x, y, 12)
    for x in range(1, 43):
        for y in range(y0, y1 + 1):
            f = (y - y0) / (y1 - y0)
            c = 11 if f < 0.22 else (10 if f < 0.6 else 9)
            if (x + y * 11) % 13 < 4 and 0.25 < f < 0.95 and y % 2 == 0:
                c = 9 if c == 10 else 8               # schorsgroeven (horizontaal)
            if f < 0.22 and (x * 3 + y) % 9 == 0:
                c = 10
            if y in (y0, y1) or x == 1:
                c = 8
            cv.set(x, y, c)
    for x in range(1, 43):                            # mos bovenop, hangt een beetje over de rand
        n = r.choice((0, 1, 1, 2, 2, 3))
        if 16 <= x <= 22 or x > 38:
            n = min(n, 1)
        for j in range(n):
            cv.set(x, y0 - 1 + j, 14 if j == 0 else (13 if j == 1 else 15))
        if n == 3 and r.random() < 0.5:
            cv.set(x, y0 + 2, 15)
    for y in range(y0, y1 + 1):                       # zaagvlak
        for x in range(40, 48):
            dx, dy = (x + 0.5 - 43.5) / 3.4, (y + 0.5 - (y0 + y1 + 1) / 2) / ((y1 - y0 + 1) / 2)
            d = dx * dx + dy * dy
            if d <= 1.0:
                c = 6 if d < 0.15 else (5 if d < 0.4 else (6 if d < 0.65 else 7))
                if d > 0.82:
                    c = 8
                elif dx > 0.2 and dy > 0.1 and c in (5, 6):
                    c = 7 if c == 6 else 6
                cv.set(x, y, c)
    mushroom(cv, 9.5, y0, 2.8, 2.2, 2, 3, 'brown', gills=0, tufts=False, shadow=False, seed=12)
    mushroom(cv, 13.5, y0, 2.2, 1.7, 1, 2, 'brown', gills=0, tufts=False, shadow=False, seed=13)
    mushroom(cv, 30.5, y0, 3.2, 2.6, 2, 3, 'red', [(-0.3, -0.6, 0.6)], gills=0, tufts=False, shadow=False, seed=14)
    for x in range(3, 47, 2):                         # gras tegen de onderkant
        h = r.choice((0, 1, 2))
        for j in range(h):
            cv.set(x, y1 + 2 - j, 15 if j == 0 else 13)
    return cv


def fairy_ring(seed):
    """Heksenkring 80x80 (5x5 metatiles): bleke/bruine paddenstoeltjes in een cirkel, daaronder een ring donker gras
    (de schimmel onder de grond)."""
    r = random.Random(seed)
    cv = Canvas(80, 80)
    for i in range(140):
        a = r.uniform(0, 2 * math.pi)
        rad = 30 + r.gauss(0, 1.6)
        x, y = int(40 + rad * math.cos(a)), int(42 + rad * math.sin(a) * 0.92)
        cv.set(x, y, 15 if r.random() < 0.7 else 12)
    n = 18
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n + r.uniform(-0.06, 0.06)
        rad = 29 + r.uniform(-1.5, 1.5)
        pts.append((40 + rad * math.cos(a), 42 + rad * math.sin(a) * 0.92, i))
    for cx, by, i in sorted(pts, key=lambda p: p[1]):
        kind = 'tan' if i % 3 else 'brown'
        big = r.random() < 0.4
        mushroom(cv, cx, int(by), 3.0 if big else 2.2, 2.4 if big else 1.8, 2 if big else 1, 3 if big else 2, kind,
                 gills=1 if big else 0, seed=100 + i)
    return cv


def giant_red():
    """Reuzenpaddenstoel 48x48 (3x3): rode hoed met roomwitte stippen op een dikke, vezelige steel met manchet."""
    cv = Canvas(48, 48)
    mushroom(cv, 24, 45, 22.4, 17.5, 12, 21, 'red',
             [(-0.62, -0.55, 2.6), (-0.10, -0.86, 2.4), (0.45, -0.62, 2.4), (0.80, -0.22, 1.8), (-0.88, -0.15, 1.5),
              (0.10, -0.30, 1.9), (-0.40, -0.18, 1.3), (0.48, -0.95, 1.2), (-0.58, -0.90, 1.0), (0.97, -0.55, 0.9)],
             lip=2, gills=3, seed=20, ring=True, grain=True)
    return cv


def giant_small(kind):
    """Reuzenpaddenstoel 32x32 (2x2), gloeiend paars of blauw."""
    cv = Canvas(32, 32)
    mushroom(cv, 16, 29, 14.4, 11.5, 8, 14, kind,
             [(-0.55, -0.5, 1.8), (0.15, -0.82, 1.6), (0.6, -0.35, 1.4), (-0.15, -0.2, 1.1), (-0.85, -0.12, 0.9)],
             lip=2, gills=2, seed=30 if kind == 'purple' else 31, grain=True)
    spores(cv, [(2, 4), (29, 6), (5, 22), (27, 24), (1, 14), (30, 15)],
           [13, 9, 9, 13, 13, 9] if kind == 'blue' else [9, 13, 4, 13, 9, 13])
    return cv


def pw_cue():
    """Hint in Petalburg Woods: twee rode paddenstoeltjes in General-palet 2 (rood 10/11, perzik 9, omlijning 8)."""
    cv = Canvas(16, 16)
    for cx, by, rx, ry, sh in ((5.5, 13, 3.4, 2.8, 3), (11.0, 15, 2.4, 2.0, 2)):
        ccy = by - sh
        for y in range(ccy, by + 1):
            cv.set(int(cx), y, 9)
        for y in range(int(ccy - ry) - 1, ccy + 1):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                dx, dy = (x + 0.5 - cx) / rx, (y + 0.5 - ccy) / ry
                if dy <= 0.2 and dx * dx + dy * dy <= 1.0:
                    cv.set(x, y, 10 if dx + dy < -0.5 else 11)
        cv.set(int(cx) - 1, ccy - 1, 9)
    cv.outline(8)
    return cv


# ================================================================ tiles verzamelen
def tile_of(cv, ox, oy):
    return tuple(cv.p[oy + y][ox + x] for y in range(8) for x in range(8))


def hflip(t):
    return tuple(t[y * 8 + 7 - x] for y in range(8) for x in range(8))


class Tiles:
    def __init__(self, base, first):
        self.base, self.list, self.idx = base, [], {}
        self.first = first

    def add(self, t, pal):
        if not any(t):
            return 0x0000
        if t in self.idx:
            return (pal << 12) | self.idx[t]
        if hflip(t) in self.idx:
            return (pal << 12) | 0x400 | self.idx[hflip(t)]
        n = self.base + self.first + len(self.list)
        self.idx[t] = n
        self.list.append(t)
        return (pal << 12) | n

    def cell(self, cv, cx, cy, pal):
        return [self.add(tile_of(cv, cx * 16 + (k % 2) * 8, cy * 16 + (k // 2) * 8), pal) for k in range(4)]


def save_tiles(path, src, tiles, first):
    if src:
        im = Image.open(src)
        out = Image.new('P', (128, 256), 0)
        out.putpalette(im.getpalette())
        out.paste(im.crop((0, 0, 128, (first + 15) // 16 * 8)), (0, 0))
        # rij waarin `first` valt: alles vanaf first leegmaken
        for n in range(first, ((first + 15) // 16) * 16):
            for p in range(64):
                out.putpixel(((n % 16) * 8 + p % 8, (n // 16) * 8 + p // 8), 0)
    else:
        out = Image.new('P', (128, 256), 0)
        out.putpalette([v for c in MUSH for v in c] + [0] * (768 - 48))
    for i, t in enumerate(tiles):
        n = first + i
        assert n < 512, 'te veel tiles'
        for p, v in enumerate(t):
            out.putpixel(((n % 16) * 8 + p % 8, (n // 16) * 8 + p // 8), v)
    out.save(path)


gm = open(GEN + '/metatiles.bin', 'rb').read()
ga = open(GEN + '/metatile_attributes.bin', 'rb').read()
gmt = lambda m: list(struct.unpack_from('<8H', gm, m * 16))
gat = lambda m: struct.unpack_from('<H', ga, m * 2)[0]
GRASS = [0x2002, 0x2003, 0x2003, 0x2002]
COVERED, NORMAL = 0x1000, 0x0000

# ---------------------------------------------------------------- Rustboro / Petalburg Woods
rm = bytearray(open(RUST + '/metatiles.bin', 'rb').read()[:RUST_MT * 16])
ra = bytearray(open(RUST + '/metatile_attributes.bin', 'rb').read()[:RUST_MT * 2])
gtiles = open(GEN + '/tiles.4bpp', 'rb').read() if os.path.exists(GEN + '/tiles.4bpp') else None
assert gtiles, 'eerst make (General tiles.4bpp nodig)'


def gtile(n):
    b = gtiles[n * 32:(n + 1) * 32]
    return [(b[i // 2] >> (4 * (i % 2))) & 15 for i in range(64)]


def merge(lo, hi, hfl_lo=False, hfl_hi=False):
    a, b = gtile(lo), gtile(hi)
    if hfl_lo:
        a = list(hflip(tuple(a)))
    if hfl_hi:
        b = list(hflip(tuple(b)))
    return tuple(bv if bv else av for av, bv in zip(a, b))


rt = Tiles(512, RUST_TILES)
# 1dc = 1a0 029 1a2 1a3 + kroon 0cc op kwart 3; 1dd = 029h 1a1 1a4 1a5 + kroon 0cd op kwart 2
m1dc, m1dd = gmt(0x1DC), gmt(0x1DD)
mA = [m1dc[0], m1dc[1], m1dc[2], rt.add(merge(0x1A3, 0x0CC), 2)]
mB = [m1dd[0], m1dd[1], rt.add(merge(0x1A4, 0x0CD), 2), m1dd[3]]
cue = pw_cue()
mCue = rt.cell(cue, 0, 0, 2)
PW_NEW = []
for upper, beh, layer in ((mA, 0x00, NORMAL), (mB, 0x00, NORMAL), (gmt(0x1D4)[:4], 0x00, NORMAL),
                          (gmt(0x1D5)[:4], 0x62, NORMAL), (mCue, 0x00, COVERED)):
    PW_NEW.append(0x200 + len(rm) // 16)
    rm += struct.pack('<8H', *GRASS, *upper)
    ra += struct.pack('<H', layer | beh)
assert len(rt.list) <= 512 - RUST_TILES
open(RUST + '/metatiles.bin', 'wb').write(rm)
open(RUST + '/metatile_attributes.bin', 'wb').write(ra)
save_tiles(RUST + '/tiles.png', RUST + '/tiles.png', rt.list, RUST_TILES)
PW_A, PW_B, PW_TOP_L, PW_WARP, PW_CUE = PW_NEW
print('Rustboro: metatiles', [hex(x) for x in PW_NEW], len(rt.list), 'nieuwe tiles')

W0, H0 = 48, 44
pwm = list(struct.unpack('<%dH' % (W0 * H0), open('data/layouts/PetalburgWoods/map.bin', 'rb').read()))
PWV = lambda x, y, mt, col, el: pwm.__setitem__(y * W0 + x, mt | (col << 10) | (el << 12))
PWV(46, 9, PW_A, 1, 0)
PWV(47, 9, PW_B, 1, 0)
PWV(46, 10, PW_TOP_L, 0, 3)        # doorloopbare boom (je verdwijnt erachter)
PWV(47, 10, PW_WARP, 0, 3)         # oostpijl-warp naar Toadstool Hollow
PWV(44, 11, PW_CUE, 0, 3)          # hint: twee rode paddenstoeltjes
PWV(43, 7, PW_CUE, 0, 3)
open('data/layouts/PetalburgWoods/map.bin', 'wb').write(struct.pack('<%dH' % (W0 * H0), *pwm))

# ================================================================ eigen tileset
tt = Tiles(512, 1)                 # tile 512 blijft leeg
MT, ATTR, NAMES = [], [], {}


def addmt(name, lower, upper, attr):
    NAMES[name] = 0x200 + len(MT)
    MT.append(list(lower) + list(upper))
    ATTR.append(attr)
    return NAMES[name]


def darken(e):
    return [(t & 0x0FFF) | (P_DARK << 12) if t & 0x3FF else t for t in e]


# Bomen op COVERED: hun bovenlaag komt op BG2 en de mist (sprites, prioriteit 2) bedekt dan ook de boomtoppen; op
# BG1 (NORMAL, zoals in vanilla) liggen ze boven de mist. Ook de kroontjes op begaanbare cellen (1c6/1c7/1ce/1cf):
# anders steken overal onbemiste boomtopjes uit de mist. Prijs: wie direct boven een boom staat, staat nu vóór het
# topje van de kruin in plaats van erachter (een paar pixels bij de voeten).
for g in (0x001, 0x00D, 0x1C6, 0x1C7, 0x1CE, 0x1CF, 0x1D4, 0x1D5, 0x1D6, 0x1D7, 0x1DC, 0x1DD, 0x1E4, 0x1E5, 0x1E6,
          0x1E7):
    e = darken(gmt(g))
    at = gat(g)
    if g >= 0x1C6:
        assert at & 0xF000 == NORMAL, hex(at)
        at = (at & 0x0FFF) | COVERED
    addmt('g%03x' % g, e[:4], e[4:], at)
DGRASS = darken(gmt(0x001))[:4]
addmt('warp_w', DGRASS, [0] * 4, 0x63)               # westpijl-warp terug naar Petalburg Woods


def deco(name, cv, pal, w=1, h=1, layer=COVERED, layers=None):
    for cy in range(h):
        for cx in range(w):
            lay = layers[cy] if layers else layer
            addmt('%s_%d_%d' % (name, cx, cy) if (w, h) != (1, 1) else name, DGRASS, tt.cell(cv, cx, cy, pal), lay)


deco('m_red', small('red'), P_MUSH)
deco('m_brown', small('brown'), P_MUSH)
deco('m_purple', small('purple'), P_GLOW)
deco('m_blue', small('blue'), P_GLOW)
deco('moss1', moss(1), P_MUSH)
deco('moss2', moss(7), P_MUSH)
deco('glow', glowdots(), P_GLOW)
deco('log', log(), P_MUSH, 3, 1)
deco('ring', fairy_ring(SEED), P_MUSH, 5, 5)
# Alles op COVERED (bovenlaag op BG2): de mistsprites (prioriteit 2) liggen dan ook over de hoeden.
deco('gred', giant_red(), P_MUSH, 3, 3)
deco('gpur', giant_small('purple'), P_GLOW, 2, 2)
deco('gblue', giant_small('blue'), P_GLOW, 2, 2)
print('eigen tileset:', len(MT), 'metatiles,', len(tt.list) + 1, 'tiles')
save_tiles(TS + '/tiles.png', None, tt.list, 1)
open(TS + '/metatiles.bin', 'wb').write(b''.join(struct.pack('<8H', *e) for e in MT))
open(TS + '/metatile_attributes.bin', 'wb').write(b''.join(struct.pack('<H', a) for a in ATTR))

hdr = open('src/data/tilesets/headers.h').read()
if 'gTileset_ToadstoolHollow' not in hdr:
    hdr += '''
const struct Tileset gTileset_ToadstoolHollow = // Project Grounded: Toadstool Hollow (paddenstoelenbos), mushroom_forest.py
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_ToadstoolHollow,
    .palettes = gTilesetPalettes_ToadstoolHollow,
    .metatiles = gMetatiles_ToadstoolHollow,
    .metatileAttributes = gMetatileAttributes_ToadstoolHollow,
    .callback = NULL,
};
'''
    open('src/data/tilesets/headers.h', 'w').write(hdr)
gfx = open('src/data/tilesets/graphics.h').read()
if 'gTilesetTiles_ToadstoolHollow' not in gfx:
    gfx += '\nconst u32 gTilesetTiles_ToadstoolHollow[] = INCBIN_U32("%s/tiles.4bpp.fastSmol");\n\n' % TS
    gfx += 'const u16 gTilesetPalettes_ToadstoolHollow[][16] =\n{\n'
    gfx += ''.join('    INCBIN_U16("%s/palettes/%02d.gbapal"),\n' % (TS, i) for i in range(16)) + '};\n'
    open('src/data/tilesets/graphics.h', 'w').write(gfx)
mh = open('src/data/tilesets/metatiles.h').read()
if 'gMetatiles_ToadstoolHollow' not in mh:
    mh += '\nconst u16 gMetatiles_ToadstoolHollow[] = INCBIN_U16("%s/metatiles.bin");\n' % TS
    mh += 'const u16 gMetatileAttributes_ToadstoolHollow[] = INCBIN_U16("%s/metatile_attributes.bin");\n' % TS
    open('src/data/tilesets/metatiles.h', 'w').write(mh)

# ================================================================ kaart
# Grof plan, 22x20; elk teken = 2x2 metatiles. '#' bos, '.' open, 'E' ingang (west).
PLAN = '''
######################
####....#######...####
###......#####.....###
###.......###......###
###...##.........#..##
####....##.......#..##
#####...##...##.....##
####...###...##....###
###...###.....#......#
##...###.............#
E...........#........#
##..##...#...........#
###.....###.##.....###
####..#..#...##..#####
###..###.......#######
###.####........######
##....##...##.....####
##.##.....###.....####
###.......####....####
######################
'''.strip('\n').split('\n')
CW, CH = 22, 20
assert len(PLAN) == CH and all(len(r) == CW for r in PLAN), [len(r) for r in PLAN]
W, H = CW * 2, CH * 2
rng = random.Random(SEED)
openc = {(x, y) for y in range(H) for x in range(W) if PLAN[y // 2][x // 2] != '#'}
m = [[None] * W for _ in range(H)]      # (metatile, collision)
for (x, y) in openc:
    m[y][x] = (NAMES['g001'], 0)

# bomen op het 2x2-raster
istree = lambda cx, cy: not (0 <= cx < CW and 0 <= cy < CH) or PLAN[cy][cx] == '#'
for cy in range(CH):
    for cx in range(CW):
        if not istree(cx, cy):
            continue
        L, R, B = istree(cx - 1, cy), istree(cx + 1, cy), istree(cx, cy + 1)
        x, y = cx * 2, cy * 2
        m[y][x] = (NAMES['g1d4' if L else 'g1d6'], 1)
        m[y][x + 1] = (NAMES['g1d5' if R else 'g1d7'], 1)
        if B:
            m[y + 1][x] = (NAMES['g1dc'], 1); m[y + 1][x + 1] = (NAMES['g1dd'], 1)
        else:
            m[y + 1][x] = (NAMES['g1e4' if L else 'g1e6'], 1); m[y + 1][x + 1] = (NAMES['g1e5' if R else 'g1e7'], 1)

# vrij te houden: events, ingang, en het hoofdpad
EVENTS = {
    'warp0': (0, 20), 'warp1': (0, 21),
    'bug': (12, 21), 'aroma': (32, 21), 'hiker': (33, 35),
    'ball_tiny': (8, 3), 'ball_big': (36, 5), 'ball_tm': (4, 35),
    'hid_balm': (35, 18), 'hid_tiny': (11, 15),
}
KEEP = {v for k, v in EVENTS.items() if not k.startswith('hid')}
RING = (33, 16)                      # linkerbovenhoek van de heksenkring (5x5), midden = hid_balm
GIANTS_RED = [(12, 2), (22, 12)]     # 3x3 linkerbovenhoek
GIANTS_SMALL = [('gpur', 8, 24), ('gblue', 36, 12), ('gpur', 20, 32), ('gblue', 30, 24)]
LOGS = [(9, 15), (24, 28), (30, 7)]  # 3x1


def free(x, y, w, h):
    return all((x + dx, y + dy) in openc and m[y + dy][x + dx][0] == NAMES['g001'] and (x + dx, y + dy) not in KEEP
               for dx in range(w) for dy in range(h))


placed = set()
BAD = []


def stamp(name, x, y, w, h, solid):
    if not free(x, y, w, h):
        BAD.append((name, x, y))
        return
    for dy in range(h):
        for dx in range(w):
            key = '%s_%d_%d' % (name, dx, dy) if (w, h) != (1, 1) else name
            m[y + dy][x + dx] = (NAMES[key], 1 if solid(dx, dy) else 0)
            placed.add((x + dx, y + dy))


stamp('ring', RING[0], RING[1], 5, 5, lambda dx, dy: False)
for x, y in GIANTS_RED:
    stamp('gred', x, y, 3, 3, lambda dx, dy: dy < 2 or dx == 1)
for name, x, y in GIANTS_SMALL:
    stamp(name, x, y, 2, 2, lambda dx, dy: True)
for x, y in LOGS:
    stamp('log', x, y, 3, 1, lambda dx, dy: True)

if BAD: print("FOUT", BAD)
# hoog gras: een paar vlekken buiten het hoofdpad
PATCHES = [(6, 6, 3.2, 2.2), (16, 3, 3.0, 1.6), (36, 15, 3.4, 2.6), (12, 24, 3.0, 2.4), (8, 31, 3.6, 2.0),
           (30, 28, 3.0, 2.0), (26, 7, 3.0, 2.0), (40, 18, 1.6, 3.0), (17, 15, 2.4, 1.8), (32, 35, 2.6, 1.4)]
for px, py, rx, ry in PATCHES:
    for y in range(H):
        for x in range(W):
            if ((x - px) / rx) ** 2 + ((y - py) / ry) ** 2 <= 1 + rng.uniform(-0.25, 0.25) and free(x, y, 1, 1) \
                    and (x, y) not in placed and abs(y - 20.5) > 1.5:
                m[y][x] = (NAMES['g00d'], 0)

# losse decoratie op gras
DECOR = ['m_red'] * 7 + ['m_brown'] * 9 + ['m_purple'] * 7 + ['m_blue'] * 6 + ['moss1'] * 12 + ['moss2'] * 12 + ['glow'] * 10
cells = sorted((x, y) for (x, y) in openc if free(x, y, 1, 1) and (x, y) not in placed and abs(y - 20.5) > 0.6)
rng.shuffle(cells)
used = set()
k = 0
for (x, y) in cells:
    if k >= len(DECOR):
        break
    if any((x + a, y + b) in used for a in (-1, 0, 1) for b in (-1, 0, 1)):
        continue
    m[y][x] = (NAMES[DECOR[k]], 0)
    used.add((x, y))
    k += 1

# kroontjes: open cel direct boven een boomtop
for y in range(1, H):
    for x in range(W):
        mt = m[y][x][0]
        if mt in (NAMES['g1d4'], NAMES['g1d6'], NAMES['g1d5'], NAMES['g1d7']) and m[y - 1][x][1] == 0:
            left = mt in (NAMES['g1d4'], NAMES['g1d6'])
            above = m[y - 1][x][0]
            if above == NAMES['g001']:
                m[y - 1][x] = (NAMES['g1ce' if left else 'g1cf'], 0)
            elif above == NAMES['g00d']:
                m[y - 1][x] = (NAMES['g1c6' if left else 'g1c7'], 0)

# ingang: westpijl-warps op x=0
for (x, y) in (EVENTS['warp0'], EVENTS['warp1']):
    m[y][x] = (NAMES['warp_w'], 0)

os.makedirs('data/layouts/ToadstoolHollow', exist_ok=True)
open('data/layouts/ToadstoolHollow/map.bin', 'wb').write(
    b''.join(struct.pack('<H', mt | (col << 10) | ((0 if col else 3) << 12)) for row in m for mt, col in row))
open('data/layouts/ToadstoolHollow/border.bin', 'wb').write(
    struct.pack('<4H', *[NAMES[k] | (1 << 10) for k in ('g1d4', 'g1d5', 'g1dc', 'g1dd')]))

# bereikbaarheid vanaf de ingang
seen, q = {EVENTS['warp0']}, deque([EVENTS['warp0']])
while q:
    x, y = q.popleft()
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in seen and m[ny][nx][1] == 0:
            seen.add((nx, ny)); q.append((nx, ny))
for name, (x, y) in EVENTS.items():
    if name.startswith('hid'):
        continue
    assert (x, y) in seen, ('onbereikbaar', name)
    # een object moet ook van minstens een kant aanspreekbaar zijn
    assert any((x + dx, y + dy) in seen for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))), name
cx, cy = EVENTS['hid_balm']
assert (cx, cy) in seen
print('bereikbaar:', len(seen), 'van', sum(1 for r in m for c in r if c[1] == 0), 'open cellen')

lj = open('data/layouts/layouts.json').read()
if '"LAYOUT_TOADSTOOL_HOLLOW"' not in lj:
    i = lj.rindex('    }\n  ]')
    j = i + len('    }')
    lj = lj[:j] + ''',
    {
      "id": "LAYOUT_TOADSTOOL_HOLLOW",
      "name": "ToadstoolHollow_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_General",
      "secondary_tileset": "gTileset_ToadstoolHollow",
      "border_filepath": "data/layouts/ToadstoolHollow/border.bin",
      "blockdata_filepath": "data/layouts/ToadstoolHollow/map.bin"
    }''' % (W, H) + lj[j:]
    open('data/layouts/layouts.json', 'w').write(lj)

g = open('data/maps/map_groups.json').read()
if '"ToadstoolHollow"' not in g:
    i = g.index('"gMapGroup_Grounded": [')
    j = g.index('\n  ]', i)
    g = g[:j] + ',\n    "ToadstoolHollow"' + g[j:]
    open('data/maps/map_groups.json', 'w').write(g)
es = open('data/event_scripts.s').read()
inc = '\t.include "data/maps/ToadstoolHollow/scripts.inc"\n'
if inc not in es:
    anchor = '\t.include "data/maps/FortreeJungle/scripts.inc"\n'
    assert anchor in es
    es = es.replace(anchor, anchor + inc, 1)
    open('data/event_scripts.s', 'w').write(es)
print('klaar', W, 'x', H)
