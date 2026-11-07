import numpy as np, sys
sys.path.insert(0, sys.argv[1]); S = sys.argv[1]
from PIL import Image, ImageDraw
from common import PAL, show
g = np.load(S + '/stap1.npy', allow_pickle=True)
ROLE2 = {'PB': 'P', 'PS': 'p'}
for y in range(64):
    for x in range(64):
        g[y, x] = ROLE2.get(g[y, x], g[y, x])
# kop: ' ' = laten staan, '.' = transparant (x 0..15, vanaf y 28)
KOP = """
................
................
.......        .
........QQQKKKL.
......QQgggKHBLH
.....QgggggLHBLH
....QggggGGGLLHH
....QgggGGGGGHHH
...QggGGGGGGGBHH
...QgGGGGGGGGBBB
...QgGGGGGGGGBBB
...QGGGGGGGGGqBB
..QGGKKKKGGGqqSB
..KKKKKKWEKGqqSB
..KKKKKKEeKqqqSB
.QGGKKKKKKqqqqSS
.QgGGGGGGGqqqSSS
PpGGGGGGGqqqqSSS
PPpqGGGGqqqqKSSS
KPKKqqqqq    KSS
..KK          K 
"""
rows = KOP.strip('\n').split('\n')
for j, r in enumerate(rows):
    for i, c in enumerate(r):
        if c != ' ': g[28 + j, i] = c
np.save(S + '/stap2.npy', g)
show(g, S + '/stap2.png'); show(g, S + '/stap2_1x.png', 1)
