"""compare.png voor ronde 14: ronde 13 en varianten A-D, frame 1, op wit en gevechtsgrond (1x en 3x),
plus een 4x-uitsnede van kop en hals (x12-39, y2-31) waar alle hints zitten.
Gebruik (vanuit de repo-root): python3 docs/concept/sprites/alpaca/ronde14/bron/vergelijk14.py"""
from PIL import Image, ImageDraw

R = 'docs/concept/sprites/alpaca/'
ITEMS = [('ronde 13', R + 'ronde13/anim_front.png'),
         ('A bombin-randje', R + 'ronde14/variant_A/anim_front.png'),
         ('B vlechtpuntjes', R + 'ronde14/variant_B/anim_front.png'),
         ('C aguayo-streepje', R + 'ronde14/variant_C/anim_front.png'),
         ('D = A+B+C', R + 'ronde14/variant_D/anim_front.png')]
BG = [('wit', (255, 255, 255)), ('gevechtsgrond', (232, 224, 176))]
W = 210


def sprite(p, bg, frame=0):
    im = Image.open(p)
    d = im.crop((0, 64 * frame, 64, 64 * frame + 64))
    rgb = d.convert('RGB'); px = d.load(); rp = rgb.load()
    for y in range(64):
        for x in range(64):
            if px[x, y] == 0:
                rp[x, y] = bg
    return rgb


rij = 16 + 64 + 6 + 192 + 10
uit_h = 8 + rij * len(BG) + 16 + 120 + 10
out = Image.new('RGB', (len(ITEMS) * W + 10, uit_h), (255, 255, 255))
d = ImageDraw.Draw(out)
for j, (bnaam, bg) in enumerate(BG):
    y0 = 4 + j * rij
    d.rectangle([0, y0, out.width, y0 + rij - 4], fill=bg)
    for i, (naam, p) in enumerate(ITEMS):
        x = 10 + i * W
        im = sprite(p, bg)
        d.text((x, y0 + 2), '%s (%s)' % (naam, bnaam), fill=(0, 0, 0))
        out.paste(im, (x, y0 + 16))
        out.paste(im.resize((192, 192), Image.NEAREST), (x, y0 + 86))
y0 = 4 + rij * len(BG)
d.text((10, y0), '4x uitsnede kop en hals (x12-39, y2-31), frame 1', fill=(0, 0, 0))
for i, (naam, p) in enumerate(ITEMS):
    c = sprite(p, (255, 255, 255)).crop((12, 2, 40, 32))
    out.paste(c.resize((112, 120), Image.NEAREST), (10 + i * W, y0 + 16))
out.save(R + 'ronde14/compare.png')
