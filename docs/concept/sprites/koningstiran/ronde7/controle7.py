"""Ronde 7: diff per zone t.o.v. ronde 6b + breedte van de gele buik per rij. Draaien vanuit de repo-root."""
import os
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(H)
a = np.array(Image.open(os.path.join(K, 'ronde6b/sapa_inca.png'))); b = np.array(Image.open(os.path.join(H, 'sapa_inca.png')))
pal = [l.split()[1] for l in open(os.path.join(H, 'sapa_inca.txt')) if l.startswith('P ')]
C = np.vectorize(lambda v: '.' if v == 0 else pal[v - 1]); La, Lb = C(a), C(b)
lab = [l[3:].ljust(64, '.') for l in open(os.path.join(K, 'ronde1/labels.txt')).read().split('\n')[:64]]
def box(x0, y0, x1, y1):
    m = np.zeros((64, 64), bool); m[y0:y1 + 1, x0:x1 + 1] = True; return m
Z = {}
Z['kroon'] = np.array([[c in 'FP' for c in r] for r in lab]); Z['kroon'][19:23, 22:33] = False
Z['gezicht en ogen (x22-33 y19-27)'] = box(22, 19, 33, 27)
Z['opgeheven rechtervleugel (x34-54 y18-33)'] = box(34, 18, 54, 33)
Z['stafkop (x12-20 y23-29)'] = box(12, 23, 20, 29)
Z['staf boven de hand (x12-17 y30-36)'] = box(12, 30, 17, 36)
Z['linkervleugel + staf voor de vleugel (x12-20 y37-48)'] = box(12, 37, 20, 48)
Z['poten (y53-62, behalve aansluiting)'] = box(24, 53, 36, 62)
Z['buik + lijf (x16-39 y34-53)'] = box(16, 34, 39, 53)
d = a != b; seen = np.zeros_like(d)
print('silhouet: erbij', int(((b > 0) & (a == 0)).sum()), 'eraf', int(((a > 0) & (b == 0)).sum()), 'totaal', int((b > 0).sum()))
for n, z in Z.items():
    zz = z & ~seen; seen |= z
    pts = [(int(x), int(y)) for y, x in zip(*np.nonzero(d & zz))]
    print(f'{n}: {len(pts)} px', pts if 0 < len(pts) <= 10 else '')
print('rest:', [(int(x), int(y)) for y, x in zip(*np.nonzero(d & ~seen))])
print('breedte gele buik (a/g/y, x18-34) per rij: ronde 6b -> ronde 7')
for y in range(34, 53):
    def w(L):
        xs = [x for x in range(18, 35) if L[y, x] in 'agy']
        return f'{min(xs)}-{max(xs)} ({len(xs)})' if xs else '-'
    print(f'  {y}: {w(La)} -> {w(Lb)}')
