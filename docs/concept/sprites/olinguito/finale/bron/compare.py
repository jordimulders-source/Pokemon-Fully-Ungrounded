#!/usr/bin/env python3
"""compare.py : finale (frame 1 en 2) naast ronde 23 en 6 echte fase-1-sprites, op 3x en 1x -> ../compare.png"""
import sys, tools as T
from PIL import Image, ImageDraw
sys.path.insert(0, '/home/user/projectgrounded/docs/lessen/vormstudie/tools')
from lib import load
items = [('finale f1', T.rgba(T.read_png(T.H + '/../anim_front.png', 0))), ('finale f2', T.rgba(T.read_png(T.H + '/../anim_front.png', 1))),
         ('ronde 23', T.rgba(T.read_png(T.OL + '/ronde23/anim_front.png', 0)))]
for n, gba in [('poochyena', 1), ('zigzagoon', 1), ('cyndaquil', 1), ('growlithe', 1), ('nickit', 0), ('purrloin', 0)]:
    items.append((n, load(n, bool(gba))))
s = 3; w = 64 * s
W = Image.new('RGB', (len(items) * w, w + 16 + 64 + 16), (255, 255, 255)); d = ImageDraw.Draw(W)
for i, (n, im) in enumerate(items):
    bg = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); bg.alpha_composite(im)
    W.paste(bg.resize((w, w), Image.NEAREST).convert('RGB'), (i * w, 0))
    W.paste(bg.convert('RGB'), (i * w + (w - 64) // 2, w + 14))
    d.text((i * w + 4, w + 1), n, fill=(200, 0, 120) if n.startswith('finale') else (0, 0, 0))
W.save(T.H + '/../compare.png')
