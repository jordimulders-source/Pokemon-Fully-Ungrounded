#!/usr/bin/env python3
"""Concept-tileset Altiplano (hoogvlakte rond de startstad, Fully Ungrounded): secondary bij General.

Gebruik (vanuit de repo-root):  python3 tools/concept/tiles/altiplano_tiles.py
Uitvoer: tilesets/eigen/altiplano/ (zelfde bestanden als la_paz).
Alles zelf getekend (vaste paletten 6..12, vaste seed); geen bronsheets van anderen.
"""
import os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
from tilelib import Canvas, Tileset, ellipse_mask, palette_strip, render_repo_map, side_by_side, Prim, budget

OUT = 'tilesets/eigen/altiplano'
random.seed(3812)  # hoogte van het Titicacameer

# ------------------------------------------------------------------ paletten
# 6 grond: goudgele aarde, weg, bofedal (veen) en water
OL6 = (88, 56, 32)
SO = [(160, 112, 56), (200, 152, 80), (224, 184, 112), (240, 216, 152)]   # aarde donker..licht
RO = [(168, 128, 96), (200, 168, 128), (224, 200, 160)]                   # weg (lichter, grijzer)
DG = (184, 168, 72)                                                       # droog grassprietje
BO = [(56, 104, 64), (96, 144, 72), (144, 176, 96)]                       # bofedal
WA = [(56, 96, 160), (96, 144, 208), (168, 208, 240)]                     # water
P6 = [OL6] + SO + RO + [DG] + BO + WA
# 7 ichu en struiken
OL7 = (80, 64, 24)
IC = [(144, 112, 32), (192, 160, 56), (224, 200, 96), (248, 232, 160)]    # ichu donker..punt
TO = [(64, 88, 48), (104, 128, 64), (152, 160, 80)]                       # tola-struik
YA = [(56, 136, 64), (112, 184, 72)]                                      # yareta (kussenplant)
FW = (216, 104, 168)                                                      # klein bloempje (cantuta-roze)
P7 = [OL7] + IC + TO + YA + [FW]
# 8 steen: rotsen, pirca-muurtjes, apacheta, korstmos, hout van de kraal
OL8 = (48, 40, 40)
STN = [(104, 96, 88), (144, 136, 120), (184, 176, 160), (216, 208, 192)]
LO, LG = (224, 152, 48), (160, 176, 96)                                   # korstmos oranje/groen
WOOD = [(104, 72, 40), (152, 112, 64)]
P8 = [OL8] + STN + [LO, LG] + WOOD
# 9 adobe en strodak
OL9 = (64, 40, 24)
AD = [(136, 80, 48), (176, 120, 72), (208, 160, 104), (232, 200, 152)]
TH = [(152, 112, 40), (200, 160, 64), (232, 208, 112)]
DR = [(88, 56, 32), (64, 96, 160)]                                        # houten deur, blauw geverfd
WIN = (40, 32, 40)
P9 = [OL9] + AD + TH + DR + [WIN]
# 10 queñua
OL10 = (56, 32, 24)
BK = [(112, 48, 32), (168, 80, 48), (216, 128, 80), (240, 184, 136)]      # schilferbast
LF = [(40, 72, 56), (72, 112, 72), (120, 152, 88), (168, 184, 120)]       # klein donker blad
P10 = [OL10] + BK + LF
# 11 verre bergen
OLN = (48, 48, 80)
SN = [(248, 248, 248), (208, 224, 240), (160, 184, 224)]
RK = [(88, 88, 128), (128, 128, 160), (168, 168, 192)]
P11 = [OLN] + SN + RK
P12 = [(0, 0, 8)]  # vrij voor later (bijv. Uyuni-zout, flamingo-lagune)

ts = Tileset([P6, P7, P8, P9, P10, P11, P12])


def ascii_canvas(rows, cmap):
    c = Canvas(len(rows[0]), len(rows))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if cmap.get(ch) is not None:
                c.px(x, y, cmap[ch])
    return c


# ------------------------------------------------------------------ grond
def soil(var=0):
    """Goudgele hoogvlakte-aarde, rustig met wat korrels en droge sprietjes."""
    c = Canvas(16, 16, SO[2])
    rnd = random.Random(40 + var)
    for _ in range(4):
        x, y = rnd.randrange(15), rnd.randrange(16)
        c.px(x, y, SO[1]); c.px(x + 1, y, SO[3])
    if var >= 1:
        for _ in range(3 + var):
            x, y = rnd.randrange(14), rnd.randrange(2, 16)
            c.px(x, y, DG); c.px(x + 1, y - 1, DG); c.px(x + 2, y, SO[1])
    if var == 3:  # kiezels
        for x, y in ((4, 5), (11, 11), (7, 13)):
            c.px(x, y, RO[2]); c.px(x + 1, y, RO[1]); c.px(x, y + 1, SO[1])
    return c


def road_tex(x, y):
    """Onverharde weg: licht, met twee wielsporen (horizontale weg) en grind."""
    col = RO[2]
    if (x * 7 + y * 3) % 23 == 0:
        col = RO[1]
    if (x * 5 + y * 11) % 31 == 0:
        col = SO[3]
    return col


def bof_tex(x, y, var=0):
    """Bofedal: drassig kussenveen (bulten met licht linksboven) met hier en daar een poeltje."""
    px, py = x % 16, y % 16
    bx, by = (px + (py // 4) * 2) % 4, py % 4
    col = BO[1]
    if bx == 0 and by == 0:
        col = BO[2]
    if bx == 3 and by == 3:
        col = BO[0]
    pools = [(9, 7, 40)] if var == 0 else ([(5, 10, 26), (12, 4, 14)] if var == 1 else [])
    for cx, cy, r in pools:
        d = (px - cx) ** 2 + (py - cy) ** 2 * 2
        if d < r:
            col = WA[1] if py >= cy else WA[2]
        elif d < r + 8 and py < cy:
            col = BO[0]
    return col


AUTO = ['tl', 't', 'tr', 'l', 'c', 'r', 'bl', 'b', 'br', 'in_tl', 'in_tr', 'in_bl', 'in_br']


def patch(kind, tex, edge_light, edge_dark, outside):
    """Autotile-stuk: binnen = tex, buiten = outside-canvas; afgeronde randen met 1 px omlijning."""
    c = Canvas(16, 16)
    inside = np.ones((16, 16), bool)
    for y in range(16):
        for x in range(16):
            ins = True
            if 't' in kind[:1] and not kind.startswith('in') and y < 4:
                ins = False
            if kind[:1] == 'b' and y > 11:
                ins = False
            if kind in ('l', 'tl', 'bl') and x < 4:
                ins = False
            if kind in ('r', 'tr', 'br') and x > 11:
                ins = False
            if kind == 't' or kind == 'b':
                pass
            # afgeronde buitenhoek
            if kind == 'tl' and (x - 4) + (y - 4) < 1:
                ins = False
            if kind == 'tr' and (11 - x) + (y - 4) < 1:
                ins = False
            if kind == 'bl' and (x - 4) + (11 - y) < 1:
                ins = False
            if kind == 'br' and (11 - x) + (11 - y) < 1:
                ins = False
            # binnenhoek: buitenmateriaal steekt in de hoek
            if kind == 'in_tl' and x + y < 4:
                ins = False
            if kind == 'in_tr' and (15 - x) + y < 4:
                ins = False
            if kind == 'in_bl' and x + (15 - y) < 4:
                ins = False
            if kind == 'in_br' and (15 - x) + (15 - y) < 4:
                ins = False
            inside[y, x] = ins
    for y in range(16):
        for x in range(16):
            if inside[y, x]:
                c.px(x, y, tex(x, y))
            else:
                c.px(x, y, outside.get(x, y))
    # omlijning: buitenpixels die aan binnen grenzen
    for y in range(16):
        for x in range(16):
            if inside[y, x]:
                continue
            nb = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            if any(0 <= a < 16 and 0 <= b < 16 and inside[b, a] for a, b in nb):
                below = 0 <= y - 1 and inside[y - 1, x]
                right = 0 <= x - 1 and inside[y, x - 1]
                c.px(x, y, edge_dark if (below or right) else edge_light)
    return c


SOIL = soil(0)
for i in range(4):
    ts.add(f'soil{i}', soil(i))
for k in AUTO:
    ts.add(f'road_{k}', patch(k, road_tex, SO[1], SO[0], SOIL))
for k in AUTO:
    ts.add(f'bofedal_{k}', patch(k, lambda x, y: bof_tex(x, y, 2), BO[0], OL6, SOIL))
ts.add('bofedal_pool', patch('c', lambda x, y: bof_tex(x, y, 0), BO[0], OL6, SOIL))
ts.add('bofedal_pool2', patch('c', lambda x, y: bof_tex(x, y, 1), BO[0], OL6, SOIL))


# ------------------------------------------------------------------ ichu en planten (palet 7, boven de aarde)
def _line(c, x0, y0, x1, y1, col_fn):
    n = int(max(abs(x1 - x0), abs(y1 - y0), 1) + 0.5)
    for i in range(n + 1):
        t = i / n
        x, y = round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t)
        c.px(x, y, col_fn(t))


def ichu_clump(c, x0, y0, size=1.0, rnd=None):
    """Pol ichu: een waaier van taaie sprieten vanuit één voet, punten naar buiten gebogen;
    licht links, schaduw rechts, donkere voet."""
    h = 9 * size
    cx, by = x0 + 4 * size, y0 + h
    tips = [(-4.5, 0.55), (-3.5, 0.85), (-2.2, 1.0), (-1, 0.9), (0.3, 1.05), (1.5, 0.95), (2.7, 0.9), (3.8, 0.7),
            (4.6, 0.45)]
    for dx, hh in tips:
        tx, ty = cx + dx * size, by - h * hh
        right = dx > 0.5

        def col(t, right=right):
            if t > 0.85:
                return IC[3] if not right else IC[2]
            if t > 0.45:
                return IC[2] if not right else IC[1]
            return IC[1] if t > 0.2 else IC[0]
        _line(c, cx + dx * 0.3, by, tx, ty, col)
    c.hline(round(cx - 2 * size), round(cx + 2 * size), round(by), IC[0])
    c.hline(round(cx - 2 * size) + 1, round(cx + 2 * size) - 1, round(by) + 1, OL7)


def ichu_grass():
    """Hoog gras van de hoogvlakte: dichte ichu-pollen (gedrag tall grass)."""
    c = Canvas(16, 16)
    ichu_clump(c, -1, -3, 0.85)
    ichu_clump(c, 8, -2, 0.85)
    ichu_clump(c, 3, 4, 0.95)
    ichu_clump(c, 11, 5, 0.8)
    return c


def ichu_single():
    c = Canvas(16, 16)
    ichu_clump(c, 3, 1, 1.2)
    return c


def ichu_big():
    """Grote ichu-pol (2 x 2), blokkerend decor."""
    c = Canvas(32, 32)
    for (x, y, s) in ((1, 6, 1.3), (14, 4, 1.4), (7, 12, 1.6), (18, 13, 1.3)):
        ichu_clump(c, x, y, s)
    return c


def tola():
    """Tola-struik: rond, olijfgroen, kort."""
    c = Canvas(16, 16)
    c.mask_fill(ellipse_mask(8, 9, 7, 5.5), TO[1])
    c.mask_fill(ellipse_mask(6.5, 7.5, 4, 3), TO[2])
    for x, y in ((4, 9), (9, 6), (11, 10), (7, 12), (12, 8)):
        c.px(x, y, TO[0])
    for x, y in ((5, 6), (8, 5), (3, 8)):
        c.px(x, y, IC[3])
    c.outline(OL7)
    return c


def yareta():
    """Yareta: felgroene kussenplant op een steen."""
    c = Canvas(16, 16)
    c.mask_fill(ellipse_mask(8, 10, 7, 4.5), YA[0])
    c.mask_fill(ellipse_mask(7, 9, 5, 3), YA[1])
    for x in range(3, 13, 2):
        c.px(x, 8 + (x % 3), YA[0])
    c.outline(OL7)
    return c


def flowers():
    c = Canvas(16, 16)
    for x, y in ((4, 5), (11, 4), (7, 11), (12, 12)):
        c.px(x, y, FW); c.px(x, y + 1, TO[1]); c.px(x - 1, y + 1, TO[2])
    return c


for nm, cv, beh in (('ichu_grass', ichu_grass(), 'MB_TALL_GRASS'), ('ichu', ichu_single(), 'MB_NORMAL'),
                    ('tola', tola(), 'MB_NORMAL'), ('yareta', yareta(), 'MB_NORMAL'), ('flowers', flowers(), 'MB_NORMAL')):
    ts.add(nm, SOIL, cv, beh=beh, layer='covered')
    ts.add(nm + '_b', soil(1), cv, beh=beh, layer='covered')


def slice_obj(name, cv, ground=SOIL, top_rows=(), beh=None):
    ids = []
    for my in range(cv.h // 16):
        row = []
        for mx in range(cv.w // 16):
            s = cv.sub(mx * 16, my * 16, 16, 16)
            if not s.a[:, :, 3].any():
                row.append(None)
                continue
            nm = f'{name}_{mx}_{my}'
            b = (beh or {}).get((mx, my), 'MB_NORMAL')
            if s.a[:, :, 3].all() and my not in top_rows:
                row.append(ts.add(nm, s, beh=b))
            else:
                row.append(ts.add(nm, ground, s, beh=b, layer='normal' if my in top_rows else 'covered'))
        ids.append(row)
    return ids


def ledge(piece):
    """Lage richel in de aarde (springen naar het zuiden): rand met licht en schaduw."""
    c = Canvas(16, 16)
    c.paste(soil(0), 0, 0)
    c.hline(0, 15, 9, SO[3]); c.hline(0, 15, 10, SO[1]); c.hline(0, 15, 11, SO[0]); c.hline(0, 15, 12, OL6)
    c.hline(0, 15, 13, SO[1])
    for x in (3, 10):
        c.px(x, 11, SO[1]); c.px(x + 1, 10, SO[0])
    if piece == 'l':
        for y in range(9, 14):
            c.px(0, y, SO[2])
        c.px(1, 9, SO[2]); c.px(1, 13, SO[2])
    if piece == 'r':
        for y in range(9, 14):
            c.px(15, y, SO[2])
        c.px(14, 9, SO[2]); c.px(14, 13, SO[2])
    return c


for p_ in ('l', 'm', 'r'):
    ts.add(f'ledge_{p_}', ledge(p_), beh='MB_JUMP_SOUTH')

OBJ = {}
OBJ['ichu_big'] = slice_obj('ichu_big', ichu_big(), top_rows=(0,))


# ------------------------------------------------------------------ steen (palet 8)
def stone(c, x0, y0, w, h, lichen=None):
    """Eén ronde steen met licht linksboven."""
    for y in range(h):
        for x in range(w):
            if (x in (0, w - 1)) and (y in (0, h - 1)):
                continue
            col = STN[2]
            if y == 0 or x == 0:
                col = STN[3]
            if y == h - 1 or x == w - 1:
                col = STN[1]
            if y == h - 1 and x == w - 1:
                col = STN[0]
            c.px(x0 + x, y0 + y, col)
    if lichen and w > 3 and h > 2:
        c.px(x0 + 2, y0 + 1, lichen); c.px(x0 + 3, y0 + 1, lichen)


def rock_small():
    c = Canvas(16, 16)
    stone(c, 3, 6, 10, 7, LO)
    stone(c, 9, 10, 5, 4)
    c.outline(OL8)
    return c


def boulder():
    """Kei (2 x 2) met korstmos."""
    c = Canvas(32, 32)
    m = ellipse_mask(16, 17, 14, 12)
    for y in range(32):
        for x in range(32):
            if m(x, y):
                dx, dy = (x - 16) / 14, (y - 17) / 12
                t = dx + dy
                col = STN[3] if t < -0.7 else (STN[2] if t < 0.1 else (STN[1] if t < 0.8 else STN[0]))
                c.px(x, y, col)
    for x, y in ((9, 8), (10, 8), (11, 9), (20, 12), (21, 12), (14, 20)):
        c.px(x, y, LO)
    for x, y in ((7, 14), (8, 14), (24, 20)):
        c.px(x, y, LG)
    c.hline(10, 18, 18, STN[1]); c.px(19, 19, STN[0])  # breuklijn
    c.outline(OL8)
    return c


def rock_hill():
    """Lage rotsheuvel (4 x 3): brokken in Hoenn-stijl, plat bovenop met aarde ertussen."""
    c = Canvas(64, 48)
    lumps = [(10, 22, 9, 8), (24, 16, 10, 9), (40, 15, 11, 9), (54, 22, 9, 8), (17, 34, 10, 8), (33, 32, 11, 9),
             (48, 34, 10, 8)]
    for y in range(48):
        for x in range(64):
            best = None
            for cx, cy, rx, ry in lumps:
                dx, dy = (x + .5 - cx) / rx, (y + .5 - cy) / ry
                d = dx * dx + dy * dy
                if d <= 1 and (best is None or d < best[0]):
                    best = (d, dx, dy)
            if best:
                d, dx, dy = best
                t = dx + dy
                col = STN[3] if t < -0.6 else (STN[2] if t < 0.2 else (STN[1] if t < 0.9 else STN[0]))
                if d > 0.75 and t > 0.3:
                    col = STN[0]
                c.px(x, y, col)
    for x, y in ((18, 11), (19, 11), (38, 9), (39, 9), (50, 17)):
        c.px(x, y, LO)
    for x, y in ((28, 26), (45, 27)):
        c.px(x, y, LG)
    c.outline(OL8)
    return c


def pirca(kind):
    """Pirca: droge stapelmuur. h = horizontaal (oost-west), v = verticaal, hoeken en uiteinden.
    3/4-aanzicht: bovenkant (lichte stenen) en voorkant (2 lagen stenen) bij horizontale stukken."""
    c = Canvas(16, 16)
    if kind in ('h', 'h_l', 'h_r', 'gate_l', 'gate_r'):
        x0 = 3 if kind in ('h_l',) else 0
        x1 = 12 if kind in ('h_r',) else 15
        # bovenkant
        for i, (sx, w) in enumerate(((0, 5), (5, 6), (11, 5))):
            stone(c, sx, 3, w, 3)
        # voorkant: twee lagen
        for (sx, w) in ((-2, 6), (4, 5), (9, 7), (16, 5)):
            stone(c, sx, 6, w, 4)
        for (sx, w) in ((0, 5), (5, 6), (11, 5)):
            stone(c, sx, 10, w, 3)
        for y in range(16):
            for x in range(16):
                if not x0 <= x <= x1:
                    c.px(x, y, None)
        for x in range(x0, x1 + 1):
            if c.get(x, 12) is not None:
                c.px(x, 13, OL8)
    if kind in ('v', 'v_t', 'v_b'):
        y0 = 4 if kind == 'v_t' else 0
        for (sy, h) in ((0, 4), (4, 5), (9, 3), (12, 4)):
            if sy + h <= y0:
                continue
            stone(c, 3, max(sy, y0), 5, min(h, sy + h - y0))
            stone(c, 8, max(sy + 1, y0), 5, min(h, sy + h - y0))
        if kind == 'v_b':
            for (sx, w) in ((3, 5), (8, 5)):
                stone(c, sx, 12, w, 3)
    if kind in ('c_tl', 'c_tr', 'c_bl', 'c_br'):
        # hoek = halve horizontale + halve verticale
        hz = pirca('h_l' if kind[2] == 'l' else 'h_r')
        vt = pirca('v_b' if kind[0:3] in ('c_b',) else 'v_t')
        if kind in ('c_tl', 'c_tr'):
            c.paste(hz, 0, 0)
            for y in range(13, 16):
                for x in range(16):
                    v = vt.get(x, y)
                    if v:
                        c.px(x, y, v)
        else:
            for y in range(0, 4):
                for x in range(16):
                    v = vt.get(x, y)
                    if v:
                        c.px(x, y, v)
            c.paste(hz, 0, 0)
    c.outline(OL8)
    return c


def gate():
    """Houten poort van de lamakraal: twee palen met dwarsliggers."""
    c = Canvas(16, 16)
    for x in (1, 13):
        c.rect(x, 1, x + 1, 13, WOOD[1]); c.vline(x + 1, 1, 13, WOOD[0])
    for y in (4, 8):
        c.rect(1, y, 14, y + 1, WOOD[1]); c.hline(1, 14, y + 1, WOOD[0])
    c.outline(OL8)
    return c


def apacheta():
    """Apacheta: stapel stenen op een pas, offerplek voor reizigers (1 x 2)."""
    c = Canvas(16, 32)
    rows = [(6, 4, 4), (5, 8, 6), (4, 12, 8), (3, 17, 10), (2, 22, 12)]
    for sx, sy, w in rows:
        for k in range(0, w, 4):
            stone(c, sx + k, sy, min(4, w - k) + 1, 5, LO if (sy + k) % 3 == 0 else None)
    c.outline(OL8)
    return c


ts.add('rock', SOIL, rock_small())
OBJ['boulder'] = slice_obj('boulder', boulder(), top_rows=())
OBJ['rockhill'] = slice_obj('rockhill', rock_hill(), top_rows=(0,))
PIRCA = {}
for k in ('h', 'h_l', 'h_r', 'v', 'v_t', 'v_b', 'c_tl', 'c_tr', 'c_bl', 'c_br'):
    PIRCA[k] = ts.add(f'pirca_{k}', SOIL, pirca(k))
PIRCA['gate'] = ts.add('pirca_gate', SOIL, gate())
OBJ['apacheta'] = slice_obj('apacheta', apacheta(), top_rows=(0,))


# ------------------------------------------------------------------ adobe en strodak (palet 9)
def thatch(piece, row):
    """Strodak (voorhelling, 2 rijen): sprieten in bundels, nok bovenaan, rafelige dakrand."""
    c = Canvas(16, 16)
    for y in range(16):
        for x in range(16):
            k = (x + (y // 4) * 2) % 4
            col = [TH[2], TH[1], TH[1], TH[0]][k]
            if (y % 4) == 3 and k == 1:
                col = TH[0]
            c.px(x, y, col)
    if row == 0:
        c.rect(0, 0, 15, 3, TH[0]); c.hline(0, 15, 0, OL9); c.hline(0, 15, 1, TH[2]); c.hline(0, 15, 3, OL9)
        for x in range(0, 16, 4):  # nokbinding
            c.px(x + 1, 2, AD[0]); c.px(x + 2, 2, AD[0])
    else:
        # rafelige onderrand
        for x in range(16):
            yy = 11 + (1 if x % 3 == 0 else 0) + (1 if x % 5 == 2 else 0)
            c.px(x, yy, TH[2])
            for y in range(yy + 1, 16):
                c.px(x, y, None)
            c.px(x, yy + 1, OL9)
        for x in range(16):
            for y in range(13, 16):
                if c.get(x, y) is None:
                    c.px(x, y, AD[0])  # schaduw onder de dakrand op de muur
    if piece == 'l':
        for y in range(16):
            c.px(0, y, OL9 if c.get(0, y) not in (AD[0],) else OL9)
            if c.get(1, y) in TH:
                c.px(1, y, TH[2])
    if piece == 'r':
        for y in range(16):
            c.px(15, y, OL9)
            if c.get(14, y) in TH:
                c.px(14, y, TH[0])
    return c


def adobe_wall(piece, row):
    """Adobe-muur (2 rijen): grote leemblokken, gepleisterde onderrand; stukken l/m/r/door/win."""
    c = Canvas(16, 16)
    for y in range(16):
        for x in range(16):
            yy = (y + row * 16)
            r = yy // 5
            bx = (x + (r % 2) * 5) % 10
            col = AD[2]
            if yy % 5 == 4 or bx == 9:
                col = AD[1]
            elif yy % 5 == 0 and bx < 6:
                col = AD[3]
            c.px(x, y, col)
    if row == 1:
        c.rect(0, 12, 15, 14, AD[1]); c.hline(0, 15, 12, AD[3]); c.hline(0, 15, 15, OL9)
    if piece == 'l':
        c.vline(0, 0, 15, OL9); c.vline(1, 0, 14, AD[3])
    if piece == 'r':
        c.vline(15, 0, 15, OL9); c.vline(14, 0, 14, AD[0])
    if piece == 'door':
        if row == 0:
            c.rect(3, 6, 12, 15, OL9); c.rect(4, 7, 11, 15, DR[1])
            c.hline(3, 12, 5, WIN)
            for x in (6, 9):
                c.vline(x, 7, 15, DR[0])
        else:
            c.rect(3, 0, 12, 14, OL9); c.rect(4, 0, 11, 13, DR[1])
            for x in (6, 9):
                c.vline(x, 0, 13, DR[0])
            c.px(10, 4, AD[3]); c.hline(3, 12, 14, AD[0])
    if piece == 'win' and row == 0:
        c.rect(5, 7, 10, 11, WIN); c.box(4, 6, 11, 12, OL9); c.vline(7, 7, 11, DR[0]); c.vline(8, 7, 11, DR[0])
        c.hline(4, 11, 13, AD[3])
    return c


for row in (0, 1):
    for p in ('l', 'm', 'r'):
        ts.add(f'thatch{row}_{p}', thatch(p, row))
    for p in ('l', 'm', 'r', 'door', 'win'):
        ts.add(f'adobe{row}_{p}', adobe_wall(p, row))


def round_hut():
    """Rond voorraadhuisje (2 x 3) met kegeldak van stro."""
    c = Canvas(32, 48)
    for y in range(2, 30):  # kegeldak
        half = 3 + (y - 2) * 12 // 27
        for x in range(16 - half, 16 + half):
            k = (x - 16) * 4 // max(1, half)
            col = TH[2] if x < 13 else (TH[1] if x < 20 else TH[0])
            if (x + y) % 5 == 0:
                col = TH[0] if col != TH[0] else TH[1]
            c.px(x, y, col)
    for x in range(1, 31):  # rafelrand
        c.px(x, 30 + (x % 3 == 0), TH[2])
    c.rect(4, 31, 27, 45, AD[2])
    for y in range(31, 46):
        for x in range(4, 28):
            if (y - 31) % 5 == 4:
                c.px(x, y, AD[1])
            if x < 8:
                c.px(x, y, AD[3] if (y - 31) % 5 != 4 else AD[2])
            if x > 23:
                c.px(x, y, AD[1] if (y - 31) % 5 != 4 else AD[0])
    for x in range(4, 28):
        c.px(x, 31, AD[0]); c.px(x, 32, AD[0])
    c.rect(13, 36, 18, 45, WIN); c.rect(14, 37, 17, 45, DR[0])
    c.outline(OL9)
    return c


OBJ['hut'] = slice_obj('hut', round_hut(), top_rows=(0, 1))


# ------------------------------------------------------------------ queñua (palet 10)
def quenua(big=True):
    """Queñua (Polylepis): kronkelige stammen met rode schilferbast, kleine donkere bladtrossen."""
    W_, H_ = (32, 48) if big else (16, 32)
    c = Canvas(W_, H_)
    rnd = random.Random(7 if big else 8)
    # stammen
    trunks = ([(13, 46, -1), (17, 46, 1), (15, 46, 0)] if big else [(7, 30, 0)])
    for x0, y0, lean in trunks:
        x = x0
        for y in range(y0, (14 if big else 10), -1):
            if (y0 - y) % 4 == 3:
                x += rnd.choice((lean, lean, -lean, 0)) if lean else rnd.choice((-1, 1, 0))
            w = 3 if (y0 - y) < (14 if big else 8) else 2
            for k in range(w):
                col = BK[2] if k == 0 else (BK[1] if k < w - 1 else BK[0])
                if (y + k) % 7 == 0:
                    col = BK[3]  # schilfers
                c.px(x + k, y, col)
    # bladtrossen
    blobs = ([(8, 12, 7, 5), (22, 11, 8, 5), (15, 6, 8, 5), (6, 21, 5, 4), (25, 20, 5, 4), (15, 17, 6, 4)]
             if big else [(8, 8, 7, 5), (5, 14, 4, 3), (11, 13, 4, 3)])
    for cx, cy, rx, ry in blobs:
        c.mask_fill(ellipse_mask(cx, cy, rx, ry), LF[1])
    for cx, cy, rx, ry in blobs:
        c.mask_fill(ellipse_mask(cx - 1.5, cy - 1.5, rx - 2.5, ry - 2), LF[2])
    for cx, cy, rx, ry in blobs:
        for _ in range(int(rx * ry / 3)):
            x, y = cx + rnd.randint(-rx + 1, rx - 1), cy + rnd.randint(-ry + 1, ry - 1)
            if c.get(x, y) in (LF[1], LF[2]):
                c.px(x, y, LF[0] if (x + y) % 2 else LF[3] if c.get(x, y) == LF[2] else LF[0])
    # stammen tussen de trossen door laten zien
    for x0, y0, lean in trunks:
        pass
    c.outline(OL10)
    return c


OBJ['quenua'] = slice_obj('quenua', quenua(True), top_rows=(0, 1))
OBJ['quenua_s'] = slice_obj('quenua_s', quenua(False), top_rows=(0,))


# ------------------------------------------------------------------ verre bergen (palet 11)
def far_range():
    """Verre besneeuwde bergketen (4 x 3, naadloos), hellingen van 45 graden, twee hoogtes."""
    W_, H_ = 64, 48
    c = Canvas(W_, H_)
    peaks = [(16, 10), (44, 18)]
    for x in range(W_):
        top = min(py + min(abs(x - px_), W_ - abs(x - px_)) for px_, py in peaks)
        px_, py = min(peaks, key=lambda p: p[1] + min(abs(x - p[0]), W_ - abs(x - p[0])))
        left = (x - px_) % W_ > W_ // 2 or x == px_ - 0
        left = ((x - px_) % W_) >= W_ // 2
        for y in range(H_):
            if y < top:
                col = SN[1]
            elif y == top:
                col = OLN
            elif y < top + 10 + ((x // 4) % 2) * 2:
                col = SN[0] if left else SN[2]
            else:
                col = RK[2] if left else RK[1]
                if (x - y) % 16 == 0:
                    col = RK[1] if left else RK[0]
            if y > 44:
                col = None
            elif y == 44:
                col = OLN
            c.px(x, y, col)
    return c


FR = far_range()
ids = []
for my in range(3):
    row = []
    for mx in range(4):
        s_ = FR.sub(mx * 16, my * 16, 16, 16)
        nm = f'range_{mx}_{my}'
        row.append(ts.add(nm, s_) if s_.a[:, :, 3].all() else ts.add(nm, SOIL, s_, layer='covered'))
    ids.append(row)
OBJ['range'] = ids

# ------------------------------------------------------------------ mock-up
N = ts.names


def put(g, x, y, ids):
    for dy, row in enumerate(ids):
        for dx, m in enumerate(row):
            if m is not None and 0 <= y + dy < len(g) and 0 <= x + dx < len(g[0]):
                g[y + dy][x + dx] = m


def area(g, x0, y0, x1, y1, prefix):
    """Autotile-vlak (inclusief randen) van x0..x1, y0..y1."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            k = ('t' if y == y0 else 'b' if y == y1 else '') + ('l' if x == x0 else 'r' if x == x1 else '')
            k = {'': 'c', 't': 't', 'b': 'b', 'l': 'l', 'r': 'r', 'tl': 'tl', 'tr': 'tr', 'bl': 'bl', 'br': 'br'}[k]
            g[y][x] = N[f'{prefix}_{k}']
            if prefix == 'bofedal' and k == 'c' and (x * 3 + y) % 4 in (0, 1):
                g[y][x] = N['bofedal_pool' if (x + y) % 2 else 'bofedal_pool2']


def adobe_house(g, x, y, w, door=1):
    rows = [[f'thatch0_l'] + ['thatch0_m'] * (w - 2) + ['thatch0_r'],
            [f'thatch1_l'] + ['thatch1_m'] * (w - 2) + ['thatch1_r']]
    for r in (0, 1):
        row = [f'adobe{r}_l'] + [f'adobe{r}_m'] * (w - 2) + [f'adobe{r}_r']
        row[door] = f'adobe{r}_door'
        if w > 3:
            row[w - 2] = f'adobe{r}_win' if r == 0 else f'adobe{r}_m'
        rows.append(row)
    put(g, x, y, [[N[n] for n in r] for r in rows])


def mockup():
    Wm, Hm = 30, 20
    rnd = random.Random(99)
    g = [[N['soil%d' % (0 if rnd.random() < .55 else rnd.choice((1, 2, 3)))] for _ in range(Wm)] for _ in range(Hm)]
    for x in range(0, Wm, 4):
        put(g, x, 0, OBJ['range'])
    # weg: van links naar rechts, buigt naar beneden
    area(g, 0, 9, 17, 10, 'road')
    for y in range(11, 20):
        g[y][16] = N['road_l']; g[y][17] = N['road_r']
    g[10][16] = N['road_in_bl']
    # boerderijtje met pirca-muur
    for x in range(2, 12):
        g[3][x] = N['pirca_h']; g[8][x] = N['pirca_h']
    for y in range(4, 8):
        g[y][2] = N['pirca_v']; g[y][11] = N['pirca_v']
    g[3][2] = N['pirca_c_tl']; g[3][11] = N['pirca_c_tr']; g[8][2] = N['pirca_c_bl']; g[8][11] = N['pirca_c_br']
    adobe_house(g, 3, 4, 4)
    put(g, 8, 5, OBJ['hut'])
    g[8][5] = N['pirca_gate']
    # lamakraal (rond = rechthoek met poort)
    for x in range(20, 27):
        g[11][x] = N['pirca_h']; g[15][x] = N['pirca_h']
    for y in range(12, 15):
        g[y][19] = N['pirca_v']; g[y][27] = N['pirca_v']
    g[11][19] = N['pirca_c_tl']; g[11][27] = N['pirca_c_tr']; g[15][19] = N['pirca_c_bl']; g[15][27] = N['pirca_c_br']
    g[11][19] = N['pirca_c_tl']
    g[13][19] = N['pirca_gate']
    # ichu-velden (hoog gras)
    for (x0, y0, x1, y1) in ((1, 11, 9, 17), (19, 4, 28, 7), (22, 17, 29, 19)):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if rnd.random() < 0.85:
                    g[y][x] = N['ichu_grass' if (x + y) % 3 else 'ichu_grass_b']
    # bofedal met poeltjes
    area(g, 10, 13, 14, 17, 'bofedal')
    # rotsen en queñua-bosje tegen een rotsheuvel
    put(g, 25, 8, OBJ['rockhill'])
    put(g, 23, 1, OBJ['quenua']) if False else None
    put(g, 12, 3, OBJ['quenua'])
    put(g, 14, 4, OBJ['quenua_s'])
    put(g, 28, 9, OBJ['quenua_s'])
    put(g, 20, 8, OBJ['boulder'])
    put(g, 12, 18, OBJ['ichu_big'])
    for x in range(18, 30):
        g[3][x] = N['ledge_m']
    g[3][18] = N['ledge_l']
    put(g, 13, 7, OBJ['apacheta'])
    for (x, y, n) in ((0, 8, 'rock'), (7, 12, 'tola'), (12, 11, 'tola_b'), (9, 18, 'yareta'), (1, 19, 'flowers'),
                      (24, 16, 'ichu'), (5, 11, 'ichu_b'), (28, 16, 'rock'), (19, 18, 'tola'), (1, 5, 'tola')):
        g[y][x] = N[n]
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
ref = render_repo_map('Route111', 62, 82, 0, 30)
side_by_side(img, ref, OUT + '/vergelijking.png')
print('tegels', len(ts.tiles), '/ 512   metatiles', len(ts.mts), '/ 512')
if ts.errors:
    from collections import Counter
    print('kleur benaderd:', Counter(str(e) for e in ts.errors).most_common(10))
GROUPS = ['ledge', 'soil', 'road', 'bofedal', 'ichu', 'tola', 'yareta', 'flowers', 'rockhill', 'rock', 'boulder', 'pirca', 'apacheta',
          'thatch', 'adobe', 'hut', 'quenua', 'range']
for k, v in budget(ts, GROUPS).items():
    print(f'  {k:12s} {v}')
