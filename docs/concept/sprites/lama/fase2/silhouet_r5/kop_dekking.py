"""Hulpscript ronde 5f: rendert het poppetje (zelfde camera/pose als bron.py, fill 0.99; alfa intern op 768) en drukt per 64-pixel
in de kopzone (y0-21, x8-31) de dekking in tienden af (0-9, '#'=volledig). Dit is de overtrekmaat; de spans zet de maker met de hand.
Draaien vanuit deze map: python3 kop_dekking.py"""
import os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../ontwerp'))
import pop3d_lama as L
import bron
P = L.P
L.set_vacht('karamel (foto 1)'); L.COL['lid'] = L.COL['head']
m = L.fase2_r4('F_pas', head_yaw=55); fill = 0.99
Rc = P.rot_x(math.radians(bron.PITCH)) @ P.rot_y(math.radians(bron.YAW))
pts = np.array([Rc @ c for c, r, R0, g in m.parts]); rs = np.array([r.max() for c, r, R0, g in m.parts])
x0, x1, y0, y1 = (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()
scale = L.R * fill / max(x1 - x0, y1 - y0)
c = ((x0 + x1) / 2, (y0 + y1) / 2 + (1 - fill) * L.R / scale * 0.5)
zbuf, gid, nrm, groups = L.render(m, bron.YAW, bron.PITCH, scale, c)
under, a = L.shade(zbuf, gid, nrm, groups, out=256)
a = np.asarray(a, float)
np.save(os.path.join(HERE, 'kop_alpha.npy'), a)
k = a.shape[0] // 64; cov = a.reshape(64, k, 64, k).mean((1, 3))
print('     ' + ''.join(str(x % 10) for x in range(8, 32)))
for y in range(0, 24):
    print(f'y{y:02d}  ' + ''.join('#' if v > 0.95 else ('.' if v < 0.05 else str(int(v * 10))) for v in cov[y, 8:32]))
