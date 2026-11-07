"""Pixeldiff ronde 3 tegen ronde 2, per zone; buiten de zones moet 0 zijn."""
import os
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
a = Image.open(os.path.join(H, '../../ronde2/coathief.png')).convert('RGBA').load()
b = Image.open(os.path.join(H, '../coathief.png')).convert('RGBA').load()
ZONES = {'1 oog (vlekglans)': (18, 36, 23, 45),
         '2 mond': (8, 45, 14, 47),
         '3 naad kop-hals': (22, 34, 28, 47),
         '4a randen staart en oren': (14, 0, 60, 33),
         '4b klauwen opgetilde poot': (16, 56, 21, 60),
         '4c voet (24,61)': (24, 61, 24, 61)}
tel = {k: 0 for k in ZONES}; buiten = []
for y in range(64):
    for x in range(64):
        if a[x, y] != b[x, y]:
            for k, (x0, y0, x1, y1) in ZONES.items():
                if x0 <= x <= x1 and y0 <= y <= y1: tel[k] += 1; break
            else: buiten.append((x, y))
for k, v in tel.items(): print('zone %-38s %3d px' % (k, v))
print('totaal', sum(tel.values()), '| buiten de zones:', len(buiten), buiten)
