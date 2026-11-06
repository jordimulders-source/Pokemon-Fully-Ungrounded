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


def plate(m, p0, p1, w, t, g):
    """Platte vleugel tussen twee punten (breedte w, dikte t)."""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0; L = np.linalg.norm(d); d /= L
    up = np.array((0, 0, 1.0)) if abs(d[2]) < 0.8 else np.array((0, 1.0, 0))
    n = np.cross(d, up); n /= np.linalg.norm(n); u = np.cross(n, d)
    m.ell((p0 + p1) / 2, (L / 2 + w * 0.3, w, t), g, np.stack([d, u, n], 1))


def wing(m, sh, wr, dirs, lens, g, z, cw=13, pw=5.5):
    """Vleugel: dekveren (schouder -> pols) en een waaier van slagpennen vanaf de pols (richtingen in x-y)."""
    plate(m, sh, wr, cw, 5, g)
    wr = np.array(wr, float)
    for (dx, dy), L in zip(dirs, lens):
        d = np.array((dx, dy, 0.0)); d /= np.linalg.norm(d)
        tip = wr + d * L; tip[2] = z
        plate(m, wr, tip, pw, 2.2, g)


def tube(m, pts, r0, r1, g, n=8):
    """Gladde buis door punten (Catmull-Rom), straal r0 -> r1."""
    C = [np.array(p, float) for p in pts]
    out = []
    for i in range(len(C) - 1):
        p0, p1, p2, p3 = C[max(i - 1, 0)], C[i], C[i + 1], C[min(i + 2, len(C) - 1)]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(C[-1])
    m.chain([tuple(q) + (r0 + (r1 - r0) * k / (len(out) - 1),) for k, q in enumerate(out)], g, 1.0)


def bird(extra=32, fan_L=58, fan_n=17, tilt=14, curl=0.5, wing_out=0.0, tail_out=0.0, staff=True, staff_top='zon'):
    """Hybride: bouw van de bergcaracara (groot, rechtop, lange poten, haaksnavel, kaal rood gezicht),
    kroon en staart van de koningstiran. De zijveren van de waaier hangen omlaag (foto 2) en vormen zo
    zelf de franje van de mascaypacha; geen losse band (geen 'dier met een hoed')."""
    m = Model()
    # pose naar Empoleon (Jordi, 5 nov): borst vooruit, iets achterover, verre vleugel naar voren uitgestoken,
    # nabije vleugel als mantel naar achteren-omlaag, poten breed; swagger, geen T-pose
    # pose naar het Pachacútec-beeld in Cuzco (Jordi, 5 nov; referenties/pachacutec_beeld_cuzco.webp):
    # nabije vleugel half de lucht in (opgeheven arm, rechts in beeld), verre vleugel gesloten en hangend
    # (Decidueye), contrapposto: gewicht op de nabije poot, verre poot naar voren op een verhoging. Slanker lijf.
    A = rot_x(math.radians(-5)) @ rot_z(math.radians(99))
    m.ell((6, 4, 0), (42, 23, 22), 'body', A)
    m.ell((-9, 8, 0), (19, 30, 20), 'breast', rot_z(math.radians(-6)))
    cy, sy = math.cos(math.radians(44)), math.sin(math.radians(44))
    W2 = lambda xp, y, zp: np.array((cy * xp - sy * zp, y, sy * xp + cy * zp))   # schermruimte -> dier (lijf 44°)
    if staff:
        # Jordi 7 nov: linkervleugel iets hoger, met een staf erin (Pachacútec houdt zijn staf op heuphoogte vast).
        # Onderarm naar voren tot de staf, de slagpennen gesloten omlaag langs de staf.
        # arm zichtbaar (Jordi: "de arm is weg"): schouder -> elleboog links naast het lijf -> hand om de staf
        elb, wr = W2(-36, 16, -2), W2(-35, 3, 13)
        plate(m, (-2, 28, -15), elb, 15, 5, 'farwing')
        plate(m, elb, wr, 13, 5, 'farwing')
        plate(m, W2(-41, 4, 15), W2(-31, 1, 16), 8, 3, 'farwing')          # vleugelpunt vouwt vóór de staf
        for k, (xp, y) in enumerate(((-30, -6), (-27, -5), (-24, -4))):      # korte gesloten pennen naar het lijf
            plate(m, wr, W2(xp, y, 10 - k), 9, 2.2, 'farwing')
        # staf: goud, rechtop, van de grond tot kophoogte, bovenaan drie veren zoals op het beeld
        # Jordi 7 nov (krabbel_jordi_staart_is_staf.png): de staart IS de staf. Onder de hand buigt de staf licht
        # naar het lijf en verdwijnt erachter; hij gaat nergens over bestaande lichaamsdelen heen (diepte achter).
        SP = [(-22, -20, -30), (-29, -12, -12), (-34, -5, 2), (-37, 3, 8), (-37, 20, 8), (-37, 44, 8)]  # staf wordt hoger staart
        tube(m, [W2(*q) for q in SP], 3.2, 3.0, 'gold')
        top = W2(-37, 44, 8)
        if staff_top == 'veren':     # drie veren zoals op het beeld
            for a in (-24, 0, 24):
                r = math.radians(a)
                d = W2(math.sin(r), math.cos(r), 0) ; d = d / np.linalg.norm(d)
                plate(m, top, top + d * 16, 4.5, 1.8, 'fan')
                m.ell(top + d * 16.5, (2.6, 3.2, 2.0), 'fanrim')
        else:                        # gouden zonneschijf (Inti), leest anders dan de kwastjes van de kroon
            ctr = top + np.array((0, 9, 0.0))
            Rs = rot_y(math.radians(-44 - 30))
            m.ell(ctr, (9, 9, 2.2), 'gold', Rs)
            for k in range(8):
                a = k * math.pi / 4
                m.ell(ctr + Rs @ np.array((math.cos(a) * 11, math.sin(a) * 11, 0)), (2.4, 2.4, 1.6), 'gold')
        # lijf linksonder: flank loopt rond door naar de dij (lijf hield daar 'opeens op', Jordi)
        m.ell(W2(-12, -28, 0), (13, 11, 13), 'body')
    else:
        # verre vleugel: gesloten, hangt langs de voorkant omlaag (Decidueye-cape)
        wing(m, (-2, 28, -15), (-14, 4, -28), [(-0.22, -1.0), (-0.16, -1.0), (-0.10, -1.0), (-0.04, -1.0)],
             (40, 37, 33, 28), 'farwing', -26, 15, 10)   # bovenarm even dik als rechts (Jordi)
    # nabije vleugel: gesloten blad met een knik in de pols: de arm gaat naar buiten, de slagpennen buigen omhoog,
    # elke pen iets verder gedraaid zodat de achterrand een bolle curve wordt (geen rechte lijn, geen vingers)
    c = curl
    dirs = [(0.62 - 0.30 * c + 0.10 * k * c + wing_out, 1.0 - 0.05 * k) for k in range(5)]
    wing(m, (8, 30, 17), (21, 35, 34), dirs, (33, 36, 34, 30, 24), 'wing', 56, 16, 12)  # iets korter (Jordi)
    # staart = staf (Jordi 7 nov): de echte staart is weg; alleen rechtsonder een klein stukje waar hij uit het lijf
    # komt en heel licht afbuigt, in het goud van de staf, achter het standbeen (nergens eroverheen).
    if staff:
        tube(m, [W2(*q) for q in ((14, -24, -16), (20, -32, -10), (18, -41, -10), (10, -45, -14), (2, -44, -20))], 3.4, 3.0, 'gold')  # uit de stuit, omlaag, dan naar links achter het standbeen
    else:
        for ang in (-62 - tail_out, -48 - tail_out, -34 - tail_out):
            Rt = rot_z(math.radians(ang)) @ rot_x(math.radians(-6))
            m.ell(np.array((34, -22, -2)) + Rt @ np.array((0, -20, 0)), (9, 24, 3), 'tail', Rt)
    # poten: geen V meer. Standbeen recht onder het zwaartepunt; vrije poot met gebogen knie naar voren,
    # het scheenbeen weer verticaal (contrapposto van het beeld)
    # beide benen even lang (dij ±10, scheen ±11) en onder het lijf, zoals het beeld; het vrije been staat
    # alleen iets naar voren met een lichte knik en de voet iets hoger (op de rots), niet schuin opzij
    legs3 = (((2, -30, 6), (3, -40, 7), (3, -51, 8)),           # standbeen
             ((-3, -30, -6), (-9, -39, -7), (-9, -49, -8)))     # vrije poot
    for hip, knee, foot in legs3:
        m.chain([hip + (5.0,), knee + (4.0,)], 'breast')
        m.chain([knee + (3.0,), foot + (2.7,)], 'leg')
        fx, fy, z = foot
        for dz, dx in ((-3, -8), (0, -9), (3, -7)):
            m.chain([(fx, fy, z, 2.3), (fx + dx, fy - 3, z + dz, 1.9)], 'leg')
            m.ell((fx + dx - 1.5, fy - 4, z + dz), 1.4, 'claw')
        m.chain([(fx, fy, z, 2.1), (fx + 5, fy - 3, z, 1.7)], 'leg')
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


def sheet(curls=(0.5,)):
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
    cw = 266 + 70
    W = Image.new('RGB', (max(12 + cw * len(curls), 760), 36 + 256 + 26), (236, 232, 222))
    d = ImageDraw.Draw(W)
    d.text((10, 10), 'Sapa Inca B3 (silhouet 1x)',
           font=FB, fill=(30, 30, 30))
    for j, c in enumerate(curls):
        im, sil = view(bird(extra=32, curl=c), 44)
        x, y = 10 + j * cw, 36
        W.paste(im, (x, y))
        W.paste(Image.new('RGB', (64, 64), (20, 20, 24)), (x + 262, y + 180), sil)
        d.text((x + 4, y + 258), f'{j + 1}: buiging {c}', font=F, fill=(50, 50, 50))
    W.save(os.path.join(HERE, 'pop3d_hoeken.png'))


if __name__ == '__main__':
    sheet()
