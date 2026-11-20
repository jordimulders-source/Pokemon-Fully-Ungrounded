# blauw.py (module): tinten van vleugels/lijf/staart opnieuw uit de cel-shading van het model (onderlaag: licht/midden/schaduw),
# gladgestreken (modus 3x3, kleine vlekjes weg) en per vorm een lichte rand langs de buitencontour linksboven en een
# sikkel langs de buitencontour rechtsonder.
import numpy as np
from collections import Counter
from scipy import ndimage as nd
K = np.load('../s5/onderlaag.npy')
BL = (2, 3, 4)
def herkleur(B, uit):
    M = np.isin(B, BL)
    M[49:, :] = False                                   # poten: eigen afwerking
    M[:, :15] = False                                   # gezicht/snavel
    for x, y in uit: M[y, x] = False
    T = B.copy()
    for y, x in zip(*np.where(M)):
        T[y, x] = {1: 2, 2: 3, 3: 4}.get(int(K[y, x]), B[y, x])
    for _ in range(2):                                   # modus 3x3 binnen de blauwe pixels
        U = T.copy()
        for y, x in zip(*np.where(M)):
            c = Counter(int(T[y + b, x + a]) for a in (-1, 0, 1) for b in (-1, 0, 1)
                        if 0 <= y + b < 64 and 0 <= x + a < 64 and M[y + b, x + a])
            U[y, x] = max(c.items(), key=lambda kv: (kv[1], kv[0] == T[y, x]))[0]
        T = U
    for t in BL:                                         # vlekjes < 5 px -> meeste buurtint
        lab, n = nd.label((T == t) & M)
        for i in range(1, n + 1):
            pts = list(zip(*np.where(lab == i)))
            if len(pts) >= 5: continue
            c = Counter(int(T[y + b, x + a]) for y, x in pts for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))
                        if 0 <= y + b < 64 and 0 <= x + a < 64 and M[y + b, x + a] and T[y + b, x + a] != t)
            if c:
                for y, x in pts: T[y, x] = c.most_common(1)[0][0]
    # buitencontour: lucht direct (of achter 1 lijnpixel) linksboven -> een stap lichter; rechtsonder -> een stap donkerder
    def lucht(x, y, dx, dy):
        for k in (1, 2):
            xx, yy = x + k * dx, y + k * dy
            if not (0 <= xx < 64 and 0 <= yy < 64) or B[yy, xx] == 0: return True
            if B[yy, xx] != 1: return False
        return False
    def rand(x, y, dx, dy, lijn_telt):          # afstand (1/2) tot de rand van de vorm in richting (dx,dy), anders 9
        for k in (1, 2):
            xx, yy = x + k * dx, y + k * dy
            if not (0 <= xx < 64 and 0 <= yy < 64) or B[yy, xx] == 0: return k
            if B[yy, xx] == 1: return k if (lijn_telt or lucht(xx, yy, dx, dy)) else 9
        return 9
    R = T.copy()
    for y, x in zip(*np.where(M)):
        tl = min(rand(x, y, -1, 0, True), rand(x, y, 0, -1, False))     # links: ook de lijn naar de vorige vorm
        br = min(rand(x, y, 1, 0, False), rand(x, y, 0, 1, True))
        if tl == 1: R[y, x] = max(2, T[y, x] - 2)
        elif tl == 2: R[y, x] = max(2, T[y, x] - 1)
        elif br == 1: R[y, x] = min(4, T[y, x] + 1)
    out = B.copy(); out[M] = R[M]
    return out
