"""Ronde 10: technische reparaties uit KEURING.md op kandidaat/sapa_inca.png. Schrijft de pixelregels per keuringspunt
onderaan sapa_inca.txt (blok 'ronde 10') en een overzicht per punt. Draaien vanuit de repo-root.
Regel open randen (strenge definitie): alleen K, d en p mogen naast transparant; een open pixel wordt d als het transparant
links/boven heeft (lichtkant) en K als het alleen rechts/onder transparant heeft (schaduwkant)."""
import os, sys
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import bouw
src = os.path.join(H, 'sapa_inca.txt')
base = open(src).read().split('# ==== ronde 10')[0].rstrip('\n') + '\n'
open(src, 'w').write(base)
pal, letters, g0 = bouw.bouw(src)
inv = {v: c for c, v in letters.items()}
L = np.vectorize(lambda v: '.' if v == 0 else inv[v])(g0).astype('<U1')
L0 = L.copy()
punt = {}
def zet(p, x, y, c):
    if L[y, x] != c:
        L[y, x] = c; punt.setdefault(p, set()).add((x, y))
# punt 1: zwart aan de lichtkant van de stafkop tegen de kroon -> donkere tint van die groep
for x, y in ((14, 20), (14, 21), (13, 22), (13, 23)):
    zet('1 stafkop lichtkant', x, y, 'a')
for x, y in ((12, 24), (12, 25)):
    zet('1 stafkop lichtkant', x, y, 'r')      # rand van het kroonkwastje: donkerrood i.p.v. zwart
# punt 2: lichte streep aan de schaduwkant rechts van de buik -> donkerder; staf links belicht
for y in range(34, 53):
    for x in range(27, 35):
        if L[y, x] == 'l':
            zet('2 buik schaduwkant', x, y, 'm')
for y in (29, 30, 31, 32):                     # 5 breed: omlijning d | licht y | g | vaan t | omlijning K
    for x, c in zip(range(13, 18), 'dygtK'):
        zet('2 staf licht links', x, y, c)
for y in (33, 34, 35):                         # 4 breed
    for x, c in zip(range(14, 18), 'dytK'):
        zet('2 staf licht links', x, y, c)
for y in range(36, 42):                        # 3 breed, deels voor de vleugel
    for x, c in zip(range(14, 17), 'dyt'):
        zet('2 staf licht links', x, y, c)
# punt 4: losse paarse puntjes van het rechter kroonkwastje weg
for x, y in ((43, 23), (44, 23), (43, 24), (46, 31), (47, 31), (46, 32), (47, 32)):
    zet('4 paarse puntjes', x, y, '.')
zet('4 paarse puntjes', 42, 23, 'K')
# punt 5: ruis in de hand (rechte penscheidingen in d) en losse stippen in de borst
hand = {43: (12, 'KmdmmdmM'), 44: (13, 'KmdmmdmM'), 45: (13, 'KmmdmmdM')}
for y, (x0, s) in hand.items():
    for i, c in enumerate(s):
        zet('5 hand', x0 + i, y, 'm' if c == 'M' else c)
for x, y in ((25, 30), (27, 31), (24, 32), (24, 34)):
    zet('5 borst', x, y, 'm')
zet('5 borst', 28, 34, 'm')
# punt 9: rechte stukken afronden (max +-1 px silhouet per plek)
zet('9 kop links', 22, 23, '.'); zet('9 kop links', 21, 25, 'd'); zet('9 kop links', 21, 26, 'd')
zet('9 kop links', 22, 25, 'R'); zet('9 kop links', 22, 26, 'r')
zet('9 flank rechts', 38, 36, '.')
zet('9 vleugelwortel', 40, 33, '.')
# punt 3 (en 1: lijf links + vleugelwortel omlijnen): alle open randen volgens de strenge definitie
def open_px():
    res = []
    for y in range(64):
        for x in range(64):
            c = L[y, x]
            if c == '.' or c in 'Kdp':
                continue
            lit = any(not (0 <= X < 64 and 0 <= Y < 64) or L[Y, X] == '.' for X, Y in ((x - 1, y), (x, y - 1)))
            sh = any(not (0 <= X < 64 and 0 <= Y < 64) or L[Y, X] == '.' for X, Y in ((x + 1, y), (x, y + 1)))
            if lit or sh:
                res.append((x, y, 'd' if lit and not sh else ('K' if sh and not lit else ('d' if L[y, x] in 'lmoRvgy' else 'K'))))
    return res
for x, y, c in open_px():
    zet('3 open randen', x, y, c)
with open(src, 'a') as f:
    f.write('# ==== ronde 10: technische reparaties uit KEURING.md (gegenereerd door reparatie10.py) ====\n')
    for y in range(64):
        for x in range(64):
            if L[y, x] != L0[y, x]:
                f.write(f'{y} {x} {"_" if L[y, x] == "." else L[y, x]}\n')
for p in sorted(punt):
    print(f'{p}: {len(punt[p])} px')
print('totaal gewijzigd:', int((L != L0).sum()), 'px; silhouet erbij', int(((L != '.') & (L0 == '.')).sum()), 'eraf', int(((L == '.') & (L0 != '.')).sum()))
print('open randen na reparatie:', len(open_px()))
