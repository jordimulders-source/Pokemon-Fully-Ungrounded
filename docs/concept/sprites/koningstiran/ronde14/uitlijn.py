"""Lijnt Jordi's krabbel (referenties/krabbel_jordi_staf_overgang.png) uit op ronde13 en zet de rode lijnen om naar spritecoordinaten.
Schrijft ronde6/krabbel_punten.txt en ronde6/krabbel_overlay.png. Draaien vanuit de repo-root."""
import os
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(H)
src = Image.open(os.path.join(K, 'referenties/krabbel_jordi_staf_overgang.png')).convert('RGB')
k = np.array(src).astype(int)
R, G, B = k[..., 0], k[..., 1], k[..., 2]
red = (R > 190) & (G < 45) & (B < 55) & (R - G > 160)
sp = Image.open(os.path.join(K, 'ronde13/sapa_inca.png')).convert('RGB')
spa = np.array(Image.open(os.path.join(K, 'ronde13/sapa_inca.png'))) > 0
spr = np.array(sp).astype(int)
bg = np.median(k[20:60, 20:60].reshape(-1, 3), 0)
def score(sc, ox, oy):
    # kleurverschil tussen krabbel en geschaalde sprite op een rooster van monsterpunten (zonder rood)
    ys = np.arange(10, k.shape[0] - 10, 3); xs = np.arange(10, k.shape[1] - 10, 3)
    yy, xx = np.meshgrid(ys, xs, indexing='ij')
    X = np.floor((xx - ox) / sc).astype(int); Y = np.floor((yy - oy) / sc).astype(int)
    ok = (X >= 0) & (X < 64) & (Y >= 0) & (Y < 64) & ~red[yy, xx]
    ref = np.broadcast_to(bg, yy.shape + (3,)).copy()
    inside = ok.copy(); inside[ok] = spa[Y[ok], X[ok]]
    ref[inside] = spr[Y[inside], X[inside]]
    return np.abs(k[yy, xx] - ref).sum(-1).mean()
best = None
for sc in np.arange(7.0, 8.8, 0.1):
    for ox in range(-30, 60, 4):
        for oy in range(-40, 40, 4):
            v = score(sc, ox, oy)
            if best is None or v < best[0]:
                best = (v, sc, ox, oy)
v, sc0, ox0, oy0 = best
for sc in np.arange(sc0 - 0.15, sc0 + 0.16, 0.02):
    for ox in np.arange(ox0 - 4, ox0 + 4.1, 0.5):
        for oy in np.arange(oy0 - 4, oy0 + 4.1, 0.5):
            v = score(sc, ox, oy)
            if v < best[0]:
                best = (v, sc, ox, oy)
v, sc, ox, oy = best
print(f'schaal {sc:.2f} px per spritepixel, verschuiving x {ox:.1f}, y {oy:.1f} (gem. kleurverschil {v:.1f})')
ry, rx = np.nonzero(red)
pts = {}
for x, y in zip(rx, ry):
    X, Y = int((x - ox) // sc), int((y - oy) // sc)
    pts[(X, Y)] = pts.get((X, Y), 0) + 1
pts = sorted(p for p, n in pts.items() if n >= 3)
from collections import defaultdict
byy = defaultdict(list)
for x, y in pts: byy[y].append(x)
with open(os.path.join(H, 'krabbel_punten.txt'), 'w') as f:
    f.write(f'schaal {sc:.2f}, ox {ox:.1f}, oy {oy:.1f}\n')
    for y in sorted(byy):
        f.write(f'{y} {sorted(byy[y])}\n')
for y in sorted(byy): print(y, sorted(byy[y]))
np.save(os.path.join(H, 'uitlijning.npy'), np.array([sc, ox, oy]))
