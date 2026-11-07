"""Lama fase 2, stap 2 (ronde 5): bron voor het silhouet. Het goedgekeurde poppetje ronde 5 pose F (lijf horizontaal, kop driekwart, alle poten op de grond)
in de hoek van foto 1 (yaw 40, pitch 8) -> onderlaag_256.png (met lijnen) en direct.txt (64x64, direct verkleind: de massa).
Draaien vanuit de repo-root: python3 docs/concept/sprites/lama/fase2/silhouet_r5/bron.py [fill]"""
import os, sys, math
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../ontwerp'))
import pop3d_lama as L
P = L.P
YAW, PITCH, HS = 8, 8, 1.45

if __name__ == '__main__':
    fill = float(sys.argv[1]) if len(sys.argv) > 1 else 0.86
    L.set_vacht('karamel (foto 1)'); L.COL['lid'] = L.COL['head']
    m = L.fase2_r4('F_pas', head_yaw=55)   # Jordi: F, alle poten zichtbaar   # hals iets korter + voller lijf: groter dan fase 1 binnen 64 hoog
    Rc = P.rot_x(math.radians(PITCH)) @ P.rot_y(math.radians(YAW))
    pts = np.array([Rc @ c for c, r, R0, g in m.parts]); rs = np.array([r.max() for c, r, R0, g in m.parts])
    x0, x1, y0, y1 = (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()
    scale = L.R * fill / max(x1 - x0, y1 - y0)
    c = ((x0 + x1) / 2, (y0 + y1) / 2 + (1 - fill) * L.R / scale * 0.5)   # onderaan uitlijnen (voeten bij de rand)
    zbuf, gid, nrm, groups = L.render(m, YAW, PITCH, scale, c)
    under, a = L.shade(zbuf, gid, nrm, groups, out=256)
    under.save(os.path.join(HERE, 'onderlaag_256.png'))
    sil = np.array(Image.fromarray((a * 255).astype(np.uint8)).resize((64, 64), Image.BOX)) > 110
    open(os.path.join(HERE, 'direct.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in row) for row in sil) + '\n')
    Image.fromarray((~sil * 255).astype(np.uint8)).save(os.path.join(HERE, 'direct_1x.png'))
    ys, xs = np.nonzero(sil)
    print('fill', fill, 'px', sil.sum(), 'box', xs.max() - xs.min() + 1, ys.max() - ys.min() + 1, 'y', ys.min(), ys.max())
