"""Ronde 6b: diff t.o.v. ronde 6 (zone x12-26 y42-53) en controle: geen stafpixel (t/y) onder rij 47 grenst aan transparant. Draaien vanuit de repo-root."""
import os
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(H)
a = np.array(Image.open(os.path.join(K, 'ronde6/sapa_inca.png'))); b = np.array(Image.open(os.path.join(H, 'sapa_inca.png')))
pal = [l.split()[1] for l in open(os.path.join(H, 'sapa_inca.txt')) if l.startswith('P ')]
C = np.vectorize(lambda v: '.' if v == 0 else pal[v - 1])
La, Lb = C(a), C(b)
zone = np.zeros((64, 64), bool); zone[42:54, 12:27] = True
d = a != b
print('binnen zone x12-26 y42-53:', int((d & zone).sum()), 'px; buiten:', int((d & ~zone).sum()), 'px')
print('silhouet: erbij', int(((b > 0) & (a == 0)).sum()), 'eraf', int(((a > 0) & (b == 0)).sum()), 'totaal', int((b > 0).sum()))
staf = [(x, y) for y in range(30, 64) for x in range(10, 26) if Lb[y, x] in 'ty' and y >= 46]
bad = []
for x, y in staf:
    if y > 47 and any(Lb[y + dy, x + dx] == '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
        bad.append((x, y))
print('stafpixels onder de vleugel:', staf)
print('stafpixels onder rij 47 naast transparant:', bad if bad else 'geen')
for (x, y) in staf:
    if y == max(s[1] for s in staf):
        print(f'  laatste rij ({x},{y}): rechts {Lb[y, x+1]}, onder {Lb[y+1, x]}')
for y in range(44, 54):
    print(y, ''.join(La[y, 12:27]), '->', ''.join(Lb[y, 12:27]))
