#!/usr/bin/env python3
"""Concept-tileset La Paz (startstad, Fully Ungrounded): secondary bij de General-primary.

Gebruik (vanuit de repo-root):  python3 tools/concept/tiles/la_paz_tiles.py
Uitvoer: tilesets/eigen/la_paz/ (tiles.png, palettes/, metatiles.bin, metatile_attributes.bin,
metatile_names.json, sheet.png, tiles_sheet.png, paletten.png, mockup.png, mockup_2x.png, vergelijking.png).

Alles is getekend met vaste paletten (6..12) en een vaste seed, dus reproduceerbaar.
Hergebruik: kabelbaanstation = Ekat99 'Cable Car' (omgekleurd), marktkraam = Slateport-tent (Game Freak, omgekleurd).
"""
import os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
from tilelib import Canvas, Tileset, T, ellipse_mask, palette_strip, render_repo_map, side_by_side, repo_top_layer, Prim

OUT = 'tilesets/eigen/la_paz'
random.seed(1825)  # onafhankelijkheid van Bolivia

# ------------------------------------------------------------------ paletten (6..12)
# 6 straat: kasseien, trappen, kleihellingen, onkruid
OL6 = (56, 48, 56)
CB = [(104, 96, 104), (144, 136, 144), (184, 176, 176), (216, 208, 200), (240, 232, 224)]
CL = [(120, 64, 48), (168, 104, 72), (208, 144, 96), (232, 184, 128)]
GR = [(80, 128, 64), (128, 176, 80)]
YL6 = (232, 192, 72)
RT6 = (184, 80, 64)
P6 = [OL6] + CB + CL + GR + [YL6, RT6]


# 7/8/9 gebouwen: zelfde indexvolgorde, andere muur- en dakkleur (muur 4, dak 3, beton 4, glas 3)
def bld(wall, roof):
    return [(48, 32, 40)] + wall + roof + [(96, 96, 104), (152, 152, 152), (200, 200, 192), (232, 232, 224)] + \
        [(40, 56, 88), (88, 136, 184), (176, 216, 240)]


P7 = bld([(136, 56, 40), (184, 88, 56), (216, 120, 72), (232, 184, 144)],        # rode baksteen
         [(88, 104, 128), (136, 152, 168), (184, 200, 208)])                     # zink
P8 = bld([(176, 120, 56), (216, 168, 88), (240, 208, 128), (248, 232, 184)],     # oker/geel gepleisterd
         [(128, 64, 40), (176, 104, 56), (216, 152, 88)])                        # roestig
P9 = bld([(72, 112, 160), (112, 160, 200), (152, 192, 224), (208, 232, 240)],    # lichtblauw
         [(144, 40, 48), (200, 72, 64), (232, 120, 96)])                         # rood plaatijzer
OLB, W, R, K, G = P7[0], P7[1:5], P7[5:8], P7[8:12], P7[12:15]
# 10 cholet
OLC = (40, 32, 48)
WHC = (248, 248, 248)
MG = [(40, 80, 128), (64, 144, 192), (160, 224, 248)]
PK = [(184, 40, 112), (240, 120, 184)]
YEC, ORC, LIC = (248, 208, 56), (240, 128, 40), (136, 208, 72)
PU = [(104, 56, 152), (168, 120, 216)]
RDC, GDC, GYC = (208, 48, 56), (192, 144, 40), (160, 160, 168)
P10 = [OLC, WHC] + MG + PK + [YEC, ORC, LIC] + PU + [RDC, GDC, GYC]
# 11 kabelbaan en markt
OLT = (32, 32, 48)
ST = [(80, 88, 104), (136, 144, 160), (192, 200, 216)]
WHT = (240, 240, 248)
RD = [(168, 40, 48), (232, 88, 72)]
YE = [(208, 152, 24), (248, 216, 72)]
GN = [(40, 128, 72), (96, 184, 88)]
BL = [(80, 112, 176), (120, 152, 240), (184, 192, 240)]
WD = (128, 96, 64)
P11 = [OLT] + ST + [WHT] + RD + YE + GN + BL + [WD]
# 12 natuur en bergen (Illimani, eucalyptus, bloemen)
OLN = (40, 40, 64)
SN = [(248, 248, 248), (208, 224, 240), (152, 176, 216)]
RK = [(72, 64, 96), (112, 104, 136), (160, 152, 176)]
TG = [(40, 88, 64), (72, 136, 88), (128, 184, 104)]
TRN = (112, 72, 48)
FLR, FLY = (232, 88, 96), (248, 216, 88)
EU = (152, 184, 168)  # blauwgroen eucalyptusblad (licht)
P12 = [OLN] + SN + RK + TG + [TRN, FLR, FLY, EU]

ts = Tileset([P6, P7, P8, P9, P10, P11, P12])


def ascii_canvas(rows, cmap):
    c = Canvas(len(rows[0]), len(rows))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in cmap and cmap[ch] is not None:
                c.px(x, y, cmap[ch])
    return c


# ------------------------------------------------------------------ grond
def cobble(var=0):
    """Kasseien (adoquines) 7x3 met 1 px voeg, rijen verspringen 4 px; periode 16."""
    c = Canvas(16, 16, CB[1])
    rnd = random.Random(10 + var)
    for row in range(4):
        y0 = row * 4
        off = 4 if row % 2 else 0
        for k in range(3):
            x0 = k * 8 - off
            base = CB[3] if rnd.random() > (0.25 + 0.15 * var) else CB[2]
            for dy in range(3):
                for dx in range(7):
                    x = (x0 + dx) % 16
                    if (dx in (0, 6)) and dy in (0, 2):
                        continue  # afgeronde hoeken
                    col = base
                    if dy == 0 and dx < 5:
                        col = CB[4] if base == CB[3] else CB[3]
                    if dy == 2 and dx > 1:
                        col = CB[2] if base == CB[3] else CB[1]
                    c.px(x, y0 + dy, col)
    if var == 2:  # onkruid in de voegen
        for x, y in [(3, 7), (4, 7), (12, 15), (11, 15), (12, 14)]:
            c.px(x, y, GR[0])
        c.px(4, 6, GR[1]); c.px(12, 13, GR[1])
    return c


def sidewalk():
    c = Canvas(16, 16, CB[3])
    for y in range(16):
        for x in range(16):
            if x % 8 == 7 or y % 8 == 7:
                c.px(x, y, CB[2])
            elif x % 8 == 0 or y % 8 == 0:
                c.px(x, y, CB[4])
    return c


def plaza():
    """Plaza-tegels: rood-wit ruitpatroon."""
    c = Canvas(16, 16, CB[4])
    for y in range(16):
        for x in range(16):
            d = abs((x % 16) - 7.5) + abs((y % 16) - 7.5)
            if d < 5:
                c.px(x, y, RT6)
            elif d < 6:
                c.px(x, y, CB[2])
            if x == 0 or y == 0:
                c.px(x, y, CB[3])
    return c


def clay(var=0):
    """Kale kleigrond van de hellingen (La Paz-kom)."""
    c = Canvas(16, 16, CL[2])
    rnd = random.Random(30 + var)
    for _ in range(5 + var * 2):
        x, y = rnd.randrange(16), rnd.randrange(16)
        c.px(x, y, CL[1]); c.px(x + 1, y, CL[3])
    if var == 2:
        for x, y in [(4, 10), (5, 9), (6, 10), (11, 4), (12, 3)]:
            c.px(x, y, GR[0])
        c.px(5, 8, GR[1]); c.px(12, 2, GR[1])
    return c


def curb(side):
    """Stoeprand: stoep (boven) -> straat (onder) enz. side = n/s/w/e: waar de straat ligt."""
    c = Canvas(16, 16)
    sw, cb = sidewalk(), cobble()
    for y in range(16):
        for x in range(16):
            d = {'s': y, 'n': 15 - y, 'e': x, 'w': 15 - x}[side]
            src = sw if d < 11 else cb
            c.px(x, y, src.get(x, y))
            if d == 11:
                c.px(x, y, CB[4])
            elif d == 12:
                c.px(x, y, CB[0] if side in 'sn' else CB[1])
    return c


def stairs(kind):
    """Trappenstraat (noord-zuid): treden 4 px; kind = l/m/r (zijmuurtjes) of 'y' (gele trapranden)."""
    c = Canvas(16, 16)
    for y in range(16):
        for x in range(16):
            r = y % 4
            col = [CB[4], CB[3], CB[2], CB[0]][r]
            if kind == 'y' and r == 0:
                col = YL6
            c.px(x, y, col)
    if kind in ('l', 'lr'):
        c.rect(0, 0, 2, 15, CB[2]); c.vline(0, 0, 15, OL6); c.vline(1, 0, 15, CB[4]); c.vline(3, 0, 15, CB[0])
    if kind in ('r', 'lr'):
        c.rect(13, 0, 15, 15, CB[2]); c.vline(15, 0, 15, OL6); c.vline(14, 0, 15, CB[1]); c.vline(12, 0, 15, CB[0])
    return c


def clay_cliff(part):
    """Uitgesleten kleiwand (de hellingen van de kom): geulen per 16 px, rechte rechthoeken (les: kliffen)."""
    c = Canvas(16, 16)
    ground = clay(0)
    flutes = [(0, 5), (5, 9), (9, 16)]
    y_from = {'top': 8, 'mid': 0, 'base': 0}[part]
    y_to = {'top': 15, 'mid': 15, 'base': 10}[part]
    for y in range(16):
        for x in range(16):
            c.px(x, y, ground.get(x, y))
    for x0, x1 in flutes:
        for y in range(y_from, y_to + 1):
            for x in range(x0, x1):
                col = CL[2]
                if x == x0:
                    col = CL[0]
                elif x == x0 + 1:
                    col = CL[3]
                elif x == x1 - 1:
                    col = CL[1]
                c.px(x, y, col)
        if part == 'top':  # afgeronde koppen van de geulen
            c.px(x0 + 1, 8, CL[2]); c.px(x1 - 1, 8, CL[2])
    if part == 'top':
        c.hline(0, 15, 6, CL[3]); c.hline(0, 15, 7, OL6)
    if part == 'mid':  # gelaagdheid
        for x in range(16):
            if c.get(x, 9) != CL[0]:
                c.px(x, 9, CL[1])
    if part == 'base':
        c.hline(0, 15, 11, OL6); c.hline(0, 15, 12, CL[1])
        for x in (3, 11):
            c.px(x, 14, CL[1]); c.px(x + 1, 14, CL[3])
    return c



def side_edge(base, side):
    """Linker- of rechterrand van een klifstuk (omlijning + licht/schaduw)."""
    c = Canvas(16, 16)
    c.paste(base, 0, 0)
    if side == 'l':
        c.vline(0, 0, 15, OL6); c.vline(1, 0, 15, CL[3])
    else:
        c.vline(15, 0, 15, OL6); c.vline(14, 0, 15, CL[0])
    return c


def retaining_wall(part):
    """Stenen keermuur (metselwerk) voor terrassen in de stad."""
    c = Canvas(16, 16, CB[1])
    for row in range(4):
        off = 3 if row % 2 else 0
        for k in range(-1, 3):
            x0 = k * 6 + off
            for dy in range(3):
                for dx in range(5):
                    col = CB[2] if dy else CB[3]
                    if dx == 4 or dy == 2:
                        col = CB[1] if dy < 2 else CB[0]
                    c.px(x0 + dx, row * 4 + dy, col)
        c.hline(0, 15, row * 4 + 3, CB[0])
    if part == 'top':
        c.rect(0, 0, 15, 3, CB[3]); c.hline(0, 15, 0, CB[4]); c.hline(0, 15, 3, CB[1]); c.hline(0, 15, 4, OL6)
    return c


for i in range(3):
    ts.add(f'cobble{i}', cobble(i))
ts.add('sidewalk', sidewalk())
ts.add('plaza', plaza())
for i in range(3):
    ts.add(f'clay{i}', clay(i))
for s in 'nsew':
    ts.add(f'curb_{s}', curb(s))
for k in ('l', 'm', 'r', 'lr', 'y'):
    ts.add(f'stairs_{k}', stairs(k))
for part in ('top', 'mid', 'base'):
    b = clay_cliff(part)
    ts.add(f'cliff_{part}', b)
    ts.add(f'cliff_{part}_l', side_edge(b, 'l'))
    ts.add(f'cliff_{part}_r', side_edge(b, 'r'))
ts.add('rwall_top', retaining_wall('top'))
ts.add('rwall', retaining_wall('mid'))


# trap in een kleiwand: treden met wangen van klei
def cliff_stairs(part):
    c = Canvas(16, 16)
    c.paste(clay_cliff(part), 0, 0)
    s = stairs('lr')
    y0 = 6 if part == 'top' else 0
    y1 = 12 if part == 'base' else 16
    for y in range(y0, y1):
        for x in range(2, 14):
            c.px(x, y, s.get(x, y))
    return c


for part in ('top', 'mid', 'base'):
    ts.add(f'cliffstairs_{part}', cliff_stairs(part))


# ------------------------------------------------------------------ gebouwen (palet 7, varianten 8/9)
def brick_tex(c, x0, y0, x1, y1, ax=0, ay=0):
    """Onafgewerkte baksteen; ax/ay = absolute oorsprong zodat het patroon per 8 px herhaalt."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            yy, xx = (y + ay) % 8, (x + ax) % 8
            row = yy // 4
            r = yy % 4
            bx = (xx + row * 4) % 8
            if r == 3 or bx == 7:
                col = W[3]
            elif r == 0:
                col = W[2] if bx < 5 else W[1]
            elif r == 2 and bx > 3:
                col = W[0]
            else:
                col = W[1]
            c.px(x, y, col)


def plaster_tex(c, x0, y0, x1, y1, ax=0, ay=0):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            c.px(x, y, W[2])
    for (px, py) in [(5, 9), (6, 10), (6, 11), (13, 5), (2, 13)]:
        X, Y = x0 + (px - ax) % 16, y0 + (py - ay) % 16
        if x0 <= X <= x1 and y0 <= Y <= y1:
            c.px(X, Y, W[1])


def slab(c, y, x0=0, x1=15):
    """Betonnen vloerplaat (3 px)."""
    c.hline(x0, x1, y, K[3]); c.hline(x0, x1, y + 1, K[1]); c.hline(x0, x1, y + 2, K[0])


def column(c, x, y0, y1, left=True):
    """Betonnen kolom van 3 px + omlijning aan de buitenkant."""
    if left:
        c.vline(x, y0, y1, OLB); c.vline(x + 1, y0, y1, K[3]); c.vline(x + 2, y0, y1, K[1]); c.vline(x + 3, y0, y1, K[0])
    else:
        c.vline(x, y0, y1, K[2]); c.vline(x + 1, y0, y1, K[1]); c.vline(x + 2, y0, y1, K[0]); c.vline(x + 3, y0, y1, OLB)


def window(c, x0, y0, w=10, h=8, kind='glass'):
    c.box(x0, y0, x0 + w - 1, y0 + h - 1, OLB)
    c.rect(x0 + 1, y0 + 1, x0 + w - 2, y0 + h - 2, G[1])
    c.rect(x0 + 1, y0 + h - 3, x0 + w - 2, y0 + h - 2, G[0])
    for i in range(3):  # glinstering diagonaal
        c.px(x0 + 2 + i, y0 + 3 - i, G[2])
    c.vline(x0 + w // 2, y0 + 1, y0 + h - 2, K[2])
    c.hline(x0, x0 + w - 1, y0 + h, K[3])  # vensterbank
    if kind == 'curtain':
        c.rect(x0 + 1, y0 + 1, x0 + 3, y0 + h - 2, R[2])
        c.vline(x0 + 3, y0 + 1, y0 + h - 2, R[1])


def facade(kind, piece, tex='brick'):
    """Gevelstuk van 16 breed. kind: up (1 rij) of gf (begane grond, 2 rijen)."""
    h = 16 if kind == 'up' else 32
    c = Canvas(16, h)
    (brick_tex if tex == 'brick' else plaster_tex)(c, 0, 0, 15, h - 1)
    slab(c, 0)
    if piece == 'l':
        column(c, 0, 3, h - 1, True)
    if piece == 'r':
        column(c, 12, 3, h - 1, False)
    if kind == 'up':
        if piece in ('win', 'curtain'):
            window(c, 3, 5, 10, 7, 'curtain' if piece == 'curtain' else 'glass')
        if piece == 'open':  # obra gruesa: open verdieping, donker binnen
            c.rect(0, 3, 15, 15, G[0]); c.rect(0, 13, 15, 15, OLB)
            c.vline(6, 3, 15, K[1]); c.vline(7, 3, 15, K[2]); c.vline(8, 3, 15, K[0])
        if piece == 'openl':
            c.rect(4, 3, 15, 15, G[0]); c.rect(4, 13, 15, 15, OLB); column(c, 0, 3, 15, True)
        if piece == 'openr':
            c.rect(0, 3, 11, 15, G[0]); c.rect(0, 13, 11, 15, OLB); column(c, 12, 3, 15, False)
    else:
        c.hline(0, 15, h - 1, K[0])  # plint
        if piece == 'door':
            c.box(3, 9, 12, h - 1, OLB)
            c.rect(4, 10, 11, h - 2, R[1])
            for x in (5, 8, 10):
                c.vline(x, 10, h - 2, R[2])
            for x in (6, 9):
                c.vline(x, 10, h - 2, R[0])
            c.px(10, 21, K[3])
            c.hline(2, 13, 8, K[3])
        if piece == 'shutter':  # rolluik van een winkeltje
            c.box(1, 6, 14, h - 1, OLB)
            for y in range(7, h - 1):
                c.hline(2, 13, y, R[2] if y % 3 == 0 else (R[1] if y % 3 == 1 else R[0]))
            c.rect(2, 7, 13, 8, K[2])
        if piece == 'shop':  # open winkeltje met waren
            c.box(1, 6, 14, h - 1, OLB)
            c.rect(2, 7, 13, h - 2, G[0])
            c.rect(2, 7, 13, 8, R[1])
            for x in range(2, 14):
                c.px(x, 9, R[0] if x % 2 else R[2])
            c.rect(2, 22, 13, 24, K[2]); c.hline(2, 13, 25, K[0])
            for x, col in [(3, R[2]), (5, W[2]), (7, G[2]), (9, R[1]), (11, W[1])]:
                c.rect(x, 19, x + 1, 21, col)
            for x, col in [(4, W[3]), (8, R[2]), (10, G[1])]:
                c.rect(x, 14, x + 1, 17, col)
        if piece == 'win':
            window(c, 3, 10, 10, 9)
        if piece == 'l':
            pass
    return c


def flat_roof(piece, extra=None):
    """Plat betonnen dak (bovenaanzicht) van 1 rij: borstwering rondom."""
    c = Canvas(16, 16, K[1])
    for (x, y) in [(4, 6), (5, 6), (11, 9), (12, 10), (8, 12), (2, 10)]:
        c.px(x, y, K[0] if (x + y) % 3 else K[2])
    c.hline(0, 15, 0, OLB); c.hline(0, 15, 1, K[3]); c.hline(0, 15, 2, K[2]); c.hline(0, 15, 3, K[0])
    c.hline(0, 15, 13, K[0]); c.hline(0, 15, 14, K[3]); c.hline(0, 15, 15, K[2])
    if piece == 'l':
        c.vline(0, 0, 15, OLB); c.vline(1, 1, 14, K[3]); c.vline(2, 2, 13, K[2]); c.vline(3, 4, 12, K[0])
    if piece == 'r':
        c.vline(15, 0, 15, OLB); c.vline(14, 1, 14, K[2]); c.vline(13, 2, 13, K[1]); c.vline(12, 4, 12, K[3])
    if extra == 'tank':  # zwarte watertank (tinaco)
        tk = ascii_canvas([
            "...oooo...",
            ".oottggoo.",
            "otgggtgggo",
            "oggggggggo",
            "oottttttoo",
            "oggggggggo",
            "ottttttttto"[:10],
            "oggggggggo",
            ".oooooooo.",
        ], {'o': OLB, 'g': G[0], 't': G[1]})
        c.paste(tk, 3, 4)
    if extra == 'rebar':  # wachtijzers op de kolommen (bouwt later verder)
        for x in ((2, 4) if piece == 'l' else (11, 13) if piece == 'r' else (7, 9)):
            c.vline(x, 4, 9, W[0]); c.px(x, 3, W[1])
    if extra == 'laundry':
        c.hline(1, 14, 5, OLB)
        for x, col in [(3, R[2]), (4, R[2]), (7, W[2]), (8, W[2]), (11, G[2]), (12, G[2])]:
            c.vline(x, 6, 9, col)
        for x, col in [(3, R[1]), (7, W[1]), (11, G[1])]:
            c.px(x, 9, col)
    if extra == 'dish':
        d = ascii_canvas(["..oooo..", ".okkkko.", "okkkkkko", "okkkkkko", ".okkkko.", "..oooo..", "...oo...", "..oooo.."],
                         {'o': OLB, 'k': K[3]})
        c.paste(d, 5, 3)
    return c


def gable_roof(piece, row, stones=False):
    """Golfplaatdak (voorhelling, 2 rijen). Ribbels per 4 px."""
    c = Canvas(16, 16)
    for y in range(16):
        for x in range(16):
            f = x % 4
            col = [R[2], R[1], R[1], R[0]][f]
            c.px(x, y, col)
    if row == 0:
        c.hline(0, 15, 0, OLB); c.hline(0, 15, 1, R[2]); c.hline(0, 15, 2, R[0]); c.hline(0, 15, 3, OLB)
        for x in range(0, 16, 4):  # nagels
            c.px(x + 1, 6, K[3])
    else:
        for x in range(0, 16, 4):
            c.px(x + 1, 6, K[3])
        c.hline(0, 15, 11, R[2]); c.hline(0, 15, 12, OLB)
        c.rect(0, 13, 15, 15, W[0]); c.hline(0, 15, 15, OLB)  # schaduw onder de dakrand
    if piece == 'l':
        c.vline(0, 0, 15, OLB); c.vline(1, 1 if row == 0 else 0, 11 if row else 15, R[2])
    if piece == 'r':
        c.vline(15, 0, 15, OLB); c.vline(14, 1 if row == 0 else 0, 11 if row else 15, R[0])
    if stones:  # stenen om de platen vast te houden
        for (x, y) in ([(3, 8), (10, 5)] if row == 0 else [(6, 3)]):
            c.rect(x, y, x + 2, y + 1, K[2]); c.hline(x, x + 2, y + 2, K[0]); c.px(x, y, K[3])
    return c


def add_grid(name, grid_canvases, layers=None):
    for y, row in enumerate(grid_canvases):
        for x, cv in enumerate(row):
            ts.add(f'{name}_{x}_{y}', cv)


# platte daken
for p in ('l', 'm', 'r'):
    ts.add(f'roof_{p}', flat_roof(p))
for p, e in [('m', 'tank'), ('m', 'laundry'), ('m', 'dish'), ('l', 'rebar'), ('r', 'rebar'), ('m', 'rebar')]:
    ts.add(f'roof_{p}_{e}', flat_roof(p, e))
# golfplaatdaken
for row in (0, 1):
    for p in ('l', 'm', 'r'):
        ts.add(f'gable{row}_{p}', gable_roof(p, row))
    ts.add(f'gable{row}_m_stones', gable_roof('m', row, True))
# gevels
for tex in ('brick', 'plaster'):
    t = 'b' if tex == 'brick' else 'p'
    for piece in ('l', 'm', 'r', 'win', 'curtain') if t == 'b' else ('l', 'r', 'win', 'curtain'):
        ts.add(f'up{t}_{piece}', facade('up', piece, tex))
    for piece in ('l', 'm', 'r', 'door', 'shutter', 'shop', 'win') if t == 'b' else ('l', 'r', 'door', 'win'):
        cv = facade('gf', piece, tex)
        ts.add(f'gf{t}_{piece}_0', cv.sub(0, 0, 16, 16))
        ts.add(f'gf{t}_{piece}_1', cv.sub(0, 16, 16, 16))
for piece in ('open', 'openl', 'openr'):
    ts.add(f'upb_{piece}', facade('up', piece, 'brick'))

# ------------------------------------------------------------------ cholet (palet 10)
def cholet_row(kind, piece, scheme=0):
    """Modulaire cholet (palet 10): rijen van 16 px, stukken l/m/m2/r (m herhaalbaar).
    kind: roof, crown, floor, hall0, hall1. scheme 0..2 = kleurenset van de banden."""
    band, band2 = [(PK[0], YEC), (ORC, PU[1]), (LIC, PK[1])][scheme]
    c = Canvas(16, 16, WHC)
    if kind == 'roof':  # plat wit dak, borstwering
        c.rect(0, 0, 15, 15, GYC)
        c.hline(0, 15, 0, OLC); c.hline(0, 15, 1, WHC); c.hline(0, 15, 13, OLC); c.hline(0, 15, 14, WHC); c.hline(0, 15, 15, band)
        for x in range(2, 16, 8):
            c.px(x, 6, WHC); c.px(x + 4, 10, WHC)
    if kind == 'crown':  # kroonlijst met trapmotief (chakana-treden)
        c.rect(0, 0, 15, 15, band)
        for x in range(16):
            s = x % 8
            h = [0, 1, 2, 3, 3, 2, 1, 0][s]
            c.vline(x, 9 - h * 2, 13, band2)
        c.hline(0, 15, 0, OLC); c.hline(0, 15, 1, WHC); c.hline(0, 15, 14, WHC); c.hline(0, 15, 15, OLC)
    if kind == 'floor':
        c.rect(0, 0, 15, 2, band)
        for x in range(0, 16, 4):
            c.px(x + 1, 1, band2); c.px(x + 2, 1, band2)
        c.rect(0, 3, 15, 13, MG[1]); c.rect(0, 10, 15, 13, MG[0])
        for x in (0, 8):
            c.vline(x, 3, 13, WHC)
        c.px(3, 5, MG[2]); c.px(4, 4, MG[2]); c.px(11, 5, MG[2]); c.px(12, 4, MG[2])
        c.hline(0, 15, 14, WHC); c.hline(0, 15, 15, GYC)
        if piece == 'm2':  # ruitmotief tussen de ramen
            c.rect(6, 4, 10, 12, WHC)
            c.px(8, 5, band); c.rect(7, 6, 9, 10, band); c.px(8, 11, band); c.px(8, 8, band2)
    if kind in ('hall0', 'hall1'):
        if kind == 'hall0':
            c.rect(0, 0, 15, 2, WHC); c.rect(0, 3, 15, 9, PU[0])
            for x in range(1, 16, 4):
                c.rect(x, 5, x + 1, 7, YEC)
            c.hline(0, 15, 10, OLC)
            c.rect(0, 11, 15, 15, MG[0])
            for x in (3, 7, 11, 15):
                c.vline(x, 11, 15, MG[1])
        else:
            c.rect(0, 0, 15, 15, MG[0])
            for x in (3, 7, 11, 15):
                c.vline(x, 0, 14, MG[1])
            c.hline(0, 15, 15, OLC)
        if piece == 'door':
            c.rect(6, 11 if kind == 'hall0' else 0, 9, 15, GDC)
            c.vline(7, 11 if kind == 'hall0' else 0, 14, YEC)
            if kind == 'hall0':
                c.rect(1, 12, 4, 13, MG[2])
    if piece == 'l':
        c.rect(0, 0, 3, 15, band if kind not in ('roof',) else GYC)
        c.vline(0, 0, 15, OLC); c.vline(1, 0, 15, band2 if kind in ('floor', 'hall1') else WHC)
        if kind == 'roof':
            c.vline(1, 1, 14, WHC); c.hline(0, 3, 0, OLC); c.hline(0, 3, 13, OLC)
    if piece == 'r':
        c.rect(12, 0, 15, 15, band if kind not in ('roof',) else GYC)
        c.vline(15, 0, 15, OLC); c.vline(14, 0, 15, band2 if kind in ('floor', 'hall1') else WHC)
        if kind == 'roof':
            c.vline(14, 1, 14, WHC); c.hline(12, 15, 0, OLC); c.hline(12, 15, 13, OLC)
    return c


def chalet():
    """Het 'chalet' van de eigenaar bovenop een cholet (3 x 2), staat op het cholet-dak."""
    c = Canvas(48, 32)
    for x in range(3):
        c.paste(cholet_row('roof', 'm'), x * 16, 0)
        c.paste(cholet_row('roof', 'm'), x * 16, 16)
    for y in range(2, 14):  # schuin dak paars
        x0, x1 = 6 + (13 - y) // 2, 41 - (13 - y) // 2
        c.hline(x0, x1, y, PU[1] if (y // 2) % 2 else PU[0])
    c.hline(4, 43, 14, OLC); c.hline(6, 41, 1, OLC)
    c.rect(6, 15, 41, 29, WHC); c.vline(6, 15, 29, OLC); c.vline(41, 15, 29, OLC); c.hline(6, 41, 29, OLC)
    for x in (10, 30):
        c.rect(x, 18, x + 6, 24, MG[1]); c.box(x - 1, 17, x + 7, 25, OLC); c.px(x + 1, 19, MG[2])
    c.rect(20, 18, 27, 29, GDC); c.box(19, 17, 28, 29, OLC); c.vline(23, 18, 28, YEC)
    return c


for k in ('roof', 'crown'):
    for p in ('l', 'm', 'r'):
        for sch in ((0, 1, 2) if k == 'crown' else (0,)):
            ts.add(f'cholet_{k}{sch}_{p}', cholet_row(k, p, sch))
for sch in (0, 1, 2):
    for p in ('l', 'm', 'm2', 'r'):
        ts.add(f'cholet_floor{sch}_{p}', cholet_row('floor', p, sch))
for k in ('hall0', 'hall1'):
    for p in ('l', 'm', 'door', 'r'):
        ts.add(f'cholet_{k}_{p}', cholet_row(k, p))
CHALET = chalet()
OBJ = {}



def slice_obj(name, cv, ground, top_rows=(), beh=None):
    """Knip een object in metatiles: dekkend -> onderlaag; met transparantie -> grond + object boven."""
    ids = []
    for my in range(cv.h // 16):
        row = []
        for mx in range(cv.w // 16):
            s = cv.sub(mx * 16, my * 16, 16, 16)
            if not s.a[:, :, 3].any():
                row.append(None)
                continue
            b = (beh or {}).get((mx, my), 'MB_NORMAL')
            nm = f'{name}_{mx}_{my}'
            if s.a[:, :, 3].all() and my not in top_rows:
                row.append(ts.add(nm, s, beh=b))
            else:
                row.append(ts.add(nm, ground, s, beh=b, layer='normal' if my in top_rows else 'covered'))
        ids.append(row)
    return ids


COB = cobble(0)
OBJ['chalet'] = slice_obj('chalet', CHALET, COB)


# ------------------------------------------------------------------ kabelbaan (palet 11)
def ekat_station():
    """Ekat99 'Cable Car': het stationsgebouw (7 x 5), omgekleurd naar palet 11."""
    im = Image.open('tilesets/nieuw/ekat/Cable Car.png').convert('RGBA')
    a = np.array(im)
    c = Canvas(112, 80)
    mp = {(49, 56, 82): OLT, (255, 255, 255): WHT, (248, 240, 216): WHT,
          (103, 151, 133): BL[2], (91, 133, 117): BL[1], (67, 97, 85): BL[0], (61, 88, 77): BL[0],
          (168, 136, 104): ST[2], (144, 104, 88): ST[1], (124, 90, 76): ST[0],
          (168, 200, 248): BL[2], (208, 224, 248): WHT, (192, 192, 168): ST[2], (144, 144, 136): ST[1],
          (120, 120, 128): ST[0], (64, 72, 104): OLT}
    for y in range(80):
        for x in range(112):
            r, g, b, al = a[y, x]
            if al == 0:
                continue
            cell_red = (a[(y // 16) * 16:(y // 16) * 16 + 16, (x // 16) * 16:(x // 16) * 16 + 16, :3] == (255, 0, 0)).all(-1).any()
            if cell_red:
                continue
            col = mp.get((int(r), int(g), int(b)))
            if col is None:
                continue
            c.px(x, y, col)
    # rode band van de lijn (Línea Roja) over de gevel en een gondel in de opening
    return c


def mast(dirn='ew'):
    """Kabelbaanmast (1 x 4): stalen buis die naar boven smaller wordt, kop met schijven."""
    c = Canvas(16, 64)
    for y in range(12, 60):
        w = 2 + (y - 12) // 16  # breder naar beneden
        cx = 8
        c.rect(cx - w, y, cx + w - 1, y, ST[1])
        c.px(cx - w, y, OLT); c.px(cx + w - 1, y, OLT)
        c.px(cx - w + 1, y, ST[2])
        if w > 2:
            c.px(cx + w - 2, y, ST[0])
    for y in range(20, 58, 9):  # klimbeugels
        c.px(9, y, ST[0])
    # voet
    c.rect(2, 56, 13, 63, ST[1]); c.box(2, 56, 13, 63, OLT); c.hline(3, 12, 57, ST[2]); c.hline(3, 12, 62, ST[0])
    # kop
    if dirn == 'ew':
        c.rect(3, 1, 12, 13, ST[1]); c.box(3, 1, 12, 13, OLT); c.vline(4, 2, 12, ST[2])
        for y in (3, 11):
            c.rect(0, y, 2, y, OLT); c.rect(13, y, 15, y, OLT)
            c.rect(5, y - 1, 10, y + 1, RD[0]); c.hline(5, 10, y - 1, RD[1])
    else:
        c.rect(1, 4, 14, 11, ST[1]); c.box(1, 4, 14, 11, OLT); c.hline(2, 13, 5, ST[2])
        for x in (4, 11):
            c.rect(x - 1, 2, x + 1, 9, RD[0]); c.vline(x - 1, 2, 9, RD[1]); c.vline(x, 0, 3, OLT)
    return c


def cable(dirn):
    c = Canvas(16, 16)
    if dirn == 'ew':
        c.hline(0, 15, 3, OLT); c.hline(0, 15, 11, OLT)
    else:
        c.vline(4, 0, 15, OLT); c.vline(11, 0, 15, OLT)
    return c


def gondola(col, dirn='ew'):
    """Gondel (1 x 2) die aan de kabel hangt: kabel op y=3 (of 11), cabine eronder."""
    light, dark = col
    c = Canvas(16, 32)
    c.hline(0, 15, 3, OLT)
    c.rect(6, 1, 9, 4, ST[0]); c.box(6, 1, 9, 4, OLT)       # klem
    c.vline(7, 5, 9, OLT); c.vline(8, 5, 9, ST[1])           # hanger
    c.rect(2, 10, 13, 12, light); c.box(2, 10, 13, 12, OLT)  # dak
    c.hline(3, 12, 11, WHT)
    c.rect(2, 13, 13, 24, dark); c.box(2, 13, 13, 24, OLT)   # cabine
    c.rect(3, 14, 12, 19, BL[2]); c.hline(3, 12, 19, BL[1])  # ramen
    c.vline(7, 14, 19, dark); c.vline(8, 14, 19, dark)
    c.px(4, 15, WHT); c.px(5, 14, WHT)
    c.rect(3, 20, 12, 23, light); c.hline(3, 12, 23, dark)
    if dirn == 'ew':
        pass
    return c


OBJ['station'] = slice_obj('station', ekat_station(), COB, top_rows=(0,))
OBJ['mast_ew'] = slice_obj('mast_ew', mast('ew'), COB, top_rows=(0, 1))
OBJ['mast_ns'] = slice_obj('mast_ns', mast('ns'), COB, top_rows=(0, 1))
CABLE = {}
for d in ('ew', 'ns'):
    CABLE[d] = cable(d)
    ts.add(f'cable_{d}', COB, CABLE[d], layer='normal')
GONDOLA = {}
for nm, col in [('red', (RD[1], RD[0])), ('yellow', (YE[1], YE[0])), ('green', (GN[1], GN[0]))]:
    GONDOLA[nm] = gondola(col)


# ------------------------------------------------------------------ markt (palet 11, op de Slateport-tent)
def slateport_tent(scheme):
    """Slateport-marktkraam (Game Freak), omgekleurd; scheme blue/red/yellow."""
    src = repo_top_layer('SlateportCity', 2, 41, 7, 44)
    c = Canvas(80, 48)
    tarp = {'blue': (BL[1], BL[0], BL[2], WHT), 'red': (RD[1], RD[0], WHT, YE[1]),
            'yellow': (YE[1], YE[0], WHT, WHT), 'green': (GN[1], GN[0], YE[1], WHT)}[scheme]
    mp = {(123, 148, 246): tarp[0], (82, 123, 180): tarp[1], (189, 197, 246): tarp[2], (238, 246, 230): tarp[3],
          (65, 74, 106): OLT, (139, 115, 74): WD, (123, 98, 65): ST[0]}
    for y in range(48):
        for x in range(80):
            col = src.get(x, y)
            if col is None or col not in mp:
                continue
            if y >= 30 and not (x < 16 or x > 60):  # potten onder de tent weg
                continue
            c.px(x, y, mp[col])
    if scheme == 'red':  # rood-witte banen op het tentdoek
        for y in range(0, 30):
            for x in range(80):
                if c.get(x, y) == RD[1] and (x // 4) % 2:
                    c.px(x, y, WHT)
    return c.sub(8, 0, 64, 48)


def stall_goods(kind):
    """Waren op een kleed of tafel (1 x 1)."""
    c = Canvas(16, 16)
    if kind == 'potatoes':  # aardappels in alle kleuren (chuño, papa)
        c.rect(1, 6, 14, 14, WD); c.box(1, 6, 14, 14, OLT); c.hline(2, 13, 7, ST[2])
        rnd = random.Random(5)
        for i in range(14):
            x, y = 2 + rnd.randrange(11), 8 + rnd.randrange(5)
            col = rnd.choice([YE[0], WD, RD[0], ST[0]])
            c.rect(x, y, x + 1, y, col)
            c.px(x, y - 1, YE[1] if col == YE[0] else ST[1])
        c.rect(3, 3, 12, 6, ST[1]); c.box(3, 3, 12, 6, OLT)  # weegschaal
        c.hline(4, 11, 4, ST[2])
    if kind == 'fruit':
        c.rect(1, 7, 14, 14, WD); c.box(1, 7, 14, 14, OLT)
        for (x, y, col) in [(3, 4, YE[1]), (6, 3, RD[1]), (9, 4, GN[1]), (5, 6, YE[0]), (8, 6, RD[1]), (11, 6, YE[1]),
                            (3, 8, RD[1]), (10, 8, GN[1])]:
            c.rect(x, y, x + 2, y + 2, col); c.px(x, y, WHT); c.px(x + 2, y + 2, OLT)
    if kind == 'aguayo':  # kleurig weefsel op de grond
        cols = [RD[1], YE[1], GN[1], BL[1], RD[0], WHT, BL[0]]
        for y in range(3, 15):
            col = cols[(y - 3) // 2 % len(cols)]
            c.hline(1, 14, y, col)
            if y % 4 == 0:
                for x in range(2, 14, 3):
                    c.px(x, y, WHT if col != WHT else RD[0])
        c.box(1, 3, 14, 14, OLT)
    if kind == 'sacks':
        for x0 in (1, 8):
            c.rect(x0, 5, x0 + 6, 14, ST[2]); c.box(x0, 5, x0 + 6, 14, OLT)
            c.rect(x0 + 1, 4, x0 + 5, 6, YE[1]); c.hline(x0 + 1, x0 + 5, 7, ST[1])
    if kind == 'crate':
        c.rect(2, 4, 13, 14, WD); c.box(2, 4, 13, 14, OLT)
        c.hline(3, 12, 8, OLT); c.hline(3, 12, 5, YE[0])
        for x in (4, 7, 10):
            c.rect(x, 2, x + 1, 4, GN[1]); c.px(x, 1, GN[0])
    if kind == 'herbs':  # gedroogde kruiden en bundels (Mercado de las Brujas, zonder het enge)
        c.rect(1, 9, 14, 14, WD); c.box(1, 9, 14, 14, OLT)
        for x in (2, 6, 10):
            c.rect(x, 3, x + 3, 9, GN[0]); c.rect(x + 1, 3, x + 2, 7, GN[1]); c.hline(x, x + 3, 6, RD[1])
    return c


for scheme in ('blue', 'red'):
    OBJ[f'tent_{scheme}'] = slice_obj(f'tent_{scheme}', slateport_tent(scheme), COB, top_rows=(0,))
GOODS = {}
for k in ('potatoes', 'fruit', 'aguayo', 'sacks', 'crate', 'herbs'):
    GOODS[k] = ts.add(f'goods_{k}', COB, stall_goods(k))


# ------------------------------------------------------------------ straatmeubilair
def lamp():
    c = Canvas(16, 32)
    c.rect(6, 2, 10, 5, YE[1]); c.box(5, 1, 11, 6, OLT); c.hline(6, 10, 2, WHT)
    c.vline(8, 7, 28, ST[0]); c.vline(7, 7, 28, ST[1])
    c.rect(5, 28, 10, 30, ST[1]); c.box(5, 28, 10, 31, OLT)
    return c


def bench():
    c = Canvas(16, 16)
    c.rect(1, 5, 14, 7, WD); c.box(1, 4, 14, 8, OLT); c.hline(2, 13, 5, YE[0])
    c.rect(1, 9, 14, 10, WD); c.box(1, 9, 14, 11, OLT)
    c.vline(2, 12, 14, OLT); c.vline(13, 12, 14, OLT)
    return c


def manhole():
    c = Canvas(16, 16)
    c.mask_fill(ellipse_mask(8, 8, 6, 5), ST[0])
    c.mask_fill(ellipse_mask(8, 8, 5, 4), ST[1])
    for x in range(4, 13, 2):
        c.vline(x, 6, 10, ST[0])
    return c


OBJ['lamp'] = slice_obj('lamp', lamp(), COB, top_rows=(0,))
ts.add('bench', COB, bench())
ts.add('manhole', COB, manhole())


# ------------------------------------------------------------------ natuur (palet 12)
def eucalyptus():
    """Eucalyptus (2 x 3): hoog, smal, blauwgroen blad, gevlekte stam."""
    c = Canvas(32, 48)
    rnd = random.Random(77)
    # stam
    c.rect(14, 26, 17, 45, TRN); c.vline(14, 26, 45, OLN); c.vline(17, 26, 45, OLN); c.vline(15, 28, 44, SN[1])
    for y in (30, 36, 41):
        c.px(16, y, RK[2])
    c.rect(11, 45, 20, 46, TG[0])
    # kruin: losse wolkjes boven elkaar
    blobs = [(16, 9, 8, 7), (10, 17, 7, 6), (22, 18, 7, 6), (16, 22, 9, 5), (15, 4, 5, 4)]
    for cx, cy, rx, ry in blobs:
        c.mask_fill(ellipse_mask(cx, cy, rx, ry), TG[1])
    for cx, cy, rx, ry in blobs:
        c.mask_fill(lambda x, y, cx=cx, cy=cy, rx=rx, ry=ry: ellipse_mask(cx - 2, cy - 2, rx - 3, ry - 3)(x, y), EU)
    for cx, cy, rx, ry in blobs:
        c.mask_fill(lambda x, y, cx=cx, cy=cy, rx=rx, ry=ry: ellipse_mask(cx, cy, rx, ry)(x, y) and not ellipse_mask(cx - 1, cy - 1, rx, ry)(x, y), TG[0])
    for _ in range(30):
        x, y = rnd.randrange(32), rnd.randrange(30)
        if c.get(x, y) == TG[1]:
            c.px(x, y, TG[2])
    c.outline(OLN)
    return c


def planter(kind):
    c = Canvas(16, 16)
    c.rect(1, 8, 14, 14, RK[1]); c.box(1, 8, 14, 15, OLN); c.hline(2, 13, 9, RK[2])
    for (x, y) in [(3, 5), (7, 3), (11, 5), (5, 6), (9, 6)]:
        c.rect(x, y, x + 2, y + 2, TG[1]); c.px(x, y, TG[2]); c.px(x + 2, y + 2, TG[0])
    if kind == 'flowers':
        for (x, y, col) in [(4, 4, FLR), (8, 3, FLY), (12, 5, FLR), (6, 6, FLY)]:
            c.px(x, y, col)
    c.outline(OLN)
    return c


OBJ['eucalyptus'] = slice_obj('eucalyptus', eucalyptus(), COB, top_rows=(0, 1))
ts.add('planter', COB, planter('green'))
ts.add('planter_flowers', COB, planter('flowers'))


def illimani():
    """De Illimani als decor (12 x 5): drie besneeuwde toppen, hellingen van 45 graden zodat de
    tegels langs de kammen herhalen (tegelzuinig). Boven de kam: hoger sneeuwveld."""
    W_, H_ = 192, 80
    c = Canvas(W_, H_)
    peaks = [(40, 16), (96, 0), (152, 24)]

    def ridge(x):
        return min(py + abs(x - px_) for px_, py in peaks)

    def tri(v, period=16, amp=8):
        v %= period
        return v if v < period // 2 else period - v
    for x in range(W_):
        top = ridge(x)
        px_, py = min(peaks, key=lambda p: p[1] + abs(x - p[0]))
        left = x < px_
        for y in range(H_):
            if y < top:
                col = SN[1]
                if (x * 3 + y * 5) % 32 == 0:
                    col = SN[2]
            elif y == top:
                col = OLN
            else:
                snowline = 40 + tri(x + (8 if left else 0))
                if y < snowline:
                    col = SN[0] if left else SN[1]
                    if not left and (x + y) % 8 == 0:
                        col = SN[2]
                    if left and (x - y) % 16 == 0 and y > top + 2:
                        col = SN[1]
                elif y == snowline:
                    col = SN[2]
                else:
                    col = RK[2] if left else RK[1]
                    if (x + 2 * y) % 16 == 0:
                        col = RK[0] if not left else RK[1]
                if x == px_ and y > top:
                    col = SN[1] if y < snowline else RK[1]
            if y > 75:
                col = None
            elif y == 75:
                col = OLN
            c.px(x, y, col)
    return c


ILL = illimani()


def slice_ill(cv):
    """Rotsrand onderaan over kleigrond (2 lagen); de rest is dekkend palet 12."""
    ids = []
    for my in range(cv.h // 16):
        row = []
        for mx in range(cv.w // 16):
            s = cv.sub(mx * 16, my * 16, 16, 16)
            nm = f'illimani_{mx}_{my}'
            if s.a[:, :, 3].all():
                row.append(ts.add(nm, s))
            else:
                row.append(ts.add(nm, clay(0), s, layer='covered'))
        ids.append(row)
    return ids



OBJ['illimani'] = slice_ill(ILL)

# ------------------------------------------------------------------ mock-up
N = ts.names


def grid_fill(w, h, name):
    return [[N[name]] * w for _ in range(h)]


def put(g, x, y, ids):
    for dy, row in enumerate(ids):
        for dx, m in enumerate(row):
            if m is not None and 0 <= y + dy < len(g) and 0 <= x + dx < len(g[0]):
                g[y + dy][x + dx] = m


def house(g, x, y, w, floors=2, roof='flat', tex='b', pal=7, extras=(), gf=None, upper=None):
    """Zet een huis neer vanaf (x, y) = linkerbovenhoek van het dak."""
    rows = []
    if roof == 'flat':
        r = ['roof_l'] + ['roof_m'] * (w - 2) + ['roof_r']
        for i, e in extras:
            r[i] = e
        rows.append(r)
    else:
        rows.append(['gable0_l'] + ['gable0_m'] * (w - 2) + ['gable0_r'])
        r = ['gable1_l'] + ['gable1_m'] * (w - 2) + ['gable1_r']
        for i, e in extras:
            r[i] = e
        rows.append(r)
    for f in range(floors - 1):
        u = (upper or {}).get(f) or ([f'up{tex}_l'] + [f'up{tex}_win'] * (w - 2) + [f'up{tex}_r'])
        rows.append(u)
    gfrow = gf or ([f'gf{tex}_l'] + [f'gf{tex}_door'] + [f'gf{tex}_win'] * (w - 3) + [f'gf{tex}_r'])
    rows.append([n + '_0' for n in gfrow])
    rows.append([n + '_1' for n in gfrow])
    ids = []
    for r in rows:
        row = []
        for n in r:
            m = N[n]
            if pal != 7:
                vn = f'{n}@{pal}'
                if vn not in N:
                    ts.add_palvariant(vn, n, 7, pal)
                m = N[vn]
            row.append(m)
        ids.append(row)
    put(g, x, y, ids)


def cholet(g, x, y, w, floors=3, scheme=0, chalet=False):
    rows = []
    if chalet:
        rows += [[None] * w]
    rows.append([f'cholet_roof0_l'] + ['cholet_roof0_m'] * (w - 2) + ['cholet_roof0_r'])
    rows.append([f'cholet_crown{scheme}_l'] + [f'cholet_crown{scheme}_m'] * (w - 2) + [f'cholet_crown{scheme}_r'])
    for f in range(floors):
        sch = (scheme + f) % 3
        mid = [f'cholet_floor{sch}_m' if (i % 2 == 0) else f'cholet_floor{sch}_m2' for i in range(w - 2)]
        rows.append([f'cholet_floor{sch}_l'] + mid + [f'cholet_floor{sch}_r'])
    for k in ('hall0', 'hall1'):
        mid = [f'cholet_{k}_m'] * (w - 2)
        mid[(w - 2) // 2] = f'cholet_{k}_door'
        rows.append([f'cholet_{k}_l'] + mid + [f'cholet_{k}_r'])
    put(g, x, y, [[N[n] if n else None for n in r] for r in rows])
    if chalet:  # chalet staat op het dak (rij 2 = dak); 2 rijen erboven
        put(g, x + (w - 3) // 2, y, OBJ['chalet'])


overlay_cache = {}


def overlay(base_id, top_canvas, key):
    """Kabel/gondel over een bestaande metatile: nieuwe combinatie (tegels worden zo veel mogelijk hergebruikt)."""
    k = (base_id, key)
    if k in overlay_cache:
        return overlay_cache[k]
    name, ents, attr = ts.mts[base_id - 512]
    # render de bestaande bovenlaag + nieuwe bovenlaag
    bottom = Canvas(16, 16)
    top = Canvas(16, 16)
    # onderlaag hergebruiken: entries kopiëren
    toprgb = Canvas(16, 16)
    for kq in range(4):
        e = ents[4 + kq]
        t = e & 0x3FF
        if t >= 512:
            tp = ts.tiles[t - 512]
            tp = tp[:, ::-1] if (e >> 10) & 1 else tp
            tp = tp[::-1, :] if (e >> 11) & 1 else tp
            pal = ts.pals[e >> 12]
            for yy in range(8):
                for xx in range(8):
                    if tp[yy, xx]:
                        toprgb.px((kq % 2) * 8 + xx, (kq // 2) * 8 + yy, pal[tp[yy, xx]])
    toprgb.paste(top_canvas, 0, 0)
    newname = f'{name}+{key}'
    ts.names[newname] = 512 + len(ts.mts)
    tents = [ts._tile(toprgb.a[(q // 2) * 8:(q // 2) * 8 + 8, (q % 2) * 8:(q % 2) * 8 + 8]) for q in range(4)]
    ts.mts.append((newname, list(ents[:4]) + tents, (attr & 0x0FFF)))  # laagtype NORMAL: kabel boven de speler
    overlay_cache[k] = ts.names[newname]
    return overlay_cache[k]


def mockup():
    Wm, Hm = 30, 20
    g = grid_fill(Wm, Hm, 'clay0')
    # Illimani boven, breder gemaakt met kleigrond eromheen
    put(g, 8, 0, OBJ['illimani'])
    for x in list(range(0, 8)) + list(range(22, 30)):
        for y in range(0, 5):
            g[y][x] = N['clay1' if (x + y) % 3 else 'clay2']
    # hoogste terras: kleiwand
    for x in range(Wm):
        g[5][x] = N['cliff_top']; g[6][x] = N['cliff_base']
    g[5][0] = N['cliff_top_l']; g[6][0] = N['cliff_base_l']
    g[5][13] = N['cliffstairs_top']; g[6][13] = N['cliffstairs_base']
    # bovenste rij huizen (op klei) y 7..10
    for x in range(Wm):
        for y in range(7, 12):
            g[y][x] = N['cobble1' if (x * 7 + y) % 5 == 0 else 'cobble0']
    house(g, 0, 7, 3, floors=2, tex='b', extras=[(1, 'roof_m_tank')])
    house(g, 3, 7, 3, floors=2, tex='p', pal=8, roof='flat', extras=[(2, 'roof_r_rebar')],
          upper={0: ['upp_l', 'upp_curtain', 'upp_r']})
    house(g, 6, 8, 3, floors=1, tex='b', roof='gable', extras=[(1, 'gable1_m_stones')])
    for y in range(7, 20):
        g[y][13] = N['stairs_y' if y % 3 == 0 else 'stairs_lr']
        g[y][12] = N['rwall' if y > 11 else 'sidewalk']
    house(g, 9, 7, 3, floors=2, tex='b', extras=[(0, 'roof_l_rebar'), (1, 'roof_m_rebar'), (2, 'roof_r_rebar')],
          upper={0: ['upb_openl', 'upb_open', 'upb_openr']}, gf=['gfb_l', 'gfb_shutter', 'gfb_r'])
    cholet(g, 14, 4, 4, floors=3, scheme=0, chalet=True)
    house(g, 18, 7, 4, floors=2, tex='p', pal=9, extras=[(2, 'roof_m_laundry')])
    cholet(g, 22, 6, 3, floors=2, scheme=1)
    house(g, 25, 7, 3, floors=2, tex='b', extras=[(1, 'roof_m_dish')])
    house(g, 28, 8, 2, floors=1, tex='p', pal=8, roof='gable')
    # straat met stoep y 12..13
    for x in range(Wm):
        if x in (12, 13):
            continue
        g[12][x] = N['curb_s']; g[13][x] = N['cobble0' if x % 4 else 'cobble2']
    # onderste rij: station + markt + plaza
    put(g, 0, 13, OBJ['station'])
    for x in range(7, 12):
        for y in range(14, 20):
            g[y][x] = N['cobble0']
    put(g, 7, 14, OBJ['mast_ew'])
    for x in range(14, 30):
        for y in range(14, 20):
            g[y][x] = N['plaza'] if x >= 23 else N['cobble0']
    put(g, 14, 14, OBJ['tent_blue']); put(g, 18, 14, OBJ['tent_red'])
    g[17][14] = GOODS['potatoes']; g[17][15] = GOODS['sacks']; g[17][16] = GOODS['fruit']
    g[17][18] = GOODS['herbs']; g[17][19] = GOODS['aguayo']; g[17][20] = GOODS['crate']
    g[19][14] = GOODS['aguayo']; g[19][16] = GOODS['fruit']
    put(g, 25, 14, OBJ['eucalyptus'])
    put(g, 23, 15, OBJ['lamp']); put(g, 28, 15, OBJ['lamp'])
    g[18][24] = N['bench']; g[18][27] = N['bench']
    g[17][23] = N['planter_flowers']; g[17][29] = N['planter']
    g[19][9] = N['manhole']
    # kabelbaan: van het station oostwaarts over de markt en de huizen (rij 13: kabel op y 3 en 11)
    cy = 14
    for x in range(7, 30):
        if x == 7:
            continue
        g[cy][x] = overlay(g[cy][x], CABLE['ew'], 'cable_ew')
    # gondels
    for x, col in [(10, 'red'), (20, 'yellow'), (27, 'green')]:
        gc = GONDOLA[col]
        g[cy][x] = overlay(g[cy][x] if not ts.mts[g[cy][x] - 512][0].endswith('+cable_ew') else
                           N[ts.mts[g[cy][x] - 512][0].split('+')[0]], gc.sub(0, 0, 16, 16), 'gondola_' + col + '0')
        g[cy + 1][x] = overlay(g[cy + 1][x], gc.sub(0, 16, 16, 16), 'gondola_' + col + '1')
    # tweede lijn noord-zuid langs de trap (over de huizen)
    for y in range(0, 14):
        g[y][11] = overlay(g[y][11], CABLE['ns'], 'cable_ns')
    return g


BASE_TILES, BASE_MTS = len(ts.tiles), len(ts.mts)
g = mockup()
ts.write(OUT)
prim = Prim('general')
img = ts.render_map(g, prim)
Image.fromarray(img).save(OUT + '/mockup.png')
Image.fromarray(img).resize((img.shape[1] * 2, img.shape[0] * 2), Image.NEAREST).save(OUT + '/mockup_2x.png')
ts.sheet(OUT + '/sheet.png')
ts.tiles_sheet(OUT + '/tiles_sheet.png')
palette_strip(ts, OUT + '/paletten.png')
ref = render_repo_map('SlateportCity', 20, 40, 0, 30)
side_by_side(img, ref, OUT + '/vergelijking.png')
print('tegels', len(ts.tiles), '/ 512   metatiles', len(ts.mts), '/ 512   (waarvan voor kabel-combinaties in de mock-up:',
      len(ts.tiles) - BASE_TILES, 'tegels,', len(ts.mts) - BASE_MTS, 'metatiles)')
if ts.errors:
    from collections import Counter
    print('kleur benaderd (kabel over ander palet):', Counter(str(e) for e in ts.errors).most_common(10))
from tilelib import budget
GROUPS = ['cobble', 'sidewalk', 'plaza', 'clay', 'curb', 'stairs', 'cliff', 'rwall', 'roof', 'gable', 'up', 'gf',
          'cholet', 'station', 'mast', 'cable', 'tent', 'goods', 'lamp', 'bench', 'manhole', 'eucalyptus', 'planter', 'illimani']
for k, v in budget(ts, GROUPS).items():
    print(f'  {k:12s} {v}')
