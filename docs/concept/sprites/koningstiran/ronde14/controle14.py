"""Ronde 14: diff per zone t.o.v. ronde 13 (0 buiten de zones), palet, losse pixels. Draaien vanuit de repo-root."""
import os
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(H)
A = Image.open(os.path.join(K, 'ronde13/sapa_inca.png')); B = Image.open(os.path.join(H, 'sapa_inca.png'))
a, b = np.array(A), np.array(B)
print('palet identiek aan ronde 13:', A.getpalette()[:48] == B.getpalette()[:48])
def box(x0, y0, x1, y1):
    m = np.zeros((64, 64), bool); m[y0:y1 + 1, x0:x1 + 1] = True; return m
Z = {'1 overgang staf/lijf (x14-21 y46-50)': box(14, 46, 21, 50), '2 stafpunt (x12-17 y15-22)': box(12, 15, 17, 22),
     '3 poten + ruimte ertussen (x20-35 y53-62)': box(20, 53, 35, 62), '4 verre oog (x22-25 y22-26)': box(22, 22, 25, 26),
     '5 paarse pixels (x40-50 y18-34)': box(40, 18, 50, 34), '6 los rood naast nabije oog (31,25)': box(31, 25, 31, 25)}
d = a != b; seen = np.zeros_like(d)
for n, z in Z.items():
    zz = z & ~seen; seen |= z
    print(f'{n}: {int((d & zz).sum())} px')
print('buiten de zones:', int((d & ~seen).sum()), 'px')
print('silhouet: erbij', int(((b > 0) & (a == 0)).sum()), 'eraf', int(((a > 0) & (b == 0)).sum()), 'totaal', int((b > 0).sum()))
