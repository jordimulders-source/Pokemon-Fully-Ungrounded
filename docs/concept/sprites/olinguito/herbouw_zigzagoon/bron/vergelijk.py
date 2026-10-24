#!/usr/bin/env python3
"""compare.png: resultaat | Zigzagoon (basis) | ronde 23 | Galar-Linoone, op 3x (boven) en 1x (onder), licht en donker.
Gebruik: python3 vergelijk.py [uit.png] [frame]"""
import os, sys
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); M = os.path.join(H, '..')
R = os.path.abspath(os.path.join(M, '..', '..', '..', '..', '..'))
uit = sys.argv[1] if len(sys.argv) > 1 else os.path.join(M, 'compare.png')
f = int(sys.argv[2]) if len(sys.argv) > 2 else 0
bronnen = [('herbouw', os.path.join(M, 'anim_front.png'), f), ('Zigzagoon (basis)', os.path.join(R, 'graphics/pokemon/zigzagoon/anim_front.png'), 0),
           ('ronde 23', os.path.join(M, '..', 'ronde23', 'anim_front.png'), 0), ('Galar-Linoone', os.path.join(M, '..', 'referenties', 'galar_linoone_front.png'), 0)]
ims = []
for n, p, fr in bronnen:
    raw = Image.open(p); raw.info['transparency'] = 0
    im = raw.convert('RGBA').crop((0, 64 * fr, 64, 64 * fr + 64))
    ims.append((n, im))
achter = [(152, 208, 160, 255), (48, 48, 56, 255)]
W = 4 * (192 + 12) + 12; Hh = 18 + 2 * 192 + 24 + 2 * 64 + 30
C = Image.new('RGBA', (W, Hh), (255, 255, 255, 255)); d = ImageDraw.Draw(C)
for i, (n, im) in enumerate(ims):
    x = 12 + i * 204
    d.text((x, 3), n, fill=(0, 0, 0, 255))
    for j, bg in enumerate(achter):
        b = Image.new('RGBA', (64, 64), bg); b.alpha_composite(im)
        C.paste(b.resize((192, 192), Image.NEAREST), (x, 18 + j * 192))
        C.paste(b, (x + j * 70, 18 + 2 * 192 + 24))
d.text((12, 18 + 2 * 192 + 8), '1x (licht en donker)', fill=(0, 0, 0, 255))
C.save(uit)
print(uit)
