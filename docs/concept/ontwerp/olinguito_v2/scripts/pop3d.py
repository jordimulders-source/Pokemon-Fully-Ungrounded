"""Olinguito v2: 3D-poppetje (bollen/ellipsoïden) met kijkhoek, als basis voor de driekwartpose.
De houding staat in diercoördinaten (x = naar achteren, y = omhoog, z = naar de kijker bij 0°);
de camera draait (yaw) en kijkt iets van boven (pitch). Render: z-buffer, vlakke kleuren met één
schaduwtoon, omlijning waar de diepte verspringt (zoals de schetsen).
Draaien vanuit de repo-root: python3 docs/concept/ontwerp/olinguito_v2/scripts/pop3d.py"""
import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..')
R = 768          # renderresolutie (3x van 256)
HEAD_SCALE = 1.35
HEAD_SHIFT = np.array((-6, 30, 0.0))
LINE = np.array((43, 27, 23), np.uint8)

COL = {
    'fur': '#6A4630', 'head': '#6B5442', 'crown': '#6A4630', 'far': '#4C3121', 'paw': '#C08A80',
    'farpaw': '#9C6E66', 'claw': '#EDE3CC', 'mask': '#241712', 'eye': '#B9481C', 'pupil': '#1A0F0B',
    'glint': '#FFFFFF', 'nose': '#8E4F58', 'muzzle': '#2E211A', 'ear': '#4A3324', 'earin': '#8A6C55',
}
NOSHADE = {'muzzle', 'mask', 'eye', 'pupil', 'glint', 'nose', 'claw'}
LINED = {'eye', 'nose', 'claw'}   # ook een lijn op de kleurgrens


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


def olinguito():
    m = Model()
    # lijf: borst, buik (achter hoger), romp
    m.ell((-30, 0, 0), 26, 'fur')
    m.ell((2, 6, 0), (34, 24, 23), 'fur', rot_z(math.radians(8)))
    m.ell((34, 12, 0), 25, 'fur')
    # staart: lang, omhoog en in een boog terug over de rug
    tail = qb((52, 18, 0), (106, 26, 0), (100, 72, 0), 10)[:-1] + qb((100, 72, 0), (94, 110, 0), (64, 104, 0), 8)[:-1] \
        + qb((64, 104, 0), (40, 98, 0), (44, 80, 0), 6)
    n = len(tail)
    m.chain([(x, y, z, 10.5 - 5 * i / (n - 1)) for i, (x, y, z) in enumerate(tail)], 'fur')
    # kop: nek, ronde schedel, snuit naar voren-omlaag (vorm van referentie_kop.png), groter dan echt (Pokémon)
    hs, piv = HEAD_SCALE, np.array((-46, -2, 0.0))
    H = lambda p: piv + (np.array(p, float) - piv) * hs + HEAD_SHIFT
    m.chain([(-36, 0, 0, 22), tuple(piv + HEAD_SHIFT) + (20,)], 'fur')
    cr = H((-64, -6, 0))
    m.ell(cr, np.array((25, 28, 25)) * hs, 'head')   # hoog rond voorhoofd (foto)
    m.chain([tuple(H(q[:3])) + (q[3] * hs,) for q in [(-76, -16, 0, 20), (-88, -22, 0, 14.5), (-98, -28, 0, 9.5)]], 'head')
    nose = H((-105, -31, 0))
    m.ell(nose, 6.0 * hs, 'nose')
    eyes = []
    for sz in (1, -1):
        d = np.array((-0.70, -0.28, 0.66 * sz)); d /= np.linalg.norm(d)   # oog laag, dicht bij de snuit
        e = cr + d * 23.5 * hs
        eyes.append(e)
        m.ell(e, 4.4 * hs, 'eye')
        m.ell(e + d * 2.0 * hs + np.array((-0.5, -0.3, 0)) * hs, 2.7 * hs, 'pupil')
        m.ell(e + d * 3.0 * hs + np.array((-0.8, 1.5, 0.0)) * hs, 1.0 * hs, 'glint')
    arc = []
    for t in np.linspace(-1.3, 1.3, 53):
        d = np.array((-0.72, -0.10, 0.69 * t)); d /= np.linalg.norm(d)
        arc.append(cr + d * 26.5 * hs)
    m.tex = dict(cr=cr, eyes=eyes, arc=np.array(arc), nose=nose, hs=hs)
    # oren bovenop, naar voren gericht
    for sz in (1, -1):
        Re = rot_y(math.radians(25 if sz > 0 else 0))
        c = H((-58, 16, 13 * sz))
        k = 1.0 if sz > 0 else 0.6    # verre oor kleiner: nauwelijks zichtbaar
        m.ell(c, np.array((4, 12, 11)) * hs * k, 'ear', Re)
        m.ell(c + Re @ np.array((-1.8, 0.5, 0)) * hs * k, np.array((2.6, 8, 7.5)) * hs * k, 'earin', Re)
    # poten (x, y, z, straal); nabij = +z
    m.chain([(-34, -2, 13, 16), (-48, -28, 15, 11.5), (-62, -52, 17, 9)], 'fur')   # nabije voorpoot: gestrekt
    m.ell((-66, -55, 18), (10, 6, 8), 'paw')
    for dz in (-3.5, 3.5):   # 2 lange Linoone-klauwen
        m.chain([(-72, -57, 18 + dz, 3.6), (-80, -66, 18 + dz, 2.6), (-82, -78, 18 + dz, 0.8)], 'claw', 0.8)
    m.chain([(-28, -2, -13, 14), (-20, -28, -15, 11), (-34, -42, -17, 8.5)], 'far')  # verre voorpoot: opgetild
    m.ell((-38, -45, -17), (9, 6, 7.5), 'farpaw')
    for dz in (-3.5, 3.5):
        m.chain([(-44, -48, -17 + dz, 3.2), (-50, -57, -17 + dz, 2.2), (-51, -66, -17 + dz, 0.7)], 'claw', 0.8)
    # achterpoten gehurkt: grote dij, knie naar voren, hak laag, voet plat naar voren
    m.chain([(30, 10, 18, 20), (6, -20, 21, 13), (30, -42, 21, 9)], 'fur')
    m.chain([(30, -42, 21, 7.5), (10, -48, 22, 6.5)], 'paw')
    m.chain([(36, 12, -17, 18), (18, -16, -19, 11.5), (40, -36, -19, 8.5)], 'far')
    m.chain([(40, -36, -19, 7), (24, -42, -20, 6)], 'farpaw')
    return m


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
    # textuur: wereldpunt terug naar diercoördinaten, tekeningen op de kop
    head = gid == groups.index('head')
    q = wpt[head] @ Rc          # = Rc^T p
    t = m.tex
    hs = t['hs']
    de = np.min([np.linalg.norm(q - e, axis=1) for e in t['eyes']], axis=0)
    da = np.min(np.linalg.norm(q[:, None, :] - t['arc'][None], axis=2), axis=1)
    dn = np.linalg.norm(q - t['nose'], axis=1)
    u = (q - t['cr']) / (25 * hs)
    g = np.full(len(q), groups.index('head'))
    g[u @ np.array((0.75, 0.66, 0)) > 0.72] = groups.index('crown')
    g[dn < 9 * hs] = groups.index("muzzle")
    band = (np.abs(u[:, 1] + 0.24) < 0.19) & (u[:, 0] < -0.50)      # brede band over beide ogen (Zigzagoon)
    g[(de < 9.5 * hs) | band] = groups.index('mask')
    gid[head] = g
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


def sheet(yaws=(52,)):
    m = olinguito()
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
    refs = [os.path.join(OUT, f) for f in ('referentie_driekwart_11.png', 'referentie_driekwart_9.png')]
    W = 10 + 266 * len(yaws)
    im = Image.new('RGB', (W, 34 + 256 + 26 + 200), 'white')
    d = ImageDraw.Draw(im)
    d.text((10, 8), 'Olinguito v2: 3D-poppetje, 52°', font=FB, fill=(30, 30, 30))
    for i, yaw in enumerate(yaws):
        v = view(m, yaw)
        v.save(os.path.join(OUT, f'pop3d_{yaw}.png'))
        im.paste(v, (10 + 266 * i, 34))
        d.text((10 + 266 * i, 34 + 258), f'{yaw}° gedraaid' if yaw else '0° (van opzij)', font=F, fill=(60, 60, 60))
    x = 10
    for r in refs:
        ref = Image.open(r).convert('RGB')
        ref.thumbnail((360, 190))
        im.paste(ref, (x, 34 + 280))
        x += ref.size[0] + 20
    im.save(os.path.join(OUT, 'pop3d_hoeken.png'))


if __name__ == '__main__':
    sheet()
