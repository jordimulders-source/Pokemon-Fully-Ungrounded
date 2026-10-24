#!/usr/bin/env python3
"""Uitsnede op schaal met raster en coordinaten: python3 crop.py uit.png x0 y0 x1 y1 [schaal] [frame]"""
import os, sys
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__))
x0, y0, x1, y1 = map(int, sys.argv[2:6]); S = int(sys.argv[6]) if len(sys.argv) > 6 else 12
f = int(sys.argv[7]) if len(sys.argv) > 7 else 0
im = Image.open(os.path.join(H, '..', 'anim_front.png')).convert('RGBA').crop((x0, y0 + 64 * f, x1 + 1, y1 + 1 + 64 * f))
b = Image.new('RGBA', im.size, (200, 220, 205, 255)); b.alpha_composite(im)
w, h = im.size; M = 22
big = Image.new('RGBA', (w * S + M, h * S + M), (255, 255, 255, 255))
big.paste(b.resize((w * S, h * S), Image.NEAREST), (M, M))
d = ImageDraw.Draw(big)
for i in range(w + 1):
    d.line([(M + i * S, M), (M + i * S, M + h * S)], fill=(160, 160, 160, 255))
    if i < w and (x0 + i) % 2 == 0: d.text((M + i * S + 1, 4), str((x0 + i) % 100), fill=(0, 0, 0, 255))
for j in range(h + 1):
    d.line([(M, M + j * S), (M + w * S, M + j * S)], fill=(160, 160, 160, 255))
    if j < h: d.text((2, M + j * S + 1), str(y0 + j), fill=(0, 0, 0, 255))
big.save(sys.argv[1])
