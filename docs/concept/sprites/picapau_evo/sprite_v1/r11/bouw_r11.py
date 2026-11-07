"""r11: neemt probeersels/P5.png, haalt de oude oren weg (oude_oren.txt), zet wijzigingen.txt erop -> raster.txt, picapau_evo.png, normal.pal.
Daarna controle.py en diff tegen P5 (zones: krullen x14-46 y0-16 en verre vleugel x8-18 y7-17). Draaien: python3.11 bouw_r11.py"""
import subprocess
from PIL import Image
from palet import PAL, RGB
inv = {c: k for k, c in PAL}
p5 = Image.open('../probeersels/P5.png').convert('RGBA')
R = [[inv[p5.getpixel((x, y))[:3]] if p5.getpixel((x, y))[3] else '.' for x in range(64)] for y in range(64)]
P = [r[:] for r in R]
def zet(lijnen, wis=False):
    for l in lijnen:
        if not l.strip() or l.startswith('#'): continue
        y, x, s = l.split(); y, x = int(y), int(x)
        for i, c in enumerate(s):
            if c == '.': continue
            R[y][x + i] = '.' if (wis or c == '_') else c
zet(open('oude_oren.txt').read().split('\n'), wis=True)
zet(open('wijzigingen.txt').read().split('\n'))
open('raster.txt', 'w').write('# sprite r11, 64x64, één teken per paletkleur (palet.py)\n' + '\n'.join(''.join(r) for r in R) + '\n')
subprocess.run(['python3.11', 'bouw.py'], check=True)
subprocess.run(['python3.11', 'controle.py'], check=True, capture_output=True)
ZONES = [('krullen', 14, 46, 0, 16), ('verre vleugel', 8, 18, 7, 17)]
def zone(x, y):
    for n, x0, x1, y0, y1 in ZONES:
        if x0 <= x <= x1 and y0 <= y <= y1: return n
buiten = [(x, y) for y in range(64) for x in range(64) if R[y][x] != P[y][x] and not zone(x, y)]
out = [f'diff r11 tegen P5. BUITEN de zones (krullen x14-46 y0-16, verre vleugel x8-18 y7-17): {len(buiten)} px {buiten}']
for n, *_ in ZONES:
    l = [f'{x},{y}:{P[y][x]}>{R[y][x]}' for y in range(64) for x in range(64) if R[y][x] != P[y][x] and zone(x, y) == n]
    out.append(f'zone {n}: {len(l)} px: ' + ' '.join(l))
open('diff_uitvoer.txt', 'w').write('\n'.join(out) + '\n'); print(out[0]); print(open('controle_uitvoer.txt').read())
