#!/usr/bin/env python3
"""zelfcheck.png: uitsnedes op 8x (frame 1) van de kop, elke poot en de staart, met coordinaten.
Gebruik: python3 zelfcheck.py [uit.png]"""
import os, sys
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); M = os.path.join(H, '..')
uit = sys.argv[1] if len(sys.argv) > 1 else os.path.join(M, 'zelfcheck.png')
im = Image.open(os.path.join(M, 'anim_front.png')).convert('RGBA').crop((0, 0, 64, 64))
DELEN = [('kop', (5, 19, 30, 43)), ('nabije voorpoot', (14, 38, 29, 51)), ('verre voorpoot', (7, 39, 22, 50)),
         ('nabije achterpoot', (31, 34, 43, 49)), ('verre achterpoot', (38, 38, 47, 48)), ('staart (J)', (42, 23, 58, 48))]
S = 12; M2 = 22; pad = 16
tiles = []
for naam, (x0, y0, x1, y1) in DELEN:
    c = im.crop((x0, y0, x1 + 1, y1 + 1)); b = Image.new('RGBA', c.size, (200, 220, 205, 255)); b.alpha_composite(c)
    w, h = c.size; t = Image.new('RGBA', (w * S + M2, h * S + M2 + 14), (255, 255, 255, 255))
    t.paste(b.resize((w * S, h * S), Image.NEAREST), (M2, M2 + 14)); d = ImageDraw.Draw(t)
    d.text((2, 0), naam, fill=(0, 0, 0, 255))
    for i in range(w + 1):
        d.line([(M2 + i * S, M2 + 14), (M2 + i * S, M2 + 14 + h * S)], fill=(170, 170, 170, 255))
        if i < w and (x0 + i) % 2 == 0: d.text((M2 + i * S, 12), str(x0 + i), fill=(90, 90, 90, 255))
    for j in range(h + 1):
        d.line([(M2, M2 + 14 + j * S), (M2 + w * S, M2 + 14 + j * S)], fill=(170, 170, 170, 255))
        if j < h and (y0 + j) % 2 == 0: d.text((1, M2 + 14 + j * S), str(y0 + j), fill=(90, 90, 90, 255))
    tiles.append(t)
W = sum(t.width for t in tiles[:3]) + 4 * pad; Hh = max(t.height for t in tiles[:3]) + max(t.height for t in tiles[3:]) + 3 * pad
C = Image.new('RGBA', (max(W, sum(t.width for t in tiles[3:]) + 4 * pad), Hh), (255, 255, 255, 255))
x = pad
for t in tiles[:3]: C.paste(t, (x, pad)); x += t.width + pad
x = pad; y = pad * 2 + max(t.height for t in tiles[:3])
for t in tiles[3:]: C.paste(t, (x, y)); x += t.width + pad
C.save(uit); print(uit)
