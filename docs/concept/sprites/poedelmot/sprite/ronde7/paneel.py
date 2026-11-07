"""Ronde 7: paneel_achterpoten.png = de poten van ronde 6 en ronde 7 op 16x (x4-48, y44-61), een vak met Giratina's
poten (frame 1, y36-64, 12x: links lager aan de onderkant, rechts hoger aan de zijkant) en de tak-foto (onderkant)."""
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
    im = Image.open(REF + n).convert('RGB').crop(crop)
    return im.resize((im.width * h // im.height, h), Image.LANCZOS)
BOX = (4, 44, 48, 61)
v7 = sprite(os.path.join(HERE, 'anim_front.png'), BOX, 16); h = v7.height
g = sprite(G, (0, 36, 64, 64), 12); g = g.resize((g.width * h // g.height, h), Image.NEAREST)
items = [('ronde 6 (16x)', sprite(os.path.join(HERE, '../ronde6/anim_front.png'), BOX, 16)), ('ronde 7 (16x)', v7),
         ('Giratina: links lager, rechts hoger', g),
         ('foto_tak_katoen_2 (onderkant)', foto('foto_tak_katoen_2.webp', (420, 820, 1320, 1340), h))]
P = Image.new('RGB', (sum(i.width + 10 for _, i in items) + 10, h + 30), (236, 236, 240)); d = ImageDraw.Draw(P); x = 10
for t, i in items: d.text((x, 6), t, fill=(0, 0, 0), font=F); P.paste(i, (x, 28)); x += i.width + 10
P.save(os.path.join(HERE, 'paneel_achterpoten.png'))
