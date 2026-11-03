"""Silhouet r1 (kolibrie pre, K1 + lijf R2): silhouet_direct.txt + handreparaties in benoemde zones.
Elke reparatie staat hier letterlijk als pixels; buiten de zones wordt niets aangeraakt."""
import os
D = os.path.dirname(os.path.abspath(__file__))
src = [list(r) for r in open(os.path.join(D, '..', 'silhouet_direct.txt')).read().split()]
g = [r[:] for r in src]
def zet(y, x0, x1, c='#'):
    for x in range(x0, x1 + 1): g[y][x] = c

ZONES = {                     # (x0, y0, x1, y1) inclusief
    'bekje':  (13, 13, 19, 20),
    'kin':    (17, 23, 21, 27),
    'poten':  (23, 42, 36, 46),
    'staart': (37, 41, 46, 46),
    'glad':   [(17, 33), (43, 38)],   # twee losse pixels van de verkleining, ±1 px
}

# 1. Bekje: linkerrand per rij (rest van de rij blijft). Bovensnavel y14-15 (punt x15, zoals de render),
#    open V y15-17 (aan de voorkant 3 rijen, top op x17), ondersnavel y17-19 (punt 2x2 op x15-16).
for y, xl in {14: 15, 15: 16, 16: 18, 17: 17, 18: 15, 19: 15}.items():
    zet(y, 13, 19, '.'); zet(y, xl, 19)

# 2. Kin: inham van 1 px dieper onder de kopbol (y24-25), zodat kop en borst twee bollen lezen.
for y in (24, 25):
    zet(y, 17, 21, '.'); zet(y, 20, 21)

# 3. Pootjes: nabije poot = stam 3 px + teenrij 5 px naar links (plek uit de render);
#    het hangende buikstukje (x30-34, y42) wordt het verre stompje, kleiner, met 2 kolommen lucht ertussen.
for y in (42, 43, 44, 45): zet(y, 23, 36, '.')
zet(42, 26, 28); zet(43, 26, 28); zet(44, 24, 28)
zet(42, 31, 33); zet(43, 31, 33)

# 5. Gladmaken (±1 px): uitsteeksel van 1 px op de borst (17,33) weg, inkeping van 1 px in de rug (43,38) dicht.
g[33][17] = '.'; g[38][43] = '#'

# 4. Staartstompje: de render is al rond (6-5-3), geen losse pixel of trapje: niets veranderd.

open(os.path.join(D, 'silhouet.txt'), 'w').write('\n'.join(''.join(r) for r in g) + '\n')
def inzone(x, y):
    for n, z in ZONES.items():
        if isinstance(z, list):
            if (x, y) in z: return n
        elif z[0] <= x <= z[2] and z[1] <= y <= z[3]: return n
    return 'buiten'
stat = {n: [0, 0] for n in list(ZONES) + ['buiten']}
for y in range(64):
    for x in range(64):
        if src[y][x] != g[y][x]: stat[inzone(x, y)][0 if g[y][x] == '#' else 1] += 1
print(f"direct {sum(r.count('#') for r in src)} px -> r1 {sum(r.count('#') for r in g)} px")
for n, (p, m) in stat.items(): print(f'  {n:7s} +{p} -{m}')
