"""Hulpfuncties ronde 7: met de hand getekende tekstrasters op een 64x64-doek leggen en wegschrijven.

Er zit hier bewust geen vormgereedschap of automatische schaduw/omlijning in: elk teken in een raster is een
pixel die met de hand is gekozen. '.' en ' ' = niets tekenen (onderliggende laag blijft), '_' = transparant maken.
"""
from PIL import Image


class Canvas:
    def __init__(self, keys):
        self.keys = keys
        self.px = [[0] * 64 for _ in range(64)]

    def put(self, x0, y0, rows):
        for j, r in enumerate(rows):
            for i, ch in enumerate(r):
                if ch in '. ':
                    continue
                x, y = x0 + i, y0 + j
                if 0 <= x < 64 and 0 <= y < 64:
                    self.px[y][x] = 0 if ch == '_' else self.keys[ch]

    def shifted(self, dx, dy):
        c = Canvas(self.keys)
        for y in range(64):
            for x in range(64):
                v = self.px[y][x]
                if v and 0 <= x + dx < 64 and 0 <= y + dy < 64:
                    c.px[y + dy][x + dx] = v
        return c

    def area(self):
        return sum(1 for r in self.px for v in r if v)

    def text(self):
        inv = {v: k for k, v in self.keys.items()}
        return '\n'.join(''.join(inv.get(v, '.') if v else '.' for v in r) for r in self.px)


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


def zoom(c, pal, path, sc=8, bg=(200, 210, 220)):
    im = Image.new('RGB', (64 * sc, 64 * sc), bg)
    for y in range(64):
        for x in range(64):
            v = c.px[y][x]
            if v:
                im.paste(pal[v], (x * sc, y * sc, x * sc + sc, y * sc + sc))
    im.save(path)
