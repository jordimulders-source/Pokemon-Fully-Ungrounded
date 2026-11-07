"""Controle potoo: alpha-diff met silhouet.png, open randen, selout-reeksen, losse pixels,
tintclusters < 3 px (vlaktinten 5-8, A-C; glans uitgezonderd), aantal kleuren. Gebruik: python3 controle.py [raster.txt]"""
import sys, os
import numpy as np
from PIL import Image
HIER = os.path.dirname(os.path.abspath(__file__))
SIL = '/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/potoo/silhouet/silhouet.png'
f = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HIER, 'raster.txt')
r = [l.rstrip('\n') for l in open(f)][:64]
assert len(r) == 64 and all(len(l) == 64 for l in r), 'raster moet 64x64 zijn'
P = [(x, y) for y in range(64) for x in range(64)]
a = np.array(Image.open(SIL).convert('RGBA'))[:, :, 3] > 0
extra = [(x, y) for x, y in P if r[y][x] != '.' and not a[y, x]]
mist = [(x, y) for x, y in P if r[y][x] == '.' and a[y, x]]
print(f'pixels: {sum(c != "." for l in r for c in l)} (silhouet {int(a.sum())})')
print(f'alpha-diff met silhouet: {len(extra) + len(mist)}  extra={extra}  mist={mist}')
nb4 = lambda x, y: [(r[y+dy][x+dx] if 0 <= y+dy < 64 and 0 <= x+dx < 64 else '.') for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
LIJN = set('12349')   # buitenlijn 1/2, selout 3/4 (grijs) en 9 (donkerblauw, muil)
open_r = [(x, y, r[y][x]) for x, y in P if r[y][x] != '.' and '.' in nb4(x, y) and r[y][x] not in LIJN]
print(f'open randen (buitenrand zonder lijnkleur 1-4/9): {len(open_r)} {open_r}')
GLANS = {(33, 6), (34, 6), (33, 7), (34, 7)}
LIJNEN = set()
try:
    LIJNEN = {tuple(map(int, l.split(','))) for l in open(os.path.join(os.path.dirname(os.path.abspath(f)), 'lijnen.txt')) if l[0].isdigit()}
except OSError: pass
VLAK = set('5678ABC')
losse = [(x, y, r[y][x]) for x, y in P if r[y][x] in VLAK and r[y][x] not in nb4(x, y) and (x, y) not in GLANS and (x, y) not in LIJNEN]
print(f'losse pixels (vlaktint zonder gelijke buur): {len(losse)} {losse}')
seen = set(); small = []
for x, y in P:
    c = r[y][x]
    if c not in VLAK or (x, y) in seen or (x, y) in LIJNEN: continue
    st = [(x, y)]; comp = []; seen.add((x, y))
    while st:
        p = st.pop(); comp.append(p)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (p[0]+dx, p[1]+dy)
            if 0 <= q[0] < 64 and 0 <= q[1] < 64 and q not in seen and q not in LIJNEN and r[q[1]][q[0]] == c: seen.add(q); st.append(q)
    if len(comp) < 3 and not set(comp) <= GLANS: small.append((c, sorted(comp)))
print(f'tintclusters < 3 px: {len(small)}')
for c, comp in small: print('  ', c, comp)
used = sorted(set(c for l in r for c in l) - {'.'})
print('gebruikte indexen:', ''.join(used), f'({len(used)} kleuren + transparant)')
