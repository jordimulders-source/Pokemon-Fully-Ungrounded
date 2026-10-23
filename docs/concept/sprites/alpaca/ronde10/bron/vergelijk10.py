"""compare.png: referentiefoto (verkleind), ronde 9, ronde 10, Mudbray, Girafarig, Mareep; 1x en 3x.
Gebruik (vanuit de repo-root): python3 docs/concept/sprites/alpaca/ronde10/bron/vergelijk10.py"""
import os
from PIL import Image, ImageDraw

R = 'docs/concept/sprites/alpaca/'


def sprite(p):
    im = Image.open(p)
    d = im.crop((0, 0, 64, 64))
    rgb = d.convert('RGB'); px = d.load(); rp = rgb.load()
    for y in range(64):
        for x in range(64):
            if px[x, y] == 0:
                rp[x, y] = (255, 255, 255)
    return rgb


def gba(n):
    p = 'graphics/pokemon/%s/anim_front_gba.png' % n
    return sprite(p if os.path.exists(p) else 'graphics/pokemon/%s/anim_front.png' % n)


foto = Image.open('docs/concept/ontwerp/alpaca/referentie_alpaca.webp').convert('RGB')
foto = foto.crop((300, 180, 1500, 1440)).transpose(Image.FLIP_LEFT_RIGHT).resize((61, 64), Image.LANCZOS)
f64 = Image.new('RGB', (64, 64), (255, 255, 255)); f64.paste(foto, (1, 0))
items = [('foto (gespiegeld)', f64), ('ronde 9', sprite(R + 'ronde9/anim_front.png')),
         ('ronde 10', sprite(R + 'ronde10/anim_front.png')), ('Mudbray', gba('mudbray')),
         ('Girafarig', gba('girafarig')), ('Mareep', gba('mareep'))]
n = len(items)
out = Image.new('RGB', (n * 202 + 10, 16 + 74 + 16 + 192 + 10), (255, 255, 255))
d = ImageDraw.Draw(out)
for i, (naam, im) in enumerate(items):
    x = 10 + i * 202
    d.text((x, 2), naam, fill=(0, 0, 0))
    out.paste(im, (x, 18))
    out.paste(im.resize((192, 192), Image.NEAREST), (x, 106))
out.save(R + 'ronde10/compare.png')
