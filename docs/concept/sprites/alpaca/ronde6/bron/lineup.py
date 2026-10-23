"""Blinde rij: de kandidaat tussen 12 echte Gen 3-sprites (frame 1), 2x en 1x, alleen nummers.
python3 lineup.py <kandidaat anim_front.png> <uit.png> <seed>"""
import sys
import random
from PIL import Image, ImageDraw

import os
G = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..', '..',
                                 'graphics', 'pokemon')) + '/'
REAL = ['treecko', 'torchic', 'mudkip', 'mareep', 'growlithe', 'zigzagoon', 'skitty',
        'electrike', 'poochyena', 'ponyta', 'eevee', 'teddiursa']
BG = (152, 208, 136)


def load(p):
    im = Image.open(p)
    px = im.load()
    pal = im.getpalette()
    out = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    for y in range(64):
        for x in range(64):
            i = px[x, y]
            if i:
                out.putpixel((x, y), tuple(pal[i * 3:i * 3 + 3]) + (255,))
    return out


cand, outp, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
items = [(G + n + '/anim_front_gba.png', n) for n in REAL] + [(cand, 'KANDIDAAT')]
random.seed(seed)
random.shuffle(items)
n = len(items)
cols = 7
sc = 2
cw = 64 * sc + 8
img = Image.new('RGB', (cols * cw + 8, 2 * (64 * sc + 22) + 2 * 74 + 20), BG)
d = ImageDraw.Draw(img)
for i, (p, nm) in enumerate(items):
    sp = load(p)
    x = 8 + (i % cols) * cw
    y = 8 + (i // cols) * (64 * sc + 22)
    img.paste(sp.resize((64 * sc, 64 * sc), Image.NEAREST), (x, y + 14), sp.resize((64 * sc, 64 * sc), Image.NEAREST))
    d.text((x + 2, y), str(i + 1), fill=(0, 0, 0))
    # 1x-rij onderaan
    x1 = 8 + (i % cols) * 72
    y1 = 2 * (64 * sc + 22) + 16 + (i // cols) * 74
    img.paste(sp, (x1, y1 + 10), sp)
    d.text((x1 + 2, y1), str(i + 1), fill=(0, 0, 0))
img.save(outp)
print(', '.join('%d=%s' % (i + 1, nm) for i, (p, nm) in enumerate(items)))
