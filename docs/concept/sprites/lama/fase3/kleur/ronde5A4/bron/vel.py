"""Vel ronde 5A4: 4x licht/donker, 1x; kop 8x: 5A | 5A2 | render (A); oog 12x naast Slakoth/Slaking. -> ../vel_ronde5A4.png"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(H); K = os.path.join(H, '../..'); ROOT = os.path.join(K, *['..'] * 6)
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
LICHT, DONKER = (248, 248, 244, 255), (44, 44, 56, 255)
def on(im, bg, s=1):
    b = Image.new('RGBA', im.size, bg); b.alpha_composite(im.convert('RGBA')); return b.resize((im.width * s, im.height * s), Image.NEAREST)
def load(p):
    raw = Image.open(p); im = raw.convert('RGBA'); im.putalpha(Image.fromarray(((np.array(raw) != 0) * 255).astype('uint8'))); return im
new = load(os.path.join(OUT, 'lama3.png')); old = load(os.path.join(K, 'ronde5A3/lama3.png')); r5a = load(os.path.join(K, 'ronde5A/lama3.png'))
W = Image.new('RGBA', (1180, 560), LICHT); d = ImageDraw.Draw(W)
d.text((10, 6), 'Lama fase 3, kleur ronde 5A4: bombin 1 rij lager; oog bevroren; rest 0 px diff met 5A3', fill=(0, 0, 0), font=F)
W.paste(on(new, LICHT, 4), (10, 30)); W.paste(on(new, DONKER, 4), (280, 30)); d.text((10, 290), '5A4: 4x licht / donker', fill=(0, 0, 0), font=F)
W.paste(on(new, LICHT), (560, 40)); W.paste(on(new, DONKER), (630, 40)); W.paste(on(old, LICHT), (560, 120)); W.paste(on(old, DONKER), (630, 120))
d.text((560, 108), '1x: 5A4', fill=(0, 0, 0), font=F); d.text((560, 188), '1x: 5A3', fill=(0, 0, 0), font=F)
box = (8, 0, 36, 26); s = 8
W.paste(on(old.crop(box), LICHT, s), (10, 320)); W.paste(on(new.crop(box), LICHT, s), (250, 320))
ov = Image.open(os.path.join(K, 'kopbron/kop_overtrekvel_A.png')).convert('RGBA'); ov = ov.crop((0, 0, ov.width // 2, ov.height))
ov = ov.resize((int(ov.width * 208 / ov.height), 208), Image.LANCZOS); W.alpha_composite(ov, (490, 320))
d.text((10, 532), 'kop 8x: 5A3', fill=(0, 0, 0), font=F); d.text((250, 532), 'kop 8x: 5A4', fill=(0, 0, 0), font=F); d.text((490, 532), 'render model (A)', fill=(0, 0, 0), font=F)
W.convert('RGB').save(os.path.join(OUT, 'vel_ronde5A4.png'))
