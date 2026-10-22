"""Alpaca ronde 4: Gen 3-stijl (cel-shading, driekwart, dynamisch). -> procbase.png
  python3 alpaca4.py <uitmap>
Daarna alpaca4.seg (gezicht, ogen, details met de hand) via segraster.py."""
import sys, os
sys.path.insert(0, '/home/user/projectgrounded/tools/concept/sprites')
import numpy as np
from shapelib import Canvas, save_indexed, write_jasc, hexpal
from celshade import cel, disk, poly

PAL = hexpal([
    '#94cd9c',
    '#ffffff', '#f4eee6', '#cec4d2', '#857894',  # 1-4 wol
    '#eeb07c', '#c07a50', '#7a3e2c',             # 5-7 vacht
    '#ff8a7a', '#e8383d', '#9e1b32',             # 8-10 handschoenen + kwastjes
    '#f6d050', '#c08a28',                        # 11-12 polsband
    '#d24a5e',                                   # 13 mond
    '#ffffff', '#101010'])
R = {'wol': [1, 2, 3, 4], 'vacht': [5, 6, 7], 'rood': [8, 9, 10], 'goud': [11, 12]}
FAR = {'vacht': (6, 7, 7, 7), 'rood': (9, 10, 10, 10), 'goud': (12, 12, 12, 12)}


def glove(c, cx, cy, r, far=False):
    """Ronde bokshandschoen (duim aan de voorkant) met een smalle gouden polsband."""
    m = disk(cx, cy, r, r * 0.88) | disk(cx - r * 0.62, cy - r * 0.2, r * 0.48)
    top = cy - r * 0.88
    band = poly([(cx - r * 0.3, top - 1.2), (cx + r * 0.6, top - 1.2),
                 (cx + r * 0.6, top + 0.4), (cx - r * 0.3, top + 0.4)]) & ~m
    cel(c, band, 'goud', tones=FAR['goud'] if far else (11, 11, 12, 12), light=0, shade=(0, 1), deep=0)
    cel(c, m, 'rood', tones=FAR['rood'] if far else None, light=1 if not far else 0, shade=(2, 2), deep=1)


def lumps(c, items, light=1, shade=(2, 2), edge=4):
    """Wolbolletjes van achter (eerst) naar voor; elk een eigen klein balletje met
    hooglicht linksboven en schaduwband rechtsonder (Mareep)."""
    for x, y, r in items:
        cel(c, disk(x, y, r, r * 0.92), 'wol', light=light, shade=shade, deep=0, edge=edge)


def frame(f2=False, stand=False):
    c = Canvas(R)
    # --- verre poten (achter het lijf): donkerder, kleiner, hoger ---
    cel(c, poly([(45, 41), (48.5, 41), (48.5, 49), (45, 49)]), 'vacht', tones=FAR['vacht'], light=0, deep=0)
    cel(c, poly([(44.5, 49), (49, 49), (49, 51), (44.5, 51)]), 'vacht', tones=(7, 7, 7, 7), light=0, deep=0)
    cel(c, poly([(29, 42), (32.5, 42), (32.5, 47), (29, 47)]), 'vacht', tones=FAR['vacht'], light=0, deep=0)
    glove(c, 31.5, 50, 3.5, far=True)
    # --- staart ---
    cel(c, disk(49, 31, 3.0), 'wol', light=1, shade=(1, 2), deep=0)
    # --- wollen lijf: één wolk met een geschulpte rand, cel-geschaduwd als geheel ---
    body = disk(36, 38.5, 9, 6.5)
    for x, y, r in [(29, 34, 4.2), (35, 31.5, 4.4), (41.5, 32, 4.2), (46, 35.5, 3.8), (47, 41, 3.6),
                    (43.5, 45.5, 3.8), (37.5, 46.5, 4.0), (31.5, 46.5, 4.0), (27, 43, 4.0), (26.5, 38, 4.0)]:
        body |= disk(x, y, r, r * 0.92)
    cel(c, body, 'wol', light=2, shade=(2, 3), deep=1)
    # --- nabije achterpoot ---
    cel(c, poly([(39.5, 46), (44, 46), (43.5, 51.5), (40, 51.5)]), 'vacht', light=1, shade=(2, 0), deep=0, edge=15)
    cel(c, poly([(39.5, 51.5), (44, 51.5), (44.5, 54), (39, 54)]), 'vacht', tones=(7, 7, 7, 7), light=0, deep=0)
    # --- hals (wol) + borst ---
    neck = disk(25.5, 38, 4.6, 5.2) | disk(23.5, 32, 4.4, 4.6) | disk(21.5, 28, 4.0, 3.6)
    cel(c, neck, 'wol', light=1, shade=(2, 2), deep=1, edge=3)
    # --- nabije voorpoot + handschoen ---
    if f2:   # stoot naar voren
        cel(c, poly([(25, 39), (28, 43.5), (18, 45.5), (15.5, 40.5)]), 'vacht', light=1, shade=(1, 2), deep=0, edge=15)
        glove(c, 12.5, 42, 5.0)
    elif stand:   # alternatief (thumbnail): staat op beide handschoenen
        cel(c, poly([(21, 42), (25.5, 42), (24, 47.5), (20, 47.5)]), 'vacht', light=1, shade=(1, 2), deep=0, edge=15)
        glove(c, 21, 51, 4.8)
    else:    # opgeheven in de dekking (staat op drie poten, zoals Ponyta's voorbeen)
        cel(c, poly([(22, 41), (26.5, 42), (22.5, 47.5), (18.5, 46)]), 'vacht', light=1, shade=(1, 2), deep=0, edge=15)
        glove(c, 18, 47.5, 4.8)
    # --- kop (naar de kijker gedraaid) ---
    hx, hy = (20, 20) if not f2 else (19, 21)
    cel(c, poly([(hx + 5, hy - 4), (hx + 7.5, hy - 11), (hx + 10, hy - 10.5), (hx + 8.5, hy - 3)]), 'vacht', tones=FAR['vacht'], light=0, deep=0)
    cel(c, poly([(hx - 5.5, hy - 3.5), (hx - 8, hy - 11), (hx - 5.5, hy - 12), (hx - 2.5, hy - 4.5)]), 'vacht', light=1, shade=(2, 1), deep=0)
    cel(c, disk(hx + 11, hy - 8.5, 1.8, 2.1), 'rood', tones=FAR['rood'], light=0, deep=0)
    cel(c, disk(hx - 9.3, hy - 8.8, 2.2, 2.5), 'rood', light=1, shade=(1, 1), deep=0)
    cel(c, disk(hx + 1, hy, 8, 6.6), 'vacht', light=1, shade=(2, 2), deep=1)
    cel(c, disk(hx - 5, hy + 3.4, 4.6, 3.2), 'vacht', tones=(5, 5, 6, 6), light=0, shade=(1, 2), deep=0)
    # mini-bolhoedje
    cel(c, disk(hx + 1.5, hy - 7.4, 4.0, 2.8), 'wol', light=1, shade=(1, 2), deep=0)
    cel(c, disk(hx + 1, hy - 5.3, 6.4, 1.3), 'wol', tones=(2, 2, 3, 3), light=0, shade=(1, 1), deep=0)
    c.outline()
    return c


if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else '.'
    fr = [frame(f).idx.astype(np.uint8) for f in (False, True)]
    save_indexed(os.path.join(d, 'procbase.png'), fr, PAL)
    write_jasc(os.path.join(d, 'normal.pal'), PAL)
    print('ok')
