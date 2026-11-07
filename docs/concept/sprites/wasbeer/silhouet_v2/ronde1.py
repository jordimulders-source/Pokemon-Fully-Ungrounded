"""Wasbeer silhouet v2 ronde 1: direct.txt (render E2, direct verkleind) + handwerk in benoemde zones.
Elke wijziging staat hieronder als expliciete pixel (x, y); niets wordt berekend of getekend met vormen.
Draaien: python3 docs/concept/sprites/wasbeer/silhouet_v2/ronde1.py"""
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))

# Zone 1 verre klauw (x 6-19, y 30-39): korte koevoet. Steel (2 rijen, y 33-34) loopt door in de lijn van de onderarm
# schuin naar links-omlaag, buitenhoek van de bocht op (8,34), eindstuk 3 px breed omlaag (x 8-10, y 35-36),
# punt gespleten in 2 tanden (8,37) en (10,37) met de inkeping op (9,37). Rest van de oude klodder weg.
Z1 = dict(rect=(6, 30, 19, 39),
          aan=[(10, 33), (8, 34), (8, 35), (8, 36), (8, 37)],
          uit=[(11, 35), (12, 35), (13, 35), (11, 36), (12, 36), (11, 37)])

# Zone 2 lucht tussen buidel en staart (x 36-48, y 19-38): spleet van 2 px op y 24-30, alleen van de staartrand
# (linkerrand van de neerhangende staarthaak); geen pixel van de buidel.
Z2 = dict(rect=(36, 19, 48, 38),
          aan=[],
          uit=[(46, 24), (46, 25), (45, 26), (46, 26), (46, 27), (47, 27), (46, 28), (47, 28),
               (46, 29), (47, 29), (47, 30)])

# Zone 3 nabije klauw (x 20-27, y 23-28): ligt binnen het silhouet, 0 px (kleurwerk, zie NOTITIES_ronde1.md).
Z3 = dict(rect=(20, 23, 27, 28), aan=[], uit=[])

# Zone 4 nabije voet (x 35-41, y 58-61): losse teenpixel (38,60) was een 1-px sliert; teen 2 px breed (onderlaag: punt op x 37-38).
Z4 = dict(rect=(35, 58, 41, 61), aan=[(37, 60)], uit=[])

ZONES = {'1 verre klauw': Z1, '2 buidel/staart': Z2, '3 nabije klauw': Z3, '4 nabije voet': Z4}


def lees(p):
    return np.array([[c != '.' for c in r.rstrip('\n')] for r in open(p) if r.strip() and not r.startswith('#')])


def main():
    A = lees(os.path.join(HERE, 'direct.txt'))
    B = A.copy()
    for z in ZONES.values():
        for x, y in z['aan']:
            assert not A[y, x], ('al aan', x, y)
            B[y, x] = True
        for x, y in z['uit']:
            assert A[y, x], ('al uit', x, y)
            B[y, x] = False
    open(os.path.join(HERE, 'ronde1.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in B) + '\n')
    im = Image.new('P', (64, 64), 0)
    im.putpalette([255, 255, 255, 40, 34, 34] + [0] * 762)
    im.putdata([1 if v else 0 for v in B.flatten()])
    im.save(os.path.join(HERE, 'ronde1_1x.png'), transparency=0)
    diff = np.argwhere(A != B)
    totaal = 0
    for n, z in ZONES.items():
        x0, y0, x1, y1 = z['rect']
        k = sum(1 for y, x in diff if x0 <= x <= x1 and y0 <= y <= y1)
        totaal += k
        print(f'zone {n}: {k} px ({len(z["aan"])} aan, {len(z["uit"])} uit)')
    buiten = [(x, y) for y, x in diff if not any(z['rect'][0] <= x <= z['rect'][2] and z['rect'][1] <= y <= z['rect'][3] for z in ZONES.values())]
    ys, xs = np.nonzero(B)
    print(f'totaal gewijzigd {len(diff)} px | buiten de zones {len(buiten)} | {A.sum()} -> {B.sum()} px, box {xs.max() - xs.min() + 1}x{ys.max() - ys.min() + 1}')


if __name__ == '__main__':
    main()
