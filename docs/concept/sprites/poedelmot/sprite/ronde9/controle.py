"""Controle ronde 9: pixeldiff tegen ronde 8 en tegen ronde 6 (voorpoten moeten gelijk zijn aan ronde 6), rood van Jordi's
schets per zone, tintclusters < 3 px, lichte kleur op de buitenrand, kleuren; diff.png (rood = gewijzigd t.o.v. ronde 8)."""
import os
import numpy as np
from PIL import Image
from overlay import cellen
HERE = os.path.dirname(os.path.abspath(__file__))
rd = lambda p: np.array([list(l.rstrip('\n')) for l in open(os.path.join(HERE, p))][:64])
R, R8, R6, R5 = rd('raster.txt'), rd('../ronde8/raster.txt'), rd('../ronde6/raster.txt'), rd('../ronde5/raster.txt')
voor = (R6 != R5) & (R6 != '.')
for l in open(os.path.join(HERE, '../ronde6/achterpoten_masker.txt')):
    x, y = map(int, l.split()); voor[y, x] = False
D = R != R8
zone = np.zeros((64, 64), bool); zone[45:53, 10:16] = True; zone[52:59, 22:30] = True; zone[41:58, 35:45] = True
print('pixeldiff tegen ronde 8: %d px; buiten de zones (links x10-15 y45-52, midden x22-29 y52-58, rechts x35-44 y41-57): %d' % (D.sum(), (D & ~zone).sum()))
print('voorpoten (pixels die ronde 6 aan de voorpoten tekende) gewijzigd t.o.v. ronde 6: %d' % ((R != R6) & voor).sum())
M = cellen() > 3
A = R != '.'
print('rode schetscellen: %d; links (x<16) op het lijf van ronde 9: %d (moet 0: geen uitstulpsel onder het kruis)' % (M.sum(), (M[:, :16] & A[:, :16]).sum()))
print('rode cellen over de voorpoten (blijven gelijk): %s' % sorted((int(x), int(y)) for y, x in zip(*np.nonzero(M & voor))))
klein = []
for c in sorted(set(R.ravel()) - {'.'}):
    Mc = R == c; seen = np.zeros_like(Mc)
    for y, x in zip(*np.nonzero(Mc)):
        if seen[y, x]: continue
        st = [(y, x)]; seen[y, x] = True; comp = []
        while st:
            a, b = st.pop(); comp.append((a, b))
            for da in (-1, 0, 1):
                for db in (-1, 0, 1):
                    q, r = a + da, b + db
                    if 0 <= q < 64 and 0 <= r < 64 and Mc[q, r] and not seen[q, r]: seen[q, r] = True; st.append((q, r))
        if len(comp) < 3 and any(zone[p] for p in comp): klein.append((str(c), [(int(b), int(a)) for a, b in comp]))
print('clusters < 3 px in de zones:', klein)
rand = [(x, y, str(R[y, x])) for y in range(64) for x in range(64) if A[y, x] and any(
    not (0 <= y + dy < 64 and 0 <= x + dx < 64) or not A[y + dy, x + dx] for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)))
    and R[y, x] not in '12b']
print('buitenrand niet in omlijningskleur:', len(rand), rand)
gat = [(x, y) for y in range(1, 63) for x in range(1, 63) if not A[y, x] and all(A[y + dy, x + dx] for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)))]
print('ingesloten transparante pixels:', gat)
print('kleuren:', len(set(R.ravel()) - {'.'}), '+ transparant')
img = np.full((64, 64, 3), 255, np.uint8); img[R8 != '.'] = (190, 190, 190); img[voor] = (120, 160, 220); img[D] = (220, 40, 40)
Image.fromarray(img).resize((1024, 1024), Image.NEAREST).save(os.path.join(HERE, 'diff.png'))
print('diff.png: grijs = ronde 8, blauw = voorpoten (ongewijzigd), rood = gewijzigd t.o.v. ronde 8')
