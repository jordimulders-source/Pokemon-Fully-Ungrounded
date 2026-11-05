"""Poedelmot 3D-model, ronde 2 (5 nov): zes benoemde reparaties op ronde 1 (../poedelmot_model.py blijft als naslag):
 1. oren = sprieten: dunne gebogen schacht met een plat kamblad en een tandjesrand, taps naar een punt, opzij en licht
    omhoog gekruld (foto_sprieten_plus_vilt, vilt);
 2. pose rechtop zoals de tak-foto: lijf verticaal, voorpoten hangen onder/iets voor de borst, achterpoten zitten;
 3. voorvleugel lang, smal en spits (tak-/vingerfoto); achtervleugel kleiner en rond (vilt);
 4. wol: grote plukken (cellulair reliëf i.p.v. golvende ruis), een duidelijke plukkenkraag met diepe inkeping tussen kop
    en lijf; pompons groot en rond met een dun enkeltje erboven (poedelknip);
 5. snuit: bruin snuitvlak tussen en onder de ogen (geen hondenneus-bolletje);
 6. kader: per hoek gecentreerd en passend (2 px marge), zonder de rand te raken.
Huid = smooth union van afstandsvelden, numpy-renderer (geen Blender in de container), orthografisch, licht linksboven.
Draaien: python3 docs/concept/sprites/poedelmot/model/ronde2/poedelmot_model_r2.py      (proef: ... 45 [pitch])"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, '../../referenties')
KOP_MEE = 0.3
MARGE = 2                         # px vrij rondom in het 64-kader
KLEUR = {'wol': (238, 234, 226), 'vleugel': (222, 216, 204), 'achtervl': (204, 198, 186), 'oor': (122, 82, 50),
         'oog': (30, 28, 38), 'snuit': (150, 108, 74)}
MATS = ['wol', 'oog', 'snuit', 'oor', 'vleugel', 'achtervl']


def rot_y(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rot_x(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def ell(P, c, r, R=None):
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
    u = np.asarray(richting, float); u /= np.linalg.norm(u)
    w = np.asarray(voorkant, float); w = w - (w @ u) * u; w /= np.linalg.norm(w)
    return np.stack([u, np.cross(w, u), w])


def plukken(P, cel, amp):
    """Cellulair reliëf: per cel een willekeurig punt; dicht bij een punt bolt de wol op -> ronde plukken met groeven."""
    g = P / cel
    b = np.floor(g)
    best = np.full(len(P), 9.0)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                c = b + np.array((dx, dy, dz))
                h = np.sin(c @ np.array((127.1, 311.7, 74.7))) * 43758.5453
                j = np.stack([h - np.floor(h), (h * 1.37) % 1.0, (h * 2.11) % 1.0], 1) * 0.8 + 0.1
                best = np.minimum(best, np.linalg.norm(g - (c + j), axis=1))
    return amp * (best ** 2) * 1.6          # 0 midden in een pluk, groter in de groeven -> afstand groter = inkeping


# ---------- model ----------
KOP_C = np.array((0.0, 31.0, 2.0)); KOP_R = 9.4
POTEN = [  # heup, knie, enkel, pompon-midden, pompon-straal (dier-rechts = -x); voorpoten hangen onder/voor de borst
    ((-5.0, 17.0, 4.5), (-6.2, 12.0, 7.6), (-6.8, 8.0, 8.2), (-7.0, 4.2, 8.6), 4.6),
    ((5.0, 17.0, 4.5), (6.2, 12.0, 7.6), (6.8, 8.0, 8.2), (7.0, 4.2, 8.6), 4.6),
    ((-8.5, 10.0, -3.5), (-12.0, 9.0, -0.8), (-12.8, 7.2, -0.2), (-13.2, 3.8, 0.2), 4.0),   # zitten
    ((8.5, 10.0, -3.5), (12.0, 9.0, -0.8), (12.8, 7.2, -0.2), (13.2, 3.8, 0.2), 4.0),
]


def lijf(P):
    d = ell(P, (0, 11.5, -4.0), (11.2, 10.2, 9.6))           # achterlijf (zit op de grond)
    d = smin(d, ell(P, (0, 19.5, -1.5), (10.4, 7.0, 8.8)), 3.0)   # borst, rechtop erboven
    for heup, knie, enkel, pc, pr in POTEN:
        d = smin(d, capsule(P, heup, knie, 3.3, 2.6), 1.4)   # wollige bovenpoot
    return d


def kraag(P):
    return ell(P, (0, 23.6, 0.2), (11.6, 3.8, 10.4))


def pompons(P):
    d = None
    for heup, knie, enkel, pc, pr in POTEN:
        e = capsule(P, knie, enkel, 1.15, 1.0)                   # geschoren enkeltje
        e = np.minimum(e, ell(P, pc, (pr, pr * 0.9, pr)))
        d = e if d is None else np.minimum(d, e)
    return d


def kop_ruimte(P, kd):
    piv = np.array((0, 22.0, 0.0))
    return (P - piv) @ rot_y(kd) + piv


def oog_c(kant):
    d = np.array((0.50 * kant, 0.10, 0.86)); d /= np.linalg.norm(d)
    return KOP_C + d * (KOP_R - 2.6)


def veer_punten(kant):
    """Middenlijn van een spriet: van de kopzijkant opzij, aan het eind licht omhoog gekruld."""
    basis = KOP_C + np.array((5.8 * kant, 5.0, -0.8))
    pts = []
    for i in range(15):
        t = i / 14
        x = basis[0] + kant * 16.0 * t
        y = basis[1] + 1.2 * t + 4.2 * t ** 2.4             # krul omhoog
        z = basis[2] - 1.5 * t
        pts.append(np.array((x, y, z)))
    return pts


VEREN = [veer_punten(1), veer_punten(-1)]


def veer(P):
    """Kamblad: dunne schacht + plat blad (breed bij de basis, taps naar een punt) met tandjes langs beide randen."""
    d = None
    for pts in VEREN:
        lo = np.min(pts, 0) - 4; hi = np.max(pts, 0) + 4
        dicht = np.all((P > lo) & (P < hi), axis=1)
        e = np.full(len(P), 4.0)
        if dicht.any():
            Q = P[dicht]
            ee = None
            for i in range(len(pts) - 1):
                a, b = pts[i], pts[i + 1]
                t = (i + 0.5) / (len(pts) - 1)
                breed = 3.0 * math.sin(math.pi * min(1.0, 0.25 + 0.9 * t)) ** 0.8 * (1.05 - 0.75 * t) + 0.25
                u = b - a
                R = assen(u, (0.0, 0.25, 1.0))                   # blad ligt ongeveer in het beeldvlak
                c = (a + b) / 2
                seg = ell(Q, c, (np.linalg.norm(u) * 0.62, breed, 0.42), R)
                # tandjes (kam): ondiepe inkepingen langs de rand
                q = (Q - c) @ R.T
                tand = 0.35 * np.abs(np.sin(q[:, 0] * 2.6))
                seg = seg + tand * np.clip(np.abs(q[:, 1]) / max(breed, 0.1), 0, 1) ** 4
                ee = seg if ee is None else np.minimum(ee, seg)
            ee = np.minimum(ee, np.min(np.stack([capsule(Q, pts[i], pts[i + 1], 0.55, 0.5) for i in range(len(pts) - 1)]), 0))
            e[dicht] = ee
        d = e if d is None else np.minimum(d, e)
    return d


def blad(P, wortel, richting, voorkant, lengte, breedte_fn, dikte=0.45, n=10):
    """Vleugelvorm als keten van platte ellipsoïden met een breedteprofiel (lang/smal/spits of rond)."""
    R = assen(richting, voorkant)
    d = None
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n
        tm = (t0 + t1) / 2
        c = wortel + R[0] * lengte * tm
        e = ell(P, c, (lengte / n * 0.75, max(breedte_fn(tm), 0.3), dikte), R)
        d = e if d is None else np.minimum(d, e)
    return d


def voorvl_breed(t):          # smal bij de wortel, breedst op ±60%, spitse punt
    return 1.6 + 4.6 * math.sin(math.pi * min(t / 0.62, 1.0) * 0.5) ** 1.2 * (1 - max(0, (t - 0.62) / 0.38) ** 1.4)


def vleugels(P):
    vv = va = None
    for kant in (1, -1):
        w = np.array((2.5 * kant, 24.5, -7.5))
        e = blad(P, w, (0.40 * kant, 0.92, -0.32), (0.05 * kant, 0.25, 1.0), 31.0, voorvl_breed, n=12)
        vv = e if vv is None else np.minimum(vv, e)
        a = ell(P, w + np.array((0, -3.0, -0.8)) + np.array((0.66 * kant, 0.70, -0.40)) / 1.06 * 8.0, (8.6, 7.0, 0.45),
                assen((0.66 * kant, 0.70, -0.40), (0, 0.2, 1.0)))
        va = a if va is None else np.minimum(va, a)
    return vv, va


def scene(P, kd):
    Pk = kop_ruimte(P, kd)
    body = lijf(P) + plukken(P, 3.6, 1.0)
    kr = kraag(P) + plukken(P + 7.3, 2.6, 1.3)                 # kraag: kleinere, diepere plukken
    kop = ell(Pk, KOP_C, (KOP_R, KOP_R * 0.95, KOP_R * 0.95)) + plukken(Pk + 3.1, 2.8, 0.7)
    wol = smin(smin(body, kr, 0.6), kop, 0.35)                 # kleine k: duidelijke inkeping kop/kraag/lijf
    pom = pompons(P)
    pomw = np.minimum(pom, pom + plukken(P + 1.7, 1.9, 0.6))
    wol = np.minimum(wol, pomw)
    d = {'wol': wol}
    d['oog'] = np.minimum(ell(Pk, oog_c(1), (4.5, 4.9, 4.2)), ell(Pk, oog_c(-1), (4.5, 4.9, 4.2)))
    # snuitvlak: plat bruin vlak tussen en onder de ogen, iets uitstekend, onderaan smaller
    sc = KOP_C + np.array((0, -2.6, KOP_R - 1.5))
    d['snuit'] = smin(ell(Pk, sc, (2.6, 4.2, 1.7)), ell(Pk, sc + np.array((0, -2.6, 0.2)), (1.8, 1.6, 1.5)), 0.8)
    d['oor'] = veer(Pk)
    d['vleugel'], d['achtervl'] = vleugels(P)
    return d


def totaal(P, kd):
    d = scene(P, kd)
    return np.min(np.stack([d[m] for m in MATS]), axis=0)


def trace(yaw_deg, pitch_deg, res, kader, mx, my):
    yaw, pitch = math.radians(yaw_deg), math.radians(pitch_deg)
    kd = KOP_MEE * yaw
    M = rot_y(yaw) @ rot_x(pitch)
    s = kader / res
    jj, ii = np.mgrid[0:res, 0:res]
    cx = (ii + 0.5) * s - kader / 2 + mx
    cy = my + kader / 2 - (jj + 0.5) * s
    o_cam = np.stack([cx.ravel(), cy.ravel() - 26.0, np.full(cx.size, 70.0)], 1)
    O = o_cam @ M.T + np.array((0, 26.0, 0)); D = np.array((0, 0, -1.0)) @ M.T
    t = np.zeros(len(O)); hit = np.zeros(len(O), bool); actief = np.ones(len(O), bool)
    for _ in range(220):
        idx = np.nonzero(actief)[0]
        if not len(idx):
            break
        p = O[idx] + t[idx, None] * D
        dist = totaal(p, kd)
        t[idx] += np.maximum(dist * 0.6, 0.02)
        hit[idx[dist < 0.03]] = True
        actief[idx[(dist < 0.03) | (t[idx] > 150)]] = False
    return O, D, t, hit, kd, M


def render(yaw_deg, pitch_deg=0.0, res=448):
    # pas 1: grof, om het kader te bepalen (ongeveer gecentreerd, passend met MARGE px rondom)
    O, D, t, hit, kd, M = trace(yaw_deg, pitch_deg, 96, 90.0, 0.0, 26.0)
    hm = hit.reshape(96, 96); ys, xs = np.nonzero(hm)
    s = 90.0 / 96
    x0, x1 = (xs.min() - 0.5) * s - 45, (xs.max() + 1.5) * s - 45
    y0, y1 = 26 + 45 - (ys.max() + 1.5) * s, 26 + 45 - (ys.min() - 0.5) * s
    kader = max(x1 - x0, y1 - y0) * 64.0 / (64 - 2 * MARGE)
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    O, D, t, hit, kd, M = trace(yaw_deg, pitch_deg, res, kader, mx, my)
    img = np.zeros((len(O), 4), np.uint8); mat = np.full(len(O), -1)
    hi = np.nonzero(hit)[0]
    p = O[hi] + t[hi, None] * D
    dd = scene(p, kd)
    mi = np.argmin(np.stack([dd[m] for m in MATS]), axis=0)
    mat[hi] = mi
    e = 0.05
    n = np.stack([totaal(p + v * e, kd) - totaal(p - v * e, kd) for v in np.eye(3)], 1)
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-6)
    L = np.array((-0.55, 0.65, 0.52)); L /= np.linalg.norm(L); L = L @ M.T
    lam = np.clip(n @ L, 0, 1)
    vlak = np.isin(mi, [MATS.index('vleugel'), MATS.index('achtervl'), MATS.index('oor')])
    lam = np.where(vlak, np.abs(n @ L), lam)
    sh = 0.48 + 0.52 * lam
    kl = np.array([KLEUR[m] for m in MATS])[mi]
    img[hi, :3] = np.clip(kl * sh[:, None], 0, 255).astype(np.uint8); img[hi, 3] = 255
    return img.reshape(res, res, 4), mat.reshape(res, res), kader


def met_lijnen(img, mat):
    out = img.copy()
    rand = np.zeros(mat.shape, bool)
    rand[1:] |= mat[1:] != mat[:-1]; rand[:, 1:] |= mat[:, 1:] != mat[:, :-1]
    out[rand & (mat >= 0)] = (70, 60, 55, 255)
    return out


def naar64(img):
    arr = np.array(Image.fromarray(img).resize((64, 64), Image.BOX))
    al = arr[..., 3]
    rgb = arr[..., :3].astype(float) / np.maximum(al[..., None], 1) * 255
    out = np.zeros_like(arr); m = al > 110
    out[m, :3] = np.clip(rgb[m], 0, 255).astype(np.uint8); out[m, 3] = 255
    return out


HOEKEN = [30, 45, 60]


def main():
    if len(sys.argv) > 1:
        img, mat, _ = render(float(sys.argv[1]), float(sys.argv[2]) if len(sys.argv) > 2 else 0.0, 320)
        Image.fromarray(met_lijnen(img, mat)).save(os.path.join(HERE, 'proef.png')); return
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
    T = 320
    tegels = []
    for yaw in HOEKEN:
        img, mat, kader = render(yaw)
        werk = met_lijnen(img, mat); e = naar64(img)
        Image.fromarray(werk).save(os.path.join(HERE, 'render_%d_werk.png' % yaw))
        Image.fromarray(e).save(os.path.join(HERE, 'render_%d_1x.png' % yaw))
        tegels.append(('3/4 links-voor %d°' % yaw, werk, e))
        print('render %d° (kader %.1f eenheden)' % (yaw, kader))
    Wd = 12 + 4 * (T + 12); H = 12 + 20 + T + 8 + 64 + 12
    out = Image.new('RGB', (Wd, H), (248, 248, 248)); dr = ImageDraw.Draw(out)
    dr.text((12, 12), 'bron: tak-foto', fill=(0, 0, 0), font=F)
    out.paste(Image.open(os.path.join(REF, 'foto_tak_katoen.webp')).convert('RGB').resize((T, T)), (12, 32))
    for i, (naam, werk, e) in enumerate(tegels):
        x = 12 + (i + 1) * (T + 12)
        dr.text((x, 12), naam, fill=(0, 0, 0), font=F)
        bg = Image.new('RGB', (T, T), (120, 124, 130)); w = Image.fromarray(werk).resize((T, T), Image.LANCZOS)
        bg.paste(w, (0, 0), w); out.paste(bg, (x, 32))
        for j, kl in enumerate(((235, 235, 235), (60, 60, 70))):
            b = Image.new('RGB', (64, 64), kl); im = Image.fromarray(e); b.paste(im, (0, 0), im)
            out.paste(b, (x + j * 72, 32 + T + 8))
        dr.text((x + 150, 32 + T + 30), '1x', fill=(0, 0, 0), font=F)
    out.save(os.path.join(HERE, 'vel.png'))


if __name__ == '__main__':
    main()
