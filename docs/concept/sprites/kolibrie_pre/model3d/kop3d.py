"""Kolibrie pre-evo, model ronde 2: lijf van het profiel (B2), kop als eigen bol in 3D met het gezicht naar de kijker
(Gen 3-driekwart: ronde kop bovenop de voorkant van het lijf, oog in het middelste derde, bekje schuin naar voren).
Les (SPRITE_WERKWIJZE): een opgeblazen profielkop blijft van opzij gezien plat. python3 kop3d.py"""
import numpy as np
from scipy import ndimage as nd
import model as M
U, N = M.U, M.N
C = dict(kap=(108, 98, 176), lila=(162, 148, 206), wit=(228, 224, 246), boven=(130, 122, 156), onder=(226, 150, 40),
         gaap=(250, 212, 72))

def frame(h, p):
    """kop-assen in modelruimte (x rechts, y omlaag, z naar de kijker): f = snavelrichting, u = boven, s = zijkant naar de kijker"""
    h, p = np.radians(h), np.radians(p)
    f = np.array([-np.cos(h) * np.cos(p), -np.sin(p), np.sin(h) * np.cos(p)])
    u = np.array([0, -1.0, 0]); u -= f * (u @ f); u /= np.linalg.norm(u)
    s = np.cross(u, f); s *= np.sign(s[2]) if s[2] else 1
    return f, u, s

def glad(m, sigma):
    """masker op voxelresolutie rond maken met behoud van oppervlak (sigma in spritepx)"""
    up = np.kron(m.astype(np.float32), np.ones((U, U), np.float32))
    if not sigma: return up > 0.5
    g = nd.gaussian_filter(up, U * sigma)
    t = np.sort(g.ravel())[::-1][int(up.sum())]
    return g > t

def bouw(h=25, p=15, c=(23.0, 17.6), r=(8.2, 7.6, 7.9), snavel=7.5, gaap=40, rond=0.0, nek=0, staart_uit=(0, 0)):
    """h = kop extra naar de kijker t.o.v. het lijf, p = bekje omhoog, c = kopmidden (spritepx), r = stralen f/u/s"""
    lijfm = (M.LIJF & ~M.KOP) | (M.LIJF & (M.yy >= 21) & (M.xx >= 19))
    if nek:   # bovenkant van het lijf lager, zodat de kop als bol boven de schouders uitkomt
        lijfm &= ~((M.yy < 21 + nek) & (M.xx < 34))
    st = np.roll(np.roll(M.STAART, staart_uit[0], 1), staart_uit[1], 0)
    lijf = glad(lijfm, rond) if rond else M.op(lijfm)
    vl = (glad(M.VLEUGEL, rond) if rond else M.op(M.VLEUGEL, 0.4)) & lijf; staart = M.op(st, 0.4); poot = M.op(M.POOT, 0.3)
    wl = M.breedte(lijf, 0.80)
    Zmax = int(max(wl.max(), max(r) * U) + 4 * U)
    zs = np.arange(-Zmax, Zmax + 1)[None, None, :]
    occ = np.zeros((N, N, 2 * Zmax + 1), np.uint8)
    a = np.abs(zs)
    occ[(a <= wl[..., None]) & (wl[..., None] > 0)] = 1
    occ[(np.abs(zs) <= 1.2 * U) & staart[..., None]] = 5
    wvl = np.maximum(wl, 0.8 * U)
    occ[vl[..., None] & (a >= 0.45 * wvl[..., None]) & (a <= wvl[..., None] + 1.2 * U)] = 3
    xg = np.mgrid[0:N, 0:N][1]
    for z0, xr in ((+2.2, (0, 26.5)), (-2.2, (26.5, 64))):
        pm = poot & (xg >= xr[0] * U) & (xg < xr[1] * U)
        occ[pm[..., None] & (np.abs(zs - z0 * U) <= 1.1 * U)] = 6
    # kop + snavel in een uitsnede rond de kop
    f, u, s = frame(h, p)
    cx, cy = c[0] * U, c[1] * U
    R = int((max(r) + snavel + 3) * U)
    y0, y1, x0, x1 = max(0, int(cy - R)), min(N, int(cy + R)), max(0, int(cx - R)), min(N, int(cx + R))
    Y, X, Zz = np.mgrid[y0:y1, x0:x1, -Zmax:Zmax + 1].astype(np.float32)
    P = np.stack([X - cx, Y - cy, Zz], -1) / U
    pf, pu, ps = P @ f, P @ u, P @ s
    kop = (pf / r[0]) ** 2 + (pu / r[1]) ** 2 + (ps / r[2]) ** 2 <= 1
    sub = occ[y0:y1, x0:x1]
    sub[kop] = 2
    # snavel: twee wiggen vanaf de voorkant van de kop, open V (gaap)
    b0 = r[0] * 0.78
    g = np.radians(gaap / 2)
    for lab, teken, dikte, breed, lengte in ((7, +1, 0.8, 2.0, snavel), (4, -1, 1.5, 2.5, snavel * 0.85)):
        ax = np.array([np.cos(g), teken * np.sin(g)])           # as in het f-u-vlak
        t = (pf - b0) * ax[0] + pu * ax[1]
        q = -(pf - b0) * ax[1] + pu * ax[0]                       # loodrecht op de as in het f-u-vlak
        k = np.clip(1 - t / lengte, 0, 1)
        wig = (t >= -1.0) & (t <= lengte) & ((q / (dikte * k + 0.3)) ** 2 + (ps / (breed * k + 0.35)) ** 2 <= 1)
        sub[wig & (sub != 2)] = lab
    oog_az = np.radians(52)
    e = f * np.cos(oog_az) + s * np.sin(oog_az) + u * 0.22; e /= np.linalg.norm(e)
    rr = 1 / np.sqrt((e @ f / r[0]) ** 2 + (e @ u / r[1]) ** 2 + (e @ s / r[2]) ** 2)
    oog = np.array([cx, cy, 0]) + e * rr * U
    info = dict(f=f, u=u, s=s, c=np.array([cx, cy, 0.0]), r=r, b0=b0, oog=oog, Zmax=Zmax)
    return occ, Zmax, info

def kleur(info):
    f, u, s, c, r = info['f'], info['u'], info['s'], info['c'], info['r']
    def fn(X, Y, Zc, lab, col):
        col = col.copy()
        P = (np.stack([X, Y, Zc], 1) - c) / U
        pf, pu, ps = P @ f, P @ u, P @ s
        n = np.sqrt((pf / r[0]) ** 2 + (pu / r[1]) ** 2 + (ps / r[2]) ** 2) + 1e-6
        df, du = pf / r[0] / n, pu / r[1] / n
        k = lab == 2
        c2 = np.where(((du * 0.75 - df * 0.65) > 0.08)[:, None], C['kap'], C['lila'])
        c2 = np.where(((du < -0.5) & (df > -0.5))[:, None], C['wit'], c2)
        dichtbij = ((pf - info['b0']) ** 2 + pu ** 2 + (np.abs(ps) - 2.3) ** 2) < 1.4 ** 2
        c2 = np.where(dichtbij[:, None], C['gaap'], c2)
        col[k] = c2[k]
        col[lab == 7] = C['boven']; col[lab == 4] = C['onder']
        return col
    return fn

def render(h=25, p=15, yaw=32, kantel=8, **kw):
    occ, Z, info = bouw(h, p, **kw)
    o = info['oog']
    img, al = M.render(occ, Z, yaw, 0, kantel, kleur_fn=kleur(info), oog3d=(o[0], o[1], o[2]))
    return img, al

if __name__ == '__main__':
    from PIL import Image
    import sys
    SP = sys.argv[1] if len(sys.argv) > 1 else '.'
    V = Image.new('RGB', (384 * 4, 384), (236, 234, 228))
    for i, (h, p) in enumerate(((10, 12), (20, 15), (30, 15), (40, 18))):
        img, al = render(h, p)
        V.paste(Image.fromarray(img), (384 * i, 0), Image.fromarray((al * 255).astype(np.uint8)))
        print(h, p, M.naar64(al).sum())
    V.save(SP + '/kop3d_test.png')
