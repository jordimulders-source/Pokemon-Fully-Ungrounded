"""Kleur ronde 5A lama fase 3: lijf_overgezet.txt (overzet.py) + lijf_reparaties.txt (hand) + kop.txt (hand, x8-35 y0-25).
Controles: alpha-diff met kopbron/silhouet_A.txt, onderdeel-diff kop vs. kop_labels_A, lijnafwijkingen, open randen."""
import os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE); KB = os.path.join(HERE, '../../kopbron')
LET = '.kHCSdRUBDrmpyGg'
PAL = [tuple(map(int, l.split())) for l in open(os.path.join(OUT, 'normal.pal')).read().split('\n')[3:19]]
grid = [list(l) for l in open(os.path.join(HERE, 'lijf_overgezet.txt')).read().split('\n')[:64]]
for l in open(os.path.join(HERE, 'lijf_reparaties.txt')):
    if l.startswith('#') or not l.strip(): continue
    x, y, c = l.split(); grid[int(y)][int(x)] = c
rows = [l.rstrip('\n') for l in open(os.path.join(HERE, 'kop.txt')) if not l.startswith('#') and l.strip()]
assert len(rows) == 26
for y, r in enumerate(rows):
    if len(r) != 28: sys.exit(f'kop y{y}: lengte {len(r)}')
    for i, c in enumerate(r):
        if c not in LET: sys.exit(f'y{y}: letter {c!r}')
        grid[y][8 + i] = c
open(os.path.join(OUT, 'ronde5A.txt'), 'w').write('\n'.join(''.join(r) for r in grid) + '\n')
G = np.array(grid); A = G != '.'
S = np.array([[c == '#' for c in l] for l in open(os.path.join(KB, 'silhouet_A.txt')).read().split('\n')[:64]])
print(f'px {int(A.sum())} | silhouet_A {int(S.sum())} | alpha-diff +{int((A & ~S).sum())} -{int((S & ~A).sum())}')
for y, x in zip(*np.nonzero(A ^ S)): print(f'   {"+" if A[y, x] else "-"} x{x} y{y}')
lab = [l[5:] for l in open(os.path.join(KB, 'kop_labels_A.txt')) if l.startswith('y')]
lij = [l[5:] for l in open(os.path.join(KB, 'kop_lijnen_A.txt')) if l.startswith('y')]
CREME = set('HCSdk'); fam = {k: CREME for k in 'KNplOD'}; fam.update({'E': set('kdSH'), 'H': set('kdSRrm'), 'B': set('RrmkS'), 'V': set('kdS')})
mis = []
for y in range(26):
    for i in range(28):
        L = lab[y][i]; c = G[y, 8 + i]
        if L == 'x': continue
        if L == '.':
            if c != '.': mis.append(f'x{8+i}y{y} leeg in bron, sprite {c}')
        elif c == '.' or c not in fam[L]: mis.append(f'x{8+i}y{y} {L} in bron, sprite {c}')
print(f'onderdeel wijkt af van de bron: {len(mis)}'); [print('   ' + m) for m in mis]
lijn = [f'x{8+i}y{y} {"lijn in bron" if lij[y][i]=="#" else "geen lijn"}, sprite {G[y, 8+i]}' for y in range(26) for i in range(28)
        if lab[y][i] in 'KNplOD' and ((lij[y][i] == '#') != (G[y, 8 + i] in 'dk'))]
print(f'lijnafwijkingen (crème onderdelen): {len(lijn)}'); [print('   ' + m) for m in lijn]
openr = []
for y, x in zip(*np.nonzero(A)):
    if G[y, x] in 'kdDm': continue
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        v, u = y + dy, x + dx
        if not (0 <= v < 64 and 0 <= u < 64) or not A[v, u]: openr.append(f'{G[y, x]}@x{x},y{y}'); break
print(f'open randen: {len(openr)}', ' '.join(openr))
idx = np.vectorize(LET.index)(G).astype(np.uint8)
im = Image.fromarray(idx, 'P'); flat = [v for c in PAL for v in c]; im.putpalette(flat + [0] * (768 - len(flat)))
im.save(os.path.join(OUT, 'lama3.png'), transparency=0); print('kleuren:', len(set(G[A].ravel())))
