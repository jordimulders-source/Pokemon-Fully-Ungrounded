"""Ronde 11: kleur/schaduw naar latere generaties, gouden staf zonder gloed, kop en ogen 1-2 px groter.
Werkt op het raster van ronde 10 (bovenaan sapa_inca.txt) en schrijft het blok 'ronde 11' + het nieuwe palet. Draaien vanuit de repo-root."""
import os, sys
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import bouw
src = os.path.join(H, 'sapa_inca.txt')
txt = open(src).read().split('# ==== ronde 11')[0].rstrip('\n') + '\n'
# ---- nieuw palet (zelfde letters; waarden naar latere generaties) ----
PAL = {
    'K': (22, 14, 26),     # zwart, iets paars
    'd': (46, 30, 50),     # schaduw lijf: koel paarsbruin
    'm': (98, 66, 64),     # basis lijf
    'l': (172, 120, 98),   # lichte selout / licht lijf: warm
    'r': (178, 46, 46),    # schaduw rood: iets koeler
    'R': (238, 98, 48), 'o': (252, 166, 96),
    'p': (112, 86, 172), 'v': (186, 168, 238),
    'a': (206, 110, 30),   # goud schaduw: oranje
    'g': (242, 180, 54),   # goud basis
    'y': (254, 240, 156),  # goud licht: bleekgeel
    'b': (106, 120, 150), 'w': (224, 232, 240),
    't': (128, 62, 44),    # donker oker/roestbruin (staf schaduwkant, vaan)
}
lines = []
for ln in txt.split('\n'):
    p = ln.split()
    if len(p) == 5 and p[0] == 'P':
        ln = 'P %s %d %d %d' % ((p[1],) + PAL[p[1]])
    lines.append(ln)
txt = '\n'.join(lines)
open(src, 'w').write(txt)
pal, letters, g0 = bouw.bouw(src)
inv = {v: c for c, v in letters.items()}
L = np.vectorize(lambda v: '.' if v == 0 else inv[v])(g0).astype('<U1'); L0 = L.copy()
punt = {}
def zet(p, x, y, c):
    if L[y, x] != c:
        L[y, x] = c; punt.setdefault(p, set()).add((x, y))
def rij(p, y, x0, s):
    for i, c in enumerate(s):
        if c != ' ':
            zet(p, x0 + i, y, '.' if c == '_' else c)
# ---- 1. staf: goud zonder gloed (basis g, schaduw t, licht y alleen kort links, glans w op de kop) ----
P1 = '1 staf'
rij(P1, 20, 14, 'gaK'); rij(P1, 21, 14, 'agK')
rij(P1, 22, 13, 'aygaK'); rij(P1, 23, 13, 'awgaK'); rij(P1, 24, 13, 'aygggK'); rij(P1, 25, 13, 'aggaK')
rij(P1, 26, 12, 'ttagatK'); rij(P1, 27, 12, 'KttgttK'); rij(P1, 28, 13, 'dtgtK')
for y in (29, 30, 31, 32):
    rij(P1, y, 13, 'dygtK' if y in (30, 31) else 'dggtK')
for y in (33, 34, 35):
    rij(P1, y, 14, 'dytK' if y == 34 else 'dgtK')
for y in range(36, 42):
    rij(P1, y, 14, 'dyt' if y == 38 else 'dgt')
# ---- 2. kop en ogen groter (kop 13 breed, rood masker 1 rij langer; ogen en snavel 2 rijen) ----
P2 = '2 kop en ogen'
rij(P2, 23, 22, 'rddRwbRrddrK')
rij(P2, 24, 21, 'rrKybwbRwKyrK')
rij(P2, 25, 21, 'rRaybwwbyyaygK')
rij(P2, 26, 21, 'rRrbwbKRRrrgaK')
rij(P2, 27, 21, 'rrbdKrrrrrmaK')
rij(P2, 28, 21, 'llKmmdmmddddK')
# ---- 3. gekleurde lichte selout aan de lichtkant van lijf, vleugels en hals ----
P3 = '3 lichte selout'
for y in range(1, 63):
    for x in range(1, 63):
        if L[y, x] not in 'dm':
            continue
        lit = L[y, x - 1] == '.' or L[y - 1, x] == '.'
        sh = L[y, x + 1] == '.' or L[y + 1, x] == '.'
        if lit and not sh and y >= 26 and x >= 12 and not (13 <= x <= 14 and 28 <= y <= 41):
            zet(P3, x, y, 'l')
with open(src, 'a') as f:
    f.write('\n# ==== ronde 11 (gegenereerd door reparatie11.py) ====\n')
    for y in range(64):
        for x in range(64):
            if L[y, x] != L0[y, x]:
                f.write(f'{y} {x} {"_" if L[y, x] == "." else L[y, x]}\n')
for p in sorted(punt):
    print(f'{p}: {len(punt[p])} px')
print('totaal gewijzigd (pixels):', int((L != L0).sum()), '; silhouet erbij', int(((L != '.') & (L0 == '.')).sum()), 'eraf', int(((L == '.') & (L0 != '.')).sum()))
