"""Eerste overtrek (automatisch, cel voor cel uit de C3-render): massa = alpha van C3_1x, onderdeel uit bron_labels.txt,
tint uit de toon van de witte render (toonkaart). Daarna omlijning: zwart aan de
schaduwkant (rechts/onder), selout (donkere tint) aan de lichtkant (links/boven); binnenlijnen waar een voorliggend
onderdeel over een achterliggend valt. Uitvoer: raster_start.txt (wordt daarna met de hand bewerkt -> raster.txt)."""
import numpy as np
from PIL import Image
from palet import RGB
kl = np.asarray(Image.open('bron/bron_kleur_1x.png').convert('RGBA')).astype(float)
LB = [l.rstrip('\n') for l in open('bron/bron_labels.txt') if not l.startswith('#')]
TOON = [l.rstrip('\n') for l in open('bron/bron_toon.txt') if not l.startswith('#')]
GROEP = dict(L='123', K='123', B='abe', W='c', U='23', I='b', N='abe', V='3v4', F='v4', S='ab', T='v4', Z='yY1', O='k', P='gG')
SELOUT = dict(L='4', K='4', B='e', W='4', U='4', I='4', N='e', V='4', F='4', S='4', T='4', Z='1', O='k', P='G')
VOOR = 'ONWKIUBLPVSZTF'   # volgorde van voor naar achter (voor = lager rangnummer)
R = [['.'] * 64 for _ in range(64)]; part = [['.'] * 64 for _ in range(64)]
for y in range(64):
    for x in range(64):
        if kl[y, x, 3] < 128: continue
        p = LB[y][x]
        if p == '.':   # alpha zonder label: neem buur-label
            nb = [LB[y+j][x+i] for i in (-1, 0, 1) for j in (-1, 0, 1) if 0 <= x+i < 64 and 0 <= y+j < 64 and LB[y+j][x+i] != '.']
            p = max(set(nb), key=nb.count) if nb else 'L'
        part[y][x] = p
        g = GROEP[p]; t = int(TOON[y][x]) if TOON[y][x] != '.' else 1
        # tint uit de toon van de witte render (licht linksboven): 3 licht, 2-1 basis, 0 schaduw
        if len(g) == 3: R[y][x] = g[{3: 0, 2: 1, 1: 1, 0: 2}[t]]
        elif len(g) == 2: R[y][x] = g[0 if t >= 2 else 1]
        else: R[y][x] = g[0]
def nb4(x, y): return [(x+dx, y+dy) for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)) if 0 <= x+dx < 64 and 0 <= y+dy < 64]
leeg = lambda x, y: part[y][x] == '.'
O = [r[:] for r in R]
for y in range(64):
    for x in range(64):
        p = part[y][x]
        if p == '.': continue
        buiten = [(a, b) for a, b in nb4(x, y) if leeg(a, b)]
        if buiten:
            licht = any(a < x or b < y for a, b in buiten) and not any(a > x or b > y for a, b in buiten)
            O[y][x] = SELOUT[p] if licht else 'k'
            continue
        # binnenlijn: grenst aan een onderdeel dat verder naar achteren ligt (andere groep)
        for a, b in nb4(x, y):
            q = part[b][a]
            if q != p and {p, q} not in ({'L', 'B'}, {'V', 'S'}, {'F', 'S'}, {'U', 'I'}, {'K', 'W'}, {'K', 'O'}) and VOOR.index(p) < VOOR.index(q):
                O[y][x] = SELOUT[p] if SELOUT[p] != 'e' else '4'
                break
open('raster_start.txt', 'w').write('\n'.join(''.join(r) for r in O) + '\n')
open('onderdelen.txt', 'w').write('\n'.join(''.join(r) for r in part) + '\n')
print(sum(c != '.' for r in O for c in r), 'px')
