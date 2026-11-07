"""Wasbeer silhouet v2 ronde 2: ronde1.txt + reparaties uit KEURING_ronde1.md, als expliciete pixellijsten (x, y).
Diff tegen ronde1.txt en direct.txt. Dekking = deel van het 4x4-blok in onderlaag_256.png dat niet wit is.
Draaien: python3 docs/concept/sprites/wasbeer/silhouet_v2/ronde2.py"""
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))

ZONES = {
    # Zone 1 verre klauw: eindstuk 3x3-blok (x 8-10, y 35-37; spleet in de punt = kleurwerk); pols: steel 2 px tegen onderarm 4-5 px.
    '1 verre klauw': dict(rect=(6, 30, 19, 39), aan=[(9, 37)], uit=[(16, 33), (17, 33)]),
    # Zone 2 buidel/staart: knobbel/gat bovenaan de zak dicht; staart van zuil/knots naar haak (rechterrand taps,
    # top smaller, holte onder de haakpunt 1 px dieper zodat de punt x 46-47, y 22-27 als lob over de spleet hangt).
    '2 buidel/staart': dict(rect=(33, 15, 56, 40), aan=[(39, 18)],
                            uit=[(54, 23), (54, 31), (54, 32), (54, 33), (53, 20), (53, 21), (48, 28), (48, 29), (48, 30)]),
    # Rand ±1 px: kop (deuk achterhoofd dicht, neus 1 px vooruit), beenranden (trapjes weg).
    'R kop': dict(rect=(12, 6, 31, 16), aan=[(30, 8), (12, 14), (12, 15)], uit=[]),
    # Zone 4 nabije voet (ronde 1: teen (37,60)); in ronde 2 ongewijzigd, staat erbij voor de diff tegen direct.txt.
    '4 nabije voet': dict(rect=(35, 58, 41, 61), aan=[], uit=[]),
    'R benen': dict(rect=(25, 49, 39, 59), aan=[(26, 50), (38, 56), (28, 58)], uit=[]),
}


def lees(p):
    return np.array([[c != '.' for c in r.rstrip('\n')] for r in open(p) if r.strip() and not r.startswith('#')])


def main():
    D, A = lees(os.path.join(HERE, 'direct.txt')), lees(os.path.join(HERE, 'ronde1.txt'))
    u = np.array(Image.open(os.path.join(HERE, 'onderlaag_256.png')).convert('RGBA')).astype(int)
    nw = (u[..., 3] > 0) & (u[..., :3].sum(-1) < 720)
    dek = lambda x, y: nw[y * 4:y * 4 + 4, x * 4:x * 4 + 4].mean()
    B = A.copy()
    for n, z in ZONES.items():
        for x, y in z['aan']:
            assert not A[y, x], ('al aan', x, y); B[y, x] = True
        for x, y in z['uit']:
            assert A[y, x], ('al uit', x, y); B[y, x] = False
        print(f'zone {n}: {len(z["aan"]) + len(z["uit"])} px | aan ' +
              ' '.join(f'{p}:{dek(*p):.2f}' for p in z['aan']) + ' | uit ' + ' '.join(f'{p}:{dek(*p):.2f}' for p in z['uit']))
    open(os.path.join(HERE, 'ronde2.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in B) + '\n')
    im = Image.new('P', (64, 64), 0)
    im.putpalette([255, 255, 255, 40, 34, 34] + [0] * 762)
    im.putdata([1 if v else 0 for v in B.flatten()])
    im.save(os.path.join(HERE, 'ronde2_1x.png'), transparency=0)
    ys, xs = np.nonzero(B)
    for naam, ref in (('ronde1', A), ('direct', D)):
        diff = np.argwhere(ref != B)
        buiten = [(x, y) for y, x in diff if not any(z['rect'][0] <= x <= z['rect'][2] and z['rect'][1] <= y <= z['rect'][3] for z in ZONES.values())]
        print(f'diff tegen {naam}: {len(diff)} px, buiten de zones {len(buiten)}')
    print(f'{B.sum()} px, box {xs.max() - xs.min() + 1}x{ys.max() - ys.min() + 1}')


if __name__ == '__main__':
    main()
