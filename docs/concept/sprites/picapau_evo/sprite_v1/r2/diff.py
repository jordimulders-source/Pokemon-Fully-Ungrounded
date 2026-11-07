"""Alpha-diff r2 tegen v1: buiten de toegestane zones moet het 0 zijn. Zones: KOP (punt 1: kop, oren, snavel;
x 2-31, rij 6-35), STROOK (punt 4; x 26-37, rij 17-35), POTEN (punt 6; x 18-33, rij 51-56). Uitvoer: diff_uitvoer.txt"""
V1 = [l.rstrip('\n') for l in open('raster_v1.txt')][:64]
R = [l.rstrip('\n') for l in open('raster.txt')][:64]
ZONES = {'KOP': {(x, y) for y in range(6, 36) for x in range(2, 32)},
         'STROOK': {(x, y) for y in range(17, 36) for x in range(26, 38)},
         'POTEN': {(x, y) for y in range(51, 57) for x in range(18, 34)}}
alle = {(x, y) for y in range(64) for x in range(64) if (V1[y][x] == '.') != (R[y][x] == '.')}
out = []
for n, z in ZONES.items(): out.append(f'alpha-diff in zone {n}: {len(alle & z)} px')
buiten = sorted(alle - set().union(*ZONES.values()), key=lambda p: (p[1], p[0]))
out.append(f'alpha-diff BUITEN de zones: {len(buiten)} {buiten}')
out.append(f'kleur gewijzigd (niet alpha): {sum(V1[y][x] != R[y][x] and V1[y][x] != "." and R[y][x] != "." for y in range(64) for x in range(64))} px')
open('diff_uitvoer.txt', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
