"""Kleine tekenbibliotheek voor modeltekeningen (Sugimori-stijl).

Coordinaten in een 256x256-ruimte; intern 4x supersampling.
Elke vorm: masker -> (optioneel) omlijning door het masker met een schijf te
dilateren -> vlakke vulling. Vormen worden in volgorde (achter naar voor)
gestapeld, zodat overlappende delen een binnenlijn krijgen.
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SS = 4
N = 256


def hexc(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def catmull(points, closed=True, steps=14):
    pts = [tuple(p) for p in points]
    n = len(pts)
    out = []
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if closed else pts[max(i - 1, 0)]
        p1 = pts[i]
        p2 = pts[(i + 1) % n] if closed else pts[i + 1]
        p3 = pts[(i + 2) % n] if closed else pts[min(i + 2, n - 1)]
        for s in range(steps):
            t = s / steps
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    if not closed:
        out.append(pts[-1])
    return out


def taper(center, w0, w1, round_end=True):
    """Polygoon rond een middenlijn met breedte w0 -> w1."""
    c = center
    n = len(c)
    left, right = [], []
    for i in range(n):
        a = c[max(i - 1, 0)]
        b = c[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        w = (w0 + (w1 - w0) * i / (n - 1)) / 2
        left.append((c[i][0] + nx * w, c[i][1] + ny * w))
        right.append((c[i][0] - nx * w, c[i][1] - ny * w))
    return left + right[::-1]


def spiral(cx, cy, r0, r1, turns, start=0.0, direction=1, steps=200):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        a = start + direction * t * turns * 2 * math.pi
        r = r0 + (r1 - r0) * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


class Canvas:
    def __init__(self, line='#2b2233', lw=2.4):
        self.W = N * SS
        self.img = np.zeros((self.W, self.W, 3), np.uint8) + 255
        self.alpha = np.zeros((self.W, self.W), bool)
        self.line = hexc(line)
        self.lw = lw
        self._disks = {}

    # --- maskers -------------------------------------------------------
    def _new(self):
        return Image.new('L', (self.W, self.W), 0)

    def m_ellipse(self, cx, cy, rx, ry, rot=0):
        if rot == 0:
            im = self._new()
            ImageDraw.Draw(im).ellipse([(cx - rx) * SS, (cy - ry) * SS, (cx + rx) * SS, (cy + ry) * SS], fill=255)
            return np.array(im) > 127
        pts = []
        for i in range(72):
            a = i / 72 * 2 * math.pi
            x, y = rx * math.cos(a), ry * math.sin(a)
            r = math.radians(rot)
            pts.append((cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r)))
        return self.m_poly(pts)

    def m_poly(self, pts):
        im = self._new()
        ImageDraw.Draw(im).polygon([(x * SS, y * SS) for x, y in pts], fill=255)
        return np.array(im) > 127

    def m_blob(self, pts):
        return self.m_poly(catmull(pts))

    def m_stroke(self, pts, w0, w1=None, smooth=True):
        c = catmull(pts, closed=False) if smooth else pts
        m = self.m_poly(taper(c, w0, w0 if w1 is None else w1))
        # ronde kopjes
        m |= self.m_ellipse(c[0][0], c[0][1], w0 / 2, w0 / 2)
        we = w0 if w1 is None else w1
        if we > 0.6:
            m |= self.m_ellipse(c[-1][0], c[-1][1], we / 2, we / 2)
        return m

    def m_tube(self, center, w0, w1=None):
        """Buis als vereniging van cirkels langs een (al gesamplede) lijn."""
        w1 = w0 if w1 is None else w1
        im = self._new()
        d = ImageDraw.Draw(im)
        # hersampelen op ~0.5 px
        pts = [center[0]]
        for p in center[1:]:
            q = pts[-1]
            L = math.hypot(p[0] - q[0], p[1] - q[1])
            k = max(1, int(L / 0.4))
            for j in range(1, k + 1):
                pts.append((q[0] + (p[0] - q[0]) * j / k, q[1] + (p[1] - q[1]) * j / k))
        n = len(pts)
        for i, (x, y) in enumerate(pts):
            r = (w0 + (w1 - w0) * i / max(n - 1, 1)) / 2 * SS
            d.ellipse([x * SS - r, y * SS - r, x * SS + r, y * SS + r], fill=255)
        return np.array(im) > 127

    def m_curl(self, cx, cy, r0, r1, turns, w0, w1, start=0.0, direction=1, tail=None):
        c = spiral(cx, cy, r0, r1, turns, start, direction)
        c = c[::-1]  # van buiten (dik) naar binnen (dun)
        if tail:
            c = catmull(tail[::-1] + [c[0]], closed=False)[:-1] + c
        return self.m_tube(c, w0, w1)

    def m_spiral(self, cx, cy, r0, r1, turns, w0, w1, start=0.0, direction=1, tail=None):
        c = spiral(cx, cy, r0, r1, turns, start, direction)
        if tail:
            c = c + catmull([c[-1]] + tail, closed=False)[1:]
        m = self.m_poly(taper(c, w0, w1))
        m |= self.m_ellipse(c[0][0], c[0][1], w0 / 2, w0 / 2)
        m |= self.m_ellipse(c[-1][0], c[-1][1], w1 / 2, w1 / 2)
        return m

    # --- tekenen -------------------------------------------------------
    def _disk(self, r):
        r = int(round(r))
        if r not in self._disks:
            offs = [(dx, dy) for dx in range(-r, r + 1) for dy in range(-r, r + 1) if dx * dx + dy * dy <= r * r + r * 0.6]
            self._disks[r] = offs
        return self._disks[r]

    def dilate(self, m, r):
        ys, xs = np.nonzero(m)
        out = np.zeros_like(m)
        if len(ys) == 0:
            return out
        R = int(round(r)) + 2
        y0, y1 = max(ys.min() - R, 0), min(ys.max() + R + 1, m.shape[0])
        x0, x1 = max(xs.min() - R, 0), min(xs.max() + R + 1, m.shape[1])
        sub = m[y0:y1, x0:x1]
        o = sub.copy()
        for dx, dy in self._disk(r):
            if dx == 0 and dy == 0:
                continue
            o |= np.roll(np.roll(sub, dy, 0), dx, 1)
        out[y0:y1, x0:x1] = o
        return out

    def fill(self, m, color, line=True, lw=None, clip=None, linecolor=None):
        if clip is not None:
            m = m & clip
        if line:
            w = (lw or self.lw) * SS
            d = self.dilate(m, w / 2 + 0.5) if w > 0 else m
            if clip is not None and line == 'inner':
                d &= clip
            lc = hexc(linecolor) if linecolor else self.line
            self.img[d & ~m] = lc
            self.alpha |= d
        self.img[m] = hexc(color)
        self.alpha |= m
        return m

    def stroke(self, pts, w, color=None, smooth=True, w1=None):
        m = self.m_stroke(pts, w, w1, smooth)
        self.img[m] = hexc(color) if color else self.line
        self.alpha |= m
        return m

    def dot(self, x, y, r, color):
        m = self.m_ellipse(x, y, r, r)
        self.img[m] = hexc(color)
        return m

    def image(self, size=256):
        im = Image.fromarray(self.img).resize((size, size), Image.LANCZOS)
        return im

    def mask(self, size=64):
        a = Image.fromarray((self.alpha * 255).astype(np.uint8))
        return a


def font(sz, bold=False):
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if bold else ''), sz)


def sprite_scale(cv, box=64, fill=0.78):
    """Verklein de tekening tot sprite-formaat: figuur ~fill van de box hoog."""
    a = Image.fromarray((cv.alpha * 255).astype(np.uint8))
    bb = a.getbbox()
    rgb = Image.fromarray(cv.img).crop(bb)
    al = a.crop(bb)
    w, h = rgb.size
    s = box * fill / max(w, h)
    nw, nh = max(1, round(w * s)), max(1, round(h * s))
    rgb = rgb.resize((nw, nh), Image.LANCZOS)
    al = al.resize((nw, nh), Image.LANCZOS).point(lambda v: 255 if v > 110 else 0)
    out = Image.new('RGBA', (box, box), (0, 0, 0, 0))
    ox, oy = (box - nw) // 2, box - nh - 2
    rgba = rgb.convert('RGBA')
    rgba.putalpha(al)
    out.paste(rgba, (ox, oy), rgba)
    return out


def silhouette(rgba, color=(20, 20, 24)):
    a = rgba.split()[3]
    s = Image.new('RGBA', rgba.size, (0, 0, 0, 0))
    s.paste(Image.new('RGBA', rgba.size, color + (255,)), (0, 0), a)
    return s
