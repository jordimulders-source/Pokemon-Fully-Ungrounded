"""Diff r4 tegen r3: alpha (omtrek) moet buiten de opdrachtzones gelijk zijn. Zones: POTEN (rij 46-55, x 14-38) en
VERRE_PUNTEN (rij 2-14, x 35-45). Telt ook kleurwijzigingen per gebied. Uitvoer: diff_uitvoer.txt. python3.11 diff.py"""
from palet import lees
A = lees('../r3/raster.txt'); B = lees('raster.txt')
ZONES = {'POTEN': (14, 46, 38, 55), 'VERRE_PUNTEN': (35, 2, 45, 14)}
def zone(x, y):
    for n, (x0, y0, x1, y1) in ZONES.items():
        if x0 <= x <= x1 and y0 <= y <= y1: return n
    return None
alpha = {}; kleur = {}
for y in range(64):
    for x in range(64):
        a, b = A[y][x], B[y][x]
        z = zone(x, y) or 'buiten'
        if (a == '.') != (b == '.'): alpha[z] = alpha.get(z, 0) + 1
        elif a != b: kleur[z] = kleur.get(z, 0) + 1
out = [f'zones: {ZONES}', f'alpha-diff (omtrek) per gebied: {alpha}', f'alpha-diff BUITEN de zones: {alpha.get("buiten", 0)}',
       f'kleurwijzigingen (zelfde omtrek) per gebied: {kleur}']
open('diff_uitvoer.txt', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
