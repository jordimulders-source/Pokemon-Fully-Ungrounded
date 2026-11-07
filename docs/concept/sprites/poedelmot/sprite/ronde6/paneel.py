"""Ronde 6: paneel_voorpoten.png = de voorpoten van ronde 5 en ronde 6 op 16x (x12-40, y44-60) naast de
vilt-uitsnede (LEIDRAAD) en de twee zijdemot-foto's, even hoog."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); REF = os.path.join(HERE, '../../referenties/')
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
def sprite(p, box, z):
    im = Image.open(p); idx = np.array(im); rgb = np.array(im.convert('RGB')); rgb[idx == 0] = 255
    x0, y0, x1, y1 = box
    return Image.fromarray(rgb[y0:y1, x0:x1]).resize(((x1 - x0) * z, (y1 - y0) * z), Image.NEAREST)
def foto(n, crop, h):
    im = Image.open(REF + n).convert('RGB').crop(crop)
    return im.resize((im.width * h // im.height, h), Image.LANCZOS)
BOX = (12, 44, 40, 61)
v6 = sprite(os.path.join(HERE, 'anim_front.png'), BOX, 16); h = v6.height
items = [('ronde 5 (16x)', sprite(os.path.join(HERE, '../ronde5/anim_front.png'), BOX, 16)), ('ronde 6 (16x)', v6),
         ('vilt_poten_LEIDRAAD', foto('vilt_poten_LEIDRAAD.png', (30, 60, 190, 192), h)),
         ('zijdemot_blad_frontaal', foto('zijdemot_blad_frontaal.webp', (340, 320, 740, 590), h)),
         ('zijdemot_vinger', foto('zijdemot_vinger.png', (120, 300, 420, 560), h))]
P = Image.new('RGB', (sum(i.width + 10 for _, i in items) + 10, h + 30), (236, 236, 240)); d = ImageDraw.Draw(P); x = 10
for t, i in items: d.text((x, 6), t, fill=(0, 0, 0), font=F); P.paste(i, (x, 28)); x += i.width + 10
P.save(os.path.join(HERE, 'paneel_voorpoten.png'))
