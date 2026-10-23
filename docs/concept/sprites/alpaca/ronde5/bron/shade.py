"""parts.txt -> geïndexeerd tekstraster (ascii_sprite-formaat, één frame) met volumeschaduw.
Gebruik: python3 shade.py parts.txt uit.txt [preview.png]"""
import sys, numpy as np
from PIL import Image

CH = '.123456789abcdef'
# laagvolgorde (achter -> voor) en tinten (hl, basis, schaduw, diep, selout)
PARTS = {
    'p': ('fur', (6, 6, 7, 7, 7), 0), 'k': ('hoof', (7, 7, 7, 15, 15), 0),
    'T': ('wool', (1, 2, 3, 3, 4), 1), 'W': ('wool', (1, 2, 3, 3, 4), 1),
    'P': ('fur', (5, 6, 7, 7, 7), 1), 'K': ('hoof', (6, 7, 7, 7, 7), 1),
    'l': ('fur', (6, 6, 7, 7, 7), 0), 'g': ('gold', (11, 12, 12, 12, 12), 0),
    'r': ('red', (9, 9, 10, 10, 10), 0),
    'N': ('wool', (1, 2, 3, 3, 4), 1), 'L': ('fur', (5, 6, 7, 7, 7), 1),
    'G': ('gold', (11, 11, 12, 12, 12), 1), 'R': ('red', (8, 9, 10, 10, 10), 1),
    'C': ('wool', (1, 2, 3, 3, 4), 1),
    'e': ('fur', (6, 6, 7, 7, 7), 0), 'q': ('red', (9, 9, 10, 10, 10), 0),
    'E': ('fur', (5, 6, 7, 7, 7), 1), 'F': ('fur', (5, 6, 7, 7, 7), 1),
    'M': ('fur', (5, 5, 6, 6, 7), 1), 'H': ('wool', (1, 2, 3, 3, 4), 1),
    'Q': ('red', (8, 9, 10, 10, 10), 1), 'X': ('band', (9, 9, 10, 10, 10), 1), 'B': ('wool', (1, 2, 3, 3, 4), 1),
}
ORDER = list(PARTS)
LIGHT = np.array([-0.55, -0.7, 0.55]); LIGHT /= np.linalg.norm(LIGHT)

g = np.array([list(l[:64].ljust(64, '.')) for l in open(sys.argv[1]).read().split('\n')[:64]])
H, W = g.shape
out = np.zeros((H, W), np.uint8)
for ch in ORDER:
    m = g == ch
    if not m.any():
        continue
    kind, (hl, base, sh, dp, sel), _n = PARTS[ch]
    ys, xs = np.nonzero(m)
    def march(x, y, dx, dy):
        k = 0
        while 0 <= x < W and 0 <= y < H and m[y, x]:
            x += dx; y += dy; k += 1
        return k
    tl = np.array([min(march(x, y, 0, -1), 1.5 * march(x, y, -1, -1), 2.2 * march(x, y, -1, 0)) for x, y in zip(xs, ys)])
    br = np.array([min(march(x, y, 0, 1), 1.5 * march(x, y, 1, 1), 2.2 * march(x, y, 1, 0)) for x, y in zip(xs, ys)])
    f = tl / (tl + br)
    th = tl + br
    t = np.where(f < 0.58, base, np.where(f < 0.9, sh, dp))
    t = np.where((f < 0.2) & (th > 5) & (tl <= 2.5), hl, t)
    out[ys, xs] = t
# omlijning: rand van het silhouet
sil = g != '.'
def nb(m, dx, dy):
    o = np.zeros_like(m)
    o[max(dy, 0):H + min(dy, 0), max(dx, 0):W + min(dx, 0)] = m[max(-dy, 0):H + min(-dy, 0), max(-dx, 0):W + min(-dx, 0)]
    return o  # o[y,x] = m[y-dy, x-dx]
rank = {c: i for i, c in enumerate(ORDER)}
rk = np.vectorize(lambda c: rank.get(c, -1))(g)
for y in range(H):
    for x in range(W):
        c = g[y, x]
        if c == '.':
            continue
        kind, tones, near = PARTS[c]
        sel = tones[4]
        up = y == 0 or g[y - 1, x] == '.'; left = x == 0 or g[y, x - 1] == '.'
        dn = y == H - 1 or g[y + 1, x] == '.'; right = x == W - 1 or g[y, x + 1] == '.'
        if up or left or dn or right:
            lit = (up or left) and not (dn or right)
            out[y, x] = sel if (lit and kind in ('wool', 'fur')) else 15
            continue
        # binnenrand: dit onderdeel ligt vóór een buur van een ander onderdeel
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            c2 = g[y + dy, x + dx]
            if c2 != c and c2 != '.' and rank[c2] < rank[c] and PARTS[c2][0] != kind:
                out[y, x] = 15
                break
            if c2 != c and c2 != '.' and rank[c2] < rank[c] and kind == 'wool' and dy >= 0 and dx >= 0:
                out[y, x] = 3
with open(sys.argv[2], 'w') as f:
    f.write('== frame 1\n')
    for r in out:
        f.write(''.join(CH[v] for v in r) + '\n')
