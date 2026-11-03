"""Lama fase 2, silhouet ronde 5b: rijen y0-30 komen letterlijk uit ronde5.txt (bevroren: kop, oren, hals, halsband,
aguayo, staart); rijen y31-62 met de hand opnieuw gezet als spans (x0, x1 inclusief): ronde wolmassa + Girafarig/Ponyta-poten.
Draaien: python3 spans_ronde5b.py -> ronde5b.txt + ronde5b_1x.png"""
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
R5 = np.array([[c == '#' for c in l.rstrip('\n')] for l in open(os.path.join(HERE, 'ronde5.txt')) if l.strip()])
S = np.zeros((64, 64), bool)
S[:31] = R5[:31]                                     # bevroren deel (en de staart/romp-top y23-30 ongewijzigd)
ROWS = {
 # --- romp (y31-45): borst als bolle boog onder de halsband, rond achterwerk, onder-de-bil-inham naar de dij -----
 31: [(15, 52)], 32: [(15, 53)], 33: [(14, 53)], 34: [(13, 53)], 35: [(13, 53)], 36: [(12, 52)], 37: [(12, 52)],
 38: [(12, 51)], 39: [(12, 51)], 40: [(13, 51)], 41: [(13, 50)], 42: [(14, 50)],
 # buiklijn: licht bol (laagste punt x35-37), krult bij de poten op (oksel achter de voorpoten, lies voor de achterpoot)
 43: [(15, 30), (33, 50)],
 44: [(16, 29), (34, 50)],
 45: [(17, 29), (35, 37), (40, 50)],
 # --- poten (y46-62): breed uit de wol, smaller naar beneden (onderbeen 4), knie voor, hak achter -----------------
 # nabije voorpoot (NF) schuin naar voren, zachte knie y48; verre voorpoot (FF) licht naar achteren, knie y50;
 # nabije achterpoot (NH) naar voren, hak y49-50 naar achteren; verre achterpoot (FH) naar achteren, hak y50-51.
 46: [(17, 22), (25, 29), (40, 45), (48, 51)],
 47: [(17, 21), (25, 29), (41, 45), (48, 51)],
 48: [(16, 21), (25, 29), (41, 45), (48, 52)],
 49: [(16, 20), (26, 29), (41, 46), (49, 52)],
 50: [(16, 20), (26, 30), (41, 46), (49, 53)],
 51: [(16, 19), (26, 30), (41, 45), (49, 53)],
 52: [(15, 19), (27, 30), (40, 44), (49, 52)],
 53: [(15, 18), (27, 30), (40, 43), (49, 52)],
 54: [(15, 18), (26, 31), (40, 43), (48, 51)],          # FF: handschoen begint
 55: [(15, 19), (25, 32), (39, 42), (48, 51)],
 56: [(14, 20), (25, 32), (39, 42), (48, 51)],          # NF: handschoen begint
 57: [(13, 20), (25, 32), (38, 42), (47, 52)],          # FH: voet
 58: [(13, 20), (25, 32), (38, 42), (47, 52)],
 59: [(13, 20), (26, 31), (37, 44), (48, 51)],          # NH: voet
 60: [(13, 20), (27, 30), (37, 44)],
 61: [(14, 19), (38, 43)],
 62: [(15, 18)],
}
for y, sp in ROWS.items():
    for a, b in sp: S[y, a:b + 1] = True
if __name__ == '__main__':
    open(os.path.join(HERE, 'ronde5b.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in S) + '\n')
    im = np.zeros((64, 64, 4), np.uint8); im[S] = (0, 0, 0, 255)
    Image.fromarray(im, 'RGBA').save(os.path.join(HERE, 'ronde5b_1x.png'))
    ys, xs = np.nonzero(S)
    print('px', S.sum(), 'box', xs.max() - xs.min() + 1, 'x', ys.max() - ys.min() + 1)
    print('bevriezingsdiff y0-30 x<=31 t.o.v. ronde5:', int((S[:31, :32] ^ R5[:31, :32]).sum()), 'px; hele y0-30:', int((S[:31] ^ R5[:31]).sum()), 'px')
