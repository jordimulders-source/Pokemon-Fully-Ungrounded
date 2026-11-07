"""Kleur fase 3 ronde 1: leest per 64-pixel af welk onderdeel van het poppetje daar zichtbaar is (meerderheid van de
12x12 subpixels in de render, zelfde camera als silhouet/bron.py, W3). Alleen ter oriëntatie bij het met de hand tekenen.
Schrijft labels.txt (één letter per onderdeel, legenda onderaan) en licht.txt (0-9: hoeveel van de cel naar het licht kijkt).
Draaien: python3 labels.py"""
import os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SIL = os.path.join(HERE, '../../../silhouet')
sys.path.insert(0, os.path.join(HERE, '../../../../ontwerp'))
import pop3d_lama as L
import fase3_r4 as F4
P = L.P
YAW, PITCH, HEAD_YAW = 45, 8, 18
W3 = dict(breed=1.26, nr=7, legk=1.85)
L.set_vacht('bont (foto 4)'); L.COL['lid'] = L.COL['head']; L.COL['lip'] = '#C9A982'
F4.HEAD_YAW = HEAD_YAW
m = F4.fase3_r4('Y', **W3)
fill = 0.99
Rc = P.rot_x(math.radians(PITCH)) @ P.rot_y(math.radians(YAW))
pts = np.array([Rc @ c for c, r, R0, g in m.parts]); rs = np.array([r.max() for c, r, R0, g in m.parts])
x0, x1, y0, y1 = (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()
scale = L.R * fill / max(x1 - x0, y1 - y0)
c = ((x0 + x1) / 2, (y0 + y1) / 2 + (1 - fill) * L.R / scale * 0.5)
zbuf, gid, nrm, groups = L.render(m, YAW, PITCH, scale, c)
used = sorted(set(int(g) for g in np.unique(gid) if g >= 0))
names = [groups[i] for i in used]
LET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
lm = {u: LET[i] for i, u in enumerate(used)}
k = gid.shape[0] // 64
Lt = np.array((-0.45, 0.65, 0.62)); Lt /= np.linalg.norm(Lt)
lit = (nrm @ Lt)
S = np.array([[ch == '#' for ch in l.rstrip('\n')] for l in open(os.path.join(SIL, 'ronde2.txt')) if l.strip()])
rows, lrows = [], []
for y in range(64):
    r, lr = '', ''
    for x in range(64):
        g = gid[y*k:(y+1)*k, x*k:(x+1)*k].ravel(); g = g[g >= 0]
        if not S[y, x]: r += '.'; lr += '.'; continue
        if len(g) == 0: r += '?'; lr += '?'; continue
        v, n = np.unique(g, return_counts=True); r += lm[int(v[n.argmax()])]
        li = lit[y*k:(y+1)*k, x*k:(x+1)*k].reshape(-1)[gid[y*k:(y+1)*k, x*k:(x+1)*k].ravel() >= 0]
        lr += str(min(9, max(0, int((li.mean() + 1) * 5))))
    rows.append(r); lrows.append(lr)
leg = '\n'.join(f'{lm[u]} = {groups[u]} ({L.COL.get(groups[u], "")})' for u in used)
open(os.path.join(HERE, 'labels.txt'), 'w').write('\n'.join(f'y{y:02d} {r}' for y, r in enumerate(rows)) + '\n\n' + leg + '\n')
open(os.path.join(HERE, 'licht.txt'), 'w').write('\n'.join(f'y{y:02d} {r}' for y, r in enumerate(lrows)) + '\n')
print(leg)
