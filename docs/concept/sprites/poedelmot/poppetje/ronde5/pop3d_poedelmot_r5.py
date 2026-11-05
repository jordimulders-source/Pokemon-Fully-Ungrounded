"""Poedelmot (eindvorm, Bug/Fairy): 3D-poppetje als praatplaat, op de lama-manier (Jordi 5 nov: "ga maar de lama kant op
qua bouwen ipv in blender"). Gedeelde bibliotheek: olinguito_v2/silhouet_kolibriemethode/pop3d.py (Model, ell, chain);
render/shade/fluff uit lama/ontwerp/pop3d_lama.py (vlakke kleuren, één schaduwtoon, lijnen op dieptesprongen).
Diercoördinaten zoals de lama: x = naar achteren (snuit naar -x), y = omhoog, z = naar de kijker bij 0° (nabije kant +z).
Bron = alleen de tak-foto (referenties/foto_tak_katoen.webp): rechtop zittend, dik en wollig, pompon-poten, V-vleugels.
Hoek 45° (bevroren, Jordi). Kopverhouding uit de posestudie (posestudie.png): kop ±45% van de hoogte zonder vleugels.
Ronde 2 (Jordi: "poten mogen dunner, de voelsprieten mogen groter, zoals op de andere fotos, vleugels ook" + keurder):
poten iets dunner maar wollig, voorpaar gespreid met knik, lijf lager, pompons in perspectief, middenpaar opzij; sprieten
en vleugels groter; verre achtervleugel met gladde rand; snuit breed en plat (neusbrug). Rest = ronde 1 (../pop3d_poedelmot.py).
Ronde 4 (basis = ronde 2; wolmassa van lijf, buik en achterlijf ongewijzigd). Uit ronde 3 alleen: dubbele kam aan de
sprieten en de zichtbare verre achtervleugel (nu kleiner en hoger, in perspectief). Poten volgens Jordi: "2 voorste poten
zijn zichtbaarder, de andere vier staan dichter op elkaar per twee": voorpaar groot en vooraan, midden- en achterpoot per
kant als tweetal dicht naast elkaar, kleiner, half onder de wol; dikte zoals ronde 2.
Ronde 5 (Jordi: "je vergeet meerdere bronfotos te gebruiken he?"): elk onderdeel naar zijn eigen bron (SPEC, bron per
onderdeel). Ogen: tak-foto + bovenste helft foto_sprieten_plus_vilt + Venomoth (beide ogen volledig zichtbaar, lager en
meer naar voren, witte wol ertussen, geen masker). Sprieten: close-up foto_sprieten_plus_vilt + vilt (dubbele kam als
boog, gestreept bruin). Vleugels: vilt (fijne bruine adertjes) + tak-foto (V). Wol, lijf en poten = ronde 4.
Draaien vanuit de repo-root: python3 docs/concept/sprites/poedelmot/poppetje/ronde5/pop3d_poedelmot_r5.py"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../../../../..'))
sys.path.insert(0, os.path.join(HERE, '../../../olinguito_v2/silhouet_kolibriemethode'))
sys.path.insert(0, os.path.join(HERE, '../../../lama/ontwerp'))
import pop3d as P
import pop3d_lama as L

YAW = 45                      # bevroren (Jordi: "ja 45 graden is oke")
KOP_EXTRA = 14                # kop draait meer naar de kijker dan het lijf
COL = {
    'wol': '#F3EFE7', 'wolver': '#D6CFC2', 'pompon': '#FBF8F2', 'pomver': '#DCD5C8',
    'vleugel': '#ECE6D9', 'achtervl': '#E0D8C8', 'vlver': '#CFC7B7', 'achtver': '#C4BBAA',
    'spriet': '#7A5234', 'sprietver': '#5E3F28', 'sprietlicht': '#A47A55', 'ader': '#B49B82', 'aderver': '#A08A72', 'oog': '#1E1A24', 'glint': '#FFFFFF',
}
NOSHADE = {'oog', 'glint', 'ader', 'aderver'}
LINED = {'oog', 'sprietlicht', 'spriet', 'sprietver', 'vleugel', 'achtervl', 'vlver', 'achtver'}


def poot(m, pts, pr, ver, seed):
    """Gelede insectenpoot (dij, knie, scheen, voet), over de hele lengte dik en wollig, pompon onderaan."""
    g, gp = ('wolver', 'pomver') if ver else ('wol', 'pompon')
    m.chain(pts, g, 2.0)
    for i, (x, y, z, r) in enumerate(pts[:-1]):
        L.fluff(m, (x, y, z), (r, r, r), g, 6, r * 0.55, seed + i)
    x, y, z, _ = pts[-1]
    c = (x - 1, y - pr * 0.55, z)
    m.ell(c, (pr, pr * 0.9, pr), gp)
    L.fluff(m, c, (pr, pr * 0.9, pr), gp, 16, pr * 0.42, seed + 9)


def blad(m, wortel, u, n_hint, lengte, breedte, dikte, g, n=9):
    """Vleugel: keten van platte ellipsoïden langs u, breedteprofiel breedte(t); vlak loodrecht op n_hint."""
    u = np.array(u, float); u /= np.linalg.norm(u)
    w = np.array(n_hint, float); w -= (w @ u) * u; w /= np.linalg.norm(w)
    v = np.cross(w, u)
    R0 = np.column_stack([u, v, w])
    for i in range(n):
        t = (i + 0.5) / n
        m.ell(np.array(wortel) + u * lengte * t, (lengte / n * 1.8, max(breedte(t), 0.8), dikte), g, R0)
    # ronde 5: fijne bruine adertjes zoals bij het vilt (vilt_hand_vleugels_gespreid.png): waaier vanuit de wortel
    ag = 'aderver' if g in ('vlver', 'achtver') else 'ader'
    for s_ in ADERS_VOOR:
        for t in np.linspace(0.06, 0.93, 34):
            b = breedte(t)
            th = dikte * math.sqrt(max(0.0, 1 - (s_ * 0.8) ** 2))
            p = np.array(wortel) + u * lengte * t + v * s_ * b * 0.8
            for sw in (1, -1):
                m.ell(p + w * sw * (th + 0.3), (1.3, 0.45, 0.2), ag, R0)


ADERS_VOOR = (-0.55, -0.15, 0.25, 0.6)   # dwarspositie van de aders over de voorvleugel (−1..1)


def aders_rond(m, scharnier, c, r, R0, g):
    """Aders op een ronde achtervleugel (één ellipsoïde c, r in frame R0): waaier van het scharnier naar de rand."""
    ag = 'aderver' if g == 'achtver' else 'ader'
    u, v, w = R0[:, 0], R0[:, 1], R0[:, 2]
    for a in np.linspace(-0.9, 0.9, 5):
        eind = c + u * r[0] * 0.82 * math.cos(a) + v * r[1] * 0.82 * math.sin(a)
        for t in np.linspace(0.15, 1.0, 28):
            p = np.array(scharnier) + (eind - scharnier) * t
            du, dv = (p - c) @ u / r[0], (p - c) @ v / r[1]
            q = 1 - du * du - dv * dv
            if q <= 0.02:
                continue
            p = c + u * ((p - c) @ u) + v * ((p - c) @ v)
            th = r[2] * math.sqrt(q)
            for sw in (1, -1):
                m.ell(p + w * sw * (th + 0.3), (1.3, 0.45, 0.2), ag, R0)


def voorvl(t):     # lang, smal, spits (tak-foto)
    return 4.5 + 11.0 * math.sin(math.pi * min(t / 0.62, 1) * 0.5) if t < 0.62 else 0.8 + 14.7 * (1 - (t - 0.62) / 0.38) ** 1.5


def achtervl(t):   # kleiner, rond
    return 3.0 + 15.0 * math.sin(math.pi * t) ** 0.6


KIJK = np.array((-math.sin(math.radians(YAW)), 0.0, math.cos(math.radians(YAW))))   # naar de kijker, diercoördinaten


SPRIET = dict(lengte=48.0, boog=11.0, n=20, tand=10.0)


def spriet(m, basis, kant, ver):
    """Kamspriet als oor. Ronde 5 naar de close-up (bovenste helft foto_sprieten_plus_vilt.png) en het vilt: de schacht
    is een boog opzij (eerst omhoog, de punt zakt weer iets), dubbele kam met dichte tanden aan beide kanten (veervorm,
    langste in het midden), gestreept bruin: tanden om en om in twee bruintinten zoals bij het vilt."""
    g, g2 = ('sprietver', 'spriet') if ver else ('spriet', 'sprietlicht')
    N = SPRIET['n']
    pts = []
    for i in range(N + 1):
        t = i / N
        pts.append(np.array(basis) + np.array((3.0 * t, SPRIET['boog'] * math.sin(math.pi * 0.8 * t), kant * SPRIET['lengte'] * t)))
    m.chain([tuple(p) + (2.2 - 1.3 * i / N,) for i, p in enumerate(pts)], g, 1.0)
    for i in range(1, N):
        t = i / N
        p = pts[i]
        lang = SPRIET['tand'] * math.sin(math.pi * min(1.0, 0.12 + 0.95 * t)) ** 0.7 + 1.0
        rich = pts[i + 1] - pts[i]; rich /= np.linalg.norm(rich)
        zij = np.cross(rich, KIJK); zij /= np.linalg.norm(zij)
        for s in (1, -1):
            d = zij * s + rich * 0.5
            d /= np.linalg.norm(d)
            c = p + d * lang * 0.55
            u = d; w = KIJK - (KIJK @ u) * u; w /= np.linalg.norm(w)
            m.ell(c, (lang * 0.55, 0.75, 0.75), g if i % 2 else g2, np.column_stack([u, np.cross(w, u), w]))


def op45(sx, y, d, r):
    """Punt zoals het op 45° in beeld komt (sx links/rechts, d diepte, + = naar de kijker) -> diercoördinaten."""
    k = math.sqrt(0.5)
    return (k * (sx - d), y, k * (sx + d), r)


# Oog: richting vanuit het kopmidden (x, y, z) en stralen. Ronde 2: (-0.80, 0.02, 0.60), (7.6, 8.2, 7.6)
OOG = (-0.84, -0.22, 0.52, (8.0, 8.6, 8.0))   # ronde 5: lager en meer naar voren (tak-foto), beide ogen heel

# Verre achtervleugel (uit ronde 3, maar kleiner en hoger): richting, middelpuntafstand, stralen
ACHTERVL_VER = ((-0.3, 0.05, -0.95), 27.0, (25.0, 16.0, 1.4))   # ronde 5: verder opzij en groter, eigen vleugel

# Poten (Jordi): voorpaar groot en zichtbaar, hangt van de borst naar voren en omlaag, grootste pompons; midden- en
# achterpoot per kant dicht naast elkaar als tweetal, kleiner, achter/naast het voorpaar, half onder de wol; verre
# tweetal hoger en kleiner. Dikte zoals ronde 2. Lucht alleen tussen het voorpaar en de tweetallen.
# (heup, knie, voet) via op45(sx, y, diepte, straal); pompon-straal; ver.
POTEN = [
    ([op45(-8, 26, 16, 5.4), op45(-18, 18, 30, 5.0), op45(-12, 2, 36, 4.6)], 10.5, False),   # voor nabij
    ([op45(-18, 27, 4, 5.0), op45(-34, 19, 10, 4.6), op45(-39, 5, 10, 4.2)], 8.6, True),      # voor ver
    ([op45(10, 22, 20, 4.8), op45(16, 15, 28, 4.4), op45(16, 4, 30, 4.0)], 7.6, False),       # midden nabij (tweetal)
    ([op45(16, 21, 14, 4.6), op45(24, 14, 22, 4.2), op45(25, 4, 23, 3.8)], 7.0, False),       # achter nabij (tweetal)
    ([op45(-16, 25, -6, 4.4), op45(-24, 16, -2, 4.0), op45(-27, 7, -2, 3.6)], 6.2, True),  # midden ver (tweetal)
    ([op45(-12, 25, -10, 4.2), op45(-19, 16, -6, 3.8), op45(-21, 8, -6, 3.4)], 5.6, True),  # achter ver (tweetal)
]
POOTKLEUR = ['#E0302A', '#F08A1C', '#2A7FE0', '#A040E0', '#2EA84A', '#E040A0']


def poedelmot(kop_r=19.0, kop_extra=KOP_EXTRA, pootkleur=False):
    m = P.Model()
    # vleugels eerst (achter het lijf): per kant voor- en achtervleugel die overlappen tot één paar, samen in een V.
    # Symmetrisch; de V staat ver genoeg open dat de verre punt in 45° naast de kop eindigt, niet erboven.
    for kant in (1, -1):
        ver = kant < 0
        w = np.array((10.0, 37.0, 7.0 * kant))
        u = np.array((0.22, 0.46, 0.86 * kant))
        blad(m, w, u, (1.0, 0.0, 0.0), 86, voorvl, 1.4, 'vlver' if ver else 'vleugel', 20)
        ua = np.array((0.35, 0.05, 0.94 * kant))
        # achtervleugel: één gladde ronde vorm (geen keten: de rand blijft glad, leest niet als wolklont)
        ua = ua / np.linalg.norm(ua); wa = np.array((1.0, 0.3, 0.0)); wa -= (wa @ ua) * ua; wa /= np.linalg.norm(wa)
        Ra = np.column_stack([ua, np.cross(wa, ua), wa])
        if not ver:
            c = w + np.array((3.0, -6.0, 0.0)) + ua * 28.0
            m.ell(c, (29.0, 19.0, 1.4), 'achtervl', Ra)
            aders_rond(m, w + np.array((3.0, -6.0, 0.0)), c, np.array((29.0, 19.0, 1.4)), Ra, 'achtervl')
        else:   # ronde 4: verre achtervleugel opzij gedraaid (zichtbaar links naast de kop), kleiner en hoger
            ua = np.array(ACHTERVL_VER[0]); ua /= np.linalg.norm(ua)
            wa = np.array((1.0, 0.3, 0.0)); wa -= (wa @ ua) * ua; wa /= np.linalg.norm(wa)
            Ra = np.column_stack([ua, np.cross(wa, ua), wa])
            c = w + np.array((0.0, 2.0, 0.0)) + ua * ACHTERVL_VER[1]
            m.ell(c, ACHTERVL_VER[2], 'achtver', Ra)
            aders_rond(m, w + np.array((0.0, 2.0, 0.0)), c, np.array(ACHTERVL_VER[2]), Ra, 'achtver')
    # lijf: dik en wollig, rechtop zittend (achterlijf laag en breed op de grond, borst erboven)
    for c, r, s in (((10, 14, 0), (22, 15, 21), 1), ((-3, 25, 0), (18, 13, 19), 2), ((-10, 12, 0), (14, 10, 16), 3)):
        m.ell(c, r, 'wol')
        L.fluff(m, c, r, 'wol', 55, 6.5, s, ymin=-0.5)
    # wolkraag tussen kop en lijf
    for i, a in enumerate(np.linspace(0, 2 * math.pi, 16, endpoint=False)):
        m.ell((-5 + 15 * math.cos(a), 36 + (i % 2) * 1.5, 18 * math.sin(a)), 6.4, 'wol')
    # zes poten aan de borst; voorpaar grootst, hangt naar voren en omlaag; middenpaar opzij; achterpaar onder het lijf
    # ronde 2: iets dunner (nog wollig), voorpaar gespreid met knie naar voren, lijf laag ertussen; perspectief in de
    # pompons: nabij (+z) lager en groter, ver (-z) hoger, kleiner, half achter het lijf
    for i, (pts, pr, ver) in enumerate(POTEN):
        n0 = len(m.parts)
        poot(m, pts, pr, ver, 20 + 10 * i)
        if pootkleur:   # controlevel: elke poot een eigen kleur
            m.parts[n0:] = [(c, r, R0, f'p{i}') for c, r, R0, g in m.parts[n0:]]
    # kop: groot, rond, wollig, op de kraag; draait extra naar de kijker
    h0 = len(m.parts)
    cr = np.array((-9.0, 53.0, 0.0))
    kr = np.array((kop_r, kop_r * 0.95, kop_r))
    m.ell(cr, kr, 'wol')
    L.fluff(m, cr, kr, 'wol', 34, 5.0, 77, ymin=-0.3)
    # ronde 4 (Jordi: "met grote donkere ogen, beetje venomoth achtig"): twee grote ronde donkere facetogen OPZIJ van
    # de kop (zoals Venomoth en de tak-foto), geen zonnebril vooraan. Op 45° is het nabije oog groot en rond, het verre
    # smaller en half achter de kopwelving. Donker met één simpele glans, geen witte ring.
    for sz in (1, -1):
        d = np.array((OOG[0], OOG[1], OOG[2] * sz)); d /= np.linalg.norm(d)
        e = cr + d * kop_r * 0.80
        m.ell(e, OOG[3], 'oog')
        m.ell(e + d * OOG[3][0] * 0.82 + np.array((-0.5, 3.4, 0.0)), 1.9, 'glint')
    # geen neus, snuit of tint: tussen de ogen alleen witte wol (ronde 5, bovenste helft foto_sprieten_plus_vilt)
    # kamsprieten opzij als oren
    for sz in (1, -1):
        spriet(m, cr + np.array((-2.0, 9.0, 13.0 * sz)), sz, sz < 0)
    Rh = P.rot_y(math.radians(kop_extra)); piv = np.array((-5.0, 36.0, 0.0))
    m.parts[h0:] = [(piv + Rh @ (c - piv), r, Rh @ R0, g) for c, r, R0, g in m.parts[h0:]]
    return m


def gebruik_kleuren():
    L.COL.clear(); L.COL.update(COL)
    L.NOSHADE.clear(); L.NOSHADE.update(NOSHADE)
    L.LINED.clear(); L.LINED.update(LINED)


ADERGROEP = {'ader': 'vleugel', 'aderver': 'vlver'}


def shade_aders(zb, gid, nrm, groups, out):
    """L.shade, maar de adertjes tellen voor de lijnen als hun vleugel (anders krijgt elk adertje een zwarte rand);
    daarna worden de aderpixels die geen lijn zijn in de aderkleur gezet."""
    g2 = gid.copy()
    ader = np.zeros(gid.shape, bool); kleur = np.zeros(gid.shape + (3,), np.float32)
    for ag, vg in ADERGROEP.items():
        i = groups.index(ag); mm = gid == i
        ader |= mm; kleur[mm] = P.hexc(COL[ag]); g2[mm] = groups.index(vg)
    img, a = L.shade(zb, g2, nrm, groups, L.R)
    arr = np.array(img).astype(np.float32)
    lijn = np.all(np.abs(arr - L.LINE) < 2, axis=-1)
    zet = ader & ~lijn
    arr[zet] = kleur[zet]
    return Image.fromarray(arr.clip(0, 255).astype(np.uint8)).resize((out, out), Image.LANCZOS), a


def view(m, yaw=YAW, pitch=8, out=256, size=236):
    Rc = P.rot_x(math.radians(pitch)) @ P.rot_y(math.radians(yaw))
    pts = np.array([Rc @ c for c, r, R0, g in m.parts]); rs = np.array([r.max() for c, r, R0, g in m.parts])
    x0, x1, y0, y1 = (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()
    scale = L.R * (size / 256) / max(x1 - x0, y1 - y0)
    zb, gid, nrm, groups = L.render(m, yaw, pitch, scale, ((x0 + x1) / 2, (y0 + y1) / 2))
    img, a = shade_aders(zb, gid, nrm, groups, out)
    return img, a, gid, groups


def kopaandeel(m, yaw=YAW, pitch=8):
    """Kop (incl. sprieten) / hoogte zonder vleugels, en / totale hoogte."""
    Rc = P.rot_x(math.radians(pitch)) @ P.rot_y(math.radians(yaw))
    yy = [((Rc @ c)[1] - r.max(), (Rc @ c)[1] + r.max(), g, c) for c, r, R0, g in m.parts]
    lo = min(y[0] for y in yy)
    hi_all = max(y[1] for y in yy)
    hi_body = max(y[1] for y in yy if y[2] not in ('vleugel', 'achtervl', 'vlver', 'achtver'))
    kop = [y for y in yy if y[3][1] > 39 and y[2] not in ('vleugel', 'achtervl', 'vlver', 'achtver')]
    kh = max(y[1] for y in kop) - min(y[0] for y in kop if y[2] == 'wol')
    return kh / (hi_body - lo), kh / (hi_all - lo)


def een_x(img, a):
    """Poppetje naar 64x64 (1x), zoals een sprite in het kader (zelfde vulling als de view)."""
    im = img.convert('RGBA'); al = Image.fromarray((a * 255).astype(np.uint8)).resize(img.size, Image.BOX)
    im.putalpha(al)
    s = im.resize((64, 64), Image.BOX); arr = np.array(s); arr[..., 3] = np.where(arr[..., 3] > 110, 255, 0)
    return Image.fromarray(arr)


def gen3(n):
    p = Image.open(os.path.join(ROOT, 'graphics/pokemon', n, 'anim_front.png')); idx = np.array(p)[:64, :64]
    rgba = np.array(p.convert('RGBA'))[:64, :64]; rgba[idx == 0, 3] = 0
    return Image.fromarray(rgba)


def vel():
    gebruik_kleuren()
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
    m = poedelmot()
    img, a, gid, groups = view(m, out=320)
    img.save(os.path.join(HERE, 'poppetje_45.png'))  # ronde 4
    e = een_x(img, a); e.save(os.path.join(HERE, 'poppetje_45_1x.png'))
    kb, kt = kopaandeel(m)
    W, H = 12 + 2 * 332 + 12, 44 + 320 + 30 + 2 * 72 + 40 + 230
    out = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(out)
    d.text((12, 12), 'Poedelmot: poppetje op 45° (praatplaat), naast de tak-foto', font=FB, fill=(30, 30, 30))
    foto = Image.open(os.path.join(HERE, '../../referenties/foto_tak_katoen.webp')).convert('RGB').resize((320, 320))
    out.paste(foto, (12, 44)); d.text((12, 44 + 322), 'tak-foto (enige bron)', font=F, fill=(60, 60, 60))
    out.paste(img, (12 + 332, 44))
    d.text((12 + 332, 44 + 322), f'poppetje 45°: kop {kb:.0%} van de hoogte zonder vleugels ({kt:.0%} met)', font=F, fill=(60, 60, 60))
    y = 44 + 320 + 30
    d.text((12, y), '1x, zelfde schaal: poppetje, butterfree, venomoth, volbeat, teddiursa (licht / donker)', font=F, fill=(0, 0, 0))
    x = 12
    for im1 in [e] + [gen3(n) for n in ('butterfree', 'venomoth', 'volbeat', 'teddiursa')]:
        for j, bg in enumerate(((235, 235, 235), (60, 60, 70))):
            b = Image.new('RGB', (64, 64), bg); b.paste(im1, (0, 0), im1); out.paste(b, (x, y + 20 + j * 72))
        x += 72
    # kopstudie (ronde 4): Venomoth, tak-foto en de kop van het poppetje naast elkaar
    y = 44 + 320 + 30 + 2 * 72 + 30
    d.text((12, y), 'kopstudie: venomoth (4x), tak-foto, poppetje-kop (werkformaat) en op 1x (4x)', font=F, fill=(0, 0, 0))
    v = gen3('venomoth').crop((2, 18, 38, 54)).resize((180, 180), Image.NEAREST)
    b = Image.new('RGB', v.size, (235, 235, 235)); b.paste(v, (0, 0), v); out.paste(b, (12, y + 20))
    fk = Image.open(os.path.join(HERE, '../../referenties/foto_tak_katoen.webp')).convert('RGB').crop((720, 620, 1180, 1080)).resize((180, 180))
    out.paste(fk, (12 + 190, y + 20))
    kk = img.crop((30, 40, 210, 220)).resize((180, 180)); out.paste(kk, (12 + 380, y + 20))
    k1 = e.crop((4, 6, 40, 42)).resize((112, 112), Image.NEAREST)
    b = Image.new('RGB', k1.size, (235, 235, 235)); b.paste(k1, (0, 0), k1); out.paste(b, (12 + 570, y + 20))
    out.save(os.path.join(HERE, 'vel.png'))
    print('kop/hoogte zonder vleugels %.2f, met vleugels %.2f' % (kb, kt))


if __name__ == '__main__':
    vel()
