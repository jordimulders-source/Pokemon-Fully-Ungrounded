"""Silhouet r1 (kolibrie pre, hoek B2): silhouet_direct.txt + handreparaties in vier zones.
Elke reparatie staat hieronder letterlijk als pixels; buiten de zones wordt niets aangeraakt."""
import os
D = os.path.dirname(os.path.abspath(__file__))
src = [list(r) for r in open(os.path.join(D, '..', 'silhouet_direct.txt')).read().split()]
g = [r[:] for r in src]

def zet(y, x0, x1, c='#'):
    for x in range(x0, x1 + 1): g[y][x] = c

# Zones (x0, y0, x1, y1), inclusief
ZONES = {
    'snavel': (13, 12, 21, 23),
    'kin':    (16, 24, 22, 30),
    'poten':  (22, 41, 37, 46),
    'staart': (38, 41, 46, 46),
}

# 1. Snavel: open bedelbekje in r7b-vorm, verkort. Linkerrand per rij (rest van de rij blijft).
#    y14: bovensnavelpunt x14-16, inkeping x17, voorhoofd x18 (ongewijzigd uit de render).
#    y15-17 onderkant bovensnavel, y18 diepste punt V (mondhoek), y19-23 bovenkant ondersnavel-wig.
links = {15: 15, 16: 17, 17: 19, 18: 20, 19: 19, 20: 18, 21: 16, 22: 15, 23: 15}
for y, xl in links.items():
    rechts = max(x for x in range(64) if src[y][x] == '#')
    zet(y, 13, 21, '.')
    zet(y, xl, min(21, rechts))

# 2. Kin/keel: kleine inham tussen kin en borst (y26-29), 2 rijen diep zodat het geen kras van 1 px is.
for y, xl in {26: 20, 27: 21, 28: 21, 29: 20}.items():
    zet(y, 16, xl - 1, '.')
    zet(y, xl, 22)

# 3. Pootjes (vorm profiel r2: stam + teenrij naar links), plekken uit de onderlaag.
zet(41, 35, 36, '.')                       # inkeping buik/staart 2 px i.p.v. spleet van 1 px
for y in (42, 43, 44, 45): zet(y, 22, 37, '.')
zet(42, 26, 28); zet(43, 26, 28); zet(44, 24, 28)   # nabije poot: stam 3, tenen naar links
zet(42, 31, 34); zet(43, 31, 34); zet(44, 32, 33)                  # verre poot: kleiner klompje (tenen van ons af), net als de render

# 4. Staartpunt: taps, geen losse pixel.
for y in (44, 45): zet(y, 38, 46, '.')
zet(44, 40, 44); zet(45, 42, 43)

open(os.path.join(D, 'silhouet.txt'), 'w').write('\n'.join(''.join(r) for r in g) + '\n')

# Diff per zone
def inzone(x, y):
    for n, (x0, y0, x1, y1) in ZONES.items():
        if x0 <= x <= x1 and y0 <= y <= y1: return n
    return 'buiten'
stat = {n: [0, 0] for n in list(ZONES) + ['buiten']}
for y in range(64):
    for x in range(64):
        a, b = src[y][x], g[y][x]
        if a != b: stat[inzone(x, y)][0 if b == '#' else 1] += 1
tot_s = sum(r.count('#') for r in src); tot = sum(r.count('#') for r in g)
print(f'direct {tot_s} px -> r1 {tot} px')
for n, (p, m) in stat.items(): print(f'  {n:7s} +{p} -{m}')
