"""Controle ronde 10: pootpixels buiten Jordi's vormen (masker.py: convex dichtgetrokken + 1 px speling), voorpoten
gelijk aan ronde 6, diff tegen ronde 9, linkerrand, buitenrand, gaten, kleuren; diff.png en overlay op het vel."""
import os
import numpy as np
from PIL import Image
from masker import maskers
HERE = os.path.dirname(os.path.abspath(__file__))
rd = lambda p: np.array([list(l.rstrip('\n')) for l in open(os.path.join(HERE, p))][:64])
R, R9, R6, R5 = rd('raster.txt'), rd('../ronde9/raster.txt'), rd('../ronde6/raster.txt'), rd('../ronde5/raster.txt')
voor = (R6 != R5) & (R6 != '.')
for l in open(os.path.join(HERE, '../ronde6/achterpoten_masker.txt')):
    x, y = map(int, l.split()); voor[y, x] = False
A = R != '.'; M = maskers()
# pootzones: rechts = x>=36, y45-58 plus de nieuwe bovenrand van S op y44 (x39-43); midden = tussen de voorpoten x22-29, y52-58
rz = np.zeros((64, 64), bool); rz[45:59, 36:64] = True; rz[44, 39:44] = True
mz = np.zeros((64, 64), bool); mz[52:59, 22:30] = True
lijfrand = np.zeros((64, 64), bool); lijfrand[52, 23:25] = True  # onderrand van de buik uit ronde 6 (blijft)
pr = A & rz & ~voor & ~M['rechts']; pm = A & mz & ~voor & ~M['midden'] & ~lijfrand
print('rechts: pootpixels buiten de lange lus: %d %s' % (pr.sum(), [(int(x), int(y)) for y, x in zip(*np.nonzero(pr))]))
print('midden: pootpixels buiten de U-vormen: %d %s' % (pm.sum(), [(int(x), int(y)) for y, x in zip(*np.nonzero(pm))]))
print('midden: onderrand van de buik uit ronde 6 net naast de U (niet meegeteld): %s' % [(int(x), int(y)) for y, x in zip(*np.nonzero(A & lijfrand & ~M['midden']))])
links = [(int(x), int(y)) for y in range(41, 53) for x in range(0, 16) if A[y, x]]
print('links: pixels voorbij de lijn borst (x17, y39-40) -> linkervoorpoot (x16, y52), dus x<16 op y41-52: %d %s' % (len(links), links))
print('links: rode kruis-cellen op het lijf: %d' % (M['links'] & A).sum())
print('voorpoten gewijzigd t.o.v. ronde 6: %d' % ((R != R6) & voor).sum())
D = R != R9
print('pixeldiff tegen ronde 9: %d px' % D.sum())
rand = [(x, y, str(R[y, x])) for y in range(64) for x in range(64) if A[y, x] and any(
    not (0 <= y + dy < 64 and 0 <= x + dx < 64) or not A[y + dy, x + dx] for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)))
    and R[y, x] not in '12b']
print('buitenrand niet in omlijningskleur:', len(rand), rand)
gat = [(x, y) for y in range(1, 63) for x in range(1, 63) if not A[y, x] and all(A[y + dy, x + dx] for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)))]
print('ingesloten transparante pixels:', gat)
print('kleuren:', len(set(R.ravel()) - {'.'}), '+ transparant')
img = np.full((64, 64, 3), 255, np.uint8); img[R9 != '.'] = (190, 190, 190); img[voor] = (120, 160, 220); img[D] = (220, 40, 40)
Image.fromarray(img).resize((1024, 1024), Image.NEAREST).save(os.path.join(HERE, 'diff.png'))
print('diff.png: grijs = ronde 9, blauw = voorpoten (ongewijzigd), rood = gewijzigd t.o.v. ronde 9')
