# Trainer-effect (Jordi, 25 nov): "de vorm wijkt in bepaalde lijnen af, dus dat een stuk hoofd opeens iets
# hoger zit, of een stuk arm iets lager". Verticale stroken (kolommen) van de sprite schuiven 1-3 px
# omhoog of omlaag; alleen bestaande pixels. Gebruik: IN OUT aantal seed
import sys, random; from PIL import Image; import numpy as np
IN, OUT, n, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
rnd = random.Random(seed)
a = np.asarray(Image.open(IN).convert('RGB')).copy(); H, W, _ = a.shape
wit = np.array([255, 255, 255], 'uint8')
xs = np.where((a.mean(2) < 235).any(0))[0]; xmin, xmax = xs.min(), xs.max()
gebruikt = set()
for _ in range(n):
    while True:
        w = rnd.choice((2, 3, 3, 4, 5)); x0 = rnd.randrange(xmin, xmax - w)
        if not any(x in gebruikt for x in range(x0 - 1, x0 + w + 1)): break
    gebruikt.update(range(x0, x0 + w))
    # alleen een deel van de kolom (een stuk hoofd of een stuk arm), niet de hele hoogte
    ys = np.where((a[:, x0:x0 + w].mean(2) < 235).any(1))[0]
    y0 = rnd.randrange(ys.min(), max(ys.min() + 1, ys.max() - 6)); y1 = min(H, y0 + rnd.randrange(6, 18))
    d = rnd.choice((-3, -2, -2, -1, 1, 2, 2, 3))
    stuk = a[y0:y1, x0:x0 + w].copy()
    a[y0:y1, x0:x0 + w] = wit
    t0, t1 = max(0, y0 + d), min(H, y1 + d)
    a[t0:t1, x0:x0 + w] = stuk[t0 - (y0 + d):t1 - (y0 + d)]
Image.fromarray(a).save(OUT)
