"""Ronde 8: paneel_achterpoten.png = de onderkant (x4-48, y40-61) van ronde 6 en ronde 8 op 16x, Giratina's onderkant
(frame 1, y34-64) op dezelfde hoogte, en de bronvakken: tak-foto (onderkant) en vilt_poten_LEIDRAAD."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); REF = os.path.join(HERE, '../../referenties/')
G = os.path.join(HERE, '../../../../../../graphics/pokemon/giratina/anim_front.png')
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
def sprite(p, box, z):
    im = Image.open(p).crop((0, 0, 64, 64)); idx = np.array(im); rgb = np.array(im.convert('RGB')); rgb[idx == 0] = 255
    x0, y0, x1, y1 = box
    return Image.fromarray(rgb[y0:y1, x0:x1]).resize(((x1 - x0) * z, (y1 - y0) * z), Image.NEAREST)
def foto(n, crop, h):
    im = Image.open(REF + n).convert('RGB')
    if crop: im = im.crop(crop)
    return im.resize((im.width * h // im.height, h), Image.LANCZOS)
BOX = (4, 40, 48, 61)
v8 = sprite(os.path.join(HERE, 'anim_front.png'), BOX, 16); h = v8.height
g = sprite(G, (4, 40, 64, 64), 16); g = g.resize((g.width * h // g.height, h), Image.NEAREST)
items = [('ronde 6 (16x)', sprite(os.path.join(HERE, '../ronde6/anim_front.png'), BOX, 16)), ('ronde 8 (16x)', v8),
         ('Giratina (16x, onderkant)', g),
         ('foto_tak_katoen (onderkant)', foto('foto_tak_katoen.webp', (500, 820, 1300, 1340), h)),
         ('vilt_poten_LEIDRAAD', foto('vilt_poten_LEIDRAAD.png', None, h))]
P = Image.new('RGB', (sum(i.width + 10 for _, i in items) + 10, h + 30), (236, 236, 240)); d = ImageDraw.Draw(P); x = 10
for t, i in items: d.text((x, 6), t, fill=(0, 0, 0), font=F); P.paste(i, (x, 28)); x += i.width + 10
P.save(os.path.join(HERE, 'paneel_achterpoten.png'))
