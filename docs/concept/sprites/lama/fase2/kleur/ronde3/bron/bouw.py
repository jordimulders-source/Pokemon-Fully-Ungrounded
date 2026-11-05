"""Kleur ronde 3: bouwt lama.png uit het raster van ronde 2c (basis, ongewijzigd ingelezen) + de met de hand getypte
overlays in deze map (wol.txt; formaat `rij x0 pixels`).
Alleen bouwen + controleren (silhouet, dubbele pixels); geen tintlogica.
Draaien: python3 docs/concept/sprites/lama/fase2/kleur/ronde3/bron/bouw.py"""
import os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
BASE = os.path.join(OUT, '../ronde2c/raster_grid.txt')
SIL = os.path.join(HERE, '../../../silhouet/ronde2.txt')
LET = '.kdsblhqrmnytpuw'
PAL = [(152,208,160),(42,22,26),(108,58,32),(168,104,58),(214,154,82),(239,194,122),(248,226,168),(242,112,94),
       (216,52,60),(152,32,58),(74,60,64),(248,192,48),(32,172,168),(222,48,132),(76,92,168),(250,246,236)]
OVERLAYS = ['wol.txt']

def build():
    grid = [list(l.rstrip('\n')) for l in open(BASE)][:64]
    seen = {}
    for name in OVERLAYS:
        p = os.path.join(HERE, name)
        if not os.path.exists(p): continue
        for ln, line in enumerate(open(p), 1):
            if line.lstrip().startswith('#') or not line.strip(): continue
            y, x0, px = line.split()[:3]; y, x0 = int(y), int(x0)
            for i, c in enumerate(px):
                x = x0 + i
                if c not in LET[1:]: sys.exit(f'{name} {ln}: onbekende letter {c!r}')
                if grid[y][x] == '.': sys.exit(f'{name} {ln}: pixel {x},{y} buiten het silhouet')
                if (x, y) in seen: sys.exit(f'{name} {ln}: pixel {x},{y} dubbel ({seen[(x, y)]})')
                seen[(x, y)] = f'{name}:{ln}'; grid[y][x] = c
    return grid

if __name__ == '__main__':
    grid = build()
    sil = [l.rstrip('\n') for l in open(SIL)]
    miss = [(x, y) for y in range(64) for x in range(64) if (sil[y][x] == '#') != (grid[y][x] != '.')]
    im = Image.new('P', (64, 64)); im.putpalette([v for rgb in PAL for v in rgb])
    im.putdata([LET.index(grid[y][x]) for y in range(64) for x in range(64)])
    im.save(os.path.join(OUT, 'lama.png'), transparency=0)
    open(os.path.join(OUT, 'raster_grid.txt'), 'w').write('\n'.join(''.join(r) for r in grid) + '\n')
    print('gebouwd; alpha-diff', len(miss))
