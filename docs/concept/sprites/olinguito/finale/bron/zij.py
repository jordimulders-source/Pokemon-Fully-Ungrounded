#!/usr/bin/env python3
"""zij.py uit.png a.txt [b.txt ...] : rasters naast elkaar op 4x en 1x (wit), met echte sprites erbij als 'pokemon:naam'."""
import sys, tools as T
from PIL import Image
sys.path.insert(0, '/home/user/projectgrounded/docs/lessen/vormstudie/tools')
from lib import load
ims = []
for a in sys.argv[2:]:
    if a.startswith('pokemon:'):
        n = a.split(':')[1]; gba = not n.endswith('+')
        im = load(n.rstrip('+'), gba)
        bg = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); bg.alpha_composite(im); ims.append(bg)
    elif a.endswith('.png'):
        g = T.read_png(a, 0); ims.append(T.rgba(g, (255, 255, 255, 255)))
    else:
        ims.append(T.rgba(T.read_txt(a), (255, 255, 255, 255)))
s = 4
W = Image.new('RGBA', (len(ims) * 64 * s, 64 * s + 70), (255, 255, 255, 255))
for i, im in enumerate(ims):
    W.paste(im.resize((64 * s, 64 * s), Image.NEAREST), (i * 64 * s, 0))
    W.paste(im, (i * 64 * s + 96, 64 * s + 3))
W.save(sys.argv[1])
