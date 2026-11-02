"""Wasbeer (Dark-starter fase 3, krabbenetende wasbeer): 3D-ontwerp v2 (2 nov), in de stijl van het lama-poppetje.
Nieuw tegenover pop3d_wasbeer.py (afgekeurd: "veel te dikke reet"): het lijf is één doorlopende getaperde buis
(geen losse heup-/dijbollen), slanke dijen, kop ±35% van de hoogte (spriteverhouding), Gumshoos-houding
(op 2 poten, romp voorover), Weavile-beenlengte, armen die zichtbaar uit de schouders komen.
Diercoördinaten: x = naar achteren, y = omhoog, z = naar de kijker bij 0°. Grond op y = 0. Kop links.
Draaien vanuit de repo-root: python3 docs/concept/sprites/wasbeer/ontwerp/pop3d_v2.py"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../olinguito_v2/silhouet_kolibriemethode'))
import pop3d as P

R = 768
LINE = np.array((34, 26, 26), np.uint8)
COL = {
    'body': '#7D756B', 'thigh': '#7D756B', 'farthigh': '#5E574F', 'belly': '#C4B79F', 'far': '#5E574F', 'farbelly': '#8E8270',
    'limb': '#2E2826', 'farlimb': '#1F1A19', 'claw': '#E9DFC6', 'farclaw': '#BFB49C',
    'head': '#8A8379', 'mask': '#1E1A1A', 'white': '#ECE6DA', 'nose': '#141010',
    'eye': '#6B2A1C', 'glint': '#FFFFFF', 'ear': '#7D756B', 'earin': '#ECE6DA',
    'tailL': '#A39A8C', 'tailD': '#2E2826', 'pouch': '#857563', 'lip': '#3A332F',
}
NOSHADE = {'eye', 'glint', 'nose', 'mask'}
LINED = {'eye', 'nose', 'claw', 'farclaw', 'lip', 'pouch'}
FAR = {'body': 'far', 'belly': 'farbelly', 'limb': 'farlimb', 'claw': 'farclaw'}


def unit(v):
    v = np.array(v, float); return v / np.linalg.norm(v)


class Model(P.Model):
    def tube(self, pts, g, step=0.8, gfun=None):
        """Getaperde buis met kleine stap (glad, geen segmentlijnen). pts: (x, y, z, r) of (x, y, z, (rx, ry, rz))."""
        L = 0.0
        for a, b in zip(pts, pts[1:]):
            a3, b3 = np.array(a[:3], float), np.array(b[:3], float)
            ra, rb = np.array(a[3] if np.ndim(a[3]) else (a[3],) * 3, float), np.array(b[3] if np.ndim(b[3]) else (b[3],) * 3, float)
            n = max(2, int(np.linalg.norm(b3 - a3) / step))
            for i in range(n):
                t = i / n
                self.ell(a3 + (b3 - a3) * t, ra + (rb - ra) * t, gfun(L + np.linalg.norm(b3 - a3) * t) if gfun else g)
            L += np.linalg.norm(b3 - a3)
        b = pts[-1]
        self.ell(b[:3], b[3], gfun(L) if gfun else g)


def koevoet(m, hand, d, bend, g, s=1.0, steel=11):
    """Koevoetklauw (SPEC): 2 klauwen tegen elkaar = rechte steel, bocht ±110°, recht eindstuk, punt gespleten in 2 tanden.
    d = richting van de steel, bend = richting waarin het eindstuk afbuigt (loodrecht-ish op d)."""
    d, bend = unit(d), unit(bend)
    side = unit(np.cross(d, bend))
    hand = np.array(hand, float)
    knee = hand + d * steel * s
    a = math.radians(70)                       # eindstuk maakt 110° met de steel
    e = unit(d * math.cos(a) + bend * math.sin(a))
    tip = knee + e * 4.5 * s
    m.tube([(*hand, 2.4 * s), (*knee, 2.2 * s)], g, 0.5)
    m.tube([(*knee, 2.2 * s), (*(knee + e * 2.8 * s), 1.8 * s)], g, 0.5)
    for sd in (-1, 1):                         # gespleten punt: twee platte tanden met een V-inkeping
        m.tube([(*(knee + e * 2.8 * s), 1.3 * s), (*(tip + side * sd * 1.1 * s), 0.7 * s)], g, 0.4)


def klauwpaar(m, hand, f, dn, g, s=1.0, gat=0.9):
    """Klauw zoals klauw3d.py (Jordi: "dit is prima, driekwart in de sprite"): 2 korte klauwen naast elkaar, tegen elkaar,
    buigen van vooruit (f) naar omlaag (dn), alleen bij de punten een kleine inkeping."""
    f, dn = unit(f), unit(dn)
    sd = unit(np.cross(f, dn))
    hand = np.array(hand, float)
    for sz in (1, -1):
        pts = []
        for t in np.linspace(0, 1, 9):
            ang = math.radians(10 + 95 * t)
            zc = 1.5 if t < 0.7 else 1.5 + gat * (t - 0.7) / 0.3
            p = hand + (f * (6 * math.sin(ang) * t + 1.0 * t) + dn * (6 * (1 - math.cos(ang)) * t) + sd * sz * zc) * s
            pts.append((*p, (2.0 - 0.9 * t) * s))
        m.tube(pts, g, 0.3)


def wasbeer(lean=38, near_arm='hoog', head_extra=14, hs=1.12, leg=1.0, leg_k=1.0, body_k=1.0, steel=11, near_back=0, shin_k=1.0, heel=0, pouch_k=0.0, pouch_z=0.0, klauw='koevoet', klauw_s=1.0, crouch=0.0, heel_far=0, head_down=0, armen=''):
    """lean = romp voorover vanaf verticaal (Gumshoos ±15-20, foto 10 ±55). near_arm: 'hoog' (actief, klauw vooruit)."""
    m = Model()
    la = math.radians(lean)
    ax = np.array((-math.sin(la), math.cos(la), 0.0))      # lijfas (van heup naar borst)
    fr = np.array((-math.cos(la), -math.sin(la), 0.0))     # voorkant (buik)
    bk = -fr                                                # rug
    hip = np.array((6.0, 30 * leg + 8 - crouch, 0))           # crouch: dieper door de knieën (sluipen)
    chest = hip + ax * 25
    m.axis = (hip, ax, fr)
    # lijf: één getaperde buis, smal bekken, iets voller onder de borst (foto 12: peer, maar slank: krabbeneter)
    bk_ = body_k
    m.tube([(*(hip - ax * 2), np.array((7.4, 7.4, 7.0)) * bk_), (*(hip + ax * 6), np.array((8.8, 8.8, 8.2)) * bk_ * 1.03),
            (*(hip + ax * 15), np.array((9.8, 9.8, 8.8)) * bk_), (*chest, np.array((10.0, 10.0, 9.2)) * bk_),
            (*(chest + ax * 6), np.array((8.0, 8.0, 7.8)) * (1 + (bk_ - 1) * 0.5))], 'body')
    # buidel op de rug: omgekeerde kangoeroebuidel, opening naar de schouders, groeit geleidelijk uit de rug
    Rp = P.rot_z(la)                       # lange as langs de lijfas
    zp = np.array((0, 0, pouch_z))   # pouch_z > 0: zak schuift iets naar de nabije flank (zichtbaar in driekwart)
    m.ell(hip + ax * 8 + bk * (7.0 * bk_ + pouch_k) + zp, np.array((6.6 + pouch_k, 8.5 + pouch_k, 8.6 + pouch_k * 0.6)), 'pouch', Rp)
    m.ell(hip + ax * 15 + bk * (6.4 * bk_ + pouch_k * 0.8) + zp * 0.8, np.array((5.6 + pouch_k * 0.6, 7.5 + pouch_k * 0.6, 7.6 + pouch_k * 0.4)), 'pouch', Rp)
    m.ell(hip + ax * (20.5 + pouch_k * 0.6) + bk * (9.6 * bk_ + pouch_k * 0.9) + zp * 0.8, (1.6, 1.4, 6.2 + pouch_k * 0.4), 'lip', Rp)   # opening (plooi)
    # nek en kop: kop naar voren, kijkt naar de speler
    neck = chest + ax * 6 + fr * 1.5
    hc = neck + np.array((-6.0, 7.5, 0)) * hs
    h0 = len(m.parts)
    m.ell(hc, np.array((10.5, 9.0, 10.0)) * hs, 'head')
    m.ell(hc + np.array((2.5, -2.5, 0)) * hs, np.array((8.5, 7.0, 9.5)) * hs, 'head')       # wangen/kaak breed
    m.tube([(*(hc + np.array((-6, -3.0, 0)) * hs), 6.2 * hs), (*(hc + np.array((-12, -4.4, 0)) * hs), 4.0 * hs),
            (*(hc + np.array((-15.5, -5.2, 0)) * hs), 2.8 * hs)], 'head', 0.5)
    m.ell(hc + np.array((-17.6, -4.9, 0)) * hs, np.array((1.9, 1.7, 2.3)) * hs, 'nose')
    eyes = []
    for sz in (1, -1):
        e = hc + np.array((-8.6, 1.2, 4.4 * sz)) * hs
        eyes.append(e)
        m.ell(e, 1.7 * hs, 'eye')
        m.ell(e + np.array((-0.6, 0.6, 0.9 * sz)) * hs, 0.55 * hs, 'glint')
    for sz in (1, -1):   # oren: rond, rechtop, witte rand (foto 11, illustratie)
        b = hc + np.array((3.0, 7.8, 6.2 * sz)) * hs
        Re = P.rot_x(math.radians(-22 * sz)) @ P.rot_y(math.radians(-25 * sz))
        m.ell(b, np.array((1.6, 5.0, 4.4)) * hs, 'earin', Re)
        m.ell(b + Re @ np.array((0.9, -0.2, 0)) * hs, np.array((1.4, 4.4, 3.6)) * hs, 'ear', Re)
    piv = neck.copy()
    Rh = P.rot_y(math.radians(head_extra)) @ P.rot_z(math.radians(-8 + head_down))
    m.parts[h0:] = [(piv + Rh @ (c - piv), r, Rh @ R0, g) for c, r, R0, g in m.parts[h0:]]
    m.head = dict(c=piv + Rh @ (hc - piv), R=Rh, hs=hs, eyes=[piv + Rh @ (e - piv) for e in eyes])
    # benen: Weavile-lengte, knie naar voren, hiel naar achteren, voet plat (plantigraad)
    for sz, gl in ((1, ''), (-1, 'far')):
        dx = near_back if sz > 0 else 7
        h = hip + np.array((0, -1, 5.5 * sz * bk_))
        kn = np.array((-9 + dx - crouch * 0.6, 19 * leg + 3 - crouch * 0.5, 7.0 * sz))
        hl = heel if sz > 0 else heel_far
        an = np.array((6 + dx, 4.5 + hl, 6.0 * sz))   # heel: hiel van de grond (stap, foto 10)
        m.tube([(*(h + np.array((1, 1, 0))), 7.4 * leg_k), (*(h * 0.45 + kn * 0.55), 6.2 * leg_k), (*kn, 4.6 * leg_k)], 'farthigh' if gl else 'thigh')
        m.tube([(*kn, 4.4 * leg_k * shin_k), (*an, 3.4 * leg_k * shin_k)], FAR['limb'] if gl else 'limb')
        fk = (0.5 + leg_k / 2) * (0.5 + shin_k / 2)
        if hl:                   # op de tenen: voet schuin naar voren-omlaag
            toe = an + np.array((-5.5, -hl + 1.2, 0))
            m.tube([(*an, 3.0 * fk), (*toe, 2.2 * fk)], FAR['limb'] if gl else 'limb', 0.5)
            m.ell(toe + np.array((-1.5, 0, 0)), np.array((3.0, 1.8, 3.2)) * fk, FAR['limb'] if gl else 'limb')
        else:
            m.ell(an + np.array((-4.5 * leg_k, -1.6, 0)), np.array((6.8, 2.4, 3.6)) * fk, FAR['limb'] if gl else 'limb')
    # armen: komen uit de schouders (schouderbol op de flank), bovenarm in vachtkleur, onderarm + hand donker
    sh_n = chest + np.array((0, 1.0, 7.6 * bk_)); sh_f = chest + np.array((2.5, 0.0, -7.6 * bk_))
    m.ell(sh_n, (5.4, 6.2, 4.4), 'body')
    if armen == 'sluip':        # sluiphandjes: hand op borsthoogte, pols geknikt, klauwen hangen (Sly)
        el = sh_n + np.array((-1.0, -8.0, 4.0)); wr = el + np.array((-7.0, 4.0, 1.0))
        cd, cb = (-0.8, 0.15, -0.55), (0, -1, 0)
    elif near_arm == 'hoog':      # actief: elleboog naar achter-onder, onderarm schuin omhoog naar voren, koevoet vooruit
        el = sh_n + np.array((-2.0, -10.0, 4.0)); wr = el + np.array((-11.0, 5.5, 1.5))
        cd, cb = (-0.8, 0.15, -0.55), (0, -1, 0)      # dwars in beeld bij draai 35-50°: koevoet in profiel
    else:                       # hangend voor de borst (foto 10)
        el = sh_n + np.array((-4.0, -10.0, 4.0)); wr = el + np.array((-7.0, -4.0, 0.5))
        cd, cb = (-0.6, -1, 0.1), (-1, 0.3, 0)
    m.tube([(*sh_n, 4.8), (*el, 4.0)], 'body')
    m.tube([(*el, 3.8), (*wr, 3.1)], 'limb')
    m.ell(wr + unit(wr - el) * 1.5, (3.2, 2.8, 3.2), 'limb')
    if klauw == 'paar':
        klauwpaar(m, wr + unit(wr - el) * 1.5, (-0.55, -0.85, 0.1) if armen == 'sluip' else unit(wr - el), (0, -1, 0), 'claw', klauw_s)
    else:
        koevoet(m, wr + unit(wr - el) * 2.5, cd, cb, 'claw', steel=steel)
    elf = sh_f + np.array((-3.0, -10.5, -2.0)); wrf = elf + np.array((-8.0, -3.5, 1.0))
    if armen == 'sluip':
        elf = sh_f + np.array((-2.0, -8.5, -2.0)); wrf = elf + np.array((-7.0, 4.0, 1.0))   # verre arm: lager, klauw omlaag-voor
    m.tube([(*sh_f, 4.4), (*elf, 3.8)], 'far')
    m.tube([(*elf, 3.6), (*wrf, 3.0)], 'farlimb')
    m.ell(wrf + unit(wrf - elf) * 1.5, (3.0, 2.6, 3.0), 'farlimb')
    if klauw == 'paar':
        klauwpaar(m, wrf + unit(wrf - elf) * 1.5, (-0.55, -0.85, 0.1) if armen == 'sluip' else unit(wrf - elf) * np.array((1, 0.3, 1)), (0, -1, 0), 'farclaw', klauw_s)
    else:
        koevoet(m, wrf + unit(wrf - elf) * 2.4, (-0.6, -0.7, -0.5), (-0.6, 0.6, 0.5), 'farclaw', 0.95, steel=steel)
    # staart: geringd, laag naar achteren, eind in een haak omhoog (Sly-knipoog)
    base = hip + bk * 4 + np.array((3, -3, -1))
    pts = [(*base, 5.4), (base[0] + 10, base[1] - 7, -3, 5.8), (base[0] + 21, base[1] - 9, -5, 5.6),
           (base[0] + 31, base[1] - 5, -5, 5.0), (base[0] + 37, base[1] + 4, -4, 4.4), (base[0] + 37, base[1] + 12, -3, 3.8),
           (base[0] + 34, base[1] + 17, -2, 3.4), (base[0] + 29, base[1] + 17, -1.5, 3.0), (base[0] + 26, base[1] + 12.5, -1, 2.6),
           (base[0] + 26.5, base[1] + 9, -1, 2.2)]
    m.tube(pts, 'tailL', 0.6, gfun=lambda s: 'tailD' if (s // 6.5) % 2 == 1 or s > 64 else 'tailL')
    return m


def render(m, yaw, pitch, scale, center):
    Rc = P.rot_x(math.radians(pitch)) @ P.rot_y(math.radians(yaw))
    zbuf = np.full((R, R), -1e9, np.float32); gid = np.full((R, R), -1, np.int16)
    nrm = np.zeros((R, R, 3), np.float32); wpt = np.zeros((R, R, 3), np.float32); groups = list(COL)
    ys, xs = np.mgrid[0:R, 0:R]
    wx = (xs - R / 2) / scale + center[0]; wy = -((ys - R / 2) / scale) + center[1]
    for c, r, R0, g in m.parts:
        cw = Rc @ c
        M = np.diag(1 / r) @ R0.T @ Rc.T
        ext = r.max()
        x0 = int(max(0, (cw[0] - ext - center[0]) * scale + R / 2 - 2)); x1 = int(min(R, (cw[0] + ext - center[0]) * scale + R / 2 + 3))
        y0 = int(max(0, (-(cw[1] + ext) + center[1]) * scale + R / 2 - 2)); y1 = int(min(R, (-(cw[1] - ext) + center[1]) * scale + R / 2 + 3))
        if x0 >= x1 or y0 >= y1:
            continue
        px = wx[y0:y1, x0:x1] - cw[0]; py = wy[y0:y1, x0:x1] - cw[1]
        a = M[:, 0, None, None] * px + M[:, 1, None, None] * py
        b = M[:, 2]; A = b @ b
        B = 2 * (a * b[:, None, None]).sum(0); C = (a * a).sum(0) - 1
        disc = B * B - 4 * A * C; hit = disc >= 0
        z = (-B + np.sqrt(np.where(hit, disc, 0))) / (2 * A) + cw[2]
        sub = zbuf[y0:y1, x0:x1]; win = hit & (z > sub)
        sub[win] = z[win]; gid[y0:y1, x0:x1][win] = groups.index(g)
        p = np.stack([px, py, z - cw[2]], -1)
        n = p @ (M.T @ M).T
        n /= np.linalg.norm(n, axis=-1, keepdims=True) + 1e-9
        nrm[y0:y1, x0:x1][win] = n[win]
        wpt[y0:y1, x0:x1][win] = np.stack([wx[y0:y1, x0:x1], wy[y0:y1, x0:x1], z], -1)[win]
    gi = groups.index
    # buik/borst geelbruin (foto 2, 10): voorkant van de lijfbuis
    hip, ax, fr = m.axis
    for gb, gl in (('body', 'belly'), ('far', 'farbelly')):
        sel = gid == gi(gb)
        q = wpt[sel] @ Rc
        rel = q - hip
        off = rel - np.outer(rel @ ax, ax)
        t = rel @ ax
        on = np.linalg.norm(off, axis=1) + 1e-6
        bel = ((off @ fr) / on > 0.62 + 1.3 * ((t - 20) / 13) ** 2) & (on < 12.5)   # ovale lichte buik, geen rechthoek
        g = gid[sel]; g[bel] = gi(gl); gid[sel] = g
    # kop: masker over de ogen en de neusrug (houdt achter het oog op), witte wenkbrauwband, witte snuitrand en kaak
    h = m.head
    sel = gid == gi('head')
    q = (wpt[sel] @ Rc - h['c']) @ h['R'] / h['hs']          # kop-lokale coördinaten
    de = np.min([np.linalg.norm((wpt[sel] @ Rc) - e, axis=1) for e in h['eyes']], axis=0) / h['hs']
    x, y, z = q[:, 0], q[:, 1], q[:, 2]
    g = gid[sel]
    white = ((y > 2.6) & (y < 5.4) & (x < -3.5) & (np.abs(z) > 1.8) & (x > -11.5)) \
        | ((y < -3.6) & (x < -6.5)) | ((y < -1.5) & (x < -12))
    mask = ((de < 3.6) | ((y > -3.6) & (y < 2.6) & (x < -5.2) & (x > -10.8))
            | ((np.abs(z) < 2.4) & (y > -3.6) & (x <= -10.8))) & (x < -4.6)
    g[white] = gi('white'); g[mask] = gi('mask')
    gid[sel] = g
    return zbuf, gid, nrm, groups


def shade(zbuf, gid, nrm, groups, out=256):
    a = gid >= 0
    rgb = np.ones((R, R, 3), np.float32) * 255
    Lt = np.array((-0.45, 0.65, 0.62)); Lt /= np.linalg.norm(Lt)
    lit = (nrm @ Lt) > -0.15
    for i, g in enumerate(groups):
        mm = gid == i; col = P.hexc(COL[g]); rgb[mm] = col
        if g not in NOSHADE:
            rgb[mm & ~lit] = col * 0.78
    edge = np.zeros((R, R), bool); z = np.where(a, zbuf, -1e9)
    lined = np.isin(gid, [groups.index(g) for g in LINED])
    for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):
        z2 = np.roll(np.roll(z, -dy, 0), -dx, 1); g2 = np.roll(np.roll(gid, -dy, 0), -dx, 1); l2 = np.roll(np.roll(lined, -dy, 0), -dx, 1)
        e = (np.abs(z - z2) > 4.5) | ((gid != g2) & (lined | l2))
        edge |= e; edge |= np.roll(np.roll(e, dy, 0), dx, 1)
    for _ in range(2):
        edge = edge | np.roll(edge, 1, 0) | np.roll(edge, 1, 1)
    inner = a.copy()
    for _ in range(7):
        inner = inner & np.roll(inner, 1, 0) & np.roll(inner, -1, 0) & np.roll(inner, 1, 1) & np.roll(inner, -1, 1)
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
    """Kophoogte (oren tot kin) / totale hoogte (FAKEMON_CHECKLIST D2)."""
    Rc = P.rot_x(math.radians(pitch)) @ P.rot_y(math.radians(yaw))
    yy = [((Rc @ c)[1] - r.max(), (Rc @ c)[1] + r.max(), g) for c, r, R0, g in m.parts]
    lo, hi = min(v[0] for v in yy), max(v[1] for v in yy)
    hd = [v for v in yy if v[2] in ('head', 'ear', 'earin', 'eye', 'nose')]
    return (max(v[1] for v in hd) - min(v[0] for v in hd)) / (hi - lo)


def sprite_ref(naam, out=200):
    im = Image.open(os.path.join(HERE, f'../../../../../graphics/pokemon/{naam}/anim_front.png'))
    t = tuple(im.getpalette()[:3]); im = im.convert('RGBA').crop((0, 0, 64, 64))
    px = im.load()
    for yy in range(64):
        for xx in range(64):
            if px[xx, yy][:3] == t:
                px[xx, yy] = (255, 255, 255, 255)
    return im.resize((out, out), Image.NEAREST).convert('RGB')


POSES = {   # Jordi: op 2 poten voorover (Gumshoos-houding, Weavile-beenlengte), één arm actief iets hoger
    'P1': dict(lean=35, near_arm='hoog'),
    'P2': dict(lean=50, near_arm='hoog'),
    'P3': dict(lean=50, near_arm='laag'),
}
YAWS = (20, 35, 50)


def vel(naam='vel_v2_ronde1.png'):
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
    ref = os.path.join(HERE, '../referenties')
    cell = 262
    im = Image.new('RGB', (12 + cell * 4, 44 + (cell + 24) * len(POSES)), 'white'); d = ImageDraw.Draw(im)
    d.text((12, 12), 'Wasbeer 3D-ontwerp v2: pose (rij) x draaiing naar de speler (kolom). Rechts: bronnen', font=FB, fill=(30, 30, 30))
    for r, (k, v) in enumerate(POSES.items()):
        m = wasbeer(**v)
        for c, yaw in enumerate(YAWS):
            img, al = view(m, yaw)
            x, y = 12 + cell * c, 44 + (cell + 24) * r
            im.paste(img, (x, y))
            bb = Image.fromarray((al * 255).astype(np.uint8)).resize(img.size).getbbox()   # 1x-voorbeeld (±60 px hoog)
            s1 = img.crop(bb); f1 = 60 / max(s1.size)
            s1 = s1.resize((max(1, round(s1.width * f1)), max(1, round(s1.height * f1))), Image.LANCZOS)
            im.paste(s1, (x + 256 - s1.width, y + 256 - s1.height))
            d.text((x + 4, y + 258), f'{k}{c + 1}: romp {v["lean"]}°, draai {yaw}°, kop {kopaandeel(m, yaw):.0%}', font=F, fill=(60, 60, 60))
    x = 12 + cell * 3
    foto = Image.open(os.path.join(ref, 'foto10_staand_reikend.jpg')).convert('RGB').transpose(Image.FLIP_LEFT_RIGHT)
    foto.thumbnail((256, 236)); im.paste(foto, (x, 44)); d.text((x + 4, 44 + 258), 'foto 10 (gespiegeld)', font=F, fill=(60, 60, 60))
    im.paste(sprite_ref('gumshoos', 236), (x, 44 + cell + 24)); d.text((x + 4, 44 + 2 * cell + 26), 'Gumshoos (houding)', font=F, fill=(60, 60, 60))
    im.paste(sprite_ref('weavile', 236), (x, 44 + 2 * (cell + 24))); d.text((x + 4, 44 + 3 * cell + 50), 'Weavile (beenlengte)', font=F, fill=(60, 60, 60))
    im.save(os.path.join(HERE, naam))


NIEUW = dict(near_arm='hoog', leg=0.8, leg_k=0.8, steel=5.5)   # Jordi over P13: klauwen kort, pootjes stomper en dunner


def vel2(naam='vel_v2_ronde2.png', yaw=50):
    """Ronde 2 rond P13 (Jordi): rij 1 romp (menselijker = rechter), rij 2 lijfdikte (zoals de foto)."""
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
    ref = os.path.join(HERE, '../referenties')
    cell = 262
    rijen = [[('P13 (ronde 1)', dict(POSES['P1'])), ('A: romp 30°, lijf 1,12', dict(NIEUW, lean=30, body_k=1.12)),
              ('B: romp 22°, lijf 1,12', dict(NIEUW, lean=22, body_k=1.12))],
             [('C: romp 26°, lijf 1,06', dict(NIEUW, lean=26, body_k=1.06)), ('D: romp 26°, lijf 1,14', dict(NIEUW, lean=26, body_k=1.14)),
              ('E: romp 26°, lijf 1,22', dict(NIEUW, lean=26, body_k=1.22))]]
    im = Image.new('RGB', (12 + cell * 4, 44 + (cell + 24) * 2), 'white'); d = ImageDraw.Draw(im)
    d.text((12, 12), f'Wasbeer 3D-ontwerp v2 ronde 2 (rond P13, draai {yaw}°): korte klauwen, stompere pootjes', font=FB, fill=(30, 30, 30))
    for r, rij in enumerate(rijen):
        for c, (lab, v) in enumerate(rij):
            m = wasbeer(**v); img, al = view(m, yaw)
            x, y = 12 + cell * c, 44 + (cell + 24) * r
            im.paste(img, (x, y))
            bb = Image.fromarray((al * 255).astype(np.uint8)).resize(img.size).getbbox()
            s1 = img.crop(bb); f1 = 60 / max(s1.size)
            s1 = s1.resize((max(1, round(s1.width * f1)), max(1, round(s1.height * f1))), Image.LANCZOS)
            im.paste(s1, (x + 256 - s1.width, y + 256 - s1.height))
            d.text((x + 4, y + 258), f'{lab}, kop {kopaandeel(m, yaw):.0%}', font=F, fill=(60, 60, 60))
    x = 12 + cell * 3
    for r, (f, lab) in enumerate((('foto10_staand_reikend.jpg', 'foto 10 (gespiegeld)'), ('foto12_rechtop_driekwart_lijf.png', 'foto 12 (lijfdikte)'))):
        foto = Image.open(os.path.join(ref, f)).convert('RGB')
        if r == 0:
            foto = foto.transpose(Image.FLIP_LEFT_RIGHT)
        foto.thumbnail((256, 236)); y = 44 + (cell + 24) * r
        im.paste(foto, (x, y)); d.text((x + 4, y + 258), lab, font=F, fill=(60, 60, 60))
    im.save(os.path.join(HERE, naam))


E = dict(NIEUW, lean=26, body_k=1.22)     # Jordi: "E is wel oke"


def vel3(naam='vel_v2_ronde3.png', yaw=50):
    """Ronde 3 op E (Jordi): voorste been verder naar achteren (niet houterig naast elkaar), onderbenen dunner."""
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
    ref = os.path.join(HERE, '../referenties')
    cell = 262
    rij = [('E (ronde 2)', dict(E)),
           ('E1: been 7 terug, onderbeen dun', dict(E, near_back=7, shin_k=0.7)),
           ('E2: been 12 terug, op de tenen', dict(E, near_back=12, shin_k=0.7, heel=5)),
           ('E3: als E2, onderbeen dunner', dict(E, near_back=12, shin_k=0.58, heel=5))]
    im = Image.new('RGB', (12 + cell * 4, 44 + (cell + 24) * 2), 'white'); d = ImageDraw.Draw(im)
    d.text((12, 12), f'Wasbeer 3D-ontwerp v2 ronde 3 (E, draai {yaw}°): benen niet naast elkaar, dunne onderbenen', font=FB, fill=(30, 30, 30))
    for c, (lab, v) in enumerate(rij):
        m = wasbeer(**v); img, al = view(m, yaw)
        x, y = 12 + cell * c, 44
        im.paste(img, (x, y))
        bb = Image.fromarray((al * 255).astype(np.uint8)).resize(img.size).getbbox()
        s1 = img.crop(bb); f1 = 60 / max(s1.size)
        s1 = s1.resize((max(1, round(s1.width * f1)), max(1, round(s1.height * f1))), Image.LANCZOS)
        im.paste(s1, (x + 256 - s1.width, y + 256 - s1.height))
        d.text((x + 4, y + 258), lab, font=F, fill=(60, 60, 60))
    y = 44 + cell + 24
    for c, (f, lab, flip) in enumerate((('foto10_staand_reikend.jpg', 'foto 10 (gespiegeld)', True), ('foto3_zijaanzicht_lopend.webp', 'foto 3 (onderbenen)', False),
                                         ('foto9_zijaanzicht_sluipend.webp', 'foto 9 (onderbenen)', False), ('foto7_frontaal_lange_poten.png', 'foto 7', False))):
        foto = Image.open(os.path.join(ref, f)).convert('RGB')
        if flip:
            foto = foto.transpose(Image.FLIP_LEFT_RIGHT)
        foto.thumbnail((256, 236)); x = 12 + cell * c
        im.paste(foto, (x, y)); d.text((x + 4, y + 258), lab, font=F, fill=(60, 60, 60))
    im.save(os.path.join(HERE, naam))


E2R = dict(E, near_back=12, shin_k=0.7, heel=5, pouch_k=3, pouch_z=4, klauw='paar', klauw_s=1.2)   # bevroren: E2 + rugzak + klauw
SLUIP = [('E2 (nu)', dict(E2R)),
         ('S1: dieper, op de tenen', dict(E2R, lean=36, crouch=5, heel_far=4)),
         ('S2: S1 + sluiphandjes', dict(E2R, lean=36, crouch=5, heel_far=4, armen='sluip')),
         ('S3: laag sluipen, kop omlaag', dict(E2R, lean=46, crouch=8, heel_far=4, armen='sluip', head_down=10))]


def vel_sluip(naam='vel_sluip.png', yaw=50):
    """Jordi: "kan de pose nog iets meer 'in de nacht sluipen' zijn?" """
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
    cell = 262
    im = Image.new('RGB', (12 + cell * 4, 44 + cell + 24), 'white'); d = ImageDraw.Draw(im)
    d.text((12, 12), 'Wasbeer: meer in de nacht sluipen (draai 50°)', font=FB, fill=(30, 30, 30))
    for c, (lab, v) in enumerate(SLUIP):
        m = wasbeer(**v); img, al = view(m, yaw)
        x, y = 12 + cell * c, 44
        im.paste(img, (x, y))
        bb = Image.fromarray((al * 255).astype(np.uint8)).resize(img.size).getbbox()
        s1 = img.crop(bb); f1 = 60 / max(s1.size)
        s1 = s1.resize((max(1, round(s1.width * f1)), max(1, round(s1.height * f1))), Image.LANCZOS)
        im.paste(s1, (x + 256 - s1.width, y + 256 - s1.height))
        d.text((x + 4, y + 258), lab, font=F, fill=(60, 60, 60))
    im.save(os.path.join(HERE, naam))


if __name__ == '__main__':
    if sys.argv[1:2] == ['ronde1']:
        vel()
    elif sys.argv[1:2] == ['ronde2']:
        vel2()
    elif sys.argv[1:2] == ['ronde3']:
        vel3()
    else:
        vel_sluip()
