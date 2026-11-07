"""Great potoo: kop als 3D-vorm, gesneden uit twee foto-omtrekken (visual hull), met de snavel uit de overgetrokken randen.
Jordi (5 nov): "maak er maar een 3d model van ... is het de vraag of de verhouding nog klopt", "check uit meerdere hoeken".
Kopcoördinaten in voorfoto-pixels: X = zijwaarts (- = nabije kant op de 3/4-foto), Y = omhoog (0 = ooghoogte), Z = naar voren (0 = oogvlak).
Gemeten:
- voorfoto (referenties/jordi_great_potoo_nacht_voor_volledig.webp): kopomtrek VOOR, ogen op X = ±97, oogstraal ±40, snavelpunt X 0
- 3/4-foto (referenties/jordi_great_potoo_bek_open_drieluik.webp): kopomtrek = samenstel.KOP, mondranden = potoo3d.BOVENRAND/...
- schaal 3/4 : voor = (kruin->oog 84 px) : (167 px) = 0,5025; kijkhoek uit de oogafstand: cos b = 68,8 / (194 x 0,5025) -> b = 45 graden
"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import potoo3d as P3
import samenstel as SM

VOOR = [(343, 117), (400, 103), (471, 101), (543, 110), (600, 139), (636, 181), (657, 224), (664, 274), (661, 324),
        (655, 380), (645, 420), (330, 420), (285, 380), (275, 310), (282, 260), (293, 210), (314, 160)]   # onderkant: snede op y 420 (kop gaat in het lijf over)
V_MID, V_OOG_Y = 486, 268                  # middenlijn (snavelpunt) en ooghoogte op de voorfoto
OOG_X, OOG_R = 97, 40
S34 = 84 / 167
B = math.radians(math.degrees(math.acos(68.8 / (194 * S34))))
U0, V0 = 271.7 + S34 * OOG_X * math.cos(B), 111.3


def proj_voor(X, Y, Z):
    return V_MID + X, V_OOG_Y - Y


def proj_34(X, Y, Z):
    return U0 + S34 * (X * math.cos(B) + Z * math.sin(B)), V0 - S34 * Y


def binnen(poly, u, v):
    """Punt-in-veelhoek voor arrays u, v (even-oneven-regel)."""
    poly = np.asarray(poly, float); res = np.zeros(u.shape, bool)
    for (x1, y1), (x2, y2) in zip(poly, np.roll(poly, -1, axis=0)):
        c = ((y1 > v) != (y2 > v)) & (u < (x2 - x1) * (v - y1) / (y2 - y1 + 1e-12) + x1)
        res ^= c
    return res


def mond3d(w=OOG_X):
    """Mondranden in 3D: X uit de plek op de rand (nabije mondhoek -w, voorkant 0, verre mondhoek +w), Y en Z uit de 3/4-projectie."""
    def lijn(pts, x0, x1, n=40):
        pts = np.array(pts, float); L = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
        out = []
        for t in np.linspace(0, 1, n):
            u, v = (np.interp(t * L[-1], L, pts[:, i]) for i in (0, 1))
            X = x0 + (x1 - x0) * math.sin(t * math.pi / 2) if x0 == 0 else x0 * math.cos(t * math.pi / 2) + x1 * math.sin(t * math.pi / 2)
            Y = -(v - V0) / S34
            Z = ((u - U0) / S34 - X * math.cos(B)) / math.sin(B)
            out.append((X, Y, Z))
        return np.array(out)
    boven = lijn(P3.BOVENRAND, -w, 0)
    verre = lijn(P3.VERRE_RAND, w, 0)
    nabij = lijn(P3.NABIJE_RAND, -w, 0)
    return boven, verre, nabij


HOOFD = {}
VOL0 = {}


def straal_rand(pts, vol0, xs, ys, zs, n=50):
    """Elk overgetrokken 3/4-punt is een kijkstraal; de rand ligt op het kopoppervlak: eerste geraakte voxel (vanaf de camera)."""
    pts = np.array(pts, float); L = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
    st = xs[1] - xs[0]; out = []
    for t in np.linspace(0, 1, n):
        u, v = (np.interp(t * L[-1], L, pts[:, i]) for i in (0, 1))
        q = (u - U0) / S34; Y = -(v - V0) / S34
        j = int(round((Y - ys[0]) / st))
        hit = None
        for d in np.arange(320, -320, -st / 2):
            X = q * math.cos(B) - d * math.sin(B); Z = q * math.sin(B) + d * math.cos(B)
            i = int(round((X - xs[0]) / st)); k = int(round((Z - zs[0]) / st))
            if 0 <= i < len(xs) and 0 <= j < len(ys) and 0 <= k < len(zs) and vol0[i, j, k]:
                hit = (X, Y, Z); break
        if hit is not None: out.append(hit)
    return np.array(out)


def hull(stap=7):
    """Visual hull: voorfoto-omtrek + 3/4-omtrek + dezelfde 3/4-omtrek gespiegeld (de vogel is links-rechts symmetrisch;
    zonder echte profielfoto begrenst dat de diepte). Mondholte = doorsnede van de mondomtrek in 3/4, gespiegeld en van voren."""
    xs = np.arange(-240, 241, stap); ys = np.arange(-300, 200, stap); zs = np.arange(-300, 200, stap)
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing='ij')
    boven, verre, nabij = mond3d()
    ymond = min(verre[:, 1].min(), nabij[:, 1].min())
    # voorfoto: kop tot de snede op y 420; daaronder alleen de hangende onderkaak (tussen de mondhoeken)
    Yc = np.where(Y < V_OOG_Y - 420, V_OOG_Y - 420 + 1, Y)
    ybot0 = V_OOG_Y - 420
    hw = (645 - 330) / 2                                          # halve kopbreedte op de snede (voorfoto)
    kin = (X / hw) ** 2 + ((Y - ybot0) / (ymond - 6 - ybot0)) ** 2 <= 1.0   # onderkaak + keel: U van de snede naar de kaakpunt
    a = binnen(VOOR, *proj_voor(X, Yc, Z)) & ((Y >= ybot0 - stap) | kin)
    b = binnen(SM.KOP, *proj_34(X, Y, Z))
    b2 = binnen(SM.KOP, *proj_34(-X, Y, Z))
    vol = a & b & b2
    VOL0['v'] = vol.copy()
    # diepte van de kop, afgeleid (niet geschat): projectie-breedte 3/4 = S34 * 2 * sqrt(a^2 cos^2 B + c^2 sin^2 B),
    # met a = halve breedte voorfoto -> c = halve diepte
    a_ = (max(p[0] for p in VOOR) - min(p[0] for p in VOOR)) / 2
    w34 = (max(p[0] for p in SM.KOP) - min(p[0] for p in SM.KOP)) / S34 / 2
    c_ = math.sqrt(max(1.0, (w34 ** 2 - a_ ** 2 * math.cos(B) ** 2) / math.sin(B) ** 2))
    zf = boven[-1][2]
    ytop = max(V_OOG_Y - p[1] for p in VOOR); ybot = V_OOG_Y - 420
    yc, hb = (ytop + ybot) / 2, (ytop - ybot) / 2
    prof = ((Z - (zf - c_)) / c_) ** 2 + ((np.maximum(Y, ybot) - yc) / hb) ** 2 <= 1.0
    vol &= prof | (Y < ybot)
    HOOFD['diepte'] = 2 * c_; HOOFD['breedte'] = 2 * a_
    boven = straal_rand(P3.BOVENRAND, vol, xs, ys, zs)
    nabij = straal_rand(P3.NABIJE_RAND, vol, xs, ys, zs)
    verre = straal_rand(P3.VERRE_RAND, vol, xs, ys, zs)
    HOOFD['bovenpunt_X'] = boven[-1][0]; HOOFD['kaakpunt_X'] = nabij[-1][0]; HOOFD['mondhoek'] = tuple(np.round(boven[0]))
    # mondholte, symmetrisch uit de nabije randen (best zichtbaar op de 3/4-foto), gespiegeld naar de verre kant
    bov = np.vstack([boven, boven[::-1] * (-1, 1, 1)])
    ond = np.vstack([nabij, nabij[::-1] * (-1, 1, 1)])
    poly_v = [(p[0], p[1]) for p in bov] + [(p[0], p[1]) for p in ond[::-1]]
    poly_z = [(p[2], p[1]) for p in boven] + [(p[2], p[1]) for p in nabij[::-1]]
    mond = np.vstack([bov, ond]); c = mond.mean(0)
    # de opening = het gebied binnen de gesloten 3D-rand (boven + onder): binnen de rand in alle drie de aanzichten
    # (voor, zij, boven); plus de keel als holte achter de mondhoeken die nergens door de wang breekt
    poly_t = [(p[0], p[2]) for p in bov] + [(p[0], p[2]) for p in ond[::-1]]
    opening = binnen(poly_v, X, Y) & binnen(poly_z, Z, Y) & binnen(poly_t, X, Z)
    hoek = boven[0]
    keel_c = np.array((0, (hoek[1] + ond[:, 1].min()) / 2, hoek[2] + 25))
    keel = ((X / (abs(hoek[0]) * 0.8)) ** 2 + ((Y - keel_c[1]) / 45) ** 2 + ((Z - keel_c[2]) / 60) ** 2) <= 1
    holte = opening | (keel & binnen(poly_v, X, Y))
    vol &= ~holte
    boven, verre, nabij = bov, ond[len(ond) // 2:], ond[:len(ond) // 2]
    cam = np.array((-math.sin(B), 0, math.cos(B)))
    _, _, vt = np.linalg.svd(mond - c); n = vt[2]
    if n @ cam < 0: n = -n
    return xs, ys, zs, vol, (boven, verre, nabij, c, n, holte)


def kop_delen(stap=7):
    """Oppervlak van de kop als bolletjes (kopcoördinaten, voorfoto-pixels) met groep: fur/eye/mouth/throat/rim/beak."""
    xs, ys, zs, vol, (boven, verre, nabij, c, n, holte) = hull(stap)
    sur = vol.copy()
    for ax in range(3):
        for s in (1, -1):
            sur &= np.roll(vol, s, axis=ax)
    sur = vol & ~sur
    I = np.argwhere(sur)
    P = np.stack([xs[I[:, 0]], ys[I[:, 1]], zs[I[:, 2]]], 1).astype(float)
    g = np.array(['fur'] * len(P), object)
    # ogen: op het oppervlak bij X = ±OOG_X, Y = 0 (voorste punt daar)
    for sx in (-1, 1):
        sel = (np.abs(P[:, 0] - sx * OOG_X) < stap) & (np.abs(P[:, 1]) < stap)
        zf = P[sel, 2].max() if sel.any() else 0
        e = np.array((sx * OOG_X, 0, zf))
        g[np.linalg.norm(P - e, axis=1) < OOG_R] = 'eye'
    nb = holte.copy()                                   # binnenkant = oppervlak dat aan de mondholte grenst
    for _ in range(2):
        n2 = nb.copy()
        for ax in range(3):
            for s_ in (1, -1):
                n2 |= np.roll(nb, s_, axis=ax)
        nb = n2
    inm = nb[I[:, 0], I[:, 1], I[:, 2]]
    diep = P[:, 2] < boven[0][2] - 45                   # ver achter de mondhoeken: keel (donker); de rest geestpaars
    g[inm & (g == 'fur')] = 'mouth'
    g[inm & diep & (g == 'mouth')] = 'throat'
    delen = [(p, stap * 0.8, gg) for p, gg in zip(P, g)]
    for lijn in (boven, verre, nabij):
        for p in lijn:
            delen.append((p + n * 2, 5.0, 'rim'))
    # spitse donkere punten (haakje en kaakpunt): 2D-omtrek -> 3D bij X = 0 (voorkant)
    for pts, X in ((SM.HAAK, 6), (SM.KAAKPUNT, 0)):
        for (uu, vv) in pts:
            Y = -(vv - V0) / S34; Z = ((uu - U0) / S34 - X * math.cos(B)) / math.sin(B)
            delen.append((np.array((X, Y, Z)), 4.0, 'beak'))
    return delen


def naar_model(delen, k, off):
    """Kopcoördinaten -> potoo3d-diercoördinaten (x = -Z naar achteren, y = Y, z = -X nabije kant naar de kijker)."""
    m = P3.Model()
    for p, r, g in delen:
        q = np.array((off[0] - p[2] * k, off[1] + p[1] * k, -p[0] * k))
        m.ell(q, r * k, g)
    return m


KLEUR = {'fur': (238, 236, 243), 'eye': (5, 5, 7), 'mouth': (90, 77, 184), 'throat': (30, 24, 66), 'rim': (230, 207, 200),
         'beak': (74, 68, 88)}


def render_kop(delen, yaw, size=300, schaal=0.55, mid=(0, -40)):
    """Orthografische render in kopcoördinaten; yaw 0 = van voren (voorfoto), yaw = B (45°) = de 3/4-foto.
    Positieve yaw draait de nabije kant (-X) naar de kijker, zoals op de 3/4-foto."""
    a = math.radians(yaw)
    im = np.full((size, size, 3), 255, np.uint8); zb = np.full((size, size), -1e9)
    L = np.array((-0.4, 0.6, 0.7)); L /= np.linalg.norm(L)
    P = np.array([p for p, r, g in delen]); Rr = np.array([r for p, r, g in delen]); G = [g for p, r, g in delen]
    u = P[:, 0] * math.cos(a) + P[:, 2] * math.sin(a); d = -P[:, 0] * math.sin(a) + P[:, 2] * math.cos(a)
    v = P[:, 1]
    order = np.argsort(d)
    for i in order:
        cx = int(size / 2 + (u[i] - mid[0]) * schaal); cy = int(size / 2 - (v[i] - mid[1]) * schaal); r = max(1, int(Rr[i] * schaal + 0.5))
        x0, x1, y0, y1 = max(0, cx - r), min(size, cx + r + 1), max(0, cy - r), min(size, cy + r + 1)
        if x0 >= x1 or y0 >= y1: continue
        sub = zb[y0:y1, x0:x1]; w = d[i] >= sub
        sub[w] = d[i]; im[y0:y1, x0:x1][w] = KLEUR[G[i]]
    # schaduw op diepte (verre kant donkerder) en omlijning op het silhouet
    a_ = zb > -1e9
    edge = a_ & ~(np.roll(a_, 1, 0) & np.roll(a_, -1, 0) & np.roll(a_, 1, 1) & np.roll(a_, -1, 1))
    jump = np.zeros_like(a_)
    for ax in (0, 1):
        jump |= np.abs(zb - np.roll(zb, 1, ax)) > 25 / schaal * 0.4
    im[(edge | (jump & a_))] = (40, 30, 30)
    return Image.fromarray(im)


def controle(delen, out):
    """Render op de hoeken van de foto's, met de foto-omtrekken eroverheen (groen = kop, roze = mond, blauw = ogen)."""
    from PIL import ImageFont
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14)
    sch = 0.62; mid = (0, -40); size = 340
    T0 = lambda X, Y: (size / 2 + (X - mid[0]) * sch, size / 2 - (Y - mid[1]) * sch)
    voor = render_kop(delen, 0, size, sch, mid); d = ImageDraw.Draw(voor)
    d.line([T0(u - V_MID, V_OOG_Y - v) for u, v in VOOR] + [T0(VOOR[0][0] - V_MID, V_OOG_Y - VOOR[0][1])], fill=(40, 200, 80), width=2)
    for sx in (-1, 1):
        x, y = T0(sx * OOG_X, 0); d.ellipse((x - OOG_R * sch, y - OOG_R * sch, x + OOG_R * sch, y + OOG_R * sch), outline=(40, 140, 255), width=2)
    # 3/4: model gedraaid over B; fotopixels -> kopcoördinaten via proj_34 terug (Z = 0 vlak: u = U0 + S34 * X')
    drie = render_kop(delen, math.degrees(B), size, sch, mid); d = ImageDraw.Draw(drie)
    T1 = lambda u, v: T0((u - U0) / S34, -(v - V0) / S34)
    for pts, kl in ((SM.KOP, (40, 200, 80)), (SM.MOND, (255, 60, 200)), (SM.HAAK, (255, 190, 0)), (SM.KAAKPUNT, (255, 190, 0))):
        d.line([T1(*p) for p in pts] + [T1(*pts[0])], fill=kl, width=2)
    for (c, rx, ry) in (SM.OOG, SM.VER_OOG):
        x, y = T1(*c); d.ellipse((x - rx / S34 * sch, y - ry / S34 * sch, x + rx / S34 * sch, y + ry / S34 * sch), outline=(40, 140, 255), width=2)
    extra = [render_kop(delen, y, size, sch, mid) for y in (20, 70, 90, 135)]
    fv = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'referenties', 'jordi_great_potoo_nacht_voor_volledig.webp')).convert('RGB').crop((230, 60, 740, 570)).resize((size, size))
    f3 = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'referenties', 'jordi_great_potoo_bek_open_drieluik.webp')).convert('RGB').crop((110, 0, 400, 290)).resize((size, size))
    S = Image.new('RGB', (size * 4 + 30, 2 * size + 70), 'white'); dd = ImageDraw.Draw(S)
    rij1 = [('voorfoto', fv), ('model 0° + omtrek voorfoto', voor), ('3/4-foto', f3), ('model 45° + omtrek 3/4-foto', drie)]
    rij2 = [(f'model {y}°', im) for y, im in zip((20, 70, 90, 135), extra)]
    for r, rij in enumerate((rij1, rij2)):
        for i, (t, im) in enumerate(rij):
            x, y = i * (size + 10), r * (size + 35)
            dd.text((x, y + 4), t, font=F, fill=(30, 30, 30)); S.paste(im, (x, y + 26))
    S.save(out)
