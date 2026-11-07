"""r4/raster.txt + wijzig_r6.py -> raster.txt"""
import os, runpy
H = os.path.dirname(os.path.abspath(__file__))
G = [list(l.rstrip('\n')) for l in open(os.path.join(H, '../kleur_r5/raster.txt'))][:64]
for y, x0, s in runpy.run_path(os.path.join(H, 'wijzig_r6.py'))['S']:
    for i, c in enumerate(s): G[y][x0 + i] = c
open(os.path.join(H, 'raster.txt'), 'w').write('\n'.join(''.join(r) for r in G) + '\n')
