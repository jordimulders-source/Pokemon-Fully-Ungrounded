"""r13: r12 zonder zijn slierten (../r12/slierten.txt gewist) + slierten.txt -> raster.txt, picapau_evo.png, normal.pal; controle.py;
diff tegen r12 (zone slierten x24-46, y0-14); minimale afstand slierten–vleugel (Chebyshev, 1 = raakt, >= 2 = minstens 1 px lucht).
Draaien: python3.11 bouw_r13.py"""
import subprocess
from palet import lees
P = [list(r) for r in lees('../r12/raster.txt')]; R = [r[:] for r in P]
def pix(fn):
    s = {}
    for l in open(fn):
        p = l.split()
        if len(p) == 3 and p[0].isdigit():
            for i, c in enumerate(p[2]):
                if c != '.': s[(int(p[1]) + i, int(p[0]))] = c
    return s
for (x, y) in pix('../r12/slierten.txt'): R[y][x] = '.'
nieuw = pix('slierten.txt')
for (x, y), c in nieuw.items(): R[y][x] = c
open('raster.txt', 'w').write('# sprite r13, 64x64, één teken per paletkleur (palet.py)\n' + '\n'.join(''.join(r) for r in R) + '\n')
subprocess.run(['python3.11', 'bouw.py'], check=True)
subprocess.run(['python3.11', 'controle.py'], check=True, capture_output=True)
Z = (24, 46, 0, 14)
inz = lambda x, y: Z[0] <= x <= Z[1] and Z[2] <= y <= Z[3]
buiten = [(x, y) for y in range(64) for x in range(64) if R[y][x] != P[y][x] and not inz(x, y)]
binnen = [f'{x},{y}:{P[y][x]}>{R[y][x]}' for y in range(64) for x in range(64) if R[y][x] != P[y][x] and inz(x, y)]
# vleugel = alle niet-slierten-pixels rechts van de kop (x >= 37) en de nabije vleugel; kop zelf telt niet
vleugel = [(x, y) for y in range(64) for x in range(64) if R[y][x] != '.' and (x, y) not in nieuw and x >= 37 and y <= 20]
afst = min((max(abs(x - a), abs(y - b)), (x, y), (a, b)) for (x, y) in nieuw for (a, b) in vleugel)
out = [f'diff r13 tegen r12. BUITEN de zone slierten (x24-46, y0-14): {len(buiten)} px {buiten}', f'binnen: {len(binnen)} px: ' + ' '.join(binnen),
       f'minimale afstand slierten-vleugel (Chebyshev; 1 = raakt, 2 = 1 px lucht): {afst[0]} (spriet {afst[1]}, vleugel {afst[2]})']
open('diff_uitvoer.txt', 'w').write('\n'.join(out) + '\n'); print(out[0]); print(out[2]); print(open('controle_uitvoer.txt').read())
