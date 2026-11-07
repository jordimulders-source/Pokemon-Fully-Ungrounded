"""Ronde 5b: diff t.o.v. ronde 5, binnen en buiten de reparatiezone x12-24 y40-53. Draaien vanuit de repo-root."""
import os
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(H)
a = np.array(Image.open(os.path.join(K, 'ronde5/sapa_inca.png'))); b = np.array(Image.open(os.path.join(H, 'sapa_inca.png')))
pal = [l.split()[1] for l in open(os.path.join(H, 'sapa_inca.txt')) if l.startswith('P ')]
C = lambda v: '.' if v == 0 else pal[v - 1]
zone = np.zeros((64, 64), bool); zone[40:54, 12:25] = True
d = a != b
print('alpha-diff:', int(((a > 0) != (b > 0)).sum()))
print('binnen zone x12-24 y40-53:', int((d & zone).sum()), 'px; buiten:', int((d & ~zone).sum()), 'px')
k = lambda g: int(sum(C(v) == 'K' for v in g[42:53, 17:24].ravel()))
print('K-pixels in x17-23 y42-52: ronde 5', k(a), '-> ronde 5b', k(b))
for y in range(44, 53):
    print(y, ''.join(C(v) for v in a[y, 14:25]), '->', ''.join(C(v) for v in b[y, 14:25]))
