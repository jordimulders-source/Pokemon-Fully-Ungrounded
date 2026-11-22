# Controle: kleine tintvlakjes (<3 px, 4-buren) per index, losse buitenlijnpixels, kleuren
import sys; import numpy as np; from PIL import Image
a = np.asarray(Image.open(sys.argv[1] if len(sys.argv) > 1 else 'lama.png')).astype(int); H, W = a.shape
seen = np.zeros_like(a, bool); klein = []
for y in range(H):
    for x in range(W):
        if a[y, x] == 0 or seen[y, x]: continue
        v = a[y, x]; st = [(y, x)]; comp = []; seen[y, x] = True
        while st:
            p = st.pop(); comp.append(p)
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (p[0] + dy, p[1] + dx)
                if 0 <= q[0] < H and 0 <= q[1] < W and not seen[q] and a[q] == v: seen[q] = True; st.append(q)
        if len(comp) < 3: klein.append((v, comp))
print('kleuren', sorted(set(a.ravel()) - {0}), 'aantal', len(set(a.ravel())) - 1, 'px', (a > 0).sum())
for v, c in klein: print('klein vlakje index %d: %s' % (v, c))
