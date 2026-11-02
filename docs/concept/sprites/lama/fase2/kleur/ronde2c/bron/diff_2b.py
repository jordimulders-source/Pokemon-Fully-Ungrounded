"""Diff ronde 2c t.o.v. ronde 2b: telt gewijzigde pixels per opdrachtzone en daarbuiten (moet 0 zijn)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
a = open(os.path.join(HERE, '../../ronde2b/raster_grid.txt')).read().split()
b = open(os.path.join(HERE, '../raster_grid.txt')).read().split()
ZONES = {  # naam: (x0, y0, x1, y1) inclusief
    'R1 romp': (18, 30, 53, 40), 'R2 verre voorpoot': (30, 41, 36, 56), 'R3 aguayo': (34, 23, 53, 29),
    'R4 snuit': (10, 19, 17, 23), 'R5 nagels': [(22, 55), (29, 61)], 'spikkels': [(43, 51), (48, 56)]}
def zone(x, y):
    for n, z in ZONES.items():
        if isinstance(z, list):
            if (x, y) in z: return n
        elif z[0] <= x <= z[2] and z[1] <= y <= z[3]: return n
    return 'BUITEN'
cnt = {}
for y in range(64):
    for x in range(64):
        if a[y][x] != b[y][x]:
            n = zone(x, y); cnt.setdefault(n, []).append((x, y, a[y][x] + '>' + b[y][x]))
for n in list(ZONES) + ['BUITEN']:
    print(f'{n}: {len(cnt.get(n, []))}', cnt.get(n, []) if n != 'R1 romp' else '')
print('totaal', sum(len(v) for v in cnt.values()))
