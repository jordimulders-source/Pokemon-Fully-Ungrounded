"""Hulpmiddelen finale olinguito: raster <-> png, renders, metingen. Tekenen gebeurt met de hand in de rasters (r*.txt)."""
from PIL import Image, ImageDraw
import os
H = os.path.dirname(os.path.abspath(__file__))
OL = os.path.join(H, '..', '..')
PAL = [tuple(map(int, l.split())) for l in open(os.path.join(OL, 'ronde23', 'normal.pal')).read().split('\n')[3:19]]
def read_png(p, frame=0):
    im = Image.open(p); px = im.load()
    return [[px[x, y + 64 * frame] for x in range(64)] for y in range(64)]
def to_txt(g):
    return '\n'.join(''.join('.' if v == 0 else '%x' % v for v in row) for row in g) + '\n'
def read_txt(p):
    rows = [l.rstrip('\n') for l in open(p) if not l.startswith('#')]
    rows = [r for r in rows if r != '' or False][:64]
    assert len(rows) == 64, len(rows)
    for r in rows: assert len(r) == 64, (len(r), r)
    return [[0 if c == '.' else int(c, 16) for c in r] for r in rows]
def save_png(frames, p):
    im = Image.new('P', (64, 64 * len(frames)))
    flat = []
    for c in PAL: flat += list(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    px = im.load()
    for f, g in enumerate(frames):
        for y in range(64):
            for x in range(64): px[x, y + 64 * f] = g[y][x]
    im.save(p, transparency=0)
def rgba(g, bg=None):
    im = Image.new('RGBA', (64, 64), bg or (0, 0, 0, 0)); px = im.load()
    for y in range(64):
        for x in range(64):
            if g[y][x]: px[x, y] = PAL[g[y][x]] + (255,)
    return im
def zoomgrid(g, s, box=None, out=None):
    x0, y0, x1, y1 = box or (0, 0, 64, 64)
    im = rgba(g, (200, 215, 200, 255)).crop((x0, y0, x1, y1)).resize(((x1 - x0) * s, (y1 - y0) * s), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for x in range(x0, x1):
        if x % 5 == 0:
            d.line([((x - x0) * s, 0), ((x - x0) * s, im.size[1])], fill=(255, 0, 255) if x % 10 == 0 else (150, 150, 255))
    for y in range(y0, y1):
        if y % 5 == 0:
            d.line([(0, (y - y0) * s), (im.size[0], (y - y0) * s)], fill=(255, 0, 255) if y % 10 == 0 else (150, 150, 255))
    for x in range(x0, x1):
        if x % 5 == 0: d.text(((x - x0) * s + 2, 2), str(x), fill=(0, 0, 0))
    for y in range(y0, y1):
        if y % 5 == 0: d.text((2, (y - y0) * s + 2), str(y), fill=(0, 0, 0))
    if out: im.save(out)
    return im
def dump(g, y0=0, y1=64):
    print('    ' + ''.join(str(x // 10) for x in range(64)))
    print('    ' + ''.join(str(x % 10) for x in range(64)))
    for y in range(y0, y1):
        r = ''.join('.' if v == 0 else '%x' % v for v in g[y])
        if r.strip('.'): print('%3d ' % y + r)
