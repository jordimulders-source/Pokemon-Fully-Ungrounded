"""Kleine hulpfuncties: met de hand getekende ASCII-stukken op een 64x64-raster zetten en wegschrijven."""
from PIL import Image


class Canvas:
    def __init__(self, keys):
        self.keys = keys  # dict teken -> index
        self.px = [[0] * 64 for _ in range(64)]

    def put(self, x0, y0, rows, keep='.'):
        for j, r in enumerate(rows):
            for i, ch in enumerate(r):
                if ch == keep or ch == ' ':
                    continue
                x, y = x0 + i, y0 + j
                if 0 <= x < 64 and 0 <= y < 64:
                    self.px[y][x] = 0 if ch == '_' else self.keys[ch]

    def copy(self):
        c = Canvas(self.keys)
        c.px = [r[:] for r in self.px]
        return c

    def area(self):
        return sum(1 for r in self.px for v in r if v)


def save(frames, pal, png, palpath):
    im = Image.new('P', (64, 64 * len(frames)))
    flat = []
    for c in pal:
        flat += list(c)
    flat += [0] * (768 - len(flat))
    im.putpalette(flat)
    for f, c in enumerate(frames):
        for y in range(64):
            for x in range(64):
                im.putpixel((x, y + 64 * f), c.px[y][x])
    im.save(png, transparency=0)
    with open(palpath, 'w', newline='\r\n') as fh:
        fh.write('JASC-PAL\n0100\n16\n')
        for c in pal:
            fh.write('%d %d %d\n' % c)


def ascii_dump(c):
    ch = '.123456789ABCDEF'
    return '\n'.join(''.join(ch[v] for v in r) for r in c.px)


def segs(c, items, dx=0, dy=0):
    """items: lijst (x, y, tekst) met absolute coördinaten."""
    for x, y, s in items:
        c.put(x + dx, y + dy, [s])
