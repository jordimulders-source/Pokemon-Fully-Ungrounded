#!/usr/bin/env python3
"""render.py raster.txt uit.png [x0 y0 x1 y1 schaal] : groot zonder raster + 3x + 1x (wit en groen)."""
import sys, tools as T
from PIL import Image
g = T.read_txt(sys.argv[1])
box = tuple(map(int, sys.argv[3:7])) if len(sys.argv) > 6 else (6, 16, 60, 56)
s = int(sys.argv[7]) if len(sys.argv) > 7 else 8
im = T.rgba(g, (205, 220, 205, 255)).crop(box)
w, h = im.size
W = Image.new('RGBA', (w * s, h * s + h * 3 + 10), (255, 255, 255, 255))
W.paste(im.resize((w * s, h * s), Image.NEAREST), (0, 0))
im1 = T.rgba(g, (255, 255, 255, 255)).crop(box)
W.paste(im1.resize((w * 3, h * 3), Image.NEAREST), (0, h * s + 5))
W.paste(im1, (w * 3 + 10, h * s + 5 + h))
W.paste(im.resize((w * 3, h * 3), Image.NEAREST), (w * 3 + 20 + w, h * s + 5))
W.paste(im, (w * 6 + 30 + w, h * s + 5 + h))
W.save(sys.argv[2])
