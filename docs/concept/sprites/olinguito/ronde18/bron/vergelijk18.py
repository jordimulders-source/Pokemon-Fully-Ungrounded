#!/usr/bin/env python3
"""compare.png: ronde 16 | ronde 18 (1 px) | ronde 18 (2 px); boven 1x (frame 1+2), onder 6x kop (frame 1)."""
from PIL import Image, ImageDraw
import os
H = os.path.dirname(os.path.abspath(__file__))
P = [('ronde 16', '../../ronde16/anim_front.png'), ('r18 1 px', '../anim_front.png'),
     ('r18 2 px', '../variant_2px/anim_front.png')]
BG = (232, 232, 224)
KOP = (2, 20, 38, 44)  # x0,y0,x1,y1 uitsnede kop frame 1
kw, kh = (KOP[2]-KOP[0])*6, (KOP[3]-KOP[1])*6
colw = max(kw, 140) + 16
W, Hh = colw*len(P), 18 + 64 + 12 + kh + 12
img = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(img)
for i, (naam, p) in enumerate(P):
    s = Image.open(os.path.join(H, p)).convert('RGBA')
    pal = Image.open(os.path.join(H, p)).getpalette()[:3]
    px = s.load()
    for y in range(s.height):
        for x in range(s.width):
            if px[x, y][:3] == tuple(pal): px[x, y] = (0, 0, 0, 0)
    x0 = i*colw + 8
    d.text((x0, 4), naam, fill=(0, 0, 0))
    img.paste(s.crop((0, 0, 64, 64)), (x0, 18), s.crop((0, 0, 64, 64)))
    img.paste(s.crop((0, 64, 64, 128)), (x0+68, 18), s.crop((0, 64, 64, 128)))
    k = s.crop(KOP).resize((kw, kh), Image.NEAREST)
    img.paste(k, (x0, 18+64+12), k)
img.save(os.path.join(H, '../compare.png'))
