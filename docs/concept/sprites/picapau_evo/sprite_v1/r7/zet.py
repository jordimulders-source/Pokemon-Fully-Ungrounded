"""Zet de handgetekende segmenten uit tekening.txt op hun plek -> raster.txt (64x64). Geen kleurregels: alleen plaatsen.
Meldt overlappende segmenten met een andere kleur (dan is er een tikfout). Draaien: python3.11 zet.py"""
from palet import IDX
R = [['.'] * 64 for _ in range(64)]; bron = {}
for n, l in enumerate(open('tekening.txt'), 1):
    if not l.strip() or l.startswith('#'): continue
    y, x, s = l.split(); y, x = int(y), int(x)
    for i, c in enumerate(s):
        assert c in IDX, (n, c)
        if x + i > 63: print(f'regel {n}: buiten beeld x={x+i}'); continue
        if R[y][x + i] != '.' and R[y][x + i] != c: print(f'regel {n}: ({x+i},{y}) {R[y][x+i]} (regel {bron[(x+i,y)]}) -> {c}')
        R[y][x + i] = c; bron[(x + i, y)] = n
open('raster.txt', 'w').write('# sprite r7, 64x64, één teken per paletkleur (palet.py)\n' + '\n'.join(''.join(r) for r in R) + '\n')
print('raster.txt', sum(c != '.' for r in R for c in r), 'px')
