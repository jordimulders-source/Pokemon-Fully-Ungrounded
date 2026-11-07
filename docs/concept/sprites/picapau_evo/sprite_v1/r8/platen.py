"""r8-platen: kop_A.png en kop_B.png (kop op 16x naast de snavels van Picapau, Staraptor en Pidgeot op 16x)
en vel.png (1x en 8x: A, B en r7). Draaien: python3.11 platen.py"""
from PIL import Image, ImageDraw
from ref_snavels import SNAVELS, vel, png
kies = dict((t, (t, f, c)) for t, f, c in SNAVELS)
refs = [kies[n] for n in ('Picapau', 'Staraptor', 'Pidgeot')]
for V in 'AB':
    vel([(f'kop r8{V}', f'picapau_evo_{V}.png', (4, 0, 34, 18))] + refs, 16, f'kop_{V}.png')
items = [('r8 A (familie Picapau)', png('picapau_evo_A.png')), ('r8 B (Gen 3-stijl)', png('picapau_evo_B.png')), ('r7', png('../r7/picapau_evo.png'))]
W8 = 512
v = Image.new('RGBA', (8 + len(items) * (W8 + 8), 16 + 72 + W8 + 8), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
for i, (t, im) in enumerate(items):
    x = 8 + i * (W8 + 8)
    d.text((x, 2), t, fill=(0, 0, 0, 255)); v.alpha_composite(im, (x, 16)); v.alpha_composite(im.resize((W8, W8), Image.NEAREST), (x, 88))
v.convert('RGB').save('vel.png'); print('vel.png', v.size)
