"""Controle poedelmot kleur_r20: alpha-diff met silhouet.png (pixellijst), open randen,
losse pixels en tintclusters < 3 px (4-samenhangend, vlaktinten 3-8; glans uitgezonderd).
Gebruik: python3 controle.py [raster.txt]"""
import sys, os
import numpy as np
from PIL import Image
HIER = os.path.dirname(os.path.abspath(__file__))
SIL = '/home/user/pokemon-fully-ungrounded/docs/concept/sprites/poedelmot/silhouet/silhouet.png'
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
LIJN = set('1234')         # buitenlijn (2/1) en selout (4)
VOET = set()   # klauwtjes en sprietpunt rechts op de rand in 4 (bewust): klauw_rand.txt
try:
    VOET = set(tuple(map(int, l.split(','))) for l in open(os.path.join(os.path.dirname(os.path.abspath(f)), 'klauw_rand.txt')))
except OSError: pass
open_r = [(x, y, r[y][x]) for x, y in P if r[y][x] != '.' and '.' in nb4(x, y) and r[y][x] not in LIJN and (x, y) not in VOET]
print(f'open randen (buitenrand zonder lijnkleur 1-4): {len(open_r)} {open_r}  | bewuste uitzondering klauwtjes: {sorted(VOET)}')
# selout: aaneengesloten reeksen A op de buitenrand (geen afwisseling A/1 binnen een rand)
op = lambda x, y: 0 <= x < 64 and 0 <= y < 64 and r[y][x] != '.'
rand = {(x, y) for x, y in P if op(x, y) and any(not op(x+dx, y+dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
Aset = {p for p in rand if r[p[1]][p[0]] == '4'}; zien = set(); reeksen = []
for p in sorted(Aset):
    if p in zien: continue
    st = [p]; c = []; zien.add(p)
    while st:
        q = st.pop(); c.append(q)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                n = (q[0]+dx, q[1]+dy)
                if n in Aset and n not in zien: zien.add(n); st.append(n)
    reeksen.append(sorted(c))
kort = [c for c in reeksen if len(c) < 3 and not set(c) <= VOET]
print(f'buitenrand {len(rand)} px: selout 4 {len(Aset)} px in {len(reeksen)} reeksen (lengtes {sorted(len(c) for c in reeksen)}), reeksen < 3 px: {kort}')
GLANS = {(27,35),(28,35),(27,36),(18,34),(18,35)}   # oogglans
VLAK = set('56789AD')   # vlaktinten; 1-4 lijn- en detailkleuren, B oogreflectie, C sprietnerf
# sprieten zijn lijnwerk (nerf en baarden 1 px), geen vlaktint
SPRIET = set()
try:
    SPRIET = set(tuple(map(int, l.split(','))) for l in open(os.path.join(os.path.dirname(os.path.abspath(f)), 'spriet_zone.txt')))
except OSError: pass
# krullen op de vleugels zijn lijnwerk (1 px)
try:
    SPRIET |= set(tuple(map(int, l.split(','))) for l in open(os.path.join(os.path.dirname(os.path.abspath(f)), 'krul_lijnen.txt')))
except OSError: pass
losse = [(x, y, r[y][x]) for x, y in P if r[y][x] in VLAK and r[y][x] not in nb4(x, y) and (x, y) not in GLANS and (x, y) not in SPRIET]
print(f'losse pixels (vlaktint zonder gelijke buur): {len(losse)} {losse}')
seen = set(); small = []
for x, y in P:
    c = r[y][x]
    if c not in VLAK or (x, y) in seen or (x, y) in SPRIET: continue
    st = [(x, y)]; comp = []; seen.add((x, y))
    while st:
        p = st.pop(); comp.append(p)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (p[0]+dx, p[1]+dy)
            if 0 <= q[0] < 64 and 0 <= q[1] < 64 and q not in seen and r[q[1]][q[0]] == c: seen.add(q); st.append(q)
    if len(comp) < 3 and not set(comp) <= GLANS: small.append((c, sorted(comp)))
print(f'tintclusters < 3 px: {len(small)}')
for c, comp in small: print('  ', c, comp)
used = sorted(set(c for l in r for c in l) - {'.'})
print('gebruikte indexen:', ''.join(used))
