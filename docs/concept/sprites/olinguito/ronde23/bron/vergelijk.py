#!/usr/bin/env python3
"""compare.png: ronde 22 | ronde 23 | Galar-Linoone, op 1x en 3x (hele sprite) en 8x (verre voorpoot)."""
from PIL import Image, ImageDraw
import os
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, '..', '..')
ims = [Image.open(os.path.join(R, p)).convert('RGBA').crop((0, 0, 64, 64)) for p in
       ('ronde22/anim_front.png', 'ronde23/anim_front.png', 'referenties/galar_linoone_front.png')]
bg = (152, 208, 160, 255)
def flat(im):
    o = Image.new('RGBA', im.size, bg); o.alpha_composite(im); return o
ims = [flat(i) for i in ims]
crops = [ims[0].crop((6, 34, 30, 56)), ims[1].crop((6, 34, 30, 56)), ims[2].crop((4, 36, 28, 58))]
W = 3 * (24 * 8) + 4 * 10
c = Image.new('RGBA', (W, 10 + 64 + 10 + 192 + 10 + 22 * 8 + 24), (255, 255, 255, 255))
d = ImageDraw.Draw(c)
for i, (im, cr, t) in enumerate(zip(ims, crops, ('ronde 22', 'ronde 23', 'Galar-Linoone'))):
    x = 10 + i * (24 * 8 + 10)
    c.paste(im, (x, 10)); c.paste(im.resize((192, 192), 0), (x, 84))
    c.paste(cr.resize((24 * 8, 22 * 8), 0), (x, 286)); d.text((x, 286 + 22 * 8 + 6), t, fill=(0, 0, 0, 255))
c.save(os.path.join(R, 'ronde23', 'compare.png'))
