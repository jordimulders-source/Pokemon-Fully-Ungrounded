"""Ronde 13: diff per zone t.o.v. ronde 12; buiten de genoemde plekken moet het 0 zijn. Draaien vanuit de repo-root."""
import os
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(H)
a = np.array(Image.open(os.path.join(K, 'ronde12/sapa_inca.png'))); b = np.array(Image.open(os.path.join(H, 'sapa_inca.png')))
pa = Image.open(os.path.join(K, 'ronde12/sapa_inca.png')).getpalette()[:48]; pb = Image.open(os.path.join(H, 'sapa_inca.png')).getpalette()[:48]
print('palet identiek aan ronde 12:', pa == pb)
def box(x0, y0, x1, y1):
    m = np.zeros((64, 64), bool); m[y0:y1 + 1, x0:x1 + 1] = True; return m
Z = {'1 ogen en snavel (x23-31 y23-26)': box(23, 23, 31, 26), '2 flank (x29-35 y36-50)': box(29, 36, 35, 50),
     '3 romp linksboven (x21-27 y28-33)': box(21, 28, 27, 33), '4 stafpunt (x13-17 y18-21)': box(13, 18, 17, 21),
     '5 klont (15,46-47)': box(15, 46, 15, 47), '5 kroononderrand + drup (x40-46 y22-24)': box(40, 22, 46, 24),
     '5 hand (x12-20 y41-45)': box(12, 41, 20, 45)}
d = a != b; seen = np.zeros_like(d)
for n, z in Z.items():
    zz = z & ~seen; seen |= z
    print(f'{n}: {int((d & zz).sum())} px')
print('buiten de genoemde plekken:', int((d & ~seen).sum()), 'px', [(int(x), int(y)) for y, x in zip(*np.nonzero(d & ~seen))])
print('silhouet: erbij', int(((b > 0) & (a == 0)).sum()), 'eraf', int(((a > 0) & (b == 0)).sum()), 'totaal', int((b > 0).sum()))
k = (b == [i for i in range(16) if tuple(pb[i*3:i*3+3]) == (24, 16, 20)][0])
print('2x2-klonten zwart:', [(x, y) for y in range(63) for x in range(63) if k[y, x] and k[y, x+1] and k[y+1, x] and k[y+1, x+1]])
