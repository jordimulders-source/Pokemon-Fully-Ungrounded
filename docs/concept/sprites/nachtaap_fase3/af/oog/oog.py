"""Linkeroog (Jordi 5 nov: "kijk vooral ook naar het linkeroog nog"). Rechteroog (x9-11, y37-38) = glans 15 + c b / b a a;
linkeroog (x5-6) = c b / b a: geen glans, donkerste teal linksboven -> leest dof/dicht. Opties (alleen y37-38, x4-6):
A glans linksboven zoals rechts; B glans + 1 px breder naar buiten (3 px zoals rechts); C glans rechtsboven (naar de neus); D = voorstel keurder: glans + iris donker boven (F C / B A, rechteroog min één kolom)."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__))
src = Image.open(os.path.join(H, '../nachtaap_fase3.png')); A0 = np.array(src); pal = src.getpalette()
OPT = {'nu': {}, 'A': {(37, 5): 15}, 'B': {(37, 4): 12, (37, 5): 15, (38, 4): 11}, 'C': {(37, 5): 11, (37, 6): 15}, 'D': {(37, 5): 15, (37, 6): 12}}
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
v = Image.new('RGB', (5 * 230 + 10, 330), 'white'); d = ImageDraw.Draw(v)
for k, (n, ch) in enumerate(OPT.items()):
    a = A0.copy()
    for (y, x), c in ch.items(): a[y, x] = c
    im = Image.fromarray(a, 'P'); im.putpalette(pal)
    if n != 'nu': im.save(os.path.join(H, f'oog_{n}.png'), transparency=0)
    r = np.array(im.convert('RGBA')); r[a == 0, 3] = 0; bb = Image.new('RGBA', (64, 64), 'white'); bb.alpha_composite(Image.fromarray(r)); t = bb.convert('RGB')
    X = 10 + k * 230; d.text((X, 4), n, font=F, fill='black')
    v.paste(t.crop((2, 32, 18, 48)).resize((208, 208), Image.NEAREST), (X, 22))
    v.paste(t.resize((128, 128), Image.NEAREST).crop((0, 40, 80, 120)), (X, 240)); v.paste(t, (X + 100, 240))
v.save(os.path.join(H, 'vel.png'))
