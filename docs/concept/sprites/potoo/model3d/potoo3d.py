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
    'fur': '#EEECF3', 'wing': '#D3CFDE', 'belly': '#FAF9FC', 'tail': '#C6C1D3', 'jaw': '#6C657C', 'rim': '#E6CFC8',
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
    onderkaaktip=(-58, 30),     # (465, 150) op de zijfoto; iets verder open zoals de 3/4-foto (opening ±1/2 kophoogte)
    oog=(-49.5, 69),            # (415, 70), ±35x20 px
    kruin=(-24, 82.5),          # (330, 25)
    achterhoofd=(6, 72),        # (230, 60)
    schouder=(36, 54),          # (130, 120) rug hoog, gebogen
    rug=(46.5, 15),             # (95, 250)
    borst=(-37.5, 30),          # (375, 200)
    onderlijf=(-18, -39),       # (310, 430)
    staartonder=(9, -73.5),     # (220, 545), staart ±185 px breed onderaan, hangt recht omlaag
)
KOP = 1.6                      # Pokémon: kop iets groter dan echt (om het achterhoofd geschaald)
# Kopmaten (kopcoördinaten, vóór KOP). NIET van de zijfoto (Jordi: "die hele platte hoofd foto mag je vergeten"),
# maar gefit op de verhoudingen van de 3/4-foto met meten.py / fit_kop.py (lijnen en verhoudingen, geen giswerk).
KP = dict(schedel=(-30, 88, 30, 22, 35), mondhoek=(-40, 63), snaveltip=(-62, 63), onderkaaktip=(-55, 36),
          bek_breed=17, rand=0.9, oog=(-49.5, 74), oog_r=7.0)


def potoo(lean=0, gape=None, kopdraai=10, kopkantel=10, kp=None):
    """kopdraai: kop extra naar de kijker (SPRITE_NORM: kop draait meer dan het lijf); kopkantel: kop omhoog (3/4-foto)."""
    m = Model()
    Rl = rot_z(math.radians(lean))
    P = lambda p: Rl @ np.array(p, float)
    E = lambda c, r, g, R0=None: m.ell(P(c), r, g, Rl if R0 is None else Rl @ R0)
    # lijf: hoge zuil, rug hoog en gebogen (zijfoto), borst vooraan
    E((6, -10, 0), (37, 68, 46), "fur")   # breedte: lijf ±1,35-1,45 x de kopbreedte (voorfoto nacht, takfoto)
    E((26, 40, 0), (20, 20, 36), 'fur')                 # gebogen rug/schouders
    E((-20, 0, 0), (20, 52, 36), 'belly')
    E((-8, 50, 0), (22, 18, 32), 'fur')                 # overgang naar de kop, geen nek
    # vleugels: gevouwen tegen het lijf; volgen de zijkant van net onder de kop (schouder) tot over de staart
    # (voorfoto nacht, takfoto, zijfoto: de vleugelrand ís de buitenomtrek van het lijf, geen los paneel)
    for sz in (1, -1):
        for t in np.linspace(0, 1, 26):
            y = 44 - 128 * t
            zb = 46 * math.sqrt(max(0.0, 1 - ((y + 10) / 68) ** 2))
            zt = 26 + 16 * min(1, max(0, (-60 - y) / 30))       # staartbreedte eronder
            z = max(zb, zt * 0.85) * 0.93 + 2
            E((16 + 8 * t, y, z * sz), (24 - 10 * t, 7, 6), 'wing')
    for t in np.linspace(0, 1, 12):                      # staart: breed, hangt recht omlaag
        E((16 + 22 * t, -58 - 40 * t, 0), (10, 8, 26 + 16 * t), 'tail')   # schuin naar achteren (Noctowl/Swellow), anders leest hij als paal
    # kop
    n0 = len(m.parts)
    piv = np.array(LM['achterhoofd'] + (0,), float)
    H = lambda p: piv + (np.array(p, float) - piv) * KOP + np.array((0, -11, 0))   # kop laag op de schouders, geen nek
    k = dict(KP if kp is None else kp)
    v = lambda key, z=0: np.array(tuple(k[key]) + (z,), float)
    sx, sy, sa, sb, sc = k['schedel']
    E(H((sx, sy, 0)), np.array((sa, sb, sc)) * KOP, 'fur')
    E(H((sx + 22, sy + 2, 0)), np.array((18, 12, sc * 0.78)) * KOP, 'fur')     # achterhoofd (niet over de ogen)
    # ogen: pikzwart (Drifloon), op het schedeloppervlak op de gemeten plek
    for sz in (1, -1):
        dx = (k['oog'][0] - sx) / sa; dy = (k['oog'][1] - sy) / sb
        n = np.array((dx, dy, math.sqrt(max(0.0, 1 - dx * dx - dy * dy)) * sz))
        c = np.array((sx + sa * n[0], sy + sb * n[1], sc * n[2]))
        E(H(c), np.array((1, 1.06, 0.62)) * k['oog_r'] * KOP, 'eye', rot_y(math.atan2(n[0], n[2])))
    Rh = rot_y(math.radians(kopdraai)) @ rot_z(math.radians(-kopkantel))
    pv = P(piv)
    m.parts[n0:] = [(pv + Rh @ (c - pv), r, Rh @ R0, g) for c, r, R0, g in m.parts[n0:]]
    m.n0 = n0
    snavel_uit_foto(m, P(piv), lambda q: pv + Rh @ (H(q) - pv), k)
    return m


# SNAVEL: omtrek punt voor punt overgetrokken van de close-up van de 3/4-foto (referenties/jordi_great_potoo_bek_open_drieluik.webp,
# fotopixels; raster 5 px op 7x). Jordi: "de puntige uiteinden", "de golvende vorm naar de punt toe", "meet ook de snavel af".
BOVENRAND = [(235.7, 130.7), (245, 134.3), (255, 137), (265, 138.6), (275, 139.3), (285, 139.3), (295, 138.9), (305, 138.3),
             (313.6, 137.9), (322, 141.4), (330.7, 147.9)]                    # nabije mondhoek -> voorkant (bij het haakje)
VERRE_RAND = [(330.7, 147.9), (331.4, 155.7), (329.3, 167), (325.7, 177), (322, 184.3), (316.4, 194.3), (309.3, 201.4),
              (296.4, 205.7)]                                                  # verre kant onderkaak: golft naar de punt
NABIJE_RAND = [(235.7, 131.4), (242, 147), (249, 158.6), (257.9, 170), (267.9, 180), (277.9, 187), (286.4, 194.3),
               (292, 201.4), (296.4, 205.7)]                                    # nabije kant onderkaak -> punt
HAAKJE = [(331.4, 141.4), (335.5, 142.5), (337.9, 144.3), (339.0, 150), (339.3, 157)]   # donker, spits, krult omlaag
KAAKPUNT = [(290.5, 202.5), (296.4, 205.7), (299.5, 208.5)]                        # donker, spits
FOTO_OOG, FOTO_KRUIN = (271.7, 111.3), (240, 27)
ONTWERP_YAW, ONTWERP_PITCH = 45, 8


def snavel_uit_foto(m, pv, wereld, k):
    """Zet de overgetrokken 2D-omtrek terug in 3D: voor elk punt is de diepte (kop-z) bekend uit zijn plek op de rand
    (nabije mondhoek +w, voorkant 0, verre mondhoek -w); x en y volgen uit de projectie op de ontwerphoek (2x2-stelsel)."""
    Rc = rot_x(math.radians(ONTWERP_PITCH)) @ rot_y(math.radians(ONTWERP_YAW))
    scr = lambda q: (Rc @ wereld(np.array(q, float)))[:2]
    # schaal en plaats: oogmidden en kruin van foto en model op elkaar
    sx, sy, sa, sb, sc = k['schedel']
    dx = (k['oog'][0] - sx) / sa; dy = (k['oog'][1] - sy) / sb
    oog_q = (sx + sa * dx, sy + sb * dy, sc * math.sqrt(max(0.0, 1 - dx * dx - dy * dy)))
    oog_s = scr(oog_q)
    kruin_s = max((Rc @ c)[1] + np.linalg.norm((Rc @ R0 @ np.diag(r))[1]) for c, r, R0, g in m.parts[m.n0:])
    kk = (kruin_s - oog_s[1]) / (FOTO_OOG[1] - FOTO_KRUIN[1])
    naar_s = lambda p: np.array((oog_s[0] - (p[0] - FOTO_OOG[0]) * kk, oog_s[1] - (p[1] - FOTO_OOG[1]) * kk))
    w = k['bek_breed']
    q0 = np.array(oog_q, float)
    J = np.array([(scr(q0 + e) - scr(q0)) for e in np.eye(3)]).T     # 2x3, de projectie is lineair in q

    def terug(p, z):
        t = naar_s(p) - scr(q0) - J[:, 2] * (z - q0[2])
        xy = np.linalg.solve(J[:, :2], t)
        return wereld(np.array((q0[0] + xy[0], q0[1] + xy[1], z)))

    def lijn(pts, z0, z1, n=60):
        pts = np.array(pts, float); L = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
        out = []
        for t in np.linspace(0, 1, n):
            p = np.array([np.interp(t * L[-1], L, pts[:, i]) for i in (0, 1)])
            out.append(terug(p, z0 + (z1 - z0) * math.sin(t * math.pi / 2) if z0 else z1 * t))
        return out
    rr = k['rand'] * KOP
    boven = lijn(BOVENRAND, w, 0); verre = lijn(VERRE_RAND, -w, 0); nabij = lijn(NABIJE_RAND, w, 0)
    for p in boven + verre + nabij:
        m.parts.append((p, np.array((rr, rr, rr)), np.eye(3), 'rim'))
    # binnenkant: tussen nabije en verre rand, iets dieper de kop in (weg van de kijker)
    achter = np.linalg.inv(Rc) @ np.array((0, 0, -1.0))
    for a, b in zip(nabij[::2], verre[::2]):
        for t in np.linspace(0.05, 0.95, 12):
            p = a * (1 - t) + b * t + achter * (6 + 6 * math.sin(math.pi * t))
            m.parts.append((p, np.array((3.2, 3.2, 3.2)) * KOP, np.eye(3), 'mouth'))
    for a, b in zip(boven[::3], nabij[::3]):
        for t in np.linspace(0.1, 0.9, 6):
            p = a * (1 - t) + b * t + achter * 7
            m.parts.append((p, np.array((3.2, 3.2, 3.2)) * KOP, np.eye(3), 'mouth'))
    for pts in (HAAKJE, KAAKPUNT):                                    # spitse donkere punten
        ln = lijn(pts, -2, -2, 12) if pts is HAAKJE else lijn(pts, 0.01, 0, 10)
        for i, p in enumerate(ln):
            r = (1.6 - 1.2 * i / (len(ln) - 1)) * KOP
            m.parts.append((p, np.array((r, r, r)), np.eye(3), 'beak'))
    # de mond zit IN de kop (foto: onderkant kop = kaakpunt): bevederde buitenkant van de onderkaak en wangen
    # achter de randen, zodat de opening niet als slab onder de kop hangt
    for p in nabij[::2] + verre[::2]:
        m.parts.append((p + achter * 15, np.array((6, 6, 6)) * KOP, np.eye(3), 'fur'))
    for a, b in zip(boven[::4], nabij[::4]):                         # wang tussen mondhoek en schedel
        m.parts.append(((a + b) / 2 + achter * 16, np.array((7, 7, 7)) * KOP, np.eye(3), 'fur'))


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
