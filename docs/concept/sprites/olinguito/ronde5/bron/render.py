"""Olinguito ronde 5: vormen -> Gen 3-cel-shading (sikkels via verschoven maskers) -> ASCII.
Daarna gaat het ASCII-bestand met de hand verder (gezicht, klauwen, munt, vacht).

  python3 render.py uit.txt
"""
import sys
import numpy as np
from PIL import Image, ImageDraw

S = 64
CH = '.123456789abcdef'
YY, XX = np.mgrid[0:S, 0:S] + 0.5

RAMP = {
    'fur': [1, 2, 3, 4],
    'far': [2, 3, 4, 4],       # verre ledematen: een tint donkerder
    'dark': [5, 5, 6, 6],
    'cream': [7, 7, 8, 8],
    'green': [12, 12, 13, 13],
    'gold': [9, 10, 11, 11],
    'black': [15, 15, 15, 15],
}


SC, OX, OY, TX, TY = 0.88, 31.0, 36.0, 0.0, 1.0


def T(x, y):
    return OX + (x - OX) * SC + TX, OY + (y - OY) * SC + TY


def m_ell(cx, cy, rx, ry, rot=0.0, raw=False):
    if not raw:
        cx, cy = T(cx, cy); rx *= SC; ry *= SC
    c, s = np.cos(rot), np.sin(rot)
    u = (XX - cx) * c + (YY - cy) * s
    w = -(XX - cx) * s + (YY - cy) * c
    return (u / rx) ** 2 + (w / ry) ** 2 <= 1


def m_poly(pts):
    im = Image.new('L', (S, S), 0)
    ImageDraw.Draw(im).polygon([T(*p) for p in pts], fill=1)
    return np.array(im).astype(bool)


def m_tube(pts, w0, w1, tmap=None):
    m = np.zeros((S, S), bool)
    n = len(pts) - 1
    for k in range(n * 16 + 1):
        t = k / (n * 16)
        i = min(int(t * n), n - 1); f = t * n - i
        x = pts[i][0] * (1 - f) + pts[i + 1][0] * f
        y = pts[i][1] * (1 - f) + pts[i + 1][1] * f
        r = w0 * (1 - t) + w1 * t
        x, y = T(x, y)
        e = m_ell(x, y, r * SC, r * SC, raw=True)
        if tmap is not None:
            tmap[e & ~m] = t
        m |= e
    return m


def shift(m, dx, dy):
    out = np.zeros_like(m)
    ys, xs = np.nonzero(m)
    ys2, xs2 = ys + dy, xs + dx
    ok = (ys2 >= 0) & (ys2 < S) & (xs2 >= 0) & (xs2 < S)
    out[ys2[ok], xs2[ok]] = True
    return out


class Sprite:
    def __init__(self):
        self.idx = np.zeros((S, S), np.uint8)
        self.pid = np.full((S, S), -1, int)
        self.parts = []

    def add(self, m, ramp, hl=1, sh=2, rim=True, hl_lim=None, cast=True, line=True, flat=None):
        """hl: dikte hooglichtsikkel linksboven (0 = geen); sh: dikte schaduwsikkel rechtsonder.
        hl_lim: (x0, y0, x1, y1) hooglicht alleen binnen dit kader."""
        r = RAMP[ramp]
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
                h &= ~(m & ~shift(m, -sh, -sh)) if sh else h
                if hl_lim:
                    x0, y0, x1, y1 = hl_lim
                    h &= (XX >= x0) & (XX < x1) & (YY >= y0) & (YY < y1)
                t[h] = r[0]
        else:
            t[:] = flat
        k = len(self.parts)
        under = self.pid >= 0
        # slagschaduw op wat eronder ligt: pixels net onder/rechts van deze vorm
        if cast:
            c = shift(m, 1, 2) & ~m & under
            for y, x in zip(*np.nonzero(c)):
                pr = self.parts[self.pid[y, x]]
                if self.idx[y, x] in (pr[0], pr[1]):
                    self.idx[y, x] = pr[2]
        # binnenlijn: rand van deze vorm waar hij over een andere vorm ligt
        self.idx[m] = t[m]
        self.pid[m] = k
        if line:
            edge = np.zeros_like(m)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                edge |= m & shift(under & ~m, -dx, -dy)
            for y, x in zip(*np.nonzero(edge)):
                # licht (linksboven) -> donkerste tint, schaduwkant -> zwart
                ny = 0; nx = 0
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < S and 0 <= xx < S and not m[yy, xx]:
                        nx += dx; ny += dy
                self.idx[y, x] = r[3] if (nx + ny) < 0 else 15
        self.parts.append(r)

    def outline(self):
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
                # buur rechtsonder van ons => wij liggen linksboven van de vorm => selout
                p = self.parts[nb[0][2]]
                if sx + sy > 0 and p[3] != 15:
                    out[y, x] = p[3]
                else:
                    out[y, x] = 15
        self.idx = out


def frame(k):
    s = Sprite()
    # --- staart (achter alles): ringen
    if k == 0:
        tp = [(41, 46), (47, 45), (51, 41), (52, 35), (50, 30.5), (46.5, 30)]
    else:
        tp = [(40, 47), (47, 47), (51.5, 43), (53.5, 37), (52, 31), (48.5, 29.5)]
    tail = m_tube(tp, 3.3, 2.3)
    s.add(tail, 'fur', hl=1, sh=2)
    # ringen: banden dwars op de staart (param t van de buis)
    tm = np.zeros((S, S))
    m_tube(tp, 3.3, 2.3, tm)
    rings = tail & (((tm > 0.27) & (tm < 0.40)) | ((tm > 0.55) & (tm < 0.67)) | (tm > 0.82))
    s.idx[rings & np.isin(s.idx, (1, 2))] = 5
    s.idx[rings & np.isin(s.idx, (3, 4))] = 6
    # --- verre achterpoot (stap naar achteren)
    s.add(m_tube([(40, 48), (43, 52), (44, 54.5)], 2.4, 1.8), 'far')
    s.add(m_ell(45.5, 55.5, 2.5, 1.5), 'dark', hl=0, sh=1)
    # --- verre arm
    if k == 0:
        s.add(m_tube([(31, 37), (30, 41), (28.5, 43)], 2.1, 1.8), 'far')
    else:
        s.add(m_tube([(31, 37), (36, 34), (39, 31)], 2.1, 1.8), 'far')
        s.add(m_ell(40, 30, 2.2, 2.2), 'dark', hl=0, sh=1)
    # --- lijf (schuin: borst linksboven, achterwerk rechtsonder)
    s.add(m_ell(32, 43, 8, 6.5, rot=0.45), 'fur', hl=1, sh=2)
    s.add(m_ell(27.5, 41.5, 3, 4.5, rot=0.3), 'cream', hl=0, sh=1, cast=False)
    # --- dichte achterpoot: ronde dij (gehurkt) + scheen + voet op de teen
    s.add(m_ell(36.5, 46, 5.5, 5.5), 'fur', hl=1, sh=2)
    s.add(m_tube([(35, 50), (32, 53.5)], 2.6, 2.2), 'fur', hl=0, sh=1, cast=False)
    s.add(m_ell(29, 55, 3.8, 1.7), 'dark', hl=0, sh=1)
    # --- halsdoek
    s.add(m_poly([(15, 32), (32, 33), (34, 37), (17, 36)]), 'green', hl=0, sh=1)
    if k == 0:
        s.add(m_poly([(32, 33), (39, 30), (40.5, 32.5), (36, 36.5), (34, 37)]), 'green', hl=0, sh=1)
    else:
        s.add(m_poly([(32, 33), (40, 31.5), (41.5, 34.5), (36, 37), (34, 37)]), 'green', hl=0, sh=1)
    # --- kop
    s.add(m_ell(14.5, 16.5, 3.2, 3.4), 'fur', hl=1, sh=1)
    s.add(m_ell(29, 13.2, 3.9, 3.9), 'fur', hl=1, sh=1)
    head = m_ell(22.5, 23, 11.2, 9.2)
    s.add(head, 'fur', hl=2, sh=2, hl_lim=(10, 13, 26, 21))
    s.add(m_ell(11.5, 26.8, 4.8, 3.2), 'cream', hl=0, sh=1, cast=False)
    # --- munt en dichte arm
    if k == 0:
        s.add(m_ell(24, 43, 4.3, 4.3), 'gold', hl=1, sh=1)
        s.add(m_tube([(25, 36), (20, 38), (16, 36.5)], 2.4, 2.1), 'fur', hl=1, sh=1)
        s.add(m_tube([(20, 38), (16, 36.5)], 2.3, 2.1), 'dark', hl=0, sh=1, cast=False)
    else:
        s.add(m_ell(45.5, 14, 2.2, 3.6), 'gold', hl=1, sh=1)
        s.add(m_tube([(16, 38), (11, 39), (7, 37.5)], 2.3, 2.1), 'dark', hl=0, sh=1)
        s.add(m_tube([(25, 36), (19, 38), (15, 38.5)], 2.4, 2.1), 'fur', hl=1, sh=1, cast=False)
    s.outline()
    return s.idx


if __name__ == '__main__':
    with open(sys.argv[1], 'w') as f:
        for k in range(2):
            f.write('== frame %d\n' % (k + 1))
            for row in frame(k):
                f.write(''.join(CH[v] for v in row) + '\n')
