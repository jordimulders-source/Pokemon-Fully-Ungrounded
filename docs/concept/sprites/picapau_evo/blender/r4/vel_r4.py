"""Vel voor de coördinator: gekozen r4-render (8x en 1x) naast Staraptor, Braviary, Talonflame, Picapau (af) en
Raichu Gen 1, elk op 1x en 4x. Draaien: python3.11 vel_r4.py V2"""
import os, sys
from PIL import Image, ImageDraw
HIER = os.path.dirname(os.path.abspath(__file__)); G = os.path.join(HIER, '../../../../../../graphics/pokemon')
def front(naam):
    im = Image.open(os.path.join(G, naam, 'anim_front.png')).convert('RGBA').crop((0, 0, 64, 64)); px = im.load(); bg = px[0, 0]
    for y in range(64):
        for x in range(64):
            if px[x, y] == bg: px[x, y] = (0, 0, 0, 0)
    return im
v = sys.argv[1] if len(sys.argv) > 1 else 'V2'
items = [(f'r4 {v} (1x-verkleining)', Image.open(os.path.join(HIER, f'{v}_1x.png')).convert('RGBA')),
         ('Staraptor', front('staraptor')), ('Braviary', front('braviary')), ('Talonflame', front('talonflame')),
         ('Picapau (af)', Image.open(os.path.join(HIER, '../../../picapau/af/picapau.png')).convert('RGBA')),
         ('Raichu Gen 1', Image.open(os.path.join(HIER, '../../referenties/jordi_inspiratie_raichu_gen1.png')).convert('RGBA').resize((64, 64), Image.NEAREST))]
R = 512; W = 256 + 8
v8 = Image.open(os.path.join(HIER, f'{v}_8x.png')).convert('RGBA')
vel = Image.new('RGBA', (R + 16 + W * len(items), 16 + R + 8), (255, 255, 255, 255)); d = ImageDraw.Draw(vel)
d.text((8, 2), f'r4 {v}: render 8x', fill=(0, 0, 0, 255)); vel.alpha_composite(v8, (8, 16))
for i, (t, im) in enumerate(items):
    x = R + 16 + i * W; d.text((x, 2), t, fill=(0, 0, 0, 255))
    vel.alpha_composite(im, (x, 16)); vel.alpha_composite(im.resize((256, 256), Image.NEAREST), (x, 88))
vel.convert('RGB').save(os.path.join(HIER, 'vel_r4.png')); print('vel_r4.png', vel.size)
