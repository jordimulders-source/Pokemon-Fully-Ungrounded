"""r8: python3.11 zet.py A|B. Zet tekening_<V>.txt op zijn plek -> raster_<V>.txt (64x64). Geen kleurregels: alleen plaatsen.
Meldt overlappende segmenten met een andere kleur (dan is er een tikfout). Draaien: python3.11 zet.py"""
import sys
from palet import IDX
V = sys.argv[1]
R = [['.'] * 64 for _ in range(64)]; bron = {}
for n, l in enumerate(open(f'tekening_{V}.txt'), 1):
    if not l.strip() or l.startswith('#'): continue
    y, x, s = l.split(); y, x = int(y), int(x)
    for i, c in enumerate(s):
        assert c in IDX, (n, c)
        if x + i > 63: print(f'regel {n}: buiten beeld x={x+i}'); continue
        if R[y][x + i] != '.' and R[y][x + i] != c: print(f'regel {n}: ({x+i},{y}) {R[y][x+i]} (regel {bron[(x+i,y)]}) -> {c}')
        R[y][x + i] = c; bron[(x + i, y)] = n
open(f'raster_{V}.txt', 'w').write(f'# sprite r8{V}, 64x64, één teken per paletkleur (palet.py)\n' + '\n'.join(''.join(r) for r in R) + '\n')
print(f'raster_{V}.txt', sum(c != '.' for r in R for c in r), 'px')
