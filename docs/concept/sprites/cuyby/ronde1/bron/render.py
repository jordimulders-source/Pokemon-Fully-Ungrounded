"""Cuyby ronde 1: vormen -> Gen 3-cel-shading -> ASCII (daarna handwerk met patch.py).

  python3 render.py A uit.txt     (A = rozet-kuif, B = chullo-muts)
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sprlib import *

CREAM = [1, 2, 3, 4]
GINGER = [5, 6, 7, 8]
PINK = [9, 9, 10, 10]
RED = [13, 13, 14, 14]
TONE = {1: 5, 2: 6, 3: 7, 4: 8}          # crème-tint -> gember-tint


def recolor(s, m, tone):
    for a, b in tone.items():
        s.idx[m & (s.idx == a)] = b


def frame(var, k):
    dy = -3 if k == 1 else 0                 # frame 2: 'popcorn'-sprongetje
    s = Sprite()
    E = lambda cx, cy, rx, ry, rot=0.0: ell(cx, cy + dy, rx, ry, rot)
    # verre poten (achter het lijf)
    if k == 0:
        s.add(E(47, 54.8, 3.0, 1.8), [6, 7, 8, 8], hl=0, sh=1)
    # verre oor
    if var == 'A':
        s.add(E(34.5, 28.0, 3.6, 3.0, -0.7), [9, 10, 10, 8], hl=0, sh=1)
    # romp: een korte ronde 'broodvorm' achter de kop
    body = E(37, 45.5, 13.5, 9.8) | E(44, 49, 7, 6)
    s.add(body, GINGER, hl=1, sh=2, hl_lim=(28, 34 + dy, 44, 42 + dy))
    belly = body & E(30, 54, 12, 5.5)
    recolor(s, belly, {5: 1, 6: 2, 7: 3, 8: 4})
    if var == 'A':
        # rozet-spiraal op de heup (Abessijnse cavia: kruinen in de vacht)
        cx, cy = 42.5, 44.0 + dy
        t = np.linspace(0, 2.5 * np.pi, 200)
        r = 0.6 + 0.85 * t
        sp = np.zeros((S, S), bool)
        for tt, rr in zip(t, r):
            x, y = cx + rr * np.cos(tt + 0.4), cy + 0.85 * rr * np.sin(tt + 0.4)
            sp[int(y), int(x)] = True
        sp &= body & ~belly
        s.idx[sp & (s.idx != 15)] = 8
    # kop: groot (fase 1), gember met crème bles en snoet
    head = E(22.5, 39.5, 13.4, 12.3)
    s.add(head, GINGER, hl=2, sh=2, hl_lim=(9, 27 + dy, 25, 37 + dy))
    blaze = head & (E(18.5, 37, 2.6, 10) | E(15.5, 46.5, 7.5, 5.0) | E(25, 50.5, 9, 3))
    recolor(s, blaze, {5: 1, 6: 2, 7: 3, 8: 4})
    if var == 'A':
        # kruin-kuif: drie plukken in een waaier (de rozet als silhouetbreker)
        s.add(E(19.0, 26.5, 2.2, 4.0, -0.8), GINGER, hl=1, sh=1)
        s.add(E(26.8, 25.8, 2.2, 4.0, 0.7), GINGER, hl=0, sh=1)
        s.add(E(22.8, 23.5 - (1 if k == 1 else 0), 2.6, 5.0, 0.05), GINGER, hl=1, sh=1)
        s.add(E(22.8, 28.5, 4.0, 2.0), GINGER, hl=0, sh=1, line=False)
        # dicht oor (rond, hangend, roze binnenkant)
        s.add(E(10.5, 32.0, 3.6, 3.3, 0.6), [9, 9, 10, 8], hl=0, sh=1)
    else:
        # chullo: pompon, kap, geweven band, oorflappen met kwastjes
        s.add(E(22.5, 23.0 - (1 if k == 1 else 0), 3.8, 3.5), RED, hl=1, sh=1)
        cap = E(22.5, 34.5, 13.2, 9.0) & (YY < 34.5 + dy)
        s.add(cap, CREAM, hl=2, sh=1, cast=False, hl_lim=(9, 23 + dy, 24, 33 + dy))
        band = E(22.5, 34.5, 13.8, 9.6) & (YY >= 30.5 + dy) & (YY < 34.5 + dy)
        s.add(band, RED, hl=0, sh=0, rim=False, cast=False)
        ix = XX.astype(int); iy = (YY - dy).astype(int)
        diam = (np.abs(((ix - 1) % 6) - 3) + np.abs(iy - 32.5) <= 1.6)
        s.idx[band & diam & (s.idx != 15)] = 1
        # flappen
        s.add(poly([(7, 34 + dy), (11.5, 34 + dy), (11.2, 43 + dy), (9.5, 45.5 + dy), (7.2, 41 + dy)]), RED, hl=0, sh=1, cast=False)
        s.add(poly([(32.5, 34 + dy), (36, 34 + dy), (36.5, 40 + dy), (35, 43 + dy), (33.5, 40 + dy)]), [13, 14, 14, 14], hl=0, sh=1, cast=False)
        s.add(E(9.3, 47.3, 1.8, 1.8), CREAM, hl=0, sh=1)
        s.add(E(35.2, 45.0, 1.6, 1.6), CREAM, hl=0, sh=1)
    # dichte voorpootjes
    if k == 0:
        s.add(E(25.5, 53.3, 2.4, 1.7), [2, 3, 4, 4], hl=0, sh=1)
        s.add(E(16.8, 52.6, 2.8, 1.8), CREAM, hl=0, sh=1)
        s.add(E(39.5, 55.6, 3.4, 1.8), GINGER, hl=0, sh=1)
    else:
        s.add(E(18, 52.4, 2.4, 1.6), CREAM, hl=0, sh=1)
        s.add(E(40, 54.6, 2.8, 1.6), GINGER, hl=0, sh=1)
    s.outline()
    return s.idx


if __name__ == '__main__':
    var, out = sys.argv[1], sys.argv[2]
    write_txt(out, [frame(var, 0), frame(var, 1)])
