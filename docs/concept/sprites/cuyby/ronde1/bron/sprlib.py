"""Gedeelde vormen + Gen 3-cel-shading (naar olinguito ronde 5, bron/render.py).
Vormen als maskers; shading met sikkels (masker min verschoven kopie): smal
hooglicht linksboven, schaduwsikkel rechtsonder, selout-omlijning.
Ook gebruikt door dj_rotom/ronde1/bron/render.py."""
import numpy as np
from PIL import Image, ImageDraw

S = 64
CH = '.123456789abcdef'
YY, XX = np.mgrid[0:S, 0:S] + 0.5


def ell(cx, cy, rx, ry, rot=0.0):
    c, s = np.cos(rot), np.sin(rot)
    u = (XX - cx) * c + (YY - cy) * s
    w = -(XX - cx) * s + (YY - cy) * c
    return (u / rx) ** 2 + (w / ry) ** 2 <= 1


def poly(pts):
    im = Image.new('L', (S, S), 0)
    ImageDraw.Draw(im).polygon([tuple(p) for p in pts], fill=1)
    return np.array(im).astype(bool)


def rect(x0, y0, x1, y1):
    return (XX >= x0) & (XX < x1) & (YY >= y0) & (YY < y1)


def tube(pts, w0, w1):
    m = np.zeros((S, S), bool)
    n = len(pts) - 1
    for k in range(n * 16 + 1):
        t = k / (n * 16)
        i = min(int(t * n), n - 1); f = t * n - i
        x = pts[i][0] * (1 - f) + pts[i + 1][0] * f
        y = pts[i][1] * (1 - f) + pts[i + 1][1] * f
        r = w0 * (1 - t) + w1 * t
        m |= ell(x, y, r, r)
    return m


def shift(m, dx, dy):
    out = np.zeros_like(m)
    ys, xs = np.nonzero(m)
    ys2, xs2 = ys + dy, xs + dx
    ok = (ys2 >= 0) & (ys2 < S) & (xs2 >= 0) & (xs2 < S)
    out[ys2[ok], xs2[ok]] = True
    return out


def dilate(m, n=1, diag=False):
    for _ in range(n):
        o = m.copy()
        nb = ((1, 0), (-1, 0), (0, 1), (0, -1))
        if diag:
            nb += ((1, 1), (-1, -1), (1, -1), (-1, 1))
        for dx, dy in nb:
            o |= shift(m, dx, dy)
        m = o
    return m


class Sprite:
    def __init__(self):
        self.idx = np.zeros((S, S), np.uint8)
        self.pid = np.full((S, S), -1, int)
        self.parts = []

    def add(self, m, r, hl=1, sh=2, rim=True, hl_lim=None, cast=True, line=True, flat=None):
        """r = ramp [licht, basis, schaduw, donker]."""
        t = np.full((S, S), r[1], np.uint8)
        if flat is None:
            if sh:
                shade = m & ~shift(m, -sh, -sh)
                t[shade] = r[2]
            if rim:
                dark = m & ~shift(m, -1, -1) & ~shift(m, 0, -1)
                t[dark & (t == r[2])] = r[3]
            if hl:
                h = m & ~shift(m, hl, hl)
                if sh:
                    h &= ~(m & ~shift(m, -sh, -sh))
                if hl_lim:
                    x0, y0, x1, y1 = hl_lim
                    h &= (XX >= x0) & (XX < x1) & (YY >= y0) & (YY < y1)
                t[h] = r[0]
        else:
            t[:] = flat
        k = len(self.parts)
        under = self.pid >= 0
        if cast:
            c = shift(m, 1, 2) & ~m & under
            for y, x in zip(*np.nonzero(c)):
                pr = self.parts[self.pid[y, x]]
                if self.idx[y, x] in (pr[0], pr[1]):
                    self.idx[y, x] = pr[2]
        self.idx[m] = t[m]
        self.pid[m] = k
        if line:
            edge = np.zeros_like(m)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                edge |= m & shift(under & ~m, -dx, -dy)
            for y, x in zip(*np.nonzero(edge)):
                ny = nx = 0
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < S and 0 <= xx < S and not m[yy, xx]:
                        nx += dx; ny += dy
                self.idx[y, x] = r[3] if (nx + ny) < 0 else 15
        self.parts.append(r)

    def paint(self, m, v):
        self.idx[m & (self.idx > 0)] = v

    def outline(self, black_only=False):
        fig = self.idx > 0
        out = self.idx.copy()
        for y in range(S):
            for x in range(S):
                if fig[y, x]:
                    continue
                nb = []
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < S and 0 <= xx < S and fig[yy, xx]:
                        nb.append((dx, dy, self.pid[yy, xx]))
                if not nb:
                    continue
                sx = sum(d[0] for d in nb); sy = sum(d[1] for d in nb)
                p = self.parts[nb[0][2]] if nb[0][2] >= 0 else [15] * 4
                out[y, x] = p[3] if (sx + sy > 0 and p[3] != 15 and not black_only) else 15
        self.pid[(out > 0) & (self.idx == 0)] = -2
        self.idx = out


def write_txt(path, frames):
    with open(path, 'w') as f:
        for k, a in enumerate(frames):
            f.write('== frame %d\n' % (k + 1))
            for row in a:
                f.write(''.join(CH[v] for v in row) + '\n')
