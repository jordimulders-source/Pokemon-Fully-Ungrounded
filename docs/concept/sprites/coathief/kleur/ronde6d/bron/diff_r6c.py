"""Pixeldiff ronde 6d tegen ronde 6c, per zone; buiten de zones moet 0 zijn."""
import os
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
a = Image.open(os.path.join(H, '../../ronde6c/coathief.png')).convert('RGBA').load()
b = Image.open(os.path.join(H, '../coathief.png')).convert('RGBA').load()
ZONES = {'overlap voorpoten (x 17-33, y 48-58)': (17, 48, 33, 58),
         'verdikking buiten die zone (x 15-34, y 48-61)': (15, 48, 34, 61)}
tel = {k: 0 for k in ZONES}; buiten = []
for y in range(64):
    for x in range(64):
        if a[x, y] != b[x, y] and not (a[x, y][3] == 0 and b[x, y][3] == 0):
            for k, (x0, y0, x1, y1) in ZONES.items():
                if x0 <= x <= x1 and y0 <= y <= y1: tel[k] += 1; break
            else: buiten.append((x, y))
for k, v in tel.items(): print('zone %-38s %3d px' % (k, v))
print('totaal', sum(tel.values()), '| buiten de zones:', len(buiten), buiten)
