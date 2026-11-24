# vel beste4.png: Dundragoon | Princadee | Zapacha | Skinguin | onze r17, 4x, met paletladders (gesorteerd op tintgroep en L)
# en per sprite: aandeel zwart(achtig) L<35, aandeel lijntint. Draaien vanuit docs/concept/sprites/bibarel_evo.
import numpy as np, colorsys
from PIL import Image, ImageDraw
from collections import Counter
S = '/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/'
P = [('Dundragoon', S+'dundragoon/af/dundragoon.png'), ('Princadee', S+'awki/af/awki.png'), ('Zapacha', S+'viscacha/af/viscacha.png'),
     ('Skinguin', S+'skinguin/af/skinguin.png'), ('ons r17', S+'bibarel_evo/sprite_r17/sprite.png'), ('r18', S+'bibarel_evo/sprite_r18/sprite.png')]
Lf = lambda c: .299*c[0]+.587*c[1]+.114*c[2]
V = Image.new('RGB', (6*270+10, 22+256+16+16*44+10), 'white'); d = ImageDraw.Draw(V)
for i, (n, p) in enumerate(P):
    im = Image.open(p).convert('RGBA').crop((0, 0, 64, 64)); a = np.asarray(im)
    c = Counter(tuple(int(v) for v in px[:3]) for row in a for px in row if px[3] > 128); tot = sum(c.values())
    bg = Image.new('RGBA', (64, 64), (152, 208, 160, 255)); bg.alpha_composite(im)
    V.paste(bg.convert('RGB').resize((256, 256), Image.NEAREST), (10+i*270, 22)); d.text((10+i*270, 6), n, fill='black')
    def key(k):
        h, s, v = colorsys.rgb_to_hsv(*(x/255 for x in k)); return (round(h*12) % 12 if s > .15 and Lf(k) > 35 else 99, Lf(k))
    y = 22+256+16
    for k in sorted(c, key=key):
        h, s, v = colorsys.rgb_to_hsv(*(x/255 for x in k))
        d.rectangle([10+i*270, y, 10+i*270+36, y+36], fill=k)
        d.text((52+i*270, y+4), f'h{int(h*360)} s{int(s*100)} L{int(Lf(k))}', fill='black')
        d.text((52+i*270, y+18), f'{100*c[k]/tot:.0f}%', fill='black'); y += 42
V.save('stijl_gen123/beste4.png')
