"""Pixeldiff ronde 2 t.o.v. ronde 1 per zone. Kroonzone = alle kroonpixels (F/P in ../ronde1/labels.txt) + kwastjes. Draaien vanuit de repo-root."""
import os
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(H)
a = np.array(Image.open(os.path.join(K, 'ronde1/sapa_inca.png'))); b = np.array(Image.open(os.path.join(H, 'sapa_inca.png')))
lab = [l[3:] for l in open(os.path.join(K, 'ronde1/labels.txt')).read().split('\n')[:64]]
kroon = np.array([[c in 'FP' for c in r.ljust(64, '.')] for r in lab])
# kopkoepel (rij 19-21 binnen de waaier) is kop, geen kroon
kroon[19:23, 22:33] = False
zones = {'kroon': kroon,
         'kop (x22-33, y19-27)': np.zeros((64, 64), bool), 'vleugel (y18-33, x34-54)': np.zeros((64, 64), bool),
         'borst/lijf (y34-52)': np.zeros((64, 64), bool), 'poten/staart (y53-62)': np.zeros((64, 64), bool)}
zones['kop (x22-33, y19-27)'][19:28, 22:34] = True
zones['vleugel (y18-33, x34-54)'][18:34, 34:55] = True
zones['borst/lijf (y34-52)'][34:53, :] = True
zones['poten/staart (y53-62)'][53:63, :] = True
d = a != b
print('alpha-diff met ronde 1:', int(((a > 0) != (b > 0)).sum()))
seen = np.zeros_like(d)
for n, z in zones.items():
    zz = z & ~seen; seen |= z
    print(f'{n}: {int((d & zz).sum())} px gewijzigd')
print('rest:', int((d & ~seen).sum()))
