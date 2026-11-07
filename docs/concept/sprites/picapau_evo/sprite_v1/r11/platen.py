"""r11-platen: vel.png. Boven: kop op 8x (r11, P5, Raichu Gen 1-kop). Onder: hele sprite op 1x en 8x (r11, P5, Raichu Gen 1).
Draaien: python3.11 platen.py"""
from PIL import Image, ImageDraw
rai = Image.open('../../referenties/jordi_inspiratie_raichu_gen1.png').convert('RGBA').resize((64, 64), Image.NEAREST)
ims = [('r11', Image.open('picapau_evo.png').convert('RGBA')), ('P5', Image.open('../probeersels/P5.png').convert('RGBA')), ('Raichu Gen 1 (Jordi)', rai)]
KOP = {'r11': (6, 0, 48, 18), 'P5': (6, 0, 48, 18), 'Raichu Gen 1 (Jordi)': (20, 0, 64, 20)}
W = 512; KW = 44 * 8
v = Image.new('RGBA', (8 + 3 * (W + 8), 16 + 20 * 8 + 16 + 72 + W + 8), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
for i, (t, im) in enumerate(ims):
    x = 8 + i * (W + 8); c = KOP[t]; k = im.crop(c)
    d.text((x, 2), t + ' (kop 8x)', fill=(0, 0, 0, 255)); v.alpha_composite(k.resize((k.size[0] * 8, k.size[1] * 8), Image.NEAREST), (x, 16))
    y = 16 + 20 * 8 + 16
    v.alpha_composite(im, (x, y)); v.alpha_composite(im.resize((W, W), Image.NEAREST), (x, y + 72))
v.convert('RGB').save('vel.png'); print('vel.png', v.size)
