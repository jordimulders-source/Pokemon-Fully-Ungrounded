"""Ronde 14: reparaties op ronde 13 (palet ongewijzigd). Schrijft het blok 'ronde 14' onderaan sapa_inca.txt, een diff per punt
(RGB voor -> na) en een lijst losse pixels. Draaien vanuit de repo-root."""
import os, sys
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(H); sys.path.insert(0, H)
import bouw
src = os.path.join(H, 'sapa_inca.txt')
_t = open(src).read().split('# ==== ronde 14')[0].rstrip('\n') + '\n'
open(src, 'w').write(_t)
pal, letters, g0 = bouw.bouw(src)
inv = {v: c for c, v in letters.items()}; rgb = {c: v for c, v in pal}
L = np.vectorize(lambda v: '.' if v == 0 else inv[v])(g0).astype('<U1'); L0 = L.copy()
r9 = np.array(Image.open(os.path.join(K, 'ronde9/v3_een_boog_gouden_rand.png')))
inv9 = {i + 1: c for i, (c, _) in enumerate(pal)}
punt = {}
def zet(p, x, y, c):
    if L[y, x] != c:
        punt.setdefault(p, []).append((x, y, L[y, x], c)); L[y, x] = c
def rij(p, y, x0, s):
    for i, c in enumerate(s):
        if c != ' ':
            zet(p, x0 + i, y, '.' if c == '_' else c)
# 1. overgang staf en lijf: donkere scheiding (K) tussen staf en lijf; staf in 3 tinten (licht boven, schaduw onder, roestbruine vaan)
P = '1 overgang staf/lijf'
rij(P, 47, 14, 'KKygaKd')     # x14-20: omlijning, licht y, basis g, schaduw a, scheiding K, lijf d
rij(P, 48, 16, 'KttKd')       # x16-20: omlijning, roestbruine vaan t t, scheiding K, lijf
rij(P, 49, 17, 'KKd')         # onderrand van de staf sluit, lijf eronder
# 2. stafpunt: spits, taps tot 1 px (zoals de puntige stafkop van ronde 9), licht/donker goud, omlijning eromheen
P = '2 stafpunt'
for y in (18, 19, 20, 21):
    for x in (13, 14, 15, 16):
        c = inv9.get(int(r9[y, x]), '.') if r9[y, x] else '.'
        zet(P, x, y, c)       # eerst de kroon terug zoals in ronde 9 waar de oude punt lag
rij(P, 16, 15, 'K')
rij(P, 17, 14, 'dyK')
rij(P, 18, 14, 'dyK')
rij(P, 19, 14, 'dyK')
rij(P, 20, 14, 'dyaK')
rij(P, 21, 13, 'dygaK')
zet(P, 17, 19, 'o')
# 3. poten: zelfde opbouw (dij, scheen, voet), verre poot donkerder; ruimte ertussen schoon
P = '3 poten'
rij(P, 54, 24, 'dgga'); rij(P, 55, 24, 'dgaa'); rij(P, 56, 24, 'daaK')
rij(P, 57, 24, 'dgK'); rij(P, 58, 24, 'dgK'); rij(P, 59, 24, 'daK')
rij(P, 60, 22, 'KdgaK'); rij(P, 61, 21, 'KKKKK')
rij(P, 54, 29, 'dyggaK'); rij(P, 55, 29, 'dggaaK'); rij(P, 56, 29, 'daaaK_')
rij(P, 57, 29, '_dyaK'); rij(P, 58, 30, 'dgaK'); rij(P, 59, 30, 'dgaK'); rij(P, 60, 30, 'dgaK')
rij(P, 61, 29, 'dgggaK'); rij(P, 62, 29, 'KKKKK')
# 4. verre oog: lid, iris, pupil en een kleine reflectie (zonder glans)
P = '4 verre oog'
zet(P, 23, 23, 'd'); zet(P, 24, 23, 'd'); zet(P, 23, 24, 'K'); zet(P, 24, 24, 'y'); zet(P, 23, 25, 'a')
P = '6 losse pixels'
zet(P, 31, 25, 'm')   # los rood naast het nabije oog
# 5. losse lavendel pixels onder de kroonrand rechts, boven de opgeheven vleugel: kroon (schaduwrood) met zwarte omlijning
P = '5 paarse pixels'
for x, y in ((46, 20), (45, 21)):
    zet(P, x, y, 'r')
for x, y in ((47, 20), (46, 21)):
    zet(P, x, y, 'K')
with open(src, 'a') as f:
    f.write('# ==== ronde 14 (gegenereerd door reparatie14.py) ====\n')
    for y in range(64):
        for x in range(64):
            if L[y, x] != L0[y, x]:
                f.write(f'{y} {x} {"_" if L[y, x] == "." else L[y, x]}\n')
c = lambda k: 'transparant' if k == '.' else str(rgb[k])
G = {'d': 'bruin', 'm': 'bruin', 'l': 'bruin', 'r': 'rood', 'R': 'rood', 'o': 'rood', 'p': 'lavendel', 'v': 'lavendel',
     'a': 'goud', 'g': 'goud', 'y': 'goud', 'b': 'snavel', 'w': 'snavel', 't': 'roest'}
los = []
for y in range(64):
    for x in range(64):
        k = L[y, x]
        if k in '.K':
            continue
        nb = [L[y + dy, x + dx] for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx or dy) and 0 <= x + dx < 64 and 0 <= y + dy < 64]
        if not any(G.get(n) == G[k] for n in nb):
            los.append((x, y, k))
with open(os.path.join(H, 'diff_per_punt.txt'), 'w') as f:
    for p in sorted(punt):
        f.write(f'{p}: {len(punt[p])} px\n')
        for x, y, a, b in punt[p]:
            f.write(f'  ({x},{y}) {c(a)} -> {c(b)}\n')
    f.write(f'totaal {int((L != L0).sum())} px; silhouet erbij {int(((L != ".") & (L0 == ".")).sum())}, eraf {int(((L == ".") & (L0 != ".")).sum())}\n')
    f.write(f'losse pixels (geen buur in dezelfde kleurgroep, zwart niet meegeteld): {los}\n')
for p in sorted(punt): print(p, len(punt[p]))
print('totaal', int((L != L0).sum()), 'silhouet +', int(((L != ".") & (L0 == ".")).sum()), '-', int(((L == ".") & (L0 != ".")).sum()))
print('losse pixels:', los)
