"""Lama fase 2, silhouet ronde 5c: ronde5b.txt + precies de reparaties R1-R6 uit KEURING_5b.md, met de hand als losse
pixelwijzigingen (y, x0, x1, +1 erbij / -1 eraf). Draaien: python3 spans_ronde5c.py -> ronde5c.txt + ronde5c_1x.png"""
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
def load(p): return np.array([[c == '#' for c in l.rstrip('\n')] for l in open(os.path.join(HERE, p)) if l.strip()])
B = load('ronde5b.txt'); S = B.copy()
R = {
 'R1 rug oplopend schoft->kruis': [(26, 28, 29, +1), (26, 39, 44, +1), (25, 34, 45, +1), (24, 42, 46, +1)],
 'R2 deuk onder staart weg':      [(28, 52, 52, +1), (29, 52, 52, +1)],
 'R3 buik als een boog':          [(43, 31, 32, +1), (45, 35, 37, -1)],
 'R4 nabije onderbenen 5 px':     [(51, 15, 15, +1), (53, 19, 19, +1), (54, 19, 19, +1),
                                   (53, 44, 44, +1), (54, 44, 44, +1), (55, 43, 43, +1), (56, 43, 43, +1)],
 'R5 achtervoeten hoeven':        [(59, 37, 37, -1), (59, 44, 44, -1), (60, 37, 37, -1), (60, 44, 44, -1),
                                   (57, 52, 52, -1), (58, 52, 52, -1)],
 'R6 handschoenen op de grond':   [(62, 14, 14, +1), (62, 19, 19, +1), (55, 32, 32, -1), (56, 32, 32, -1),
                                   (57, 32, 32, -1), (58, 32, 32, -1), (60, 26, 26, +1), (60, 31, 31, +1)],
}
zone = np.zeros_like(S)
if __name__ == '__main__':
    for n, ops in R.items():
        plus = minus = 0
        for y, a, b, v in ops:
            for x in range(a, b + 1):
                zone[y, x] = True
                if v > 0 and not S[y, x]: S[y, x] = True; plus += 1
                elif v < 0 and S[y, x]: S[y, x] = False; minus += 1
        print(f'{n:32s} +{plus} / -{minus}')
    open(os.path.join(HERE, 'ronde5c.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in S) + '\n')
    im = np.zeros((64, 64, 4), np.uint8); im[S] = (0, 0, 0, 255)
    Image.fromarray(im, 'RGBA').save(os.path.join(HERE, 'ronde5c_1x.png'))
    ys, xs = np.nonzero(S); D = S ^ B
    print('px', S.sum(), '(5b', B.sum(), ') box', xs.max() - xs.min() + 1, 'x', ys.max() - ys.min() + 1, '| totaal +', int((S & ~B).sum()), '-', int((B & ~S).sum()))
    print('diff kop/oren/hals/halsband x<=27, y0-30:', int(D[:31, :28].sum()), 'px')
    print('diff x<=31, y0-30:', int(D[:31, :32].sum()), 'px (', [(int(y), int(x)) for y, x in zip(*np.nonzero(D[:31, :32]))], ')')
    print('diff buiten de R-zones:', int((D & ~zone).sum()), 'px')
