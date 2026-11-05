"""Ronde 5A2: ronde5A.txt + wijzigingen.txt (hand). Controles: alleen oog (x21-27 y13-18) en vlecht (labels V) gewijzigd,
alpha-diff met silhouet_A, open randen."""
import os
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(H); K = os.path.join(H, '../..')
LET = '.kHCSdRUBDrmpyGg'
PAL = [tuple(map(int, l.split())) for l in open(os.path.join(OUT, 'normal.pal')).read().split('\n')[3:19]]
base = [list(l) for l in open(os.path.join(K, 'ronde5A/ronde5A.txt')).read().split('\n')[:64]]
g = [r[:] for r in base]
for l in open(os.path.join(H, 'wijzigingen.txt')):
    if l.startswith('#') or not l.strip(): continue
    x, y, c = l.split(); g[int(y)][int(x)] = c
open(os.path.join(OUT, 'ronde5A2.txt'), 'w').write('\n'.join(''.join(r) for r in g) + '\n')
G = np.array(g); B = np.array(base); A = G != '.'
lab = [l[5:] for l in open(os.path.join(K, 'kopbron/kop_labels_A.txt')) if l.startswith('y')]
ch = list(zip(*np.nonzero(G != B)))
oog = [(y, x) for y, x in ch if 21 <= x <= 27 and 13 <= y <= 18 and not (y < 26 and 8 <= x < 36 and lab[y][x - 8] == 'V')]
vl = [(y, x) for y, x in ch if y < 26 and 8 <= x < 36 and lab[y][x - 8] == 'V']
rest = [(y, x) for y, x in ch if (y, x) not in oog and (y, x) not in vl]
print(f'gewijzigd t.o.v. 5A: {len(ch)} (oog {len(oog)}, vlecht {len(vl)}, elders {len(rest)} {rest})')
S = np.array([[c == '#' for c in l] for l in open(os.path.join(K, 'kopbron/silhouet_A.txt')).read().split('\n')[:64]])
print(f'alpha-diff met silhouet_A: +{int((A & ~S).sum())} -{int((S & ~A).sum())}')
o = [f'{G[y,x]}@x{x},y{y}' for y, x in zip(*np.nonzero(A)) if G[y, x] not in 'kdDm' and any(not (0 <= y+a < 64 and 0 <= x+b < 64) or not A[y+a, x+b] for a, b in ((-1,0),(1,0),(0,-1),(0,1)))]
print('open randen:', len(o), ' '.join(o))
idx = np.vectorize(LET.index)(G).astype(np.uint8)
im = Image.fromarray(idx, 'P'); flat = [v for c in PAL for v in c]; im.putpalette(flat + [0] * (768 - len(flat)))
im.save(os.path.join(OUT, 'lama3.png'), transparency=0); print('kleuren:', len(set(G[A].ravel())))
