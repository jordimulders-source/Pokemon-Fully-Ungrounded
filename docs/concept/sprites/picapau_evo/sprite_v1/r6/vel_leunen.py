"""Vel leunen: r5 en r6 naast elkaar en Raichu Gen 1, op 1x en 8x, met een hulplijn van heup (24,38) naar het kopmidden.
Draaien: python3.11 vel_leunen.py"""
from PIL import Image, ImageDraw
def png(p):
    return Image.open(p).convert('RGBA')
items = [('r5', png('../r5/picapau_evo.png'), (24, 38), (20, 8)), ('r6 (8 graden achterover)', png('picapau_evo.png'), (24, 38), (24, 8)),
         ('Raichu Gen 1', png('../../referenties/jordi_inspiratie_raichu_gen1.png').resize((64, 64), Image.NEAREST), None, None)]
W = 512; v = Image.new('RGBA', (8 + len(items) * (W + 8), 16 + 72 + W + 8), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
for i, (t, im, a, b) in enumerate(items):
    x = 8 + i * (W + 8); d.text((x, 2), t, fill=(0, 0, 0, 255)); v.alpha_composite(im, (x, 16))
    v.alpha_composite(im.resize((W, W), Image.NEAREST), (x, 88))
    if a: d.line([(x + a[0] * 8 + 4, 88 + a[1] * 8 + 4), (x + b[0] * 8 + 4, 88 + b[1] * 8 + 4)], fill=(0, 120, 255, 255), width=3)
v.convert('RGB').save('vel_leunen.png'); print('vel_leunen.png', v.size)
