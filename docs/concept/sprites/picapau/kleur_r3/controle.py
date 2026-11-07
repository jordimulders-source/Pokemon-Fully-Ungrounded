"""Controle Picapau kleur r2. Gebruik: python3 controle.py A  (versie A, zones +-1 px)  |  python3 controle.py B  (variant B: elke silhouetwijziging gemeld, budget 30 px).
1. alpha-diff met het bevroren silhouet (silhouet_b1_1x.png): buiten de vrije zones moet het 0 zijn;
   in de zones (snavelpunt, kuiftoppen, achterkuif-puntjes, tenen) mag +-1 px, elke afwijking wordt gemeld.
2. open randen: elke pixel naast transparant (4-buren) moet een omlijningskleur zijn.
3. losse pixels (geen enkele 8-buur).
4. clusters < 3 px per tint (8-samenhangend), glans uitgezonderd.
5. tellingen: pixels, kleuren, bbox."""
import os, sys
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from bouw import PAL, lees
NAAM = {i: c for i, (c, _) in enumerate(PAL)}
V = sys.argv[1] if len(sys.argv) > 1 else 'A'
rows = lees(os.path.join(D, f'raster_{V}.txt'))
print('versie', V)
sil = Image.open(os.path.join(D, '..', 'silhouet', 'silhouet_b1_1x.png')).convert('RGBA')
S = [[sil.getpixel((x, y))[3] > 0 for x in range(64)] for y in range(64)]
A = [[rows[y][x] != '.' for x in range(64)] for y in range(64)]
# vrije zones (x0, y0, x1, y1) inclusief
ZONES = {
    'snavelpunt': (14, 16, 17, 19),
    'kuiftoppen': (31, 2, 39, 6),
    'achterkuif': (37, 11, 41, 19),
    'tenen': (25, 45, 36, 49),
}
def zone(x, y):
    for n, (x0, y0, x1, y1) in ZONES.items():
        if x0 <= x <= x1 and y0 <= y <= y1:
            return n
    return None
fout = 0
print('1. silhouet-diff')
buiten = [(x, y) for y in range(64) for x in range(64) if A[y][x] != S[y][x] and not zone(x, y)]
binnen = [(x, y, zone(x, y), '+' if A[y][x] else '-') for y in range(64) for x in range(64) if A[y][x] != S[y][x] and zone(x, y)]
print('   buiten de zones:', len(buiten), buiten)
print('   in de zones (gemeld):', len(binnen), binnen)
if V == 'A':
    fout += len(buiten)
else:
    alle = [(x, y, '+' if A[y][x] else '-') for y in range(64) for x in range(64) if A[y][x] != S[y][x]]
    print('   B: alle silhouetwijzigingen:', len(alle), '(budget 30)', alle)
    fout += max(0, len(alle) - 30)
RAND_OK = set('k4dGg')  # g = donkere hoorn (snavelbovenrand)  # omlijning: zwart, goudbruine selout, donkerbruin, kuiftop-zwart, poot-schaduw
print('2. open randen (niet-omlijningskleur naast transparant)')
open_r = []
for y in range(64):
    for x in range(64):
        if not A[y][x]:
            continue
        n4 = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        if any(not (0 <= a < 64 and 0 <= b < 64) or not A[b][a] for a, b in n4) and rows[y][x] not in RAND_OK:
            open_r.append((x, y, rows[y][x]))
print('  ', len(open_r), open_r)
print('3. losse pixels')
los = [(x, y) for y in range(64) for x in range(64) if A[y][x] and not any(
    0 <= x+dx < 64 and 0 <= y+dy < 64 and A[y+dy][x+dx] for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy)]
print('  ', len(los), los); fout += len(los)
print('4. clusters < 3 px per tint (8-samenhangend; glans w en het overgenomen Pikachu-oog uitgezonderd)')
seen = set(); klein = []
for y in range(64):
    for x in range(64):
        c = rows[y][x]
        if c == '.' or (x, y) in seen:
            continue
        st = [(x, y)]; seen.add((x, y)); cl = []
        while st:
            a, b = st.pop(); cl.append((a, b))
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    p = (a+dx, b+dy)
                    if 0 <= p[0] < 64 and 0 <= p[1] < 64 and p not in seen and rows[p[1]][p[0]] == c:
                        seen.add(p); st.append(p)
        if len(cl) < 3 and c != 'w' and not all(25 <= a <= 28 and 18 <= b <= 21 for a, b in cl):  # oog = overgenomen van Pikachu
            klein.append((c, cl))
for c, cl in klein:
    print('   ', c, cl)
print('   aantal:', len(klein))
px = sum(A[y][x] for y in range(64) for x in range(64))
xs = [x for y in range(64) for x in range(64) if A[y][x]]; ys = [y for y in range(64) for x in range(64) if A[y][x]]
kl = sorted(set(ch for r in rows for ch in r) - {'.'})
print('5. pixels', px, '| kleuren', len(kl), ''.join(kl), '| bbox', min(xs), min(ys), max(xs), max(ys), f'({max(xs)-min(xs)+1}x{max(ys)-min(ys)+1})')
print('UITSLAG:', 'OK' if fout == 0 and not open_r else f'{fout} harde fouten, {len(open_r)} randpunten')
