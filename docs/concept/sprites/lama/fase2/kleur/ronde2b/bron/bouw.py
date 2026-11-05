"""Kleur ronde 2b: bouwt lama.png uit raster.txt (ronde 2) + hals.txt (wolhals, ronde 2b) (met de hand getypt) en controleert tegen het bevroren silhouet.
Draaien: python3 docs/concept/sprites/lama/fase2/kleur/ronde1/bron/bouw.py"""
import os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
SIL = os.path.join(HERE, '../../../silhouet/ronde2.txt')
PAL = [  # (letter, rgb, gebruik)
    ('.', (152, 208, 160), 'transparant (zoals de alpaca)'),
    ('k', (42, 22, 26), 'omlijning schaduwkant, oog, neus/mond'),
    ('d', (108, 58, 32), 'vacht donker 6c3a20: selout lichtkant, scheidingen (spaarzaam)'),
    ('s', (168, 104, 58), 'vacht schaduw a8683a, snuitmasker'),
    ('b', (214, 154, 82), 'vacht basis karamel d69a52'),
    ('l', (239, 194, 122), 'vacht licht efc27a (hoofdtint)'),
    ('h', (248, 226, 168), 'vacht hooglicht f8e2a8 (wolpunten)'),
    ('q', (242, 112, 94), 'rood licht (handschoen, kwast, aguayo)'),
    ('r', (216, 52, 60), 'rood basis'),
    ('m', (152, 32, 58), 'rood schaduw / selout van de doek'),
    ('n', (74, 60, 64), 'donkergrijs: polsband, nagels, hoeven'),
    ('y', (248, 192, 48), 'geel (halsband, pompon, aguayo)'),
    ('t', (32, 172, 168), 'teal (halsband, pompon)'),
    ('p', (222, 48, 132), 'roze (aguayo-rand, pompons)'),
    ('u', (76, 92, 168), 'blauw (aguayo; reflectie in het oog)'),
    ('w', (250, 246, 236), 'wit: glans oog en handschoen'),
]
IDX = {c: i for i, (c, _, _) in enumerate(PAL)}

def build():
    grid = [['.'] * 64 for _ in range(64)]
    seen = {}
    for ln, line in enumerate(open(os.path.join(HERE, 'raster.txt')), 1):
        if line.lstrip().startswith('#') or not line.strip(): continue
        y, x0, px = line.split(); y, x0 = int(y), int(x0)
        for i, c in enumerate(px):
            x = x0 + i
            if c not in IDX: sys.exit(f'regel {ln}: onbekende letter {c!r}')
            if (x, y) in seen: sys.exit(f'regel {ln}: pixel {x},{y} dubbel (ook regel {seen[(x, y)]})')
            seen[(x, y)] = ln; grid[y][x] = c
    hp = os.path.join(HERE, 'hals.txt')
    for ln, line in enumerate(open(hp), 1):
        if line.lstrip().startswith('#') or not line.strip(): continue
        y, x0, px = line.split(); y, x0 = int(y), int(x0)
        for i, c in enumerate(px):
            x = x0 + i
            if c not in IDX: sys.exit(f'hals {ln}: onbekende letter {c!r}')
            if grid[y][x] == '.': sys.exit(f'hals {ln}: pixel {x},{y} buiten het silhouet')
            grid[y][x] = c
    return grid

if __name__ == '__main__':
    grid = build()
    sil = [l.rstrip('\n') for l in open(SIL)]
    miss = [(x, y) for y in range(64) for x in range(64) if (sil[y][x] == '#') != (grid[y][x] != '.')]
    if miss: print('ALPHA-DIFF', len(miss), miss[:60])
    im = Image.new('P', (64, 64))
    im.putpalette([v for _, rgb, _ in PAL for v in rgb])
    im.putdata([IDX[grid[y][x]] for y in range(64) for x in range(64)])
    im.save(os.path.join(OUT, 'lama.png'), transparency=0)
    open(os.path.join(OUT, 'raster_grid.txt'), 'w').write('\n'.join(''.join(r) for r in grid) + '\n')
    with open(os.path.join(OUT, 'normal.pal'), 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % rgb for _, rgb, _ in PAL))
    print('gebouwd; alpha-diff', len(miss))
