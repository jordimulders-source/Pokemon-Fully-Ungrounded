"""Poedelmot silhouet ronde 2, stap 1: bron = het poppetje van ronde 5b (../../poppetje/ronde5b/pop3d_poedelmot_r5b.py, 45°,
pitch 8, zelfde kader als poppetje_45_1x.png). Rendert op 768 (12x12 subpixels per spritepixel) en schrijft:
- alpha.npy: dekking van het hele poppetje (met poten), alleen voor de meting
- dekking_zonder_poten.npy + model50.txt: massa zonder poten (lijf, kop, wol, vleugels, sprieten) op de 50%-grens
- delen.npy: per spritepixel het onderdeel met de meeste dekking (0 leeg, 1 lijf/wol, 2 kop, 3 oog, 4 spriet,
  5 voorvleugel, 6 achtervleugel, 10+i poot i van POTEN)
- poten_ref.npy: dekking per poot (6 x 64 x 64), alleen als plek- en maatgids voor de handgetekende poten
- onderlaag_512.png: render (8x) als onderlaag voor de vellen
Draaien vanuit de repo-root: python3 docs/concept/sprites/poedelmot/silhouet/ronde2/bron.py"""
import os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../poppetje/ronde5b'))
import pop3d_poedelmot_r5b as Q
P, L = Q.P, Q.L

GROEP = {'wol': 1, 'kopwol': 2, 'glint': 3, 'oog': 3, 'spriet': 4, 'sprietver': 4, 'sprietlicht': 4,
         'vleugel': 5, 'vlver': 5, 'achtervl': 6, 'achtver': 6, 'ader': 6, 'aderver': 6, 'ader2': 6, 'aderver2': 6}

if __name__ == '__main__':
    Q.gebruik_kleuren()
    m = Q.poedelmot(pootkleur=True)
    for i in range(6): L.COL[f'p{i}'] = Q.POOTKLEUR[i]
    L.COL['kopwol'] = Q.COL['wol']
    # kopwol apart labelen (alles vanaf kop0 dat 'wol' is)
    m.parts = [(c, r, R0, ('kopwol' if (j >= m.kop0 and g == 'wol') else g)) for j, (c, r, R0, g) in enumerate(m.parts)]
    # zelfde kader als Q.view (size 236 van 256)
    Rc = P.rot_x(math.radians(8)) @ P.rot_y(math.radians(Q.YAW))
    pts = np.array([Rc @ c for c, r, R0, g in m.parts]); rs = np.array([r.max() for c, r, R0, g in m.parts])
    x0, x1, y0, y1 = (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()
    scale = L.R * (236 / 256) / max(x1 - x0, y1 - y0); ctr = ((x0 + x1) / 2, (y0 + y1) / 2)
    zb, gid, nrm, groups = L.render(m, Q.YAW, 8, scale, ctr)
    k = L.R // 64
    blok = lambda b: b.astype(float).reshape(64, k, 64, k).mean((1, 3))
    a = gid >= 0; np.save(os.path.join(HERE, 'alpha.npy'), blok(a))
    poot = np.isin(gid, [groups.index(f'p{i}') for i in range(6)])
    # zonder poten: opnieuw renderen zonder pootdelen (wat achter de poten zit komt dan wel mee)
    m2 = P.Model(); m2.parts = [p for p in m.parts if p[3] not in [f'p{i}' for i in range(6)]]
    zb2, gid2, _, gr2 = L.render(m2, Q.YAW, 8, scale, ctr)
    cov = blok(gid2 >= 0); np.save(os.path.join(HERE, 'dekking_zonder_poten.npy'), cov)
    M = cov >= 0.5
    open(os.path.join(HERE, 'model50.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in M) + '\n')
    lab = np.zeros(gid2.shape, np.int16)
    for g, v in GROEP.items():
        if g in gr2: lab[gid2 == gr2.index(g)] = v
    dl = np.zeros((64, 64), np.int16)
    for y in range(64):
        for x in range(64):
            b = lab[y*k:(y+1)*k, x*k:(x+1)*k].ravel(); b = b[b > 0]
            if len(b): dl[y, x] = np.bincount(b).argmax()
    pr = np.stack([blok(gid == groups.index(f'p{i}')) for i in range(6)])
    for i in range(6): dl[(pr[i] >= 0.5) & ~M] = 10 + i
    np.save(os.path.join(HERE, 'delen.npy'), dl); np.save(os.path.join(HERE, 'poten_ref.npy'), pr)
    # sprietassen + tandpunten in spritepixels (zelfde berekening als Q.spriet + kopdraai + camera)
    kop_r = 19.0; cr = np.array((-9.0, 53.0, 0.0)); Rh = P.rot_y(math.radians(Q.KOP_EXTRA)); piv = np.array((-5.0, 36.0, 0.0))
    def scr(p):
        w = Rc @ (piv + Rh @ (np.array(p) - piv))
        return ((w[0] - ctr[0]) * scale + L.R / 2) / k, ((-w[1] + ctr[1]) * scale + L.R / 2) / k
    S = Q.SPRIET; N = S['n']; uit = {}
    for sz in (1, -1):
        basis = cr + np.array((-2.0, 9.0, 13.0 * sz))
        pts = [np.array(basis) + np.array((3.0 * t, S['boog'] * math.sin(math.pi * 0.8 * t), sz * S['lengte'] * t)) for t in np.arange(N + 1) / N]
        rij = []
        for i in range(N + 1):
            row = [*scr(pts[i]), 0, 0, 0, 0]
            if 0 < i < N:
                t = i / N; lang = S['tand'] * math.sin(math.pi * min(1.0, 0.12 + 0.95 * t)) ** 0.7 + 1.0
                rich = pts[i + 1] - pts[i]; rich /= np.linalg.norm(rich); zij = np.cross(rich, Q.KIJK); zij /= np.linalg.norm(zij)
                tips = []
                for s_ in (1, -1):
                    d = zij * s_ + rich * 0.5; d /= np.linalg.norm(d); tips += list(scr(pts[i] + d * lang * 1.1))
                row[2:] = tips
            rij.append(row)
        uit['nabij' if sz > 0 else 'ver'] = np.array(rij)
    np.save(os.path.join(HERE, 'spriet_as.npy'), np.stack([uit['nabij'], uit['ver']]))
    # oogcentra (alleen de plek markeren)
    for sz in (1, -1):
        d = np.array((Q.OOG[0], Q.OOG[1], Q.OOG[2] * sz)); d /= np.linalg.norm(d)
        print('oog', 'nabij' if sz > 0 else 'ver', ['%.1f' % v for v in scr(cr + d * kop_r * 0.80)])
    Q.gebruik_kleuren()
    img, _a, _, _ = Q.view(Q.poedelmot(), out=512); img.save(os.path.join(HERE, 'onderlaag_512.png'))
    ys, xs = np.nonzero(M)
    print('zonder poten:', int(M.sum()), 'px, box', xs.min(), xs.max(), ys.min(), ys.max(), '| met poten:', int((blok(a) >= .5).sum()))
    for i in range(6):
        yy, xx = np.nonzero(pr[i] >= .5)
        if len(yy): print(f'poot {i}: x{xx.min()}-{xx.max()} y{yy.min()}-{yy.max()}, {len(yy)} px')
