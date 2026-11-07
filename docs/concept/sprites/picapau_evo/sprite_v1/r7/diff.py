"""Diff r7 tegen r6: bewijst 0 px verschil buiten de drie opdrachtzones en somt op wat er binnen elke zone veranderde.
Zones (rechthoeken, x0..x1 en y0..y1 inclusief): snavel x6-22 y7-14, krullen x14-46 y0-8 (zonder de snavelrechthoek), buik x9-28 y15-35.
Uitvoer: diff_uitvoer.txt. Draaien: python3.11 diff.py"""
import numpy as np
from PIL import Image
from palet import lees
a = lees('../r6/raster.txt'); b = lees('raster.txt')
pa = np.asarray(Image.open('../r6/picapau_evo.png').convert('RGBA')); pb = np.asarray(Image.open('picapau_evo.png').convert('RGBA'))
ZONES = [('snavel', 6, 22, 7, 14), ('krullen', 14, 46, 0, 8), ('buik', 9, 28, 15, 35)]
def zone(x, y):
    for n, x0, x1, y0, y1 in ZONES:
        if x0 <= x <= x1 and y0 <= y <= y1: return n
    return None
out = []; per = {n: [] for n, *_ in ZONES}; buiten = []
for y in range(64):
    for x in range(64):
        if a[y][x] != b[y][x]:
            z = zone(x, y)
            (per[z] if z else buiten).append((x, y, a[y][x], b[y][x]))
# controle op de png zelf (RGBA, transparant = alpha 0), los van het tekstraster
pd = [(x, y) for y in range(64) for x in range(64) if not zone(x, y) and
      not (pa[y, x, 3] == 0 and pb[y, x, 3] == 0) and tuple(pa[y, x]) != tuple(pb[y, x])]
out.append(f'BUITEN de zones: {len(buiten)} px verschil in raster.txt, {len(pd)} px verschil in picapau_evo.png {buiten or ""}{pd or ""}')
for n, x0, x1, y0, y1 in ZONES:
    l = per[n]
    out.append(f'\nzone {n} (x{x0}-{x1}, y{y0}-{y1}): {len(l)} px veranderd')
    kind = {}
    for x, y, o, w in l: kind[f'{o}->{w}'] = kind.get(f'{o}->{w}', 0) + 1
    out.append('  per overgang (oud->nieuw, . = transparant): ' + ', '.join(f'{k}: {v}' for k, v in sorted(kind.items())))
    rows = {}
    for x, y, o, w in l: rows.setdefault(y, []).append(f'{x}:{o}>{w}')
    for y in sorted(rows): out.append(f'  rij {y}: ' + ' '.join(rows[y]))
open('diff_uitvoer.txt', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
