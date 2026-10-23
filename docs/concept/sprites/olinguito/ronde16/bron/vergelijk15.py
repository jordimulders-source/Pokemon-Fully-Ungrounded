"""vergelijk15.py <repo-root>: maakt ronde15/compare.png: ronde 14 en 15 (beide frames) naast Poochyena
(referentie-skelet), bovenaan 3x, onderaan 1x."""
import sys
from PIL import Image, ImageDraw

R = sys.argv[1]
O = R + '/docs/concept/sprites/olinguito/'
BG = (152, 208, 160)


def frames(p, n=2):
    im = Image.open(p).convert('RGBA')
    uit = []
    for i in range(n):
        f = Image.new('RGBA', (64, 64), BG + (255,))
        c = im.crop((0, 64 * i, 64, 64 * i + 64))
        f.paste(c, (0, 0), c)
        uit.append(f.convert('RGB'))
    return uit


panelen = [('ronde 14 f1', frames(O + 'ronde14/anim_front.png')[0]),
           ('ronde 14 f2', frames(O + 'ronde14/anim_front.png')[1]),
           ('ronde 15 f1', frames(O + 'ronde15/anim_front.png')[0]),
           ('ronde 15 f2', frames(O + 'ronde15/anim_front.png')[1]),
           ('Poochyena (skelet)', frames(R + '/graphics/pokemon/poochyena/anim_front.png', 1)[0])]
S = 3
W = Image.new('RGB', (len(panelen) * (64 * S + 8) + 8, 64 * S + 64 + 36), (255, 255, 255))
d = ImageDraw.Draw(W)
for i, (t, p) in enumerate(panelen):
    x = 8 + i * (64 * S + 8)
    d.text((x, 4), t, fill=(0, 0, 0))
    W.paste(p.resize((64 * S, 64 * S), Image.NEAREST), (x, 18))
    W.paste(p, (x + 64, 64 * S + 28))
W.save(O + 'ronde15/compare.png')
