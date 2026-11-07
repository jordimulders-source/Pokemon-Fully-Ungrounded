"""Ronde 2: (1) Jordi's rode lijnen (referenties/jordi_schets_poten_ronde1.png) teruggezet op de 16x-close-up
x4-46, y42-63 van ronde 1 en, op dezelfde plek, over ronde 2 -> schets_overlay.png.
Uitlijning gemeten (zoeken naar de kleinste kleurafwijking): schetspixel (u, v) = spritepixel ((u-7)/8.1+4, (v-3)/8.1+42).
(2) pootpaneel.png: pootclose-up ronde 2 (16x) naast de LEIDRAAD-foto (groot), de schets-overlay en de pootstudie."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); REF = os.path.join(HERE, '../../referenties/')
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
X0, Y0, X1, Y1, Z = 4, 42, 46, 64, 16
def close(p):
    im = Image.open(p); idx = np.array(im); rgb = np.array(im.convert('RGB')); rgb[idx == 0] = 255
    return Image.fromarray(rgb[Y0:Y1, X0:X1]).resize(((X1 - X0) * Z, (Y1 - Y0) * Z), Image.NEAREST)
sk = np.array(Image.open(REF + 'jordi_schets_poten_ronde1.png').convert('RGB')).astype(int)
red = (sk[..., 0] > 180) & (sk[..., 1] < 90) & (sk[..., 2] < 90)
vs, us = np.nonzero(red)
def rood(im):
    d = ImageDraw.Draw(im)
    for u, v in zip(us, vs):
        x = ((u - 7) / 8.1 + 4 - X0) * Z; y = ((v - 3) / 8.1 + 42 - Y0) * Z
        d.rectangle([x, y, x + 1, y + 1], fill=(230, 20, 20))
    for gx in range(0, (X1 - X0) * Z + 1, 4 * Z):   # raster per 4 px met spritecoordinaten
        d.line([(gx, 0), (gx, 6)], fill=(0, 0, 255)); d.text((gx + 2, 6), str(X0 + gx // Z), fill=(0, 0, 255), font=F)
    for gy in range(0, (Y1 - Y0) * Z + 1, 4 * Z):
        d.line([(0, gy), (6, gy)], fill=(0, 0, 255)); d.text((8, gy + 2), str(Y0 + gy // Z), fill=(0, 0, 255), font=F)
    return im
a = rood(close(os.path.join(HERE, '../ronde1/anim_front.png'))); b = rood(close(os.path.join(HERE, 'anim_front.png')))
W, H = a.size
ov = Image.new('RGB', (2 * W + 30, H + 30), (236, 236, 240)); d = ImageDraw.Draw(ov)
d.text((10, 6), 'ronde 1 + Jordi\'s lijnen (16x)', fill=(0, 0, 0), font=F); d.text((W + 20, 6), 'ronde 2 + dezelfde lijnen (16x)', fill=(0, 0, 0), font=F)
ov.paste(a, (10, 28)); ov.paste(b, (W + 20, 28)); ov.save(os.path.join(HERE, 'schets_overlay.png'))
# pootpaneel
c = close(os.path.join(HERE, 'anim_front.png'))
leid = Image.open(REF + 'vilt_poten_LEIDRAAD.png').convert('RGB'); leid = leid.resize((leid.width * c.height // leid.height, c.height), Image.LANCZOS)
st = Image.open(os.path.join(HERE, 'studie_poten.png')); st = st.resize((st.width * c.height // st.height, c.height), Image.LANCZOS)
items = [('poten ronde 2, close-up x4-46 y42-63 (16x)', c), ('LEIDRAAD: vilt_poten_LEIDRAAD.png', leid), ('studie_poten.png (Gen 3, niet-insecten)', st)]
P = Image.new('RGB', (sum(i.width + 10 for _, i in items) + 10, c.height + 30), (236, 236, 240)); d = ImageDraw.Draw(P); x = 10
for t, i in items: d.text((x, 6), t, fill=(0, 0, 0), font=F); P.paste(i, (x, 28)); x += i.width + 10
P.save(os.path.join(HERE, 'pootpaneel.png'))
