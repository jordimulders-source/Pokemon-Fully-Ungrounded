"""Controlevel bron fase 3: onderlaag | model50 4x | overlay | 1x naast fase 2 (af) als silhouet en als sprite.
Draaien vanuit deze map: python3 vel.py"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
M = np.array([[c == '#' for c in l.rstrip('\n')] for l in open(os.path.join(HERE, 'model50.txt')) if l.strip()])
f2 = np.array(Image.open(os.path.join(HERE, '../../fase2/af/lama.png')).convert('RGBA'))
A2 = f2[..., 3] > 0
def sil(m, col=(40, 30, 30)):
    im = np.full((64, 64, 3), 255, np.uint8); im[m] = col; return Image.fromarray(im)
und = Image.open(os.path.join(HERE, 'onderlaag_256.png')).convert('RGB')
ov = und.copy(); o = np.array(ov); mm = np.array(sil(M).resize((256, 256), Image.NEAREST))[..., 0] < 128
o[mm] = (o[mm] * 0.45 + np.array((40, 60, 200)) * 0.55).astype(np.uint8); ov = Image.fromarray(o)
tiles = [(und, 'onderlaag (poppetje Y, pose C)'), (sil(M).resize((256, 256), Image.NEAREST), f'fase 3 model 50%: {int(M.sum())} px'),
         (ov, 'silhouet over de onderlaag'), (sil(A2).resize((256, 256), Image.NEAREST), f'fase 2 (af): {int(A2.sum())} px')]
im = Image.new('RGB', (12 + 266 * 4, 44 + 290 + 120), 'white'); d = ImageDraw.Draw(im)
d.text((12, 12), 'Lama fase 3: bron voor het silhouet (ruwe 50%-dekking van het poppetje, nog niet overgetrokken)', font=FB, fill=(30, 30, 30))
for i, (t, lab) in enumerate(tiles):
    im.paste(t, (12 + 266 * i, 44)); d.text((16 + 266 * i, 304), lab, font=F, fill=(60, 60, 60))
y = 334
bg = Image.new('RGBA', (64, 64), 'white'); bg.alpha_composite(Image.fromarray(f2))
for i, (t, lab) in enumerate(((sil(M), 'fase 3, 1x'), (sil(A2), 'fase 2, 1x'), (bg.convert('RGB'), 'fase 2 sprite, 1x'))):
    im.paste(t, (12 + 120 * i, y)); d.text((12 + 120 * i, y + 68), lab, font=F, fill=(60, 60, 60))
im.save(os.path.join(HERE, 'vel_bron.png'))
