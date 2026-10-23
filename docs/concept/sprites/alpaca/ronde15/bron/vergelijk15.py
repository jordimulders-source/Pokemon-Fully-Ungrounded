"""compare.png voor ronde 15: ronde 13, ronde 14 B+C (samengevoegd uit variant_B en variant_C) en
ronde 15 (frame 1 en 2), op wit en gevechtsgrond (1x en 3x), plus een 4x-uitsnede van kop en hals
(x12-39, y2-31). Gebruik (vanuit de repo-root):
python3 docs/concept/sprites/alpaca/ronde15/bron/vergelijk15.py"""
from PIL import Image, ImageDraw

R = 'docs/concept/sprites/alpaca/'


def frame(p, frame=0):
    return Image.open(p).crop((0, 64 * frame, 64, 64 * frame + 64))


# ronde 14 B+C: variant_C plus de pixels waarin variant_B van ronde 13 verschilt
r13 = frame(R + 'ronde13/anim_front.png')
b14, bc = frame(R + 'ronde14/variant_B/anim_front.png'), frame(R + 'ronde14/variant_C/anim_front.png')
for y in range(64):
    for x in range(64):
        if b14.getpixel((x, y)) != r13.getpixel((x, y)):
            bc.putpixel((x, y), b14.getpixel((x, y)))

ITEMS = [('ronde 13', r13), ('ronde 14 B+C', bc),
         ('ronde 15', frame(R + 'ronde15/anim_front.png')),
         ('ronde 15 frame 2', frame(R + 'ronde15/anim_front.png', 1))]
BG = [('wit', (255, 255, 255)), ('gevechtsgrond', (232, 224, 176))]
W = 210


def rgb(d, bg):
    out = d.convert('RGB'); px = d.load(); rp = out.load()
    for y in range(64):
        for x in range(64):
            if px[x, y] == 0:
                rp[x, y] = bg
    return out


rij = 16 + 64 + 6 + 192 + 10
out = Image.new('RGB', (len(ITEMS) * W + 10, 8 + rij * len(BG) + 16 + 120 + 10), (255, 255, 255))
d = ImageDraw.Draw(out)
for j, (bnaam, bg) in enumerate(BG):
    y0 = 4 + j * rij
    d.rectangle([0, y0, out.width, y0 + rij - 4], fill=bg)
    for i, (naam, f) in enumerate(ITEMS):
        x = 10 + i * W
        im = rgb(f, bg)
        d.text((x, y0 + 2), '%s (%s)' % (naam, bnaam), fill=(0, 0, 0))
        out.paste(im, (x, y0 + 16))
        out.paste(im.resize((192, 192), Image.NEAREST), (x, y0 + 86))
y0 = 4 + rij * len(BG)
d.text((10, y0), '4x uitsnede kop en hals (x12-39, y2-31)', fill=(0, 0, 0))
for i, (naam, f) in enumerate(ITEMS):
    c = rgb(f, (255, 255, 255)).crop((12, 2, 40, 32))
    out.paste(c.resize((112, 120), Image.NEAREST), (10 + i * W, y0 + 16))
out.save(R + 'ronde15/compare.png')
