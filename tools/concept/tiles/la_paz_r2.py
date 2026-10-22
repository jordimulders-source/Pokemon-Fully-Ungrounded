#!/usr/bin/env python3
"""La Paz, ronde 2: secondary op de Andes-primary, gebouwd op Hoenn-tegels.

Basis (omgekleurd, tegels 1-op-1 overgenomen):
- huizen: het Mauville-huis met golfplaatdak (MauvilleCity x18-21, y11-14; Mauville-palet 7) in drie kleuren
  (baksteen/zink, oker/roest, lichtblauw/groen) en met een baksteen-variant van de muurtegels;
- markt: kraam, potten, kisten en fruit van de Slateport-markt (Slateport-paletten 6, 7, 9), kasseien uit Slateport;
- grond, kliffen (General-rotsen in rode klei), paden, bomen, bloemen, borden: de Andes-primary (General).
Zelf getekend, in Hoenn-stijl (navy omlijning, licht linksboven, dezelfde tinten): plat dak met watertank en
wachtijzers, extra verdiepingen, cholets, kabelbaan (masten, kabels, gondels; station = Ekat 'Cable Car'
omgekleurd naar het Pokémon Center-palet), de Illimani.

Gebruik: python3 tools/concept/tiles/la_paz_r2.py  ->  tilesets/eigen/la_paz/ronde2/
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
from r2lib import load_set, recolor, Canvas, comparison
from andes_primary import build, CLAY, PUNA
from tilelib import ellipse_mask, render_repo_map

OUT = 'tilesets/eigen/la_paz/ronde2'
pair = build()
P = pair.pals
mau = load_set('secondary', 'mauville')
sl = load_set('secondary', 'slateport')

# ------------------------------------------------------------------ paletten 6..12
M7 = [tuple(int(v) for v in c) for c in mau['pals'][7]]
GR15 = PUNA[1]


def house_pal(wall, roof):
    return recolor(M7, {1: wall[0], 2: wall[1], 3: wall[2], 4: wall[3], 11: roof[0], 12: roof[1], 13: roof[2],
                        14: roof[3]})


P[6] = house_pal([(248, 216, 176), (232, 152, 104), (200, 104, 72), (152, 72, 56)],      # baksteen
                 [(216, 224, 232), (176, 192, 208), (136, 152, 176), (96, 104, 136)])    # zink
P[7] = house_pal([(255, 248, 192), (240, 216, 128), (216, 176, 88), (176, 136, 72)],     # oker
                 [(248, 176, 144), (224, 112, 88), (184, 72, 64), (128, 56, 56)])        # roest-rood
P[8] = house_pal([(232, 248, 255), (184, 224, 240), (136, 184, 224), (104, 144, 192)],   # lichtblauw
                 [(192, 240, 152), (128, 200, 104), (80, 160, 80), (56, 112, 64)])       # groen
P[9] = [tuple(int(v) for v in c) for c in sl['pals'][9]]
S6 = [tuple(int(v) for v in c) for c in sl['pals'][6]]
P[10] = recolor(S6, {3: (224, 216, 200), 4: (216, 200, 184), 11: (240, 232, 216), 12: (216, 200, 184),
                     13: (184, 168, 152), 14: (144, 128, 120), 15: GR15})
P[11] = recolor([tuple(int(v) for v in c) for c in sl['pals'][7]], {})
# 12: cholet + kabelbaan (eigen), Hoenn-omlijning en glas
NAVY, NAVY2 = (65, 74, 106), (41, 49, 90)
WH = (255, 255, 255)
GL = [(98, 164, 222), (115, 189, 246), (189, 230, 255)]
MG = [(205, 65, 130), (246, 140, 197)]
YE, OR, LI = (255, 213, 65), (246, 140, 57), (148, 213, 74)
PU = [(123, 82, 180), (180, 148, 230)]
RD = (222, 57, 57)
ST = [(164, 164, 180), (115, 115, 139)]
GD = OR
P[12] = [(255, 0, 255), NAVY, WH] + GL + MG + [YE, OR, LI] + PU + [RD] + ST
assert len(P[12]) == 16, len(P[12])

# ------------------------------------------------------------------ huizen (Mauville)


def brickify(idx, srcpal):
    """Muurpixels (index 2-4 van het Mauville-palet) -> onafgewerkte baksteen: voeg licht (1), steen 3,
    licht randje 2, schaduw 4. Periode 8, dus naadloos."""
    if srcpal != 7:
        return idx
    out = idx.copy()
    for y in range(8):
        for x in range(8):
            if idx[y, x] in (2, 3, 4):
                row, r = y // 4, y % 4
                bx = (x + row * 4) % 8
                v = 1 if (r == 3 or bx == 7) else (2 if (r == 0 and bx < 5) else (4 if (r == 2 and bx > 4) else 3))
                out[y, x] = v
    return out


HOUSE = pair.import_region(mau, 'MauvilleCity', 18, 11, 22, 15, {7: 6}, 'mau')
HB = []
for y, row in enumerate(HOUSE):
    r = []
    for x, m in enumerate(row):
        name = [k for k, v in pair.names.items() if v == m and k.startswith('mau_')]
        if y < 2 or not name:
            r.append(m)
            continue
        sid = int(name[0].split('_')[1], 16)
        nm = f'maub_{sid:03x}'
        if nm not in pair.names:
            pair.import_mt(mau, sid, {7: 6}, nm, tilemap=brickify)
        r.append(pair.names[nm])
    HB.append(r)


def compose(name, src_tiles, pal, src=mau, bottom=(0x2002, 0x2003, 0x2003, 0x2002), tilemap=None, layer=1):
    """Metatile uit losse brontegels (bovenlaag), bijv. een extra verdieping uit Mauville-muurtegels."""
    ents = list(bottom)
    for t in src_tiles:
        if t is None:
            ents.append(0)
            continue
        tid, hf = t if isinstance(t, tuple) else (t, 0)
        idx = src['tiles'][tid - 512].copy()
        if tilemap:
            idx = tilemap(idx, 7)
        idx = idx[:, ::-1] if hf else idx
        ents.append(pair.tile_ref(idx, pal))
    return pair.add_mt(name, ents, layer << 12)


# extra verdieping (muur + raam in één rij), gepleisterd en baksteen
for tag, tm in (('', None), ('b', brickify)):
    compose(f'floor{tag}_l', [0x245, 0x246, 0x245, 0x246], 6, tilemap=tm)
    compose(f'floor{tag}_m', [0x246, 0x246, 0x246, 0x246], 6, tilemap=tm)
    compose(f'floor{tag}_r', [0x246, 0x247, 0x246, 0x247], 6, tilemap=tm)
    compose(f'floor{tag}_win', [0x229, 0x22a, 0x239, 0x23a], 6, tilemap=tm)


# plat betonnen dak (2 rijen) in de grijstinten van het huispalet (index 5-10), Hoenn-opbouw
def flat_roof(piece, row, extra=None):
    c = Canvas(16, 16)
    g = [P[6][9], P[6][10], P[6][5], P[6][6], P[6][7], P[6][8]]   # licht .. donker (navy)
    for y in range(16):
        for x in range(16):
            col = g[1]
            if (x * 3 + y * 7) % 11 == 0:
                col = g[2]
            elif (x * 5 + y * 3) % 13 == 0:
                col = g[0]
            c.px(x, y, col)
    if row == 0:
        c.hline(0, 15, 0, g[5]); c.hline(0, 15, 1, g[0]); c.hline(0, 15, 2, g[0]); c.hline(0, 15, 3, g[3])
    else:
        c.hline(0, 15, 11, g[3]); c.hline(0, 15, 12, g[0]); c.hline(0, 15, 13, g[1]); c.hline(0, 15, 14, g[3])
        c.hline(0, 15, 15, g[5])
    if piece == 'l':
        c.vline(0, 0, 15, g[5]); c.vline(1, 1 if row == 0 else 0, 14, g[0]); c.vline(2, 2 if row == 0 else 0, 14, g[0])
        c.vline(3, 4 if row == 0 else 0, 10 if row else 15, g[3])
    if piece == 'r':
        c.vline(15, 0, 15, g[5]); c.vline(14, 1 if row == 0 else 0, 14, g[2]); c.vline(13, 2 if row == 0 else 0, 14, g[1])
        c.vline(12, 4 if row == 0 else 0, 10 if row else 15, g[0])
    if extra == 'tank':  # zwarte watertank (tinaco)
        k = [g[5], g[4], g[3]]
        c.mask_fill(ellipse_mask(8, 9, 5.5, 5), k[1])
        c.mask_fill(ellipse_mask(7, 8, 3.5, 3), k[2])
        for x in range(4, 13, 3):
            c.vline(x, 6, 12, k[0]) if False else None
        c.hline(4, 12, 11, k[0]); c.px(6, 6, g[0]); c.px(7, 6, g[0])
        cc = Canvas(16, 16)
        cc.a = c.a.copy()
        cc.mask_fill(lambda x, y: ellipse_mask(8, 9, 6.5, 6)(x, y) and not ellipse_mask(8, 9, 5.5, 5)(x, y), k[0])
        c = cc
    if extra == 'rebar':  # wachtijzers: het huis groeit nog
        xs = (3, 5) if piece == 'l' else ((10, 12) if piece == 'r' else (7, 9))
        for x in xs:
            c.vline(x, 1, 6, P[6][4]); c.px(x, 0, P[6][3]); c.px(x + 1, 6, g[3])
    if extra == 'laundry':
        c.hline(1, 14, 4, g[5])
        for x, col in ((3, P[6][12]), (4, P[6][12]), (7, P[6][2]), (8, P[6][2]), (11, P[6][15]), (12, P[6][15])):
            c.vline(x, 5, 8, col)
        for x in (3, 7, 11):
            c.px(x + 1, 8, g[3])
    return c


for row in (0, 1):
    for p in ('l', 'm', 'r'):
        pair.add_drawn(f'flat{row}_{p}', flat_roof(p, row), pals=(6,))
for row, p, e in ((0, 'm', 'tank'), (0, 'l', 'rebar'), (0, 'm', 'rebar'), (0, 'r', 'rebar'), (1, 'm', 'laundry')):
    pair.add_drawn(f'flat{row}_{p}_{e}', flat_roof(p, row, e), pals=(6,))

# kleurvarianten: elk huisstuk ook in palet 7 en 8 (0 extra tegels)
HOUSE_KEYS = [k for k in list(pair.names) if k.startswith(('mau_', 'maub_', 'floor', 'flat'))]


def palvariant(name, to):
    m = pair.names[name]
    ents = [((e & 0x0FFF) | (to << 12)) if (e >> 12) == 6 and e else e for e in pair.sm[m - 512]]
    return pair.add_mt(f'{name}@{to}', ents, pair.sa[m - 512])


for k in HOUSE_KEYS:
    for to in (7, 8):
        palvariant(k, to)

# ------------------------------------------------------------------ markt en straat (Slateport)
SLMAP = {6: 10, 7: 11, 9: 9}
TENT = pair.import_region(sl, 'SlateportCity', 9, 41, 13, 44, SLMAP, 'sl')
for mid in (0x211, 0x210, 0x212, 0x23a, 0x33f, 0x344, 0x20c, 0x213, 0x23b, 0x219):
    if f'sl_{mid:03x}' not in pair.names:
        pair.import_mt(sl, mid, SLMAP, f'sl_{mid:03x}')
N = pair.names
COBBLE = N['sl_211']


# ------------------------------------------------------------------ cholets (palet 12)
def cholet_row(kind, piece, scheme=0):
    band, band2 = [(MG[0], YE), (OR, PU[1]), (LI, MG[1])][scheme]
    c = Canvas(16, 16, WH)
    if kind == 'roof':
        c.rect(0, 0, 15, 15, ST[0])
        for x in range(16):
            for y in range(16):
                if (x * 3 + y * 5) % 9 == 0:
                    c.px(x, y, WH)
        c.hline(0, 15, 0, NAVY); c.hline(0, 15, 1, WH); c.hline(0, 15, 13, ST[1]); c.hline(0, 15, 14, WH)
        c.hline(0, 15, 15, NAVY)
    if kind == 'crown':
        c.rect(0, 0, 15, 15, band)
        for x in range(16):
            h = [0, 1, 2, 3, 3, 2, 1, 0][x % 8]
            c.vline(x, 9 - h * 2, 13, band2)
        c.hline(0, 15, 0, NAVY); c.hline(0, 15, 1, WH); c.hline(0, 15, 14, WH); c.hline(0, 15, 15, NAVY)
    if kind == 'floor':
        c.rect(0, 0, 15, 2, band)
        for x in range(0, 16, 4):
            c.px(x + 1, 1, band2); c.px(x + 2, 1, band2)
        c.rect(0, 3, 15, 13, GL[1]); c.rect(0, 9, 15, 13, GL[0])
        for x in (0, 8):
            c.vline(x, 3, 13, WH)
        for k in (2, 10):
            c.px(k, 5, GL[2]); c.px(k + 1, 4, GL[2]); c.px(k, 4, GL[2]); c.px(k + 2, 4, WH)
        c.hline(0, 15, 14, WH); c.hline(0, 15, 15, ST[1])
        if piece == 'm2':
            c.rect(6, 4, 10, 12, WH)
            c.px(8, 5, band); c.rect(7, 6, 9, 10, band); c.px(8, 11, band); c.px(8, 8, band2)
    if kind in ('hall0', 'hall1'):
        if kind == 'hall0':
            c.rect(0, 0, 15, 1, WH); c.rect(0, 2, 15, 9, PU[0]); c.hline(0, 15, 2, PU[1])
            for x in range(1, 16, 4):
                c.rect(x, 4, x + 1, 7, YE)
            c.hline(0, 15, 10, NAVY)
            c.rect(0, 11, 15, 15, GL[0])
            for x in (3, 7, 11, 15):
                c.vline(x, 11, 15, GL[1])
        else:
            c.rect(0, 0, 15, 15, GL[0])
            for x in (3, 7, 11, 15):
                c.vline(x, 0, 13, GL[1])
            c.hline(0, 15, 14, ST[1]); c.hline(0, 15, 15, NAVY)
        if piece == 'door':
            y0 = 11 if kind == 'hall0' else 0
            c.rect(5, y0, 10, 13 if kind == 'hall1' else 15, GD); c.vline(7, y0, 13, YE); c.vline(8, y0, 13, NAVY)
    if piece == 'l':
        c.rect(0, 0, 3, 15, band if kind != 'roof' else ST[0])
        c.vline(0, 0, 15, NAVY); c.vline(1, 0, 15, band2 if kind in ('floor', 'hall1') else WH)
    if piece == 'r':
        c.rect(12, 0, 15, 15, band if kind != 'roof' else ST[0])
        c.vline(15, 0, 15, NAVY); c.vline(14, 0, 15, band2 if kind in ('floor', 'hall1') else ST[1])
    return c


for k in ('roof', 'crown'):
    for sch in ((0, 1, 2) if k == 'crown' else (0,)):
        for p in ('l', 'm', 'r'):
            pair.add_drawn(f'cholet_{k}{sch}_{p}', cholet_row(k, p, sch), pals=(12,))
for sch in (0, 1, 2):
    for p in ('l', 'm', 'm2', 'r'):
        pair.add_drawn(f'cholet_floor{sch}_{p}', cholet_row('floor', p, sch), pals=(12,))
for k in ('hall0', 'hall1'):
    for p in ('l', 'm', 'door', 'r'):
        pair.add_drawn(f'cholet_{k}_{p}', cholet_row(k, p), pals=(12,))


def chalet():
    """Het 'chalet' van de eigenaar bovenop een cholet (3 x 2)."""
    c = Canvas(48, 32)
    for x in range(3):
        c.paste(cholet_row('roof', 'm'), x * 16, 0)
        c.paste(cholet_row('roof', 'm'), x * 16, 16)
    for y in range(2, 14):
        x0, x1 = 6 + (13 - y) // 2, 41 - (13 - y) // 2
        c.hline(x0, x1, y, PU[1] if (y // 2) % 2 else PU[0])
    c.hline(4, 43, 14, NAVY); c.hline(6, 41, 1, NAVY)
    for y in range(2, 14):
        c.px(6 + (13 - y) // 2 - 1, y, NAVY); c.px(41 - (13 - y) // 2 + 1, y, NAVY)
    c.rect(6, 15, 41, 29, WH); c.vline(6, 15, 29, NAVY); c.vline(41, 15, 29, NAVY); c.hline(6, 41, 29, NAVY)
    c.hline(7, 40, 15, ST[0])
    for x in (10, 30):
        c.rect(x, 18, x + 6, 24, GL[1]); c.box(x - 1, 17, x + 7, 25, NAVY); c.px(x + 1, 19, GL[2]); c.px(x + 2, 19, WH)
    c.rect(20, 18, 27, 29, GD); c.box(19, 17, 28, 29, NAVY); c.vline(23, 18, 28, YE)
    return c


def slice_drawn(name, cv, pals, ground=None, top_rows=()):
    """Object knippen: dekkende vakken in de onderlaag, de rest als bovenlaag op een grondmetatile."""
    gb = pair.ents(ground)[:4] if ground is not None else None
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


OBJ = {'chalet': slice_drawn('chalet', chalet(), (12,))}


# ------------------------------------------------------------------ kabelbaan
def ekat_station():
    """Ekat & Heartlessdragoon, 'Cable Car': het stationsgebouw (7 x 5), omgekleurd naar het Pokémon Center-
    palet (primary 0): navy omlijning, wit, lichtgrijs, blauw glas, dak in het blauw van de Mart."""
    a = np.array(Image.open('tilesets/nieuw/ekat/Cable Car.png').convert('RGBA'))
    p0 = P[0]
    mp = {(49, 56, 82): p0[7], (255, 255, 255): p0[1], (248, 240, 216): p0[2],
          (103, 151, 133): p0[11], (91, 133, 117): p0[12], (67, 97, 85): p0[13], (61, 88, 77): p0[14],
          (168, 136, 104): p0[3], (144, 104, 88): p0[4], (124, 90, 76): p0[6],
          (168, 200, 248): p0[9], (208, 224, 248): p0[2], (192, 192, 168): p0[3], (144, 144, 136): p0[5],
          (120, 120, 128): p0[6], (64, 72, 104): p0[7]}
    c = Canvas(112, 80)
    for y in range(80):
        for x in range(112):
            r, g, b, al = a[y, x]
            if not al:
                continue
            if (a[(y // 16) * 16:(y // 16) * 16 + 16, (x // 16) * 16:(x // 16) * 16 + 16, :3] == (255, 0, 0)).all(-1).any():
                continue
            col = mp.get((int(r), int(g), int(b)))
            if col:
                c.px(x, y, col)
    return c


def mast(dirn='ew'):
    c = Canvas(16, 64)
    g = [P[0][2], P[0][5], P[0][6], P[0][7]]
    for y in range(12, 58):
        w = 2 + (y - 12) // 16
        c.rect(8 - w, y, 7 + w, y, g[1]); c.px(8 - w, y, g[3]); c.px(7 + w, y, g[3]); c.px(9 - w, y, g[0])
        if w > 2:
            c.px(6 + w, y, g[2])
    for y in range(18, 56, 6):
        c.px(9, y, g[2])
    c.rect(2, 56, 13, 63, g[1]); c.box(2, 56, 13, 63, g[3]); c.hline(3, 12, 57, g[0]); c.hline(3, 12, 62, g[2])
    if dirn == 'ew':
        c.rect(3, 1, 12, 13, g[1]); c.box(3, 1, 12, 13, g[3]); c.vline(4, 2, 12, g[0])
        for y in (3, 11):
            c.hline(0, 2, y, NAVY2); c.hline(13, 15, y, NAVY2)
            c.rect(5, y - 1, 10, y + 1, P[0][13]); c.hline(5, 10, y - 1, P[0][9])
    else:
        c.rect(1, 4, 14, 11, g[1]); c.box(1, 4, 14, 11, g[3]); c.hline(2, 13, 5, g[0])
        for x in (4, 11):
            c.rect(x - 1, 2, x + 1, 9, P[0][13]); c.vline(x - 1, 2, 9, P[0][9]); c.vline(x, 0, 2, NAVY2)
    return c


def cable(dirn):
    c = Canvas(16, 16)
    if dirn == 'ew':
        c.hline(0, 15, 3, NAVY2); c.hline(0, 15, 11, NAVY2)
    else:
        c.vline(4, 0, 15, NAVY2); c.vline(11, 0, 15, NAVY2)
    return c


def gondola(light, dark):
    c = Canvas(16, 32)
    c.hline(0, 15, 3, NAVY2)
    c.rect(6, 1, 9, 4, ST[1]); c.box(6, 1, 9, 4, NAVY)
    c.vline(7, 5, 9, NAVY); c.vline(8, 5, 9, ST[0])
    c.rect(2, 10, 13, 12, light); c.box(2, 10, 13, 12, NAVY); c.hline(3, 12, 11, WH)
    c.rect(2, 13, 13, 24, dark); c.box(2, 13, 13, 24, NAVY)
    c.rect(3, 14, 12, 19, GL[1]); c.hline(3, 12, 19, GL[0]); c.vline(7, 14, 19, dark); c.vline(8, 14, 19, dark)
    c.px(4, 15, WH); c.px(5, 14, WH); c.px(4, 14, GL[2])
    c.rect(3, 20, 12, 23, light)
    return c


OBJ['station'] = slice_drawn('station', ekat_station(), (0,), ground=COBBLE, top_rows=(0,))
OBJ['mast_ew'] = slice_drawn('mast_ew', mast('ew'), (0,), ground=COBBLE, top_rows=(0, 1))
OBJ['mast_ns'] = slice_drawn('mast_ns', mast('ns'), (0,), ground=COBBLE, top_rows=(0, 1))
CABLE = {d: cable(d) for d in ('ew', 'ns')}
for d in ('ew', 'ns'):
    pair.add_drawn(f'cable_{d}', None, CABLE[d], pals=(12,), layer='normal', bottom_ents=pair.ents(COBBLE)[:4])
GONDOLA = {'red': gondola(MG[1], RD), 'yellow': gondola(YE, OR), 'green': gondola(LI, (80, 160, 80) if False else LI)}
GONDOLA['green'] = gondola(LI, PU[0])


# ------------------------------------------------------------------ Illimani (primary-palet 4)
def illimani():
    p4 = P[4]
    SN, SN2, SH, SKY = p4[1], p4[2], p4[12], p4[11]
    RK = [p4[3], p4[4], p4[5]]
    OL = p4[0]
    W_, H_ = 192, 80
    c = Canvas(W_, H_)
    peaks = [(40, 18), (96, 2), (152, 26)]
    for x in range(W_):
        px_, py = min(peaks, key=lambda p: p[1] + abs(x - p[0]))
        top = py + abs(x - px_)
        left = x < px_
        snowline = 42 + (x // 8) % 2 * 2 + (4 if (x // 16) % 2 else 0)
        for y in range(H_):
            if y < top:
                col = SKY
            elif y == top:
                col = OL
            elif y < snowline:
                col = SN if left else SN2
                if not left and (x - y) % 8 == 0:
                    col = SH
                if left and (x + y) % 16 == 0 and y > top + 3:
                    col = SN2
                if x == px_:
                    col = SN2
            elif y < snowline + 2:
                col = SH if (x + y) % 2 else RK[0]
            else:
                col = RK[0] if left else RK[1]
                if (y - snowline) % 6 == 0 or (x + y) % 8 == 0:
                    col = RK[1] if left else RK[2]
            if y > 75:
                col = None
            elif y == 75:
                col = OL
            if col:
                c.px(x, y, col)
    return c


GROUND = 0x001
OBJ['illimani'] = slice_drawn('illimani', illimani(), (4,), ground=GROUND)

# ------------------------------------------------------------------ mock-up
G_TREE = [[0x1d4, 0x1d5], [0x1dc, 0x1dd]]


def put(g, x, y, ids):
    for dy, row in enumerate(ids):
        for dx, m in enumerate(row):
            if m is not None and 0 <= y + dy < len(g) and 0 <= x + dx < len(g[0]):
                g[y + dy][x + dx] = m


def V(name, pal):
    return N[name if pal == 6 else f'{name}@{pal}']


def house(g, x, y, pal=6, brick=False, floors=0, roof='tin', w=4, extras=()):
    """Mauville-huis (4 breed) of breder; floors = extra verdiepingen; roof tin/flat."""
    H = HB if brick else HOUSE
    rows = []
    if roof == 'tin':
        rows.append([H[0][0]] + [H[0][1]] * (w - 2) + [H[0][3]])
        rows.append([H[1][0]] + [H[1][1]] * (w - 2) + [H[1][3]])
    else:
        for rr in (0, 1):
            r = [N[f'flat{rr}_l']] + [N[f'flat{rr}_m']] * (w - 2) + [N[f'flat{rr}_r']]
            for i, e in extras:
                if e.startswith(f'flat{rr}_'):
                    r[i] = N[e]
            rows.append(r)
    tag = 'b' if brick else ''
    for f in range(floors):
        rows.append([N[f'floor{tag}_l']] + [N[f'floor{tag}_win'] if i % 2 == 0 else N[f'floor{tag}_m']
                                             for i in range(w - 2)] + [N[f'floor{tag}_r']])
    rows.append([H[2][0], H[2][1]] + [H[2][2]] * (w - 3) + [H[2][3]])
    rows.append([H[3][0], H[3][1]] + [H[3][2]] * (w - 3) + [H[3][3]])
    if pal != 6:
        rows = [[pair.names.get(f'{name_of(m)}@{pal}', m) for m in r] for r in rows]
    put(g, x, y, rows)


REV = None


def name_of(m):
    global REV
    if REV is None or m not in REV:
        REV = {v: k for k, v in pair.names.items()}
    return REV[m]


def cholet(g, x, y, w, floors=3, scheme=0, chal=False):
    rows = []
    if chal:
        rows.append([None] * w)
    rows.append([N['cholet_roof0_l']] + [N['cholet_roof0_m']] * (w - 2) + [N['cholet_roof0_r']])
    rows.append([N[f'cholet_crown{scheme}_l']] + [N[f'cholet_crown{scheme}_m']] * (w - 2) + [N[f'cholet_crown{scheme}_r']])
    for f in range(floors):
        s = (scheme + f) % 3
        rows.append([N[f'cholet_floor{s}_l']] + [N[f'cholet_floor{s}_m' if i % 2 == 0 else f'cholet_floor{s}_m2']
                                                  for i in range(w - 2)] + [N[f'cholet_floor{s}_r']])
    for k in ('hall0', 'hall1'):
        mid = [N[f'cholet_{k}_m']] * (w - 2)
        mid[(w - 2) // 2] = N[f'cholet_{k}_door']
        rows.append([N[f'cholet_{k}_l']] + mid + [N[f'cholet_{k}_r']])
    put(g, x, y, rows)
    if chal:
        put(g, x + (w - 3) // 2, y, OBJ['chalet'])


ovc = {}


def reground(ids, ground, from_row=0):
    """Zelfde object op andere grond: alleen de onderlaag wisselt (0 extra tegels)."""
    gb = pair.ents(ground)[:4]
    out = []
    for i, row in enumerate(ids):
        r = []
        for m in row:
            if i < from_row:
                r.append(m)
                continue
            nm = f'{name_of(m)}@{name_of(ground)}'
            if nm not in pair.names:
                e = pair.ents(m)
                attr = pair.pa[m] if m < 512 else pair.sa[m - 512]
                pair.add_mt(nm, list(gb) + list(e[4:]), attr)
            r.append(pair.names[nm])
        out.append(r)
    return out


def overlay(base, top_cv, key):
    """Kabel/gondel boven op een bestaande metatile (eigen combinatie)."""
    if (base, key) in ovc:
        return ovc[(base, key)]
    ents = pair.ents(base)
    top = Canvas(16, 16)
    for k in range(4):
        e = ents[4 + k]
        t = e & 0x3FF
        if t:
            tp = pair.tile(t)
            tp = tp[:, ::-1] if (e >> 10) & 1 else tp
            tp = tp[::-1, :] if (e >> 11) & 1 else tp
            pal = P[e >> 12]
            for yy in range(8):
                for xx in range(8):
                    if tp[yy, xx]:
                        top.px((k % 2) * 8 + xx, (k // 2) * 8 + yy, pal[tp[yy, xx]])
    top.paste(top_cv, 0, 0)
    pals = sorted({e >> 12 for e in ents[4:] if e & 0x3FF} | {12})
    m = pair.add_drawn(f'ov{len(ovc)}', None, top, pals=tuple(pals), layer='normal', bottom_ents=ents[:4])
    ovc[(base, key)] = m
    return m


def mockup():
    Wm, Hm = 30, 24
    g = [[GROUND] * Wm for _ in range(Hm)]
    for x in range(0, Wm, 4):
        put(g, x, 0, [[N['andes_sky']] * 4] * 2)
        put(g, x, 2, [[N[f'andes_range_{mx}_{my}'] for mx in range(4)] for my in range(3)])
    put(g, 9, 0, OBJ['illimani'])
    # kleiterras (General-rotsen in rode klei): zuidwand 0x7C boven, 0x79 onder
    for x in range(Wm):
        g[5][x] = 0x7C; g[6][x] = 0x79
    for x in (13, 14):
        g[5][x] = 0x1  # trap-opening
        g[6][x] = 0x1
    # bovenste huizenrij
    house(g, 0, 7, pal=6, brick=True, roof='flat', extras=[(1, 'flat0_m_tank'), (3, 'flat0_r_rebar')])
    house(g, 4, 7, pal=7, roof='tin')
    house(g, 8, 6, pal=8, brick=False, floors=1, roof='tin')
    cholet(g, 15, 5, 4, floors=3, scheme=0, chal=True)
    house(g, 19, 7, pal=6, brick=True, roof='tin')
    house(g, 23, 6, pal=7, brick=True, floors=1, roof='flat', extras=[(1, 'flat1_m_laundry'), (2, 'flat0_m_tank')])
    cholet(g, 27, 7, 3, floors=2, scheme=1)
    # trappenstraat door het midden (Hoenn-paadje), kantuta's ernaast
    for y in range(5, 13):
        g[y][13] = 0x121; g[y][14] = 0x121
    for y in (5, 6):
        g[y][13] = 0xaf; g[y][14] = 0xaf
    # leven op de puna-strook voor de huizen: bloemen, kantuta, struikjes, bordjes
    for (x, y, m) in ((2, 11, 0x004), (3, 11, 0x004), (6, 12, N['andes_kantuta']), (9, 12, 0x00e), (11, 11, 0x004),
                      (12, 12, N['andes_kantuta']), (20, 12, 0x004), (21, 12, 0x004), (22, 11, 0x00e),
                      (25, 12, N['andes_kantuta']), (26, 12, 0x003)):
        g[y][x] = m
    # straat: Slateport-kasseien
    for y in (13, 14):
        for x in range(Wm):
            g[y][x] = COBBLE
    # onderste deel: station, mast, markt, pleintje met bomen
    put(g, 0, 15, [[COBBLE] * 30 for _ in range(9)])
    for y in range(15, Hm):
        for x in range(Wm):
            g[y][x] = COBBLE
    put(g, 0, 15, OBJ['station'])
    put(g, 7, 15, OBJ['mast_ew'])
    put(g, 14, 16, TENT); put(g, 14, 20, TENT)
    g[18][15] = N['sl_23a']; g[18][16] = N['sl_344']; g[22][16] = N['sl_33f']; g[22][15] = N['sl_20c']
    g[17][19] = N['sl_344']; g[19][19] = N['sl_23a']; g[21][19] = N['sl_33f']
    # pleintje (puna-grond met Hoenn-bomen, bloemen, lantaarns, banken)
    for y in range(16, Hm):
        for x in range(21, Wm):
            g[y][x] = GROUND
    put(g, 25, 16, G_TREE); put(g, 27, 19, G_TREE)
    put(g, 22, 16, [[N['andes_lamp_0']], [N['andes_lamp_1']]]); put(g, 28, 16, [[N['andes_lamp_0']], [N['andes_lamp_1']]])
    g[18][23] = N['andes_bench']; g[18][24] = N['andes_bench']
    for (x, y) in ((22, 20), (23, 20), (22, 21), (24, 22), (25, 22), (21, 23)):
        g[y][x] = 0x004
    g[21][24] = N['andes_kantuta']; g[23][27] = N['andes_kantuta']; g[16][21] = 0x003
    # straatlantaarns op de kasseien
    for x in (5, 12, 20):
        put(g, x, 12, reground([[N['andes_lamp_0']], [N['andes_lamp_1']]], COBBLE, 1))
    # kabelbaan: oost-west op rij 15 (koppen van de mast), noord-zuid over de huizen
    cy = 15
    for x in range(8, Wm):
        g[cy][x] = overlay(g[cy][x], CABLE['ew'], 'ew')
    for x, col in ((11, 'red'), (20, 'yellow')):
        gc = GONDOLA[col]
        g[cy][x] = overlay(g[cy][x], gc.sub(0, 0, 16, 16), col + '0')
        g[cy + 1][x] = overlay(g[cy + 1][x], gc.sub(0, 16, 16, 16), col + '1')
    put(g, 10, 16, OBJ['mast_ns'])
    for y in range(5, 16):
        g[y][10] = overlay(g[y][10], CABLE['ns'], 'ns')
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
r1 = np.array(Image.open('tilesets/eigen/la_paz/mockup.png').convert('RGB'))
hoenn = render_repo_map('MauvilleCity', 0, 20, 0, 30)
for sc in (1, 2):
    comparison([r1, img, hoenn], ['ronde 1', 'ronde 2', 'Hoenn: Mauville'], OUT + f'/vergelijking_{sc}x.png', scale=sc)
print('secondary-tegels', len(pair.st), '/ 512   metatiles', len(pair.sm), '/ 512',
      f'(mock-upcombinaties: {len(pair.st) - BASE_ST} tegels, {len(pair.sm) - BASE_SM} metatiles)')
groups = {}
for k, v in pair.cost.items():
    if k.startswith('andes_'):
        continue
    gk = k.split('_')[0].split('@')[0]
    groups[gk] = groups.get(gk, 0) + v
print(groups)
