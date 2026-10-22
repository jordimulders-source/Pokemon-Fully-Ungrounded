#!/usr/bin/env python3
"""Altiplano, ronde 2: secondary op de Andes-primary, gebouwd op de Fallarbor-tegels (Route 113/114).

Basis (omgekleurd, tegels 1-op-1 overgenomen uit de Fallarbor-secondary):
- huis van Route 114 (x28-31, y2-5) -> adobe-huis met strodak;
- bolle boom van Route 114 (x32-33, y3-4) -> queñua (donker blad, rode schilferbast);
- gelaagde klifwand van Route 114 -> roodbruine rotswand;
- akker van Route 114 -> aardappelakker (chacra);
- asgrond en asgras van Route 113 -> droge puna en paja brava; de richels van Route 113;
- oranje pad van Route 114 -> onverharde weg.
Uit de Andes-primary: puna-grond, ichu (hoog gras), bergketen, rotsen, bloemen, water.
Zelf getekend (Hoenn-stijl, bestaande paletten): pirca-muurtjes en lamakraal, apacheta, rond voorraadhuisje,
bofedal (veen) met poeltjes.

Gebruik: python3 tools/concept/tiles/altiplano_r2.py  ->  tilesets/eigen/altiplano/ronde2/
"""
import json, os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
from r2lib import load_set, recolor, Canvas, comparison
from andes_primary import build, PUNA, CLAY
from tilelib import ellipse_mask, render_repo_map

OUT = 'tilesets/eigen/altiplano/ronde2'
pair = build()
P = pair.pals
fal = load_set('secondary', 'fallarbor')
F = [[tuple(int(v) for v in c) for c in fal['pals'][i]] for i in range(16)]

BARK = [(232, 176, 120), (200, 136, 88), (168, 104, 64), (120, 72, 48), (72, 40, 24)]
LEAF = [(168, 200, 120), (104, 152, 88), (56, 104, 64), (32, 56, 32)]
TREE = {1: LEAF[0], 2: LEAF[1], 3: LEAF[2], 4: LEAF[3], 5: PUNA[0], 6: PUNA[2], 7: PUNA[3],
        9: BARK[0], 10: BARK[1], 11: BARK[2], 12: BARK[3], 13: BARK[4], 14: CLAY[4], 15: CLAY[5]}
P[6] = recolor(F[6], TREE)
P[9] = recolor(F[9], TREE)
P[7] = recolor(F[7], {1: (240, 208, 168), 2: (216, 168, 120), 3: (184, 128, 88), 4: (144, 96, 64),       # adobe
                      11: (248, 224, 128), 12: (224, 184, 80), 13: (192, 144, 56), 14: (144, 104, 40),  # stro
                      9: (64, 112, 176), 10: (120, 168, 224), 15: PUNA[1]})
P[8] = recolor(F[8], {1: (248, 232, 184), 2: (232, 208, 152), 3: (208, 176, 120), 4: (184, 144, 96),
                      9: CLAY[0], 10: CLAY[1], 11: CLAY[2], 12: CLAY[3], 13: CLAY[4], 14: CLAY[5]})
DRY = [(240, 224, 176), (216, 200, 144), (192, 168, 112), (168, 144, 96), (136, 112, 72), (104, 88, 56)]
P[11] = recolor(F[11], {1: DRY[0], 2: DRY[1], 3: DRY[1], 4: DRY[3], 9: DRY[0], 10: DRY[1], 11: DRY[2],
                        12: DRY[3], 13: DRY[4], 14: DRY[5], 15: PUNA[1]})
# 10: kopie van primary-palet 3 met de rots/grondtinten als puna: grond onder bomen en klifvoeten sluit zo aan
P[10] = recolor(P[3], {9: (248, 240, 184), 10: PUNA[0], 11: PUNA[1], 12: PUNA[2], 13: PUNA[3], 14: (120, 88, 40)})
# 12: bofedal (eigen): veengroen, water, puna voor de geditherde rand
BO = [(56, 96, 56), (80, 136, 72), (120, 176, 88), (168, 208, 112)]
WA = [(65, 90, 189), (82, 106, 213), (139, 164, 222), (222, 230, 238)]
P[12] = [(255, 0, 255), (41, 49, 90)] + BO + WA + [PUNA[0], PUNA[1], PUNA[2], (232, 120, 168), (255, 255, 255),
                                                    (40, 64, 40)]
assert len(P[12]) == 16

GROUND = 0x001
FMAP = {6: 6, 7: 7, 8: 8, 9: 9, 11: 11, 3: 10}
FMAP_CLAY = {6: 6, 7: 7, 8: 8, 9: 9, 11: 11}


def adobify(idx, srcpal):
    """Muurpixels (index 1-4 van Fallarbor-palet 7) -> grote leemblokken (8 x 4, verspringend)."""
    if srcpal != 7:
        return idx
    out = idx.copy()
    for y in range(8):
        for x in range(8):
            if idx[y, x] in (1, 2, 3, 4):
                row, r = y // 4, y % 4
                bx = (x + row * 4) % 8
                out[y, x] = 3 if (r == 3 or bx == 7) else (1 if (r == 0 and bx < 4) else (4 if (r == 2 and bx > 4) else 2))
    return out


HOUSE = []
for y in range(2, 6):
    row = []
    for x in range(28, 32):
        pass
    HOUSE.append(row)
_hg = [[0x344, 0x345, 0x345, 0x346], [0x285, 0x286, 0x286, 0x287], [0x28d, 0x29d, 0x29e, 0x28f],
       [0x295, 0x2a5, 0x2a6, 0x297]]
HOUSE = [[(pair.names.get(f'adobe_{m:03x}') or pair.import_mt(fal, m, FMAP, f'adobe_{m:03x}',
                                                              tilemap=adobify if r >= 2 else None))
          for m in row] for r, row in enumerate(_hg)]
TREE2 = []
for row in ((0x204, 0x205), (0x20c, 0x20d)):
    r = []
    for m in row:
        nm = f'tree_{m:03x}'
        pair.import_mt(fal, m, FMAP, nm + '_src')
        e = pair.sm[pair.names[nm + '_src'] - 512]
        r.append(pair.add_mt(nm, list(pair.ents(GROUND)[:4]) + e[4:], (1 << 12)))
    TREE2.append(r)
for m in (0x31e, 0x269, 0x271, 0x268, 0x270):
    pair.import_mt(fal, m, FMAP, f'fal_{m:03x}')
CLIFF = [[pair.names['fal_31e']] * 4, [pair.names['fal_269']] * 4, [pair.names['fal_269']] * 4,
         [pair.names['fal_271']] * 4]
FIELD = pair.import_region(fal, 'Route114', 33, 6, 36, 9, FMAP_CLAY, 'chacra')
LEDGE = pair.import_region(fal, 'Route113', 20, 4, 26, 5, FMAP, 'fal')
for m in (0x218, 0x20a, 0x2e8, 0x2ea, 0x2f0, 0x2f2, 0x279, 0x21b, 0x21d, 0x225, 0x21e, 0x226, 0x229):
    if f'fal_{m:03x}' not in pair.names:
        pair.import_mt(fal, m, FMAP, f'fal_{m:03x}')
N = pair.names


# ------------------------------------------------------------------ zelf getekend
P3 = P[3]
ST = [P3[1], P3[2], P3[3], P3[4], P3[5]]   # wit..grijs
STO = P3[8]                                # donkere omlijning


def stone(c, x0, y0, w, h, moss=False):
    for y in range(h):
        for x in range(w):
            if (x in (0, w - 1)) and (y in (0, h - 1)):
                continue
            col = ST[2]
            if y == 0 or x == 0:
                col = ST[1]
            if y == h - 1 or x == w - 1:
                col = ST[3]
            if y == h - 1 and x == w - 1:
                col = ST[4]
            c.px(x0 + x, y0 + y, col)
    if moss and w > 4:
        c.px(x0 + 2, y0 + 1, P3[13]); c.px(x0 + 3, y0 + 1, P3[12])


def pirca(kind):
    """Pirca (droge stapelmuur) in Hoenn-stijl: bovenkant + voorkant, donkere omlijning, schaduw op de grond."""
    c = Canvas(16, 16)
    if kind.startswith('h'):
        for sx, w in ((0, 6), (6, 5), (11, 5)):
            stone(c, sx, 3, w, 4, moss=(sx == 6))
        for sx, w in ((-3, 6), (3, 6), (9, 5), (14, 5)):
            stone(c, sx, 7, w, 4)
        for sx, w in ((0, 5), (5, 6), (11, 5)):
            stone(c, sx, 11, w, 3)
        if kind == 'h_l':
            for y in range(16):
                for x in range(0, 3):
                    c.px(x, y, None)
        if kind == 'h_r':
            for y in range(16):
                for x in range(13, 16):
                    c.px(x, y, None)
    else:
        y0 = 4 if kind == 'v_t' else 0
        for sy, h in ((0, 5), (5, 4), (9, 4), (13, 3)):
            if sy + h <= y0:
                continue
            stone(c, 3, max(sy, y0), 6, sy + h - max(sy, y0))
            stone(c, 8, max(sy + 2, y0), 5, sy + h - max(sy + 2, y0) + 1)
    c.outline(STO)
    return c


def gate():
    c = Canvas(16, 16)
    w = [BARK[1], BARK[3]]
    for x in (1, 13):
        c.rect(x, 2, x + 1, 14, w[0]); c.vline(x + 1, 2, 14, w[1])
    for y in (5, 9):
        c.rect(1, y, 14, y + 1, w[0]); c.hline(1, 14, y + 1, w[1])
    c.outline(BARK[4])
    return c


def apacheta():
    c = Canvas(16, 32)
    for sx, sy, w in ((6, 6, 4), (5, 10, 6), (4, 14, 8), (3, 19, 10), (2, 24, 12)):
        for k in range(0, w, 4):
            stone(c, sx + k, sy, min(4, w - k) + 1, 5, moss=((sy + k) % 3 == 0))
    c.px(8, 4, P3[13]); c.px(8, 5, P3[12])  # bloemetje als offer
    c.outline(STO)
    return c


def hut():
    """Rond voorraadhuisje (2 x 3) met kegeldak van stro, in de adobe/stro-kleuren (palet 7)."""
    A, S = [P[7][1], P[7][2], P[7][3], P[7][4]], [P[7][11], P[7][12], P[7][13], P[7][14]]
    c = Canvas(32, 48)
    for y in range(2, 30):
        half = 3 + (y - 2) * 12 // 27
        for x in range(16 - half, 16 + half):
            col = S[0] if x < 13 else (S[1] if x < 19 else S[2])
            if (x + y) % 4 == 0:
                col = S[2] if col != S[2] else S[3]
            c.px(x, y, col)
    for x in range(2, 30):
        c.px(x, 30 + (x % 3 == 0), S[1])
    for y in range(31, 46):
        for x in range(4, 28):
            col = A[0] if x < 8 else (A[3] if x > 24 else A[1])
            if (y - 31) % 5 == 4:
                col = A[2]
            c.px(x, y, col)
    c.hline(4, 27, 31, A[3]); c.hline(4, 27, 32, A[2])
    c.rect(13, 36, 18, 45, P[7][8]); c.rect(14, 37, 17, 45, P[7][14])
    c.outline(P[7][7])
    return c


def bofedal(kind):
    """Bofedal: kussenveen met poeltjes; rand naar de puna met een Hoenn-dither (geen lijn)."""
    c = Canvas(16, 16)
    for y in range(16):
        for x in range(16):
            bx, by = (x + (y // 4) * 2) % 4, y % 4
            col = BO[2]
            if bx == 0 and by == 0:
                col = BO[3]
            elif bx == 3 and by == 3:
                col = BO[1]
            elif (x * 3 + y * 5) % 7 == 0:
                col = BO[1]
            c.px(x, y, col)
    if kind in ('pool', 'pool2'):
        cx, cy, rx, ry = (8, 8, 5.5, 3.5) if kind == 'pool' else (6, 10, 4.5, 3)
        for y in range(16):
            for x in range(16):
                d = ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2
                if d < 1:
                    col = WA[1] if y > cy - 1 else WA[2]
                    if d < 0.35 and y < cy:
                        col = WA[3] if (x + y) % 3 == 0 else WA[2]
                    c.px(x, y, col)
                elif d < 1.5 and y <= cy:
                    c.px(x, y, BO[0])
    # dither-rand (Hoenn): naar buiten toe puna met een tussenkleur
    edges = {'t': lambda x, y: y, 'b': lambda x, y: 15 - y, 'l': lambda x, y: x, 'r': lambda x, y: 15 - x}
    for side in [s for s in ('t', 'b', 'l', 'r') if s in kind.split('_')[-1]] if kind.startswith('e_') else []:
        for y in range(16):
            for x in range(16):
                d = edges[side](x, y)
                if d < 3:
                    c.px(x, y, PUNA[1])
                elif d == 3:
                    c.px(x, y, PUNA[1] if (x + y) % 2 else BO[3])
                elif d == 4:
                    c.px(x, y, BO[3] if (x + y) % 2 else BO[2])
    return c


def slice_drawn(name, cv, pals, ground=GROUND, top_rows=()):
    gb = pair.ents(ground)[:4]
    ids = []
    for my in range(cv.h // 16):
        row = []
        for mx in range(cv.w // 16):
            s = cv.sub(mx * 16, my * 16, 16, 16)
            if not s.a[:, :, 3].any():
                row.append(None)
                continue
            nm = f'{name}_{mx}_{my}'
            if s.a[:, :, 3].all() and my not in top_rows:
                row.append(pair.add_drawn(nm, s, pals=pals))
            else:
                row.append(pair.add_drawn(nm, None, s, pals=pals, bottom_ents=gb,
                                          layer='normal' if my in top_rows else 'covered'))
        ids.append(row)
    return ids


PIRCA = {}
for k in ('h', 'h_l', 'h_r', 'v', 'v_t'):
    PIRCA[k] = slice_drawn(f'pirca_{k}', pirca(k), (3,))[0][0]
PIRCA['gate'] = slice_drawn('pirca_gate', gate(), (6,))[0][0]
OBJ = {'apacheta': slice_drawn('apacheta', apacheta(), (3,), top_rows=(0,)),
       'hut': slice_drawn('hut', hut(), (7,), top_rows=(0, 1))}
BOF = {}
for k in ('c', 'pool', 'pool2', 'e_t', 'e_b', 'e_l', 'e_r', 'e_tl', 'e_tr', 'e_bl', 'e_br'):
    BOF[k] = pair.add_drawn(f'bofedal_{k}', bofedal(k), pals=(12,))


# ------------------------------------------------------------------ mock-up
def put(g, x, y, ids):
    for dy, row in enumerate(ids):
        for dx, m in enumerate(row):
            if m is not None and 0 <= y + dy < len(g) and 0 <= x + dx < len(g[0]):
                g[y + dy][x + dx] = m


def mockup():
    Wm, Hm = 30, 20
    g = [[GROUND] * Wm for _ in range(Hm)]
    for x in range(0, Wm, 4):
        put(g, x, 0, [[N['andes_sky']] * 4] * 2)
        put(g, x, 2, [[N[f'andes_range_{mx}_{my}'] for mx in range(4)] for my in range(3)])
    # droge puna (Route 113-asgrond) als vlakken
    for y in range(14, 20):
        for x in range(18, 24):
            g[y][x] = N['fal_218']
    for y in range(12, 20):
        for x in range(0, 6):
            g[y][x] = N['fal_218']
    # klifwand (Route 114) rechtsboven, met richel (Route 113) eronder
    for x in range(18, 30, 4):
        put(g, x, 5, CLIFF)
    # ichu (hoog gras, primary) en paja brava (Route 113-asgras)
    for (x0, y0, x1, y1, m) in ((1, 13, 5, 18, 0x0D), (19, 15, 22, 18, N['fal_20a']), (7, 15, 12, 19, 0x0D),
                                (24, 14, 29, 19, 0x0D)):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                g[y][x] = m
    # weg (Route 114-pad) van boven naar beneden
    for y in range(5, 20):
        g[y][14] = N['fal_2f0']; g[y][15] = N['fal_2f2']
    g[5][14] = N['fal_2e8']; g[5][15] = N['fal_2ea']
    # boerderijtje: adobe-huis met pirca-erf, rond huisje, akker
    put(g, 2, 6, HOUSE)
    put(g, 7, 7, OBJ['hut'])
    for x in range(1, 11):
        g[5][x] = PIRCA['h']; g[11][x] = PIRCA['h']
    for y in range(6, 11):
        g[y][1] = PIRCA['v']; g[y][10] = PIRCA['v']
    g[5][1] = PIRCA['h_l']; g[5][10] = PIRCA['h_r']; g[11][1] = PIRCA['h_l']; g[11][10] = PIRCA['h_r']
    g[11][4] = PIRCA['gate']
    put(g, 16, 10, FIELD)
    # lamakraal
    for x in range(20, 29):
        g[11][x] = PIRCA['h']; g[13][x] = PIRCA['h']
    g[12][20] = PIRCA['v']; g[12][28] = PIRCA['v']
    g[11][20] = PIRCA['h_l']; g[11][28] = PIRCA['h_r']; g[13][20] = PIRCA['h_l']; g[13][28] = PIRCA['h_r']
    g[13][24] = PIRCA['gate']
    # queñua's
    put(g, 11, 6, TREE2); put(g, 12, 12, TREE2); put(g, 17, 15, TREE2)
    # bofedal met poeltjes
    x0, y0, x1, y1 = 6, 14, 11, 18
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            k = ('t' if y == y0 else 'b' if y == y1 else '') + ('l' if x == x0 else 'r' if x == x1 else '')
            g[y][x] = BOF['e_' + k] if k else BOF[('pool', 'c', 'pool2', 'c')[(x * 3 + y) % 4]]
    put(g, 13, 8, OBJ['apacheta'])
    for (x, y, m) in ((0, 9, 0x004), (12, 4 + 1, 0x004), (17, 18, N['andes_kantuta']), (22, 16, 0x004),
                      (5, 11, N['andes_kantuta']), (29, 10, 0x004), (17, 6, 0xe0), (0, 11, 0xe0), (12, 18, 0xe0),
                      (27, 10, 0xe0)):
        g[y][x] = m
    return g


BASE_ST, BASE_SM = len(pair.st), len(pair.sm)
g = mockup()
os.makedirs(OUT, exist_ok=True)
pair.write(OUT, 'S')
img = pair.render(g)
Image.fromarray(img).save(OUT + '/mockup.png')
Image.fromarray(img).resize((img.shape[1] * 2, img.shape[0] * 2), Image.NEAREST).save(OUT + '/mockup_2x.png')
pair.sheet(list(range(512, 512 + len(pair.sm))), OUT + '/sheet.png')
pair.palette_strip(range(6, 13), OUT + '/paletten.png')
r1 = np.array(Image.open('tilesets/eigen/altiplano/mockup.png').convert('RGB'))
hoenn = render_repo_map('Route113', 0, 20, 10, 40)
for sc in (1, 2):
    comparison([r1, img, hoenn], ['ronde 1', 'ronde 2', 'Hoenn: Route 113'], OUT + f'/vergelijking_{sc}x.png', scale=sc)
print('secondary-tegels', len(pair.st), '/ 512   metatiles', len(pair.sm), '/ 512')
