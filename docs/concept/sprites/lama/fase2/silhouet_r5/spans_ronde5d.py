"""Lama fase 2, silhouet ronde 5d: ronde5c.txt + de staartpluim terug (Jordi: "als c nu gewoon een staart zou hebben,
zou die het beste zijn"). Alleen de staartzone y19-24, x47-53 verandert; met de hand gezet als spans.
Draaien: python3 spans_ronde5d.py -> ronde5d.txt + ronde5d_1x.png"""
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
def load(p): return np.array([[c == '#' for c in l.rstrip('\n')] for l in open(os.path.join(HERE, p)) if l.strip()])
C = load('ronde5c.txt'); S = C.copy()
Y0, Y1, X0, X1 = 19, 24, 47, 53                       # staartzone
# staartpluim: ronde koepel die boven het kruis opstaat en licht naar achteren helt; y24 = kruis (rug x42-) + staartvoet
STAART = {19: (49, 51), 20: (48, 52), 21: (47, 53), 22: (47, 53), 23: (47, 53), 24: (47, 52)}
for y, (a, b) in STAART.items(): S[y, a:b + 1] = True
if __name__ == '__main__':
    open(os.path.join(HERE, 'ronde5d.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in S) + '\n')
    im = np.zeros((64, 64, 4), np.uint8); im[S] = (0, 0, 0, 255)
    Image.fromarray(im, 'RGBA').save(os.path.join(HERE, 'ronde5d_1x.png'))
    D = S ^ C; zone = np.zeros_like(S); zone[Y0:Y1 + 1, X0:X1 + 1] = True
    ys, xs = np.nonzero(S)
    print('px', S.sum(), '(5c', C.sum(), ') box', xs.max() - xs.min() + 1, 'x', ys.max() - ys.min() + 1)
    print('staartzone y%d-%d x%d-%d: +%d / -%d' % (Y0, Y1, X0, X1, (S & ~C & zone).sum(), (C & ~S & zone).sum()))
    print('diff buiten de staartzone:', int((D & ~zone).sum()), 'px; kop/oren/hals/halsband x<=27 y0-30:', int(D[:31, :28].sum()), 'px')
