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


def glove(c, cx, cy, r, far=False, cuff=True):
    tr = FAR['rood'] if far else None
    if cuff:
        cel(c, poly([(cx - r * 0.5, cy - r - 1.6), (cx + r * 0.7, cy - r - 1.6), (cx + r * 0.7, cy - r + 1.2), (cx - r * 0.5, cy - r + 1.2)]),
            'goud', tones=FAR['goud'] if far else (11, 11, 12, 12), light=0, shade=(0, 2), deep=0)
    m = disk(cx, cy, r, r * 0.86) | disk(cx - r * 0.55, cy - r * 0.25, r * 0.5)
    cel(c, m, 'rood', tones=tr, light=1 if not far else 0, shade=(2, 2), deep=1, edge=None)


def frame(f2=False):
    c = Canvas(R)
    # --- verre poten (achter het lijf): donkerder, kleiner, hoger ---
    cel(c, poly([(48, 42), (52, 42), (52, 50), (48, 50)]), 'vacht', tones=FAR['vacht'], light=0, deep=0)
    cel(c, poly([(48, 50), (52, 50), (52.5, 52), (47.5, 52)]), 'vacht', tones=(7, 7, 7, 7), light=0, deep=0)
    cel(c, poly([(29, 43), (32.5, 43), (32.5, 47), (29, 47)]), 'vacht', tones=FAR['vacht'], light=0, deep=0)
    glove(c, 31, 50, 3.6, far=True)
    # --- staart ---
    cel(c, disk(53, 31, 3.2), 'wol', light=1, shade=(1, 2), deep=0)
    # --- wollen lijf: bolletjes, cel-geschaduwd t.o.v. het hele lijf ---
    lumps = [(38, 39, 12, 7.5), (31, 34, 5.5, 5.5), (38, 32.5, 5.5, 5.5), (45, 33, 5, 5), (50, 37, 4.5, 4.5),
             (26, 41, 5, 5), (31, 45, 4.6, 4.6), (38, 46, 4.6, 4.6), (45, 45, 4.4, 4.4), (50, 42, 3.6, 3.6)]
    body = np.zeros((64, 64), bool)
    for x, y, rx, ry in lumps:
        body |= disk(x, y, rx, ry)
    cel(c, body, 'wol', light=0, shade=(2, 3), deep=1)
    # lichte kapjes linksboven op elk bovenste bolletje
    for x, y, rx, ry in lumps[1:5]:
        m = disk(x, y, rx, ry) & ~disk(x + 1.6, y + 1.6, rx, ry) & body
        c.idx[m & (c.idx == 2)] = 1
    # krulboogjes: onderrand van de bovenste bolletjes waar ze op het lijf liggen
    for x, y, rx, ry in lumps[1:5]:
        m = disk(x, y, rx, ry)
        rim = m & ~disk(x - 0.8, y - 1.3, rx, ry) & body
        inner = rim & np.roll(body, -2, 0) & np.roll(body, -2, 1)
        c.idx[inner & (c.idx == 2)] = 3
    # --- hals (wol) ---
    neck = disk(24, 33, 5.2, 6) | disk(22.5, 27, 4.6, 4.6)
    cel(c, neck, 'wol', light=1, shade=(2, 2), deep=1, edge=3)
    # --- nabije achterpoot ---
    cel(c, poly([(42, 46), (47, 46), (46.5, 52), (42.5, 52)]), 'vacht', light=1, shade=(2, 0), deep=0)
    cel(c, poly([(42.5, 52), (46.5, 52), (47, 54.5), (42, 54.5)]), 'vacht', tones=(7, 7, 7, 7), light=0, deep=0)
    # --- nabije voorpoot + handschoen ---
    if f2:
        cel(c, poly([(25, 42), (29, 44), (20, 46), (17, 43)]), 'vacht', light=1, shade=(1, 2), deep=0, edge=7)
        glove(c, 13, 44, 5.2)
    else:
        cel(c, poly([(21, 43), (26, 43), (24.5, 48), (20.5, 48)]), 'vacht', light=1, shade=(2, 1), deep=0, edge=7)
        glove(c, 21, 50.5, 4.8)
    # --- kop (naar de kijker gedraaid) ---
    hx, hy = (20, 21) if not f2 else (19, 22)
    # oren (banaan) + hangende kwastjes
    cel(c, poly([(hx + 5, hy - 5), (hx + 7, hy - 12), (hx + 9.5, hy - 11.5), (hx + 8.5, hy - 4)]), 'vacht', tones=FAR['vacht'], light=0, deep=0)
    cel(c, poly([(hx - 6, hy - 4), (hx - 8.5, hy - 11.5), (hx - 6, hy - 12.5), (hx - 3, hy - 5)]), 'vacht', light=1, shade=(2, 1), deep=0)
    cel(c, disk(hx + 10.5, hy - 9.5, 2, 2.2), 'rood', tones=FAR['rood'], light=0, deep=0)
    cel(c, disk(hx - 9.5, hy - 9.5, 2.4, 2.6), 'rood', light=1, shade=(1, 1), deep=0)
    head = disk(hx + 1, hy, 8, 6.8)
    cel(c, head, 'vacht', light=1, shade=(2, 2), deep=1)
    snout = disk(hx - 5.5, hy + 3.4, 4.6, 3.3)
    cel(c, snout, 'vacht', tones=(5, 5, 6, 6), light=0, shade=(1, 2), deep=0)
    # mini-bolhoedje: koepel + rand
    cel(c, disk(hx + 1.5, hy - 7.6, 4.2, 3.0), 'wol', light=1, shade=(1, 2), deep=0)
    cel(c, disk(hx + 1, hy - 5.4, 6.6, 1.4), 'wol', tones=(2, 2, 3, 3), light=0, shade=(1, 1), deep=0)
    c.outline()
    return c


if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else '.'
    fr = [frame(f).idx.astype(np.uint8) for f in (False, True)]
    save_indexed(os.path.join(d, 'procbase.png'), fr, PAL)
    write_jasc(os.path.join(d, 'normal.pal'), PAL)
    print('ok')
