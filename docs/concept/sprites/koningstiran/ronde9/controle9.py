"""Ronde 9: diff per zone t.o.v. ronde 8 voor elke variant + aantal vlekken per boog. Draaien vanuit de repo-root."""
import os
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(H)
a = np.array(Image.open(os.path.join(K, 'ronde8/sapa_inca.png')))
lab = [l[3:].ljust(64, '.') for l in open(os.path.join(K, 'ronde1/labels.txt')).read().split('\n')[:64]]
def box(x0, y0, x1, y1):
    m = np.zeros((64, 64), bool); m[y0:y1 + 1, x0:x1 + 1] = True; return m
stafkop = box(11, 19, 19, 27)
kroon = np.array([[c in 'FP' for c in r] for r in lab]); kroon[19:23, 22:33] = False; kroon &= ~stafkop
gezicht = box(22, 19, 33, 28)
for n in ('v1_een_boog_zwarte_rand', 'v2_twee_bogen_gouden_rand', 'v3_een_boog_gouden_rand'):
    b = np.array(Image.open(os.path.join(H, n + '.png')))
    d = a != b
    rest = d & ~kroon & ~stafkop
    print(n)
    print('  kroon:', int((d & kroon).sum()), 'px | stafkop (x11-19 y19-27):', int((d & stafkop).sum()), 'px | gezicht:', int((d & gezicht).sum()),
          'px | rest (lijf, staf eronder, vleugels, poten):', int(rest.sum()), 'px', [(int(x), int(y)) for y, x in zip(*np.nonzero(rest))][:8])
    print('  silhouet: erbij', int(((b > 0) & (a == 0)).sum()), 'eraf', int(((a > 0) & (b == 0)).sum()))
    pal = [l.split()[1] for l in open(os.path.join(H, n + '.txt')) if l.startswith('P ')]
    K_old = sum(1 for y in range(1, 22) for x in range(9, 49) if kroon[y, x] and a[y, x] and pal[a[y, x] - 1] == 'K')
    K_new = sum(1 for y in range(1, 22) for x in range(9, 49) if kroon[y, x] and b[y, x] and pal[b[y, x] - 1] == 'K')
    print('  zwarte pixels in de kroon: ronde 8', K_old, '->', K_new)
