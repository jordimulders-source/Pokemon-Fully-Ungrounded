"""Great potoo (Ghost/Normal): 3D-poppetje in de stijl van het lama-poppetje (lama/ontwerp/pop3d_lama.py):
vlakke kleuren, één schaduwtoon, donkere lijn waar de diepte verspringt. Praatplaat + bron voor het silhouet.

Verschil met de lama-renderer: naast losse ellipsoïden kent deze renderer *volumes met snijvlakken en holtes*
(een ellipsoïde ∩ halfruimtes − holtes). Zo is de open bek één echte, holle onderkaak (een schaal die om het
scharnier is opengeklapt) en geen losse stokjes of schijfjes: de mondkleur zit alleen op de binnenwand.

Maat: oogstraal = 1 (r_e). Diercoördinaten: x = naar achteren, y = omhoog, z = zijwaarts (naar de kijker bij yaw 0,
dan zie je de flank met de snavel naar links). yaw > 0 draait het gezicht naar de kijker.
Bronnen: alleen Jordi's 5 foto's (SPEC); maten in NOTITIES.md.
Draaien vanuit de repo-root: python3 docs/concept/sprites/potoo/poppetje/pop3d_potoo.py"""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, '../referenties')
R = 768
LINE = np.array((40, 34, 54), np.uint8)
COL = {
    'fur': '#F1EFF6', 'wing': '#E1DDEB', 'far': '#CFCADC', 'tail': '#D9D4E4', 'bark': '#B3A9C2',
    'eye': '#09080D', 'rim': '#C4BCD6', 'hook': '#4A4258', 'tip': '#7A7290',
    'mouth': '#7A68DE', 'palate': '#6656C8', 'throat': '#2B2163', 'brow': '#CCC5DC',
}
NOSHADE = {'eye', 'throat'}
LINED = {'eye', 'hook', 'mouth', 'palate', 'throat', 'rim', 'tip'}
GROUPS = list(COL)


def hexc(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float32)


def rot_x(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def rot_y(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rot_z(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


# ---------------------------------------------------------------- volumes
def E(c, r, R0=None):
    """Voorwaarde 'binnen ellipsoïde'."""
    return ('E', np.array(c, float), np.array(r if np.ndim(r) else (r, r, r), float), np.eye(3) if R0 is None else R0)


def H(n, d):
    """Voorwaarde 'n·p <= d' (halfruimte)."""
    return ('P', np.array(n, float), float(d))


class Solid:
    """Convex volume (doorsnede van voorwaarden) min convexe holtes; star verplaatst met (Ro, t).
    faces: tag -> groep (tag i = voorwaarde i van het volume, 100*(k+1)+i = voorwaarde i van holte k).
    paint(tag, p_local) -> lijst groepsnamen (optioneel, overschrijft faces)."""

    def __init__(self, base, group, cavs=(), faces=None, paint=None, Ro=None, t=(0, 0, 0)):
        self.base, self.cavs, self.group = base, list(cavs), group
        self.faces, self.paint = faces or {}, paint
        self.Ro = np.eye(3) if Ro is None else np.array(Ro, float)
        self.t = np.array(t, float)

    def moved(self, Rm, piv):
        """Starre beweging om een draaipunt (dierruimte)."""
        piv = np.array(piv, float)
        self.Ro = Rm @ self.Ro
        self.t = piv + Rm @ (self.t - piv)
        return self


def interval(cond, A0, Bv):
    """Straal p(z) = A0 + z*Bv (lokaal). Geeft lo, hi (z-bereik binnen de voorwaarde) en hit."""
    if cond[0] == 'E':
        _, c, r, R0 = cond
        M = np.diag(1 / r) @ R0.T
        u0 = np.tensordot(A0 - c, M.T, axes=([-1], [0]))
        ub = M @ Bv
        A = ub @ ub
        B = 2 * (u0 @ ub)
        C = (u0 * u0).sum(-1) - 1
        disc = B * B - 4 * A * C
        hit = disc >= 0
        sq = np.sqrt(np.where(hit, disc, 0))
        return (-B - sq) / (2 * A), (-B + sq) / (2 * A), hit
    _, n, d = cond
    a = A0 @ n
    b = n @ Bv
    if abs(b) < 1e-9:
        ok = a <= d
        return np.where(ok, -1e9, 1e9), np.where(ok, 1e9, -1e9), ok
    zc = (d - a) / b
    if b > 0:
        return np.full_like(zc, -1e9), zc, np.ones_like(zc, bool)
    return zc, np.full_like(zc, 1e9), np.ones_like(zc, bool)


def conv(conds, A0, Bv):
    los, his, hits = zip(*[interval(c, A0, Bv) for c in conds])
    los, his = np.stack(los), np.stack(his)
    lo, hi = los.max(0), his.min(0)
    ok = np.logical_and.reduce(hits) & (lo < hi)
    return lo, hi, ok, los.argmax(0), his.argmin(0)


def normal(cond, p):
    if cond[0] == 'E':
        _, c, r, R0 = cond
        q = (p - c) @ R0
        return (q / r ** 2) @ R0.T
    return np.broadcast_to(cond[1], p.shape)


def render(solids, yaw, pitch, scale, center, res=R):
    Rc = rot_x(math.radians(pitch)) @ rot_y(math.radians(yaw))
    zbuf = np.full((res, res), -1e9, np.float32)
    gid = np.full((res, res), -1, np.int16)
    nrm = np.zeros((res, res, 3), np.float32)
    ys, xs = np.mgrid[0:res, 0:res]
    wx = (xs - res / 2) / scale + center[0]
    wy = -((ys - res / 2) / scale) + center[1]
    for s in solids:
        RR = Rc @ s.Ro                       # lokaal -> camera
        # begrenzing: eerste ellipsoïde van het volume
        e = next(c for c in s.base if c[0] == 'E')
        cw = RR @ e[1] + Rc @ s.t
        ext = e[2].max()
        x0 = int(max(0, (cw[0] - ext - center[0]) * scale + res / 2 - 2)); x1 = int(min(res, (cw[0] + ext - center[0]) * scale + res / 2 + 3))
        y0 = int(max(0, (-(cw[1] + ext) + center[1]) * scale + res / 2 - 2)); y1 = int(min(res, (-(cw[1] - ext) + center[1]) * scale + res / 2 + 3))
        if x0 >= x1 or y0 >= y1:
            continue
        q = np.stack([wx[y0:y1, x0:x1], wy[y0:y1, x0:x1], np.zeros((y1 - y0, x1 - x0))], -1)
        A0 = (q @ Rc - s.t) @ s.Ro           # lokaal punt bij z = 0
        Bv = s.Ro.T @ Rc.T @ np.array((0, 0, 1.0))
        lo, hi, ok, ilo, ihi = conv(s.base, A0, Bv)
        z = hi.copy()
        tag = ihi.astype(np.int32)
        cv = [conv(c, A0, Bv) for c in s.cavs]
        for _ in range(len(cv) + 1):
            for k, (clo, chi, cok, cilo, _) in enumerate(cv):
                inside = cok & (z > clo + 1e-6) & (z <= chi + 1e-6)
                z = np.where(inside, clo, z)
                tag = np.where(inside, 100 * (k + 1) + cilo, tag)
        ok &= z >= lo - 1e-6
        sub = zbuf[y0:y1, x0:x1]
        win = ok & (z > sub)
        if not win.any():
            continue
        sub[win] = z[win]
        P = A0[win] + z[win][:, None] * Bv
        T = tag[win]
        nl = np.zeros_like(P)
        for t_ in np.unique(T):
            m = T == t_
            if t_ < 100:
                nl[m] = normal(s.base[t_], P[m])
            else:
                nl[m] = -normal(s.cavs[t_ // 100 - 1][t_ % 100], P[m])
        nc = nl @ RR.T
        nc /= np.linalg.norm(nc, axis=1, keepdims=True) + 1e-9
        nrm[y0:y1, x0:x1][win] = nc
        if s.paint is not None:
            g = s.paint(T, P)
        else:
            g = [s.faces.get(int(t_), s.group) for t_ in T]
        gid[y0:y1, x0:x1][win] = [GROUPS.index(x) for x in g]
    return zbuf, gid, nrm


def shade(zbuf, gid, nrm, out=256, res=R, thr=1.1, dil=2, sil=7):
    a = gid >= 0
    rgb = np.ones((res, res, 3), np.float32) * 255
    Lt = np.array((-0.45, 0.65, 0.62)); Lt /= np.linalg.norm(Lt)
    lit = (nrm @ Lt) > -0.2
    for i, g in enumerate(GROUPS):
        mm = gid == i
        col = hexc(COL[g]); rgb[mm] = col
        if g not in NOSHADE:
            rgb[mm & ~lit] = col * 0.80
    edge = np.zeros((res, res), bool); z = np.where(a, zbuf, -1e9)
    lined = np.isin(gid, [GROUPS.index(g) for g in LINED])
    for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):
        z2 = np.roll(np.roll(z, -dy, 0), -dx, 1); g2 = np.roll(np.roll(gid, -dy, 0), -dx, 1); l2 = np.roll(np.roll(lined, -dy, 0), -dx, 1)
        soft = (gid == GROUPS.index('brow')) | (g2 == GROUPS.index('brow'))   # veertjes: geen losse lijnstukjes
        e = ((np.abs(z - z2) > thr) & ~soft) | ((gid != g2) & (lined | l2))
        edge |= e; edge |= np.roll(np.roll(e, dy, 0), dx, 1)
    for _ in range(dil):
        edge = edge | np.roll(edge, 1, 0) | np.roll(edge, 1, 1)
    inner = a.copy()
    for _ in range(sil):
        inner = inner & np.roll(inner, 1, 0) & np.roll(inner, -1, 0) & np.roll(inner, 1, 1) & np.roll(inner, -1, 1)
    edge = (edge & a) | (a & ~inner)
    rgb[edge] = LINE; rgb[~a] = 255
    return Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).resize((out, out), Image.LANCZOS)


# ---------------------------------------------------------------- het dier
P0 = dict(
    open_deg=62,       # hoe ver de onderkaak hangt
    eye_y=0.3,         # oog hoger op de koepel (Jordi: "de ogen moeten hoger")
    eye_r=1.25,        # oogstraal (Pokémon: iets groter dan 1)
    lean=12,           # voorover hangen
    body_k=0.85,       # lijf kleiner t.o.v. de kop (Pokémon)
    head_pitch=9,      # kop iets voorover: bovenrand daalt naar het haakje (close-up)
    xh=0.9, yh=-2.4,   # scharnier = mondhoek, recht onder het oog (zijfoto)
    tip=-6.6,          # haakje / kaakpunt vóór (bovenrand ±6 r_e lang, zijfoto)
    half=52,           # halve tophoek van de snavel van boven gezien
    jaw_extra=0.0,     # onderkaak langer dan de bovensnavel
    half_jaw=63,       # spitsere kaakpunt (close-up)
)


def lens(tip, corner, alpha, yc, ry, y_ref, k=0.0):
    """Twee grote, bijna verticale ellipsoïden waarvan de doorsnede (bovenaanzicht) een spitse boog is:
    punt bij tip (x), door de mondhoeken (corner = (x, z)), halve tophoek alpha. Op hoogte y_ref klopt de boog;
    hoger wordt hij breder (raakt de koepel niet), lager smaller. k = alles k naar binnen (holte)."""
    al = math.radians(alpha)
    tp = np.array((tip, 0.0)); c = np.array(corner, float)
    n = np.array((math.sin(al), -math.cos(al)))
    v = c - tp
    Rr = (v @ v) / (2 * (v @ n))
    ctr = tp + Rr * n
    R0 = Rr / math.sqrt(1 - ((y_ref - yc) / ry) ** 2)
    return [E((ctr[0], yc, ctr[1] * s), (R0 - k, ry - k, R0 - k)) for s in (1, -1)]


def leaf(c, ax, wd, a, b, th):
    """Veertje: spits blad (vesica) met halve lengte a, halve breedte b, dikte th; ax = lengterichting,
    wd = breedterichting. Doorsnede van twee ellipsoïden, dus twee spitse punten zonder losse stokjes."""
    ax = np.array(ax, float); ax /= np.linalg.norm(ax)
    wd = np.array(wd, float); wd -= ax * (wd @ ax); wd /= np.linalg.norm(wd)
    tz = np.cross(ax, wd)
    Rm = np.stack([ax, wd, tz], 1)
    Rr = (a * a + b * b) / (2 * b)
    c = np.array(c, float)
    return [E(c + wd * (Rr - b), (Rr, Rr, th), Rm), E(c - wd * (Rr - b), (Rr, Rr, th), Rm)]


def potoo(**kw):
    p = dict(P0, **kw)
    S = []
    xh, yh, tip = p['xh'], p['yh'], p['tip']
    tg = math.tan(math.radians(6))                          # gaplijn loopt licht op naar het haakje (leidraad)
    gy = lambda x: yh + (xh - x) * tg
    above = H((-tg, -1, 0), -yh - tg * xh)
    below = H((tg, 1, 0), yh + tg * xh)
    # --- kop: brede ronde koepel (kruin breed, iets plat) + 'gezicht' dat breed en plat naar het haakje loopt
    Ed = E((1.4, -0.4, 0), (4.9, 3.75, 5.15))
    Ec = E((1.3, 1.3, 0), (3.9, 2.3, 4.8))
    Ef = E((-0.9, -1.4, 0), (5.6, 3.15, 4.2))
    L = lambda k=0.0: lens(tip, (xh, 4.25), p['half'], 2.5, 9.0, yh, k)
    rimw = 0.30

    def paint_upper(T, P):
        g = np.array(['fur'] * len(T), object)
        h = P[:, 1] - gy(P[:, 0])
        f = np.clip((xh - P[:, 0]) / (xh - tip), 0, 1)
        g[(h < rimw + 0.75 * f ** 1.6) & (P[:, 0] < xh + 0.2)] = 'rim'     # bovensnavel: hoornrand, breder naar het haakje
        return list(g)
    Ec = E((1.5, 0.9, 0), (4.6, 2.45, 5.2))                  # brede kruin: kop wordt van voren iets 'vierkanter' (close-up)
    for Eb in (Ed, Ef, Ec):
        S.append(Solid([Eb, above] + L(), 'fur', paint=paint_upper))

    def surf(o, d):
        """Punt op de kop (koepel ∪ gezicht) vanuit o in richting d, met de normaal."""
        best = None
        for Eb in (Ed, Ef, Ec):
            u0, ub = (o - Eb[1]) / Eb[2], d / Eb[2]
            A, B, C = ub @ ub, 2 * u0 @ ub, u0 @ u0 - 1
            if B * B - 4 * A * C < 0:
                continue
            t = (-B + math.sqrt(B * B - 4 * A * C)) / (2 * A)
            if best is None or t > best[0]:
                q = o + d * t
                best = (t, q, (q - Eb[1]) / Eb[2] ** 2)
        return best[1], best[2] / np.linalg.norm(best[2])
    # --- ogen: enorm, bol, pikzwart, voor-opzij, hoog op de koepel
    eyes = []
    for sz in (1, -1):
        d = np.array((-0.76, 0.10, 0.64 * sz)); d /= np.linalg.norm(d)
        q, _ = surf(np.array((0.9, p['eye_y'], 0)), d)
        e = q + d * 0.05 * p['eye_r']
        eyes.append(e)
        S.append(Solid([E(e, p['eye_r'])], 'eye'))

    # --- veertjes tussen de ogen (close-up): wenkbrauwkam boven elk oog + rijen kleine spitse veertjes
    #     die van tussen de ogen naar het haakje wijzen en met de punt iets loskomen
    o = np.array((1.0, -0.6, 0))
    rows = [(-1.5, (0.0,), 1.0, 30), (-0.9, (-0.5, 0.5), 0.95, 24), (-0.25, (-0.95, 0.0, 0.95), 0.95, 16), (0.45, (-1.25, 1.25), 0.9, 10)]
    for el, zs, a, lift in rows:                       # el = hoogte van de rij (graden-achtig), zs = zijwaartse plek
        for zz in zs:
            d = np.array((-1.0, 0.36 + 0.33 * el + 0.25, zz * 0.30)); d /= np.linalg.norm(d)
            q, nn = surf(o, d)
            if q[1] - gy(q[0]) < 2.1:
                continue
            down = np.array((-0.55, -1.0, -0.22 * zz)); down -= nn * (down @ nn); down /= np.linalg.norm(down)
            ax = down * math.cos(math.radians(lift)) + nn * math.sin(math.radians(lift))   # punt komt iets los
            S.append(Solid(leaf(q + ax * a * 0.5 + nn * 0.04, ax, np.cross(nn, ax), a * 1.15, 0.2, 0.2), 'brow'))
    # haakje: klein, donker, krult omlaag over de punt
    hk = [(tip + 0.35, gy(tip) + 0.55, 0.42), (tip - 0.05, gy(tip) + 0.05, 0.38), (tip - 0.1, gy(tip) - 0.45, 0.30), (tip + 0.15, gy(tip) - 0.85, 0.18)]
    for (x0, y0, r0), (x1, y1, r1) in zip(hk, hk[1:]):
        for t in np.linspace(0, 1, 5):
            S.append(Solid([E((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, 0), (r0 + (r1 - r0) * t) * np.array((1, 1, 0.85)))], 'hook'))

    # --- onderkaak: holle schaal (gezicht onder de gaplijn, vóór het scharnier), opengeklapt om het scharnier
    # de onderkaak is iets langer dan de bovensnavel (leidraad: de kaak hangt ver omlaag; Jordi: overdreven grote bek)
    tj = tip - p['jaw_extra']
    Ej = E((Ef[1][0] - p['jaw_extra'] / 2 - 0.8, Ef[1][1], 0), Ef[2] + np.array((p['jaw_extra'] / 2 + 0.8, 0, 0)))   # lang: de lens maakt de punt
    Lj = lambda k=0.0: lens(tj, (xh, 4.25), p['half_jaw'], 2.5, 9.0, yh, k)
    inner = E(Ej[1] + np.array((-0.6, 0.45, 0)), Ej[2] - np.array((0.0, 0.55, 0.55)))

    def paint_jaw(T, P):
        g = np.array(['fur'] * len(T), object)
        h = gy(P[:, 0]) - P[:, 1]
        f = np.clip((xh - P[:, 0]) / (xh - tj), 0, 1)
        g[h < rimw + 0.35 * f] = 'rim'
        g[(P[:, 0] < tj + 1.6) & (T != 1)] = 'tip'
        g[T == 1] = 'rim'
        g[(P[:, 0] < tj + 0.9) & (T < 100)] = 'tip'                      # donkere kaakpunt (close-up)
        g[T >= 100] = 'mouth'
        tt = (P[:, 0] - (xh - 4.6)) / 2.6                                 # 0 = naar de punt, 1 = naar de keel
        v = (T >= 100) & (tt > 0) & (tt < 1) & (np.abs(P[:, 2]) < 0.55 * np.clip(tt, 0, 1) ** 1.3)   # donkere V-keel (close-up)
        g[v] = 'throat'
        return list(g)
    jaw = Solid([Ej, below, H((1, 0, 0), xh)] + Lj(), 'fur', cavs=[[inner] + Lj(0.5)], paint=paint_jaw)
    jaw.moved(rot_z(math.radians(p['open_deg'])), (xh, yh, 0))
    S.append(jaw)

    # --- keel: onder de gaplijn achter het scharnier; voorvlak = achterwand van de muil met donkere keel
    def paint_throat(T, P):
        g = np.array(['fur'] * len(T), object)
        f = T == 2
        g[f] = 'mouth'
        g[f] = 'palate'
        g[f & ((P[:, 2] / 0.75) ** 2 + ((P[:, 1] - (yh - 1.6)) / 1.35) ** 2 < 1)] = 'throat'
        return list(g)
    inL = Lj(0.5)

    def paint_cheek(T, P):
        g = np.array(['fur'] * len(T), object)
        f = T == 2
        ins = np.ones(len(T), bool)
        for c in [inner] + inL:
            ins &= ((((P - c[1]) @ c[3]) / c[2]) ** 2).sum(1) < 1
        gap = ((P[:, 2] / 3.2) ** 2 + ((P[:, 1] - (yh - 1.2)) / 1.35) ** 2 < 1) & (P[:, 1] < yh - 0.1)
        g[f & (ins | gap)] = 'mouth'
        
        return list(g)
    for Eb in (Ed, Ef, E((2.4, -4.6, 0), (3.4, 3.2, 4.4))):
        S.append(Solid([Eb, below, H((-1, 0, 0), -xh)], 'fur', paint=paint_cheek))

    for s_ in S:
        s_.moved(rot_z(math.radians(p['head_pitch'])), (xh, yh, 0))
    # --- lijf: rechtop, taps; schouders/vleugels hoog naast de kop, geen hals ----------------------------
    body = []
    sp_body = streaks('fur', [((2.4, -11.0), (3.4, -15.5), 0.55, 1)])
    sp_wing = streaks('wing', [((4.6, -5.6), (6.2, -11.8), 0.6, 1), ((7.6, -8.8), (8.2, -12.6), 0.42, 1)])
    sp_far = streaks('far', [((5.2, -6.5), (6.4, -11.0), 0.5, -1)])
    sp_pen = streaks('wing', [((6.0, -14.0), (6.9, -18.5), 0.4, 1)])
    body.append(Solid([E((5.0, -10.0, 0), (4.6, 8.6, 6.0))], 'fur', paint=sp_body))         # peervormig lijf: breed onder de kop
    body.append(Solid([E((5.4, -16.0, 0), (3.2, 3.8, 4.2))], 'fur'))         # onderlijf, op de (onzichtbare) tak
    for sz in (1, -1):
        g = 'wing' if sz > 0 else 'far'
        body.append(Solid([E((6.0, -7.6, 4.7 * sz), (3.4, 7.6, 1.9), rot_z(math.radians(-5)))], g, paint=sp_wing if sz > 0 else sp_far))    # gevouwen vleugel, schouder hoog
        body.append(Solid([E((6.6, -15.4, 3.4 * sz), (2.3, 5.2, 1.5), rot_z(math.radians(-8)))], g, paint=sp_pen if sz > 0 else None))   # slagpennen, taps naar de staart
    body.append(Solid([E((7.2, -20.5, 0), (1.3, 6.0, 2.5), rot_z(math.radians(-8)))], 'tail'))        # lange platte staart
    # Pokémon-verhouding: kop/ogen/bek groot, lijf iets kleiner dan echt (schaal om de schouder)
    k, o = p['body_k'], np.array((3.5, -3.0, 0))
    for b in body:
        b.base = [(c[0], o + (c[1] - o) * k, c[2] * k, c[3]) for c in b.base]
        if b.paint is not None:
            b.paint = _scaled(b.paint, o, k)
    if p.get('body', 1):
        S += body
    # alles licht voorover (om de 'tak' onder het lijf)
    piv = (2.5, -17, 0)
    Rl = rot_z(math.radians(p['lean']))
    for s in S:
        s.moved(Rl, piv)
    return S


def streaks(base, lst):
    """Schorsvlekken (Hisui-Zorua-idee): een paar langgerekte, getande vegen in de veerrichting.
    lst: (a, b, breedte, zijde) met a, b = (x, y) in lokale coördinaten; zijde = +1/-1 (z-kant) of 0 (beide)."""
    def paint(T, P):
        g = np.array([base] * len(T), object)
        for (a, b, w, side) in lst:
            a, b = np.array(a, float), np.array(b, float)
            v = b - a
            t = np.clip(((P[:, :2] - a) @ v) / (v @ v), 0, 1)
            d = np.linalg.norm(P[:, :2] - (a + t[:, None] * v), axis=1)
            ww = w * np.sin(np.pi * t) ** 0.55 * (1 + 0.28 * np.sin(11 * t + 3 * a[0]))
            ok = (P[:, 2] * side > 0.5) if side else (np.abs(P[:, 2]) > 0.5)
            g[(d < ww) & ok] = 'bark'
        return list(g)
    return paint


def _scaled(paint, o, k):
    return lambda T, P: paint(T, o + (P - o) / k)


def _frame(ax):
    """Rotatie met lokale x langs ax."""
    ax = ax / np.linalg.norm(ax)
    up = np.array((0, 0, 1.0)) if abs(ax[2]) < 0.9 else np.array((0, 1.0, 0))
    yv = np.cross(up, ax); yv /= np.linalg.norm(yv)
    zv = np.cross(ax, yv)
    return np.stack([ax, yv, zv], 1)


# ---------------------------------------------------------------- beelden
def extent(solids, yaw, pitch):
    Rc = rot_x(math.radians(pitch)) @ rot_y(math.radians(yaw))
    pts, rs = [], []
    for s in solids:
        e = next(c for c in s.base if c[0] == 'E')
        pts.append(Rc @ (s.Ro @ e[1] + s.t)); rs.append(e[2].max())
    pts, rs = np.array(pts), np.array(rs)
    return pts, rs


def view(solids, yaw, pitch=8, size=236, out=256, focus=None):
    """focus = (cx, cy, halve breedte) in schermcoördinaten voor een ingezoomde kop."""
    if focus is None:
        # hele dier (begrenzing van de hoofdvolumes; de grote lens-bollen tellen niet mee)
        pts, rs = extent(solids, yaw, pitch)
        x0, x1, y0, y1 = (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()
        scale = R * (size / 256) / max(x1 - x0, y1 - y0)
        c = ((x0 + x1) / 2, (y0 + y1) / 2)
    else:
        c = focus[:2]; scale = R / (2 * focus[2])
    return shade(*render(solids, yaw, pitch, scale, c), out=out)


def head_focus(solids, yaw, pitch=8, half=8.0):
    Rc = rot_x(math.radians(pitch)) @ rot_y(math.radians(yaw))
    s = solids[0]
    c = Rc @ (s.Ro @ np.array((-0.6, -2.4, 0)) + s.t)
    return (c[0], c[1], half)


def foto(naam, box=None, maxwh=(300, 300)):
    im = Image.open(os.path.join(REF, naam)).convert('RGB')
    if box:
        im = im.crop(box)
    im.thumbnail(maxwh)
    return im


def vel(naam='vel_ronde1.png', titel='ronde 1', **kw):
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
    m = potoo(**kw)
    W = 1340
    im = Image.new('RGB', (W, 1420), 'white')
    d = ImageDraw.Draw(im)
    lab = lambda x, y, t: d.text((x, y), t, font=F, fill=(60, 60, 60))
    d.text((12, 8), f'Great potoo (Ghost/Normal): 3D-poppetje {titel}: spritehoek, bek open, licht voorover op een onzichtbare tak', font=FB, fill=(30, 30, 30))
    # rij 1: spritehoek groot + kop ingezoomd naast de gespiegelde leidraad (dezelfde hoek)
    SY, SP = 48, 4
    im.paste(view(m, SY, SP, out=400), (10, 34)); lab(14, 436, f'spritehoek: 3/4 links ({SY}°), bijna recht')
    im.paste(view(m, SY, SP, out=330, focus=head_focus(m, SY, SP, 10)), (430, 50)); lab(434, 384, 'kop in de spritehoek')
    ld = Image.open(os.path.join(REF, 'jordi_great_potoo_bek_open_duo.webp')).convert('RGB').crop((80, 80, 580, 580)).resize((330, 330))
    im.paste(ld.transpose(Image.FLIP_LEFT_RIGHT), (780, 50)); lab(784, 384, 'leidraad (duo links), gespiegeld')
    lab(1130, 60, 'Lees de rij hieronder:')
    lab(1130, 80, 'kop op dezelfde hoek en')
    lab(1130, 100, 'grootte als de foto.')
    # rij 2: kop naast close-up en leidraad op dezelfde hoek en grootte
    y2 = 460
    cu = Image.open(os.path.join(REF, 'jordi_great_potoo_kop_closeup_bek_open.webp')).convert('RGB').crop((80, 200, 900, 1200)).resize((300, 366))
    im.paste(cu, (10, y2)); lab(14, y2 + 370, 'close-up (Jordi)')
    im.paste(view(m, 140, 4, out=330, focus=head_focus(m, 140, 4, 9)).crop((15, 0, 315, 330)), (320, y2 + 18)); lab(324, y2 + 370, 'poppetje, hoek close-up (140°)')
    ld2 = Image.open(os.path.join(REF, 'jordi_great_potoo_bek_open_duo.webp')).convert('RGB').crop((150, 90, 560, 500)).resize((330, 330))
    im.paste(ld2, (660, y2 + 18)); lab(664, y2 + 370, 'leidraad (duo links)')
    im.paste(view(m, 120, -4, out=330, focus=head_focus(m, 120, -4, 9)), (1000, y2 + 18)); lab(1004, y2 + 370, 'poppetje, hoek leidraad (120°, iets van onder)')
    # rij 3 en 4: rondom (niet verplicht, ter controle)
    y3 = 860
    hoeken = [(0, 'zij (0°)'), (90, 'voor (90°)'), (-135, 'schuin achter'), (-90, 'achter'), (132, '3/4 rechts')]
    for i, (yaw, t) in enumerate(hoeken):
        x = 10 + 266 * i
        im.paste(view(m, yaw, 8, out=250), (x, y3))
        lab(x + 4, y3 + 250, t)
        im.paste(view(m, yaw, 8, out=250, focus=head_focus(m, yaw, 8)), (x, y3 + 270))
        lab(x + 4, y3 + 520, 'kop ' + t)
    im = im.crop((0, 0, W, y3 + 545))
    im.save(os.path.join(HERE, naam))
    return im


if __name__ == '__main__':
    vel()
