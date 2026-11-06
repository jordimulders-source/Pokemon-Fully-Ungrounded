"""Controle ronde 7: pixeldiff tegen ronde 6 (0 buiten de achterpoten, 0 in de voorpoten), tintclusters < 3 px,
lichte kleur op de buitenrand en het aantal kleuren. Voorpootzone = rijen 52-59, zonder de achterpoten."""
import os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
R = np.array([list(l.rstrip('\n')) for l in open(os.path.join(HERE, 'raster.txt'))][:64])
R6 = np.array([list(l.rstrip('\n')) for l in open(os.path.join(HERE, '../ronde6/raster.txt'))][:64])
A = R != '.'
# achterpootzone ronde 7: links x7-14 y51-58 (P), onder de buik x23-25 y52-57 (Q), rechts x37-45 y48-59 (heup, S, R1)
zone = np.zeros((64, 64), bool); zone[51:59, 7:15] = True; zone[52:58, 23:26] = True; zone[48:60, 37:46] = True
# voorpoten ronde 6: de pixels die ronde 6 aan de voorpoten tekende + rijen 41-51 van de voorpoten (blijven gelijk)
R5 = np.array([list(l.rstrip('\n')) for l in open(os.path.join(HERE, '../ronde5/raster.txt'))][:64])
voor = (R6 != R5) & (R6 != '.')  # alleen pixels die ronde 6 aan de voorpoten tekende
for l in open(os.path.join(HERE, '../ronde6/achterpoten_masker.txt')):
    x, y = map(int, l.split()); voor[y, x] = False
achter = ~voor
D = R != R6
print('pixeldiff tegen ronde 6: %d px; buiten de achterpootzone: %d; in de voorpoten van ronde 6: %d' % (D.sum(), (D & ~zone).sum(), (D & voor).sum()))
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
