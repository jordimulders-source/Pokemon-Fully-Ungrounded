"""rijen_rN.py (met de hand gezette rijen) -> raster.txt; meldt rijen die niet op het silhouet passen."""
import sys, os, runpy, numpy as np; from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
SIL = '/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/potoo/silhouet/silhouet.png'
a = np.array(Image.open(SIL).convert('RGBA'))[:, :, 3] > 0
NS = runpy.run_path(sys.argv[1]); R = NS['R']; W = NS.get('W', {})
G = [['.'] * 64 for _ in range(64)]
for y, (x0, parts) in R.items():
    s = ''.join(parts)
    for i, ch in enumerate(s): G[y][x0 + i] = ch
    xs = np.where(a[y])[0]; end = x0 + len(s) - 1
    if x0 != xs.min() or end != xs.max(): print(f'rij {y}: x{x0}-{end}, silhouet x{xs.min()}-{xs.max()}')
for (x, y), c in W.items(): G[y][x] = c
open(os.path.join(H, 'raster.txt'), 'w').write('\n'.join(''.join(r) for r in G) + '\n')
