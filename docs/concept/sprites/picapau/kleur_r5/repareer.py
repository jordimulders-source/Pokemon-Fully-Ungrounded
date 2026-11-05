"""Ronde 5 (B): op kleur_r4/raster.txt -> raster.txt. Met de hand gekozen pixels."""
import os
D = os.path.dirname(os.path.abspath(__file__))
rows = [list(r.rstrip('\n')) for r in open(os.path.join(D, '..', 'kleur_r4', 'raster.txt'))][:64]
# 1. verre poot: twee teentjes die naar beneden/voren steken; silhouet +2: (35,48), (37,48)
rows[47][35] = 'G'; rows[47][37] = 'G'
rows[48][35] = 'k'; rows[48][37] = 'k'
# 3. diepe schaduw 4 -> 3, behalve (19,18): lijn snavel over voorhoofd (vorm over vorm), blijft 4
for x, y in [(39, 40), (39, 41), (40, 42), (40, 43), (41, 43), (41, 44), (42, 44), (41, 45), (39, 46), (40, 46)]:
    assert rows[y][x] == '4'; rows[y][x] = '3'
# 4. koplicht: lint langs de rand -> één vlek op de bolling van de kop
for y in range(12, 17):
    for x in range(19, 33):
        if rows[y][x] == '1':
            rows[y][x] = '2'
for x, y in [(26, 14), (27, 14), (28, 14), (25, 15), (26, 15), (27, 15), (28, 15), (26, 16), (27, 16)]:
    rows[y][x] = '1'
open(os.path.join(D, 'raster.txt'), 'w').write('\n'.join(''.join(r) for r in rows) + '\n')
