"""Ronde 6: diff per zone t.o.v. ronde 5b. Draaien vanuit de repo-root."""
import os
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(H)
a = np.array(Image.open(os.path.join(K, 'ronde5b/sapa_inca.png'))); b = np.array(Image.open(os.path.join(H, 'sapa_inca.png')))
lab = [l[3:].ljust(64, '.') for l in open(os.path.join(K, 'ronde1/labels.txt')).read().split('\n')[:64]]
def box(x0, y0, x1, y1):
    m = np.zeros((64, 64), bool); m[y0:y1 + 1, x0:x1 + 1] = True; return m
Z = {}
Z['kroon'] = np.array([[c in 'FP' for c in r] for r in lab]); Z['kroon'][19:23, 22:33] = False
Z['gezicht en ogen (x22-33 y19-27)'] = box(22, 19, 33, 27)
Z['opgeheven rechtervleugel (x34-54 y18-33)'] = box(34, 18, 54, 33)
Z['staf + zon boven de hand (x13-19 y25-36)'] = box(13, 25, 19, 36)
Z['staf voor de vleugel + vouwrand (x14-16 y37-42)'] = box(14, 37, 16, 42)
Z['linkervleugel overig (x12-20 y37-46)'] = box(12, 37, 20, 46)
Z['staf onder de vleugel + boog (x12-23 y47-52)'] = box(12, 47, 23, 52)
Z['buik + lijf (x20-39 y34-52)'] = box(20, 34, 39, 52)
Z['poten (y53-62)'] = box(20, 53, 36, 62)
d = a != b; seen = np.zeros_like(d)
print('silhouet: erbij', int(((b > 0) & (a == 0)).sum()), 'eraf', int(((a > 0) & (b == 0)).sum()), 'totaal', int((b > 0).sum()))
for n, z in Z.items():
    zz = z & ~seen; seen |= z
    print(f'{n}: {int((d & zz).sum())} px (silhouet +{int((zz & (b > 0) & (a == 0)).sum())} / -{int((zz & (a > 0) & (b == 0)).sum())})')
print('rest:', [(int(x), int(y)) for y, x in zip(*np.nonzero(d & ~seen))])
