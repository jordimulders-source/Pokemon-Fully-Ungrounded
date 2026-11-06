"""Onderlaag-labels: welk onderdeel van het 3D-poppetje ligt op welke 64x64-pixel (meerderheid per cel).
Hulpmiddel voor het handwerk; schrijft ronde1/labels.txt. Draaien vanuit de repo-root."""
import os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(HERE)
sys.path.insert(0, K)
import pop3d
YAW, PITCH = 44, 8
m = pop3d.bird(extra=32, curl=0.5)
x0, x1, y0, y1 = pop3d.bbox(m, YAW, PITCH)
scale = pop3d.R * (236 / 256) / max(x1 - x0, y1 - y0)
zb, gid, nrm, groups = pop3d.render(m, YAW, PITCH, scale, ((x0 + x1) / 2, (y0 + y1) / 2))
a = gid >= 0
ys, xs = np.nonzero(a)
crop = gid[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
L = np.array((-0.45, 0.65, 0.62)); L /= np.linalg.norm(L)
lit = ((nrm @ L)[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
h, w = crop.shape
s = min(62 / h, 62 / w)
nw, nh = round(w * s), round(h * s)
ox, oy = (64 - nw) // 2, 63 - nh
CH = {'body':'b','breast':'o','wing':'w','farwing':'f','tail':'t','head':'h','face':'r','beak':'k','eye':'e','glint':'g','fan':'F','fanspot':'s','fanrim':'P','gold':'G','leg':'l','claw':'c'}
sil = np.array(Image.open(os.path.join(K, 'silhouet_v1_1x.png'))) > 128
out = []; litmap=[]
for Y in range(64):
    row = ''; lr=''
    for X in range(64):
        if not sil[Y, X]:
            row += '.'; lr+='.'; continue
        cy0 = int((Y - oy) / s); cy1 = max(cy0 + 1, int((Y - oy + 1) / s))
        cx0 = int((X - ox) / s); cx1 = max(cx0 + 1, int((X - ox + 1) / s))
        blk = crop[max(0,cy0):cy1, max(0,cx0):cx1].ravel(); lb = lit[max(0,cy0):cy1, max(0,cx0):cx1].ravel()
        v = blk[blk >= 0]
        if len(v) == 0:
            row += '?'; lr+='?'; continue
        g = groups[np.bincount(v).argmax()]
        row += CH[g]
        lr += str(min(9,max(0,int((lb[blk>=0].mean()+1)*4.5))))
    out.append('%2d %s' % (Y, row)); litmap.append('%2d %s'%(Y,lr))
open(os.path.join(HERE, 'labels.txt'), 'w').write('\n'.join(out) + '\n\nbelichting (0 donker - 9 licht)\n' + '\n'.join(litmap) + '\n')
print('\n'.join(out)); print(); print('\n'.join(litmap))
