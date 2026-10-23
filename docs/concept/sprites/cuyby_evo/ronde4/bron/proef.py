"""Proef: legt een blok (proef_blok.txt: eerste regel 'x0 y0', daarna rijen; '.' = laat staan, '_' = leeg maken)
over een raster (standaard ronde 4; argv[1] = ander raster, argv[2] = map voor blok en uitvoer) en rendert 12x (crop) + 1x/3x naast het origineel."""
import sys
from PIL import Image, ImageDraw
import os
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(HERE, '../..')) + '/'
SP = os.path.join(HERE, '') if len(sys.argv) < 3 else sys.argv[2]
pal = {}
for i, l in enumerate(open(R + 'ronde4/bron/palet.txt')):
    p = l.split('#')[0].split()
    if p:
        pal[p[0]] = tuple(map(int, p[1:4]))
src = sys.argv[1] if len(sys.argv) > 1 else R + 'ronde4/bron/raster_f1.txt'
g = [list(r) for r in open(src).read().split('\n')[:64]]
orig = [r[:] for r in g]
lines = open(SP + 'proef_blok.txt').read().split('\n')
x0, y0 = map(int, lines[0].split())
for dy, row in enumerate(lines[1:]):
    for dx, c in enumerate(row):
        if c == '.':
            continue
        g[y0 + dy][x0 + dx] = '.' if c == '_' else c
open(SP + 'proef_raster.txt', 'w').write('\n'.join(''.join(r) for r in g) + '\n')


def img(g, bg=(255, 255, 255)):
    im = Image.new('RGB', (64, 64), bg)
    im.putdata([bg if c == '.' else pal[c] for r in g for c in r])
    return im


W = Image.new('RGB', (56 * 12 + 20 + 400, 44 * 12), (230, 230, 235))
z = img(g).crop((2, 10, 58, 54)).resize((56 * 12, 44 * 12), Image.NEAREST)
d = ImageDraw.Draw(z)
for k in range(57):
    if (k + 2) % 5 == 0:
        d.line([(k * 12, 0), (k * 12, 528)], fill=(0, 0, 255) if (k + 2) % 10 == 0 else (160, 160, 255))
for k in range(45):
    if (k + 10) % 5 == 0:
        d.line([(0, k * 12), (672, k * 12)], fill=(0, 0, 255) if (k + 10) % 10 == 0 else (160, 160, 255))
W.paste(z, (0, 0))
W.paste(img(orig).resize((192, 192), Image.NEAREST), (690, 0))
W.paste(img(g).resize((192, 192), Image.NEAREST), (890, 0))
W.paste(img(orig), (690, 210)); W.paste(img(g), (770, 210))
W.paste(img(orig, (60, 70, 80)), (850, 210)); W.paste(img(g, (60, 70, 80)), (930, 210))
W.save(SP + 'proef.png')
