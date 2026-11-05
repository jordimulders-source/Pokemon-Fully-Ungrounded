"""Controle: losse pixels, 1-px slierten (pixel met <=1 vulbuur in 4-buurt), 1-px spleten (leeg tussen twee vol, horizontaal/verticaal, met leeg erboven/eronder dat geen gat is)."""
import os, numpy as np
from scipy import ndimage
D = os.path.dirname(os.path.abspath(__file__))
g = np.array([[c == '#' for c in r] for r in open(os.path.join(D, 'silhouet.txt')).read().split()])
print('afmeting', g.shape, 'px', g.sum())
lab, n = ndimage.label(g); print('delen', n)
gaten = ndimage.binary_fill_holes(g) & ~g; print('gaten', gaten.sum())
p = np.pad(g, 1)
for y in range(64):
    for x in range(64):
        if g[y, x]:
            nb = int(p[y, x+1]) + int(p[y+2, x+1]) + int(p[y+1, x]) + int(p[y+1, x+2])
            if nb <= 1: print('uitsteeksel 1px', x, y, 'buren', nb)
        else:
            if p[y+1, x] and p[y+1, x+2]: print('h-spleet 1px', x, y)
            if p[y, x+1] and p[y+2, x+1]: print('v-spleet 1px', x, y)
