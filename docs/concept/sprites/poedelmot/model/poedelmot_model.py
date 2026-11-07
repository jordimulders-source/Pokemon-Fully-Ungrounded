"""Poedelmot (eindvorm): 3D-poppetje voor de 3/4-keuze (Jordi 5 nov: "maak maar eerst een model en dan draaien we die
driekwart"). Geen Blender in deze container: zelfde principe als kolibrie_pre.py (huid = smooth union van afstandsvelden,
één huid, geen losse bollen), maar direct in numpy gerenderd (orthografisch, sphere tracing, lambert-licht linksboven).
Eenheden ~ spritepixels: het 64x64-kader is 64 eenheden. Grond op y=0, dier kijkt naar +z (naar de kijker bij 0 graden).

Vorm (coördinator, punten 1-5 + SPEC):
 1. per kant één vleugelpaar (voorvleugel + achtervleugel overlappen), samen in een V omhoog en naar achteren;
    geen vleugelpunt recht boven de kop;
 2. kop = eigen bol op het wollige lijf, met een wolkraag ertussen; kop draait extra naar de kijker (KOP_MEE);
 3. sprieten = kamvormige oren opzij, iets omhoog, vóór de vleugels;
 4. vier pompon-poten (poedelknip): wollige bovenpoot, dun enkeltje, pompon; achterste paar verder naar achteren;
 5. grote ronde donkere ogen (Venomoth-achtig), bruin snuitje.
Draaien: python3 docs/concept/sprites/poedelmot/model/poedelmot_model.py   -> rondom_vel.png + renders/"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FOTO = os.path.join(HERE, '../referenties/foto_tak_katoen.webp')
KADER = 64.0                    # eenheden per beeld (= 64 spritepx)
MIDDEN_Y = 29.0
MIDDEN_X = -3.0                 # kader iets naar links: de kop steekt in 3/4 naar links uit
KOP_MEE = 0.3                   # kop draait 30% van de lijfdraai terug naar de kijker (Gen 3-regel)

# kleuren per materiaal
KLEUR = {'wol': (238, 234, 226), 'vleugel': (214, 208, 196), 'achtervl': (196, 190, 178), 'oor': (128, 86, 52),
         'oog': (30, 28, 38), 'snuit': (160, 118, 84)}


def rot_y(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rot_x(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def rot_z(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def ell(P, c, r, R=None):
    """Ellipsoïde (benaderd afstandsveld). R = rotatie model->lokaal (rijen = lokale assen)."""
    q = P - np.asarray(c, float)
    if R is not None:
        q = q @ R.T
    r = np.asarray(r, float)
    k0 = np.linalg.norm(q / r, axis=1)
    k1 = np.linalg.norm(q / (r * r), axis=1)
    return k0 * (k0 - 1.0) / np.maximum(k1, 1e-6)


def capsule(P, a, b, ra, rb):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ba = b - a
    h = np.clip(((P - a) @ ba) / (ba @ ba), 0, 1)
    return np.linalg.norm(P - (a + h[:, None] * ba), axis=1) - (ra + (rb - ra) * h)


def smin(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)


def assen(richting, voorkant):
    """Lokale assen: u = langs de vleugel/het oor, w = normaal van het vlak (ongeveer 'voorkant'), v = u x w."""
    u = np.asarray(richting, float); u /= np.linalg.norm(u)
    w = np.asarray(voorkant, float); w = w - (w @ u) * u; w /= np.linalg.norm(w)
    v = np.cross(w, u)
    return np.stack([u, v, w])


# ---------- het model ----------
POTEN = [  # heup, knie, enkel, pompon (midden, straal); dier-rechts = -x
    ((-5.5, 8, 6), (-7.0, 6.0, 12.0), (-7.5, 4.6, 14.0), (-7.8, 3.9, 15.0), 4.3),     # rechtsvoor
    ((5.5, 8, 6), (7.0, 6.0, 12.0), (7.5, 4.6, 14.0), (7.8, 3.9, 15.0), 4.3),         # linksvoor
    ((-9.5, 8, -1), (-13.0, 6.0, 3.0), (-14.0, 4.4, 4.0), (-14.6, 3.5, 4.5), 3.6),    # rechtsachter
    ((9.5, 8, -1), (13.0, 6.0, 3.0), (14.0, 4.4, 4.0), (14.6, 3.5, 4.5), 3.6),        # linksachter
]
KOP_C = np.array((0.0, 29.0, 3.0)); KOP_R = 9.6


def wol(P):
    """Lijf + kraag + poten + pompons als één huid, met een plukjesreliëf."""
    d = ell(P, (0, 14.5, -3), (12.6, 10.2, 12.0))                     # zittend achterlijf/borst
    d = smin(d, ell(P, (0, 21.0, 0.5), (10.8, 5.2, 10.4)), 2.4)     # wolkraag (breder dan de hals)
    for heup, knie, enkel, pc, pr in POTEN:
        d = smin(d, capsule(P, heup, knie, 3.4, 2.6), 1.6)          # wollige bovenpoot
        d = smin(d, capsule(P, knie, enkel, 2.0, 1.5), 0.6)         # geschoren enkeltje
        pom = ell(P, pc, (pr, pr * 0.85, pr))
        for i in range(6):                                          # plukken rond de pompon
            a = i * math.pi / 3
            pom = smin(pom, ell(P, (pc[0] + math.cos(a) * pr * 0.6, pc[1] + 0.4, pc[2] + math.sin(a) * pr * 0.6),
                                (pr * 0.55,) * 3), 0.6)
        d = smin(d, pom, 0.5)
    return d


def kop(P):
    return ell(P, KOP_C, (KOP_R, KOP_R * 0.95, KOP_R * 0.95))


def ruis(P, amp):
    x, y, z = P[:, 0], P[:, 1], P[:, 2]
    return amp * (np.sin(1.0 * x + 0.5 * y) * np.sin(0.95 * y + 0.8 * z + 1) + 0.5 * np.sin(1.4 * z - 0.7 * x + 2) * np.sin(1.3 * y))


def oog_c(kant):
    d = np.array((0.50 * kant, 0.08, 0.86)); d /= np.linalg.norm(d)
    return KOP_C + d * (KOP_R - 2.7)


def oor_delen():
    out = []
    for kant in (1, -1):
        basis = KOP_C + np.array((6.4 * kant, 4.2, -0.6))
        richting = (kant * 1.0, 0.06, -0.12)
        R = assen(richting, (0.15 * kant, 0.35, 1.0))
        c = basis + R[0] * 8.4
        out.append((c, R))
    return out


def vleugel_delen():
    """Per kant: voorvleugel (lang, driehoekig = twee ellipsoïden) en achtervleugel (rond), overlappend tot één paar."""
    out = []
    for kant in (1, -1):
        wortel = np.array((2.5 * kant, 23.0, -8.0))
        # voorvleugel: V omhoog en naar buiten (±40 graden van de verticaal), naar achteren gekanteld
        rv = (0.40 * kant, 0.92, -0.34)
        Rv = assen(rv, (0.05 * kant, 0.25, 1.0))
        out.append(('vleugel', wortel + Rv[0] * 15.5, (16.5, 6.6, 0.5), Rv))
        out.append(('vleugel', wortel + Rv[0] * 21.5 - Rv[1] * kant * 2.6, (9.5, 7.8, 0.5), Rv))   # bredere top
        # achtervleugel: lager en meer opzij, rond, deels onder de voorvleugel
        ra = (0.66 * kant, 0.70, -0.42)
        Ra = assen(ra, (0.0, 0.2, 1.0))
        out.append(('achtervl', wortel + np.array((0, -3.0, -0.6)) + Ra[0] * 11.0, (12.0, 8.5, 0.5), Ra))
    return out


VLEUGELS = vleugel_delen()
OREN = oor_delen()


def scene(P, kop_draai):
    """Afstanden per materiaal. kop_draai: extra draai (rad) van kop + oren rond de hals."""
    Rk = rot_y(kop_draai)
    piv = np.array((0, 21.0, 0.0))
    Pk = (P - piv) @ Rk + piv          # punten in kop-ruimte (kop draait, dus punt terugdraaien)
    w = wol(P) + ruis(P, 0.42)
    k = kop(Pk) + ruis(Pk, 0.30)
    huid = smin(w, k, 0.9)            # kleine k: kraag/kop-inkeping blijft zichtbaar
    d = {'wol': huid}
    d['oog'] = np.minimum(ell(Pk, oog_c(1), (4.5, 4.9, 4.2)), ell(Pk, oog_c(-1), (4.5, 4.9, 4.2)))
    d['snuit'] = ell(Pk, KOP_C + np.array((0, -2.2, KOP_R - 0.6)), (2.4, 2.8, 2.0))
    oo = None
    for c, R in OREN:
        e = ell(Pk, c, (8.8, 3.6, 0.6), R)
        oo = e if oo is None else np.minimum(oo, e)
    d['oor'] = oo
    vv = va = None
    for mat, c, r, R in VLEUGELS:
        e = ell(P, c, r, R)
        if mat == 'vleugel':
            vv = e if vv is None else np.minimum(vv, e)
        else:
            va = e if va is None else np.minimum(va, e)
    d['vleugel'] = vv; d['achtervl'] = va
    return d


MATS = ['wol', 'oog', 'snuit', 'oor', 'vleugel', 'achtervl']


def totaal(P, kd):
    d = scene(P, kd)
    return np.min(np.stack([d[m] for m in MATS]), axis=0)


def render(yaw_deg, pitch_deg=0.0, res=512):
    """Orthografisch. yaw > 0: dier draait naar links-voor (snuit naar links van de kijker)."""
    yaw, pitch = math.radians(yaw_deg), math.radians(pitch_deg)
    kd = KOP_MEE * yaw if 0 < yaw_deg <= 100 else 0.0
    # camera->model: model draait met -yaw om y (snuit naar -x van de kijker = links), pitch om x
    M = rot_y(yaw) @ rot_x(pitch)     # model = M @ camera
    s = KADER / res
    jj, ii = np.mgrid[0:res, 0:res]
    cx = (ii + 0.5) * s - KADER / 2 + MIDDEN_X
    cy = MIDDEN_Y + KADER / 2 - (jj + 0.5) * s
    o_cam = np.stack([cx.ravel(), cy.ravel() - MIDDEN_Y, np.full(cx.size, 60.0)], 1)
    dir_cam = np.array((0, 0, -1.0))
    O = o_cam @ M.T + np.array((0, MIDDEN_Y, 0)); D = dir_cam @ M.T
    t = np.zeros(len(O)); hit = np.zeros(len(O), bool); actief = np.ones(len(O), bool)
    for _ in range(160):
        idx = np.nonzero(actief)[0]
        if not len(idx):
            break
        p = O[idx] + t[idx, None] * D
        dist = totaal(p, kd)
        t[idx] += np.maximum(dist * 0.8, 0.02)
        hit[idx[dist < 0.03]] = True
        actief[idx[(dist < 0.03) | (t[idx] > 130)]] = False
    img = np.zeros((len(O), 4), np.uint8)
    mat = np.full(len(O), -1)
    hi = np.nonzero(hit)[0]
    p = O[hi] + t[hi, None] * D
    dd = scene(p, kd)
    st = np.stack([dd[m] for m in MATS])
    mi = np.argmin(st, axis=0)
    mat[hi] = mi
    e = 0.05
    n = np.stack([totaal(p + np.array(v) * e, kd) - totaal(p - np.array(v) * e, kd) for v in np.eye(3)], 1)
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-6)
    licht_cam = np.array((-0.55, 0.65, 0.52)); licht_cam /= np.linalg.norm(licht_cam)
    L = licht_cam @ M.T
    lam = np.clip(n @ L, 0, 1)
    vlak = np.isin(mi, [MATS.index('vleugel'), MATS.index('achtervl'), MATS.index('oor')])
    lam = np.where(vlak, np.abs(n @ L), lam)                # dunne vlakken: beide kanten belicht
    sh = 0.50 + 0.50 * lam
    kl = np.array([KLEUR[m] for m in MATS])[mi]
    img[hi, :3] = np.clip(kl * sh[:, None], 0, 255).astype(np.uint8)
    img[hi, 3] = 255
    return img.reshape(res, res, 4), mat.reshape(res, res)


def met_lijnen(img, mat):
    """Werkweergave: grenzen tussen materialen als dunne donkere lijn (laat zien welk deel waar voor ligt)."""
    out = img.copy()
    rand = np.zeros(mat.shape, bool)
    rand[1:] |= mat[1:] != mat[:-1]; rand[:, 1:] |= mat[:, 1:] != mat[:, :-1]
    out[rand & (mat >= 0)] = (70, 60, 55, 255)
    return out


def naar64(img):
    a = Image.fromarray(img).resize((64, 64), Image.BOX)
    arr = np.array(a)
    al = arr[..., 3]
    rgb = arr[..., :3].astype(float) / np.maximum(al[..., None], 1) * 255
    out = np.zeros_like(arr)
    m = al > 110
    out[m, :3] = np.clip(rgb[m], 0, 255).astype(np.uint8); out[m, 3] = 255
    return out


HOEKEN = [('frontaal 0°', 0, 0), ('3/4 links-voor 30°', 30, 0), ('3/4 links-voor 45°', 45, 0), ('3/4 links-voor 60°', 60, 0),
          ('zijkant 90°', 90, 0), ('achter-3/4 135°', 135, 0), ('45° van boven (+20°)', 45, 20), ('45° van onder (-15°)', 45, -15)]


def main():
    import sys
    if len(sys.argv) > 1:                     # snelle proef: python3 poedelmot_model.py 45 [pitch]
        img, mat = render(float(sys.argv[1]), float(sys.argv[2]) if len(sys.argv) > 2 else 0.0, 320)
        Image.fromarray(met_lijnen(img, mat)).save(os.path.join(HERE, 'proef.png')); return
    os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True)
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
    tegels = []
    for naam, yaw, pitch in HOEKEN:
        img, mat = render(yaw, pitch)
        werk = met_lijnen(img, mat)
        e = naar64(img)
        slug = naam.split()[0].replace('/', '') + '_%d_%d' % (yaw, pitch)
        Image.fromarray(werk).save(os.path.join(HERE, 'renders', slug + '_512.png'))
        Image.fromarray(e).save(os.path.join(HERE, 'renders', slug + '_1x.png'))
        tegels.append((naam, werk, e))
        print('render', naam)
    T = 256
    kol = 4
    rijen = (len(tegels) + kol - 1) // kol
    Wd = 12 + (kol + 1) * (T + 12)
    H = 12 + rijen * (20 + T + 8 + 64 + 16)
    out = Image.new('RGB', (Wd, H), (248, 248, 248))
    dr = ImageDraw.Draw(out)
    foto = Image.open(FOTO).convert('RGB').resize((T, T))
    dr.text((12, 12), 'bron: tak-foto', fill=(0, 0, 0), font=F)
    out.paste(foto, (12, 32))
    for i, (naam, werk, e) in enumerate(tegels):
        r, c = divmod(i, kol)
        x = 12 + (c + 1) * (T + 12); y = 12 + r * (20 + T + 8 + 64 + 16)
        dr.text((x, y), naam, fill=(0, 0, 0), font=F)
        bg = Image.new('RGB', (T, T), (120, 124, 130))
        w = Image.fromarray(werk).resize((T, T), Image.LANCZOS); bg.paste(w, (0, 0), w)
        out.paste(bg, (x, y + 20))
        for j, kleur in enumerate(((235, 235, 235), (60, 60, 70))):
            b = Image.new('RGB', (64, 64), kleur); im = Image.fromarray(e); b.paste(im, (0, 0), im)
            out.paste(b, (x + j * 72, y + 20 + T + 8))
        dr.text((x + 150, y + 20 + T + 30), '1x', fill=(0, 0, 0), font=F)
    out.save(os.path.join(HERE, 'rondom_vel.png'))


if __name__ == '__main__':
    main()
