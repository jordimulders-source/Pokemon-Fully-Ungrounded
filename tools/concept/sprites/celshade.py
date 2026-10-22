"""Cel-shading in Gen 3-stijl voor sprites uit vormen (aanvulling op shapelib.py).

Gen 3 schaduwt niet met verlopen maar met vaste vlakken: een egale basistint, een
lichte rand linksboven (het hooglicht van elke bolling) en een schaduwband langs
onder/rechts, met de donkerste tint als smalle rand vlak bij de omlijning. Dat doet
`cel()` per masker, met verschuivingen in hele pixels: strak, geen ruis.

    from celshade import cel, disk, poly
    m = disk(30, 40, 6)
    cel(canvas, m, 'wol', light=2, shade=(2, 3), deep=1)
"""
import numpy as np
from PIL import Image, ImageDraw

S = 64


def disk(cx, cy, rx, ry=None):
    ry = rx if ry is None else ry
    y, x = np.mgrid[0:S, 0:S].astype(float)
    return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0


def poly(pts):
    im = Image.new('L', (S, S), 0)
    ImageDraw.Draw(im).polygon([tuple(p) for p in pts], fill=1)
    return np.array(im).astype(bool)


def shift(m, dx, dy):
    out = np.zeros_like(m)
    ys, xs = slice(max(dy, 0), S + min(dy, 0)), slice(max(dx, 0), S + min(dx, 0))
    yd, xd = slice(max(-dy, 0), S + min(-dy, 0)), slice(max(-dx, 0), S + min(-dx, 0))
    out[yd, xd] = m[ys, xs]
    return out   # out[p] = m[p + (dx, dy)]


def cel(c, m, part, light=2, shade=(2, 3), deep=1, tones=None, edge=None, within=None):
    """Vul masker m (bool 64x64) op canvas c (shapelib.Canvas) als onderdeel `part`.
    tones: (hooglicht, basis, schaduw, diep) als paletindexen; standaard uit c.ramps
    (bij 3 tinten is diep = schaduw). light: breedte van de lichte rand linksboven.
    shade: (dx, dy) — een pixel is schaduw als p+(dx,dy) buiten het masker valt.
    deep: breedte van de donkerste rand rechtsonder (0 = geen).
    edge: binnenlijn (index) waar m over al getekende vormen ligt, aan de
    onder-/rechterkant van m (None = geen). within: masker waarbinnen de randen
    gemeten worden (bijv. het hele lijf i.p.v. één bolletje)."""
    r = c.ramps[part]
    if tones is None:
        tones = (r[0], r[1], r[2] if len(r) > 2 else r[-1], r[3] if len(r) > 3 else r[-1])
    hl, base, sh, dp = tones
    ref = m if within is None else within
    t = np.full((S, S), base, np.int16)
    if light:
        lit = m & ~shift(ref, -light, -light)
        t[lit] = hl
    dx, dy = shade
    t[m & ~shift(ref, dx, dy)] = sh
    if deep:
        t[m & ~shift(ref, deep, deep)] = dp
    old = c.prim >= 0
    c.idx[m] = t[m]; c.part[m] = part; c.prim[m] = c.n; c.n += 1
    if edge is not None:
        # binnenlijn: rand van m die tegen eerder getekende vormen ligt, onder/rechts
        nb = np.zeros_like(m)
        for ox, oy in ((1, 0), (0, 1), (1, 1)):
            nb |= shift(old & ~m, ox, oy)
        line = m & nb
        c.idx[line] = edge
    return m
