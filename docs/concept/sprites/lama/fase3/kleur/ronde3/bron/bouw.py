"""Kleur ronde 3 lama fase 3: ronde2b.txt met de kopzone (y0-21, x10-33) vervangen door kop.txt (met de hand getekend).
Alleen plaatsen en controleren: letters, 0 px diff buiten de kopzone, pixels buiten het silhouet (per zone), open randen."""
import os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
SIL = os.path.join(HERE, '../../../silhouet/ronde2.txt'); BASE = os.path.join(HERE, '../../ronde2b/ronde2b.txt')
LET = '.kHCSdRUBDrmpyGg'
PAL = [tuple(map(int, l.split())) for l in open(os.path.join(OUT, 'normal.pal')).read().split('\n')[3:19]]
base = [list(l.rstrip('\n')) for l in open(BASE) if l.strip()]
rows = [l.rstrip('\n') for l in open(os.path.join(HERE, 'kop.txt')) if not l.startswith('#') and l.strip()]
if len(rows) != 22: sys.exit(f'kop.txt: {len(rows)} rijen, verwacht 22')
grid = [r[:] for r in base]
for y, r in enumerate(rows):
    if len(r) != 24: sys.exit(f'kop.txt rij y{y}: lengte {len(r)}')
    for i, c in enumerate(r):
        if c not in LET: sys.exit(f'y{y}: onbekende letter {c!r}')
        grid[y][10 + i] = c
open(os.path.join(OUT, 'ronde3.txt'), 'w').write('\n'.join(''.join(r) for r in grid) + '\n')
G = np.array(grid); A = G != '.'; B = np.array(base)
S = np.array([[c == '#' for c in l.rstrip('\n')] for l in open(SIL) if l.strip()])
diff = np.nonzero(G != B)
buiten = [(x, y) for y, x in zip(*diff) if not (y <= 21 and 10 <= x <= 33)]
print(f'gewijzigd t.o.v. ronde 2b: {len(diff[0])} px; buiten de kopzone: {len(buiten)}')
plus = [(x, y) for y, x in zip(*np.nonzero(A & ~S))]; minus = [(x, y) for y, x in zip(*np.nonzero(S & ~A))]
def zone(x, y):
    if y <= 2: return 'oren'
    if y <= 9 and x <= 27: return 'bombin/oren'
    if x >= 27: return 'vlecht'
    return 'kop'
zp, zm = {}, {}
for x, y in plus: zp[zone(x, y)] = zp.get(zone(x, y), []) + [f'x{x}y{y}']
for x, y in minus: zm[zone(x, y)] = zm.get(zone(x, y), []) + [f'x{x}y{y}']
print(f'px {int(A.sum())} | silhouet {int(S.sum())} | buiten silhouet +{len(plus)} | silhouet niet gevuld -{len(minus)}')
for k, v in zp.items(): print(f'   + {k}: {len(v)}  ' + ' '.join(v))
for k, v in zm.items(): print(f'   - {k}: {len(v)}  ' + ' '.join(v))
openr = []
for y, x in zip(*np.nonzero(A)):
    if G[y, x] in 'kdDm': continue
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        v, u = y + dy, x + dx
        if not (0 <= v < 64 and 0 <= u < 64) or not A[v, u]: openr.append(f'{G[y, x]}@x{x},y{y}'); break
print(f'open randen: {len(openr)}', ' '.join(openr))
idx = np.vectorize(LET.index)(G).astype(np.uint8)
im = Image.fromarray(idx, 'P'); flat = [v for c in PAL for v in c]; im.putpalette(flat + [0] * (768 - len(flat)))
im.save(os.path.join(OUT, 'lama3.png'), transparency=0)
used = sorted(set(G[A].ravel())); print('kleuren gebruikt:', len(used), ''.join(used))
