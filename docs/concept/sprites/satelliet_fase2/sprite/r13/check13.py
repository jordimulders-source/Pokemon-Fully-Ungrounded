# Controle r13: tintvlakjes < 3 px (4-samenhangend) per kleur, nieuw t.o.v. r12; lichte pixels op de buitenrand; kleuren; silhouet
import numpy as np, sys
from PIL import Image
from scipy import ndimage as nd
def kleintjes(o):
    uit = set()
    for v in sorted(set(o.ravel()) - {0, 1}):
        lab, n = nd.label(o == v)
        for c in range(1, n + 1):
            ys, xs = np.where(lab == c)
            if len(ys) < 3: uit.add((int(v), tuple(sorted(zip(xs.tolist(), ys.tolist())))))
    return uit
a = np.array(Image.open(sys.argv[1])); b = np.array(Image.open(sys.argv[2]))
ka, kb = kleintjes(a), kleintjes(b)
print('kleuren (zonder transparant):', len(set(a.ravel()) - {0}), ' silhouet-diff:', ((a == 0) != (b == 0)).sum())
print('tintvlakjes < 3 px: %d (r12: %d); nieuw:' % (len(ka), len(kb)))
for v, p in sorted(ka - kb): print('   kleur %X %s' % (v, p))
print('verdwenen t.o.v. r12:', len(kb - ka))
rand = [(x, y, int(a[y, x])) for y in range(64) for x in range(64) if a[y, x] and any(
    0 <= y + dy < 64 and 0 <= x + dx < 64 and a[y + dy, x + dx] == 0 for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1))) and a[y, x] in (2, 3, 4, 15, 12)]
print('lichte pixels op de buitenrand (2/3/4/F/C):', rand)
