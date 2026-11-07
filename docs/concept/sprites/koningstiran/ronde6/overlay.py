"""Overlay: Jordi's rode lijnen (krabbel_jordi_lijf_staf.png) via de uitlijning op ronde 5b en ronde 6, op 8x. Schrijft overlay.png. Draaien vanuit de repo-root."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(H)
sc, ox, oy = np.load(os.path.join(H, 'uitlijning.npy'))
k = np.array(Image.open(os.path.join(K, 'referenties/krabbel_jordi_lijf_staf.png')).convert('RGB')).astype(int)
red = (k[..., 0] > 190) & (k[..., 1] < 45) & (k[..., 2] < 55) & (k[..., 0] - k[..., 1] > 160)
Z = 8
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
crop = (8, 26, 44, 63)
W = Image.new('RGB', (2 * ((crop[2] - crop[0]) * Z + 20), (crop[3] - crop[1]) * Z + 30), (236, 232, 222))
d = ImageDraw.Draw(W)
ry, rx = np.nonzero(red)
for i, r in enumerate(('ronde5b', 'ronde6')):
    im = Image.open(os.path.join(K, r, 'sapa_inca.png')).convert('RGBA').resize((64 * Z, 64 * Z), Image.NEAREST)
    bg = Image.new('RGBA', im.size, (248, 248, 240, 255)); bg.alpha_composite(im)
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); px = lay.load()
    for x, y in zip(rx, ry):
        X = int((x - ox) / sc * Z); Y = int((y - oy) / sc * Z)
        if 0 <= X < 64 * Z and 0 <= Y < 64 * Z:
            px[X, Y] = (230, 0, 30, 255)
    bg.alpha_composite(lay)
    W.paste(bg.crop(tuple(c * Z for c in crop)).convert('RGB'), (10 + i * ((crop[2] - crop[0]) * Z + 20), 25))
    d.text((10 + i * ((crop[2] - crop[0]) * Z + 20), 5), f'{r} + rode lijnen van Jordi (8x)', font=F, fill=(20, 20, 24))
W.save(os.path.join(H, 'overlay.png'))
