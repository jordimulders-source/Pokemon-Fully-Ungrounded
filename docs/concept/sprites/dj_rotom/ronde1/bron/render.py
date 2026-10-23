"""DJ Rotom ronde 1: vormen -> Gen 3-cel-shading -> ASCII (daarna handwerk met patch.py).

  python3 render.py uit.txt
Deelt sprlib.py met cuyby/ronde1/bron.
"""
import sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'cuyby', 'ronde1', 'bron'))
from sprlib import *

GLOW = [2, 2, 1, 1]
ORANGE = [3, 4, 5, 6]
STEEL = [7, 7, 8, 9]
CONE = [10, 10, 11, 11]


def frame(k):
    s = Sprite()
    # --- handvat (chroom, achter de kop)
    handle = tube([(13, 28), (13.5, 19.5), (41.5, 19.5), (42, 27)], 1.3, 1.3)
    s.add(handle, STEEL, hl=1, sh=1)
    # --- kast: voorkant, bovenkant (licht), zijkant (schaduw)
    top = poly([(5, 30), (46, 30), (51, 26), (10, 26)])
    side = poly([(46, 30), (51, 26), (51, 51), (46, 55.5)])
    front = rect(5, 30, 46.5, 55.5) & ~((XX < 6) & (YY < 31)) & ~((XX < 6) & (YY > 54.5))
    s.add(top, ORANGE, flat=3)
    s.add(side, ORANGE, flat=5, cast=False)
    s.idx[side & (((YY.astype(int) - 0) % 3) == 0) & (XX > 47) & (XX < 50.5) & (YY > 32) & (YY < 51)] = 6
    s.add(front, ORANGE, hl=1, sh=2, cast=False)
    # --- speakers: stalen rand, donkere conus, ring, stofkap
    pump = 1.0 if k == 1 else 0.0
    for cx in (12.0, 39.5):
        cy = 43.5
        s.add(ell(cx, cy, 6.6, 6.6), STEEL, hl=1, sh=1)
        s.add(ell(cx, cy, 5.2, 5.2), CONE, hl=0, sh=2, line=False)
        ring = ell(cx, cy, 3.6 + pump, 3.6 + pump) & ~ell(cx, cy, 2.6 + pump, 2.6 + pump)
        s.idx[ring] = 10
        s.add(ell(cx - 0.3, cy - 0.3, 1.6 + pump * 0.6, 1.6 + pump * 0.6), STEEL, hl=0, sh=1, line=False, cast=False)
    # --- cassettedek in het midden
    deck = rect(19.5, 41, 32, 53)
    s.add(deck, STEEL, hl=1, sh=1)
    s.add(rect(21, 44, 30.5, 50), CONE, hl=0, sh=0, rim=False, line=False, cast=False)
    # --- Rotom-kop als koepel bovenop (met de kenmerkende kuif)
    head = ell(25.8, 32.5, 11.2, 8.8) & (YY < 40)
    spike = poly([(23.0, 26), (29.5, 26), (28.6, 13.0), (27.6, 12.5)])
    s.add(spike | head, ORANGE, hl=2, sh=2, hl_lim=(14, 12, 27, 31))
    # mond = equalizer-scherm
    s.add(rect(19.5, 33.5, 32, 39), CONE, hl=0, sh=0, rim=False, cast=False)
    eq = [[2, 3, 2, 4, 3], [3, 1, 4, 2, 3]][k]
    for i, h in enumerate(eq):
        x = 21 + 2 * i
        for j in range(h):
            s.idx[37 - j, x] = 1 if j == h - 1 else 2
    # cassettespoeltjes
    for cx in (23, 28):
        s.idx[46:49, cx:cx + 2] = 8
        s.idx[47, cx] = 12
    s.idx[45, 21:31] = 9
    s.outline()
    # --- elektrische gloed rondom (zoals alle Rotom-vormen)
    fig = s.idx > 0
    g1 = dilate(fig, 1) & ~fig
    g2 = dilate(fig, 2, diag=False) & ~fig & ~g1
    s.idx[g1] = 2
    s.idx[g2] = 1
    # --- plasma (zonder zwarte lijn, zoals de armen van de andere vormen):
    # antenne = bliksem die in een muzieknoot eindigt
    # met de hand per pixel (x 43.., y 2..): '2' = plasma, 'c' = witte kern
    NOTE = [
        '........22.....',
        '........2222...',
        '........22c22..',
        '........22.222.',
        '........22..22.',
        '........22...2.',
        '........22.....',
        '.....22222.....',
        '....22cc22.....',
        '....22cc2......',
        '.....222.......',
        '......22.......',
        '.....22........',
        '.....2c........',
        '....2c2........',
        '....2c2222.....',
        '....2cccc2.....',
        '....22222c2....',
        '.......2c2.....',
        '......2c2......',
        '......2c2......',
        '.....2c2.......',
        '....2c2........',
        '...2c2.........',
        '...22..........',
    ]
    pl = np.zeros((S, S), bool)
    ox, oy = (43, 2) if k == 0 else (44, 2)
    if k == 1:
        NOTE = [r.replace('c', '2') for r in NOTE[:11]] + NOTE[11:]
    for j, row in enumerate(NOTE):
        for i, ch in enumerate(row):
            y, x = oy + j, ox + i
            if k == 1 and j >= 11:
                x -= 1; y += 1     # bliksem blijft op de kast staan
            if ch != '.' and s.idx[y, x] in (0, 1, 2):
                s.idx[y, x] = {'2': 2, 'c': 12}[ch]
                pl[y, x] = True
    ring = dilate(pl, 1) & ~pl & ((s.idx == 0) | (s.idx == 1))
    s.idx[ring] = 1
    if k == 1:
        # geluidsgolven links (bogen van gloed)
        for r in (3.5, 6.0):
            arc = (ell(12, 43.5, 6.6 + r + 0.7, 6.6 + r + 0.7) & ~ell(12, 43.5, 6.6 + r - 0.5, 6.6 + r - 0.5)
                   & (XX < 12 - 6.0) & (np.abs(YY - 43.5) < 3.5 + r * 0.6))
            arc &= (s.idx == 0) & (XX > 2)
            s.idx[arc] = 2
            s.idx[dilate(arc, 1) & ~arc & (s.idx == 0)] = 1
    return s.idx


if __name__ == '__main__':
    write_txt(sys.argv[1], [frame(0), frame(1)])
