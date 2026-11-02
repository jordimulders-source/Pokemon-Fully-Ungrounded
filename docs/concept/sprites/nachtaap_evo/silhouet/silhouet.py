"""Nachtaap fase 2: silhouet op 64x64 uit het goedgekeurde 3D-poppetje (SPRITE_WERKWIJZE stap 2).
Bron = de render (lijf 40°, kop 80°, staart omhoog, kené) direct verkleind: de massa is heilig.
Alleen dunne delen (vingers, staart/spiraal, oren) krijgen een minimale dikte; daarna handwerk in benoemde zones.
Draaien vanuit de repo-root: python3 docs/concept/sprites/nachtaap_evo/silhouet/silhouet.py"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'pop3d'))
import nachtaap3d as N  # noqa: E402
import pop3d as P  # noqa: E402

YAW, PITCH, HEAD_EXTRA = 40, 8, 40
BOX = 64
TARGET = 1500          # fase 2 ≈ 1,5–1,7× fase 1 (950 px); Lairon 1599, Vigoroth 1480


def model():
    return N.nachtaap(HEAD_EXTRA, 'omhoog', 'kene', cam=(YAW, PITCH))


def gid_render(m, fill):
    x0, x1, y0, y1 = P.bbox(m, YAW, PITCH)
    scale = P.R * fill / max(x1 - x0, y1 - y0)
    zbuf, gid, nrm, groups = P.render(m, YAW, PITCH, scale, ((x0 + x1) / 2, (y0 + y1) / 2))
    return gid, groups


def to64(gid, groups, thin=('hand', 'farhand'), min_px=1.8, thr=110):
    k = gid.shape[0] // BOX
    alls = gid >= 0
    sil = np.array(Image.fromarray((alls * 255).astype(np.uint8)).resize((BOX, BOX), Image.BOX)) > thr
    for g in thin:
        tm = Image.fromarray(((gid == groups.index(g)) * 255).astype(np.uint8))
        r = int(k * min_px / 2)
        tm = tm.filter(ImageFilter.MaxFilter(2 * r + 1))
        sil |= np.array(tm.resize((BOX, BOX), Image.BOX)) > 90
    far = np.isin(gid, [groups.index('far'), groups.index('farhand')])
    farm = np.array(Image.fromarray((far * 255).astype(np.uint8)).resize((BOX, BOX), Image.BOX)) > 140
    return sil, farm & sil


def place(sil, far):
    """Onderkant op rij 62, horizontaal gecentreerd (zoals Gen 3-frontsprites)."""
    ys, xs = np.nonzero(sil)
    dy = 62 - ys.max()
    dx = int(round(31.5 - (xs.min() + xs.max()) / 2))
    out = np.zeros_like(sil); of = np.zeros_like(far)
    out[ys + dy, xs + dx] = True
    fy, fx = np.nonzero(far)
    of[fy + dy, fx + dx] = True
    return out, of, (dx, dy)


def fit():
    m = model()
    best = None
    for fill in np.linspace(0.70, 1.0, 31):
        gid, groups = gid_render(m, fill)
        sil, far = to64(gid, groups)
        n = int(sil.sum())
        if best is None or abs(n - TARGET) < abs(best[1] - TARGET):
            best = (fill, n, sil, far, gid, groups)
    return best


def save_png(sil, path, far=None):
    im = Image.new('RGBA', (BOX, BOX), (0, 0, 0, 0))
    a = np.zeros((BOX, BOX, 4), np.uint8)
    a[sil] = (40, 32, 56, 255)
    if far is not None:
        a[far] = (96, 80, 120, 255)
    Image.fromarray(a).save(path)


if __name__ == '__main__':
    fill, n, sil, far, gid, groups = fit()
    sil, far, off = place(sil, far)
    print(f'fill {fill:.3f} -> {n} px, offset {off}')
    np.save(os.path.join(HERE, 'basis_sil.npy'), sil)
    np.save(os.path.join(HERE, 'basis_far.npy'), far)
    save_png(sil, os.path.join(HERE, 'basis_1x.png'))
    # onderlaag: de render op dezelfde schaal en plek, 4x
    m = model()
    x0, x1, y0, y1 = P.bbox(m, YAW, PITCH)
    scale = P.R * fill / max(x1 - x0, y1 - y0)
    img = P.shade(*P.render(m, YAW, PITCH, scale, ((x0 + x1) / 2, (y0 + y1) / 2)))  # 256x256
    big = Image.new('RGB', (256, 256), 'white')
    big.paste(img, (off[0] * 4, off[1] * 4))
    big.save(os.path.join(HERE, 'onderlaag_256.png'))
