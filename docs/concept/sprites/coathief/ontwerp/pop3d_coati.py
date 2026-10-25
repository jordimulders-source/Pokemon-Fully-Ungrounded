"""Coathief (coati, fase 2): 3D-poppetje voor de pose, op basis van olinguito_v2/silhouet_kolibriemethode/pop3d.py.
Diercoördinaten: x = naar achteren, y = omhoog, z = naar de kijker bij 0°. Pose (Jordi, 25 okt): driekwart naar je
toe lopen alsof hij de confrontatie aangaat, één poot opgetild; lang lijf, lange snuit, geringde (krullende) staart,
bivakmuts-kop (zwart op een kring rond de ogen na), 2 lange klauwen.
Draaien: python3 docs/concept/sprites/coathief/ontwerp/pop3d_coati.py"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../olinguito_v2/silhouet_kolibriemethode'))
import pop3d as P

R = 768
LINE = np.array((30, 20, 18), np.uint8)
COL = {
    'fur': '#93602F', 'far': '#69431F', 'leg': '#3A2A22', 'farleg': '#2A1E19', 'paw': '#C08A80', 'farpaw': '#9C6E66',
    'claw': '#EDE3CC', 'head': '#2B2422', 'ring': '#C9B08C', 'muzzle': '#2B2422', 'nose': '#141010',
    'eye': '#B9481C', 'pupil': '#1A0F0B', 'ear': '#2B2422', 'earin': '#C9B08C', 'tl': '#C9A57A', 'td': '#3E2A1E',
    'chin': '#C9B08C', 'spot': '#D8C3A0',
}
NOSHADE = {'eye', 'pupil', 'nose', 'claw'}
LINED = {'eye', 'nose', 'claw', 'ring'}


def coati(head_extra=15, tilt=0, leg_k=1.3, claw_k=1.8):
    m = P.Model()
    L = lambda pts: [(x, y, z, r * leg_k) for x, y, z, r in pts]
    # lang lijf: borst, buik, hoge heup (foto 2: rug stijgt naar achteren)
    m.ell((-38, 0, 0), 25, 'fur')
    m.ell((2, 5, 0), (42, 24, 22), 'fur', P.rot_z(math.radians(6)))
    m.ell((42, 9, 0), 24, 'fur')
    # staart: omhoog als vlag, top krult terug; ringen licht/donker (patroon is heilig)
    tail = P.qb((60, 14, 0), (98, 26, 0), (98, 78, 0), 12)[:-1] + P.qb((98, 78, 0), (98, 114, 0), (72, 114, 0), 8)[:-1] \
        + P.qb((72, 114, 0), (56, 112, 0), (60, 96, 0), 5)
    acc = [0.0]
    for a, b in zip(tail, tail[1:]):
        acc.append(acc[-1] + np.linalg.norm(np.subtract(b, a)))
    n = len(tail)
    pts = [(x, y, z, 12.5 - 6 * i / (n - 1)) for i, (x, y, z) in enumerate(tail)]
    for (a, b, sa, sb) in zip(pts, pts[1:], acc, acc[1:]):
        a, b = np.array(a), np.array(b)
        k = max(2, int(np.linalg.norm(b[:3] - a[:3]) / 1.2))
        for i in range(k):
            t = i / k
            p = a + (b - a) * t
            s = sa + (sb - sa) * t
            m.ell(p[:3], p[3], 'td' if (s // 13) % 2 else 'tl')
    m.ell(pts[-1][:3], pts[-1][3], 'td')
    # nek + kop (laag, naar voren), lange snuit
    hs, piv = 1.25, np.array((-52, -2, 0.0))
    m.chain([(-44, 0, 0, 21), (-58, -4, 0, 18)], 'fur')
    h0 = len(m.parts)
    cr = np.array((-74, 0, 0.0))
    m.ell(cr, np.array((20, 19, 19)) * hs, 'head')
    snout = [(-90, -8, 0, 14), (-104, -13, 0, 10), (-118, -17, 0, 7), (-128, -19, 0, 5.5)]
    m.chain([(x, y, z, r * hs) for x, y, z, r in snout], 'muzzle')
    nose = np.array((-132, -20, 0.0))
    m.ell(nose, 5.5 * hs, 'nose')
    eyes = []
    for sz in (1,):   # lange snuit: één oog in beeld
        d = np.array((-0.62, -0.05, 0.78 * sz)); d /= np.linalg.norm(d)
        e = cr + d * 18.7 * hs
        eyes.append(e)
        m.ell(e, 2.7 * hs, 'eye')
        m.ell(e + d * 1.4 * hs, 1.3 * hs, 'pupil')
    for sz in (1, -1):
        c = cr + np.array((4, 20, 11 * sz))
        k = 1.0 if sz > 0 else 0.7
        Re = P.rot_y(math.radians(20 * sz))
        m.ell(c, np.array((4, 9.5, 9.5)) * hs * k, 'ear', Re)
        m.ell(c + Re @ np.array((-1.6, 0, 0)) * hs * k, np.array((2.4, 7, 7)) * hs * k, 'earin', Re)
    tex = dict(eyes=eyes, cr=cr, nose=nose, hs=hs)
    if head_extra:
        Rh = P.rot_y(math.radians(head_extra))
        rot = lambda p: piv + Rh @ (np.array(p) - piv)
        m.parts[h0:] = [(rot(c), r, Rh @ R0, g) for c, r, R0, g in m.parts[h0:]]
        tex = dict(eyes=[rot(e) for e in eyes], cr=rot(cr), nose=rot(nose), hs=hs)
    m.tex = tex
    # poten (langer dan de olinguito, foto 2); diagonale gang: nabije voor + verre achter zwaaien,
    # verre voor + nabije achter dragen. Grond op y = -64.
    # nabije voorpoot opgetild, gebogen naar de kijker, klauwen hangen dreigend omlaag
    m.chain(L([(-40, -2, 14, 14), (-50, -28, 18, 10)]), 'fur')
    m.chain(L([(-50, -28, 18, 8.5), (-66, -34, 22, 7.5)]), 'leg')
    m.ell((-71, -36, 23), np.array((7, 5.5, 7)) * leg_k ** 0.5, 'leg')
    for dz in (-4.5, 4.5):
        m.chain([(-77, -38, 23 + dz, 3.2 * claw_k), (-86, -42, 23 + dz, 2.3 * claw_k), (-91, -50, 23 + dz, 0.9 * claw_k)], 'claw', 0.8)
    # verre voorpoot: staat, iets naar voren
    m.chain(L([(-32, -2, -13, 13), (-40, -30, -15, 9.5)]), 'far')
    m.chain(L([(-40, -30, -15, 8), (-46, -60, -16, 7)]), 'farleg')
    m.ell((-50, -63, -16), np.array((8, 5, 7)) * leg_k ** 0.5, 'farleg')
    for dz in (-4, 4):
        m.chain([(-56, -64, -16 + dz, 2.9 * claw_k), (-65, -66, -16 + dz, 2.0 * claw_k), (-72, -69, -16 + dz, 0.8 * claw_k)], 'claw', 0.8)
    # nabije achterpoot: draagt, naar achteren afgezet
    m.chain(L([(42, 6, 18, 19), (34, -24, 20, 11.5)]), 'fur')
    m.chain(L([(34, -24, 20, 9), (54, -46, 21, 7.5), (50, -61, 21, 6.5)]), 'leg')
    m.ell((44, -63, 21), np.array((8, 4.5, 7)), 'leg')
    # verre achterpoot: zwaait naar voren
    m.chain(L([(46, 8, -16, 17), (30, -22, -18, 10.5)]), 'far')
    m.chain(L([(30, -22, -18, 8), (40, -42, -19, 7), (30, -54, -19, 6)]), 'farleg')
    m.ell((25, -56, -19), np.array((7, 4, 6)), 'farleg')
    if tilt:
        Rt = P.rot_z(math.radians(-tilt))
        m.parts = [(Rt @ c, r, Rt @ R0, g) for c, r, R0, g in m.parts]
        t = m.tex
        m.tex = dict(eyes=[Rt @ e for e in t['eyes']], cr=Rt @ t['cr'], nose=Rt @ t['nose'], hs=t['hs'])
    return m


def render(m, yaw, pitch, scale, center):
    Rc = P.rot_x(math.radians(pitch)) @ P.rot_y(math.radians(yaw))
    zbuf = np.full((R, R), -1e9, np.float32)
    gid = np.full((R, R), -1, np.int16)
    nrm = np.zeros((R, R, 3), np.float32)
    wpt = np.zeros((R, R, 3), np.float32)
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
        q = np.stack([wx[y0:y1, x0:x1], wy[y0:y1, x0:x1], z], -1)
        wpt[y0:y1, x0:x1][win] = q[win]
    # bivakmuts: zwarte kop met een lichte kring rond elk oog; lichte kin
    t = m.tex
    var, hs, e = getattr(m, 'var', 'A'), t['hs'], t['eyes'][0]
    for grp in ('head', 'muzzle'):
        sel = gid == groups.index(grp)
        q = wpt[sel] @ Rc
        de = np.linalg.norm(q - e, axis=1)
        g = gid[sel].copy()
        if var == 'A':      # bivakmuts met kring
            g[de < 5.2 * hs] = groups.index('ring')
        else:               # vlekken boven en onder het oog (foto 6-8)
            up = np.linalg.norm(q - (e + np.array((1.5, 5.2, 0)) * hs), axis=1) < 4.0 * hs
            dn = np.linalg.norm(q - (e + np.array((3.5, -5.0, 0)) * hs), axis=1) < 4.4 * hs
            if var == 'B':  # natuurlijk: bruine kop, donkere band door het oog naar de snuit
                g[de < 4.4 * hs] = groups.index('muzzle')
                band = (np.abs(q[:, 1] - e[1]) < 3.4 * hs) & (q[:, 0] < e[0] + 3 * hs)
                g[band & (g == groups.index('head'))] = groups.index('muzzle')
            g[(up | dn) & (de > 3.2 * hs)] = groups.index('spot')
        gid[sel] = g
    return zbuf, gid, nrm, groups


def shade(zbuf, gid, nrm, groups, out=256):
    a = gid >= 0
    rgb = np.ones((R, R, 3), np.float32) * 255
    Lt = np.array((-0.45, 0.65, 0.62)); Lt /= np.linalg.norm(Lt)
    lit = (nrm @ Lt) > -0.2
    for i, g in enumerate(groups):
        mm = gid == i
        col = P.hexc(COL[g])
        rgb[mm] = col
        if g not in NOSHADE:
            rgb[mm & ~lit] = col * 0.78
    edge = np.zeros((R, R), bool)
    z = np.where(a, zbuf, -1e9)
    lined = np.isin(gid, [groups.index(g) for g in LINED])
    for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):
        z2 = np.roll(np.roll(z, -dy, 0), -dx, 1)
        g2 = np.roll(np.roll(gid, -dy, 0), -dx, 1)
        l2 = np.roll(np.roll(lined, -dy, 0), -dx, 1)
        e = (np.abs(z - z2) > 5) | ((gid != g2) & (lined | l2))
        edge |= e
        edge |= np.roll(np.roll(e, dy, 0), dx, 1)
    for _ in range(3):
        edge = edge | np.roll(edge, 1, 0) | np.roll(edge, 1, 1)
    inner = a.copy()
    for _ in range(9):
        inner = inner & np.roll(inner, 1, 0) & np.roll(inner, -1, 0) & np.roll(inner, 1, 1) & np.roll(inner, -1, 1)
    edge = (edge & a) | (a & ~inner)
    rgb[edge] = LINE
    rgb[~a] = 255
    return Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).resize((out, out), Image.LANCZOS)


def view(m, yaw, pitch=10, size=232):
    Rc = P.rot_x(math.radians(pitch)) @ P.rot_y(math.radians(yaw))
    pts = np.array([Rc @ c for c, r, R0, g in m.parts]); rs = np.array([r.max() for c, r, R0, g in m.parts])
    x0, x1, y0, y1 = (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()
    scale = R * (size / 256) / max(x1 - x0, y1 - y0)
    return shade(*render(m, yaw, pitch, scale, ((x0 + x1) / 2, (y0 + y1) / 2)))


def raster():
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
    yaws, heads = (30, 42, 54), (10, 22)
    W, cell = 12 + 262 * len(yaws), 262
    im = Image.new('RGB', (W, 40 + (cell + 22) * len(heads)), 'white')
    d = ImageDraw.Draw(im)
    d.text((12, 10), 'Coathief: 3D-poppetje, kies een hoek (lijf / kop extra)', font=FB, fill=(30, 30, 30))
    for j, he in enumerate(heads):
        for i, yw in enumerate(yaws):
            v = view(coati(head_extra=he), yw)
            x, y = 12 + cell * i, 40 + (cell + 22) * j
            im.paste(v, (x, y))
            lab = f'{"ABC"[i]}{j + 1}: lijf {yw}°, kop {yw + he}°'
            d.text((x + 4, y + 258), lab, font=F, fill=(60, 60, 60))
    im.save(os.path.join(HERE, 'hoeken.png'))


def abc():
    """A/B/C-test op B1 (Jordi, 25 okt): A bivakmuts met kring, B natuurlijke kop, C bivakmuts met vlekken."""
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
    labs = {'A': 'A: bivakmuts, kring', 'B': 'B: natuurlijke kop, vlekken', 'C': 'C: bivakmuts, vlekken'}
    base = dict(COL)
    im = Image.new('RGB', (12 + 262 * 3, 40 + 262 + 26 + 230), 'white')
    d = ImageDraw.Draw(im)
    d.text((12, 10), 'Coathief: kop A/B/C (hoek B1: lijf 42°, kop 52°)', font=FB, fill=(30, 30, 30))
    for i, v in enumerate('ABC'):
        COL.clear(); COL.update(base)
        if v == 'B':
            COL.update(head='#93602F', ear='#93602F')
        m = coati(head_extra=10); m.var = v
        img = view(m, 42)
        im.paste(img, (12 + 262 * i, 40))
        d.text((16 + 262 * i, 40 + 258), labs[v], font=F, fill=(60, 60, 60))
        im.paste(img.crop((20, 105, 130, 215)).resize((220, 220), Image.LANCZOS), (12 + 262 * i + 20, 40 + 262 + 26))
    COL.clear(); COL.update(base)
    im.save(os.path.join(HERE, 'kop_abc.png'))


if __name__ == '__main__':
    raster()
    abc()
