"""Ronde 10: masker van Jordi's rode vormen (jordi_schets_ronde8_vormen.png) in spritecoördinaten.
Elke rode streep-groep (8-buren, schets-px) wordt dichtgetrokken tot zijn convexe omhulsel; een spritecel telt als
'binnen' als zijn middelpunt binnen het omhulsel ligt, daarna 1 px speling (schetsen). Vormen: links = kruis,
midden = de twee U-lussen samen, rechts = de lange lus + onderstreep. Schrijft masker_<vorm>.txt (rasters, '#' = binnen)."""
import os
import numpy as np
from overlay import rood
HERE = os.path.dirname(os.path.abspath(__file__))
def groepen():
    r = rood(); H, W = r.shape; lab = np.zeros(r.shape, int); n = 0
    for y0, x0 in zip(*np.nonzero(r)):
        if lab[y0, x0]: continue
        n += 1; st = [(y0, x0)]; lab[y0, x0] = n
        while st:
            y, x = st.pop()
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    q, p = y + dy, x + dx
                    if 0 <= q < H and 0 <= p < W and r[q, p] and not lab[q, p]: lab[q, p] = n; st.append((q, p))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) > 20: out.append(((xs + 9) / 10, (ys + 51) / 10))  # spritecoördinaten
    return out
def hull(pts):
    pts = sorted(set(pts))
    def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]
def binnen(h, x, y):
    n = len(h)
    return all((h[(i + 1) % n][0] - h[i][0]) * (y - h[i][1]) - (h[(i + 1) % n][1] - h[i][1]) * (x - h[i][0]) >= 0 for i in range(n))
def maskers():
    G = groepen(); vorm = {'links': [], 'midden': [], 'rechts': []}
    for xs, ys in G:
        cx = xs.mean()
        k = 'links' if cx < 18 else ('midden' if cx < 33 else 'rechts')
        vorm[k].append(list(zip(np.round(xs, 1), np.round(ys, 1))))
    M = {}
    for k, gs in vorm.items():
        m = np.zeros((64, 64), bool)
        for pts in ([sum(gs, [])] if k == 'midden' else gs):
            h = hull(pts)
            for y in range(64):
                for x in range(64):
                    if binnen(h, x + .5, y + .5): m[y, x] = True
        s = m.copy()  # 1 px speling
        s[1:] |= m[:-1]; s[:-1] |= m[1:]; s[:, 1:] |= m[:, :-1]; s[:, :-1] |= m[:, 1:]
        M[k] = s
    return M
if __name__ == '__main__':
    M = maskers()
    for k, m in M.items():
        ys, xs = np.nonzero(m); print(k, 'x%d-%d y%d-%d, %d cellen' % (xs.min(), xs.max(), ys.min(), ys.max(), m.sum()))
        open(os.path.join(HERE, 'masker_%s.txt' % k), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in m) + '\n')
