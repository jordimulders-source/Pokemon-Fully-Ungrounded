"""Vel: 1x-rij en 8x-rij met de sprite naast Picapau (af), Raichu Gen 1, Taillow en de C3-render. python3.11 vel.py"""
from PIL import Image, ImageDraw
def png(p, crop=None):
    im = Image.open(p)
    if im.mode == 'P' and 'transparency' not in im.info:
        im = im.convert('RGBA'); px = im.load(); bg = px[0, 0]
        for y in range(im.size[1]):
            for x in range(im.size[0]):
                if px[x, y] == bg: px[x, y] = (0, 0, 0, 0)
    im = im.convert('RGBA')
    return im.crop(crop) if crop else im
items = [('sprite v1', png('picapau_evo.png')),
         ('Picapau (af)', png('../../picapau/af/picapau.png')),
         ('Raichu Gen 1', png('../referenties/jordi_inspiratie_raichu_gen1.png').resize((64, 64), Image.NEAREST)),
         ('Taillow', png('../../../../../graphics/pokemon/taillow/anim_front.png', (0, 0, 64, 64))),
         ('C3-render', png('../blender/r3/C3_1x.png'))]
W8 = 512
v = Image.new('RGBA', (8 + len(items) * (W8 + 8), 16 + 72 + 16 + W8 + 8), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
for i, (t, im) in enumerate(items):
    x = 8 + i * (W8 + 8)
    d.text((x, 2), t, fill=(0, 0, 0, 255)); v.alpha_composite(im, (x, 16))
    big = Image.open('../blender/r3/C3_8x.png').convert('RGBA') if t == 'C3-render' else im.resize((W8, W8), Image.NEAREST)
    v.alpha_composite(big, (x, 104))
v.convert('RGB').save('vel.png'); print('vel.png', v.size)
