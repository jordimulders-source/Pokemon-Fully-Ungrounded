"""Kolibrie pre-evo: 3D-model gebouwd OP de goedgekeurde vorm (SPEC, overdracht 3 nov).
Bron = r10-raster (omtrek = silhouet r2 + kop van r8 lager, Starly-oog, r7b-snavel met mondhoeklijn).
Elk deel is een opgeblazen profiel: punt (x,y,z) hoort bij een deel als |z - z0| <= w(x,y), met w uit de
afstand tot de rand (ronde doorsnede). Daardoor is het zijaanzicht (0 graden) per constructie het profiel;
draaien (lijf-yaw, kop extra yaw, kanteling) geeft de 3/4-stand. Kleur = het r10-raster zonder lijnen,
van opzij op het model geprojecteerd (verre kant gespiegeld); licht linksboven-voor.
Draaien vanuit deze map: python3 model.py"""
import numpy as np
from PIL import Image
from scipy import ndimage as nd

U = 6                      # voxels per spritepixel
N = 64 * U
CH = '.123456789ABCDEF'
HERE = __file__.rsplit('/', 1)[0] if '/' in __file__ else '.'
RASTER = HERE + '/../maker/kleur_r10/raster.txt'
PROFIEL = HERE + '/../maker/silhouet_r2/silhouet.txt'
PAL = [(152, 208, 160), (20, 14, 30), (70, 52, 104), (116, 98, 160), (162, 148, 206), (186, 176, 224),
       (228, 224, 246), (255, 255, 255), (236, 120, 146), (150, 40, 84), (64, 56, 82), (108, 98, 176),
       (250, 212, 72), (226, 150, 40), (72, 62, 134), (130, 122, 156)]
LIJN = np.array((34, 24, 50), float)

def lees(p, kar='#'):
    rows = [l.rstrip('\n') for l in open(p)][:64]
    return rows
R = np.array([[CH.index(c) for c in r.ljust(64, '.')] for r in lees(RASTER)])
S = R > 0                                            # omtrek r10
P2 = np.array([[c == '#' for c in r.ljust(64, '.')] for r in lees(PROFIEL)])   # goedgekeurd profiel r2
yy, xx = np.mgrid[0:64, 0:64]

# ---- delen in spritecoördinaten (zie ../maker/kleur_r10 op 16x) ----
OOG = (xx >= 19) & (xx <= 25) & (yy >= 12) & (yy <= 18)
BEK = S & (xx <= 17) & (yy >= 10) & (yy <= 22) & ~(((xx - 24) / 9.0) ** 2 + ((yy - 17) / 8.5) ** 2 <= 1)
KOP = S & ((((xx - 24.5) / 9.6) ** 2 + ((yy - 16.5) / 8.6) ** 2 <= 1) | ((yy <= 22) & (xx <= 33))) & ~BEK
# het Starly-oog (bevroren) als plaatje: positie volgt het model, vorm blijft gelijk (zoals een spritemaker het oog plakt)
OOGPX = ((xx >= 21) & (xx <= 25) & (yy >= 14) & (yy <= 18)) & (np.isin(R, [1, 2, 7]) | ((xx == 23) & (yy == 17)))
BOVENSNAVEL = BEK & (yy <= 15)
ONDERSNAVEL = BEK & (yy >= 16)
MONDLIJN = (xx >= 15) & (xx <= 16) & (yy >= 13) & (yy <= 16)
POOT = S & (yy >= 41) & (xx <= 30)
STAART = S & (yy >= 40) & (xx >= 38)
VL_KLEUR = np.isin(R, [11, 14]) & (yy >= 23)
VLEUGEL = nd.binary_closing(VL_KLEUR, iterations=2) | (S & nd.binary_dilation(VL_KLEUR, iterations=1) & (xx >= 29) & (yy >= 23))
VLEUGEL &= S & ~KOP & ~POOT
LIJF = S & ~BEK & ~POOT & ~STAART

# ---- textuur: r10 zonder lijnen en zonder getekende schaduw (het licht komt van het model) ----
# tinten per kleurgroep terug naar de basis: lila 3/5 -> 4, buik 7 -> 6, kap/vleugel E -> B
GROEP = {3: 4, 5: 4, 7: 6, 14: 11}
def textuur():
    Rg = R.copy()
    for a, b in GROEP.items():
        Rg[R == a] = b
    Rg[BEK & (R == 1) & (yy <= 15)] = 15          # bovensnavel: grijze snavel i.p.v. omlijning
    Rg[BEK & (R == 1) & (yy >= 16)] = 13          # ondersnavel: oranje
    rgb = np.array(PAL, float)[Rg]
    houd = BEK | MONDLIJN
    lijn = (np.isin(Rg, [1, 2]) & ~houd) | OOGPX
    vul = S & ~lijn
    _, (iy, ix) = nd.distance_transform_edt(~vul, return_indices=True)
    t = rgb[iy, ix]
    t[houd] = rgb[houd]
    return t
TEX = textuur()

def textuur_glad():
    """textuur op voxelresolutie met gladde grenzen tussen kleurvlakken (oog, snavel en mondlijn blijven scherp)"""
    kl, inv = np.unique(TEX.reshape(-1, 3), axis=0, return_inverse=True)
    inv = inv.reshape(64, 64)
    score = np.stack([nd.gaussian_filter(np.kron((inv == i).astype(np.float32), np.ones((U, U))), U * 0.55) for i in range(len(kl))])
    T = kl[score.argmax(0)].astype(float)
    houd = np.kron((MONDLIJN).astype(np.uint8), np.ones((U, U), np.uint8)) > 0
    T[houd] = np.kron(TEX, np.ones((U, U, 1)))[houd]
    return T
TEXU = textuur_glad()

def op(m, sigma=0.6, drempel=0.5):
    """masker naar voxelresolutie, licht afgerond"""
    up = np.kron(m.astype(float), np.ones((U, U)))
    return nd.gaussian_filter(up, U * sigma) > drempel if sigma else up > 0.5

def breedte(m, schaal, minimum=0.0, R0=None):
    """halve dikte (in voxels) van een opgeblazen deel: ronde doorsnede uit de afstand tot de rand"""
    d = nd.distance_transform_edt(m)
    Rm = R0 * U if R0 else d.max()
    d = np.minimum(d, Rm)
    w = schaal * np.sqrt(np.maximum(d * (2 * Rm - d), 0))
    return np.where(m, np.maximum(w, minimum * U), 0)

def bouw(dik=0.80, kopdik=0.92):
    """occupancy-grid met labels. dik/kopdik = breedte t.o.v. een ronde doorsnede."""
    lijf = op(LIJF | KOP); kop = op(KOP); bek = op(BEK, 0.3, 0.4); poot = op(POOT, 0.3); staart = op(STAART, 0.4)
    vl = op(VLEUGEL, 0.4)
    wl = breedte(op(LIJF), dik, R0=None)
    wk = breedte(kop, kopdik)
    wl = np.maximum(wl, wk)
    # snavel: twee wiggen, breed aan de mondhoek (nestjong), smal aan de punt
    xg = np.mgrid[0:N, 0:N][1] / U
    taps = np.clip((xg - 9.0) / 8.0, 0, 1)
    wb = np.where(bek, U * (0.4 + 1.7 * taps ** 1.4), 0)
    ws = np.where(staart, 1.2 * U, 0)
    Z = int(wl.max() + 3 * U)
    zs = np.arange(-Z, Z + 1)[None, None, :]
    occ = np.zeros((N, N, 2 * Z + 1), np.uint8)    # 0 leeg, 1 lijf, 2 kop, 3 vleugel, 4 bek, 5 staart, 6 poot
    a = np.abs(zs)
    occ[(a <= wl[..., None]) & (wl[..., None] > 0)] = 1
    occ[(a <= wk[..., None]) & (kop & (wk > 0))[..., None]] = 2
    occ[(a <= wb[..., None]) & (bek & (wb > 0))[..., None]] = 4
    occ[(a <= ws[..., None]) & staart[..., None]] = 5
    wvl = np.maximum(wl, 0.8 * U)
    occ[vl[..., None] & (a >= 0.45 * wvl[..., None]) & (a <= wvl[..., None] + 1.2 * U)] = 3
    for z0, xr in ((+2.2, (0, 26.5)), (-2.2, (26.5, 64))):      # voorste/achterste pootje
        pm = poot & (np.mgrid[0:N, 0:N][1] >= xr[0] * U) & (np.mgrid[0:N, 0:N][1] < xr[1] * U)
        occ[pm[..., None] & (np.abs(zs - z0 * U) <= 1.1 * U)] = 6
    return occ, Z

def render(occ, Z, yaw=0.0, kop_extra=0.0, kantel=0.0, licht=True, pivot=(24.0, 22.5), kleur_fn=None, oog3d=None):
    vol = occ > 0
    surf = vol & ~nd.binary_erosion(vol)
    sm = nd.gaussian_filter(vol.astype(np.float32), 3.4)
    iy, ix, iz = np.nonzero(surf)
    gy, gx, gz = [g[iy, ix, iz] for g in np.gradient(sm)]
    n = -np.stack([gx, gy, gz], 1); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-9
    lab = occ[iy, ix, iz]
    X = ix + 0.5; Y = iy + 0.5; Zc = (iz - Z).astype(float)
    oogpunt = OOGPX[(iy // U), (ix // U)] & (Zc > 0)
    # kleur: projectie van opzij
    col = TEXU[np.clip(Y.astype(int), 0, N - 1), np.clip(X.astype(int), 0, N - 1)]
    if kleur_fn is not None:
        col = kleur_fn(X, Y, Zc, lab, col)
    if oog3d is not None:
        oogpunt = np.zeros_like(oogpunt)
        X = np.append(X, oog3d[0]); Y = np.append(Y, oog3d[1]); Zc = np.append(Zc, oog3d[2])
        lab = np.append(lab, 0); col = np.vstack([col, [[0, 0, 0]]]); n = np.vstack([n, [[0, 0, 1]]])
        oogpunt = np.append(oogpunt, True)
    # kop (en bek) extra draaien rond de nek
    def rot_y(x, z, th, cx=0.0):
        c, s = np.cos(th), np.sin(th)
        return (x - cx) * c + z * s + cx, -(x - cx) * s + z * c
    kopdeel = (lab == 2) | (lab == 4)
    if kop_extra:
        th = np.radians(kop_extra)
        X2, Z2 = rot_y(X[kopdeel], Zc[kopdeel], th, pivot[0] * U)
        X = X.copy(); Zc = Zc.copy(); X[kopdeel], Zc[kopdeel] = X2, Z2
        nx2, nz2 = rot_y(n[kopdeel, 0], n[kopdeel, 2], th)
        n[kopdeel, 0], n[kopdeel, 2] = nx2, nz2
    th = np.radians(yaw); cx = 32 * U
    X, Zc = rot_y(X, Zc, th, cx)
    nx, nz = rot_y(n[:, 0], n[:, 2], th); n = np.stack([nx, n[:, 1], nz], 1)
    ph = np.radians(kantel); cy = 32 * U
    Yr = (Y - cy) * np.cos(ph) + Zc * np.sin(ph) + cy
    Zr = Zc * np.cos(ph) - (Y - cy) * np.sin(ph)
    ny = n[:, 1] * np.cos(ph) + n[:, 2] * np.sin(ph); nz = n[:, 2] * np.cos(ph) - n[:, 1] * np.sin(ph)
    n = np.stack([n[:, 0], ny, nz], 1)
    if licht:
        L = np.array([-0.45, -0.6, 0.66]); L /= np.linalg.norm(L)
        lam = np.clip(n @ L, 0, 1)
        f = 0.52 + 0.6 * lam
        spec = np.clip(n @ (L + np.array([0, 0, 1])) / np.linalg.norm(L + np.array([0, 0, 1])), 0, 1) ** 24
        col = np.clip(col * f[:, None] + 60 * spec[:, None], 0, 255)
    W = N
    img = np.zeros((W, W, 3)); dep = np.full((W, W), -1e9); lb = np.zeros((W, W), np.uint8)
    o = np.argsort(Zr)
    for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1), (-1, 0), (0, -1)):
        px = np.clip(np.round(X[o]).astype(int) + dx, 0, W - 1); py = np.clip(np.round(Yr[o]).astype(int) + dy, 0, W - 1)
        m = Zr[o] > dep[py, px] - 0  # nearest last wins
        dep_tmp = dep.copy()
        img[py, px] = np.where((Zr[o] >= dep_tmp[py, px])[:, None], col[o], img[py, px])
        lb[py, px] = np.where(Zr[o] >= dep_tmp[py, px], lab[o], lb[py, px])
        dep[py, px] = np.maximum(dep_tmp[py, px], Zr[o]) if False else np.where(Zr[o] >= dep_tmp[py, px], Zr[o], dep_tmp[py, px])
    alpha = dep > -1e8
    alpha = nd.binary_closing(alpha, iterations=1) & nd.binary_fill_holes(alpha)
    # gaatjes in de kleur vullen
    gat = alpha & (dep < -1e8)
    if gat.any():
        _, (jy, jx) = nd.distance_transform_edt(gat, return_indices=True); img[gat] = img[jy[gat], jx[gat]]; dep[gat] = dep[jy[gat], jx[gat]]
    # omlijning: buitenrand + dieptesprongen (vleugel over lijf, kop over borst)
    rand = alpha & ~nd.binary_erosion(alpha, iterations=2)
    dmax = nd.maximum_filter(np.where(alpha, dep, -1e9), 3); sprong = alpha & (dmax - dep > 2.2 * U)
    sprong = nd.binary_dilation(sprong) & alpha & ~(lb == 4)
    out = img.copy(); out[rand | sprong] = LIJN
    # oog plakken op de plek waar het model het heeft
    if oogpunt.any():
        ex, ey, ez = X[oogpunt].mean(), Yr[oogpunt].mean(), Zr[oogpunt].max()
        if dep[int(ey), int(ex)] - ez < 1.5 * U:
            oy, ox = np.nonzero(OOGPX); cy0, cx0 = oy.mean() + 0.5, ox.mean() + 0.5
            for py, px in zip(oy, ox):
                y0 = int(round(ey + (py - cy0) * U)); x0 = int(round(ex + (px - cx0) * U))
                out[y0:y0 + U, x0:x0 + U] = PAL[R[py, px]]
    return out.astype(np.uint8), alpha

def naar64(alpha):
    """render-alpha (voxelresolutie) terug naar spritepixels"""
    a = Image.fromarray((alpha * 255).astype(np.uint8)).resize((64, 64), Image.BOX)
    return np.asarray(a) >= 128

def iou(a, b): return (a & b).sum() / (a | b).sum()

if __name__ == '__main__':
    occ, Z = bouw()
    img, al = render(occ, Z, 0, 0, 0)
    m = naar64(al)
    print('0 graden: overlap r2', round(iou(m, P2), 3), 'r10', round(iou(m, S), 3), 'px', m.sum())
    Image.fromarray(img).save(HERE + '/zij_0.png')
