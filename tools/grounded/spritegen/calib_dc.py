"""Kalibratie op het voorbeeld uit de Dragonfly Cave-gids: Sugimori-tekening -> onze pixel-over,
naast de pixel-over uit de gids (zelfde maat). Gebruik: calib_dc.py tekening.png gids_pixelover.png k uit.png"""
import sys
import numpy as np
from PIL import Image
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from pixelover import pixelover

art = np.array(Image.open(sys.argv[1]).convert('RGB')).astype(float)
ref = Image.open(sys.argv[2]).convert('RGB')
k = int(sys.argv[3])
R, G, B = art[..., 0], art[..., 1], art[..., 2]
luma = 0.3 * R + 0.59 * G + 0.11 * B
mx, mn = art.max(2), art.min(2)
sat = (mx - mn) / np.maximum(mx, 1)
fig = (R > B + 8) | (luma < 120)
# grootste component, gaten dicht
from collections import deque
H, W = fig.shape
lab = np.zeros((H, W), int); best = (0, 0)
cur = 0
for y in range(0, H, 3):
    for x in range(0, W, 3):
        if fig[y, x] and not lab[y, x]:
            cur += 1; q = deque([(y, x)]); lab[y, x] = cur; n = 0
            while q:
                cy, cx = q.popleft(); n += 1
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    yy, xx = cy + dy, cx + dx
                    if 0 <= yy < H and 0 <= xx < W and fig[yy, xx] and not lab[yy, xx]:
                        lab[yy, xx] = cur; q.append((yy, xx))
            if n > best[0]:
                best = (n, cur)
fig = lab == best[1]
bg = np.zeros((H, W), bool); q = deque([(0, 0)]); bg[0, 0] = True
while q:
    cy, cx = q.popleft()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        yy, xx = cy + dy, cx + dx
        if 0 <= yy < H and 0 <= xx < W and not fig[yy, xx] and not bg[yy, xx]:
            bg[yy, xx] = True; q.append((yy, xx))
fig = ~bg
line = fig & (luma < np.percentile(luma[fig], 9)) & (sat < 0.55)
# materialen: k-means op kleur (genormaliseerd naar helderheid) van niet-lijnpixels
px = art[fig & ~line]
chrom = px / np.maximum(px.sum(1, keepdims=True), 1)
rng = np.random.default_rng(0)
cent = chrom[rng.choice(len(chrom), k, replace=False)]
for _ in range(25):
    d = ((chrom[:, None] - cent[None]) ** 2).sum(2); a = d.argmin(1)
    cent = np.array([chrom[a == i].mean(0) if (a == i).any() else cent[i] for i in range(k)])
allchrom = art / np.maximum(art.sum(2, keepdims=True), 1)
mat = ((allchrom[..., None, :] - cent[None, None]) ** 2).sum(3).argmin(2)
mat[~fig] = -1
tone = luma / 255.0
names = {i: f'm{i}' for i in range(k)}
palette = {'K': (16, 16, 16)}
for i in range(k):
    sel = (mat == i) & ~line
    base = np.median(art[sel], 0)
    lit = np.percentile(art[sel], 85, axis=0)
    dark = np.percentile(art[sel], 20, axis=0)
    palette[f'm{i}h'] = tuple(np.clip(lit * 1.05, 0, 255).astype(int))
    palette[f'm{i}b'] = tuple(base.astype(int))
    palette[f'm{i}s'] = tuple((dark * 0.85).astype(int))
    palette[f'm{i}l'] = tuple((dark * 0.45).astype(int))
out, info = pixelover(art, fig, line, mat, tone, ref.size[0], ref.size[1], dict(materials=names, style={}))
h, w = out.shape
img = np.full((h, w, 3), 245, np.uint8)
for y in range(h):
    for x in range(w):
        if out[y, x]:
            img[y, x] = palette[out[y, x]]
mine = Image.fromarray(img)
S = 6
canvas = Image.new('RGB', (w * S + ref.size[0] * S + 20, max(h, ref.size[1]) * S), (245, 245, 245))
canvas.paste(mine.resize((w * S, h * S), Image.NEAREST), (0, 0))
canvas.paste(ref.resize((ref.size[0] * S, ref.size[1] * S), Image.NEAREST), (w * S + 20, 0))
canvas.save(sys.argv[4])
print('maat', w, h, 'lijnpixels', int(info['line'].sum()))
