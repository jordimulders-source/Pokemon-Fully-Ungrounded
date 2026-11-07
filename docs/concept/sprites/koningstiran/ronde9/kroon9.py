"""Ronde 9: kroonpatroon als constructie op de 9 radiale veren (centrum kopbasis (28.5,21), veren elk 20 graden).
Schrijft per variant een raster (ronde 8 + pixelregels onderaan) en bouwt de PNG. Draaien vanuit de repo-root.
Regels: (1) oude zwarte stippen/vlekken in het oranje weg (opgevuld met de veertint eromheen); zwarte veerscheidingen
aan de schaduwkant worden R (lichte veerrand), de andere scheidingen blijven; (2) per veer hetzelfde motief op dezelfde
afstand van de kop; (3) per veerpunt in de lavendel rand dezelfde vlek, rondom."""
import math, os, sys
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(H)
sys.path.insert(0, H)
import bouw
pal, letters, g0 = bouw.bouw(os.path.join(H, 'sapa_inca.txt'))
inv = {v: c for c, v in letters.items()}
L0 = np.vectorize(lambda v: '.' if v == 0 else inv[v])(g0)
lab = [l[3:].ljust(64, '.') for l in open(os.path.join(K, 'ronde1/labels.txt')).read().split('\n')[:64]]
fan = np.array([[c == 'F' for c in r] for r in lab])
CX, CY = 28.5, 21.0
r8 = np.array(Image.open(os.path.join(K, 'ronde8/sapa_inca.png')))
r7b = np.array(Image.open(os.path.join(K, 'ronde7b/sapa_inca.png')))
vrij = (r8 == r7b)            # zon van de staf (ronde 8) niet aanraken
vrij[19:23, 22:33] = False    # kopkoepel niet aanraken
def rad(x, y):
    return math.hypot(x + 0.5 - CX - 0.5, CY - y), math.degrees(math.atan2(CY - y, x - CX))
sep = set()
for A in range(20, 180, 20):
    for r10 in range(60, 175, 5):
        r = r10 / 10
        sep.add((int(math.floor(CX + r * math.cos(math.radians(A)))), int(math.floor(CY - r * math.sin(math.radians(A)) + 0.5))))
def schoon():
    L = L0.copy()
    for y in range(1, 23):
        for x in range(9, 49):
            if not (vrij[y, x] and L0[y, x] == 'K'):
                continue
            r, a = rad(x, y)
            if r >= 17.6 or y >= 22 or not fan[y, x] and r < 17.6 and y > 21:
                continue
            if (x, y) in sep:
                L[y, x] = 'R'
            else:
                nb = [L0[y + dy, x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if L0[y + dy, x + dx] in 'rRo']
                L[y, x] = max(set(nb), key=nb.count) if nb else 'r'
    for y in range(1, 22):
        for x in range(29, 49):
            if not (vrij[y, x] and L[y, x] in 'rR' and fan[y, x]):
                continue
            r, a = rad(x, y)
            if r >= 17.6 or r < 6 or a >= 80:
                continue
            L[y, x] = 'r' if ((x, y) in sep or r < 11) else 'R'
    return L
def punt(k, r):
    A = math.radians(10 + 20 * k)
    return int(math.floor(CX + r * math.cos(A))), int(math.floor(CY - r * math.sin(A) + 0.5))
def zet(L, x, y, c, alleen='rRo'):
    if vrij[y, x] and L[y, x] in alleen:
        L[y, x] = c
def goud(k):
    return ('y', 'g') if k >= 5 else (('y', 'g') if k == 4 else ('g', 'a'))
def boog(L, r, groot=True):
    for k in range(9):
        x, y = punt(k, r)
        if groot:   # 2x2: licht linksboven, middentint, schaduw (a) rechtsonder; schaduwkant (rechts) een tint donkerder
            licht = k >= 4
            blok = {(0, 0): 'y' if licht else 'g', (1, 0): 'g', (0, 1): 'g' if licht else 'a', (1, 1): 'a'}
            for (dx, dy), c in blok.items():
                zet(L, x + dx, y + dy, c)
        else:       # kleine boog: 1 punt licht + 1 schaduw eronder
            zet(L, x, y, 'y' if k >= 4 else 'g'); zet(L, x, y + 1, 'a')
def rand(L, c, n=2):
    kand = []
    # per veerpunt: de lavendel vulling (niet de buitenste omlijning) binnen +-4,5 graden van het veermidden
    for y in range(0, 24):
        for x in range(8, 50):
            if not vrij[y, x] or L0[y, x] not in 'vpK':
                continue
            r, a = rad(x, y)
            if r < 17.6 or y > 21:
                continue
            buiten = any(L0[y + dy, x + dx] == '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if buiten:
                continue
            if L0[y, x] == 'K' and not any(L0[y + dy, x + dx] in 'mdl' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1))):
                L[y, x] = 'p'   # oude zwarte streepjes in de rand tussen de veerpunten weg
            kand.append((min(abs(a - (10 + 20 * k)) for k in range(9)), min(range(9), key=lambda k: abs(a - (10 + 20 * k))), x, y))
    for k in range(9):   # per veerpunt precies de 2 vullingpixels die het dichtst bij het veermidden liggen
        for _, kk, x, y in sorted(c2 for c2 in kand if c2[1] == k)[:n]:
            L[y, x] = c
def schrijf(naam, L):
    with open(os.path.join(H, naam + '.txt'), 'w') as f:
        f.write(open(os.path.join(H, 'sapa_inca.txt')).read().rstrip('\n') + f'\n# ==== ronde 9 kroon: {naam} (gegenereerd door kroon9.py) ====\n')
        for y in range(64):
            for x in range(64):
                if L[y, x] != L0[y, x]:
                    f.write(f'{y} {x} {"_" if L[y, x] == "." else L[y, x]}\n')
    p, le, g = bouw.bouw(os.path.join(H, naam + '.txt'))
    bouw.save(p, g, os.path.join(H, naam + '.png'))
    return int((g != g0).sum())
r2 = np.array(Image.open(os.path.join(K, 'ronde2/sapa_inca.png')))
def stafkop(L):
    for y in range(19, 28):
        for x in range(11, 20):
            L[y, x] = '.' if r2[y, x] == 0 else inv[r2[y, x]]
    rows = {19: (15, 'K'), 20: (14, 'KaK'), 21: (14, 'KyK'), 22: (13, 'KayaK'), 23: (13, 'Kyyga'),
            24: (12, 'Kayggga'), 25: (13, 'aggga'), 26: (12, 'ttagatt'), 27: (12, 'tttyttt')}
    for y, (x0, st) in rows.items():
        for i, c in enumerate(st):
            L[y, x0 + i] = c
V = {}
L = schoon(); stafkop(L); boog(L, 14.6); rand(L, 'K'); V['v1_een_boog_zwarte_rand'] = L
L = schoon(); stafkop(L); boog(L, 14.6); boog(L, 10.2, groot=False); rand(L, 'g'); V['v2_twee_bogen_gouden_rand'] = L
L = schoon(); stafkop(L); boog(L, 14.6); rand(L, 'g', n=3); V['v3_een_boog_gouden_rand'] = L
for n, L in V.items():
    print(n, schrijf(n, L), 'px gewijzigd t.o.v. ronde 8')
