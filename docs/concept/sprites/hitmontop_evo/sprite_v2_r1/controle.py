# Anatomie-/netheidscontrole: samenhang, marge, palet, kleine tintclusters (<3 px), lichte pixels op de buitenrand.
import numpy as np
from PIL import Image
from scipy import ndimage as nd
im = Image.open('sprite.png'); a = np.array(im)
print('modus', im.mode, 'grootte', im.size, 'kleuren gebruikt', len(np.unique(a)), 'paletlengte', len(im.getpalette())//3)
m = a > 0
lab, n = nd.label(m, structure=np.ones((3,3)))
print('samenhangende delen (8-buren):', n, [int((lab==i).sum()) for i in range(1, n+1)])
ys, xs = np.nonzero(m)
print('bbox x', xs.min(), xs.max(), 'y', ys.min(), ys.max(), '(marge >=1:', xs.min()>=1 and ys.min()>=1 and xs.max()<=62 and ys.max()<=62, ')')
NAMEN = '. W L S D o b B N n r R g G h K'.split()
klein = []
for c in np.unique(a):
    if c in (0, 15, 1): continue
    l, k = nd.label(a == c, structure=np.ones((3,3)))
    for i in range(1, k+1):
        z = np.argwhere(l == i)
        if len(z) < 3:
            klein.append((NAMEN[c], [(int(x), int(y)) for y, x in z]))
print('tintclusters < 3 px (x,y):', len(klein))
for k in klein: print('  ', k)
# lichte kleur op de buitenrand
buiten = m & ~nd.binary_erosion(m)
licht = [(int(x), int(y), NAMEN[a[y, x]]) for y, x in np.argwhere(buiten) if a[y, x] in (1, 2, 6, 12)]
print('lichte pixels op de buitenrand:', licht)
