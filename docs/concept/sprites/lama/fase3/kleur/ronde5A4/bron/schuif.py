"""Ronde 5A4: de bombin van 5A3 exact 1 rij omlaag. De hoedcellen staan hier met de hand opgesomd; de vrijgekomen cellen
krijgen met de hand wat erachter zat (oor/leeg). Het oog (x22-26 y14-18) is bevroren: het zakkende rechterdeel van de rand
landt alleen op x27-30 (bovenkant van de vlecht)."""
import os
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(H); K = os.path.join(H, '../..')
LET = '.kHCSdRUBDrmpyGg'
PAL = [tuple(map(int, l.split())) for l in open(os.path.join(OUT, 'normal.pal')).read().split('\n')[3:19]]
src = [list(l) for l in open(os.path.join(K, 'ronde5A3/ronde5A3.txt')).read().split('\n')[:64]]
g = [r[:] for r in src]
HOED = {6: range(22, 25), 7: range(20, 27), 8: range(19, 27), 9: range(19, 27), 10: range(19, 27), 11: range(19, 27),
        12: range(16, 30), 13: range(24, 31)}
cells = {(x, y) for y, xs in HOED.items() for x in xs}
# 1. vrijgekomen cellen (met de hand): oor of leeg
VUL = {(22, 6): '.', (23, 6): '.', (24, 6): '.', (20, 7): 'C', (21, 7): 'k', (25, 7): '.', (26, 7): 'd', (19, 8): 'd',
       (16, 12): '.', (17, 12): '.', (18, 12): '.', (27, 12): 'k', (28, 12): 'k', (29, 12): '.', (30, 13): '.'}
VUL_OOR = {(27, 11): 'C'}   # rechteroor loopt door waar de hoed is gezakt (geen hoedcel in 5A3, wel oorvlak)
for (x, y), c in list(VUL.items()) + list(VUL_OOR.items()): g[y][x] = c
# 2. hoed 1 rij omlaag (niet op het bevroren oog)
for (x, y) in sorted(cells, key=lambda t: -t[1]):
    if 22 <= x <= 26 and 14 <= y + 1 <= 18: continue
    g[y + 1][x] = src[y][x]
open(os.path.join(OUT, 'ronde5A4.txt'), 'w').write('\n'.join(''.join(r) for r in g) + '\n')
G = np.array(g); B = np.array(src); A = G != '.'
ch = list(zip(*np.nonzero(G != B)))
print('gewijzigd t.o.v. 5A3:', len(ch), '| buiten y6-14:', [c for c in ch if not 6 <= c[0] <= 14], '| in het oog:', [c for c in ch if 14 <= c[0] <= 18 and 22 <= c[1] <= 26])
S = np.array([[c == '#' for c in l] for l in open(os.path.join(K, 'kopbron/silhouet_A.txt')).read().split('\n')[:64]])
print(f'buiten silhouet_A: +{int((A & ~S).sum())}', ' '.join(f'x{x}y{y}' for y, x in zip(*np.nonzero(A & ~S))))
print(f'silhouet_A leeg: -{int((S & ~A).sum())}', ' '.join(f'x{x}y{y}' for y, x in zip(*np.nonzero(S & ~A))))
o = [f'{G[y,x]}@x{x},y{y}' for y, x in zip(*np.nonzero(A)) if G[y, x] not in 'kdDm' and any(not (0 <= y+a < 64 and 0 <= x+b < 64) or not A[y+a, x+b] for a, b in ((-1,0),(1,0),(0,-1),(0,1)))]
print('open randen:', len(o), ' '.join(o))
idx = np.vectorize(LET.index)(G).astype(np.uint8)
im = Image.fromarray(idx, 'P'); flat = [v for c in PAL for v in c]; im.putpalette(flat + [0] * (768 - len(flat)))
im.save(os.path.join(OUT, 'lama3.png'), transparency=0); print('kleuren:', len(set(G[A].ravel())))
for y in range(0, 17): print('%2d  ' % y + ''.join(g[y][10:34]))
