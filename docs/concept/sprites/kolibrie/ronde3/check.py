import sys, numpy as np
from PIL import Image
import teken
im = np.array(teken.build()); s = np.array(Image.open('../silhouet/silhouet_v6_groot_1x.png'))[:, :, 3] > 0
m = im > 0
add = np.argwhere(m & ~s); rem = np.argwhere(s & ~m)
def far(pts, ref):
    out = []
    for y, x in pts:
        if not ref[max(0, y-1):y+2, max(0, x-1):x+2].any(): out.append((int(x), int(y)))
    return out
print('px', m.sum(), 'sil', s.sum(), 'erbij', len(add), 'eraf', len(rem))
print('erbij >1px:', far(add, s)); print('eraf >1px:', far(rem, m))
if '-v' in sys.argv:
    print('erbij', [(int(x), int(y)) for y, x in add]); print('eraf', [(int(x), int(y)) for y, x in rem])
