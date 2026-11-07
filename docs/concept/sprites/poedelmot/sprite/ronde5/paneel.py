"""Ronde 5: panelen onder het keurvel.
(1) paneel_poten.png: de poten van ronde 5 op 16x (x4-46, y38-61) naast de pootuitsneden van vier foto's (even hoog).
(2) paneel_schets.png: Jordi's schets (zijn zwarte lijnen op ronde 4) naast ronde 5 met dezelfde lijnen erover, op 16x.
    De lijnen zijn uit de schets gehaald (registratie schaal 3,82, verschuiving 9,8 = beste overeenkomst met ronde 4)."""
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
W = os.path.join(HERE, 'anim_front.png'); W4 = os.path.join(HERE, '../ronde4/anim_front.png')
BOX = (4, 38, 46, 61)
v = sprite(W, BOX, 16); h = v.height
rij([('poten ronde 5 (16x)', v),
     ('vilt_poten_LEIDRAAD', foto('vilt_poten_LEIDRAAD.png', (30, 60, 190, 192), h)),
     ('foto_tak_katoen_2', foto('foto_tak_katoen_2.webp', (540, 850, 1280, 1330), h)),
     ('vilt_hand', foto('vilt_hand_vleugels_gespreid.png', (280, 230, 510, 390), h)),
     ('zijdemot_blad_frontaal', foto('zijdemot_blad_frontaal.webp', (340, 320, 740, 590), h))], 'paneel_poten.png')
# Jordi's lijnen: donkere pixels in de schets die op een lichte pixel van ronde 4 vallen
S = np.array(Image.open(REF + 'jordi_schets_ronde4_aansluiting.png').convert('RGB')).astype(int)
r4 = np.array(Image.open(W4).convert('RGB')).astype(int)
s, ox, oy, z = 3.82, 9, 8, 16
def met_lijnen(p):
    im = sprite(p, BOX, z); d = ImageDraw.Draw(im)
    for py in range(S.shape[0]):
        for px in range(S.shape[1]):
            if S[py, px].sum() < 60:
                x = (px - ox) / s; y = (py - oy) / s
                if 0 <= int(x) < 64 and 0 <= int(y) < 64 and r4[int(y), int(x)].sum() > 200:
                    X = (x - BOX[0]) * z; Y = (y - BOX[1]) * z
                    d.ellipse((X - 3, Y - 3, X + 3, Y + 3), fill=(220, 0, 40))
    return im
rij([('Jordi: schets op ronde 4 (rood = zijn lijnen)', met_lijnen(W4)),
     ('ronde 5 met dezelfde lijnen', met_lijnen(W)),
     ('ronde 5 zonder lijnen', sprite(W, BOX, z))], 'paneel_schets.png')
