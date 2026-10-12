#!/usr/bin/env python3
"""Project Grounded: kleine tekenhulpjes voor filmtransities (Mimi, Keccles, Burglar, Dave-tribune).
Alles werkt op numpy-RGB-beelden van 240x160 (uint8) en PIL-RGBA-sprites."""
import os
import numpy as np
from PIL import Image

import film
import gbagfx_render as gr

W, H = film.W, film.H
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0


def canvas(col=(0, 0, 0)):
    a = np.zeros((H, W, 3), np.uint8)
    a[:] = col
    return a


def rect(a, x0, y0, x1, y1, col):
    """Vult [x0, x1) x [y0, y1) (geknipt op het beeld)."""
    x0, y0, x1, y1 = max(int(x0), 0), max(int(y0), 0), min(int(x1), a.shape[1]), min(int(y1), a.shape[0])
    if x1 > x0 and y1 > y0:
        a[y0:y1, x0:x1] = col


def dither(a, mask, col, level):
    """Zet col op de pixels van mask waar het Bayer-patroon onder level (0..1) ligt."""
    ys, xs = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    m = mask & (BAYER[ys % 4, xs % 4] < level)
    a[m] = col


def blit(a, spr, x, y, alpha_min=128):
    """Plakt een RGBA-sprite (PIL of numpy) met zijn linkerbovenhoek op (x, y)."""
    s = np.array(spr) if not isinstance(spr, np.ndarray) else spr
    h, w = s.shape[:2]
    x, y = int(round(x)), int(round(y))
    sx0, sy0 = max(0, -x), max(0, -y)
    sx1, sy1 = min(w, a.shape[1] - x), min(h, a.shape[0] - y)
    if sx1 <= sx0 or sy1 <= sy0:
        return a
    sub = s[sy0:sy1, sx0:sx1]
    m = sub[..., 3] >= alpha_min
    dst = a[y + sy0:y + sy1, x + sx0:x + sx1]
    dst[m] = sub[..., :3][m]
    return a


def scale(spr, k):
    return spr.resize((int(spr.width * k), int(spr.height * k)), Image.NEAREST)


def mon(name, path='anim_front_gba.png', frame=0, pal='normal_gba.pal'):
    d = 'graphics/pokemon/%s/' % name
    p = d + path
    if not os.path.exists(os.path.join(film.ROOT, p)):
        p = d + 'front.png'
    pp = d + pal
    if not os.path.exists(os.path.join(film.ROOT, pp)):
        pp = d + 'normal.pal'
    return gr.sprite(p, pp, frame)


def shade(col, k):
    return tuple(int(min(255, max(0, c * k))) for c in col)


def mix(a, b, k):
    return tuple(int(round(a[i] + (b[i] - a[i]) * k)) for i in range(3))
