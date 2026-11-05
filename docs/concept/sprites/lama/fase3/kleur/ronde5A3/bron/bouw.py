"""Ronde 5A3: ronde5A2.txt + wijzigingen.txt (hand). Controles: diff per zone t.o.v. 5A2, oog t.o.v. 5A, buiten silhouet_A, open randen."""
import os
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(H); K = os.path.join(H, '../..')
LET = '.kHCSdRUBDrmpyGg'
PAL = [tuple(map(int, l.split())) for l in open(os.path.join(OUT, 'normal.pal')).read().split('\n')[3:19]]
rd = lambda p: [list(l) for l in open(os.path.join(K, p)).read().split('\n')[:64]]
base = rd('ronde5A2/ronde5A2.txt'); r5a = rd('ronde5A/ronde5A.txt'); g = [r[:] for r in base]
for l in open(os.path.join(H, 'wijzigingen.txt')):
    if l.startswith('#') or not l.strip(): continue
    p = l.split()
    if p[0] == 'R':
        for i, c in enumerate(p[3]): g[int(p[1])][int(p[2]) + i] = c
    else: g[int(p[2])][int(p[1])] = p[3]
open(os.path.join(OUT, 'ronde5A3.txt'), 'w').write('\n'.join(''.join(r) for r in g) + '\n')
G = np.array(g); B = np.array(base); A = G != '.'
ch = list(zip(*np.nonzero(G != B)))
hoed = [c for c in ch if c[0] <= 13]; oog = [c for c in ch if 14 <= c[0] <= 18 and 22 <= c[1] <= 26]; rest = [c for c in ch if c not in hoed and c not in oog]
print(f'gewijzigd t.o.v. 5A2: {len(ch)} (hoed/kop y0-13: {len(hoed)}, oog: {len(oog)}, elders: {len(rest)} {rest})')
R = np.array(r5a); od = [(x, y, R[y, x], G[y, x]) for y in range(14, 19) for x in range(22, 27) if R[y, x] != G[y, x]]
print('oog t.o.v. 5A:', len(od), ' '.join(f'x{x}y{y} {a}->{b}' for x, y, a, b in od))
S = np.array([[c == '#' for c in l] for l in open(os.path.join(K, 'kopbron/silhouet_A.txt')).read().split('\n')[:64]])
print(f'buiten silhouet_A: +{int((A & ~S).sum())}', ' '.join(f'x{x}y{y}' for y, x in zip(*np.nonzero(A & ~S))))
print(f'silhouet_A leeg: -{int((S & ~A).sum())}', ' '.join(f'x{x}y{y}' for y, x in zip(*np.nonzero(S & ~A))))
o = [f'{G[y,x]}@x{x},y{y}' for y, x in zip(*np.nonzero(A)) if G[y, x] not in 'kdDm' and any(not (0 <= y+a < 64 and 0 <= x+b < 64) or not A[y+a, x+b] for a, b in ((-1,0),(1,0),(0,-1),(0,1)))]
print('open randen:', len(o), ' '.join(o))
idx = np.vectorize(LET.index)(G).astype(np.uint8)
im = Image.fromarray(idx, 'P'); flat = [v for c in PAL for v in c]; im.putpalette(flat + [0] * (768 - len(flat)))
im.save(os.path.join(OUT, 'lama3.png'), transparency=0); print('kleuren:', len(set(G[A].ravel())))
