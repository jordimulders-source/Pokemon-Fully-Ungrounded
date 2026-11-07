"""Kleur ronde 4b: bouwt lama.png en oog_A/B/C.png uit de met de hand getypte rasters: lama_raster.txt (64x64, één letter
per pixel) + oog_X.txt (formaat `rij x0 pixels`, alleen binnen de oogzone x19-23 y11-15).
Alleen bouwen en controleren (letters geldig, oog alleen in de oogzone); geen tint- of vormlogica.
Draaien: python3 docs/concept/sprites/lama/fase2/kleur/ronde4/bron/bouw.py [A|B|C voor lama.png, standaard KEUZE]"""
import os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
LET = '.kdsblhormnygpuv'
PAL = [(152, 208, 160),  # . transparant (achtergrond)
       (42, 22, 26),     # k omlijning, pupil
       (108, 58, 32),    # d vacht 5 / omlijningsbasis   6c3a20
       (168, 104, 58),   # s vacht 4 (schaduw)           a8683a
       (214, 154, 82),   # b vacht 3 (basis kop/poten)   d69a52
       (239, 194, 122),  # l vacht 2 (basis wol)         efc27a
       (248, 226, 168),  # h vacht 1 (licht, wolpunten)  f8e2a8
       (240, 96, 74),    # o rood licht
       (216, 36, 60),    # r rood (handschoen, kwast, aguayo)
       (152, 32, 58),    # m donkerrood
       (74, 64, 72),     # n polsband, hoef, grijsbruine iris
       (242, 176, 42),   # y geel
       (46, 156, 90),    # g groen
       (232, 90, 154),   # p roze
       (47, 95, 184),    # u blauw
       (150, 140, 150)]  # v lichtgrijs (nagels, glans polsband, hoef)
KEUZE = 'B'

def lees(path, grid, seen, zone=None):
    for ln, line in enumerate(open(path), 1):
        if line.lstrip().startswith('#') or not line.strip(): continue
        y, x0, px = line.split()[:3]; y, x0 = int(y), int(x0)
        for i, c in enumerate(px):
            x = x0 + i
            if c not in LET[1:]: sys.exit(f'{path}:{ln}: onbekende letter {c!r}')
            if zone and not (zone[0] <= x <= zone[2] and zone[1] <= y <= zone[3]): sys.exit(f'{path}:{ln}: pixel {x},{y} buiten de oogzone')
            if (x, y) in seen: sys.exit(f'{path}:{ln}: pixel {x},{y} dubbel ({seen[(x, y)]})')
            seen[(x, y)] = f'{os.path.basename(path)}:{ln}'; grid[y][x] = c

def build(oog):
    grid = [list(l.rstrip('\n')) for l in open(os.path.join(HERE, 'lama_raster.txt'))][:64]
    for r in grid:
        for c in r:
            if c not in LET: sys.exit(f'lama_raster.txt: onbekende letter {c!r}')
    return grid

def save(grid, path):
    im = Image.new('P', (64, 64)); im.putpalette([v for rgb in PAL for v in rgb])
    im.putdata([LET.index(grid[y][x]) for y in range(64) for x in range(64)])
    im.save(path, transparency=0)

if __name__ == '__main__':
    keuze = sys.argv[1] if len(sys.argv) > 1 else KEUZE
    g = build(None); save(g, os.path.join(OUT, 'lama.png'))
    open(os.path.join(OUT, 'raster_grid.txt'), 'w').write('\n'.join(''.join(r) for r in g) + '\n')
    with open(os.path.join(OUT, 'normal.pal'), 'w') as f:
        f.write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join(f'{r} {g} {b}\r\n' for r, g, b in PAL))
    print('gebouwd: lama.png (ronde 4d)')
