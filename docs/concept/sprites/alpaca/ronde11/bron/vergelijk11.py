"""compare.png: referentiefoto (verkleind), ronde 10, ronde 11 (frame 1 en 2), Torchic, Mudkip, Mudbray; 1x en 3x.
Gebruik (vanuit de repo-root): python3 docs/concept/sprites/alpaca/ronde11/bron/vergelijk11.py [blind.png]
Met een tweede argument ook een blinde-checkvel: ronde 11 op 1x en 2x tussen echte sprites, zonder namen."""
import os
import sys
from PIL import Image, ImageDraw

R = 'docs/concept/sprites/alpaca/'


def sprite(p, frame=0, bg=(255, 255, 255)):
    im = Image.open(p)
    d = im.crop((0, 64 * frame, 64, 64 * frame + 64))
    rgb = d.convert('RGB'); px = d.load(); rp = rgb.load()
    for y in range(64):
        for x in range(64):
            if px[x, y] == 0:
                rp[x, y] = bg
    return rgb


def gba(n, bg=(255, 255, 255)):
    p = 'graphics/pokemon/%s/anim_front_gba.png' % n
    return sprite(p if os.path.exists(p) else 'graphics/pokemon/%s/anim_front.png' % n, 0, bg)


foto = Image.open('docs/concept/ontwerp/alpaca/referentie_alpaca.webp').convert('RGB')
foto = foto.crop((300, 180, 1500, 1440)).transpose(Image.FLIP_LEFT_RIGHT).resize((61, 64), Image.LANCZOS)
f64 = Image.new('RGB', (64, 64), (255, 255, 255)); f64.paste(foto, (1, 0))
items = [('foto (gespiegeld)', f64), ('ronde 10 (1248 px)', sprite(R + 'ronde10/anim_front.png')),
         ('ronde 11 (869 px)', sprite(R + 'ronde11/anim_front.png')),
         ('ronde 11 frame 2', sprite(R + 'ronde11/anim_front.png', 1)),
         ('Torchic (782)', gba('torchic')), ('Mudkip (852)', gba('mudkip')), ('Mudbray (1080)', gba('mudbray'))]
n = len(items)
out = Image.new('RGB', (n * 202 + 10, 16 + 74 + 192 + 10), (255, 255, 255))
d = ImageDraw.Draw(out)
for i, (naam, im) in enumerate(items):
    x = 10 + i * 202
    d.text((x, 2), naam, fill=(0, 0, 0))
    out.paste(im, (x, 18))
    out.paste(im.resize((192, 192), Image.NEAREST), (x, 96))
out.save(R + 'ronde11/compare.png')

if len(sys.argv) > 1:
    bg = (200, 216, 176)
    namen = ['mareep', 'ponyta', 'torchic', None, 'girafarig', 'mudkip', 'makuhita']
    ims = [sprite(R + 'ronde11/anim_front.png', 0, bg) if n is None else gba(n, bg) for n in namen]
    bl = Image.new('RGB', (len(ims) * 68 + 4, 68 + 132), bg)
    for i, im in enumerate(ims):
        bl.paste(im, (4 + i * 68, 2))
    for i, im in enumerate(ims[1:6]):
        bl.paste(im.resize((128, 128), Image.NEAREST), (4 + i * 132, 70))
    bl.save(sys.argv[1])
