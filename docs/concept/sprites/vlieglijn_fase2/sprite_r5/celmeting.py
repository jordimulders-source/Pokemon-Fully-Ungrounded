#!/usr/bin/env python3
"""Model (1024) op het spriteraster: per spritecel % zwart, % wit (achtergrond) en gemiddelde niet-zwarte kleur.
Ook: beste verschuiving (dx, dy in modelpx) zodat het model-silhouet het r4B-silhouet het best dekt."""
import sys, os
import numpy as np
from PIL import Image
HIER = os.path.dirname(os.path.abspath(__file__)); BASIS = os.path.dirname(HIER)
M = np.array(Image.open(os.path.join(BASIS, 'referenties/gemini_gekozen_r1.png')).convert('RGB')).astype(int)
bg = M.min(-1) > 235
ys, xs = np.where(~bg); X0, Y0, X1, Y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
sx = (X1 - X0) / 56; sy = (Y1 - Y0) / 63
lum = 0.299 * M[..., 0] + 0.587 * M[..., 1] + 0.114 * M[..., 2]
zwart = (lum < 45) & ~bg


def cel(x, y, dx=0, dy=0, rand=0.15):
    mx0 = X0 + (x - 4 + rand) * sx + dx; mx1 = X0 + (x + 1 - 4 - rand) * sx + dx
    my0 = Y0 + (y - 1 + rand) * sy + dy; my1 = Y0 + (y + 1 - 1 - rand) * sy + dy
    sl = (slice(int(my0), int(my1)), slice(int(mx0), int(mx1)))
    b = bg[sl]; z = zwart[sl]; c = M[sl]
    rest = ~b & ~z
    kl = tuple(int(v) for v in c[rest].mean(0)) if rest.any() else None
    return b.mean(), z.mean(), kl


def uitlijning(a):
    best = None
    for dx in range(-8, 9, 2):
        for dy in range(-8, 9, 2):
            s = 0
            for y in range(28, 60):
                for x in range(18, 44):
                    b, z, k = cel(x, y, dx, dy)
                    s += ((b < 0.5) == (a[y, x] > 0))
            if best is None or s > best[0]:
                best = (s, dx, dy)
    return best


if __name__ == '__main__':
    a = np.array(Image.open(os.path.join(BASIS, 'sprite_r4/mug_r4B.png')))
    print('uitlijning (match, dx, dy):', uitlijning(a))
