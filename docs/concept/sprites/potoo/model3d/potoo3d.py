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
    'fur': '#EEECF3', 'wing': '#D3CFDE', 'belly': '#FAF9FC', 'tail': '#C6C1D3', 'jaw': '#6C657C', 'rim': '#F7F5F9',
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


# Oriëntatiepunten gemeten op referenties/jordi_great_potoo_vooroverhangend_bek_open.webp (578x565, kijkt naar rechts).
# Omrekening: x = -(px - 250) * 0.3 (kop links), y = -(py - 300) * 0.3. Waarden in fotopixels erbij.
LM = dict(
    snaveltip=(-76.5, 66),      # (505, 80) haakje
    mondhoek=(-37.5, 60),       # (375, 100) onder/achter het oog
    onderkaaktip=(-62, 38),     # (465, 150) op de zijfoto; iets verder open zoals de 3/4-foto (opening ±1/2 kophoogte)
    oog=(-49.5, 69),            # (415, 70), ±35x20 px
    kruin=(-24, 82.5),          # (330, 25)
    achterhoofd=(6, 72),        # (230, 60)
    schouder=(36, 54),          # (130, 120) rug hoog, gebogen
    rug=(46.5, 15),             # (95, 250)
    borst=(-37.5, 30),          # (375, 200)
    onderlijf=(-18, -39),       # (310, 430)
    staartonder=(9, -73.5),     # (220, 545), staart ±185 px breed onderaan, hangt recht omlaag
)
KOP = 1.8                      # Pokémon: kop iets groter dan echt (om het achterhoofd geschaald)


def potoo(lean=0, gape=None, kopdraai=30, kopkantel=18):
    """kopdraai: kop extra naar de kijker (SPRITE_NORM: kop draait meer dan het lijf); kopkantel: kop omhoog (3/4-foto)."""
    m = Model()
    Rl = rot_z(math.radians(lean))
    P = lambda p: Rl @ np.array(p, float)
    E = lambda c, r, g, R0=None: m.ell(P(c), r, g, Rl if R0 is None else Rl @ R0)
    # lijf: hoge zuil, rug hoog en gebogen (zijfoto), borst vooraan
    E((6, 0, 0), (37, 58, 30), "fur")
    E((26, 40, 0), (20, 20, 24), 'fur')                 # gebogen rug/schouders
    E((-20, 10, 6), (20, 38, 22), 'belly')
    E((-8, 52, 0), (22, 18, 22), 'fur')                 # overgang naar de kop, geen nek
    for sz in (1, -1):                                   # vleugels: lang paneel langs de zij
        E((26, -12, 26 * sz), (15, 58, 8), 'wing', rot_z(math.radians(-6)))
    for t in np.linspace(0, 1, 12):                      # staart: breed, hangt recht omlaag
        E((16 + 24 * t, -40 - 52 * t, 0), (10, 8, 18 + 16 * t), 'tail')   # schuin naar achteren (Noctowl/Swellow), anders leest hij als paal
    # kop
    n0 = len(m.parts)
    piv = np.array(LM['achterhoofd'] + (0,), float)
    H = lambda p: piv + (np.array(p, float) - piv) * KOP
    v = lambda k, z=0: np.array(LM[k] + (z,), float)
    E(H((-24, 72, 0)), np.array((30, 18, 24)) * KOP, 'fur')          # schedel; 3/4-foto: kop incl. kaak ±0,85 x zo hoog als breed
    # kaken als massieve wiggen met een paarse binnenbekleding (zo zit de kleur ín de snavel, niet als bol ervoor)
    def kaak(tip, r0, w0, op):
        for t in np.linspace(0, 1, 16):
            c = v('mondhoek') * (1 - t) + v(tip) * t + np.array((0, op * 3 * (1 - t), 0))
            r = r0 * (1 - t) + 2.2 * t
            w = w0 * (1 - t) + 4 * t
            E(H(c), np.array((r * 0.8, r * 0.6, w)) * KOP, 'fur')
            E(H(c + np.array((0, -op * r * 0.35, 0))), np.array((r * 0.72, r * 0.42, w * 0.86)) * KOP, 'mouth')
    kaak('snaveltip', 11, 21, +1)      # bovenkaak: bekleding aan de onderkant
    kaak('onderkaaktip', 8, 19, -1)    # onderkaak: bekleding aan de bovenkant
    E(H(v('snaveltip') + np.array((1, -2.5, 0))), np.array((2, 3.2, 2)) * KOP, 'beak')
    E(H(v('onderkaaktip') + np.array((-1, 0, 0))), np.array((1.8, 2, 2)) * KOP, 'beak')
    E(H(v('mondhoek') + np.array((-3, -4, 0))), np.array((6, 9, 13)) * KOP, 'throat')
    # ogen: hoog op de zijkant boven de mondhoek, groot (Pokémon) en pikzwart (Drifloon)
    for sz in (1, -1):
        E(H(v('oog', 17.5 * sz)), np.array((8, 6.5, 4)) * KOP, 'eye', rot_y(math.radians(-30 * sz)))
    Rh = rot_y(math.radians(kopdraai)) @ rot_z(math.radians(-kopkantel))
    pv = P(piv)
    m.parts[n0:] = [(pv + Rh @ (c - pv), r, Rh @ R0, g) for c, r, R0, g in m.parts[n0:]]
    return m


def sheet():
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
    yaws, leans = (30, 45, 60), (0, 10)
    im = Image.new('RGB', (10 + 266 * len(yaws), 40 + 290 * len(leans)), 'white')
    d = ImageDraw.Draw(im)
    d.text((10, 10), 'Great potoo: 3D-poppetje (gemeten aan de zijfoto)', font=FB, fill=(30, 30, 30))
    for r, lean in enumerate(leans):
        m = potoo(lean)
        for c, yaw in enumerate(yaws):
            v = view(m, yaw)
            im.paste(v, (10 + 266 * c, 40 + 290 * r))
            d.text((10 + 266 * c, 40 + 290 * r + 260), f'{chr(65 + r)}{c + 1}: lijf {yaw}°, voorover {lean}°', font=F, fill=(60, 60, 60))
    im.save(os.path.join(OUT, 'hoeken.png'))


if __name__ == '__main__':
    sheet()
