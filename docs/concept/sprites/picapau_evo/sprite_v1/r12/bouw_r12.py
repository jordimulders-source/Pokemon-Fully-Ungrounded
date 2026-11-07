"""r12: r11 zonder zijn slierten (de oor-regels uit ../r11/wijzigingen.txt worden gewist) + slierten.txt (met de hand)
-> raster.txt, picapau_evo.png, normal.pal; controle.py; diff tegen r11 (zone slierten x24-46, y0-14). Draaien: python3.11 bouw_r12.py"""
import subprocess
from palet import lees
P = [list(r) for r in lees('../r11/raster.txt')]; R = [r[:] for r in P]
lees_oor = False
for l in open('../r11/wijzigingen.txt'):
    if l.startswith('# --- 2.'): lees_oor = True
    if l.startswith('# --- 3.'): lees_oor = False
    p = l.split()
    if lees_oor and len(p) == 3 and p[0].isdigit():
        for i, c in enumerate(p[2]): R[int(p[0])][int(p[1]) + i] = '.'
for l in open('slierten.txt'):
    p = l.split()
    if len(p) != 3 or not p[0].isdigit(): continue
    for i, c in enumerate(p[2]):
        if c != '.': R[int(p[0])][int(p[1]) + i] = c
open('raster.txt', 'w').write('# sprite r12, 64x64, één teken per paletkleur (palet.py)\n' + '\n'.join(''.join(r) for r in R) + '\n')
subprocess.run(['python3.11', 'bouw.py'], check=True)
subprocess.run(['python3.11', 'controle.py'], check=True, capture_output=True)
Z = (24, 46, 0, 14)
inz = lambda x, y: Z[0] <= x <= Z[1] and Z[2] <= y <= Z[3]
buiten = [(x, y) for y in range(64) for x in range(64) if R[y][x] != P[y][x] and not inz(x, y)]
binnen = [f'{x},{y}:{P[y][x]}>{R[y][x]}' for y in range(64) for x in range(64) if R[y][x] != P[y][x] and inz(x, y)]
open('diff_uitvoer.txt', 'w').write(f'diff r12 tegen r11. BUITEN de zone slierten (x24-46, y0-14): {len(buiten)} px {buiten}\nbinnen: {len(binnen)} px: ' + ' '.join(binnen) + '\n')
print(open('diff_uitvoer.txt').read().split('\n')[0]); print(open('controle_uitvoer.txt').read())
