"""Pixeldiff ronde 2 tegen ronde 1, per zone; buiten de zones moet 0 zijn."""
import os
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
a = Image.open(os.path.join(H, '../../ronde1/coathief.png')).convert('RGBA').load()
b = Image.open(os.path.join(H, '../coathief.png')).convert('RGBA').load()
ZONES = {'1 vlekken rond het oog': (14, 34, 26, 47),
         '2 verre voorpoot': (26, 48, 33, 60),
         '4 klauwtjes verre voorpoot': (20, 61, 31, 62),
         '3 opgetilde voorpoot (boven klauwen)': (17, 49, 26, 55),
         '3 verre achterpoot': (34, 48, 42, 57),
         '3 nabije achterpoot': (43, 49, 53, 60)}
tel = {k: 0 for k in ZONES}; buiten = []
for y in range(64):
    for x in range(64):
        if a[x, y] != b[x, y]:
            for k, (x0, y0, x1, y1) in ZONES.items():
                if x0 <= x <= x1 and y0 <= y <= y1: tel[k] += 1; break
            else: buiten.append((x, y))
for k, v in tel.items(): print('zone %-38s %3d px' % (k, v))
print('totaal', sum(tel.values()), '| buiten de zones:', len(buiten), buiten)
