"""Ronde 4: diff per zone t.o.v. ronde 3 (incl. de 2 staartpixels van de coordinator). Draaien vanuit de repo-root."""
import os
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(H)
r3 = np.array(Image.open(os.path.join(K, 'ronde3/sapa_inca.png'))); r4 = np.array(Image.open(os.path.join(H, 'sapa_inca.png')))
lab = [l[3:].ljust(64, '.') for l in open(os.path.join(K, 'ronde1/labels.txt')).read().split('\n')[:64]]
Z = {}
Z['kroon'] = np.array([[c in 'FP' for c in r] for r in lab]); Z['kroon'][19:23, 22:33] = False
def box(x0, y0, x1, y1):
    m = np.zeros((64, 64), bool); m[y0:y1 + 1, x0:x1 + 1] = True; return m
Z['gezicht (x22-33 y19-27)'] = box(22, 19, 33, 27)
Z['opgeheven rechtervleugel (x34-54 y18-33)'] = box(34, 18, 54, 33)
Z['buik (goud van ronde 3, y34-52)'] = np.isin(r3, [10, 11, 12]) & box(20, 34, 33, 52)
Z['rechterpoot + staartpixels (x28-34 y53-62)'] = box(28, 53, 34, 62)
Z['linkerpoot (x21-27 y53-61)'] = box(21, 53, 27, 61)
Z['staf + zon (x13-19 y25-39)'] = box(13, 25, 17, 35) | box(13, 25, 19, 29)
Z['linkervleugel + staf-onderkant + opvulling (x12-24 y36-53)'] = box(12, 36, 24, 53)
d = r3 != r4; seen = np.zeros_like(d)
print('alpha: erbij', int(((r4 > 0) & (r3 == 0)).sum()), 'eraf', int(((r3 > 0) & (r4 == 0)).sum()), 'totaal', int((r4 > 0).sum()))
for n, z in Z.items():
    zz = z & ~seen; seen |= z
    pts = [(int(x), int(y)) for y, x in zip(*np.nonzero(d & zz))]
    print(f'{n}: {len(pts)} px', pts if 0 < len(pts) <= 14 else '')
print('rest:', [(int(x), int(y)) for y, x in zip(*np.nonzero(d & ~seen))])
