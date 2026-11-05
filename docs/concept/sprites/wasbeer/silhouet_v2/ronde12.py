"""Silhouet ronde 12: klauw uit het 3D-ontwerp (klauw3d.py, Jordi: "dit is prima, driekwart in de sprite").
Het ontwerp met klauw='paar' (2 klauwen naast elkaar, inkeping bij de punten, 1,4x) gerenderd met EXACT dezelfde
uitsnede als direct.txt (kader van het oude model), direct verkleind; alleen de klauwzone (x 3-14, y 31-44) uit
die render, de rest = ronde2.txt (bevroren). Draaien: python3 docs/concept/sprites/wasbeer/silhouet_v2/ronde12.py"""
import os, sys, math
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import direct as D
W, P = D.W, D.P
KS = 1.2


def render_kader(m_kader, m, fill=1.03):
    Rc = P.rot_x(math.radians(D.PITCH)) @ P.rot_y(math.radians(D.YAW))
    pts = np.array([Rc @ c for c, r, R0, g in m_kader.parts]); rs = np.array([r.max() for c, r, R0, g in m_kader.parts])
    x0, x1, y0, y1 = (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()
    scale = W.R * fill / max(x1 - x0, y1 - y0)
    return W.render(m, D.YAW, D.PITCH, scale, ((x0 + x1) / 2, (y0 + y1) / 2))


oud = W.wasbeer(**D.GEKOZEN)
nieuw = W.wasbeer(**dict(D.GEKOZEN, klauw='paar', klauw_s=KS))
zb, gid, nrm, groups = render_kader(oud, nieuw)
sil = np.array(Image.fromarray(((gid >= 0) * 255).astype(np.uint8)).resize((64, 64), Image.BOX)) > 110
zb0, gid0, _, _ = render_kader(oud, oud)
sil0 = np.array(Image.fromarray(((gid0 >= 0) * 255).astype(np.uint8)).resize((64, 64), Image.BOX)) > 110
direct = np.array([[c == '#' for c in r.rstrip('\n')] for r in open(os.path.join(HERE, 'direct.txt')) if r.strip()])
print('controle kader: oud model opnieuw = direct.txt?', (sil0 != direct).sum(), 'px verschil')
r2 = np.array([[c == '#' for c in r.rstrip('\n')] for r in open(os.path.join(HERE, 'ronde2.txt')) if r.strip()])
a = r2.copy()
Z = (slice(31, 45), slice(3, 15))
a[Z] = sil[Z]
d = a != r2
print('t.o.v. ronde2', d.sum(), 'totaal', a.sum())
open(os.path.join(HERE, 'ronde12.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in a) + '\n')
Image.fromarray((a * 255).astype(np.uint8)).save(os.path.join(HERE, 'ronde12_1x.png'))
img = W.shade(zb, gid, nrm, groups, out=256)[0]
img.save(os.path.join(HERE, 'onderlaag_r12_256.png'))
K = 16
vel = Image.new('RGB', (12 * K * 2 + 40 + 64 + 140, 14 * K), 'white'); px = vel.load()
und = img.resize((1024, 1024), Image.LANCZOS).crop((3 * 16, 31 * 16, 15 * 16, 45 * 16))
vel.paste(und, (0, 0))
for y in range(31, 45):
    for x in range(3, 15):
        c = (40, 34, 34) if a[y, x] else (255, 255, 255)
        for dy in range(K):
            for dx in range(K):
                px[12 * K + 20 + (x - 3) * K + dx, (y - 31) * K + dy] = c if (dx and dy) else (205, 205, 215)
one = Image.fromarray(np.where(a, 40, 255).astype(np.uint8)).convert('RGB')
vel.paste(one, (24 * K + 40, 0)); vel.paste(one.resize((128, 128), Image.NEAREST), (24 * K + 40 + 70, 0))
vel.save(os.path.join(HERE, 'vel_ronde12_klauw.png'))
