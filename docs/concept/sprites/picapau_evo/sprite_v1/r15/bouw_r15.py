"""r15: r14 (../r14/raster.txt) + reparaties.txt (met de hand, per zone) -> raster.txt, picapau_evo.png, normal.pal; controle.py;
diff tegen r14 per zone, en bewijs dat snavel (P5) en slierten 0 px veranderen. Draaien: python3.11 bouw_r15.py"""
import subprocess
from palet import lees
P = [list(r) for r in lees('../r14/raster.txt')]; R = [r[:] for r in P]
zone_van = {}; zones = []; z = None
for l in open('reparaties.txt'):
    if l.startswith('@'):
        z = l.split()[1]; zones.append(z); continue
    p = l.split()
    if len(p) == 3 and p[0].isdigit():
        y, x = int(p[0]), int(p[1])
        for i, c in enumerate(p[2]):
            if c == '.': continue
            R[y][x + i] = '.' if c == '_' else c; zone_van[(x + i, y)] = z
open('raster.txt', 'w').write('# sprite r15, 64x64, één teken per paletkleur (palet.py)\n' + '\n'.join(''.join(r) for r in R) + '\n')
subprocess.run(['python3.11', 'bouw.py'], check=True)
subprocess.run(['python3.11', 'controle.py'], check=True, capture_output=True)
def pix(fn):
    s = set()
    for l in open(fn):
        p = l.split()
        if len(p) == 3 and p[0].isdigit():
            for i, c in enumerate(p[2]):
                if c not in '._': s.add((int(p[1]) + i, int(p[0])))
    return s
# snavel P5 = de snavelregels uit ../r11/p5.txt (rij 8-13, zonder de vleugelrand '9 10 kkkkkkk')
snavel = set()
for l in open('../r11/p5.txt'):
    p = l.split()
    if len(p) == 3 and '_' not in p[2] and p[2] != 'kkkkkkk':
        for i in range(len(p[2])): snavel.add((int(p[1]) + i, int(p[0])))
slierten = pix('slierten.txt')
veranderd = [(x, y) for y in range(64) for x in range(64) if R[y][x] != P[y][x]]
out = [f'diff r15 tegen r14: {len(veranderd)} px veranderd']
for zn in zones:
    l = [f'{x},{y}:{P[y][x]}>{R[y][x]}' for (x, y) in veranderd if zone_van.get((x, y)) == zn]
    out.append(f'zone {zn}: {len(l)} px: ' + ' '.join(l))
out.append(f'buiten de zones: {sum(1 for p in veranderd if p not in zone_van)} px')
out.append(f'snavel P5 ({len(snavel)} px): {sum(1 for p in veranderd if p in snavel)} px verschil')
out.append(f'slierten ({len(slierten)} px): {sum(1 for p in veranderd if p in slierten)} px verschil')
# omtrek: pixels die van/naar transparant gingen, per zone
om = {}
for (x, y) in veranderd:
    if (P[y][x] == '.') != (R[y][x] == '.'): om.setdefault(zone_van.get((x, y)), []).append((x, y))
out.append('omtrek veranderd (transparant <-> gevuld) per zone: ' + '; '.join(f'{k}: {len(v)} px' for k, v in om.items()))
open('diff_uitvoer.txt', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out[:1] + out[-4:])); print(open('controle_uitvoer.txt').read())
