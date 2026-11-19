# controle: losse donkere lijnpixels (1) zonder buur aan de rand/lijn, kleine tintvlakjes (<3 px) per kleur, kleurtelling
import sys, numpy as np
from collections import Counter
a = np.load(sys.argv[1] if len(sys.argv) > 1 else 'stap4.npy'); H, W = a.shape
def g(x, y): return a[y, x] if 0 <= x < W and 0 <= y < H else 0
N8 = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]
los = [(x, y) for y in range(H) for x in range(W) if a[y, x] == 1 and not any(g(x + dx, y + dy) in (0, 1, 2, 3, 9) for dx, dy in N8)]
print('losse 1 zonder rand/lijn-buur:', los)
seen = np.zeros_like(a, bool); klein = Counter()
for y in range(H):
    for x in range(W):
        if a[y, x] == 0 or seen[y, x]: continue
        v = a[y, x]; st = [(x, y)]; seen[y, x] = True; n = 0
        while st:
            cx, cy = st.pop(); n += 1
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < W and 0 <= ny < H and not seen[ny, nx] and a[ny, nx] == v:
                    seen[ny, nx] = True; st.append((nx, ny))
        if n < 3: klein[v] += 1
print('vlakjes < 3 px per index:', dict(sorted(klein.items())))
ys, xs = np.nonzero(a); print('box %dx%d (x %d-%d, y %d-%d), %d px, %d kleuren + transparant' % (xs.max() - xs.min() + 1, ys.max() - ys.min() + 1, xs.min(), xs.max(), ys.min(), ys.max(), (a > 0).sum(), len(np.unique(a[a > 0]))))
