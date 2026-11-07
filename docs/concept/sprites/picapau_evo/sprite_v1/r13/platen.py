"""r13-platen: vel.png. Boven: kop op 8x (r13, r12, Raichu Gen 1-kop). Onder: hele sprite op 1x (r13, r12, Raichu Gen 1).
Draaien: python3.11 platen.py"""
from PIL import Image, ImageDraw
rai = Image.open('../../referenties/jordi_inspiratie_raichu_gen1.png').convert('RGBA').resize((64, 64), Image.NEAREST)
ims = [('r13', Image.open('picapau_evo.png').convert('RGBA'), (6, 0, 50, 18)), ('r12', Image.open('../r12/picapau_evo.png').convert('RGBA'), (6, 0, 50, 18)),
       ('Raichu Gen 1 (Jordi)', rai, (20, 0, 64, 20))]
W = 44 * 8
v = Image.new('RGBA', (8 + 3 * (W + 8), 16 + 20 * 8 + 16 + 72), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
for i, (t, im, c) in enumerate(ims):
    x = 8 + i * (W + 8); k = im.crop(c)
    d.text((x, 2), t + ' (kop 8x, eronder 1x)', fill=(0, 0, 0, 255)); v.alpha_composite(k.resize((k.size[0] * 8, k.size[1] * 8), Image.NEAREST), (x, 16))
    v.alpha_composite(im, (x, 16 + 20 * 8 + 8))
v.convert('RGB').save('vel.png'); print('vel.png', v.size)
