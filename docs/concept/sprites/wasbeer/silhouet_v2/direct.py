"""Wasbeer stap 2: het gekozen 3D-ontwerp (E2, rugzak +3; Jordi 2 nov) direct verkleind naar 64x64 (massa = bron),
zoals coathief/silhouet/silhouet_direct.py. Geen handwerk hier; reparaties alleen in benoemde zones (klauwen).
Draaien: python3 docs/concept/sprites/wasbeer/silhouet_v2/direct.py [fill]"""
import os, sys, math
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../ontwerp'))
import pop3d_v2 as W
P = W.P
YAW, PITCH, BOX = 50, 8, 64
GEKOZEN = dict(W.E, near_back=12, shin_k=0.7, heel=5, pouch_k=3, pouch_z=4)


def render(fill):
    m = W.wasbeer(**GEKOZEN)
    Rc = P.rot_x(math.radians(PITCH)) @ P.rot_y(math.radians(YAW))
    pts = np.array([Rc @ c for c, r, R0, g in m.parts]); rs = np.array([r.max() for c, r, R0, g in m.parts])
    x0, x1, y0, y1 = (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()
    scale = W.R * fill / max(x1 - x0, y1 - y0)
    return W.render(m, YAW, PITCH, scale, ((x0 + x1) / 2, (y0 + y1) / 2))


def direct(fill, thr=110):
    zbuf, gid, nrm, groups = render(fill)
    sil = np.array(Image.fromarray(((gid >= 0) * 255).astype(np.uint8)).resize((BOX, BOX), Image.BOX)) > thr
    # onderdelen per spritepixel (meerderheid), voor de maker: welke pixel is klauw, arm, been, zak, ...
    k = W.R // BOX
    lab = np.full((BOX, BOX), '.', '<U1')
    code = {'claw': 'K', 'farclaw': 'k', 'limb': 'A', 'farlimb': 'a', 'pouch': 'Z', 'lip': 'Z', 'tailL': 'S', 'tailD': 'S'}
    for y in range(BOX):
        for x in range(BOX):
            if sil[y, x]:
                blk = gid[y * k:(y + 1) * k, x * k:(x + 1) * k].ravel(); blk = blk[blk >= 0]
                g = groups[np.bincount(blk).argmax()] if len(blk) else 'body'
                lab[y, x] = code.get(g, '#')
    under = W.shade(zbuf, gid, nrm, groups, out=256)[0]
    return sil, lab, under


if __name__ == '__main__':
    fill = float(sys.argv[1]) if len(sys.argv) > 1 else 0.92
    sil, lab, under = direct(fill)
    ys, xs = np.nonzero(sil)
    print('fill', fill, 'px', sil.sum(), 'box', xs.max() - xs.min() + 1, ys.max() - ys.min() + 1)
    open(os.path.join(HERE, 'direct.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in sil) + '\n')
    open(os.path.join(HERE, 'labels.txt'), 'w').write('# K/k = nabije/verre klauw, A/a = nabije/verre onderarm+onderbeen (donker), Z = buidel, S = staart, # = rest\n'
                                                     + '\n'.join(''.join(r) for r in lab) + '\n')
    Image.fromarray((sil * 255).astype(np.uint8)).save(os.path.join(HERE, 'direct_1x.png'))
    under.save(os.path.join(HERE, 'onderlaag_256.png'))
