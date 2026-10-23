"""Ronde 7: zet een handgetekend tekstraster om naar een Gen 3-frontsprite.

Gebruik (vanuit de repo-root):
    python3 render.py sprite.txt uitmap

sprite.txt:
  - kopregels 'TEKEN RRGGBB beschrijving', in paletvolgorde (eerste = index 0, transparant);
  - een regel 'FRAME2 <rij>': frame 2 = rij <rij> weglaten en alles erboven 1 px laten zakken
    (inademen/hurken; de pixels zelf blijven handwerk, er wordt niets getekend);
  - een lege regel, dan het raster (elk teken is één pixel).
Schrijft uitmap/anim_front.png (64x128, 4bpp geïndexeerd, index 0 transparant) en uitmap/normal.pal (JASC).
Het script tekent niets: geen vormen, geen schaduw, geen omlijning.
"""
import os
import sys
from PIL import Image


def load(path):
    lines = open(path).read().split('\n')
    pal, order, frame2, i = {}, [], None, 0
    while lines[i].strip():
        parts = lines[i].split()
        if parts[0] == 'FRAME2':
            frame2 = int(parts[1])
        else:
            pal[parts[0]] = tuple(int(parts[1][j:j + 2], 16) for j in (0, 2, 4))
            order.append(parts[0])
        i += 1
    rows = [l.rstrip('\n') for l in lines[i + 1:] if l.strip()]
    w = max(len(r) for r in rows)
    rows = [r.ljust(w, order[0]) for r in rows]
    return pal, order, frame2, rows


def place(rows, order):
    h, w = len(rows), len(rows[0])
    assert w <= 64 and h <= 64, (w, h)
    ox, oy = (64 - w) // 2, 64 - h - (64 - h) // 2
    idx = {c: n for n, c in enumerate(order)}
    px = [[0] * 64 for _ in range(64)]
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            px[oy + y][ox + x] = idx[c]
    return px


def main():
    src, out = sys.argv[1], sys.argv[2]
    pal, order, frame2, rows = load(src)
    assert len(order) <= 16
    f1 = rows
    if frame2 is not None:
        f2 = [order[0] * len(rows[0])] + rows[:frame2] + rows[frame2 + 1:]
    else:
        f2 = rows
    a, b = place(f1, order), place(f2, order)
    im = Image.new('P', (64, 128))
    flat = []
    for n in range(16):
        flat += list(pal[order[n]]) if n < len(order) else [0, 0, 0]
    im.putpalette(flat)
    im.putdata([v for r in a + b for v in r])
    os.makedirs(out, exist_ok=True)
    im.save(os.path.join(out, 'anim_front.png'), transparency=0, bits=4)
    with open(os.path.join(out, 'normal.pal'), 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for n in range(16):
            c = pal[order[n]] if n < len(order) else (0, 0, 0)
            f.write('%d %d %d\n' % c)
    opaque = sum(c != order[0] for r in f1 for c in r)
    print('raster %dx%d, oppervlak %d px, %d kleuren' % (len(rows[0]), len(rows), opaque, len(order)))


if __name__ == '__main__':
    main()
