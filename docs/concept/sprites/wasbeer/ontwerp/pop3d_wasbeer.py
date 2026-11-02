"""Dark-starter fase 3 (krabbenetende wasbeer): 3D-poppetje voor de pose, op basis van
coathief/ontwerp/pop3d_coati.py en olinguito_v2/silhouet_kolibriemethode/pop3d.py.
Diercoördinaten: x = naar achteren, y = omhoog, z = naar de kijker bij 0°.
Pose (Jordi, 2 nov): op 2 poten staand, voorover hangend (niet rechtop); lange poten (foto 7);
haakstaart; masker met Andes-trapjes; klauwen: de 2 klauwen per hand vormen samen één koevoet.
Draaien: python3 docs/concept/sprites/wasbeer/ontwerp/pop3d_wasbeer.py"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../olinguito_v2/silhouet_kolibriemethode'))
import pop3d as P

R = 768
LINE = np.array((26, 22, 22), np.uint8)
COL = {
    'fur': '#7A7068', 'far': '#585049', 'chest': '#B59A6A', 'leg': '#2E2826', 'farleg': '#201C1B',
    'claw': '#EDE3CC', 'farclaw': '#BDB29A', 'head': '#857A70', 'muzzle': '#D9D0C2', 'mask': '#1E1A1A',
    'brow': '#E6DFD2', 'nose': '#4A3436', 'eye': '#7A3A22', 'pupil': '#0E0909', 'ear': '#6C625A',
    'earin': '#D9D0C2', 'tl': '#9A8E7E', 'td': '#3A332F', 'rock': '#8C8C84',
}
NOSHADE = {'eye', 'pupil', 'nose', 'claw', 'farclaw', 'mask'}
LINED = {'eye', 'nose', 'claw', 'farclaw', 'mask'}


def koevoet(m, top, down, fwd, side, k, g):
    """Twee klauwen tegen elkaar = één koevoet: rechte steel omlaag, dan een J-bocht naar voren
    en omhoog; alleen de punt is gespleten (de 'klauw' van een echte koevoet)."""
    top = np.array(top, float)
    for dz in (-side, side):
        o = top + np.array((0, 0, dz))
        bend = o + np.array((-1, -down, 0))
        path = [o, bend] + P.qb(bend, bend + np.array((-fwd * 0.2, -fwd * 0.55, 0)), bend + np.array((-fwd, -fwd * 0.25, 0)), 6)[1:]
        rs = np.linspace(1.9, 0.8, len(path)) * k
        m.chain([(p[0], p[1], p[2], r) for p, r in zip(path, rs)], g, 0.7)


def wasbeer(lean=45, head_up=0, leg_k=1.15, claw_k=1.5, arm_fwd=0):
    m = P.Model()
    L = lambda pts: [(x, y, z, r * leg_k) for x, y, z, r in pts]
    # romp: heup laag-achter, borst hoog-voor; 'lean' = hoek van de romp met de horizontaal
    a = math.radians(lean)
    hip = np.array((30.0, 4, 0)); ax = np.array((-math.cos(a), math.sin(a), 0))
    chest = hip + ax * 60
    for t, r, g in ((0, 25, 'fur'), (0.35, 23, 'fur'), (0.7, 22, 'fur'), (1.0, 21, 'fur')):
        m.ell(hip + ax * 60 * t, r, g)
    m.ell(chest + np.array((-9, -6, 0)), (12, 17, 16), 'chest')
    # staart: hangt achter de heup omlaag en eindigt in een haak (haakstaart, ringen)
    tail = P.qb((50, -10, 0), (78, -26, 0), (80, -58, 0), 10)[:-1] + P.qb((80, -58, 0), (82, -82, 0), (66, -84, 0), 7)[:-1] \
        + P.qb((66, -84, 0), (54, -82, 0), (58, -70, 0), 5)
    acc = [0.0]
    for p1, p2 in zip(tail, tail[1:]):
        acc.append(acc[-1] + np.linalg.norm(np.subtract(p2, p1)))
    n = len(tail)
    pts = [(x, y, z, 12 - 5.5 * i / (n - 1)) for i, (x, y, z) in enumerate(tail)]
    for (p1, p2, sa, sb) in zip(pts, pts[1:], acc, acc[1:]):
        p1, p2 = np.array(p1), np.array(p2)
        kk = max(2, int(np.linalg.norm(p2[:3] - p1[:3]) / 1.2))
        for i in range(kk):
            t = i / kk
            p = p1 + (p2 - p1) * t
            s = sa + (sb - sa) * t
            m.ell(p[:3], p[3], 'td' if (s // 12) % 2 else 'tl')
    m.ell(pts[-1][:3], pts[-1][3], 'td')
    # achterpoten: staan op de rand (grond y = -64), lang (foto 7)
    m.chain(L([(32, 6, 14, 17), (40, -24, 16, 11)]), 'fur')
    m.chain(L([(40, -24, 16, 8), (34, -44, 16, 6.5), (32, -52, 16, 6)]), 'leg')
    m.ell((25, -54, 16), np.array((9, 4.5, 7)), 'leg')
    m.chain(L([(32, 6, -14, 16), (42, -24, -16, 10)]), 'far')
    m.chain(L([(42, -24, -16, 7.5), (36, -44, -16, 6), (34, -52, -16, 5.5)]), 'farleg')
    m.ell((27, -54, -16), np.array((8.5, 4.5, 6.5)), 'farleg')
    # rand (rots/dakrand) onder de achtervoeten; de voorkant steekt net voor de tenen uit,
    # het voorlijf hangt over de rand heen
    if getattr(P, 'ROCK', True):
        for rx in range(16, 64, 6):
            m.ell((rx, -63, 0), (9, 6, 30), 'rock')
    # voorpoten: hangen voorover omlaag vanaf de schouders, lang en dun (foto 7)
    sh = chest + np.array((-4, 2, 0))
    for sz, g, gl, gc in ((1, 'fur', 'leg', 'claw'), (-1, 'far', 'farleg', 'farclaw')):
        s = sh + np.array((0, 0, 13 * sz))
        fx = -arm_fwd if sz > 0 else 4
        elbow = s + np.array((-6 + fx * 0.5, -20, 2 * sz))
        wrist = elbow + np.array((-1 + fx, -20, 0))
        m.chain(L([(*s, 12), (*elbow, 8)]), g)
        m.chain(L([(*elbow, 7), (*wrist, 6)]), gl)
        m.ell(wrist + np.array((-1, -3, 0)), np.array((6, 5, 6.5)) * leg_k, gl)
        koevoet(m, wrist + np.array((-1, -5, 0)), 15, 13, 1.7, claw_k, gc)
    # nek + kop: kop voor de borst, kijkt naar de speler
    hs = 1.15
    neck = chest + np.array((-10, 8, 0))
    m.chain([(*chest, 19), (*neck, 16)], 'fur')
    cr = neck + np.array((-14, 6, 0))
    h0 = len(m.parts)
    m.ell(cr, np.array((19, 17, 18)) * hs, 'head')
    m.ell(cr + np.array((2, -9, 0)) * hs, np.array((15, 9, 15)) * hs, 'head')   # wangen
    snout = [(-14, -5, 0, 10), (-22, -8, 0, 7.5), (-29, -10, 0, 5.5)]
    m.chain([(cr[0] + x * hs, cr[1] + y * hs, z, r * hs) for x, y, z, r in snout], 'muzzle')
    nose = cr + np.array((-32, -11, 0)) * hs
    m.ell(nose, 4.6 * hs, 'nose')
    eyes = []
    for sz in (1, -1):
        d = np.array((-0.66, 0.12, 0.74 * sz)); d /= np.linalg.norm(d)
        e = cr + d * 17.6 * hs
        eyes.append(e)
        m.ell(e, 2.9 * hs, 'eye')
        m.ell(e + d * 1.2 * hs, 1.5 * hs, 'pupil')
    for sz in (1, -1):
        c = cr + np.array((6, 17, 11 * sz)) * hs
        Re = P.rot_y(math.radians(25 * sz))
        m.ell(c, np.array((3.5, 8, 7)) * hs, 'ear', Re)
        m.ell(c + Re @ np.array((-1.5, -0.5, 0)) * hs, np.array((2, 5.5, 4.8)) * hs, 'earin', Re)
    Rh = np.eye(3)
    if head_up:
        Rh = P.rot_z(math.radians(-head_up))
        piv = neck
        rot = lambda p: piv + Rh @ (np.array(p) - piv)
        m.parts[h0:] = [(rot(c), r, Rh @ R0, g) for c, r, R0, g in m.parts[h0:]]
        eyes, cr, nose = [rot(e) for e in eyes], rot(cr), rot(nose)
    m.tex = dict(eyes=eyes, cr=cr, nose=nose, hs=hs, Rh=Rh)
    return m


def mask_rule(var, x, y, ex, ey):
    """Masker in kop-coördinaten t.o.v. het kopcentrum (x naar achteren, y omhoog; eenheden hs).
    Een band over beide ogen en de neusrug (zoals foto 7); ex/ey = plek van het oog.
    T = trapjes: achter het oog loopt de band in treden schuin omlaag naar de wang (Andes-trapmotief);
    K = idem + getrapte inkeping in de wenkbrauw boven het oog (halve chakana);
    W = gewoon wasbeermasker ter vergelijking (ronde randen)."""
    u, v = x - ex, y - ey
    if var == 'W':
        inside = (u > -12) & (u < 9) & (np.abs(v + 0.025 * u * u) < 5.2)
        brow = (u > -7) & (u < 5) & (v > 5.2) & (v < 8.2)
        return inside, brow
    top = np.select([u < 3.5, u < 7.5, u < 11.5], [5.0, 1.5, -2.0], -99)
    bot = np.select([u < 3.5, u < 7.5, u < 11.5], [-4.5, -8.0, -11.5], 99)
    inside = (u > -13) & (v < top) & (v > bot)
    brow = (u > -7) & (u < 11.5) & (v >= top) & (v < top + 3.0)
    if var == 'K':
        notch = (u > -2.5) & (u < 1.5) & (v >= top - 2.0) & (v < top)
        inside, brow = inside & ~notch, brow | notch
    return inside, brow


def render(m, yaw, pitch, scale, center, var='T'):
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
    t = m.tex
    sel = np.isin(gid, [groups.index('head'), groups.index('muzzle')])
    q = wpt[sel] @ Rc                     # terug naar diercoördinaten
    g = gid[sel].copy()
    ql = (q - t['cr']) @ t['Rh'] / t['hs']
    el = (t['eyes'][0] - t['cr']) @ t['Rh'] / t['hs']
    inside, brow = mask_rule(var, ql[:, 0], ql[:, 1], el[0], el[1])
    g[brow] = groups.index('brow')
    g[inside] = groups.index('mask')
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
    for _ in range(2):
        edge = edge | np.roll(edge, 1, 0) | np.roll(edge, 1, 1)
    inner = a.copy()
    for _ in range(9):
        inner = inner & np.roll(inner, 1, 0) & np.roll(inner, -1, 0) & np.roll(inner, 1, 1) & np.roll(inner, -1, 1)
    edge = (edge & a) | (a & ~inner)
    rgb[edge] = LINE
    rgb[~a] = 255
    return Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).resize((out, out), Image.LANCZOS)


def view(m, yaw, pitch=10, size=232, var='T'):
    Rc = P.rot_x(math.radians(pitch)) @ P.rot_y(math.radians(yaw))
    pts = np.array([Rc @ c for c, r, R0, g in m.parts]); rs = np.array([r.max() for c, r, R0, g in m.parts])
    x0, x1, y0, y1 = (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()
    scale = R * (size / 256) / max(x1 - x0, y1 - y0)
    return shade(*render(m, yaw, pitch, scale, ((x0 + x1) / 2, (y0 + y1) / 2), var))


F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)


def raster():
    """Hoeken: rij = voorover (romphoek), kolom = draaiing naar de speler."""
    yaws, leans = (25, 40, 55), (45, 60)
    cell = 262
    im = Image.new('RGB', (12 + cell * len(yaws), 40 + (cell + 22) * len(leans)), 'white')
    d = ImageDraw.Draw(im)
    d.text((12, 10), 'Wasbeer: waterspuwer, kies een hoek (draaiing / voorover)', font=FB, fill=(30, 30, 30))
    for j, ln in enumerate(leans):
        for i, yw in enumerate(yaws):
            v = view(wasbeer(lean=ln), yw)
            x, y = 12 + cell * i, 40 + (cell + 22) * j
            im.paste(v, (x, y))
            d.text((x + 4, y + 258), f'{"ABC"[i]}{j + 1}: draai {yw}°, romp {ln}°', font=F, fill=(60, 60, 60))
    im.save(os.path.join(HERE, 'hoeken.png'))


def maskers(yaw=40, lean=45):
    labs = {'T': 'T: trapjes', 'K': 'K: trapjes + inkeping', 'W': 'W: gewoon wasbeermasker'}
    im = Image.new('RGB', (12 + 262 * 3, 40 + 262 + 26 + 230), 'white')
    d = ImageDraw.Draw(im)
    d.text((12, 10), f'Wasbeer: masker (draai {yaw}°, romp {lean}°)', font=FB, fill=(30, 30, 30))
    for i, v in enumerate('TKW'):
        img = view(wasbeer(lean=lean), yaw, var=v)
        im.paste(img, (12 + 262 * i, 40))
        d.text((16 + 262 * i, 40 + 258), labs[v], font=F, fill=(60, 60, 60))
        bb = img.convert('L').point(lambda p: p < 250 and 255).getbbox()
        x0, y0 = bb[0], bb[1]
        im.paste(img.crop((x0, y0, x0 + 100, y0 + 100)).resize((220, 220), Image.LANCZOS), (12 + 262 * i + 20, 40 + 262 + 26))
    im.save(os.path.join(HERE, 'maskers.png'))


if __name__ == '__main__':
    raster()
    maskers()
