"""Kleur ronde 2 lama fase 3: ronde1b.txt + met de hand getypte wijzigingen (wijzigingen.txt: 'y x0 pixels', '.' = transparant)
-> ronde2.txt, lama3.png, normal.pal. Alleen plaatsen en controleren (geen tint- of vormlogica).
Controles: letters, alpha-diff met silhouet/ronde2.txt (alleen de gemelde bombin-pixels mogen erbij), open randen, telling gewijzigde px."""
import os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
SIL = os.path.join(HERE, '../../../silhouet/ronde2.txt'); R1B = os.path.join(HERE, '../../ronde1b/ronde1b.txt')
LET = '.kHCSdRUBDrmpyGg'
PAL = [tuple(map(int, l.split())) for l in open(os.path.join(OUT, 'normal.pal')).read().split('\n')[3:19]]
TOEGESTAAN = {(22, 4), (23, 4), (17, 9), (18, 9)}   # bombin buiten het silhouet (gemeld in NOTITIES)
base = [list(l.rstrip('\n')) for l in open(R1B) if l.strip()]
grid = [r[:] for r in base]; seen = {}
for ln, line in enumerate(open(os.path.join(HERE, 'wijzigingen.txt')), 1):
    if line.startswith('#') or not line.strip(): continue
    y, x0, px = line.split(); y, x0 = int(y), int(x0)
    for i, c in enumerate(px):
        x = x0 + i
        if c not in LET: sys.exit(f'regel {ln}: onbekende letter {c!r}')
        if (x, y) in seen: sys.exit(f'regel {ln}: pixel x{x} y{y} dubbel (ook regel {seen[(x, y)]})')
        seen[(x, y)] = ln; grid[y][x] = c
open(os.path.join(OUT, 'ronde2.txt'), 'w').write('\n'.join(''.join(r) for r in grid) + '\n')
G = np.array(grid); A = G != '.'; B = np.array(base)
S = np.array([[c == '#' for c in l.rstrip('\n')] for l in open(SIL) if l.strip()])
plus = [(x, y) for y, x in zip(*np.nonzero(A & ~S))]; minus = [(x, y) for y, x in zip(*np.nonzero(S & ~A))]
print(f'px {int(A.sum())} | silhouet {int(S.sum())} | alpha-diff: +{len(plus)} -{len(minus)}')
for x, y in plus: print(f'   + x{x} y{y} {G[y, x]}' + ('  (bombin, toegestaan)' if (x, y) in TOEGESTAAN else '  FOUT'))
for x, y in minus: print(f'   - x{x} y{y}  FOUT')
ch = np.nonzero(G != B); zones = {}
for y, x in zip(*ch):
    z = 'kop/bombin/vlecht (y0-23)' if y <= 23 else ('poten (y40-63)' if y >= 40 else 'lijf (y24-39)')
    zones[z] = zones.get(z, 0) + 1
print('gewijzigd t.o.v. ronde 1b:', len(ch[0]), zones)
openr = []
for y, x in zip(*np.nonzero(A)):
    if G[y, x] in 'kdDm': continue
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        v, u = y + dy, x + dx
        if not (0 <= v < 64 and 0 <= u < 64) or not A[v, u]: openr.append((x, y, G[y, x])); break
print(f'open randen (vulkleur naast transparant): {len(openr)}', ' '.join(f'{c}@x{x},y{y}' for x, y, c in openr))
idx = np.vectorize(LET.index)(G).astype(np.uint8)
im = Image.fromarray(idx, 'P'); flat = [v for c in PAL for v in c]; im.putpalette(flat + [0] * (768 - len(flat)))
im.save(os.path.join(OUT, 'lama3.png'), transparency=0)
used = sorted(set(G[A].ravel())); print('kleuren gebruikt:', len(used), ''.join(used))
