"""Koningstiran (Sapa Inca): 3D-poppetje voor pose A (rustig zittend, kop driekwart naar voren).
Gebaseerd op olinguito_v2/silhouet_kolibriemethode/pop3d.py. Diercoördinaten: x = naar achteren (kop links),
y = omhoog, z = naar de kijker bij 0° (zijaanzicht). Het lijf draait `yaw`, de kop draait `yaw + extra`
(kop naar de kijker, olinguito-les). De waaier staat dwars op de kop (vlak y-z), zoals bij de echte vogel.
Draaien vanuit de repo-root: python3 docs/concept/sprites/koningstiran/pop3d.py"""
import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
R = 768
LINE = np.array((43, 27, 23), np.uint8)
COL = {
    'body': '#2e2a2c', 'breast': '#e8b850', 'wing': '#3a3436', 'farwing': '#242022', 'tail': '#b8602e',
    'head': '#2e2a2c', 'face': '#e0482c', 'beak': '#c8d0d8', 'eye': '#140e0a', 'glint': '#ffffff',
    'fan': '#f0561e', 'fanspot': '#140e0a', 'fanrim': '#9c8ad8', 'gold': '#f0c040', 'leg': '#f0a040',
    'claw': '#1a1416',
}
NOSHADE = {'eye', 'glint', 'fanspot'}
LINED = {'eye', 'gold', 'beak', 'face'}


def hexc(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float32)


def rot_y(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rot_x(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def rot_z(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


class Model:
    def __init__(self):
        self.parts = []

    def ell(self, c, r, g, R0=None):
        self.parts.append((np.array(c, float), np.array(r if np.ndim(r) else (r, r, r), float),
                           np.eye(3) if R0 is None else R0, g))

    def chain(self, pts, g, step=1.2):
        for a, b in zip(pts, pts[1:]):
            a, b = np.array(a, float), np.array(b, float)
            n = max(2, int(np.linalg.norm(b[:3] - a[:3]) / step))
            for i in range(n):
                p = a + (b - a) * i / n
                self.ell(p[:3], p[3], g)
        p = np.array(pts[-1], float)
        self.ell(p[:3], p[3], g)

    def transform(self, i0, Rm, piv):
        """Draai onderdelen vanaf index i0 om een draaipunt (kop t.o.v. het lijf)."""
        piv = np.array(piv, float)
        for k in range(i0, len(self.parts)):
            c, r, R0, g = self.parts[k]
            self.parts[k] = (piv + Rm @ (c - piv), r, Rm @ R0, g)


def bird(extra=25, fan_L=58, fan_n=17, tilt=6):
    """Hybride: bouw van de bergcaracara (groot, rechtop, lange poten, haaksnavel, kaal rood gezicht),
    kroon en staart van de koningstiran. De zijveren van de waaier hangen omlaag (foto 2) en vormen zo
    zelf de franje van de mascaypacha; geen losse band (geen 'dier met een hoed')."""
    m = Model()
    A = rot_z(math.radians(104))  # bijna rechtop, zoals de caracara op de foto
    m.ell((6, 4, 0), (44, 28, 27), 'body', A)
    m.ell((-8, 6, 0), (22, 32, 25), 'breast', rot_z(math.radians(-8)))
    for sz, g in ((1, 'wing'), (-1, 'farwing')):
        m.ell((12, 6, 19 * sz), (40, 14, 7), g, A)
    m.ell((22, -50, 0), (7, 26, 11), 'tail', rot_z(math.radians(-14)))
    for sz in (1, -1):
        m.chain([(0, -32, 9 * sz, 5.5), (-2, -44, 9 * sz, 4.2)], 'breast')   # broek
        m.chain([(-2, -44, 9 * sz, 3.2), (-3, -60, 9 * sz, 2.8)], 'leg')     # lange caracarapoten
        for dz, dx in ((-3, -8), (0, -9), (3, -7)):
            m.chain([(-3, -60, 9 * sz, 2.4), (dx, -63, 9 * sz + dz, 2.0)], 'leg')
            m.ell((dx - 1.5, -64, 9 * sz + dz), 1.4, 'claw')
        m.chain([(-3, -60, 9 * sz, 2.2), (2, -63, 9 * sz, 1.8)], 'leg')
    # ---- kop: kleiner t.o.v. het lijf dan bij de tiran (caracara), wel groter dan echt ----
    i0 = len(m.parts)
    hc = np.array((-12, 50, 0.0))
    m.chain([(-6, 26, 0, 18), (-10, 42, 0, 16)], 'body')
    m.ell(hc, (16, 15, 15), 'head')
    for sz in (1, -1):
        m.ell(hc + np.array((-9, -1, 6.5 * sz)), (8, 7, 5), 'face')        # kaal rood gezicht
    # haaksnavel: breed aan de basis (tiran), punt omlaag (caracara)
    m.chain([(-22, 48, 0, 5.2), (-30, 47, 0, 4.0), (-36, 45, 0, 2.8), (-38, 41, 0, 1.8), (-36, 38, 0, 1.0)], 'beak', 0.6)
    for sz in (1, -1):
        d = np.array((-0.55, 0.28, 0.78 * sz)); d /= np.linalg.norm(d)
        e = hc + d * 14.6
        m.ell(e, 3.0, 'eye')
        m.ell(e + d * 1.5 + np.array((-0.6, 1.1, 0)), 0.9, 'glint')
        dc = np.array((0.25, -0.15, 1.0 * sz)); dc /= np.linalg.norm(dc)
        m.ell(hc + dc * 14.8 + np.array((3, -3, 0)), (5.5, 5.5, 1.6), 'gold')  # gouden oorschijf (orejon)
    # waaier: dichte halve paraplu dwars op de kop; brede platte veren die overlappen (foto's),
    # zijveren buigen omlaag tot onder ooghoogte en vormen zo de franje
    base = hc + np.array((3, 10, 0))
    nrm = np.array((1.0, -0.28, 0)); nrm /= np.linalg.norm(nrm)
    def feather(th):
        d = np.array((0.28, math.cos(th), math.sin(th))); d /= np.linalg.norm(d)
        t = np.cross(nrm, d); t /= np.linalg.norm(t)
        return d, np.stack([d, t, np.cross(d, t)], 1)
    for k in range(fan_n):   # kap: dichte halve paraplu
        d, Rf = feather(math.radians(-88 + 176 * k / (fan_n - 1)))
        L = fan_L
        m.ell(base + d * L * 0.42, (L * 0.38, 6.0, 1.8), 'fan', Rf)
        m.ell(base + d * L * 0.76, (L * 0.22, 10.0, 2.0), 'fan', Rf)
        m.ell(base + d * L * 0.95, (L * 0.08, 9.5, 2.2), 'fanrim', Rf)
    for sg in (1, -1):        # franje: drie losse kwastjes per kant die van de rand van de kap omlaag hangen
        for j, (ang, ln) in enumerate(((82, 30), (70, 26), (58, 20))):
            d, Rf = feather(math.radians(ang * sg))
            root = base + d * fan_L * 0.88
            end = root + np.array((0.1, -1.0, 0.12 * sg)) * ln
            m.chain([tuple(root) + (3.4,), tuple((root + end) / 2) + (3.0,), tuple(end) + (2.8,)], 'fan', 1.0)
            m.ell(end + np.array((0, -2.5, 0)), (3.4, 4.2, 3.0), 'fanrim')
    Rh = rot_y(math.radians(extra)) @ rot_z(math.radians(-tilt))
    m.transform(i0, Rh, (-8, 30, 0))
    return m


def render(m, yaw, pitch, scale, center):
    Rc = rot_x(math.radians(pitch)) @ rot_y(math.radians(yaw))
    zbuf = np.full((R, R), -1e9, np.float32)
    gid = np.full((R, R), -1, np.int16)
    nrm = np.zeros((R, R, 3), np.float32)
    groups = list(COL)
    ys, xs = np.mgrid[0:R, 0:R]
    wx = (xs - R / 2) / scale + center[0]
    wy = -((ys - R / 2) / scale) + center[1]
    for c, r, R0, g in m.parts:
        cw = Rc @ c
        M = np.diag(1 / r) @ R0.T @ Rc.T
        ext = r.max()
        x0 = int(max(0, (cw[0] - ext - center[0]) * scale + R / 2 - 2)); x1 = int(min(R, (cw[0] + ext - center[0]) * scale + R / 2 + 3))
        y0 = int(max(0, (-(cw[1] + ext) + center[1]) * scale + R / 2 - 2)); y1 = int(min(R, (-(cw[1] - ext) + center[1]) * scale + R / 2 + 3))
        if x0 >= x1 or y0 >= y1:
            continue
        px = wx[y0:y1, x0:x1] - cw[0]
        py = wy[y0:y1, x0:x1] - cw[1]
        a = M[:, 0, None, None] * px + M[:, 1, None, None] * py
        b = M[:, 2]
        A = b @ b
        B = 2 * (a * b[:, None, None]).sum(0)
        C = (a * a).sum(0) - 1
        disc = B * B - 4 * A * C
        hit = disc >= 0
        z = (-B + np.sqrt(np.where(hit, disc, 0))) / (2 * A) + cw[2]
        sub = zbuf[y0:y1, x0:x1]
        win = hit & (z > sub)
        sub[win] = z[win]
        gid[y0:y1, x0:x1][win] = groups.index(g)
        p = np.stack([px, py, z - cw[2]], -1)
        n = p @ (M.T @ M).T
        n /= np.linalg.norm(n, axis=-1, keepdims=True) + 1e-9
        nrm[y0:y1, x0:x1][win] = n[win]
    return zbuf, gid, nrm, groups


def shade(zbuf, gid, nrm, groups):
    a = gid >= 0
    rgb = np.ones((R, R, 3), np.float32) * 255
    L = np.array((-0.45, 0.65, 0.62)); L /= np.linalg.norm(L)
    lit = (nrm @ L) > -0.2
    for i, g in enumerate(groups):
        mm = gid == i
        col = hexc(COL[g])
        rgb[mm] = col
        if g not in NOSHADE:
            rgb[mm & ~lit] = col * 0.80
    edge = np.zeros((R, R), bool)
    z = np.where(a, zbuf, -1e9)
    lined = np.isin(gid, [groups.index(g) for g in LINED])
    for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):
        z2 = np.roll(np.roll(z, -dy, 0), -dx, 1)
        g2 = np.roll(np.roll(gid, -dy, 0), -dx, 1)
        l2 = np.roll(np.roll(lined, -dy, 0), -dx, 1)
        e = (np.abs(z - z2) > 6) | ((gid != g2) & (lined | l2))
        edge |= e
        edge |= np.roll(np.roll(e, dy, 0), dx, 1)
    for _ in range(2):
        edge = edge | np.roll(edge, 1, 0) | np.roll(edge, 1, 1)
    inner = a.copy()
    for _ in range(7):
        inner = inner & np.roll(inner, 1, 0) & np.roll(inner, -1, 0) & np.roll(inner, 1, 1) & np.roll(inner, -1, 1)
    edge = (edge & a) | (a & ~inner)
    rgb[edge] = LINE
    rgb[~a] = 255
    return Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).resize((256, 256), Image.LANCZOS), a


def bbox(m, yaw, pitch):
    Rc = rot_x(math.radians(pitch)) @ rot_y(math.radians(yaw))
    pts = np.array([Rc @ c for c, r, R0, g in m.parts])
    rs = np.array([r.max() for c, r, R0, g in m.parts])
    return (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()


def view(m, yaw, pitch=8, size=236):
    x0, x1, y0, y1 = bbox(m, yaw, pitch)
    scale = R * (size / 256) / max(x1 - x0, y1 - y0)
    im, a = shade(*render(m, yaw, pitch, scale, ((x0 + x1) / 2, (y0 + y1) / 2)))
    sil = Image.fromarray((a * 255).astype(np.uint8)).resize((64, 64), Image.LANCZOS).point(lambda v: 255 if v > 110 else 0)
    return im, sil


def sheet(yaws=(20, 32, 44), extras=(15, 28, 40)):
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
    cw, ch = 266 + 70, 256 + 26
    W = Image.new('RGB', (12 + cw * len(extras), 40 + ch * len(yaws)), (236, 232, 222))
    d = ImageDraw.Draw(W)
    d.text((10, 10), 'Sapa Inca (koningstiran x bergcaracara), pose A. Rij = lijf, kolom = kop extra gedraaid. Rechts: silhouet 1x.',
           font=FB, fill=(30, 30, 30))
    for i, yaw in enumerate(yaws):
        for j, ex in enumerate(extras):
            im, sil = view(bird(extra=ex), yaw)
            x, y = 10 + j * cw, 36 + i * ch
            W.paste(im, (x, y))
            blk = Image.new('RGB', (64, 64), (20, 20, 24))
            W.paste(blk, (x + 262, y + 180), sil)
            tag = f'{chr(65 + i)}{j + 1}'
            d.text((x + 4, y + 258), f'{tag}: lijf {yaw}°, kop {yaw + ex}° (frontaal = 90°)', font=F, fill=(50, 50, 50))
    W.save(os.path.join(HERE, 'pop3d_hoeken.png'))


if __name__ == '__main__':
    sheet()
