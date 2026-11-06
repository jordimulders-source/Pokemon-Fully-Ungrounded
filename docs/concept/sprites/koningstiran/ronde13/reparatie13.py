"""Ronde 13: top 5 uit EINDKEURING.md op ronde12/sapa_inca.png (palet van ronde 10/12 ongewijzigd).
Schrijft het blok 'ronde 13' onderaan sapa_inca.txt en een diff per punt (met RGB voor/na). Draaien vanuit de repo-root."""
import os, sys
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import bouw
src = os.path.join(H, 'sapa_inca.txt')
_t = open(src).read().split('# ==== ronde 13')[0].rstrip('\n') + '\n'
open(src, 'w').write(_t)
pal, letters, g0 = bouw.bouw(src)
inv = {v: c for c, v in letters.items()}; rgb = {c: v for c, v in pal}
L = np.vectorize(lambda v: '.' if v == 0 else inv[v])(g0).astype('<U1'); L0 = L.copy()
punt = {}
def zet(p, x, y, c):
    if L[y, x] != c:
        punt.setdefault(p, []).append((x, y, L[y, x], c)); L[y, x] = c
# 1. ogen en snavel (binnen de huidige kopmaat)
P = '1 ogen en snavel'
zet(P, 29, 24, 'w'); zet(P, 30, 24, 'K'); zet(P, 31, 24, 'y'); zet(P, 30, 25, 'a')   # nabije oog: glans lichtkant, pupil, iris, reflectie
zet(P, 24, 23, 'd')                                                              # verre oog: lid
zet(P, 23, 26, 'd'); zet(P, 24, 26, 'b')                                         # snavel: donkere haakpunt
# 2. banding rechterflank: de 2 px lijfbasis na de buikschaduw loopt uit naar 1 px en verdwijnt
P = '2 banding flank'
for y in range(36, 51):
    xs = [x for x in range(26, 36) if L0[y, x] == 'a' and L0[y, x + 1] == 'm']
    if not xs:
        continue
    x = xs[-1] + 1
    run = [xx for xx in range(x, x + 3) if L0[y, xx] == 'm']
    keep = 1 if y <= 44 else 0
    for xx in run[keep:]:
        zet(P, xx, y, 'd')
# 3. klein hooglicht op de romp linksboven (alleen m -> l)
P = '3 hooglicht romp'
for x, y in ((24, 29), (25, 29), (23, 30), (24, 30), (25, 30), (22, 31), (23, 31), (24, 31), (22, 32), (23, 32)):
    if L[y, x] == 'm':
        zet(P, x, y, 'l')
# 4. stafpunt zichtbaar: omlijning links in omlijningsbruin, rechts zwart, punt licht/donker goud
P = '4 stafpunt'
for y in (18, 19, 20, 21):
    zet(P, 13, y, 'd'); zet(P, 14, y, 'y' if y < 21 else 'a'); zet(P, 15, y, 'a')
zet(P, 16, 18, 'K'); zet(P, 16, 19, 'K')
zet(P, 17, 19, 'o')
# 5. opschonen
P = '5 opschonen'
zet(P, 15, 46, 'd'); zet(P, 15, 47, 'K')                                       # klont onder de hand: geen 2x2 zwart meer
for x in (40, 41, 42, 45):
    zet(P, x, 22, 'K')                                                         # kroononderrand in een lijn, los rood weg
for x, y in ((40, 23), (41, 23), (42, 23), (42, 24)):
    zet(P, x, y, '.')                                                          # drup onder de kroon weg
for x, y in ((14, 43), (15, 44), (16, 45)):
    zet(P, x, y, 'm')                                                          # hand: een doorlopende penscheiding over
with open(src, 'a') as f:
    f.write('# ==== ronde 13: top 5 uit EINDKEURING.md (gegenereerd door reparatie13.py) ====\n')
    for y in range(64):
        for x in range(64):
            if L[y, x] != L0[y, x]:
                f.write(f'{y} {x} {"_" if L[y, x] == "." else L[y, x]}\n')
c = lambda k: 'transparant' if k == '.' else str(rgb[k])
with open(os.path.join(H, 'diff_per_punt.txt'), 'w') as f:
    for p in sorted(punt):
        f.write(f'{p}: {len(punt[p])} px\n')
        for x, y, a, b in punt[p]:
            f.write(f'  ({x},{y}) {c(a)} -> {c(b)}\n')
    f.write(f'totaal {int((L != L0).sum())} px; silhouet erbij {int(((L != ".") & (L0 == ".")).sum())}, eraf {int(((L == ".") & (L0 != ".")).sum())}\n')
for p in sorted(punt): print(p, len(punt[p]))
print('totaal', int((L != L0).sum()))
