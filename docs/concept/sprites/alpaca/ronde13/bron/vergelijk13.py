"""compare.png voor ronde 13: ronde 11, ronde 12 en ronde 13 (frame 1 en 2), op wit, gevechtsgrond en donker; 1x en 3x.
Gebruik (vanuit de repo-root): python3 docs/concept/sprites/alpaca/ronde13/bron/vergelijk13.py [uit.png]"""
import os
import sys
from PIL import Image, ImageDraw

R = 'docs/concept/sprites/alpaca/'
UIT = sys.argv[1] if len(sys.argv) > 1 else R + 'ronde13/compare.png'
ACHTERGRONDEN = [('wit', (255, 255, 255)), ('gevechtsgrond', (232, 224, 176)), ('donker', (40, 40, 52))]


def sprite(p, frame, bg):
    im = Image.open(p)
    d = im.crop((0, 64 * frame, 64, 64 * frame + 64))
    rgb = d.convert('RGB'); px = d.load(); rp = rgb.load()
    for y in range(64):
        for x in range(64):
            if px[x, y] == 0:
                rp[x, y] = bg
    return rgb


def pk(n):
    p = 'graphics/pokemon/%s/anim_front_gba.png' % n
    return p if os.path.exists(p) else 'graphics/pokemon/%s/anim_front.png' % n


items = [('ronde 11', R + 'ronde11/anim_front.png', 0), ('ronde 12', R + 'ronde12/anim_front.png', 0),
         ('ronde 13', R + 'ronde13/anim_front.png', 0), ('ronde 13 frame 2', R + 'ronde13/anim_front.png', 1),
         ('Torchic', pk('torchic'), 0)]
n = len(items)
rij = 18 + 66 + 196
out = Image.new('RGB', (n * 200 + 10, 10 + rij * len(ACHTERGRONDEN)), (255, 255, 255))
d = ImageDraw.Draw(out)
for j, (bnaam, bg) in enumerate(ACHTERGRONDEN):
    y0 = 6 + j * rij
    d.rectangle([0, y0, out.width, y0 + rij - 4], fill=bg)
    tc = (230, 230, 230) if sum(bg) < 300 else (0, 0, 0)
    for i, (naam, p, f) in enumerate(items):
        x = 10 + i * 200
        im = sprite(p, f, bg)
        d.text((x, y0 + 2), '%s (%s)' % (naam, bnaam), fill=tc)
        out.paste(im, (x, y0 + 16))
        out.paste(im.resize((192, 192), Image.NEAREST), (x, y0 + 82))
out.save(UIT)
