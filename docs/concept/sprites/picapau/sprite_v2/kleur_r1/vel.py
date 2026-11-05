"""vel.png: boven 8x render | Picapau | Taillow | Pikachu; onder 1x en 2x op twee achtergronden."""
from PIL import Image, ImageDraw
R = '../../../../../../graphics/pokemon/'
def spr(p):
    im = Image.open(p); return im.convert('RGBA').crop((0, 0, 64, 64))
def trans(im, key=(152, 208, 160)):
    px = im.load()
    for y in range(64):
        for x in range(64):
            if px[x, y][:3] == key: px[x, y] = (0, 0, 0, 0)
    return im
pic = trans(spr('picapau.png'))
tai = spr(R + 'taillow/anim_front.png'); pik = spr(R + 'pikachu/anim_front.png')
ren = Image.open('../../blender/B1/b1.png').convert('RGBA')
W = 512; v = Image.new('RGBA', (W * 4 + 50, W + 200), (232, 232, 232, 255)); d = ImageDraw.Draw(v)
for i, (im, naam) in enumerate([(ren, 'render B1 (8x)'), (pic, 'Picapau sprite_v2 r1'), (tai, 'Taillow'), (pik, 'Pikachu')]):
    big = im if im.size[0] == W else im.resize((W, W), Image.NEAREST)
    v.alpha_composite(big, (10 + i * (W + 10), 20)); d.text((14 + i * (W + 10), 4), naam, fill=(0, 0, 0))
y = W + 40
for j, bg in enumerate([(232, 232, 232, 255), (152, 208, 160, 255)]):
    x0 = 10 + j * 700
    v.paste(bg[:3], (x0, y, x0 + 660, y + 150))
    for k, im in enumerate([pic, tai, pik]):
        v.alpha_composite(im, (x0 + 10 + k * 70, y + 40))
        v.alpha_composite(im.resize((128, 128), Image.NEAREST), (x0 + 230 + k * 140, y + 10))
d.text((14, W + 26), '1x en 2x: Picapau, Taillow, Pikachu', fill=(0, 0, 0))
v.save('vel.png')
