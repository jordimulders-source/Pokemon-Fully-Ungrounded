#!/usr/bin/env python3
"""Werkvoorbeeld: Zigzagoon | overlay (olinguito over halfdoorzichtige basis) | resultaat, op 8x met raster.
Gebruik: python3 preview.py uit.png [frame]"""
import os, sys
from PIL import Image, ImageDraw

H = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(H, '..', '..', '..', '..', '..', '..'))
f = int(sys.argv[2]) if len(sys.argv) > 2 else 0
Z = Image.open(os.path.join(R, 'graphics/pokemon/zigzagoon/anim_front.png')).convert('RGBA').crop((0, 64 * f, 64, 64 * f + 64))
O = Image.open(os.path.join(H, '..', 'anim_front.png')).convert('RGBA').crop((0, 64 * f, 64, 64 * f + 64))
bg = (200, 220, 205, 255)


def schoon(im):
    b = Image.new('RGBA', (64, 64), bg)
    b.alpha_composite(im)
    return b


zb = Image.new('RGBA', (64, 64), bg)
zh = Z.copy(); zh.putalpha(Z.getchannel('A').point(lambda a: 90 if a else 0))
zb.alpha_composite(zh)
ov = zb.copy(); oh = O.copy(); oh.putalpha(O.getchannel('A').point(lambda a: 200 if a else 0)); ov.alpha_composite(oh)
S = 8
W = Image.new('RGBA', (64 * S * 3 + 40, 64 * S), (255, 255, 255, 255))
for i, im in enumerate([schoon(Z), ov, schoon(O)]):
    big = im.resize((64 * S, 64 * S), Image.NEAREST)
    d = ImageDraw.Draw(big)
    for k in range(0, 64, 4):
        c = (150, 150, 150, 255) if k % 8 == 0 else (215, 215, 215, 255)
        d.line([(k * S, 0), (k * S, 64 * S)], fill=c); d.line([(0, k * S), (64 * S, k * S)], fill=c)
    W.paste(big, (i * (64 * S + 20), 0))
W.save(sys.argv[1])
