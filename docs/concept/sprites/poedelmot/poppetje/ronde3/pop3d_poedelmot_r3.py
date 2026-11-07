"""Poedelmot (eindvorm, Bug/Fairy): 3D-poppetje als praatplaat, op de lama-manier (Jordi 5 nov: "ga maar de lama kant op
qua bouwen ipv in blender"). Gedeelde bibliotheek: olinguito_v2/silhouet_kolibriemethode/pop3d.py (Model, ell, chain);
render/shade/fluff uit lama/ontwerp/pop3d_lama.py (vlakke kleuren, één schaduwtoon, lijnen op dieptesprongen).
Diercoördinaten zoals de lama: x = naar achteren (snuit naar -x), y = omhoog, z = naar de kijker bij 0° (nabije kant +z).
Bron = alleen de tak-foto (referenties/foto_tak_katoen.webp): rechtop zittend, dik en wollig, pompon-poten, V-vleugels.
Hoek 45° (bevroren, Jordi). Kopverhouding uit de posestudie (posestudie.png): kop ±45% van de hoogte zonder vleugels.
Ronde 2 (Jordi: "poten mogen dunner, de voelsprieten mogen groter, zoals op de andere fotos, vleugels ook" + keurder):
poten iets dunner maar wollig, voorpaar gespreid met knik, lijf lager, pompons in perspectief, middenpaar opzij; sprieten
en vleugels groter; verre achtervleugel met gladde rand; snuit breed en plat (neusbrug). Rest = ronde 1 (../pop3d_poedelmot.py).
Ronde 3 (opdracht: alleen poten, verre achtervleugel, dubbele kam; rest = ronde 2 ../ronde2/pop3d_poedelmot_r2.py):
poten nagebouwd naar de overlay op de tak-foto (overlay_poten.png): zes poten uit de borst die als een waaier uitlopen,
voeten ver uit elkaar met lucht ertussen, lijf laag maar niet op de grond; nabij lager en groter, ver hoger en kleiner.
Verre achtervleugel opzij gedraaid zodat hij links naast het lijf onder de verre voorvleugel uitsteekt (gladde rand).
Sprieten: tanden aan beide kanten, in het vlak loodrecht op de kijkrichting (dubbele kam, foto_sprieten_plus_vilt.png).
Draaien vanuit de repo-root: python3 docs/concept/sprites/poedelmot/poppetje/ronde3/pop3d_poedelmot_r3.py"""
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
    'spriet': '#7A5234', 'sprietver': '#5E3F28', 'snuit': '#8C603E', 'oog': '#1E1A24', 'glint': '#FFFFFF',
}
NOSHADE = {'oog', 'glint'}
LINED = {'oog', 'snuit', 'spriet', 'sprietver', 'vleugel', 'achtervl', 'vlver', 'achtver'}


def poot(m, pts, pr, ver, seed, nfluff=7):
    """Gelede insectenpoot (heup, knie, voet), over de hele lengte dik en wollig, pompon onderaan (poedelknip).
    Ronde 3: wolbobbels op de gewrichten én halverwege elk segment, maar klein (≤ half de pootstraal), zodat de poot
    wollig blijft en toch een eigen omtrek houdt met lucht tussen de poten; de pompon staat óp de voet."""
    g, gp = ('wolver', 'pomver') if ver else ('wol', 'pompon')
    m.chain(pts, g, 1.6)
    for (xa, ya, za, ra), (xb, yb, zb, rb) in zip(pts, pts[1:]):   # extra wol halverwege elk segment
        L.fluff(m, ((xa + xb) / 2, (ya + yb) / 2, (za + zb) / 2), ((ra + rb) / 2,) * 3, g, nfluff, (ra + rb) * 0.25, seed + 5)
    for i, (x, y, z, r) in enumerate(pts[:-1]):
        L.fluff(m, (x, y, z), (r, r, r), g, nfluff, r * 0.5, seed + i)
    x, y, z, _ = pts[-1]
    c = (x, y + pr * 0.85, z)
    m.ell(c, (pr, pr * 0.88, pr), gp)
    L.fluff(m, c, (pr * 0.95, pr * 0.85, pr * 0.95), gp, 12, pr * 0.36, seed + 9)


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
    return 4.5 + 11.0 * math.sin(math.pi * min(t / 0.62, 1) * 0.5) if t < 0.62 else 0.8 + 14.7 * (1 - (t - 0.62) / 0.38) ** 1.5


def achtervl(t):   # kleiner, rond
    return 3.0 + 15.0 * math.sin(math.pi * t) ** 0.6


KIJK = np.array((-math.sin(math.radians(YAW)), 0.0, math.cos(math.radians(YAW))))   # naar de kijker, diercoördinaten


def spriet(m, basis, kant, ver):
    """Kamspriet als oor: gebogen schacht opzij (z), licht omhoog gekruld. Ronde 3: dubbele kam (bipectinaat): per punt
    twee tanden, naar beide kanten van de schacht, in het vlak loodrecht op de kijkrichting en iets naar de punt
    gericht, zoals een veertje (foto_sprieten_plus_vilt.png). Langste tanden in het midden."""
    g = 'sprietver' if ver else 'spriet'
    pts = []
    for i in range(13):
        t = i / 12
        pts.append(np.array(basis) + np.array((3.0 * t, 5.0 * t + 15.0 * t ** 2.2, kant * 44.0 * t)))   # lange boog opzij, omhoog
    m.chain([tuple(p) + (2.4 - 1.4 * i / 12,) for i, p in enumerate(pts)], g, 1.0)
    for i in range(1, 12):
        t = i / 12
        p = pts[i]
        lang = 10.0 * math.sin(math.pi * min(1.0, 0.15 + 0.95 * t)) ** 0.8 + 1.0
        rich = pts[min(i + 1, 12)] - pts[i]; rich /= np.linalg.norm(rich)
        zij = np.cross(rich, KIJK); zij /= np.linalg.norm(zij)
        for s in (1, -1):
            d = zij * s + rich * 0.55
            d /= np.linalg.norm(d)
            c = p + d * lang * 0.55
            u = d; w = KIJK - (KIJK @ u) * u; w /= np.linalg.norm(w)
            m.ell(c, (lang * 0.55, 0.85, 0.85), g, np.column_stack([u, np.cross(w, u), w]))


# Lijf (centrum, stralen, zaad). Borst = ronde 2; achterlijf iets hoger (onderkant y 2 i.p.v. -1); borstwol smaller en
# lager zodat ze tussen de voorpoten hangt zonder de lucht tussen de poten te vullen. Voeten op y −12 (nabij) tot −5 (ver).
ACHTERVL_VER = (-0.3, 0.08, -0.95)   # richting verre achtervleugel (ronde 3)
LIJF = (((10, 16, 0), (22, 14, 21), 1), ((-3, 25, 0), (18, 13, 19), 2), ((-12, 11, 0), (10, 9, 11), 3))

def op45(sx, y, d, r):
    """Punt opgeven zoals het op 45° in beeld komt: sx = links/rechts in beeld, d = diepte (+ = naar de kijker).
    Terug naar diercoördinaten: x = 0,71·(sx − d), z = 0,71·(sx + d). Zo staan de voeten waar de overlay ze wil."""
    k = math.sqrt(0.5)
    return (k * (sx - d), y, k * (sx + d), r)


# Zes poten naar de overlay op de tak-foto (overlay_poten.png). Op de foto lopen de poten als een waaier uit de borst:
# dij schuin naar buiten, knie naar buiten/voren, onderbeen weer iets naar binnen omlaag, voeten ver uit elkaar met donkere
# lucht ertussen; het lijf hangt laag tussen de poten. Van links naar rechts in beeld: verre voorpoot, verre middenpoot
# (half achter de nabije voorpoot), nabije voorpoot (laagst, grootst), verre achterpoot (piept tussen de poten door),
# nabije middenpoot, nabije achterpoot. Ver = hoger, kleiner en in de schaduwtint; nabij = lager en groter.
# (heup, knie, voet) via op45(sx, y, diepte, straal); dan pompon-straal en ver.
POTEN = [
    ([op45(-8, 26, 14, 5.0), op45(-22, 14, 26, 4.8), op45(-14, -12, 30, 4.4)], 8.6, False),   # voor nabij
    ([op45(-16, 27, 0, 4.6), op45(-31, 13, 2, 4.4), op45(-37, -7, 0, 3.8)], 6.6, True),      # voor ver
    ([op45(-8, 26, -10, 4.2), op45(-21, 14, -10, 4.0), op45(-25, -4, -12, 3.6)], 6.0, True),  # midden ver
    ([op45(4, 24, 14, 4.8), op45(15, 14, 24, 4.6), op45(12, -11, 28, 4.2)], 7.8, False),      # midden nabij
    ([op45(12, 22, 4, 4.6), op45(30, 12, 8, 4.4), op45(34, -10, 6, 4.0)], 7.2, False),        # achter nabij
    ([op45(2, 24, -16, 4.0), op45(4, 13, -18, 3.8), op45(-1, -5, -20, 3.4)], 5.4, True),      # achter ver
]


def poedelmot(kop_r=19.0, kop_extra=KOP_EXTRA, pootkleur=False):
    m = P.Model()
    # vleugels eerst (achter het lijf): per kant voor- en achtervleugel die overlappen tot één paar, samen in een V.
    # Symmetrisch; de V staat ver genoeg open dat de verre punt in 45° naast de kop eindigt, niet erboven.
    for kant in (1, -1):
        ver = kant < 0
        w = np.array((10.0, 37.0, 7.0 * kant))
        u = np.array((0.22, 0.46, 0.86 * kant))
        blad(m, w, u, (1.0, 0.0, 0.0), 86, voorvl, 1.4, 'vlver' if ver else 'vleugel', 20)
        # ronde 3: de verre achtervleugel naar voren-opzij gedraaid (in 45° naar links), zodat hij naast het lijf onder de
        # verre voorvleugel uitsteekt in plaats van er recht achter te verdwijnen; de nabije is ronde 2
        ua = np.array((0.35, 0.05, 0.94 * kant)) if not ver else np.array(ACHTERVL_VER)
        # achtervleugel: één gladde ronde vorm (geen keten: de rand blijft glad, leest niet als wolklont)
        ua = ua / np.linalg.norm(ua); wa = np.array((1.0, 0.3, 0.0)); wa -= (wa @ ua) * ua; wa /= np.linalg.norm(wa)
        Ra = np.column_stack([ua, np.cross(wa, ua), wa])
        m.ell(w + np.array((3.0, -6.0, 0.0)) + ua * 28.0, (29.0, 19.0, 1.4), 'achtver' if ver else 'achtervl', Ra)
    # lijf: dik en wollig, rechtop zittend. Ronde 3: het achterlijf rust niet meer op de grond en de lage buikwol tussen de
    # voorpoten is weg (die vulden de ruimte tussen de poten tot één wolmassa); het lijf hangt laag tússen de poten, met
    # de onderkant net boven de pompons, zoals op de tak-foto (overlay_poten.png).
    for c, r, s in LIJF:
        m.ell(c, r, 'wol')
        L.fluff(m, c, r, 'wol', 55, 6.5, s, ymin=-0.5)
    # wolkraag tussen kop en lijf
    for i, a in enumerate(np.linspace(0, 2 * math.pi, 16, endpoint=False)):
        m.ell((-5 + 15 * math.cos(a), 36 + (i % 2) * 1.5, 18 * math.sin(a)), 6.4, 'wol')
    for i, (pts, pr, ver) in enumerate(POTEN):
        n0 = len(m.parts)
        poot(m, pts, pr, ver, 20 + 10 * i)
        if pootkleur:   # controlevel: elke poot een eigen kleur (zelfde kleuren als op de overlay)
            m.parts[n0:] = [(c, r, R0, f'p{i}') for c, r, R0, g in m.parts[n0:]]
    # kop: groot, rond, wollig, op de kraag; draait extra naar de kijker
    h0 = len(m.parts)
    cr = np.array((-9.0, 53.0, 0.0))
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
    # neusbrug zoals op de foto: smal tussen de ogen, onderaan breed en plat (geen bolletje, geen driehoekje)
    m.ell(cr + np.array((-kop_r * 0.95, -1.0, 0.0)), (1.6, 6.0, 3.0), 'snuit')
    m.ell(cr + np.array((-kop_r * 0.90, -6.5, 0.0)), (1.6, 3.0, 6.4), 'snuit')
    # kamsprieten opzij als oren
    for sz in (1, -1):
        spriet(m, cr + np.array((-2.0, 9.0, 13.0 * sz)), sz, sz < 0)
    Rh = P.rot_y(math.radians(kop_extra)); piv = np.array((-5.0, 36.0, 0.0))
    m.parts[h0:] = [(piv + Rh @ (c - piv), r, Rh @ R0, g) for c, r, R0, g in m.parts[h0:]]
    return m


# per poot (volgorde van POTEN) de kleur op de overlay en de naam op de foto
POOTKLEUR = ['#E0302A', '#F08A1C', '#2EA84A', '#2A7FE0', '#A040E0', '#E040A0']
POOTNAAM = ['voor nabij', 'voor ver', 'midden ver', 'midden nabij', 'achter nabij', 'achter ver']
# Overlay op foto_tak_katoen.webp (1500×1500): per zichtbare poot heup, knie, voet, pompon (met de hand afgelezen op
# 3× uitvergrote, contrastrijke uitsneden). De moth kijkt op de foto recht naar de camera: links in beeld = zijn rechterkant
# = de verre kant op 45°, rechts in beeld = de nabije kant. De verre achterpoot is op de foto niet te zien.
FOTO_POTEN = {
    1: [(745, 965), (725, 1060), (705, 1185), (690, 1222)],      # links voor   -> voor ver
    2: [(705, 990), (640, 1090), (600, 1185), (582, 1215)],      # links midden -> midden ver
    0: [(950, 1000), (985, 1100), (1000, 1185), (1002, 1215)],   # rechts voor  -> voor nabij
    3: [(1040, 995), (1100, 1075), (1110, 1200), (1108, 1238)],  # rechts midden -> midden nabij
    4: [(1120, 1000), (1180, 1040), (1220, 1135), (1225, 1160)], # rechts achter (gespreid) -> achter nabij
}
FOTO_LUCHT = [(820, 1150), (1050, 1150), (1165, 1110)]          # donkere lucht tussen de poten
FOTO_LIJF = [(760, 1150), (960, 1170), (1120, 1110)]            # onderkant van het lijf (hangt tussen de poten)


def overlay():
    """overlay_poten.png: de poten op de tak-foto nagetrokken, naast het poppetje met dezelfde kleur per poot."""
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
    foto = Image.open(os.path.join(HERE, '../../referenties/foto_tak_katoen.webp')).convert('RGB')
    x0, y0, x1, y1 = 480, 640, 1320, 1330
    k = 0.5
    crop = foto.crop((x0, y0, x1, y1)).resize((int((x1 - x0) * k), int((y1 - y0) * k)), Image.LANCZOS)
    d = ImageDraw.Draw(crop)
    T = lambda p: ((p[0] - x0) * k, (p[1] - y0) * k)
    d.line([T(p) for p in FOTO_LIJF], fill=(255, 255, 255), width=1)
    for i, pts in FOTO_POTEN.items():
        c = P.hexc(POOTKLEUR[i]).astype(int).tolist(); c = tuple(c)
        q = [T(p) for p in pts]
        d.line(q[:3], fill=c, width=4)
        for j, (x, y) in enumerate(q[:3]):
            rr = 4 if j < 2 else 3
            d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=c, outline=(0, 0, 0))
        x, y = q[3]; d.ellipse((x - 9, y - 6, x + 9, y + 6), outline=c, width=3)
    for p in FOTO_LUCHT:
        x, y = T(p); d.text((x - 4, y - 7), '*', font=FB, fill=(255, 255, 0))
    gebruik_kleuren()
    L.COL.update({f'p{i}': c for i, c in enumerate(POOTKLEUR)})
    img, a, _, _ = view(poedelmot(pootkleur=True), out=crop.size[1])
    W = max(12 + crop.size[0] + 12 + img.size[0] + 12, 940)
    out = Image.new('RGB', (W, 44 + crop.size[1] + 120), 'white'); dd = ImageDraw.Draw(out)
    dd.text((12, 12), 'Poedelmot ronde 3: poten nagetrokken op de tak-foto -> poppetje 45° (zelfde kleur = zelfde poot)', font=FB, fill=(30, 30, 30))
    out.paste(crop, (12, 44)); out.paste(img, (24 + crop.size[0], 44))
    y = 44 + crop.size[1] + 8
    dd.text((12, y), 'stip = heup, knie, voet; ring = pompon; * = donkere lucht tussen de poten; witte lijn = onderkant lijf', font=F, fill=(40, 40, 40))
    for i, n in enumerate(POOTNAAM):
        xx = 12 + (i % 3) * 230; yy = y + 24 + (i // 3) * 20
        dd.rectangle((xx, yy + 2, xx + 12, yy + 14), fill=POOTKLEUR[i])
        extra = '' if i in FOTO_POTEN else ' (op de foto verborgen)'
        dd.text((xx + 18, yy), n + extra, font=F, fill=(40, 40, 40))
    dd.text((12, y + 72), 'Foto: links in beeld = rechterkant van de mot = verre kant op 45°. Voorpoten lang en geknikt, voeten ver uit elkaar, lijf laag ertussen.', font=F, fill=(40, 40, 40))
    out.save(os.path.join(HERE, 'overlay_poten.png'))


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
    img.save(os.path.join(HERE, 'poppetje_45.png'))  # ronde 3
    e = een_x(img, a); e.save(os.path.join(HERE, 'poppetje_45_1x.png'))
    kb, kt = kopaandeel(m)
    W, H = 12 + 2 * 332 + 12, 44 + 320 + 30 + 2 * 72 + 40
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
    out.save(os.path.join(HERE, 'vel.png'))
    print('kop/hoogte zonder vleugels %.2f, met vleugels %.2f' % (kb, kt))


if __name__ == '__main__':
    overlay()
    vel()
