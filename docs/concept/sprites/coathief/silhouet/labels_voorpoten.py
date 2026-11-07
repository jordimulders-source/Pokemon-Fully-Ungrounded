"""Welk onderdeel is elke silhouetpixel in de voorpotenzone (x 8-33, y 48-62), afgelezen van de onderlaag-render
(meerderheid per 12x12-blok). Jordi (25 okt) over het silhouet over de onderlaag: "hier gaat ie goed" -> de kleur volgt
deze indeling. Labels: N = opgetilde nabije poot (donker), F = staande verre poot (donker, schaduw), c = klauw,
v = vacht (borst/bovenarm, roodbruin), k = kop, . = transparant."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, silhouet_direct as S
m, scale, c, zbuf, gid, nrm, groups = S.render(0.98)
sil = np.array([[ch == '#' for ch in l.rstrip()] for l in open(os.path.join(os.path.dirname(__file__), 'ronde4.txt'))])
G = {'leg': 'N', 'farleg': 'F', 'far': 'F', 'claw': 'c', 'fur': 'v', 'head': 'k', 'muzzle': 'k', 'ring': 'k', 'spot': 'k',
     'eye': 'k', 'pupil': 'k', 'nose': 'k', 'ear': 'k', 'earin': 'k'}
k = gid.shape[0] // 64
out = []
for y in range(48, 63):
    s = ''
    for x in range(8, 34):
        if not sil[y, x]: s += '.'; continue
        blk = gid[y * k:(y + 1) * k, x * k:(x + 1) * k].ravel(); blk = blk[blk >= 0]
        if len(blk) == 0:
            # geen render hier (handreparatie): neem het dichtstbijzijnde gerenderde blok
            yy, xx = np.nonzero(gid[max(0, (y - 2) * k):(y + 3) * k, max(0, (x - 2) * k):(x + 3) * k] >= 0)
            sub = gid[max(0, (y - 2) * k):(y + 3) * k, max(0, (x - 2) * k):(x + 3) * k]
            blk = sub[sub >= 0]
        if len(blk) == 0: s += '?'; continue
        vals, cnt = np.unique(blk, return_counts=True)
        s += G.get(groups[vals[cnt.argmax()]], 'v')
    out.append('%02d %s' % (y, s))
txt = '\n'.join(out) + '\n    x = 8..33\n'
open(os.path.join(os.path.dirname(__file__), 'labels_voorpoten.txt'), 'w').write(txt); print(txt)
