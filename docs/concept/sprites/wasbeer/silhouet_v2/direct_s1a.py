"""Silhouet van de gekozen sluippose S1a (Jordi 2 nov: "S1a, ga maar door naar het silhouet"), direct verkleind
zoals direct.py; de goedgekeurde klauw (klauwpaar, 1,2x) zit in de render.
Draaien: python3 docs/concept/sprites/wasbeer/silhouet_v2/direct_s1a.py [fill]"""
import os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import direct as D
W = D.W
D.GEKOZEN = dict(W.SLUIP[1][1])
assert W.SLUIP[1][0].startswith('S1a')

if __name__ == '__main__':
    fill = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    sil, lab, under = D.direct(fill)
    ys, xs = np.nonzero(sil)
    print('fill', fill, 'px', sil.sum(), 'box', xs.max() - xs.min() + 1, ys.max() - ys.min() + 1)
    open(os.path.join(HERE, 'direct_s1a.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in sil) + '\n')
    open(os.path.join(HERE, 'labels_s1a.txt'), 'w').write('# K/k = nabije/verre klauw, A/a = donkere onderarm/onderbeen, Z = buidel, S = staart, # = rest\n'
                                                         + '\n'.join(''.join(r) for r in lab) + '\n')
    Image.fromarray((sil * 255).astype(np.uint8)).save(os.path.join(HERE, 'direct_s1a_1x.png'))
    under.save(os.path.join(HERE, 'onderlaag_s1a_256.png'))
