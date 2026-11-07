"""PROEF (niet gebruikt): draaien met dichtstbijzijnde pixel gaf gebroken oog, spiraal en stippen; vervangen door schuin.py. Stap 1 van r6 (Jordi: "verder mag die nog iets meer achterover leunen"): het bovenlijf van sprite r5 (kop, nek, borst,
vleugels) eenmalig HOEK graden naar achteren draaien om de heup (DRAAIPUNT), dichtstbijzijnde pixel, geen kleurregels.
Poten, bliksem, steunstaart en staartlus (ONDER) blijven op hun plek. Uitvoer: raster_gedraaid.txt; daarna zet.py met de
handreparaties uit tekening.txt. Draaien: python3.11 draai.py"""
import math
import sys
sys.path.insert(0, '.')
from palet import lees
HOEK = 8.0                 # graden, met de klok mee = bovenlijf naar achteren (naar rechts)
DRAAIPUNT = (24.0, 38.0)   # heup
A = lees('../r5/raster.txt')
def onder(x, y):
    """blijft staan: alles vanaf rij 38 (poten, steunstaart, staartlus) en de bliksem links (x <= 13, rij 28-46)"""
    return y >= 38 or (x <= 13 and 28 <= y <= 46 and A[y][x] in '2y1k')
B = [['.'] * 64 for _ in range(64)]
for y in range(64):
    for x in range(64):
        if onder(x, y) and A[y][x] != '.': B[y][x] = A[y][x]
t = math.radians(HOEK); c, s = math.cos(t), math.sin(t); cx, cy = DRAAIPUNT
for y in range(64):
    for x in range(64):
        if B[y][x] != '.': continue
        # terugrekenen: welk bronpixel komt hier terecht (inverse draaiing)
        dx, dy = x - cx, y - cy
        sx, sy = cx + dx * c + dy * s, cy - dx * s + dy * c
        ix, iy = int(round(sx)), int(round(sy))
        if 0 <= ix < 64 and 0 <= iy < 64 and not onder(ix, iy) and A[iy][ix] != '.': B[y][x] = A[iy][ix]
open('raster_gedraaid.txt', 'w').write(f'# sprite r5, bovenlijf {HOEK} graden achterover om {DRAAIPUNT} (draai.py)\n' + '\n'.join(''.join(r) for r in B) + '\n')
print('raster_gedraaid.txt', sum(ch != '.' for r in B for ch in r), 'px')
