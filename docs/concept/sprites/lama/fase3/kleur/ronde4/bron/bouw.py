"""Kleur ronde 4 lama fase 3: ronde2b.txt met de kopzone (x8-35, y0-25) vervangen door kop.txt ('=' = 2b houden).
Controles: 0 px diff buiten de kopzone, diff kop vs. bron (onderdeel per cel), afwijkingen van kop_lijnen, buiten silhouet, open randen."""
import os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
KB = os.path.join(HERE, '../../kopbron')
SIL = os.path.join(HERE, '../../../silhouet/ronde2.txt'); BASE = os.path.join(HERE, '../../ronde2b/ronde2b.txt')
LET = '.kHCSdRUBDrmpyGg'
PAL = [tuple(map(int, l.split())) for l in open(os.path.join(OUT, 'normal.pal')).read().split('\n')[3:19]]
base = [list(l.rstrip('\n')) for l in open(BASE) if l.strip()]
rows = [l.rstrip('\n') for l in open(os.path.join(HERE, 'kop.txt')) if not l.startswith('#') and l.strip()]
lab = [l[5:] for l in open(os.path.join(KB, 'kop_labels.txt')) if l.startswith('y')]
lij = [l[5:] for l in open(os.path.join(KB, 'kop_lijnen.txt')) if l.startswith('y')]
assert len(rows) == 26, len(rows)
grid = [r[:] for r in base]
for y, r in enumerate(rows):
    if len(r) != 28: sys.exit(f'kop.txt y{y}: lengte {len(r)}')
    for i, c in enumerate(r):
        if c == '=': continue
        if c not in LET: sys.exit(f'y{y}: onbekende letter {c!r}')
        grid[y][8 + i] = c
open(os.path.join(OUT, 'ronde4.txt'), 'w').write('\n'.join(''.join(r) for r in grid) + '\n')
G = np.array(grid); A = G != '.'; B = np.array(base)
d = np.nonzero(G != B)
print(f'gewijzigd t.o.v. 2b: {len(d[0])} px; buiten de kopzone: {sum(1 for y, x in zip(*d) if not (y <= 25 and 8 <= x <= 35))}')
# onderdeel-diff: leeg/gevuld en kleurfamilie per label
CREME, DONKER = set('HCSd'), set('kdS')
fam = {'K': CREME | {'k'}, 'N': CREME | {'k'}, 'p': CREME | {'k'}, 'l': CREME | {'k'}, 'O': CREME | {'k'}, 'D': CREME | {'k'}, 'E': {'k', 'd', 'S'},
       'H': DONKER, 'B': set('RrmkS') , 'V': DONKER}
mis = []
for y in range(26):
    for i in range(28):
        x = 8 + i; L = lab[y][i]; c = G[y, x]
        if L == 'x': continue
        if L == '.':
            if c != '.' and rows[y][i] != '=': mis.append(f'x{x}y{y} leeg in bron, sprite {c}')
            continue
        if c == '.': mis.append(f'x{x}y{y} {L} in bron, sprite leeg'); continue
        if c not in fam[L]: mis.append(f'x{x}y{y} {L} in bron, sprite {c}')
print(f'onderdeel wijkt af van de bron: {len(mis)}'); [print('   ' + m) for m in mis]
lijn = []
for y in range(26):
    for i in range(28):
        x = 8 + i; L = lab[y][i]
        if L in '.x': continue
        isl = lij[y][i] == '#'; c = G[y, x]
        if L in 'KNplODE' and isl and c not in 'dk': lijn.append(f'x{x}y{y} lijn in bron, sprite {c}')
        if L in 'KNplOD' and not isl and c in 'dk' and not (L == 'K' and c == 'k' and False): lijn.append(f'x{x}y{y} geen lijn in bron, sprite {c}')
print(f'lijnafwijkingen (crème onderdelen): {len(lijn)}'); [print('   ' + m) for m in lijn]
S = np.array([[c == '#' for c in l.rstrip('\n')] for l in open(SIL) if l.strip()])
print(f'px {int(A.sum())} | buiten silhouet +{int((A & ~S).sum())} | silhouet leeg -{int((S & ~A).sum())}')
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
print('kleuren:', len(set(G[A].ravel())))
