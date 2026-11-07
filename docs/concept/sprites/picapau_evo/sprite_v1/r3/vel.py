"""Vel: 1x-rij en 8x-rij met sprite r3 naast r2, Picapau (af), Taillow, Staraptor, Raichu Gen 1 en de r5-render.
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
items = [('sprite r3', png('picapau_evo.png')), ('sprite r2', png('../r2/picapau_evo.png')),
         ('Picapau (af)', png('../../../picapau/af/picapau.png')), ('Taillow', png(G + 'taillow/anim_front.png', (0, 0, 64, 64))),
         ('Staraptor', png(G + 'staraptor/anim_front.png', (0, 0, 64, 64))),
         ('Raichu Gen 1', png('../../referenties/jordi_inspiratie_raichu_gen1.png').resize((64, 64), Image.NEAREST)),
         ('r5-render (bron)', png('../../blender/r5/R5_1x.png'))]
W8 = 512
v = Image.new('RGBA', (8 + len(items) * (W8 + 8), 16 + 72 + 16 + W8 + 8), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
for i, (t, im) in enumerate(items):
    x = 8 + i * (W8 + 8)
    d.text((x, 2), t, fill=(0, 0, 0, 255)); v.alpha_composite(im, (x, 16))
    big = im.resize((W8, W8), Image.NEAREST) if t != 'r5-render (bron)' else png('../../blender/r5/R5_8x.png')
    v.alpha_composite(big, (x, 104))
uit = sys.argv[1] if len(sys.argv) > 1 else 'vel.png'
v.convert('RGB').save(uit); print(uit, v.size)
