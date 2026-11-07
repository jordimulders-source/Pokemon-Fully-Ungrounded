"""Vel: 1x-rij en 8x-rij met sprite r5 naast r4, Pidgeot, Picapau (af), Taillow, Raichu Gen 1 en de R2-render (bron).
Draaien: python3.11 vel.py [uit.png]"""
import sys
from PIL import Image, ImageDraw
G = '../../../../../../graphics/pokemon/'
def png(p, crop=None):
    im = Image.open(p)
    if im.mode == 'P' and 'transparency' not in im.info:
        im = im.convert('RGBA'); px = im.load(); bg = px[0, 0]
        for y in range(im.size[1]):
            for x in range(im.size[0]):
                if px[x, y] == bg: px[x, y] = (0, 0, 0, 0)
    im = im.convert('RGBA')
    return im.crop(crop) if crop else im
items = [('sprite r5', png('picapau_evo.png'), None), ('sprite r4', png('../r4/picapau_evo.png'), None),
         ('Pidgeot', png(G + 'pidgeot/anim_front.png', (0, 0, 64, 64)), None),
         ('Picapau (af)', png('../../../picapau/af/picapau.png'), None),
         ('Taillow', png(G + 'taillow/anim_front.png', (0, 0, 64, 64)), None),
         ('Raichu Gen 1', png('../../referenties/jordi_inspiratie_raichu_gen1.png').resize((64, 64), Image.NEAREST), None),
         ('R2-render (bron)', png('../../blender/r7pose/R2_1x.png'), png('../../blender/r7pose/R2_8x.png'))]
W8 = 512
v = Image.new('RGBA', (8 + len(items) * (W8 + 8), 16 + 72 + 16 + W8 + 8), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
for i, (t, im, groot) in enumerate(items):
    x = 8 + i * (W8 + 8)
    d.text((x, 2), t, fill=(0, 0, 0, 255)); v.alpha_composite(im, (x, 16))
    v.alpha_composite(groot if groot else im.resize((W8, W8), Image.NEAREST), (x, 104))
uit = sys.argv[1] if len(sys.argv) > 1 else 'vel.png'
v.convert('RGB').save(uit); print(uit, v.size)
