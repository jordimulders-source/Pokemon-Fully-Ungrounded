"""Great potoo (Ghost/Normal): 3D-poppetje in de stijl van het lama-poppetje (lama/ontwerp/pop3d_lama.py):
onderdelen als bollen/ketens, vlakke kleuren met één schaduwtoon en een donkere lijn. Praatplaat + bron voor het silhouet.
Diercoördinaten: x = naar achteren, y = omhoog, z = naar de kijker bij yaw 0 (dan zie je de linkerflank, snavel naar links).
Bronnen: alleen Jordi's 5 foto's (SPEC). Kop: linkerhelft van de duo-foto (leidraad).
Draaien vanuit de repo-root: python3 docs/concept/sprites/potoo/poppetje/pop3d_potoo.py"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../olinguito_v2/silhouet_kolibriemethode'))
import pop3d as P

R = 768
LINE = np.array((44, 36, 58), np.uint8)
COL = {
    'body': '#EEEDF4', 'head': '#F2F1F7', 'wing': '#D9D5E6', 'far': '#C9C4D8', 'tail': '#D2CEE0', 'bark': '#9A8F9C',
    'eye': '#08070C', 'rim': '#DAD6E4', 'hook': '#3A3442', 'tip': '#4A4352',
    'mouth': '#6E5FD0', 'throat': '#2E2468', 'palate': '#5A4CB8', 'tuft': '#D3CEE0',
}
NOSHADE = {'eye', 'throat'}
LINED = {'eye', 'rim', 'hook', 'tip', 'mouth', 'throat', 'palate', 'tuft', 'bark'}


def potoo(kop=1.0, oog=6.2, bek=1.0, open_=1.0, voorover=8):
    """kop: schaal van de kop; oog: oogstraal; bek: schaal van de muil; open_: hoe ver de onderkaak hangt."""
    m = P.Model()
    k = kop
    # ---- lijf: rechtop, taps (nachtfoto): breed net onder de kop, smal naar de staart; vleugels liggen langs de flanken
    m.ell((11, -16, 0), (16, 24, 25), 'body')
    m.ell((12, -42, 0), (12, 18, 19), 'body')
    for sz, g in ((1, 'wing'), (-1, 'far')):
        m.ell((13, -22, 20 * sz), (11, 28, 6), g, P.rot_z(math.radians(-8)))
        m.ell((17, -50, 13 * sz), (7, 20, 5), g, P.rot_z(math.radians(-12)))
    m.chain([(15, -54, 0, 7.5), (19, -70, 0, 6.5), (22, -84, 0, 5.0)], 'tail', 1.2)
    # een paar schorsvlekken (Hisui-Zorua-idee)
    for c, r in (((14, -16, 25.5), (2.6, 4.5, 1.2)), ((18, -46, 18), (2.2, 3.8, 1.2))):
        m.ell(c, r, 'bark')
    h0 = len(m.parts)
    # ---- kop: grote ronde bol zonder nek, breder dan hoog, kruin breed (close-up)
    cr = np.array((0, 16, 0.0))
    m.ell(cr, np.array((17, 16, 19)) * k, 'head')
    m.ell(cr + np.array((3, 7, 0)) * k, np.array((15, 10, 17)) * k, 'head')       # brede kruin
    # ---- ogen: groot, pikzwart, voor-opzij, ruim boven de bek
    ogen = []
    for sz in (1, -1):
        d = np.array((-0.62, 0.30, 0.72 * sz)); d /= np.linalg.norm(d)
        e = cr + d * np.array((17, 16, 19)) * k * 0.90
        m.ell(e, oog * k, 'eye'); ogen.append(e)
    # ---- kleine veertjes tussen de ogen: plukjes in een V die naar het haakje wijst (close-up: de 'frons')
    for sz in (1, -1):
        for t in np.linspace(0, 1, 5):
            y = cr[1] + (10 - 12 * t) * k; zz = (6.5 - 5.5 * t) * sz * k
            x = cr[0] - 16.3 * k * math.sqrt(max(0.05, 1 - (zz / (19 * k)) ** 2 - ((y - cr[1]) / (16 * k)) ** 2)) - 0.6
            Rt = P.rot_y(math.radians(-30 * sz)) @ P.rot_x(math.radians(-48 * sz))
            m.ell((x, y, zz), np.array((1.0, 2.6, 0.9)) * k, 'tuft', Rt)
    # ---- bek (bovensnavel): rechte harde rand van mondhoek (onder/achter het oog) naar het haakje
    gy = cr[1] - 5.5 * k                                # hoogte gaplijn
    hoek = [np.array((0.5, gy + 0.5, 17.5 * sz)) * np.array((1, 1, k)) for sz in (1, -1)]
    voor = np.array((cr[0] - 18.5 * k, gy - 0.5, 0))
    for h in hoek:
        pts = [tuple(h + (voor - h) * t) + (1.5 * k,) for t in np.linspace(0, 1, 9)]
        m.chain(pts, 'rim', 1.0)
    m.chain([(voor[0] + 1.5, voor[1] + 2.0, 0, 2.2 * k), (voor[0] - 1.6, voor[1] + 0.8, 0, 1.7 * k),
             (voor[0] - 2.0, voor[1] - 2.5, 0, 1.1 * k), (voor[0] - 0.8, voor[1] - 4.6, 0, 0.5 * k)], 'hook', 0.6)
    # gehemelte: net onder de rand, iets donkerder
    m.ell((cr[0] - 7 * k, gy - 0.8, 0), np.array((11, 1.6, 14)) * k, 'palate')
    # ---- onderkaak: uitgesproken V; muil = kom precies tussen de kaaktakken (dezelfde breedtelijn)
    b = bek
    tip = np.array((cr[0] - 24 * k * b, gy - 30 * k * b * open_, 0))
    c1, c2 = hoek
    u = tip - (c1 + c2) / 2; L = np.linalg.norm(u); u /= L
    v = np.array((0, 0, 1.0)); n = np.cross(u, v); n /= np.linalg.norm(n)
    if n[0] > 0: n = -n
    Rj = np.stack([u, v, n], 1)
    W0 = abs(c1[2])
    breed = lambda t: W0 * (1.04 * max(0.0, 1 - t ** 2.0) ** 0.75 + 0.15 * math.sin(math.pi * t)) * (1 - t) ** 0.15   # brede U, klein puntje
    base = (c1 + c2) / 2
    hol = lambda t: -n * 9.0 * math.sin(math.pi * min(1, t * 1.15)) ** 0.7          # kom: midden ligt dieper dan de randen
    for t in np.linspace(0.0, 0.97, 26):
        w = breed(t); c = base + u * L * t
        m.ell(c - n * 3.5 + hol(t), (L / 9, w + 1.6, 4.0), 'body', Rj)     # bevederde buitenkant
        for f, dz in ((0.0, 1.0), (0.55, 0.6), (0.85, 0.3)):             # muil: midden het diepst (kom)
            m.ell(c + hol(t) * dz + v * 0, (L / 9, max(w * (1 - f) - 0.6, 0.4), 1.2), 'mouth', Rj) if f == 0 else None
        m.ell(c + hol(t) * 0.35, (L / 9, max(w - 0.6, 0.4), 1.2), 'mouth', Rj)
    m.ell(base + u * L * 0.2 + hol(0.2) * 0.6 + n * 0.5, (L * 0.12, 3.2 * k, 0.6), 'throat', Rj)   # keel: donker, achterin
    for sd in (1, -1):
        pts = [tuple(base + u * L * t + v * sd * breed(t) + n * 0.6) + (2.4 * k * (1 - 0.5 * t),) for t in np.linspace(0, 1, 16)]
        m.chain(pts, 'rim', 0.8)
    m.ell(tip + n * 0.6, np.array((2.4, 2.8, 2.0)) * k, 'tip')
    # kop iets omhoog (bek open), hele vogel licht voorover
    lean = P.rot_z(math.radians(voorover))
    m.parts = [(lean @ c, r, lean @ R0, g) for c, r, R0, g in m.parts]
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
        a = M[:, 0, None, None] * px + M[:, 1, None, None] * py
        bb = M[:, 2]; A = bb @ bb
        B = 2 * (a * bb[:, None, None]).sum(0); C = (a * a).sum(0) - 1
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
        if g not in NOSHADE: rgb[mm & ~lit] = col * 0.84
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


def view(m, yaw, pitch=8, size=236, out=256):
    Rc = P.rot_x(math.radians(pitch)) @ P.rot_y(math.radians(yaw))
    pts = np.array([Rc @ c for c, r, R0, g in m.parts]); rs = np.array([r.max() for c, r, R0, g in m.parts])
    x0, x1, y0, y1 = (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()
    scale = R * (size / 256) / max(x1 - x0, y1 - y0)
    return shade(*render(m, yaw, pitch, scale, ((x0 + x1) / 2, (y0 + y1) / 2)), out=out)


def kop_view(m, yaw, pitch=8, out=256):
    """ingezoomd op de kop"""
    Rc = P.rot_x(math.radians(pitch)) @ P.rot_y(math.radians(yaw))
    kop = [Rc @ c for c, r, R0, g in m.parts if g in ('head', 'eye', 'rim', 'mouth', 'hook', 'tip')]
    kop = np.array(kop); x0, x1 = kop[:, 0].min() - 22, kop[:, 0].max() + 22; y0, y1 = kop[:, 1].min() - 20, kop[:, 1].max() + 20
    scale = R / max(x1 - x0, y1 - y0)
    return shade(*render(m, yaw, pitch, scale, ((x0 + x1) / 2, (y0 + y1) / 2)), out=out)[0]


if __name__ == '__main__':
    uit = sys.argv[1] if len(sys.argv) > 1 else HERE
    m = potoo()
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    hoeken = [(40, 8, 'sprite 3/4'), (0, 0, 'zij'), (90, 5, 'voor'), (140, 12, 'schuin achter'), (180, 5, 'achter'), (-40, 8, '3/4 rechts')]
    im = Image.new('RGB', (262 * 6 + 12, 262 * 2 + 40), 'white'); d = ImageDraw.Draw(im)
    for i, (y, p, n) in enumerate(hoeken):
        im.paste(view(m, y, p)[0], (12 + 262 * i, 10)); d.text((16 + 262 * i, 268), n, font=F, fill=(60, 60, 60))
        im.paste(kop_view(m, y, p), (12 + 262 * i, 286))
    im.save(os.path.join(uit, 'rondom.png'))
