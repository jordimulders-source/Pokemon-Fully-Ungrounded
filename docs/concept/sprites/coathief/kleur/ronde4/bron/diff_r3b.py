"""Pixeldiff ronde 4 tegen ronde 3b, per zone; buiten de zones moet 0 zijn."""
import os
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
a = Image.open(os.path.join(H, '../../ronde3b/coathief.png')).convert('RGBA').load()
b = Image.open(os.path.join(H, '../coathief.png')).convert('RGBA').load()
ZONES = {'1 oren': (14, 30, 26, 34),
         '2 mond': (8, 45, 14, 47),
         '3 klauwen opgetilde poot': (10, 56, 23, 61),
         '4 staande verre voorpoot': (24, 50, 33, 62),
         '4 losse teentjes y 62 (weg)': (21, 62, 25, 62)}
tel = {k: 0 for k in ZONES}; buiten = []
for y in range(64):
    for x in range(64):
        if a[x, y] != b[x, y] and not (a[x, y][3] == 0 and b[x, y][3] == 0):
            for k, (x0, y0, x1, y1) in ZONES.items():
                if x0 <= x <= x1 and y0 <= y <= y1: tel[k] += 1; break
            else: buiten.append((x, y))
for k, v in tel.items(): print('zone %-38s %3d px' % (k, v))
print('totaal', sum(tel.values()), '| buiten de zones:', len(buiten), buiten)
