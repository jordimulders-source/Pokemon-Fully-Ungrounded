"""Poedelmot (eindvorm, Bug/Fairy): 3D-poppetje als praatplaat, op de lama-manier (Jordi 5 nov: "ga maar de lama kant op
qua bouwen ipv in blender"). Gedeelde bibliotheek: olinguito_v2/silhouet_kolibriemethode/pop3d.py (Model, ell, chain);
render/shade/fluff uit lama/ontwerp/pop3d_lama.py (vlakke kleuren, één schaduwtoon, lijnen op dieptesprongen).
Diercoördinaten zoals de lama: x = naar achteren (snuit naar -x), y = omhoog, z = naar de kijker bij 0° (nabije kant +z).
Bron = alleen de tak-foto (referenties/foto_tak_katoen.webp): rechtop zittend, dik en wollig, pompon-poten, V-vleugels.
Hoek 45° (bevroren, Jordi). Kopverhouding uit de posestudie (posestudie.png): kop ±45% van de hoogte zonder vleugels.
Draaien vanuit de repo-root: python3 docs/concept/sprites/poedelmot/poppetje/pop3d_poedelmot.py"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../../../..'))
sys.path.insert(0, os.path.join(HERE, '../../olinguito_v2/silhouet_kolibriemethode'))
sys.path.insert(0, os.path.join(HERE, '../../lama/ontwerp'))
import pop3d as P
import pop3d_lama as L

YAW = 45                      # bevroren (Jordi: "ja 45 graden is oke")
KOP_EXTRA = 14                # kop draait meer naar de kijker dan het lijf
COL = {
    'wol': '#F3EFE7', 'wolver': '#D6CFC2', 'pompon': '#FBF8F2', 'pomver': '#DCD5C8',
    'vleugel': '#ECE6D9', 'achtervl': '#E0D8C8', 'vlver': '#CFC7B7', 'achtver': '#C4BBAA',
    'spriet': '#7A5234', 'sprietver': '#5E3F28', 'snuit': '#8C603E', 'oog': '#1E1A24', 'glint': '#FFFFFF',
}
NOSHADE = {'oog', 'glint'}
LINED = {'oog', 'snuit', 'spriet', 'sprietver', 'vleugel', 'achtervl', 'vlver', 'achtver'}


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


def voorvl(t):     # lang, smal, spits (tak-foto)
    return 3.5 + 8.5 * math.sin(math.pi * min(t / 0.62, 1) * 0.5) if t < 0.62 else 0.8 + 11.2 * (1 - (t - 0.62) / 0.38) ** 1.5


def achtervl(t):   # kleiner, rond
    return 3.0 + 15.0 * math.sin(math.pi * t) ** 0.6


def spriet(m, basis, kant, ver):
    """Kamspriet als oor: gebogen schacht opzij (z), licht omhoog gekruld, met tanden boven en onder (bipectinaat)."""
    g = 'sprietver' if ver else 'spriet'
    pts = []
    for i in range(13):
        t = i / 12
        pts.append(np.array(basis) + np.array((2.0 * t, 3.0 * t + 9.0 * t ** 2.5, kant * 30.0 * t)))
    m.chain([tuple(p) + (2.0 - 1.1 * i / 12,) for i, p in enumerate(pts)], g, 1.0)
    for i in range(1, 12):
        t = i / 12
        p = pts[i]
        lang = 7.5 * math.sin(math.pi * min(1.0, 0.25 + 0.85 * t)) ** 0.7 * (1.15 - 0.8 * t) + 0.8
        rich = pts[min(i + 1, 12)] - pts[i]; rich /= np.linalg.norm(rich)
        for s in (1, -1):
            d = np.array((0.15, s * 1.0, 0.0)) + rich * 0.45
            d /= np.linalg.norm(d)
            c = p + d * lang * 0.55
            u = d; w = np.array((1.0, 0, 0)); w -= (w @ u) * u; w /= np.linalg.norm(w)
            m.ell(c, (lang * 0.55, 0.75, 0.75), g, np.column_stack([u, np.cross(w, u), w]))


def poedelmot(kop_r=19.0, kop_extra=KOP_EXTRA):
    m = P.Model()
    # vleugels eerst (achter het lijf): per kant voor- en achtervleugel die overlappen tot één paar, samen in een V.
    # Symmetrisch; de V staat ver genoeg open dat de verre punt in 45° naast de kop eindigt, niet erboven.
    for kant in (1, -1):
        ver = kant < 0
        w = np.array((10.0, 43.0, 7.0 * kant))
        u = np.array((0.22, 0.46, 0.86 * kant))
        blad(m, w, u, (1.0, 0.0, 0.0), 70, voorvl, 1.4, 'vlver' if ver else 'vleugel', 18)
        ua = np.array((0.35, 0.05, 0.94 * kant))
        blad(m, w + np.array((3.0, -6.0, 0.0)), ua, (1.0, 0.3, 0.0), 44, achtervl, 1.4,
             'achtver' if ver else 'achtervl', 12)
    # lijf: dik en wollig, rechtop zittend (achterlijf laag en breed op de grond, borst erboven)
    for c, r, s in (((10, 17, 0), (22, 17, 21), 1), ((-3, 30, 0), (18, 14, 19), 2), ((-10, 17, 0), (14, 12, 16), 3)):
        m.ell(c, r, 'wol')
        L.fluff(m, c, r, 'wol', 55, 6.5, s, ymin=-0.5)
    # wolkraag tussen kop en lijf
    for i, a in enumerate(np.linspace(0, 2 * math.pi, 16, endpoint=False)):
        m.ell((-5 + 15 * math.cos(a), 42 + (i % 2) * 1.5, 18 * math.sin(a)), 6.4, 'wol')
    # zes poten aan de borst; voorpaar grootst, hangt naar voren en omlaag; middenpaar opzij; achterpaar onder het lijf
    POTEN = [  # (punten x,y,z,r), pompon-straal
        ([(-15, 29, 9, 7.2), (-29, 21, 13, 6.8), (-28, 10, 14, 6.4)], 10.5),     # voor: knie naar voren, voet eronder
        ([(-15, 29, -9, 7.2), (-29, 21, -13, 6.8), (-28, 10, -14, 6.4)], 10.5),
        ([(-4, 27, 15, 6.6), (-8, 21, 26, 6.2), (-10, 9, 28, 5.8)], 9.0),         # midden: opzij
        ([(-4, 27, -15, 6.6), (-8, 21, -26, 6.2), (-10, 9, -28, 5.8)], 9.0),
        ([(10, 22, 14, 6.2), (16, 15, 23, 5.8), (14, 8, 24, 5.4)], 8.4),          # achter: onder lijf/vleugels
        ([(10, 22, -14, 6.2), (16, 15, -23, 5.8), (14, 8, -24, 5.4)], 8.4),
    ]
    for i, (pts, pr) in enumerate(POTEN):
        poot(m, pts, pr, pts[0][2] < 0, 20 + 10 * i)
    # kop: groot, rond, wollig, op de kraag; draait extra naar de kijker
    h0 = len(m.parts)
    cr = np.array((-9.0, 59.0, 0.0))
    kr = np.array((kop_r, kop_r * 0.95, kop_r))
    m.ell(cr, kr, 'wol')
    L.fluff(m, cr, kr, 'wol', 34, 5.0, 77, ymin=-0.3)
    # grote bolle ogen, niet tegen elkaar (snuitvlak ertussen)
    for sz in (1, -1):
        d = np.array((-0.80, 0.02, 0.60 * sz)); d /= np.linalg.norm(d)
        e = cr + d * kop_r * 0.86
        m.ell(e, (7.6, 8.2, 7.6), 'oog')
        m.ell(e + d * 6.0 + np.array((0.5, 3.2, 0.0)), 1.8, 'glint')
    # bruin snuitvlak tussen en onder de ogen
    m.ell(cr + np.array((-kop_r * 0.90, -6.5, 0.0)), (2.4, 6.5, 4.4), 'snuit')
    # kamsprieten opzij als oren
    for sz in (1, -1):
        spriet(m, cr + np.array((-2.0, 9.0, 13.0 * sz)), sz, sz < 0)
    Rh = P.rot_y(math.radians(kop_extra)); piv = np.array((-5.0, 42.0, 0.0))
    m.parts[h0:] = [(piv + Rh @ (c - piv), r, Rh @ R0, g) for c, r, R0, g in m.parts[h0:]]
    return m


def gebruik_kleuren():
    L.COL.clear(); L.COL.update(COL)
    L.NOSHADE.clear(); L.NOSHADE.update(NOSHADE)
    L.LINED.clear(); L.LINED.update(LINED)


def view(m, yaw=YAW, pitch=8, out=256, size=236):
    Rc = P.rot_x(math.radians(pitch)) @ P.rot_y(math.radians(yaw))
    pts = np.array([Rc @ c for c, r, R0, g in m.parts]); rs = np.array([r.max() for c, r, R0, g in m.parts])
    x0, x1, y0, y1 = (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()
    scale = L.R * (size / 256) / max(x1 - x0, y1 - y0)
    zb, gid, nrm, groups = L.render(m, yaw, pitch, scale, ((x0 + x1) / 2, (y0 + y1) / 2))
    img, a = L.shade(zb, gid, nrm, groups, out)
    return img, a, gid, groups


def kopaandeel(m, yaw=YAW, pitch=8):
    """Kop (incl. sprieten) / hoogte zonder vleugels, en / totale hoogte."""
    Rc = P.rot_x(math.radians(pitch)) @ P.rot_y(math.radians(yaw))
    yy = [((Rc @ c)[1] - r.max(), (Rc @ c)[1] + r.max(), g, c) for c, r, R0, g in m.parts]
    lo = min(y[0] for y in yy)
    hi_all = max(y[1] for y in yy)
    hi_body = max(y[1] for y in yy if y[2] not in ('vleugel', 'achtervl', 'vlver', 'achtver'))
    kop = [y for y in yy if y[3][1] > 45 and y[2] not in ('vleugel', 'achtervl', 'vlver', 'achtver')]
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
    img.save(os.path.join(HERE, 'poppetje_45.png'))
    e = een_x(img, a); e.save(os.path.join(HERE, 'poppetje_45_1x.png'))
    kb, kt = kopaandeel(m)
    W, H = 12 + 2 * 332 + 12, 44 + 320 + 30 + 2 * 72 + 40
    out = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(out)
    d.text((12, 12), 'Poedelmot: poppetje op 45° (praatplaat), naast de tak-foto', font=FB, fill=(30, 30, 30))
    foto = Image.open(os.path.join(HERE, '../referenties/foto_tak_katoen.webp')).convert('RGB').resize((320, 320))
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
    out.save(os.path.join(HERE, 'vel.png'))
    print('kop/hoogte zonder vleugels %.2f, met vleugels %.2f' % (kb, kt))


if __name__ == '__main__':
    vel()
