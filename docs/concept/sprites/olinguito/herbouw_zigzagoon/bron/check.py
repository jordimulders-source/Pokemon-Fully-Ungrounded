#!/usr/bin/env python3
"""Controles: palet, transparency, open randen, formaat, rechte runs in de omtrek (>= 4 px)."""
import os
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); M = os.path.join(H, '..')
b = Image.open(os.path.join(M, 'anim_front.png'))
OUT = {1, 2, 9}
print('mode', b.mode, b.size, '| transparency', b.info.get('transparency'))
ref = open(os.path.join(M, '..', 'ronde23', 'normal.pal')).read() == open(os.path.join(M, 'normal.pal')).read()
print('normal.pal gelijk aan ronde 23:', ref)
for f in (0, 1):
    g = [[b.getpixel((x, y + 64 * f)) for x in range(64)] for y in range(64)]
    ob = []
    for y in range(64):
        for x in range(64):
            v = g[y][x]
            if v and v not in OUT:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    X, Y = x + dx, y + dy
                    if not (0 <= X < 64 and 0 <= Y < 64) or g[Y][X] == 0:
                        ob.append((x, y)); break
    px = [(x, y) for y in range(64) for x in range(64) if g[y][x]]
    xs = [p[0] for p in px]; ys = [p[1] for p in px]
    rand = {(x, y) for x, y in px if any(not (0 <= x + dx < 64 and 0 <= y + dy < 64) or g[y + dy][x + dx] == 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
    # rechte runs in de omtrek: horizontale/verticale rijen randpixels met transparant aan dezelfde kant
    runs = []
    for y in range(64):
        for side in (-1, 1):
            x = 0
            while x < 64:
                if (x, y) in rand and 0 <= y + side < 64 and g[y + side][x] == 0:
                    s = x
                    while x < 64 and (x, y) in rand and g[y + side][x] == 0: x += 1
                    if x - s >= 4: runs.append(('hor', y, s, x - 1, x - s))
                else: x += 1
    for x in range(64):
        for side in (-1, 1):
            y = 0
            while y < 64:
                if (x, y) in rand and 0 <= x + side < 64 and g[y][x + side] == 0:
                    s = y
                    while y < 64 and (x, y) in rand and g[y][x + side] == 0: y += 1
                    if y - s >= 4: runs.append(('ver', x, s, y - 1, y - s))
                else: y += 1
    print('frame %d: %d px, box %dx%d (x%d-%d, y%d-%d) | open randen %d %s' % (f + 1, len(px), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1, min(xs), max(xs), min(ys), max(ys), len(ob), ob))
    print('  rechte omtrekruns >= 4:', runs)
