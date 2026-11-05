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
    'fur': '#F1EFF6', 'jawfur': '#F1EFF6', 'wing': '#E1DDEB', 'far': '#CFCADC', 'tail': '#D9D4E4', 'bark': '#A99FB8',
    'eye': '#09080D', 'lid': '#D3CCE2', 'rim': '#E4DFEE', 'horn': '#8F84A3', 'hook': '#3A3346', 'tip': '#4A4259', 'hk1': '#A79FB0', 'hk2': '#7A7085', 'hk3': '#544A60', 'jt1': '#CCC4D6', 'jt2': '#9F96AB',
    'mouth': '#8E7EE8', 'mouth2': '#6F60CF', 'palate': '#6A5BCB', 'throat': '#231B52', 'brow': '#A79CBE',
}
NOSHADE = {'eye', 'throat'}
LINED = {'eye', 'lid', 'throat'}   # ronde 4c: punten zonder eigen lijn (onderdeel van de snavel, geen kapje)
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
    # wat binnen de mondrand ligt maar geen mondwand is (een stukje wang/borst diep in de keel), is keelholte:
    # zo staat er nooit vacht ín de muil en nooit mondkleur buiten de rand
    bar = np.isin(gid, [GROUPS.index(x) for x in ('mouth', 'mouth2', 'palate', 'throat', 'rim', 'horn', 'hook', 'tip', 'hk1', 'hk2', 'hk3', 'jt1', 'jt2', 'brow', 'eye', 'lid')])
    img = Image.fromarray(np.where(bar, 0, 255).astype(np.uint8)).copy()
    ImageDraw.floodfill(img, (0, 0), 128)
    hole = np.array(img) == 255
    gid[hole] = GROUPS.index('mouth2')
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
        jf = GROUPS.index('jawfur')
        jawb = (gid != g2) & ((gid == jf) | (g2 == jf)) & (gid >= 0) & (g2 >= 0)   # omtrek van de onderkaak
        e = ((np.abs(z - z2) > thr) & ~soft) | ((gid != g2) & (lined | l2)) | jawb
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
    open_deg=50,       # hoe ver de onderkaak hangt
    eye_r=1.15,        # oogstraal (Pokémon: iets groter dan 1)
    eye_gap=1.0,       # ruimte tussen oog en bovenrand, in oogstralen (foto's: ±½)
    eye_z=3.7,         # ogen naar voren, ±1 oogdiameter uit elkaar (nachtfoto)
    lean=12,           # voorover hangen
    body_k=0.85,       # lijf kleiner t.o.v. de kop (Pokémon)
    head_pitch=6,      # kop iets voorover: bovenrand daalt naar het haakje (close-up)
    xh=1.6, yh=-2.3,   # scharnier = mondhoek, op de breedste plek van de kop (muil zo breed als de kop)
    tip=-4.8,          # voorkant bovensnavel (basis van het haakje)
    half=70,           # bovenrand van boven gezien: brede boog naar het haakje
    jaw_tip=-6.6,      # punt van de onderkaak: diepe schep (±6-7 r_e onder de gaplijn als hij hangt)
    half_jaw=64,       # kaakpunt van boven gezien
)


def on_surf(Eb, o, d):
    """Snijpunt van de straal o + t d met ellipsoïde Eb (achterste snijpunt) en de normaal daar."""
    c, r = Eb[1], Eb[2]
    u0, ub = (o - c) / r, d / r
    A, B, C = ub @ ub, 2 * u0 @ ub, u0 @ u0 - 1
    t = (-B + math.sqrt(max(0.0, B * B - 4 * A * C))) / (2 * A)
    q = o + d * t
    n = (q - c) / r ** 2
    return q, n / np.linalg.norm(n)


def tufts(S, Eb, o, dirs, flow, size, group, lift=22, sink=0.3, keep=None):
    """Veerplukjes langs het oppervlak (geeft een getekende, licht onregelmatige omtrek zoals de lama-wol).
    dirs: richtingen vanuit o; flow(q) = richting waarin de veer ligt (bv. naar achteren-omlaag)."""
    for i, d in enumerate(dirs):
        d = np.array(d, float); d /= np.linalg.norm(d)
        q, nn = on_surf(Eb, o, d)
        if keep is not None and not keep(q):
            continue
        fl = np.array(flow(q), float); fl -= nn * (fl @ nn); fl /= np.linalg.norm(fl)
        ax = fl * math.cos(math.radians(lift)) + nn * math.sin(math.radians(lift))
        a, b = size[0] * (0.85 + 0.3 * ((i * 37) % 7) / 6), size[1]
        S.append(Solid(leaf(q + ax * a * 0.55 - nn * sink, ax, np.cross(nn, ax), a, b, size[2]), group))


def lens(tip, corner, alpha, yc, ry, y_ref, k=0.0, sag=None):
    """Twee grote, bijna verticale ellipsoïden waarvan de doorsnede (bovenaanzicht) een spitse boog is:
    punt bij tip (x), door de mondhoeken (corner = (x, z)), halve tophoek alpha. Op hoogte y_ref klopt de boog;
    hoger wordt hij breder (raakt de koepel niet), lager smaller. k = alles k naar binnen (holte)."""
    al = math.radians(alpha)
    tp = np.array((tip, 0.0)); c = np.array(corner, float)
    n = np.array((math.sin(al), -math.cos(al)))
    v = c - tp
    Rr = (v @ v) / (2 * (v @ n))
    ctr = tp + Rr * n
    if sag is not None:            # yc = y_ref; ry zo dat de boog sag[1] naar binnen loopt op sag[0] onder y_ref (bolle kom)
        yc, ry = y_ref, sag[0] * math.sqrt(Rr / (2 * sag[1]))
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
    # --- kop: brede, lage koepel; het breedst vlak boven de gaplijn (mondhoeken op de omtrek), voorhoofd in één
    #     bolle bocht naar het haakje; de kruin ligt naar achteren (close-up)
    Ed = E((2.4, -0.7, 0), (5.5, 4.7, 5.5))                  # ronde 5: volle, bolle koepel; kruin hoger en verder naar achteren
    Ef = E((-0.4, -1.3, 0), (4.6, 3.3, 4.8))                 # voorhoofd bolt in één ronde lijn naar de snavel
    zc = 5.5 * math.sqrt(1 - ((yh + 0.7) / 4.7) ** 2) - 0.08
    L = lambda k=0.0: lens(tip, (xh, zc), p['half'], 0.0, 60.0, yh, k)

    def paint_upper(T, P):
        g = np.array(['fur'] * len(T), object)
        h = P[:, 1] - gy(P[:, 0])
        f = np.clip((xh - P[:, 0]) / (xh - tip), 0, 1)
        band = (h < 0.2 + 0.4 * f ** 2) & (P[:, 0] < xh + 0.3)
        g[band] = 'rim'                                                  # de onderrand van het gezicht zelf
        g[band & (f > 0.72) & (np.abs(P[:, 2]) < 0.4 + 2.2 * (1 - f))] = 'horn'   # bovensnavelpunt: hoorn, rond het haakje                                    # naar voren dikker en donkerder (hoorn)
        pal = T == 1
        for c in L(0.4):
            pal &= ((((P - c[1]) @ c[3]) / c[2]) ** 2).sum(1) < 1
        g[(T == 1) & ~pal] = 'rim'
        g[pal] = 'palate'
        kv = np.array(streaks('fur', [((3.6, 1.4), (5.2, -0.4), 0.22, 0), ((2.2, 2.2), (3.4, 1.4), 0.18, 0)])(T, P), object)
        g[(kv == 'bark') & (g == 'fur')] = 'bark'
        return list(g)
    S.append(Solid([Ed, above] + L(), 'fur', paint=paint_upper))
    S.append(Solid([Ef, above] + L(), 'fur', paint=paint_upper))

    def surf2(o, d):
        qs = [on_surf(Eb, o, d) for Eb in (Ed, Ef)]
        return max(qs, key=lambda qn: (qn[0] - o) @ d)

    # --- ogen: naar voren, binnen de kopomtrek, ±1 oogdiameter uit elkaar, ½ oogstraal boven de rand;
    #     smal licht ooglidrandje, geen glans
    er = p['eye_r']
    eyes = []
    for sz in (1, -1):
        x = -2.5
        for _ in range(4):
            ye = gy(x) + (1 + p['eye_gap']) * er
            q, nn = surf2(np.array((2.0, ye, p['eye_z'] * sz)), np.array((-1.0, 0, 0)))
            x = q[0]
        e = q - nn * 0.22 * er
        eyes.append(e)
        S.append(Solid([E(q - nn * 0.8 * er, er * 1.22)], 'lid'))
        S.append(Solid([E(e, er)], 'eye'))

    # --- veertjes tussen de ogen: donkerdere plukjes boven het haakje die de omtrek breken (close-up)
    for zz, yo, a, lift in ((0.0, 2.0, 0.95, 12), (0.6, 2.25, 0.9, 10), (-0.6, 2.25, 0.9, 10), (0.0, 2.9, 0.95, 10),
                            (1.1, 2.8, 0.85, 8), (-1.1, 2.8, 0.85, 8)):   # ronde 5: platter tegen de bolle kop, boven het haakje
        q, nn = surf2(np.array((2.0, gy(tip) + yo, zz)), np.array((-1.0, 0, 0)))
        fl = np.array((-0.6, -1.0, 0.25 * zz)); fl -= nn * (fl @ nn); fl /= np.linalg.norm(fl)
        ax = fl * math.cos(math.radians(lift)) + nn * math.sin(math.radians(lift))
        S.append(Solid(leaf(q + ax * a * 0.55 - nn * 0.1, ax, np.cross(nn, ax), a * 1.2, 0.42, 0.3), 'brow'))
    # --- ruige kruin en wangen: plukjes langs de omtrek (getekend, niet perfect rond)
    rng = np.random.default_rng(7)
    dirs = []
    for th in np.linspace(-35, 215, 15):                                  # rond de kruin, van voorhoofd tot achterhoofd
        for ph in (-0.55, 0.0, 0.55):
            t = math.radians(th)
            dirs.append((-math.cos(t), math.sin(t) * 0.9 + 0.1, ph + rng.uniform(-0.12, 0.12)))
    tufts(S, Ed, np.array((1.6, -1.0, 0)), dirs, lambda q: (1.0, -0.55, 0.15 * np.sign(q[2])), (1.1, 0.5, 0.35), 'fur',
          lift=14, sink=0.32, keep=lambda q: q[0] > -1.2 and q[1] > gy(q[0]) + 1.0)
    # --- haakje: duidelijk, donker, omgekruld (±1,5 r_e), het voorste punt van het profiel, hangt vóór de muil
    g0 = gy(tip)
    # ronde 4c: de bovensnavel steekt pas vóóraan uit het gezicht, wordt smaller en loopt zelf door in het haakje
    # (één taps toelopende vorm; kleur verloopt van hoorngrijs naar donker, zonder eigen lijn)
    hk = [(tip + 2.2, g0 + 0.25, 0.62, 'rim'), (tip + 1.3, g0 + 0.35, 0.6, 'hk1'), (tip + 0.5, g0 + 0.38, 0.52, 'hk1'),
          (tip - 0.1, g0 + 0.2, 0.44, 'hk2'), (tip - 0.4, g0 - 0.2, 0.36, 'hk2'), (tip - 0.35, g0 - 0.65, 0.27, 'hk3'),
          (tip - 0.1, g0 - 0.95, 0.18, 'hook'), (tip + 0.12, g0 - 1.05, 0.1, 'hook')]
    for (x0, y0, r0, c0), (x1, y1, r1, c1) in zip(hk, hk[1:]):
        for t in np.linspace(0, 1, 6)[:-1]:
            zr = 0.9 - 0.25 * (1 - (r0 + (r1 - r0) * t) / 0.62)
            S.append(Solid([E((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, 0), (r0 + (r1 - r0) * t) * np.array((1.2, 1, zr)))], c0 if t < 0.5 else c1))

    # --- onderkaak: diepe schep met eigen bevederde buitenkant, opengeklapt om de mondhoeken
    tj = p['jaw_tip']
    Ej = E((0.2, yh, 0), (7.8, 3.0, zc / math.sqrt(1 - ((xh - 0.2) / 7.8) ** 2)))
    Lj = lambda k=0.0: lens(tj, (xh, zc), p['half_jaw'], 0.0, 60.0, yh, k, sag=(3.0, 2.0))
    inner = E(Ej[1] + np.array((-0.4, 0.35, 0)), Ej[2] - np.array((0.0, 0.5, 0.45)))

    def paint_jaw(T, P):
        g = np.array(['jawfur'] * len(T), object)                       # eigen bevederde buitenkant (met omtrek)
        g[T == 1] = 'rim'                                                # dunne lichte kaakrand
        # ronde 4c: de kaak loopt zelf spits toe; rand en buitenkant worden geleidelijk donkerder naar de punt
        d = P[:, 0] - tj
        out = T < 100
        g[out & (d < 1.7 + 0.25 * np.abs(P[:, 2]))] = 'jt1'
        g[out & (d < 0.95 + 0.2 * np.abs(P[:, 2]))] = 'jt2'
        g[out & (d < 0.4)] = 'tip'
        cav = T >= 100
        deep = gy(P[:, 0]) - P[:, 1]
        g[cav] = 'mouth'                                                 # licht bij de rand
        g[cav & ((deep > 1.4) | (P[:, 0] > xh - 1.2))] = 'mouth2'      # donkerder naar de bodem en de keel
        tt = (P[:, 0] - (xh - 4.6)) / 3.0
        # ronde 4: geen keelspleet meer in de kaakbodem (las als hoektand); alleen een klein V-spleetje achterin
        g[T == 2] = 'mouth2'
        return list(g)
    jaw = Solid([Ej, below, H((1, 0, 0), xh)] + Lj(), 'fur', cavs=[[inner] + Lj(0.45)], paint=paint_jaw)
    jaw.moved(rot_z(math.radians(p['open_deg'])), (xh, yh, 0))
    S.append(jaw)

    # --- keel/wangen achter het scharnier, met de keelholte (donker, alleen binnen de rand)
    gul = E((xh + 0.8, yh - 2.0, 0), (2.8, 3.3, zc - 0.45))

    def paint_cheek(T, P):
        g = np.array(['fur'] * len(T), object)
        g[T >= 100] = 'mouth2'
        yy = (P[:, 1] - (yh - 2.2)) / 1.4                                 # smalle V-spleet achter in de keel (close-up)
        g[(T >= 100) & (P[:, 0] > xh + 1.0) & (yy > 0) & (yy < 1) & (np.abs(P[:, 2]) < 0.3 * yy)] = 'throat'
        return list(g)
    for Eb in (Ed, E((3.0, -4.3, 0), (3.6, 3.0, 4.9))):
        S.append(Solid([Eb, below, H((-1, 0, 0), -xh)], 'fur', cavs=[[gul, below]], paint=paint_cheek))

    for s_ in S:
        s_.moved(rot_z(math.radians(p['head_pitch'])), (xh, yh, 0))

    # --- lijf: peervormig, schouders tot ±de gaplijn; vleugel met getrapte pennen; lange smalle staart
    body = []
    sp_body = streaks('fur', [((3.9, -11.0), (4.3, -13.6), 0.22, 1), ((4.6, -14.4), (4.9, -16.4), 0.2, 1)])
    sp_wing = streaks('wing', [((4.7, -6.0), (5.2, -8.6), 0.26, 1), ((6.6, -7.0), (7.0, -9.8), 0.24, 1),
                               ((5.5, -10.6), (5.9, -13.2), 0.25, 1), ((7.5, -11.0), (7.8, -13.6), 0.22, 1)])
    sp_far = streaks('far', [((5.4, -7.0), (5.8, -9.6), 0.24, -1), ((6.2, -11.0), (6.5, -13.4), 0.22, -1)])
    body.append(Solid([E((6.2, -10.5, 0), (4.6, 8.4, 6.0))], 'fur', paint=sp_body))
    body.append(Solid([E((5.6, -16.0, 0), (3.3, 3.8, 4.4))], 'fur'))
    for sz in (1, -1):
        g = 'wing' if sz > 0 else 'far'
        body.append(Solid([E((6.3, -12.3, 4.7 * sz), (3.4, 7.2, 1.9), rot_z(math.radians(-5)))], g, paint=sp_wing if sz > 0 else sp_far))
        for i in range(4):                                                # getrapte slagpennen langs de staart
            c = np.array((6.9 + 0.5 * i, -16.0 - 1.8 * i, (5.0 - 0.75 * i) * sz))
            body.append(Solid(leaf(c, (0.2, -1.0, -0.2 * sz), (1, 0, 0), 3.2, 1.0, 0.5), g))
    for i, t in enumerate(np.linspace(0, 1, 12)):                         # staart: in het verlengde van het lijf, versmallend
        body.append(Solid([E((6.6 + 2.0 * t, -16.5 - 11.0 * t, 0), (1.0, 2.0, 2.5 - 1.6 * t))], 'tail'))
    body.append(Solid(leaf((8.7, -28.2, 0), (0.18, -1, 0), (0, 0, 1), 1.4, 0.75, 0.8), 'tail'))
    # plukjes langs borst en flanken: licht onregelmatige omtrek
    Eb = body[0].base[0]
    dirs = [(math.cos(math.radians(a)) * -0.4, -0.1 + 0.5 * math.sin(math.radians(b)), math.sin(math.radians(a)))
            for a in range(-80, 81, 20) for b in (-60, -20, 20)]
    tufts(body, Eb, np.array((6.2, -10.5, 0)), dirs, lambda q: (0.1, -1.0, 0), (1.3, 0.6, 0.4), 'fur', lift=12, sink=0.3,
          keep=lambda q: q[1] < -5.5)
    # Pokémon-verhouding: lijf iets kleiner dan echt (schaal om de schouder)
    k, o = p['body_k'], np.array((3.5, -3.0, 0))
    for b in body:
        b.base = [(c[0], o + (c[1] - o) * k, c[2] * k, c[3]) for c in b.base]
        if b.paint is not None:
            b.paint = _scaled(b.paint, o, k)
    if p.get('body', 1):
        S += body
    piv = (2.5, -17, 0)
    Rl = rot_z(math.radians(p['lean']))
    for s_ in S:
        s_.moved(Rl, piv)
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


# ---------------------------------------------------------------- controle: met de hand overgetrokken foto-omtrek
# Pixelcoördinaten in de originele foto's (overgetrokken op een raster): oogmidden, oogstraal, omtrek kop+muil, mondrand.
TRACES = {
    'leidraad': dict(
        file='jordi_great_potoo_bek_open_duo.webp', eye=(380, 222), r=29,
        outline=[(288, 225), (295, 165), (320, 120), (360, 107), (400, 110), (440, 124), (470, 145), (495, 175),
                 (510, 205), (520, 240), (515, 275), (500, 312), (470, 370), (440, 412), (405, 450), (385, 438),
                 (360, 400), (335, 355), (318, 310), (300, 265), (288, 225)],
        rim=[(322, 290), (360, 279), (400, 272), (440, 263), (480, 255), (512, 248), (515, 275), (500, 312),
             (470, 370), (440, 412), (405, 448), (370, 415), (345, 375), (330, 335), (322, 290)]),
    'closeup': dict(
        file='jordi_great_potoo_kop_closeup_bek_open.webp', eye=(500, 660), r=78,
        outline=[(125, 620), (140, 480), (200, 380), (300, 300), (400, 268), (500, 262), (600, 268), (700, 300),
                 (780, 350), (835, 430), (850, 530), (850, 650), (840, 760), (800, 820), (785, 880), (760, 950),
                 (730, 1020), (690, 1080), (640, 1122), (590, 1100), (520, 1050), (450, 980), (390, 900),
                 (350, 820), (300, 760), (200, 700), (125, 620)],
        rim=[(335, 750), (400, 770), (500, 790), (600, 800), (700, 800), (790, 800), (780, 870), (760, 950),
             (730, 1020), (690, 1080), (640, 1120), (590, 1100), (520, 1050), (450, 980), (390, 900), (350, 820),
             (335, 750)]),
}


def project(m, yaw, pitch, focus, out, pt):
    Rc = rot_x(math.radians(pitch)) @ rot_y(math.radians(yaw))
    c = Rc @ pt
    sc = out / (2 * focus[2])
    return ((c[0] - focus[0]) * sc + out / 2, -(c[1] - focus[1]) * sc + out / 2), sc


def near_eye(m, yaw):
    es = [s for s in m if s.group == 'eye']
    Rc = rot_y(math.radians(yaw))
    pts = [s.Ro @ s.base[0][1] + s.t for s in es]
    return max(pts, key=lambda p: (Rc @ p)[2])


def overlay_view(m, key, yaw, pitch, out=330, half=9.0):
    """Render op de hoek van de foto met de overgetrokken foto-omtrek eroverheen (uitgelijnd op het oog,
    geschaald op de oogstraal: foto-oogstraal = 1 r_e van het poppetje)."""
    fo = head_focus(m, yaw, pitch, half)
    im = view(m, yaw, pitch, out=out, focus=fo).convert('RGB')
    tr = TRACES[key]
    (ex, ey), sc = project(m, yaw, pitch, fo, out, near_eye(m, yaw))
    k = sc / tr['r']
    P = lambda pts: [(ex + (x - tr['eye'][0]) * k, ey + (y - tr['eye'][1]) * k) for x, y in pts]
    d = ImageDraw.Draw(im)
    d.line(P(tr['outline']), fill=(230, 40, 40), width=2)
    d.line(P(tr['rim']), fill=(255, 150, 0), width=2)
    r = sc
    d.ellipse((ex - r, ey - r, ex + r, ey + r), outline=(230, 40, 40), width=2)
    return im


def traced_photo(key, box, size):
    tr = TRACES[key]
    im = Image.open(os.path.join(REF, tr['file'])).convert('RGB').crop(box)
    k = size[0] / im.width
    im = im.resize(size)
    d = ImageDraw.Draw(im)
    P = lambda pts: [((x - box[0]) * k, (y - box[1]) * k) for x, y in pts]
    d.line(P(tr['outline']), fill=(230, 40, 40), width=2)
    d.line(P(tr['rim']), fill=(255, 150, 0), width=2)
    return im


def vel(naam='vel_ronde5.png', titel='ronde 5', **kw):
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
    m = potoo(**kw)
    W = 1340
    im = Image.new('RGB', (W, 1480), 'white')
    d = ImageDraw.Draw(im)
    lab = lambda x, y, t: d.text((x, y), t, font=F, fill=(60, 60, 60))
    d.text((12, 8), f'Great potoo (Ghost/Normal): 3D-poppetje {titel}: spritehoek, bek open, licht voorover op een onzichtbare tak', font=FB, fill=(30, 30, 30))
    # rij 1: spritehoek groot + kop ingezoomd naast de gespiegelde leidraad (dezelfde hoek)
    SY, SP = 48, 4
    im.paste(view(m, SY, SP, out=400), (10, 34)); lab(14, 436, f'spritehoek: 3/4 links ({SY}°), bijna recht')
    im.paste(view(m, SY, SP, out=330, focus=head_focus(m, SY, SP, 10)), (430, 50)); lab(434, 384, 'kop in de spritehoek')
    ld = Image.open(os.path.join(REF, 'jordi_great_potoo_bek_open_duo.webp')).convert('RGB').crop((80, 80, 580, 580)).resize((330, 330))
    im.paste(ld.transpose(Image.FLIP_LEFT_RIGHT), (780, 50)); lab(784, 384, 'leidraad (duo links), gespiegeld')
    sm = view(m, SY, SP, out=400).resize((64, 64), Image.LANCZOS)
    im.paste(sm, (1140, 130)); im.paste(sm.resize((96, 96), Image.NEAREST), (1215, 120)); lab(1130, 222, '1x (64 px) en 2x')
    vgl = []
    for i, rn in enumerate(('3', '4', '4c')):                            # eerdere rondes ter vergelijking
        try:
            r3 = Image.open(os.path.join(HERE, f'vel_ronde{rn}.png')).crop((10, 34, 410, 434)).resize((110, 110), Image.LANCZOS)
            vgl.append((rn, r3))
        except FileNotFoundError:
            pass
    for i, (rn, r3) in enumerate(vgl):
        x, y = 1120 + (i % 2) * 110, 250 + (i // 2) * 0 if i < 2 else 250
        x, y = (1120, 240) if i == 0 else ((1230, 240) if i == 1 else (1175, 345))
        im.paste(r3, (x, y)); lab(x + 30, y + 98, 'r' + rn)
    lab(1130, 60, 'Lees de rij hieronder:')
    lab(1130, 80, 'kop op dezelfde hoek en')
    lab(1130, 100, 'grootte als de foto.')
    # rij 2: foto met overgetrokken omtrek (rood) en mondrand (oranje), en dezelfde lijnen over het poppetje
    y2 = 460
    im.paste(traced_photo('closeup', (60, 220, 900, 1200), (300, 350)), (10, y2)); lab(14, y2 + 354, 'close-up, overgetrokken')
    im.paste(overlay_view(m, 'closeup', 140, 4, out=330, half=9.5), (320, y2 + 10)); lab(324, y2 + 354, 'poppetje 140°, lijnen van de close-up')
    im.paste(traced_photo('leidraad', (260, 80, 580, 480), (280, 350)), (670, y2)); lab(674, y2 + 354, 'leidraad, overgetrokken')
    im.paste(overlay_view(potoo(**dict(kw, head_pitch=-5)), 'leidraad', 140, -4, out=330, half=9.5), (960, y2 + 10)); lab(964, y2 + 354, 'poppetje 140°, iets van onder, kop 5° omhoog (foto)')
    lab(14, y2 + 372, 'rood = omtrek kop+muil, oranje = mondrand; uitgelijnd op het oog, geschaald op de oogstraal (foto-oog = 1 r_e; het poppetjesoog is 1,15x)')
    # rij 3 en 4: rondom (niet verplicht, ter controle)
    y3 = 860 + 20
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
