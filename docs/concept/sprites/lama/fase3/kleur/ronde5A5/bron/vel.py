"""Vel ronde 5A5: 4x licht/donker, 1x (5A5 en 5A4); kop 8x 5A4|5A5; achterpoten 8x 5A4|5A5. -> ../vel_ronde5A5.png"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(H); K = os.path.join(H, '../..')
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
LICHT, DONKER = (248, 248, 244, 255), (44, 44, 56, 255)
def on(im, bg, s=1):
    b = Image.new('RGBA', im.size, bg); b.alpha_composite(im.convert('RGBA')); return b.resize((im.width * s, im.height * s), Image.NEAREST)
def load(p):
    raw = Image.open(p); im = raw.convert('RGBA'); im.putalpha(Image.fromarray(((np.array(raw) != 0) * 255).astype('uint8'))); return im
new = load(os.path.join(OUT, 'lama3.png')); old = load(os.path.join(K, 'ronde5A4/lama3.png'))
W = Image.new('RGBA', (800, 510), LICHT); d = ImageDraw.Draw(W)
d.text((10, 6), 'Lama fase 3, kleur ronde 5A5: bombin links in hoedtinten en 2 px korter; verre achterpoot met volume; rest 0 px diff met 5A4', fill=(0, 0, 0), font=F)
W.paste(on(new, LICHT, 4), (10, 30)); W.paste(on(new, DONKER, 4), (280, 30)); d.text((10, 290), '5A5: 4x licht / donker', fill=(0, 0, 0), font=F)
W.paste(on(new, LICHT), (560, 40)); W.paste(on(new, DONKER), (630, 40)); W.paste(on(old, LICHT), (560, 120)); W.paste(on(old, DONKER), (630, 120))
d.text((560, 108), '1x: 5A5', fill=(0, 0, 0), font=F); d.text((560, 188), '1x: 5A4', fill=(0, 0, 0), font=F)
kb = (12, 0, 34, 20); pb = (28, 44, 50, 63); s = 8
W.paste(on(old.crop(kb), LICHT, s), (10, 320)); W.paste(on(new.crop(kb), LICHT, s), (200, 320))
d.text((10, 484), 'kop 8x: 5A4', fill=(0, 0, 0), font=F); d.text((200, 484), 'kop 8x: 5A5', fill=(0, 0, 0), font=F)
W.paste(on(old.crop(pb), LICHT, s), (400, 320)); W.paste(on(new.crop(pb), LICHT, s), (590, 320))
d.text((400, 484), 'achterpoten 8x: 5A4', fill=(0, 0, 0), font=F); d.text((590, 484), 'achterpoten 8x: 5A5', fill=(0, 0, 0), font=F)
W.convert('RGB').save(os.path.join(OUT, 'vel_ronde5A5.png'))
