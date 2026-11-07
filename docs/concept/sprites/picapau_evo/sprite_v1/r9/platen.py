"""r9-platen: vel.png (1x en 8x: r9, r7, Swellow, Pidgeotto, Picapau) en kop_closeup.png (kop r9 op 16x naast de kop van Swellow,
Pidgeotto en Picapau op 16x). Draaien: python3.11 platen.py"""
from PIL import Image, ImageDraw
from ref_snavels import png, vel, G
items = [('sprite r9', png('picapau_evo.png')), ('sprite r7', png('../r7/picapau_evo.png')), ('Swellow (hoofdbron kop)', png(G + 'swellow/anim_front.png')),
         ('Pidgeotto (aanvulling)', png(G + 'pidgeotto/anim_front.png')), ('Picapau (af)', png('../../../picapau/af/picapau.png'))]
W8 = 512
v = Image.new('RGBA', (8 + len(items) * (W8 + 8), 16 + 72 + W8 + 8), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
for i, (t, im) in enumerate(items):
    x = 8 + i * (W8 + 8)
    d.text((x, 2), t, fill=(0, 0, 0, 255)); v.alpha_composite(im, (x, 16)); v.alpha_composite(im.resize((W8, W8), Image.NEAREST), (x, 88))
v.convert('RGB').save('vel.png'); print('vel.png', v.size)
vel([('kop r9', 'picapau_evo.png', (6, 0, 40, 18)), ('kop r7', '../r7/picapau_evo.png', (6, 0, 40, 18)),
     ('Swellow', G + 'swellow/anim_front.png', (3, 7, 31, 25)), ('Pidgeotto', G + 'pidgeotto/anim_front.png', (13, 6, 37, 24)),
     ('Picapau', '../../../picapau/af/picapau.png', (10, 8, 34, 26))], 16, 'kop_closeup.png')
