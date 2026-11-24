# per band: radiale minimum-positie in het model per hoek (alleen echt donkere pixels), daarna cirkelfit
import numpy as np
from PIL import Image
M = np.array(Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB')).astype(float); k = 12.703
L = M @ [0.299, 0.587, 0.114]
cx, cy = 18.5, 34.9
def sm(x, y): return L[int(round(143 + (y - 7) * k)), int(round(103 + x * k))], M[int(round(143 + (y - 7) * k)), int(round(103 + x * k))]
BANDS = {'irisrand': (2.3, 4.0, 70), 'lensring': (4.8, 7.2, 45), 'ring85': (7.3, 9.6, 140), 'voorvlakrand': (9.6, 12.2, 45), 'buiten': (12.2, 14.5, 40)}
res = {}
for n, (r0, r1, thr) in BANDS.items():
    pts = []
    for ang in range(0, 360, 5):
        t = np.radians(ang); dx, dy = np.cos(t), -np.sin(t)
        rs = np.arange(r0, r1, 0.05); v = np.array([sm(cx + r * dx, cy + r * dy)[0] for r in rs])
        i = v.argmin()
        if v[i] < thr and 0 < i < len(rs) - 1:
            c = sm(cx + rs[i] * dx, cy + rs[i] * dy)[1]
            pts.append((ang, rs[i], v[i], c))
    res[n] = pts
    P = np.array([(cx + r * np.cos(np.radians(a)), cy - r * np.sin(np.radians(a))) for a, r, _, _ in pts])
    A = np.c_[2 * P, np.ones(len(P))]; b = (P ** 2).sum(1); s = np.linalg.lstsq(A, b, rcond=None)[0]
    R = np.sqrt(s[2] + s[0] ** 2 + s[1] ** 2)
    print('%-13s n=%2d fit midden (%.2f, %.2f) r=%.2f' % (n, len(P), s[0], s[1], R))
    print('   ' + ' '.join('%d:%.1f' % (a, r) for a, r, _, _ in pts))
