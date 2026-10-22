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
    band = poly([(cx - r * 0.35, cy - r - 1.2), (cx + r * 0.75, cy - r - 1.2),
                 (cx + r * 0.75, cy - r + 0.9), (cx - r * 0.35, cy - r + 0.9)]) & ~m
    cel(c, band, 'goud', tones=FAR['goud'] if far else (11, 11, 12, 12), light=0, shade=(0, 1), deep=0)
    cel(c, m, 'rood', tones=FAR['rood'] if far else None, light=1 if not far else 0, shade=(2, 2), deep=1)


def lumps(c, items, light=1, shade=(2, 2), edge=4):
    """Wolbolletjes van achter (eerst) naar voor; elk een eigen klein balletje met
    hooglicht linksboven en schaduwband rechtsonder (Mareep)."""
    for x, y, r in items:
        cel(c, disk(x, y, r, r * 0.92), 'wol', light=light, shade=shade, deep=0, edge=edge)


def frame(f2=False):
    c = Canvas(R)
    # --- verre poten (achter het lijf): donkerder, kleiner, hoger ---
    cel(c, poly([(47.5, 41), (51, 41), (51, 49), (47.5, 49)]), 'vacht', tones=FAR['vacht'], light=0, deep=0)
    cel(c, poly([(47, 49), (51.5, 49), (51.5, 51), (47, 51)]), 'vacht', tones=(7, 7, 7, 7), light=0, deep=0)
    cel(c, poly([(29, 42), (32.5, 42), (32.5, 47), (29, 47)]), 'vacht', tones=FAR['vacht'], light=0, deep=0)
    glove(c, 31.5, 50, 3.5, far=True)
    # --- staart ---
    lumps(c, [(52.5, 30, 3.0)])
    # --- wollen lijf: achterste bolletjes eerst, voorste (links/onder) laatst ---
    cel(c, disk(39, 38, 11, 7), 'wol', light=0, shade=(2, 3), deep=1)
    lumps(c, [(49, 35, 4.0), (44, 31.5, 4.4), (49, 41, 3.8), (37, 31, 4.8), (44, 38, 4.6),
              (44, 44, 4.2), (37, 37, 5.0), (30, 33, 4.8), (37, 44.5, 4.4), (31, 39, 5.0), (30, 45, 4.2)])
    # --- nabije achterpoot ---
    cel(c, poly([(41.5, 46), (46, 46), (45.5, 51.5), (42, 51.5)]), 'vacht', light=1, shade=(2, 0), deep=0, edge=15)
    cel(c, poly([(41.5, 51.5), (46, 51.5), (46.5, 54), (41, 54)]), 'vacht', tones=(7, 7, 7, 7), light=0, deep=0)
    # --- hals (wol) + borst ---
    lumps(c, [(25, 39, 4.6), (24.5, 33.5, 4.6), (23.5, 29, 4.2)])
    # --- nabije voorpoot + handschoen ---
    if f2:   # stoot naar voren
        cel(c, poly([(25, 40), (27.5, 43), (18, 44.5), (16, 41.5)]), 'vacht', light=1, shade=(1, 2), deep=0, edge=15)
        glove(c, 12.5, 42, 5.0)
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
