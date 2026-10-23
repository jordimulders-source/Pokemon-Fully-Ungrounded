"""compare.png: modeltekening concept A naast de sprite en echte Gen 3-sprites, op 3x en 1x.
Draaien vanuit de repo-root:
    python3 docs/concept/sprites/alpaca/ronde6/bron/compare.py
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'docs/concept/ontwerp/alpaca/scripts'))
from concepten import concept_a  # noqa: E402

G = os.path.join(REPO, 'graphics/pokemon')
OUT = os.path.join(HERE, '..')
BG = (152, 208, 136)


def font(sz, bold=False):
    n = 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/' + n, sz)


def frame(path, f=0):
    im = Image.open(path)
    pal = im.getpalette()
    px = im.load()
    out = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    for y in range(64):
        for x in range(64):
            i = px[x, 64 * f + y]
            if i:
                out.putpixel((x, y), tuple(pal[i * 3:i * 3 + 3]) + (255,))
    return out


def area(sp):
    return sum(1 for a in sp.split()[3].getdata() if a)


ours = os.path.join(OUT, 'anim_front.png')
items = [('alpaca r6 (frame 1)', frame(ours, 0)), ('alpaca r6 (frame 2)', frame(ours, 1)),
         ('Mareep (skelet wol)', frame(os.path.join(G, 'mareep/anim_front_gba.png'))),
         ('Growlithe (skelet 3/4)', frame(os.path.join(G, 'growlithe/anim_front_gba.png')))]
small = [('alpaca', frame(ours))] + [(n.capitalize(), frame(os.path.join(G, n, 'anim_front_gba.png')))
                                      for n in ['treecko', 'torchic', 'mudkip', 'mareep', 'growlithe', 'eevee', 'skitty']]

W = 256 + 24 + 4 * (192 + 16) + 16
H = 40 + 256 + 40 + 110
im = Image.new('RGB', (W, H), (255, 255, 255))
d = ImageDraw.Draw(im)
d.text((12, 10), 'Alpaca fase 1, ronde 6: modeltekening concept A -> Gen 3-sprite (3x en 1x)',
       fill=(40, 30, 40), font=font(16, True))
im.paste(concept_a().result(), (8, 40))
d.text((12, 300), 'modeltekening (concept A)', fill=(110, 100, 110), font=font(12))
x = 256 + 24
for lab, sp in items:
    bg = Image.new('RGB', (192, 192), BG)
    big = sp.resize((192, 192), Image.NEAREST)
    bg.paste(big, (0, 0), big)
    im.paste(bg, (x, 40 + 32))
    d.text((x, 40 + 32 + 196), lab, fill=(40, 30, 40), font=font(12, True))
    d.text((x, 40 + 32 + 212), '%d px' % area(sp), fill=(110, 100, 110), font=font(12))
    x += 192 + 16
y = 40 + 256 + 40
d.text((12, y), '1x op gevechtsgrond:', fill=(110, 100, 110), font=font(12))
x = 12
for lab, sp in small:
    bg = Image.new('RGB', (64, 64), BG)
    bg.paste(sp, (0, 0), sp)
    im.paste(bg, (x, y + 18))
    d.text((x, y + 86), lab, fill=(40, 30, 40), font=font(11))
    x += 76
im.save(os.path.join(OUT, 'compare.png'))
print('compare.png')
