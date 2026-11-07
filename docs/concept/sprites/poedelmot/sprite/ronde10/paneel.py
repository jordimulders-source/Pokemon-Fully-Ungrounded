"""Ronde 10: paneel.png = schets over ronde 9, schets over ronde 10, masker (geel = binnen de vormen, met speling) over
ronde 10, ronde 10 los (alle 8x), en de onderkant op 16x (schets over ronde 10, ronde 10 los)."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from overlay import over
from masker import maskers
HERE = os.path.dirname(os.path.abspath(__file__))
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
r9 = os.path.join(HERE, '../ronde9/anim_front.png'); r10 = os.path.join(HERE, 'anim_front.png')
los = lambda z: Image.open(r10).crop((0, 0, 64, 64)).convert('RGB').resize((64 * z, 64 * z), Image.NEAREST)
def met_masker(z=8):
    a = np.array(over(r10, z)); M = maskers(); m = M['links'] | M['midden'] | M['rechts']
    for y in range(64):
        for x in range(64):
            if m[y, x]:
                for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    q, p = y + dy, x + dx
                    if not (0 <= q < 64 and 0 <= p < 64 and m[q, p]):  # randlijn van het masker in geel
                        if dx: a[y * z:(y + 1) * z, (x * z if dx < 0 else (x + 1) * z - 2):(x * z + 2 if dx < 0 else (x + 1) * z)] = (240, 200, 0)
                        else: a[(y * z if dy < 0 else (y + 1) * z - 2):(y * z + 2 if dy < 0 else (y + 1) * z), x * z:(x + 1) * z] = (240, 200, 0)
    return Image.fromarray(a)
items = [('schets over ronde 9 (8x)', over(r9)), ('schets over ronde 10 (8x)', over(r10)),
         ('masker (geel, 1 px speling) over ronde 10', met_masker()), ('ronde 10 los (8x)', los(8))]
onder = [('16x onderkant: schets + masker over ronde 10', met_masker(16).crop((0, 36 * 16, 52 * 16, 61 * 16))),
         ('16x onderkant: ronde 10 los', los(16).crop((0, 36 * 16, 52 * 16, 61 * 16)))]
W = max(sum(i.width + 10 for _, i in items), sum(i.width + 10 for _, i in onder)) + 10
P = Image.new('RGB', (W, 512 + 30 + 400 + 40), (236, 236, 240)); d = ImageDraw.Draw(P); x = 10
for t, i in items: d.text((x, 6), t, fill=(0, 0, 0), font=F); P.paste(i, (x, 28)); x += i.width + 10
x = 10
for t, i in onder: d.text((x, 548), t, fill=(0, 0, 0), font=F); P.paste(i, (x, 570)); x += i.width + 10
P.save(os.path.join(HERE, 'paneel.png'))
