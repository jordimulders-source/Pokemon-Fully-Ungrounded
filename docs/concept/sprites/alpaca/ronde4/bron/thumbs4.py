"""Drie silhouetten voor ronde 4: A dekking (nabije handschoen opgeheven, gekozen als
frame 1), B staand op beide handschoenen (zoals ronde 3), C stoot (frame 2).
Kop zonder handwerk (alleen de vormen). python3 thumbs4.py <uitmap>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
import alpaca4 as A
sil = [('A dekking (gekozen f1)', A.frame().idx), ('B staand op handschoenen', A.frame(stand=True).idx),
       ('C stoot (f2)', A.frame(f2=True).idx)]
Z = 4
W = 3 * (64 * Z + 8) + 8 + 3 * 72
sheet = Image.new('RGB', (W, 64 * Z + 30), (246, 244, 236)); d = ImageDraw.Draw(sheet)
for i, (n, a) in enumerate(sil):
    im = Image.fromarray(np.where(a[..., None] > 0, [20, 20, 20], [255, 255, 255]).astype(np.uint8))
    x = 8 + i * (64 * Z + 8)
    d.text((x, 4), n, fill=(120, 20, 20))
    sheet.paste(im.resize((64 * Z, 64 * Z), Image.NEAREST), (x, 18))
    x1 = 3 * (64 * Z + 8) + 8 + i * 72
    sheet.paste(im, (x1, 18)); d.text((x1, 86), n[0] + ' 1x', fill=(0, 0, 0))
sheet.save(os.path.join(sys.argv[1], 'thumbnails.png')); print('ok')
