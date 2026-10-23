"""Kleine vectortekenaar voor modeltekeningen (Sugimori-stijl).

Alles in een 256-eenheden-ruimte; intern op 4x getekend en verkleind
(alleen anti-aliasing, geen schaduw of ruis). Een onderdeel is een unie
van polygonen; elk onderdeel krijgt een donkere omlijning, ook waar het
een eerder onderdeel overlapt (zo ontstaan de binnenlijnen).
"""
import math
from PIL import Image, ImageDraw, ImageChops

S = 4            # supersampling
LINE = (46, 32, 38)


def ellipse(cx, cy, rx, ry, rot=0.0, n=72):
    a = math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return pts


def circle(cx, cy, r, n=48):
    return ellipse(cx, cy, r, r, 0, n)


def bez(*segs, n=24):
    """Gesloten pad uit kubische bezier-segmenten: segs = (p0, c1, c2, p3), ..."""
    pts = []
    for p0, c1, c2, p3 in segs:
        for i in range(n):
            t = i / n
            u = 1 - t
            x = u**3*p0[0] + 3*u*u*t*c1[0] + 3*u*t*t*c2[0] + t**3*p3[0]
            y = u**3*p0[1] + 3*u*u*t*c1[1] + 3*u*t*t*c2[1] + t**3*p3[1]
            pts.append((x, y))
    return pts


def wool(cx, cy, rx, ry, bumps, br, rot=0.0, skip=None, start=0.0):
    """Wolwolk: een ellips met een rand van gelijke bolletjes (Mareep-rand).
    skip = (van, tot) in graden: daar geen bolletjes (aansluiting)."""
    polys = [ellipse(cx, cy, rx - br * 0.55, ry - br * 0.55, rot)]
    a = math.radians(rot)
    for i in range(bumps):
        t = 2 * math.pi * i / bumps + math.radians(start)
        deg = math.degrees(t) % 360
        if skip and skip[0] <= deg <= skip[1]:
            continue
        x, y = (rx - br * 0.55) * math.cos(t), (ry - br * 0.55) * math.sin(t)
        polys.append(circle(cx + x * math.cos(a) - y * math.sin(a),
                            cy + x * math.sin(a) + y * math.cos(a), br))
    return polys


class Drawing:
    def __init__(self, size=256, bg=(255, 255, 255)):
        self.size = size
        self.img = Image.new('RGB', (size * S, size * S), bg)
        self.sil = Image.new('L', (size * S, size * S), 0)   # silhouet
        self.masks = {}

    def _mask(self, polys, grow=0.0):
        m = Image.new('L', self.img.size, 0)
        d = ImageDraw.Draw(m)
        for p in polys:
            sp = [(x * S, y * S) for x, y in p]
            d.polygon(sp, fill=255)
            if grow > 0:
                w = int(round(grow * 2 * S))
                d.line(sp + [sp[0]], fill=255, width=w, joint='curve')
                r = grow * S
                for x, y in sp[::3]:
                    d.ellipse((x - r, y - r, x + r, y + r), fill=255)
        return m

    def part(self, name, polys, fill, line=3.0, clip=None, lc=LINE, sil=True):
        """Teken een onderdeel. clip = naam van een eerder onderdeel (vachttekening)."""
        fm = self._mask(polys)
        om = self._mask(polys, line) if line else None
        if clip:
            cm = self.masks[clip]
            fm = ImageChops.multiply(fm, cm)
            if om:
                om = ImageChops.multiply(om, cm)
        if om:
            self.img.paste(lc, mask=om)
        self.img.paste(fill, mask=fm)
        self.masks[name] = fm
        if sil and not clip:
            self.sil = ImageChops.lighter(self.sil, om if om else fm)
        return fm

    def stroke(self, pts, width=2.0, col=LINE, closed=False):
        d = ImageDraw.Draw(self.img)
        sp = [(x * S, y * S) for x, y in pts]
        if closed:
            sp = sp + [sp[0]]
        d.line(sp, fill=col, width=int(round(width * S)), joint='curve')
        r = width * S / 2
        for x, y in (sp[0], sp[-1]):
            d.ellipse((x - r, y - r, x + r, y + r), fill=col)

    def dot(self, x, y, r, col):
        d = ImageDraw.Draw(self.img)
        d.ellipse(((x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S), fill=col)

    def result(self):
        return self.img.resize((self.size, self.size), Image.LANCZOS)

    def silhouette(self, col=(30, 30, 40), bg=(255, 255, 255)):
        out = Image.new('RGB', self.img.size, bg)
        out.paste(col, mask=self.sil)
        return out.resize((self.size, self.size), Image.LANCZOS), \
            self.sil.resize((self.size, self.size), Image.LANCZOS)


def curve(p0, c1, c2, p3, n=24):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        pts.append((u**3*p0[0] + 3*u*u*t*c1[0] + 3*u*t*t*c2[0] + t**3*p3[0],
                    u**3*p0[1] + 3*u*u*t*c1[1] + 3*u*t*t*c2[1] + t**3*p3[1]))
    return pts
