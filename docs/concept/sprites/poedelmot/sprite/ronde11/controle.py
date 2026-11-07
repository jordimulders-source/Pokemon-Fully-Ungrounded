"""Controle ronde 11: pootpixels buiten Jordi's vormen (masker.py), zichtbare achterpoten per kant, breedte per poot,
voorpoten gelijk aan ronde 6, diff tegen ronde 10, buitenrand, gaten, kleuren; diff.png."""
import os
import numpy as np
from PIL import Image
from masker import maskers
HERE = os.path.dirname(os.path.abspath(__file__))
rd = lambda p: np.array([list(l.rstrip('\n')) for l in open(os.path.join(HERE, p))][:64])
R, R10, R6, R5 = rd('raster.txt'), rd('../ronde10/raster.txt'), rd('../ronde6/raster.txt'), rd('../ronde5/raster.txt')
voor = (R6 != R5) & (R6 != '.')
for l in open(os.path.join(HERE, '../ronde6/achterpoten_masker.txt')):
    x, y = map(int, l.split()); voor[y, x] = False
A = R != '.'; M = maskers()
P = {}
for l in open(os.path.join(HERE, 'poten.txt')):
    n, x, y = l.split(); P.setdefault(n, []).append((int(x), int(y)))
vorm = {'M1': 'midden', 'A1': 'midden', 'S': 'rechts', 'A2': 'rechts'}
for n, cs in P.items():
    buiten = [c for c in cs if not M[vorm[n]][c[1], c[0]]]
    rij = {}
    for x, y in cs:
        if R[y, x] != 'b': rij.setdefault(y, []).append(x)
    br = max(max(v) - min(v) + 1 for v in rij.values())
    print('%-2s (%s): %d px, buiten de vorm: %d %s; breedte max %d px (incl. omlijning), rijen y%d-%d, klauwtjes %d' % (
        n, vorm[n], len(cs), len(buiten), buiten, br, min(rij), max(rij), sum(R[y, x] == 'b' for x, y in cs)))
print('zichtbare achterpoten: links/midden (verre kant) 2 (M1 + stukje A1), rechts (nabije kant) 2 (S + stukje A2)')
rz = np.zeros((64, 64), bool); rz[45:59, 36:64] = True; rz[44, 39:44] = True
mz = np.zeros((64, 64), bool); mz[52:59, 22:30] = True
lijfrand = np.zeros((64, 64), bool); lijfrand[52, 23:25] = True
pr = A & rz & ~voor & ~M['rechts']; pm = A & mz & ~voor & ~M['midden'] & ~lijfrand
print('alle pootzonepixels buiten de vormen: rechts %d, midden %d (buikrand ronde 6 op (23-24,52) apart)' % (pr.sum(), pm.sum()))
print('links: pixels x<16 op y41-52: %d' % sum(A[y, x] for y in range(41, 53) for x in range(16)))
print('voorpoten (rijen 52-59, pixels ronde 6) gewijzigd: %d' % ((R != R6) & voor).sum())
arm = [(x, y, str(R10[y, x]), str(R[y, x])) for y in range(41, 52) for x in range(30, 42) if R[y, x] != R10[y, x]]
print('aansluiting rechts, gewijzigde pixels boven rij 52 (x, y, was, nu):', arm)
D = R != R10
print('pixeldiff tegen ronde 10: %d px' % D.sum())
rand = [(x, y, str(R[y, x])) for y in range(64) for x in range(64) if A[y, x] and any(
    not (0 <= y + dy < 64 and 0 <= x + dx < 64) or not A[y + dy, x + dx] for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)))
    and R[y, x] not in '12b']
print('buitenrand niet in omlijningskleur:', len(rand), rand)
gat = [(x, y) for y in range(1, 63) for x in range(1, 63) if not A[y, x] and all(A[y + dy, x + dx] for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)))]
print('ingesloten transparante pixels:', gat)
print('kleuren:', len(set(R.ravel()) - {'.'}), '+ transparant')
img = np.full((64, 64, 3), 255, np.uint8); img[R10 != '.'] = (190, 190, 190); img[voor] = (120, 160, 220); img[D] = (220, 40, 40)
Image.fromarray(img).resize((1024, 1024), Image.NEAREST).save(os.path.join(HERE, 'diff.png'))
print('diff.png: grijs = ronde 10, blauw = voorpoten (ongewijzigd), rood = gewijzigd t.o.v. ronde 10')
