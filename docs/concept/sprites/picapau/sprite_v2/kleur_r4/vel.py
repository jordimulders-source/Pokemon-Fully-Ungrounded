"""vel.png: boven 8x render | r3 | r4 | Taillow | Pikachu; onder 1x en 2x op twee achtergronden."""
from PIL import Image, ImageDraw
R = '../../../../../../graphics/pokemon/'
def spr(p):
    return Image.open(p).convert('RGBA').crop((0, 0, 64, 64))
def trans(im, key=(152, 208, 160)):
    px = im.load()
    for y in range(64):
        for x in range(64):
            if px[x, y][:3] == key: px[x, y] = (0, 0, 0, 0)
    return im
r3 = trans(spr('../kleur_r3/picapau.png')); r4 = trans(spr('picapau.png'))
tai = spr(R + 'taillow/anim_front.png'); pik = spr(R + 'pikachu/anim_front.png')
ren = Image.open('../../blender/B1/b1.png').convert('RGBA')
W = 512; v = Image.new('RGBA', (W * 5 + 60, W + 200), (232, 232, 232, 255)); d = ImageDraw.Draw(v)
for i, (im, naam) in enumerate([(ren, 'render B1 (8x)'), (r3, 'sprite_v2 r3'), (r4, 'sprite_v2 r4'), (tai, 'Taillow'), (pik, 'Pikachu')]):
    big = im if im.size[0] == W else im.resize((W, W), Image.NEAREST)
    v.alpha_composite(big, (10 + i * (W + 10), 20)); d.text((14 + i * (W + 10), 4), naam, fill=(0, 0, 0))
y = W + 40
for j, bg in enumerate([(232, 232, 232, 255), (152, 208, 160, 255)]):
    x0 = 10 + j * 1300
    v.paste(bg[:3], (x0, y, x0 + 1000, y + 150))
    for k, im in enumerate([r3, r4, tai, pik]):
        v.alpha_composite(im, (x0 + 10 + k * 66, y + 40))
        v.alpha_composite(im.resize((128, 128), Image.NEAREST), (x0 + 290 + k * 140, y + 10))
d.text((14, W + 26), '1x en 2x: r3, r4, Taillow, Pikachu', fill=(0, 0, 0))
v.save('vel.png')
