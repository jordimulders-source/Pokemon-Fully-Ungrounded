"""Wolkenlijf: binnenellips + bulten op de rand, met Gen 3-schaduw per bult.
cloud() -> (mask, idx) als 64x64 numpy-arrays."""
import numpy as np, math

S = 64
yy, xx = np.mgrid[0:S, 0:S].astype(float)

# (cx, cy, r) van de bulten, met de klok mee vanaf de schouder
BUMPS = [(31.0, 29.2, 3.2), (36.6, 27.9, 3.6), (42.3, 28.9, 3.4), (46.0, 32.4, 3.0),
         (46.2, 37.3, 3.0), (42.8, 40.2, 2.7), (34.6, 40.4, 2.7), (29.8, 39.6, 2.8)]
CORE = (37.4, 33.6, 9.0, 6.2)


def disk(cx, cy, r):
    return (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r


def cloud():
    cx, cy, rx, ry = CORE
    core = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1.0
    m = core.copy()
    for b in BUMPS:
        m |= disk(*b)
    idx = np.zeros((S, S), np.uint8)
    # basis: licht van linksboven, schaduw onder/rechts (afstand tot de rand)
    ys, xs = np.nonzero(m)

    def march(x, y, dx, dy):
        k = 0
        while 0 <= x < S and 0 <= y < S and m[y, x]:
            x += dx; y += dy; k += 1
        return k
    for x, y in zip(xs, ys):
        tl = min(march(x, y, 0, -1), 1.5 * march(x, y, -1, -1), 2.2 * march(x, y, -1, 0))
        br = min(march(x, y, 0, 1), 1.5 * march(x, y, 1, 1), 2.2 * march(x, y, 1, 0))
        f = tl / (tl + br)
        idx[y, x] = 2 if f < 0.55 else 3
    # per bult: hooglicht-sikkel linksboven, krullijn rechtsonder waar hij over het lijf ligt
    for i, (bx, by, r) in enumerate(BUMPS):
        d = np.sqrt((xx - bx) ** 2 + (yy - by) ** 2)
        ang = np.arctan2(yy - by, xx - bx)          # 0 = rechts, -pi/2 = boven
        upper = by < cy + 1
        if upper:
            hl = m & (d <= r - 0.6) & (d > r - 2.2) & (ang < -math.pi * 0.35) & (ang > -math.pi * 0.95)
            idx[hl & (idx == 2)] = 1
        # krullijn: alleen bij de bovenste bulten, kort, rechts van de bult over de volgende bult
        if upper and i + 1 < len(BUMPS) and BUMPS[i + 1][1] < cy + 1:
            nb = disk(*BUMPS[i + 1]) | core
            ring = (d > r - 1.0) & (d <= r) & nb & m & (ang > -math.pi * 0.25) & (ang < math.pi * 0.25)
            idx[ring] = np.where(idx[ring] >= 3, 4, 3)
    # omlijning
    up = np.zeros_like(m); up[1:] = m[:-1]
    dn = np.zeros_like(m); dn[:-1] = m[1:]
    lf = np.zeros_like(m); lf[:, 1:] = m[:, :-1]
    rt = np.zeros_like(m); rt[:, :-1] = m[:, 1:]
    edge = m & ~(up & dn & lf & rt)
    lit = m & (~up | ~lf) & dn & rt
    idx[edge] = 15
    idx[lit] = 4
    return m, idx


if __name__ == '__main__':
    m, idx = cloud()
    CH = '.123456789abcdef'
    for r in idx[22:50]:
        print(''.join(CH[v] for v in r[20:56]))
