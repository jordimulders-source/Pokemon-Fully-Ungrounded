"""Kleine vectorbibliotheek voor modeltekeningen in Sugimori-stijl.
Coordinaten in 256-eenheden, intern 4x supersampling."""
import math
import numpy as np
from PIL import Image, ImageDraw

S = 4
N = 256 * S
LINE = (43, 27, 23)


def hexc(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def ell(cx, cy, rx, ry, rot=0, n=72):
    r = math.radians(rot)
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        x, y = rx * math.cos(a), ry * math.sin(a)
        pts.append((cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r)))
    return pts


def blob(pts, n=14):
    """Gesloten Catmull-Rom-curve door de punten."""
    out = []
    k = len(pts)
    for i in range(k):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % k], pts[(i + 2) % k]
        for j in range(n):
            t = j / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[d]) + (-p0[d] + p2[d]) * t + (2 * p0[d] - 5 * p1[d] + 4 * p2[d] - p3[d]) * t2
                                    + (-p0[d] + 3 * p1[d] - 3 * p2[d] + p3[d]) * t3) for d in (0, 1)))
    return out


def qbez(a, c, b, n=24):
    return [((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0],
             (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1]) for t in (i / n for i in range(n + 1))]


def claw(base, tip, bend, w):
    """Sikkelklauw: middenlijn = kwadratische bezier, breedte loopt af naar 0."""
    mx, my = (base[0] + tip[0]) / 2, (base[1] + tip[1]) / 2
    dx, dy = tip[0] - base[0], tip[1] - base[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    c = (mx + nx * bend, my + ny * bend)
    cl = qbez(base, c, tip, 20)
    left, right = [], []
    for i, p in enumerate(cl):
        t = i / (len(cl) - 1)
        if i < len(cl) - 1:
            q = cl[i + 1]
            ddx, ddy = q[0] - p[0], q[1] - p[1]
        dl = math.hypot(ddx, ddy) or 1
        px, py = -ddy / dl, ddx / dl
        ww = w * (1 - t ** 1.5) / 2
        left.append((p[0] + px * ww, p[1] + py * ww))
        right.append((p[0] - px * ww, p[1] - py * ww))
    return left + right[::-1]


def tube(pts, widths):
    """Dikke lijn langs punten met per punt een breedte (staarten, ledematen)."""
    left, right = [], []
    for i, p in enumerate(pts):
        q = pts[min(i + 1, len(pts) - 1)]
        o = pts[max(i - 1, 0)]
        dx, dy = q[0] - o[0], q[1] - o[1]
        dl = math.hypot(dx, dy) or 1
        px, py = -dy / dl, dx / dl
        w = widths[i] / 2
        left.append((p[0] + px * w, p[1] + py * w))
        right.append((p[0] - px * w, p[1] - py * w))
    return left + right[::-1]


def erode(m, n):
    m = m.copy()
    for i in range(n):
        e = m.copy()
        e[1:, :] &= m[:-1, :]
        e[:-1, :] &= m[1:, :]
        e[:, 1:] &= m[:, :-1]
        e[:, :-1] &= m[:, 1:]
        if i % 2:
            e[1:, 1:] &= m[:-1, :-1]
            e[:-1, :-1] &= m[1:, 1:]
            e[1:, :-1] &= m[:-1, 1:]
            e[:-1, 1:] &= m[1:, :-1]
        m = e
    return m


class Canvas:
    def __init__(self):
        self.rgb = np.zeros((N, N, 3), np.uint8)
        self.alpha = np.zeros((N, N), bool)

    def mask(self, pts):
        im = Image.new('L', (N, N), 0)
        ImageDraw.Draw(im).polygon([(x * S, y * S) for x, y in pts], fill=255)
        return np.array(im) > 127

    def part(self, pts, color, line=2.0, clip=None, open_at=None):
        m = self.mask(pts) if not isinstance(pts, np.ndarray) else pts
        if clip is not None:
            m = m & clip
        self.rgb[m] = hexc(color) if isinstance(color, str) else color
        if line:
            ring = m & ~erode(m, int(line * S))
            if open_at:
                ox, oy, orr = open_at
                yy, xx = np.ogrid[:N, :N]
                ring &= (xx - ox * S) ** 2 + (yy - oy * S) ** 2 > (orr * S) ** 2
            self.rgb[ring] = LINE
        self.alpha |= m
        return m

    def mark(self, pts, color, clip, line=0):
        m = self.mask(pts) & clip
        self.rgb[m] = hexc(color)
        if line:
            ring = m & ~erode(m, int(line * S))
            # alleen de lijn binnen de ouder, niet op diens rand
            self.rgb[ring & erode(clip, int(line * S))] = LINE
        return m

    def stroke(self, pts, w=2.0, color=None):
        im = Image.new('L', (N, N), 0)
        ImageDraw.Draw(im).line([(x * S, y * S) for x, y in pts], fill=255, width=int(w * S), joint='curve')
        m = np.array(im) > 127
        self.rgb[m] = color if color else LINE
        self.alpha |= m
        return m

    def dot(self, x, y, r, color):
        return self.part(ell(x, y, r, r), color, line=0)

    def finish(self, outer=3.0, size=256):
        a = self.alpha
        ring = a & ~erode(a, int(outer * S))
        rgb = self.rgb.copy()
        rgb[ring] = LINE
        out = np.full((N, N, 3), 255, np.uint8)
        out[a] = rgb[a]
        im = Image.fromarray(out).resize((size, size), Image.LANCZOS)
        sil = Image.fromarray((a * 255).astype(np.uint8)).resize((size, size), Image.LANCZOS)
        return im, sil
