"""Ronde 3: panelen onder het keurvel.
(1) voorpoten: close-up variant B x8-40, y36-61 (16x) naast vilt_poten_LEIDRAAD, zijdemot_blad_frontaal (uitsnede poten),
    zijdemot_closeup_kop, foto_tak_katoen_2 (uitsnede poten) en vilt_hand_vleugels_gespreid (uitsnede), allemaal even hoog.
(2) achterpoten: close-up variant B x4-46, y46-61 (16x) naast Giratina frame 1 op 8x en de onderkant ervan op 16x."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); REF = os.path.join(HERE, '../../referenties/')
G = os.path.join(HERE, '../../../../../../graphics/pokemon/giratina/')
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
def sprite(p, box, z):
    im = Image.open(p); idx = np.array(im); rgb = np.array(im.convert('RGB')); rgb[idx == 0] = 255
    x0, y0, x1, y1 = box
    return Image.fromarray(rgb[y0:y1, x0:x1]).resize(((x1 - x0) * z, (y1 - y0) * z), Image.NEAREST)
def foto(n, crop, h):
    im = Image.open(REF + n).convert('RGB')
    if crop: im = im.crop(crop)
    return im.resize((im.width * h // im.height, h), Image.LANCZOS)
def rij(items, uit):
    H = max(i.height for _, i in items)
    P = Image.new('RGB', (sum(i.width + 10 for _, i in items) + 10, H + 30), (236, 236, 240)); d = ImageDraw.Draw(P); x = 10
    for t, i in items: d.text((x, 6), t, fill=(0, 0, 0), font=F); P.paste(i, (x, 28)); x += i.width + 10
    P.save(os.path.join(HERE, uit)); return P
B = os.path.join(HERE, 'variant_B/anim_front.png')
v = sprite(B, (8, 36, 40, 61), 16); h = v.height
rij([('voorpoten B (16x)', v), ('LEIDRAAD vilt_poten', foto('vilt_poten_LEIDRAAD.png', None, h)),
     ('zijdemot_blad_frontaal', foto('zijdemot_blad_frontaal.webp', (380, 140, 760, 600), h)),
     ('zijdemot_closeup_kop', foto('zijdemot_closeup_kop.png', None, h)),
     ('foto_tak_katoen_2', foto('foto_tak_katoen_2.webp', (560, 620, 1270, 1320), h)),
     ('vilt_hand', foto('vilt_hand_vleugels_gespreid.png', (270, 140, 520, 420), h)),
     ('zijdemot_vinger', foto('zijdemot_vinger.png', None, h))], 'paneel_voorpoten.png')
a = sprite(B, (4, 46, 46, 62), 16)
gi = Image.open(G + 'anim_front.png'); gp = [tuple(map(int, l.split())) for l in open(G + 'normal.pal').read().split('\n')[3:19]]
gi = gi.crop((0, 0, 64, 64)); idx = np.array(gi); rgb = np.array([[gp[i] if i else (255, 255, 255) for i in r] for r in idx], np.uint8)
g8 = Image.fromarray(rgb).resize((512, 512), Image.NEAREST); g16 = Image.fromarray(rgb[44:64, 0:64]).resize((64 * 16 // 2, 20 * 16 // 2), Image.NEAREST)
rij([('achterpoten B (16x)', a), ('Giratina frame 1 (8x)', g8.resize((a.height, a.height), Image.NEAREST)), ('Giratina onderkant y44-63 (8x)', g16)], 'paneel_achterpoten.png')
