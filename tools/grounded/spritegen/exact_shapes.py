"""Kalibratie met exacte vormen: de figuurpixels van een echte sprite worden per deel ingedeeld (via de nagetrokken
curven als labels) en als pixelrand-polygonen in een spec gezet. Zo test de renderer alleen zijn regels.
Gebruik: exact_shapes.py spec.json soort uit.json"""
import json, sys
import numpy as np
from PIL import Image, ImageDraw

spec = json.load(open(sys.argv[1]))
im = Image.open(f'graphics/pokemon/{sys.argv[2]}/anim_front.png')
fig = np.array(im)[:64, :64] != 0
parts = sorted(spec['parts'], key=lambda p: p.get('z', 0))


def cat(pts, k=12):
    out = []; n = len(pts)
    for i in range(n):
        p0, p1, p2, p3 = (np.array(pts[(i + d) % n]) for d in (-1, 0, 1, 2))
        for j in range(k):
            t = j / k
            out.append(tuple(0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)))
    return out


labels = np.full((64, 64), -1)
masks = []
for i, p in enumerate(parts):
    m = Image.new('L', (640, 640)); ImageDraw.Draw(m).polygon([(x * 10, y * 10) for x, y in cat(p['pts'])], fill=1)
    a = np.array(m)[5::10, 5::10] > 0
    masks.append(a)
    labels[a] = i
# figuurpixels zonder label: dichtstbijzijnde label
ys, xs = np.nonzero(fig & (labels < 0))
lab_pts = np.argwhere(labels >= 0)
for y, x in zip(ys, xs):
    d = ((lab_pts - (y, x)) ** 2).sum(1)
    labels[y, x] = labels[tuple(lab_pts[d.argmin()])]
labels[~fig] = -1


def contour(mask):
    """Pixelrand-polygoon (grootste component) langs de pixelhoeken."""
    edges = {}
    H, W = mask.shape
    for y in range(H):
        for x in range(W):
            if not mask[y, x]:
                continue
            for (a, b), (dy, dx) in (((((x, y), (x + 1, y))), (-1, 0)), (((x + 1, y), (x + 1, y + 1)), (0, 1)),
                                     (((x + 1, y + 1), (x, y + 1)), (1, 0)), (((x, y + 1), (x, y)), (0, -1))):
                yy, xx = y + dy, x + dx
                if not (0 <= yy < H and 0 <= xx < W) or not mask[yy, xx]:
                    edges.setdefault(a, []).append(b)
    best = []
    used = set()
    for start in list(edges):
        if start in used:
            continue
        loop, cur = [], start
        while cur not in used:
            used.add(cur); loop.append(cur)
            nxt = [n for n in edges.get(cur, []) if n not in used]
            if not nxt:
                break
            cur = nxt[0]
        if len(loop) > len(best):
            best = loop
    return [[float(x), float(y)] for x, y in best]


new = []
for i, p in enumerate(parts):
    m = labels == i
    if not m.any():
        continue
    q = dict(p); q['pts'] = contour(m); q['poly'] = True
    new.append(q)
spec['parts'] = new
json.dump(spec, open(sys.argv[3], 'w'))
print('delen', len(new))
