"""Ronde 8: diff t.o.v. ronde 7b; hoeveel kroonpixels (incl. kwastje) de zon bedekt. Draaien vanuit de repo-root."""
import os
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(H)
a = np.array(Image.open(os.path.join(K, 'ronde7b/sapa_inca.png'))); b = np.array(Image.open(os.path.join(H, 'sapa_inca.png')))
lab = [l[3:].ljust(64, '.') for l in open(os.path.join(K, 'ronde1/labels.txt')).read().split('\n')[:64]]
kroon = np.array([[c in 'FP' for c in r] for r in lab]); kroon[19:23, 22:33] = False
kroon &= a > 0
d = a != b
top = np.zeros((64, 64), bool); top[20:30, 11:20] = True
print('totaal gewijzigd:', int(d.sum()), 'px; binnen stafkop-zone x11-19 y20-29:', int((d & top).sum()), '; erbuiten:', int((d & ~top).sum()))
print('kroonpixels (incl. kwastje) bedekt door zon/omlijning:', int((d & kroon).sum()), [(int(x), int(y)) for y, x in zip(*np.nonzero(d & kroon))])
print('silhouet: erbij', int(((b > 0) & (a == 0)).sum()), 'eraf', int(((a > 0) & (b == 0)).sum()), 'totaal', int((b > 0).sum()))
ys, xs = np.nonzero(d & top & np.isin(b, [10, 11, 12]))
print('zonneschijf (goud a/g/y) bbox: x', xs.min(), '-', xs.max(), 'y', ys.min(), '-', ys.max())
