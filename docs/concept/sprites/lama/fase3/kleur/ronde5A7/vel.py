"""Vel ronde 5A7: 5A6 | 5A7 (eindkeuring R1-R7 uitgevoerd) op 4x licht/donker, poten 8x, 1x. Draaien vanuit deze map."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__))
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
def op(p, bg):
    s = Image.open(p).convert('RGBA'); b = Image.new('RGBA', s.size, bg); b.alpha_composite(s); return b.convert('RGB')
a, b = os.path.join(H, '../ronde5A6/lama3.png'), os.path.join(H, 'lama3.png')
im = Image.new('RGB', (12 + 4 * 266 + 160, 44 + 266 + 26 + 8 * 24 + 30), (246, 246, 240)); d = ImageDraw.Draw(im)
d.text((12, 12), 'Lama fase 3: 5A6 | 5A7 (eindkeuring R1-R7 uitgevoerd, 28 px)', font=F, fill=(30, 30, 30))
for i, (p, bg, lab) in enumerate(((a, 'white', '5A6 licht'), (b, 'white', '5A7 licht'), (a, (40, 40, 52), '5A6 donker'), (b, (40, 40, 52), '5A7 donker'))):
    im.paste(op(p, bg).resize((256, 256), Image.NEAREST), (12 + 266 * i, 44)); d.text((12 + 266 * i, 304), lab, font=F, fill=(60, 60, 60))
for i, p in enumerate((a, b)):
    im.paste(op(p, 'white'), (12 + 4 * 266 + 10, 44 + 80 * i)); im.paste(op(p, (40, 40, 52)), (12 + 4 * 266 + 80, 44 + 80 * i))
y0 = 44 + 266 + 26
for i, p in enumerate((a, b)):
    im.paste(op(p, 'white').crop((14, 38, 54, 64)).resize((40 * 8, 26 * 8), Image.NEAREST), (12 + i * 340, y0))
    d.text((12 + i * 340, y0 + 26 * 8 + 4), ('5A6' if i == 0 else '5A7') + ' poten 8x', font=F, fill=(60, 60, 60))
im.save(os.path.join(H, 'vel_ronde5A7.png'))
