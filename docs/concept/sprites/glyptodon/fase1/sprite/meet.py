# Meten per spritepixel op het natieve model (S=0,6, fase 0, zelfde raster als reductie.py/vel.py).
# cellen(x, y) -> lijst (gewicht, rgb, klasse) van de natieve cellen onder spritepixel (x, y);
# klasse: 'bg' achtergrond, 'K' lijn (som<150), 'O' oogwit, anders 'V' (vulling).
import numpy as np
from collections import deque
D = __file__.rsplit('/', 1)[0]
S = 0.6; X0, Y0 = 10, 24
W, H = int(np.ceil(85 * S)), int(np.ceil(52 * S)); OX, OY = (64 - W) // 2, 64 - H - 4
n = np.load(D + '/nat.npy').astype(int); som = n.sum(2)
wit = som >= 720
buiten = np.zeros_like(wit); q = deque([(0, 0)]); buiten[0, 0] = True
while q:
    y, x = q.popleft()
    for yy, xx in ((y+1, x), (y-1, x), (y, x+1), (y, x-1)):
        if 0 <= yy < 100 and 0 <= xx < 100 and wit[yy, xx] and not buiten[yy, xx]:
            buiten[yy, xx] = True; q.append((yy, xx))

def _w(a0, a1):
    return [(c, min(a1, c + 1) - max(a0, c)) for c in range(int(np.floor(a0)), int(np.ceil(a1))) if min(a1, c + 1) - max(a0, c) > 1e-9]

def cellen(x, y):
    out = []
    for yy, a in _w(Y0 + (y - OY) / S, Y0 + (y + 1 - OY) / S):
        for xx, b in _w(X0 + (x - OX) / S, X0 + (x + 1 - OX) / S):
            if not (0 <= yy < 100 and 0 <= xx < 100) or buiten[yy, xx]: k = 'bg'
            elif wit[yy, xx]: k = 'O'
            elif som[yy, xx] < 150: k = 'K'
            else: k = 'V'
            out.append((a * b, n[yy, xx] if 0 <= yy < 100 and 0 <= xx < 100 else np.array([255, 255, 255]), k))
    return out

def meerderheid(x, y, pal, kandidaten):
    """paletindex (uit kandidaten) met het grootste gewicht onder de vulcellen; elke cel telt voor zijn dichtstbijzijnde kleur."""
    g = {}
    for w, c, k in cellen(x, y):
        if k != 'V': continue
        d = [((np.array(pal[i]) - c) ** 2).sum() for i in kandidaten]
        i = kandidaten[int(np.argmin(d))]; g[i] = g.get(i, 0) + w
    return max(g, key=g.get) if g else None, g

def licht(x, y, drempel):
    """aandeel (van de hele pixel) vulcellen met helderheid >= drempel"""
    c = cellen(x, y); tot = sum(w for w, _, _ in c)
    return sum(w for w, rgb, k in c if k == 'V' and rgb.sum() / 3 >= drempel) / tot
