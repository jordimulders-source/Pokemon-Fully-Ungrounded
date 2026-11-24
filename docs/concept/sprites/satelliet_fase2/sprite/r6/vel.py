# vel r6: r5_80b 8x | r6 8x | model verkleind 8x, reparatieplekken gemarkeerd (kleur per punt), plus 1x op licht en donker.
# Draaien vanuit sprite/:  python3 r6/vel.py
import sys
from PIL import Image, ImageDraw
sys.path.insert(0, 'r6')
from repareer import FIX

Z = 8
KLEUR = {1: (230, 0, 0), 2: (0, 150, 0), 3: (0, 90, 230), 4: (230, 140, 0), 5: (200, 0, 200), 6: (0, 170, 170), 'K': (120, 120, 120)}

def groot(pad, bg=(255, 255, 255)):
    im = Image.open(pad).convert('RGBA')
    b = Image.new('RGBA', im.size, bg + (255,)); b.alpha_composite(im)
    return b.convert('RGB').resize((64 * Z, 64 * Z), Image.NEAREST)

panelen = [('r5_80b 8x', groot('r5_80b/sprite.png')), ('r6 8x', groot('r6/sprite.png')),
           ('model panelen_80b verkleind 8x', Image.open('../keuring_r5_80b/model64.png').convert('RGB').resize((64 * Z, 64 * Z), Image.NEAREST))]
W = 3 * 64 * Z + 2 * 10 + 140
vel = Image.new('RGB', (W, 64 * Z + 40), 'white')
d = ImageDraw.Draw(vel)
for i, (t, p) in enumerate(panelen):
    ox = i * (64 * Z + 10)
    vel.paste(p, (ox, 30)); d.text((ox, 8), t, fill='black')
    for (x, y), (v, punt) in FIX.items():
        d.rectangle([ox + x * Z, 30 + y * Z, ox + x * Z + Z - 1, 30 + y * Z + Z - 1], outline=KLEUR[punt])
ox = 3 * (64 * Z + 10)
d.text((ox, 8), '1x', fill='black')
for j, bg in enumerate([(248, 248, 248), (40, 40, 48)]):
    for k, pad in enumerate(['r6/sprite.png', 'r6/oog_b.png']):
        im = Image.open(pad).convert('RGBA'); b = Image.new('RGBA', (64, 64), bg + (255,)); b.alpha_composite(im)
        vel.paste(b.convert('RGB'), (ox + k * 68, 30 + j * 70))
y = 30 + 150
for punt, kl in KLEUR.items():
    d.rectangle([ox, y, ox + 8, y + 8], outline=kl); d.text((ox + 14, y - 2), 'punt %s' % punt if punt != 'K' else 'KAN', fill='black'); y += 16
vel.save('r6/vel.png')
