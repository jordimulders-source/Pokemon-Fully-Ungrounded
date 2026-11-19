# telt per zone hoeveel spritepixels afwijken van de kale reductie (onderlaag_idx) en waardoor (buitenlijn/ruis vs hand)
import numpy as np
o = np.load('onderlaag_idx.npy'); s2 = np.load('stap2_idx.npy'); f = np.load('lama_idx.npy'); H, W = f.shape
rand = np.zeros_like(f, bool)
for y in range(H):
    for x in range(W):
        if f[y, x] and any(not (0 <= x + dx < W and 0 <= y + dy < H) or f[y + dy, x + dx] == 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): rand[y, x] = True
def zone(x, y):
    if y < 20: return 'kop'
    if y < 36 and x < 27: return 'hals + halsband'
    if y < 50: return 'lijf + kleed'
    return 'voorpoten' if x < 29 else 'achterpoten'
T = {}
for y in range(H):
    for x in range(W):
        if not f[y, x]: continue
        z = zone(x, y); t = T.setdefault(z, [0, 0, 0, 0])
        t[0] += 1
        if s2[y, x] != o[y, x]: t[1 if rand[y, x] else 2] += 1
        if f[y, x] != s2[y, x]: t[3] += 1
print('%-16s %5s %9s %6s %5s' % ('zone', 'px', 'buitenlijn', 'ruis', 'hand'))
for z, t in T.items(): print('%-16s %5d %9d %6d %5d' % (z, *t))
print('totaal afwijkend', int((f != o).sum()), 'van', int((f > 0).sum()))
