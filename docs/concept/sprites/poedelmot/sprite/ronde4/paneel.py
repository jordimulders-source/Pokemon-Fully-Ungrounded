"""Ronde 4: panelen onder het keurvel.
(1) pootuiteinden: close-up ronde 4 x6-44, y50-60 (16x) naast uitsneden van de voeten op de bronfoto's (even hoog).
(2) voorpoten: close-up x8-40, y36-61 (16x) ronde 3 B en ronde 4 naast elkaar."""
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
def rij(items, uit):
    H = max(i.height for _, i in items)
    P = Image.new('RGB', (sum(i.width + 10 for _, i in items) + 10, H + 30), (236, 236, 240)); d = ImageDraw.Draw(P); x = 10
    for t, i in items: d.text((x, 6), t, fill=(0, 0, 0), font=F); P.paste(i, (x, 28)); x += i.width + 10
    P.save(os.path.join(HERE, uit))
W = os.path.join(HERE, 'anim_front.png')
v = sprite(W, (6, 50, 44, 60), 16); h = v.height
rij([('pootuiteinden ronde 4 (16x)', v),
     ('zijdemot_blad_frontaal', foto('zijdemot_blad_frontaal.webp', (330, 380, 720, 580), h)),
     ('vilt_hand', foto('vilt_hand_vleugels_gespreid.png', (330, 300, 480, 380), h)),
     ('vilt_poten_LEIDRAAD', foto('vilt_poten_LEIDRAAD.png', (55, 95, 175, 160), h)),
     ('foto_tak_katoen_2', foto('foto_tak_katoen_2.webp', (580, 1050, 1270, 1320), h)),
     ('zijdemot_vinger', foto('zijdemot_vinger.png', (180, 380, 360, 530), h))], 'paneel_uiteinden.png')
rij([('ronde 3 B (16x)', sprite(os.path.join(HERE, '../ronde3/variant_B/anim_front.png'), (8, 36, 44, 61), 16)),
     ('ronde 4 (16x)', sprite(W, (8, 36, 44, 61), 16))], 'paneel_poten.png')
