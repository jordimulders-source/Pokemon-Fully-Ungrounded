# Vlakken (kaders) en meting: gemiddelde helderheid per vlak, sprite (paletkleur) tegen model (ML, mediaan zonder lijn), zonder lijnpixels.
import numpy as np
from PIL import Image
DF = np.load('sprite_v2_r5/DF.npy'); ML = np.load('sprite_v2_r5/ML.npy')
BRUIN = (3, 4, 5, 14); ROOM = (6, 7, 8); ROOD = (9, 10, 11, 12)
def kader(x0, x1, y0, y1, extra=None):
    m = np.zeros((64, 64), bool); m[y0:y1 + 1, x0:x1 + 1] = True
    if extra is not None: m &= extra
    return m
_rug = np.zeros((64, 64), bool); _rug[18:41, 36:57] = True; _rug[29:41, 36:44] = False
VLAKKEN = {
 'kopschild': (kader(8, 36, 9, 21), BRUIN), 'gezicht': (kader(11, 22, 22, 33), BRUIN),
 'schouderkoepel': (kader(32, 39, 29, 35), BRUIN), 'nabije arm': (kader(31, 43, 36, 45), BRUIN),
 'verre arm': (kader(9, 18, 40, 46), BRUIN), 'rug': (_rug, BRUIN), 'staart': (kader(46, 63, 36, 58), BRUIN),
 'dij nabij': (kader(33, 45, 46, 55), BRUIN), 'scheen nabij': (kader(35, 46, 56, 62), BRUIN),
 'dij ver': (kader(14, 24, 46, 54), BRUIN), 'scheen ver': (kader(14, 24, 55, 61), BRUIN),
 'buik': (kader(18, 34, 32, 53), ROOM), 'kaken': (kader(0, 30, 22, 42), ROOD),
}
def lum(c): return 0.299 * c[..., 0] + 0.587 * c[..., 1] + 0.114 * c[..., 2]
def meet(a, pal):
    Lp = lum(np.array(pal, float).reshape(-1, 3)); uit = {}
    for n, (m, idx) in VLAKKEN.items():
        k = m & np.isin(a, idx) & (DF >= 0) & (DF < 0.2)
        uit[n] = (int(k.sum()), round(float(Lp[a[k]].mean()), 1), round(float(ML[k].mean()), 1))
    return uit
