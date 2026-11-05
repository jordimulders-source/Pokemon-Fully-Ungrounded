"""Lama fase 3, stap 2: bron voor het silhouet. Goedgekeurd ontwerp (Jordi 5 nov: "Doe maar Y en zonder franje"):
fase3_r4('Y') in ontwerp/fase3_r4.py, pose C2 (Jordi 5 nov: "ik zie C2 wel zitten"): camera yaw 45, kop +18, pitch 8. Schrijft:
- onderlaag_256.png (render met lijnen), alpha.npy (alfa op 768, voor dekkingsmetingen)
- model50.txt (64x64 op de 50%-dekkingsgrens = het over te trekken silhouet), model50_1x.png
- dekking.txt (dekking per 64-pixel in tienden: '.'=0, '#'=vol, 1-9 = deels)
Draaien vanuit de repo-root: python3 docs/concept/sprites/lama/fase3/silhouet/bron.py [fill]"""
import os, sys, math
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../ontwerp'))
import pop3d_lama as L
import fase3_r4 as F4
P = L.P
YAW, PITCH, HEAD_YAW = 45, 8, 18
W3 = dict(breed=1.26, nr=7, legk=1.85)   # Jordi 5 nov: "eigenlijk vind ik W3 wel goed" (ronde 1 = zonder W3)

if __name__ == '__main__':
    fill = float(sys.argv[1]) if len(sys.argv) > 1 else 0.99
    L.set_vacht('bont (foto 4)'); L.COL['lid'] = L.COL['head']; L.COL['lip'] = '#C9A982'
    F4.HEAD_YAW = HEAD_YAW
    m = F4.fase3_r4('Y', **W3)
    Rc = P.rot_x(math.radians(PITCH)) @ P.rot_y(math.radians(YAW))
    pts = np.array([Rc @ c for c, r, R0, g in m.parts]); rs = np.array([r.max() for c, r, R0, g in m.parts])
    x0, x1, y0, y1 = (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()
    scale = L.R * fill / max(x1 - x0, y1 - y0)
    c = ((x0 + x1) / 2, (y0 + y1) / 2 + (1 - fill) * L.R / scale * 0.5)
    zbuf, gid, nrm, groups = L.render(m, YAW, PITCH, scale, c)
    under, a = L.shade(zbuf, gid, nrm, groups, out=256)
    under.save(os.path.join(HERE, 'onderlaag_256.png'))
    a = np.asarray(a, float); np.save(os.path.join(HERE, 'alpha.npy'), a)
    k = a.shape[0] // 64; cov = a.reshape(64, k, 64, k).mean((1, 3)); M = cov >= 0.5
    open(os.path.join(HERE, 'model50.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in M) + '\n')
    Image.fromarray((~M * 255).astype(np.uint8)).save(os.path.join(HERE, 'model50_1x.png'))
    open(os.path.join(HERE, 'dekking.txt'), 'w').write('\n'.join(
        ''.join('#' if v > 0.95 else ('.' if v < 0.05 else str(int(v * 10))) for v in r) for r in cov) + '\n')
    ys, xs = np.nonzero(M)
    print('fill', fill, 'px', int(M.sum()), 'box', xs.max() - xs.min() + 1, ys.max() - ys.min() + 1, 'x', xs.min(), xs.max(), 'y', ys.min(), ys.max())
