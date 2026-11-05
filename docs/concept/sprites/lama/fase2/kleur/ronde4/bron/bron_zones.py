"""Kijkscript ronde 4 (geen tekenen): rendert het goedgekeurde poppetje met dezelfde camera als silhouet_r5/kop_dekking.py
en drukt per 64-pixel de meest voorkomende onderdeelgroep af (zones.txt) plus de lichtkant (l/s per pixel, licht.txt).
Dit is alleen de kaart waar de onderdelen van het model liggen; de kleuren in lama.png zijn met de hand gezet.
Draaien vanuit deze map: python3 bron_zones.py"""
import os, sys, math
from collections import Counter
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../silhouet_r5'))
sys.path.insert(0, os.path.join(HERE, '../../../../ontwerp'))
import pop3d_lama as L
import bron
P = L.P
L.set_vacht('karamel (foto 1)'); L.COL['lid'] = L.COL['head']; L.COL['lip'] = '#8A5530'
m = L.fase2_r4('F_pas', head_yaw=55); fill = 0.99
Rc = P.rot_x(math.radians(bron.PITCH)) @ P.rot_y(math.radians(bron.YAW))
pts = np.array([Rc @ c for c, r, R0, g in m.parts]); rs = np.array([r.max() for c, r, R0, g in m.parts])
x0, x1, y0, y1 = (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()
scale = L.R * fill / max(x1 - x0, y1 - y0)
c = ((x0 + x1) / 2, (y0 + y1) / 2 + (1 - fill) * L.R / scale * 0.5)
zbuf, gid, nrm, groups = L.render(m, bron.YAW, bron.PITCH, scale, c)
CODE = {'body': 'w', 'neck': 'w', 'tail': 't', 'head': 'k', 'lid': 'l', 'ear': 'e', 'earin': 'i', 'leg': 'p', 'far': 'f',
        'muzzle': 'm', 'nose': 'n', 'eye': 'o', 'glint': '*', 'hoof': 'h', 'glove': 'G', 'strap': 'S', 'nail': 'N',
        'tassel': 'T', 'lip': 'L', 'pp_r': 'P', 'pp_y': 'P', 'pp_g': 'P', 'pp_p': 'P'}
for i in range(7): CODE[f'ag{i}'] = str(i)
Lt = np.array((-0.45, 0.65, 0.62)); Lt /= np.linalg.norm(Lt)
lit = (nrm @ Lt)
k = L.R // 64
zones, licht = [], []
for y in range(64):
    zr, lr = '', ''
    for x in range(64):
        g = gid[y*k:(y+1)*k, x*k:(x+1)*k].ravel()
        g = g[g >= 0]
        if len(g) < k*k/2: zr += '.'; lr += '.'; continue
        top = Counter(g).most_common(1)[0][0]
        zr += CODE.get(groups[top], '?')
        v = lit[y*k:(y+1)*k, x*k:(x+1)*k].ravel()[(gid[y*k:(y+1)*k, x*k:(x+1)*k].ravel() >= 0)].mean()
        lr += 'H' if v > 0.75 else 'l' if v > 0.35 else 'b' if v > 0 else 's' if v > -0.35 else 'd'
    zones.append(zr); licht.append(lr)
open(os.path.join(HERE, 'bron_zones.txt'), 'w').write('\n'.join(zones) + '\n')
open(os.path.join(HERE, 'bron_licht.txt'), 'w').write('\n'.join(licht) + '\n')
print('\n'.join(f'{i:02d} {z}  {l}' for i, (z, l) in enumerate(zip(zones, licht))))
