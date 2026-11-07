"""Controle ronde 8: pixeldiff tegen ronde 6 (0 buiten de achterpootzone, 0 in de voorpoten, 0 bestaande pixels boven rij 51), tintclusters < 3 px,
lichte kleur op de buitenrand en het aantal kleuren. Voorpootzone = rijen 52-59, zonder de achterpoten."""
import os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
R = np.array([list(l.rstrip('\n')) for l in open(os.path.join(HERE, 'raster.txt'))][:64])
R6 = np.array([list(l.rstrip('\n')) for l in open(os.path.join(HERE, '../ronde6/raster.txt'))][:64])
A = R != '.'
# achterpootzone ronde 8: links x7-15 y45-58 (oude P weg, flanklob rond afgewerkt, ronde 8b), onder de buik x23-29 y52-57 (verre achterpoot),
# rechts x36-46 y45-59 (achterlijf onder de vleugel, S, R1)
zone = np.zeros((64, 64), bool); zone[45:59, 7:16] = True; zone[52:58, 23:30] = True; zone[45:60, 36:47] = True
# voorpoten ronde 6: de pixels die ronde 6 aan de voorpoten tekende + rijen 41-51 van de voorpoten (blijven gelijk)
R5 = np.array([list(l.rstrip('\n')) for l in open(os.path.join(HERE, '../ronde5/raster.txt'))][:64])
voor = (R6 != R5) & (R6 != '.')  # alleen pixels die ronde 6 aan de voorpoten tekende
for l in open(os.path.join(HERE, '../ronde6/achterpoten_masker.txt')):
    x, y = map(int, l.split()); voor[y, x] = False
achter = ~voor
D = R != R6
print('pixeldiff tegen ronde 6: %d px; buiten de achterpootzone: %d; in de voorpoten van ronde 6: %d' % (D.sum(), (D & ~zone).sum(), (D & voor).sum()))
boven = D.copy(); boven[51:] = False; boven[45:51, 7:16] = False
print('boven rij 51 gewijzigd (buiten de linkerlob): %d px, waarvan bestaande (niet-transparante) pixels van ronde 6: %d' % (boven.sum(), (boven & (R6 != '.')).sum()))
print('gewijzigd in de voorpootzone van ronde 6 (rijen 52-59, x15-36):', int((D[52:60, 15:37] & ~zone[52:60, 15:37]).sum()))
oog = np.zeros((64, 64), bool); oog[25:30, 18:27] = True
klein = []
for c in sorted(set(R.ravel()) - {'.'}):
    M = R == c; seen = np.zeros_like(M)
    for y, x in zip(*np.nonzero(M)):
        if seen[y, x]: continue
        st = [(y, x)]; seen[y, x] = True; comp = []
        while st:
            a, b = st.pop(); comp.append((a, b))
            for da in (-1, 0, 1):
                for db in (-1, 0, 1):
                    q, r = a + da, b + db
                    if 0 <= q < 64 and 0 <= r < 64 and M[q, r] and not seen[q, r]: seen[q, r] = True; st.append((q, r))
        if len(comp) < 3 and not all(oog[p] for p in comp): klein.append((str(c), [(int(b), int(a)) for a, b in comp]))
print('clusters < 3 px buiten de ogen (tint, [(x,y)]):', len(klein))
for k in klein: print('  ', k)
rand = [(x, y, str(R[y, x])) for y in range(64) for x in range(64) if A[y, x] and any(
    not (0 <= y + dy < 64 and 0 <= x + dx < 64) or not A[y + dy, x + dx] for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)))
    and R[y, x] not in '12b']
print('buitenrand niet in omlijningskleur (1, 2, b):', len(rand), rand[:30])
print('kleuren:', len(set(R.ravel()) - {'.'}), '+ transparant')
# diff.png: ronde 6 grijs, gewijzigde pixels rood (16x); bewijs dat voorpoten en alles boven de onderrand gelijk zijn
from PIL import Image
img = np.full((64, 64, 3), 255, np.uint8); img[R6 != '.'] = (190, 190, 190); img[voor] = (120, 160, 220); img[D] = (220, 40, 40)
Image.fromarray(img).resize((1024, 1024), Image.NEAREST).save(os.path.join(HERE, 'diff.png'))
print('diff.png: grijs = ronde 6, blauw = voorpoten ronde 6 (ongewijzigd), rood = gewijzigd')
