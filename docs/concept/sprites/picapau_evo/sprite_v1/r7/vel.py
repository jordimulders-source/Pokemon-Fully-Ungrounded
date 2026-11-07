"""Vel r7: 1x-rij en 8x-rij met sprite r7 naast r6, Fearow, Pidgeot, Picapau (af) en Raichu Gen 1. Draaien: python3.11 vel.py [uit.png]"""
import sys
from PIL import Image, ImageDraw
from ref_snavels import png, G
items = [('sprite r7', png('picapau_evo.png')), ('sprite r6', png('../r6/picapau_evo.png')),
         ('Fearow', png(G + 'fearow/anim_front.png')), ('Pidgeot', png(G + 'pidgeot/anim_front.png')),
         ('Picapau (af)', png('../../../picapau/af/picapau.png')),
         ('Raichu Gen 1 (Jordi)', Image.open('../../referenties/jordi_inspiratie_raichu_gen1.png').convert('RGBA').resize((64, 64), Image.NEAREST))]
W8 = 512
v = Image.new('RGBA', (8 + len(items) * (W8 + 8), 16 + 72 + W8 + 8), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
for i, (t, im) in enumerate(items):
    x = 8 + i * (W8 + 8)
    d.text((x, 2), t, fill=(0, 0, 0, 255)); v.alpha_composite(im, (x, 16))
    v.alpha_composite(im.resize((W8, W8), Image.NEAREST), (x, 88))
uit = sys.argv[1] if len(sys.argv) > 1 else 'vel.png'
v.convert('RGB').save(uit); print(uit, v.size)
