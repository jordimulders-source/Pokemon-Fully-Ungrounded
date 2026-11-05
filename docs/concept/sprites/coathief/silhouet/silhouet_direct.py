"""Coathief stap 2: het gekozen ontwerp (B1: lijf 42°, kop 52°, kop C) direct verkleind naar 64x64 (massa = bron).
Draaien: python3 docs/concept/sprites/coathief/silhouet/silhouet_direct.py [fill]"""
import os, sys, math
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../ontwerp'))
import pop3d_coati as C
YAW, HEAD, PITCH, BOX = 42, 10, 10, 64


def render(fill):
    m = C.coati(head_extra=HEAD); m.var = 'C'
    P = C.P
    Rc = P.rot_x(math.radians(PITCH)) @ P.rot_y(math.radians(YAW))
    pts = np.array([Rc @ c for c, r, R0, g in m.parts]); rs = np.array([r.max() for c, r, R0, g in m.parts])
    x0, x1, y0, y1 = (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()
    scale = C.R * fill / max(x1 - x0, y1 - y0)
    zbuf, gid, nrm, groups = C.render(m, YAW, PITCH, scale, ((x0 + x1) / 2, (y0 + y1) / 2))
    return m, scale, ((x0 + x1) / 2, (y0 + y1) / 2), zbuf, gid, nrm, groups


def direct(fill, thr=110):
    m, scale, c, zbuf, gid, nrm, groups = render(fill)
    sil = np.array(Image.fromarray(((gid >= 0) * 255).astype(np.uint8)).resize((BOX, BOX), Image.BOX)) > thr
    under = C.shade(zbuf, gid, nrm, groups, out=256)
    return sil, under


if __name__ == '__main__':
    fill = float(sys.argv[1]) if len(sys.argv) > 1 else 0.92
    sil, under = direct(fill)
    ys, xs = np.nonzero(sil)
    print('fill', fill, 'px', sil.sum(), 'box', xs.max() - xs.min() + 1, ys.max() - ys.min() + 1)
