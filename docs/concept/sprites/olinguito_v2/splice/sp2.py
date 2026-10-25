import numpy as np, sys
from PIL import Image
sys.path.insert(0, sys.argv[1]); S = sys.argv[1]
from common import PAL, show
sil = np.array(Image.open(S + '/sil5.png').convert('RGBA'))[..., 3] > 0
b = np.array(Image.open(S + '/b2_64.png').convert('RGB')).astype(int)
g = np.full((64, 64), '.', object)
HEAD = np.zeros((64, 64), bool); HEAD[:42, :31] = sil[:42, :31]
L = np.array([-0.6, -0.75, 0.5]); L /= np.linalg.norm(L)
cx, cy, r = 19.5, 29.0, 11.5
for y in range(64):
    for x in range(64):
        if not sil[y, x]: continue
        if HEAD[y, x]:
            nx, ny = (x + 0.5 - cx) / r, (y + 0.5 - cy) / r; d = nx * nx + ny * ny
            nz = np.sqrt(max(0, 1 - min(d, 0.95)))
            lam = nx * L[0] + ny * L[1] + nz * L[2]
            g[y, x] = 'g' if lam > 0.82 else 'G' if lam > 0.42 else 'q'
        else: g[y, x] = 'B'
# masker (B2: zwarte band), oog, neus, snoet
for y in range(64):
    for x in range(64):
        if not HEAD[y, x]: continue
        c = b[y, x]
        if c.sum() < 150: g[y, x] = 'K'
for (x, y), v in {(19, 32): 'W', (20, 32): 'E', (19, 33): 'E', (20, 33): 'e'}.items(): g[y, x] = v
for (x, y), v in {(7, 37): 'P', (8, 37): 'P', (7, 38): 'p', (8, 38): 'P', (9, 38): 'p'}.items(): g[y, x] = v
# omtrek
for y in range(64):
    for x in range(64):
        if not sil[y, x]: continue
        out = [(dx, dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if not (0 <= x + dx < 64 and 0 <= y + dy < 64) or not sil[y + dy, x + dx]]
        if out and g[y, x] not in ('P', 'p'):
            lit = any(dx < 0 or dy < 0 for dx, dy in out); dark = any(dx > 0 or dy > 0 for dx, dy in out)
            g[y, x] = ('Q' if HEAD[y, x] else 'L') if lit and not dark else 'K'
np.save(S + '/sp2.npy', g); show(g, S + '/sp2.png')
