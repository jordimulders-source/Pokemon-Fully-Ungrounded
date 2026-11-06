"""Controle ronde 1: alpha tegen silhouet ronde 3 (alleen de verre voorvleugel mag erbij komen), tintclusters < 3 px
(behalve de ogen, overgenomen van Emolga), open randen (lichte kleur op de buitenrand) en het aantal kleuren."""
import os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
R = np.array([list(l.rstrip('\n')) for l in open(os.path.join(HERE, 'raster.txt'))][:64])
S = np.array([[c == '#' for c in l.rstrip('\n')] for l in open(os.path.join(HERE, '../../silhouet/ronde3/ronde3.txt'))][:64])
A = R != '.'
# verre voorvleugel: x <= 14, y 16..27, links van/onder het verre oor
zone = np.zeros((64, 64), bool); zone[16:28, 0:15] = True; zone[43:64, :] = True   # draft: poten opnieuw (Giratina)
bij, weg = A & ~S, S & ~A
print('alpha: +%d px (buiten zone %d), -%d px' % (bij.sum(), (bij & ~zone).sum(), weg.sum()))
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
        if len(comp) < 3 and not all(oog[p] for p in comp): klein.append((c, [(b, a) for a, b in comp]))
print('clusters < 3 px buiten de ogen (tint, [(x,y)]):', len(klein))
for k in klein: print('  ', k)
rand = [(x, y, R[y, x]) for y in range(64) for x in range(64) if A[y, x] and any(
    not (0 <= y + dy < 64 and 0 <= x + dx < 64) or not A[y + dy, x + dx] for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)))
    and R[y, x] not in '12b']
print('buitenrand niet in omlijningskleur (1, 2, b):', len(rand), rand[:30])
print('kleuren:', len(set(R.ravel()) - {'.'}), '+ transparant')
