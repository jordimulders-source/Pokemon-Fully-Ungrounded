"""Pixeldiff ronde 7 tegen ronde 6g, per zone; buiten de zones moet 0 zijn."""
import os
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
a = Image.open(os.path.join(H, '../../ronde6g/coathief.png')).convert('RGBA').load()
b = Image.open(os.path.join(H, '../coathief.png')).convert('RGBA').load()
ZONES = {'staande verre voorpoot (x 23-33, y 55-62)': (23, 55, 33, 62),
         'klauwen (x 12-30, y 53-62)': (12, 53, 30, 62)}
tel = {k: 0 for k in ZONES}; buiten = []
for y in range(64):
    for x in range(64):
        if a[x, y] != b[x, y] and not (a[x, y][3] == 0 and b[x, y][3] == 0):
            for k, (x0, y0, x1, y1) in ZONES.items():
                if x0 <= x <= x1 and y0 <= y <= y1: tel[k] += 1; break
            else: buiten.append((x, y))
for k, v in tel.items(): print('zone %-38s %3d px' % (k, v))
print('totaal', sum(tel.values()), '| buiten de zones:', len(buiten), buiten)

print('bevroren gumrand x 31-32, y 48-54 en bovenarm/manchet y < 55:', sum(1 for y in range(48,55) for x in range(17,34) if a[x,y]!=b[x,y]), 'px verschil')
