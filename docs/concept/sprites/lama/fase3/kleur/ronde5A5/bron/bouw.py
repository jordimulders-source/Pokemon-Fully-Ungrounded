"""Ronde 5A5: ronde5A4.txt + wijzigingen.txt (hand). Controles: diff per zone, oog/rechterhoed 0, alpha-diff, open randen."""
import os
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(H); K = os.path.join(H, '../..')
LET = '.kHCSdRUBDrmpyGg'
PAL = [tuple(map(int, l.split())) for l in open(os.path.join(OUT, 'normal.pal')).read().split('\n')[3:19]]
base = [list(l) for l in open(os.path.join(K, 'ronde5A4/ronde5A4.txt')).read().split('\n')[:64]]; g = [r[:] for r in base]
for l in open(os.path.join(H, 'wijzigingen.txt')):
    if l.startswith('#') or not l.strip(): continue
    x, y, c = l.split(); g[int(y)][int(x)] = c
open(os.path.join(OUT, 'ronde5A5.txt'), 'w').write('\n'.join(''.join(r) for r in g) + '\n')
G = np.array(g); B = np.array(base); A = G != '.'
ch = list(zip(*np.nonzero(G != B)))
hoed = [c for c in ch if c[0] <= 13 and c[1] <= 23]; poot = [c for c in ch if 47 <= c[0] <= 58 and 33 <= c[1] <= 40]
print(f'gewijzigd t.o.v. 5A4: {len(ch)} (bombin links {len(hoed)}, verre achterpoot {len(poot)}, elders {len(ch)-len(hoed)-len(poot)})')
print('alpha t.o.v. 5A4:', ' '.join(f'{"+" if A[y,x] else "-"}x{x}y{y}' for y, x in zip(*np.nonzero(A != (B != '.')))))
o = [f'{G[y,x]}@x{x},y{y}' for y, x in zip(*np.nonzero(A)) if G[y, x] not in 'kdDm' and any(not (0 <= y+a < 64 and 0 <= x+b < 64) or not A[y+a, x+b] for a, b in ((-1,0),(1,0),(0,-1),(0,1)))]
print('open randen:', len(o), ' '.join(o))
idx = np.vectorize(LET.index)(G).astype(np.uint8)
im = Image.fromarray(idx, 'P'); flat = [v for c in PAL for v in c]; im.putpalette(flat + [0] * (768 - len(flat)))
im.save(os.path.join(OUT, 'lama3.png'), transparency=0); print('kleuren:', len(set(G[A].ravel())))
for y in range(46, 61): print('%2d  ' % y + ''.join(g[y][28:50]))
