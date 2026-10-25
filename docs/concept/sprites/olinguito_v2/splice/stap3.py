import numpy as np, sys
S = sys.argv[1]; sys.argv = sys.argv[:1] + [S]
exec(open(S + '/stap2.py').read().split('np.save')[0])   # g met kop
from common import show
# nekrand dichten tussen oor en rug
for (x, y) in [(15, 30)]: g[y, x] = 'L'
# staart: dikke curve, gestempeld en daarna als sprite ingekleurd
def bez(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    a = (1 - t) ** 3; b = 3 * (1 - t) ** 2 * t; c = 3 * (1 - t) * t * t; d = t ** 3
    return a * x0 + b * x1 + c * x2 + d * x3, a * y0 + b * y1 + c * y2 + d * y3
segs = [((44, 30), (49, 25), (53, 18), (52, 10)), ((52, 10), (51.5, 4), (45, 2.5), (44.5, 8))]
T = np.zeros((64, 64), bool)
for seg, (r0, r1) in zip(segs, ((2.4, 1.7), (1.7, 1.3))):
    for t in np.linspace(0, 1, 200):
        cx, cy = bez(seg, t); r = r0 + (r1 - r0) * t
        for y in range(64):
            for x in range(64):
                if (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2 <= r * r: T[y, x] = True
# alleen waar nu leeg (achter het lijf langs)
for y in range(64):
    for x in range(64):
        if T[y, x] and g[y, x] == '.':
            nb = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            edge = any(not (0 <= a < 64 and 0 <= b < 64) or not T[b, a] for a, b in nb)
            if edge:
                # licht van linksboven: omlijningsbasis links/boven, zwart rechts/onder
                lit = any((0 <= a < 64 and 0 <= b < 64) and not T[b, a] and (a < x or b < y) for a, b in nb)
                dark = any((0 <= a < 64 and 0 <= b < 64) and not T[b, a] and (a > x or b > y) for a, b in nb)
                g[y, x] = 'K' if dark and not lit else 'L'
            else:
                g[y, x] = 'B'
# hooglicht/schaduw binnen de staart: linker binnenrij licht, rechter schaduw
for y in range(64):
    for x in range(64):
        if T[y, x] and g[y, x] == 'B':
            if x - 1 >= 0 and g[y, x - 1] in ('L', 'K'): g[y, x] = 'H'
            elif x + 1 < 64 and g[y, x + 1] in ('L', 'K'): g[y, x] = 'S'
# achterlijf dichten: rechterrand van het lijf krijgt omlijning
for y in range(20, 50):
    xs = [x for x in range(40, 48) if g[y, x] not in ('.',)]
    if xs and not T[y, xs[-1]]:
        x = xs[-1]
        if g[y, x] not in ('K', 'L'): g[y, x] = 'K'
np.save(S + '/stap3.npy', g)
show(g, S + '/stap3.png'); show(g, S + '/stap3_1x.png', 1)
