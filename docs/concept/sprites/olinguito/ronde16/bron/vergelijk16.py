"""vergelijk16.py <repo-root>: maakt ronde16/compare.png: ronde 15 en 16 (beide frames) naast drie Dark-types
(Poochyena, Sneasel, Umbreon); bovenaan 3x, onderaan 1x op licht en donker."""
import sys
from PIL import Image, ImageDraw

R = sys.argv[1]
O = R + '/docs/concept/sprites/olinguito/'
BG, DONKER = (152, 208, 160), (40, 40, 48)


def frames(p, n=2, bg=BG):
    im = Image.open(p)
    pal = im.getpalette()[:48]
    uit = []
    for i in range(n):
        c = im.crop((0, 64 * i, 64, 64 * i + 64))
        f = Image.new('RGB', (64, 64), bg)
        for y in range(64):
            for x in range(64):
                v = c.getpixel((x, y))
                if v:
                    f.putpixel((x, y), tuple(pal[v * 3:v * 3 + 3]))
        uit.append(f)
    return uit


def panelen(bg):
    r15, r16 = frames(O + 'ronde15/anim_front.png', bg=bg), frames(O + 'ronde16/anim_front.png', bg=bg)
    g = lambda n: frames(R + '/graphics/pokemon/%s/anim_front.png' % n, 1, bg)[0]
    return [('ronde 15 f1', r15[0]), ('ronde 16 f1', r16[0]), ('ronde 16 f2', r16[1]),
            ('Poochyena', g('poochyena')), ('Sneasel', g('sneasel')), ('Umbreon', g('umbreon'))]


S = 3
licht, donker = panelen(BG), panelen(DONKER)
W = Image.new('RGB', (len(licht) * (64 * S + 8) + 8, 64 * S + 64 + 64 + 44), (255, 255, 255))
d = ImageDraw.Draw(W)
for i, ((t, p), (_, q)) in enumerate(zip(licht, donker)):
    x = 8 + i * (64 * S + 8)
    d.text((x, 4), t, fill=(0, 0, 0))
    W.paste(p.resize((64 * S, 64 * S), Image.NEAREST), (x, 18))
    W.paste(p, (x + 32, 64 * S + 28))
    W.paste(q, (x + 32 + 64 + 4, 64 * S + 28))
d.text((8, 64 * S + 28 + 70), '1x op licht en donker', fill=(0, 0, 0))
W.save(O + 'ronde16/compare.png')
