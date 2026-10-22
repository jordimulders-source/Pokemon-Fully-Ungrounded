"""Vormbibliotheek voor fakemon-sprites (Fully Ungrounded, ronde 2).

Bouw een sprite op uit eenvoudige vormen (ellipsen, cirkels, polygonen, wolken met
een geschulpte rand), elk met een *onderdeel* (part) en een ramp van paletindexen.
Elke vorm wordt als een bol belicht vanuit linksboven (zoals de Hoenn-sprites) en in
de tinten van zijn ramp gezet: grote egale vlakken, geen ruis. Daarna:
  - binnenlijnen waar een vorm over een andere ligt (donkerste tint van de voorste);
  - een buitenlijn van 1 px: zwart rechtsonder, selout (donkerste tint) linksboven;
  - handmatige pixels (`put`) en ASCII-rasters (`stamp`) voor ogen, mond, details.

    from shapelib import Canvas
    c = Canvas(ramps={'wol': [1, 2, 3, 4], ...}, black=15)
    c.ellipse(32, 40, 14, 12, 'wol')
    img = c.finish()        # 64x64 indexarray

Alleen numpy + PIL. Geen randomness: alles is reproduceerbaar.
"""
import numpy as np
from PIL import Image, ImageDraw

LIGHT = np.array([-0.55, -0.65, 0.52])
LIGHT = LIGHT / np.linalg.norm(LIGHT)


class Canvas:
    def __init__(self, ramps, black=15, size=64, thresholds=None):
        """ramps: {part: [licht, ..., donker]} (paletindexen). De laatste index van een
        ramp is de selout-/lijntint. thresholds: {part: [t_hooglicht, t_basis, ...]}:
        belichtingsgrenzen (dot met het licht) per tint, van licht naar donker."""
        self.S = size
        self.ramps = ramps
        self.black = black
        self.idx = np.zeros((size, size), np.int16)      # paletindex (0 = leeg)
        self.part = np.full((size, size), '', object)
        self.prim = np.full((size, size), -1, np.int32)
        self.n = 0
        self.th = thresholds or {}
        self.noline = np.zeros((size, size), bool)        # geen buitenlijn hier

    # ---------- maskers ----------
    def _yx(self):
        return np.mgrid[0:self.S, 0:self.S].astype(float)

    def m_ellipse(self, cx, cy, rx, ry):
        y, x = self._yx()
        return ((x + 0.5 - cx - 0.5) / rx) ** 2 + ((y + 0.5 - cy - 0.5) / ry) ** 2 <= 1.0

    def m_poly(self, pts):
        im = Image.new('L', (self.S, self.S), 0)
        ImageDraw.Draw(im).polygon([tuple(p) for p in pts], fill=1)
        return np.array(im).astype(bool)

    def m_cloud(self, cx, cy, rx, ry, bumps, br, a0=0.0, inner=0.86):
        """Wolk: gevulde ellips + `bumps` cirkels (straal br) op de rand: geschulpte rand."""
        m = self.m_ellipse(cx, cy, rx * inner, ry * inner)
        cs = []
        for k in range(bumps):
            a = a0 + 2 * np.pi * k / bumps
            bx, by = cx + np.cos(a) * (rx - br * 0.6), cy + np.sin(a) * (ry - br * 0.6)
            m |= self.m_ellipse(bx, by, br, br)
            cs.append((bx, by))
        return m, cs

    def curls(self, cs, br, part, tone, side=0.2, only=None, arc=(0.0, 3.2)):
        """Krulboogjes in een wolk: per bobbel een boog van 1 px (straal br-1) aan de
        onderkant (hoek arc in radialen, 0 = rechts, pi/2 = onder), alleen op pixels
        van `part` met een tint in `only` (standaard de basistint)."""
        only = only or [self.ramps[part][1]]
        for bx, by in cs:
            for t in np.linspace(arc[0], arc[1], 40):
                x = int(round(bx + np.cos(t) * (br - 1))); y = int(round(by + np.sin(t) * (br - 1)))
                if 0 <= x < self.S and 0 <= y < self.S and self.part[y, x] == part and self.idx[y, x] in only:
                    self.idx[y, x] = tone

    # ---------- belichting ----------
    def _shade(self, cx, cy, rx, ry, m, flat=0.0):
        y, x = self._yx()
        u = (x + 0.5 - cx - 0.5) / max(rx, 1e-3)
        v = (y + 0.5 - cy - 0.5) / max(ry, 1e-3)
        r2 = np.clip(u * u + v * v, 0, 1)
        w = np.sqrt(1 - r2)
        n = np.stack([u, v, w + flat], -1)
        n /= np.linalg.norm(n, axis=-1, keepdims=True)
        return n @ LIGHT

    def _tone(self, part, d):
        r = self.ramps[part]
        th = self.th.get(part)
        if th is None:
            # standaard: hooglicht klein, basis groot, schaduw rechtsonder
            th = {1: [], 2: [0.15], 3: [0.82, 0.12], 4: [0.86, 0.30, -0.05]}.get(len(r), [0.85, 0.3, -0.1])
        out = np.full(d.shape, r[min(len(th), len(r) - 1)], np.int16)
        for k in range(len(th) - 1, -1, -1):
            out[d > th[k]] = r[k]
        return out

    # ---------- tekenen ----------
    def fill(self, m, part, cx=None, cy=None, rx=None, ry=None, edge=True, tone=None,
             flat=0.0, shift=0, glob=None, mix=0.5, linetone=None):
        """Vul masker m met onderdeel `part`. Belichting als bol (cx,cy,rx,ry), standaard
        de omhullende ellips van het masker. edge: binnenlijn waar m over bestaande
        vormen ligt. tone: vaste index i.p.v. belichting. shift: tinten verschuiven
        (+1 = een tint donkerder, voor verre ledematen)."""
        m = m.copy()
        if not m.any():
            return m
        ys, xs = np.nonzero(m)
        if cx is None:
            cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
            rx, ry = (xs.max() - xs.min() + 1) / 2, (ys.max() - ys.min() + 1) / 2
        if tone is not None:
            t = np.full(m.shape, tone, np.int16)
        else:
            d = self._shade(cx, cy, rx, ry, m, flat)
            if glob is not None:   # mengen met de belichting van een grotere vorm
                d = (1 - mix) * d + mix * self._shade(*glob, m, flat)
            t = self._tone(part, d)
            if shift:
                r = self.ramps[part]
                lut = {r[i]: r[min(i + shift, len(r) - 1)] if shift > 0 else r[max(i + shift, 0)] for i in range(len(r))}
                t = np.vectorize(lambda v: lut.get(v, v))(t).astype(np.int16)
        self.idx[m] = t[m]
        self.part[m] = part
        self.prim[m] = self.n
        if edge:
            filled_before = self.prim >= 0
            filled_before &= self.prim != self.n
            nb_other = np.zeros_like(m)
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                sh = np.roll(np.roll(filled_before, dy, 0), dx, 1)
                out = ~np.roll(np.roll(m, dy, 0), dx, 1)
                nb_other |= sh & out
            line = m & nb_other
            # lijnkleur: zwart waar de lijn rechtsonder van de vorm zit, anders donkerste tint
            y, x = self._yx()
            nx, ny = x - cx, y - cy
            darkside = (nx * -LIGHT[0] + ny * -LIGHT[1]) > 0.35 * max(rx, ry)
            lt = self.ramps[part][-1] if linetone is None else linetone
            col = np.where(darkside, self.black if linetone is None else lt, lt)
            self.idx[line] = col[line]
        self.n += 1
        return m

    def ellipse(self, cx, cy, rx, ry, part, **kw):
        return self.fill(self.m_ellipse(cx, cy, rx, ry), part, cx, cy, rx, ry, **kw)

    def poly(self, pts, part, **kw):
        return self.fill(self.m_poly(pts), part, **kw)

    def erase(self, m):
        self.idx[m] = 0; self.part[m] = ''; self.prim[m] = -1

    def put(self, pts, index):
        for x, y in pts:
            if 0 <= x < self.S and 0 <= y < self.S:
                self.idx[y, x] = index
                if index == 0:
                    self.part[y, x] = ''; self.prim[y, x] = -1
                elif self.prim[y, x] < 0:
                    self.prim[y, x] = 10 ** 6

    def stamp(self, x0, y0, rows, key):
        """ASCII-raster: elk teken via key -> index ('.' of ' ' = niets doen)."""
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch in key:
                    self.put([(x0 + i, y0 + j)], key[ch])

    # ---------- afronden ----------
    def outline(self):
        fig = self.idx > 0
        ring = np.zeros_like(fig)
        nbpart = np.full(fig.shape, '', object)
        nx = np.zeros(fig.shape); ny = np.zeros(fig.shape)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            sh = np.roll(np.roll(fig, dy, 0), dx, 1)
            r = sh & ~fig
            ring |= r
            pp = np.roll(np.roll(self.part, dy, 0), dx, 1)
            nbpart = np.where(r & (nbpart == ''), pp, nbpart)
            # buur zit op (-dy,-dx) gezien vanaf de ringpixel; buitennormaal = (dx,dy)
            nx += r * dx; ny += r * dy
        ring &= ~self.noline
        out = self.idx.copy()
        lit = (nx * LIGHT[0] + ny * LIGHT[1]) > 0.25
        for y, x in zip(*np.nonzero(ring)):
            p = nbpart[y, x]
            if lit[y, x] and p in self.ramps:
                out[y, x] = self.ramps[p][-1]
            else:
                out[y, x] = self.black
        self.idx = out

    def finish(self, outline=True):
        if outline:
            self.outline()
        return self.idx.copy()


def save_indexed(path, frames, pal):
    a = np.concatenate(frames, 0).astype(np.uint8)
    im = Image.fromarray(a, 'P')
    flat = []
    for c in pal:
        flat += list(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    im.save(path, transparency=0)


def write_jasc(path, pal):
    with open(path, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for c in pal:
            f.write('%d %d %d\n' % c)


def gba15(c):
    """Rond een RGB-kleur af op een 15-bit GBA-kleur (zoals de Hoenn-paletten)."""
    return tuple(round(v / 255 * 31) * 255 // 31 for v in c)


def hexpal(hexes):
    return [gba15(tuple(int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))) for h in hexes]
