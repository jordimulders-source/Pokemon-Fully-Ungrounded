"""Ronde 10: paneel.png = schets over ronde 10, schets over ronde 11, masker (geel = binnen de vormen, met speling) over
ronde 11, ronde 11 los (alle 8x), en de onderkant op 16x (schets over ronde 11, ronde 11 los)."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from overlay import over
from masker import maskers
HERE = os.path.dirname(os.path.abspath(__file__))
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
r10 = os.path.join(HERE, "../ronde10/anim_front.png"); r11 = os.path.join(HERE, "anim_front.png")
los = lambda z: Image.open(r11).crop((0, 0, 64, 64)).convert('RGB').resize((64 * z, 64 * z), Image.NEAREST)
def met_masker(z=8):
    a = np.array(over(r11, z)); M = maskers(); m = M['links'] | M['midden'] | M['rechts']
    for y in range(64):
        for x in range(64):
            if m[y, x]:
                for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    q, p = y + dy, x + dx
                    if not (0 <= q < 64 and 0 <= p < 64 and m[q, p]):  # randlijn van het masker in geel
                        if dx: a[y * z:(y + 1) * z, (x * z if dx < 0 else (x + 1) * z - 2):(x * z + 2 if dx < 0 else (x + 1) * z)] = (240, 200, 0)
                        else: a[(y * z if dy < 0 else (y + 1) * z - 2):(y * z + 2 if dy < 0 else (y + 1) * z), x * z:(x + 1) * z] = (240, 200, 0)
    return Image.fromarray(a)
items = [('schets over ronde 10 (8x)', over(r10)), ('schets over ronde 11 (8x)', over(r11)),
         ('masker (geel, 1 px speling) over ronde 11', met_masker()), ('ronde 11 los (8x)', los(8))]
onder = [('16x onderkant: schets + masker over ronde 11', met_masker(16).crop((0, 36 * 16, 52 * 16, 61 * 16))),
         ('16x onderkant: ronde 11 los', los(16).crop((0, 36 * 16, 52 * 16, 61 * 16)))]
W = max(sum(i.width + 10 for _, i in items), sum(i.width + 10 for _, i in onder)) + 10
P = Image.new('RGB', (W, 512 + 30 + 400 + 40), (236, 236, 240)); d = ImageDraw.Draw(P); x = 10
for t, i in items: d.text((x, 6), t, fill=(0, 0, 0), font=F); P.paste(i, (x, 28)); x += i.width + 10
x = 10
for t, i in onder: d.text((x, 548), t, fill=(0, 0, 0), font=F); P.paste(i, (x, 570)); x += i.width + 10
P.save(os.path.join(HERE, 'paneel.png'))
# aansluiting rechts op 16x naast Giratina's nabije achterpoten (16x)
G = os.path.join(HERE, '../../../../../../graphics/pokemon/giratina/anim_front.png')
crop = lambda p, b: Image.open(p).crop((0, 0, 64, 64)).convert('RGB').crop(b)
aan = [('aansluiting rechts ronde 10 (16x)', crop(os.path.join(HERE, '../ronde10/anim_front.png'), (28, 40, 44, 58)).resize((256, 288), Image.NEAREST)),
       ('aansluiting rechts ronde 11 (16x)', crop(r11, (28, 40, 44, 58)).resize((256, 288), Image.NEAREST)),
       ('Giratina nabije achterpoten (16x)', crop(G, (42, 38, 62, 60)).resize((320, 352), Image.NEAREST)),
       ('Giratina verre achterpoten (16x)', crop(G, (14, 48, 36, 60)).resize((352, 192), Image.NEAREST)),
       ('midden ronde 11 (16x)', crop(r11, (14, 48, 36, 60)).resize((352, 192), Image.NEAREST))]
Q = Image.new('RGB', (max(P.width, sum(i.width + 10 for _, i in aan) + 10), P.height + 400), (236, 236, 240))
Q.paste(P, (0, 0)); d = ImageDraw.Draw(Q); x = 10
for t, i in aan: d.text((x, P.height + 4), t, fill=(0, 0, 0), font=F); Q.paste(i, (x, P.height + 26)); x += i.width + 10
Q.save(os.path.join(HERE, 'paneel.png'))
