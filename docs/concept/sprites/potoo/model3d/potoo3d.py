"""Great potoo: 3D-poppetje (ellipsoïden) vóór het silhouet (Jordi, 5 nov: "Voordat je een silhouet bouwt, bouw je eerst een 3d model").
Ontwerp: ontwerp/model_c2.png + ONTWERP.md. Diercoördinaten: x = naar achteren (kop links), y = omhoog, z = naar de kijker.
Engine overgenomen uit olinguito_v2/silhouet_kolibriemethode/pop3d.py (zonder de olinguito-kopkleuring).
Draaien: python3 docs/concept/sprites/potoo/model3d/potoo3d.py"""
import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = HERE
R = 768          # renderresolutie (3x van 256)
HEAD_SCALE = 1.35
LEG_K = 1.0      # dikte van de poten (sprite: dikker, geen stokpoten)
HEAD_SHIFT = np.array((-6, 30, 0.0))
LINE = np.array((43, 27, 23), np.uint8)

COL = {
    'fur': '#EEECF3', 'wing': '#D3CFDE', 'belly': '#FAF9FC', 'tail': '#C6C1D3', 'jaw': '#6C657C',
    'mouth': '#5A4DB8', 'throat': '#1E1842', 'beak': '#7A7388', 'eye': '#050507',
}
NOSHADE = {'eye', 'throat'}
LINED = {'eye', 'mouth', 'throat', 'beak'}


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
        self.parts = []   # (center, radii, R0, group)

    def ell(self, c, r, g, R0=None):
        self.parts.append((np.array(c, float), np.array(r if np.ndim(r) else (r, r, r), float),
                           np.eye(3) if R0 is None else R0, g))

    def chain(self, pts, g, step=1.5):
        """Getaperde buis: bollen langs punten (x, y, z, straal)."""
        for (a, b) in zip(pts, pts[1:]):
            a, b = np.array(a, float), np.array(b, float)
            n = max(2, int(np.linalg.norm(b[:3] - a[:3]) / step))
            for i in range(n):
                t = i / n
                p = a + (b - a) * t
                self.ell(p[:3], p[3], g)
        p = np.array(pts[-1], float)
        self.ell(p[:3], p[3], g)


def qb(a, c, b, n):
    a, c, b = map(np.array, (a, c, b))
    return [tuple((1 - t) ** 2 * a + 2 * (1 - t) * t * c + t * t * b) for t in np.linspace(0, 1, n)]



def render(m, yaw, pitch, scale, center):
    Rc = rot_x(math.radians(pitch)) @ rot_y(math.radians(yaw))
    zbuf = np.full((R, R), -1e9, np.float32)
    gid = np.full((R, R), -1, np.int16)
    nrm = np.zeros((R, R, 3), np.float32)
    wpt = np.zeros((R, R, 3), np.float32)
    groups = list(COL)
    ys, xs = np.mgrid[0:R, 0:R]
    # schermcoördinaten -> wereld (x rechts, y omhoog)
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
        q = np.stack([wx[y0:y1, x0:x1], wy[y0:y1, x0:x1], z], -1)
        wpt[y0:y1, x0:x1][win] = q[win]
    return zbuf, gid, nrm, groups


def shade(zbuf, gid, nrm, groups):
    a = gid >= 0
    rgb = np.ones((R, R, 3), np.float32) * 255
    L = np.array((-0.45, 0.65, 0.62)); L /= np.linalg.norm(L)
    lit = (nrm @ L) > -0.2
    for i, g in enumerate(groups):
        m = gid == i
        col = hexc(COL[g])
        rgb[m] = col
        if g not in NOSHADE:
            rgb[m & ~lit] = col * 0.80
    # omlijning: dieptesprong tussen buren, plus kleurgrens bij oog/neus/klauwen, plus silhouet
    edge = np.zeros((R, R), bool)
    z = np.where(a, zbuf, -1e9)
    lined = np.isin(gid, [groups.index(g) for g in LINED])
    for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):
        z2 = np.roll(np.roll(z, -dy, 0), -dx, 1)
        g2 = np.roll(np.roll(gid, -dy, 0), -dx, 1)
        l2 = np.roll(np.roll(lined, -dy, 0), -dx, 1)
        jump = np.abs(z - z2) > 5
        cb = (gid != g2) & (lined | l2)
        e = jump | cb
        edge |= e
        edge |= np.roll(np.roll(e, dy, 0), dx, 1)
    for _ in range(3):
        edge = edge | np.roll(edge, 1, 0) | np.roll(edge, 1, 1)
    sil = a.copy()
    inner = a.copy()
    for _ in range(9):
        inner = inner & np.roll(inner, 1, 0) & np.roll(inner, -1, 0) & np.roll(inner, 1, 1) & np.roll(inner, -1, 1)
    edge = (edge & a) | (sil & ~inner)
    rgb[edge] = LINE
    rgb[~a] = 255
    im = Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).resize((256, 256), Image.LANCZOS)
    return im


def bbox(m, yaw, pitch):
    Rc = rot_x(math.radians(pitch)) @ rot_y(math.radians(yaw))
    pts = np.array([Rc @ c for c, r, R0, g in m.parts])
    rs = np.array([r.max() for c, r, R0, g in m.parts])
    return (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()


def view(m, yaw, pitch=8, size=232):
    x0, x1, y0, y1 = bbox(m, yaw, pitch)
    scale = R * (size / 256) / max(x1 - x0, y1 - y0)
    return shade(*render(m, yaw, pitch, scale, ((x0 + x1) / 2, (y0 + y1) / 2)))


HEAD = 1.25   # kop groter dan echt (Pokémon), grote ogen, grote mond


def potoo(lean=15, gape=46):
    m = Model()
    Rl = rot_z(math.radians(lean))           # hele vogel licht voorover (kop naar links)
    P = lambda p: Rl @ np.array(p, float)
    E = lambda c, r, g, R0=None: m.ell(P(c), r, g, Rl if R0 is None else Rl @ R0)
    # lijf: rechtop peervormig, breed van onder; schouders lopen zonder nek in de kop over
    E((2, -6, 0), (23, 33, 24), 'fur')
    E((-5, -10, 5), (16, 25, 18), 'belly')
    E((0, 20, 0), (22, 18, 23), 'fur')
    # vleugels langs de zij, punten over de staartwortel
    for sz in (1, -1):
        E((9, -10, 19 * sz), (10, 33, 7), 'wing', rot_z(math.radians(-12)))
    # staart: lang, breed en plat (veren), hangt schuin naar achteren-omlaag
    for t in np.linspace(0, 1, 14):
        E((12 + 12 * t, -28 - 48 * t, 0), (6, 10, 12 + 5 * t), 'tail')
    # kop: groot, breed, plat van boven
    h = HEAD
    sk = np.array((-6, 44, 0.0))
    E(sk, np.array((26, 19, 26)) * h, 'fur')
    # snavel (Jordi: "de muil moet wel echt een snavel zijn"): brede platte bovensnavel met haakpunt,
    # ondersnavel hangt open (gape graden) vanaf de mondhoek; geestpaarse binnenkant en donkere keel ertussen
    hinge = sk + np.array((-2, -8, 0)) * h
    def snavel(rot, g, haak):
        for t in np.linspace(0, 1, 12):
            r = 19 * (1 - t) + 2.6 * t
            c = hinge + rot @ (np.array((-36 * t, 0, 0)) * h)
            rz = r if haak else 19 * (1 - t) + 7 * t      # ondersnavel: brede lepel, ronde punt
            E(c, np.array((r * 0.7, r * 0.42, rz)) * h, g, rot)
        if haak:
            E(hinge + rot @ (np.array((-36.5, -3, 0)) * h), np.array((2, 2.6, 1.8)) * h, g, rot)
    Ru = rot_z(math.radians(-8)); Rd = rot_z(math.radians(gape))
    snavel(Ru, 'beak', True)
    snavel(Rd, 'jaw', False)
    Rm = rot_z(math.radians(gape * 0.5))
    E(hinge + Rm @ (np.array((-15, 0, 0)) * h), np.array((17, 9, 16)) * h, 'mouth', Rm)
    E(hinge + np.array((3, -2, 0)) * h, np.array((6, 6, 8)) * h, 'throat')
    # ogen: groot, pikzwart (Drifloon), naar voren zodat in 3/4 beide te zien zijn
    for sz in (1, -1):
        d = np.array((-0.72, 0.32, 0.62 * sz)); d /= np.linalg.norm(d)
        c = sk + np.array((26 * d[0], 19 * d[1], 26 * d[2])) * h * 0.88
        E(c, np.array((9, 10, 5)) * h, 'eye', rot_y(math.atan2(d[0], d[2])))
    return m


def sheet():
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
    yaws, leans = (35, 50, 65), (10, 20)
    im = Image.new('RGB', (10 + 266 * len(yaws), 40 + 290 * len(leans)), 'white')
    d = ImageDraw.Draw(im)
    d.text((10, 10), 'Great potoo: 3D-poppetje (lijfhoek x voorover)', font=FB, fill=(30, 30, 30))
    for r, lean in enumerate(leans):
        m = potoo(lean)
        for c, yaw in enumerate(yaws):
            v = view(m, yaw)
            im.paste(v, (10 + 266 * c, 40 + 290 * r))
            d.text((10 + 266 * c, 40 + 290 * r + 260), f'{chr(65 + r)}{c + 1}: lijf {yaw}°, voorover {lean}°', font=F, fill=(60, 60, 60))
    im.save(os.path.join(OUT, 'hoeken.png'))


if __name__ == '__main__':
    sheet()
