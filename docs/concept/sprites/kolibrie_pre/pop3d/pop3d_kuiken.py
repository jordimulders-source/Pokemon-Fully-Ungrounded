"""Kolibrie pre-evo (puur Flying): 3D-poppetje als praatplaat, werkwijze van de lama/Coathief
(lama/ontwerp/pop3d_lama.py op branch claude/blissful-sagan-4f6hqj; renderer olinguito_v2/silhouet_kolibriemethode/pop3d.py).
Diercoördinaten: x = naar achteren (staart), y = omhoog, z = naar de kijker bij 0° (zijaanzicht, kop links).
Pose = silhouet v3A (Jordi 2 nov: "a veel beter"), dus foto 1 (zittend jong, kop links) + foto 3 (open bedelbek):
zittend, vleugels ingeklapt, bekje open. "Moet echt cute zijn."
Draaien vanuit deze map: python3 pop3d_kuiken.py"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../olinguito_v2/silhouet_kolibriemethode'))
import pop3d as P

R = 768
LINE = np.array((34, 24, 44), np.uint8)
PALET = {   # kleur van de pre-evo (eindvorm: fluweelzwarte kop, violet lijf, blauwgroene schouder)
    'fluweel (als eindvorm)': dict(body='#6E5A8C', head='#3E2E52', wing='#4A3A63', belly='#D9CFE8', shoulder='#3FA3A0'),
    'dons (jong, doffer)': dict(body='#8A7F96', head='#5E5470', wing='#5A4F68', belly='#EEE8F2', shoulder='#6FA9A2'),
    'hillstar + violet': dict(body='#8C7A6A', head='#6A5A62', wing='#5E4E5E', belly='#F2EEE8', shoulder='#7A5AA0'),
}
COL = {'body': '', 'belly': '', 'head': '', 'wing': '', 'far': '', 'shoulder': '', 'tail': '', 'tuft': '',
       'beak': '#262030', 'gape': '#F4C83C', 'mouth': '#E8707A', 'eye': '#120C18', 'glint': '#FFFFFF', 'feet': '#262030'}
NOSHADE = {'eye', 'glint', 'gape', 'mouth'}
LINED = {'eye', 'gape', 'beak'}


def set_palet(naam):
    v = PALET[naam]; COL.update(v)
    dark = lambda h: '#%02X%02X%02X' % tuple(int(c * 0.78) for c in P.hexc(h))
    COL.update(far=dark(v['wing']), tail=v['wing'], tuft=v['head'])


def fluff(m, c, r, g, n, rs, seed, ymin=-1.0, R0=None):
    """Donsbobbels op het oppervlak van een ellipsoïde (pluizige omtrek, zoals de lamawol)."""
    rng = np.random.default_rng(seed)
    R0 = np.eye(3) if R0 is None else R0
    for _ in range(n):
        d = rng.normal(size=3); d /= np.linalg.norm(d)
        if d[1] < ymin: continue
        m.ell(np.array(c) + R0 @ (d * np.array(r) * 0.92), rs * rng.uniform(0.8, 1.15), g)


def kuiken(hs=1.0, open_=46, kantel=24, dons=True):
    m = P.Model()
    rz = P.rot_z
    # lijf: peer, schuin (foto 1: kop linksboven, staart rechtsonder), donzige buik
    Rb = rz(math.radians(26))
    m.ell((8, 0, 0), (21, 28, 20), 'body', Rb)
    m.ell((-1, -5, 5), (17, 22, 16), 'belly', rz(math.radians(22)))
    if dons:
        fluff(m, (-1, -5, 5), (17, 22, 16), 'belly', 18, 6.5, 3, ymin=-0.9, R0=rz(math.radians(22)))
    # kop: groot (fase 1), iets omhoog: hij bedelt
    hc = np.array((-12, 30 + 10 * (hs - 1), 0.0)); HR = 19.0 * hs
    m.ell(hc, (HR, HR * 0.95, HR * 0.92), 'head')
    if dons:
        fluff(m, hc, (HR, HR * 0.95, HR * 0.92), 'head', 26, 3.6 * hs, 11, ymin=0.15)
    m.ell(hc + np.array((-3, -12, 0)) * hs, np.array((11, 8, 12)) * hs, 'belly')       # lichte kin
    # open bedelbekje (foto 3): kort, breed aan de basis, gele mondhoeken
    a = math.radians(180 - kantel); base = hc + np.array((-HR * 0.84, -2.5 * hs, 0))
    def snavel(hoek, L, r0):
        d = np.array((math.cos(hoek), math.sin(hoek), 0))
        return [tuple(base + d * L * t) + (r0 * (1 - t) + 0.9 * t,) for t in np.linspace(0, 1, 7)]
    m.chain(snavel(a - math.radians(open_ / 2), 22 * hs, 4.6 * hs), 'beak', 0.8)   # bovensnavel (omhoog)
    m.chain(snavel(a + math.radians(open_ / 2), 19 * hs, 4.0 * hs), 'beak', 0.8)   # ondersnavel
    m.ell(base + np.array((-1, 0, 0)), np.array((6, 6.5, 5)) * hs, 'gape')
    m.ell(base + np.array((-4, 0, 0)), np.array((5, 4.2, 3.2)) * hs, 'mouth')
    # grote glimmende ogen
    for sz in (1, -1):
        d = np.array((-0.45, 0.20, 0.87 * sz)); d /= np.linalg.norm(d)
        e = hc + d * HR * 0.88
        m.ell(e, 5.6 * hs, 'eye')
        m.ell(e + d * 3.6 * hs + np.array((-1.4, 2.2, 0)) * hs, 1.8 * hs, 'glint')
    # donsplukje op de kruin (voorbode van de jeguaka van de eindvorm)
    t0 = hc + np.array((5, HR * 0.92, 0))
    m.chain([tuple(t0) + (3.4 * hs,), tuple(t0 + np.array((7, 5, 0)) * hs) + (2.2 * hs,), tuple(t0 + np.array((12, 6, 0)) * hs) + (1.0,)], 'tuft', 0.8)
    # vleugels ingeklapt langs het lijf, punten over het staartje
    for sz, g in ((1, 'wing'), (-1, 'far')):
        m.ell((18, -4, 15 * sz), (7, 25, 5), g, rz(math.radians(36)))
    m.ell((5, 13, 17.0), (6, 3.2, 4), 'shoulder', rz(math.radians(30)))
    # staartstompje
    m.ell((36, -26, 0), (12, 4.5, 8), 'tail', rz(math.radians(-38)))
    # pootjes (kort, zwart)
    for dz in (7, -7):
        m.chain([(2, -26, dz, 2.6), (0, -31, dz, 2.0)], 'feet', 0.8)
        m.chain([(0, -31, dz, 1.8), (-7, -32, dz, 1.3)], 'feet', 0.8)
    return m


def render(m, yaw, pitch, scale, center):
    Rc = P.rot_x(math.radians(pitch)) @ P.rot_y(math.radians(yaw))
    zbuf = np.full((R, R), -1e9, np.float32); gid = np.full((R, R), -1, np.int16)
    nrm = np.zeros((R, R, 3), np.float32); groups = list(COL)
    ys, xs = np.mgrid[0:R, 0:R]
    wx = (xs - R / 2) / scale + center[0]; wy = -((ys - R / 2) / scale) + center[1]
    for c, r, R0, g in m.parts:
        cw = Rc @ c; M = np.diag(1 / r) @ R0.T @ Rc.T; ext = r.max()
        x0 = int(max(0, (cw[0] - ext - center[0]) * scale + R / 2 - 2)); x1 = int(min(R, (cw[0] + ext - center[0]) * scale + R / 2 + 3))
        y0 = int(max(0, (-(cw[1] + ext) + center[1]) * scale + R / 2 - 2)); y1 = int(min(R, (-(cw[1] - ext) + center[1]) * scale + R / 2 + 3))
        if x0 >= x1 or y0 >= y1: continue
        px = wx[y0:y1, x0:x1] - cw[0]; py = wy[y0:y1, x0:x1] - cw[1]
        a = M[:, 0, None, None] * px + M[:, 1, None, None] * py; b = M[:, 2]; A = b @ b
        B = 2 * (a * b[:, None, None]).sum(0); C = (a * a).sum(0) - 1
        disc = B * B - 4 * A * C; hit = disc >= 0
        z = (-B + np.sqrt(np.where(hit, disc, 0))) / (2 * A) + cw[2]
        sub = zbuf[y0:y1, x0:x1]; win = hit & (z > sub)
        sub[win] = z[win]; gid[y0:y1, x0:x1][win] = groups.index(g)
        p = np.stack([px, py, z - cw[2]], -1); n = p @ (M.T @ M).T
        n /= np.linalg.norm(n, axis=-1, keepdims=True) + 1e-9
        nrm[y0:y1, x0:x1][win] = n[win]
    return zbuf, gid, nrm, groups


def shade(zbuf, gid, nrm, groups, out=256):
    a = gid >= 0
    rgb = np.ones((R, R, 3), np.float32) * 255
    Lt = np.array((-0.45, 0.65, 0.62)); Lt /= np.linalg.norm(Lt)
    lit = (nrm @ Lt) > -0.2
    for i, g in enumerate(groups):
        mm = gid == i; col = P.hexc(COL[g]); rgb[mm] = col
        if g not in NOSHADE: rgb[mm & ~lit] = col * 0.78
    edge = np.zeros((R, R), bool); z = np.where(a, zbuf, -1e9)
    lined = np.isin(gid, [groups.index(g) for g in LINED])
    for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):
        z2 = np.roll(np.roll(z, -dy, 0), -dx, 1); g2 = np.roll(np.roll(gid, -dy, 0), -dx, 1); l2 = np.roll(np.roll(lined, -dy, 0), -dx, 1)
        e = (np.abs(z - z2) > 6) | ((gid != g2) & (lined | l2))
        edge |= e; edge |= np.roll(np.roll(e, dy, 0), dx, 1)
    for _ in range(2): edge = edge | np.roll(edge, 1, 0) | np.roll(edge, 1, 1)
    inner = a.copy()
    for _ in range(7): inner = inner & np.roll(inner, 1, 0) & np.roll(inner, -1, 0) & np.roll(inner, 1, 1) & np.roll(inner, -1, 1)
    edge = (edge & a) | (a & ~inner)
    rgb[edge] = LINE; rgb[~a] = 255
    return Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).resize((out, out), Image.LANCZOS), a


def view(m, yaw, pitch=8, size=236):
    Rc = P.rot_x(math.radians(pitch)) @ P.rot_y(math.radians(yaw))
    pts = np.array([Rc @ c for c, r, R0, g in m.parts]); rs = np.array([r.max() for c, r, R0, g in m.parts])
    x0, x1, y0, y1 = (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()
    scale = R * (size / 256) / max(x1 - x0, y1 - y0)
    return shade(*render(m, yaw, pitch, scale, ((x0 + x1) / 2, (y0 + y1) / 2)))


def kopaandeel(m, yaw, pitch=8):
    """Kophoogte / totale hoogte (D2 in FAKEMON_CHECKLIST; fase 1 ±40-55%)."""
    Rc = P.rot_x(math.radians(pitch)) @ P.rot_y(math.radians(yaw))
    yy = [((Rc @ c)[1] - r.max(), (Rc @ c)[1] + r.max(), g) for c, r, R0, g in m.parts]
    lo, hi = min(y[0] for y in yy), max(y[1] for y in yy)
    hd = [y for y in yy if y[2] in ('head', 'eye', 'tuft')]
    return (max(y[1] for y in hd) - min(y[0] for y in hd)) / (hi - lo)


VARIANTEN = {'A': dict(hs=0.9), 'B': dict(hs=1.05), 'C': dict(hs=1.2)}
YAW = 22   # foto 1: lijf iets naar de kijker gedraaid


def vel():
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
    ref = os.path.join(HERE, '../referenties')
    cell, W = 262, 12 + 262 * 4
    im = Image.new('RGB', (W, 44 + (cell + 24) * 2), 'white'); d = ImageDraw.Draw(im)
    d.text((12, 12), 'Kolibrie pre-evo: poppetje in de hoek van foto 1. Rij 1: kopgrootte, rij 2: kleur (op B)', font=FB, fill=(30, 30, 30))
    set_palet('fluweel (als eindvorm)')
    for i, (k, v) in enumerate(VARIANTEN.items()):
        m = kuiken(**v); img, _ = view(m, YAW)
        x, y = 12 + cell * i, 44; im.paste(img, (x, y))
        d.text((x + 4, y + 258), f'{k}: kop {kopaandeel(m, YAW):.0%} van de hoogte', font=F, fill=(60, 60, 60))
    foto = Image.open(os.path.join(ref, 'jordi_1_zittend_jong.webp')).convert('RGB').crop((200, 140, 740, 710))
    foto.thumbnail((256, 256)); im.paste(foto, (12 + cell * 3, 44)); d.text((16 + cell * 3, 44 + 258), 'foto 1 (pose)', font=F, fill=(60, 60, 60))
    for i, naam in enumerate(PALET):
        set_palet(naam); img, _ = view(kuiken(**VARIANTEN['B']), YAW)
        x, y = 12 + cell * i, 44 + cell + 24; im.paste(img, (x, y)); d.text((x + 4, y + 258), naam, font=F, fill=(60, 60, 60))
    f3 = Image.open(os.path.join(ref, 'jordi_3_nestjongen.png')).convert('RGB').crop((0, 225, 220, 447)).resize((256, 256))
    im.paste(f3, (12 + cell * 3, 44 + cell + 24)); d.text((16 + cell * 3, 44 + 2 * cell + 26), 'foto 3 (bek)', font=F, fill=(60, 60, 60))
    im.save(os.path.join(HERE, 'vel_ronde1.png'))


def lijn():
    """Pre-evo (poppetje B) naast de eindvorm (sprite, af) op schaal: hoogte ~ wortel van het oppervlak."""
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
    W, H, base = 12 + 380 * 2, 380, 340
    im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)
    d.text((12, 10), 'Kolibrie-lijn op schaal: pre-evo (Flying) - eindvorm (Ghost/Flying, af)', font=FB, fill=(30, 30, 30))
    set_palet('fluweel (als eindvorm)')
    img, a = view(kuiken(**VARIANTEN['B']), YAW)
    bb = Image.fromarray((a * 255).astype(np.uint8)).resize(img.size).getbbox(); img = img.crop(bb)
    eind = Image.open(os.path.join(HERE, '../../kolibrie/af/kolibrie.png')).convert('RGBA'); eind = eind.crop(eind.getbbox())
    k = 4.0   # sprites op 4x; pre-evo hoogte uit het silhouet v3A (36 px) op dezelfde schaal
    eind = eind.resize((eind.width * 4, eind.height * 4), Image.NEAREST)
    h = 36 * 4 * 0.9; img = img.resize((int(img.width * h / img.height), int(h)), Image.LANCZOS)
    im.paste(img, (12 + (330 - img.width) // 2, base - img.height)); d.text((18, base + 12), 'pre-evo (poppetje B, ±600 px)', font=F, fill=(60, 60, 60))
    bg = Image.new('RGBA', eind.size, 'white'); bg.alpha_composite(eind)
    im.paste(bg.convert('RGB'), (392 + (380 - eind.width) // 2, base - eind.height)); d.text((398, base + 12), 'eindvorm (sprite af, ±1000 px)', font=F, fill=(60, 60, 60))
    im.save(os.path.join(HERE, 'lijn_ronde1.png'))


if __name__ == '__main__':
    vel(); lijn()
