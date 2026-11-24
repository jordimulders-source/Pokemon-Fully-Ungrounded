# vel: r7 (oog b) 8x | r8 p1 8x | r8 p2 8x | model verkleind 8x; close-ups 12x (lijf/lens, antennes/bolletjes) r7 naast r8;
# 1x op licht en donker naast Magnemite/Metang/Claydol.  Draaien vanuit deze map: python3 vel.py
import numpy as np
from PIL import Image, ImageDraw
G = '../../../../../../graphics/pokemon/'
def rgba(p):
    im = Image.open(p)
    if im.mode == 'P':
        a = np.array(im); r = np.array(im.convert('RGBA')); r[a == 0, 3] = 0; return Image.fromarray(r)
    return im.convert('RGBA')
def op(im, bg=(255, 255, 255)):
    b = Image.new('RGBA', im.size, bg + (255,)); b.alpha_composite(im); return b.convert('RGB')
def ref(n):
    im = Image.open(G + n + '/anim_front.png'); a = np.array(im)[:64]; r = np.array(im.convert('RGBA'))[:64]
    r[a == 0, 3] = 0; return Image.fromarray(r)
R7 = rgba('../../eindkeuring_r6/r7/oog_b.png'); P1 = rgba('sprite_p1.png'); P2 = rgba('sprite_p2.png')
M = Image.open('../../keuring_r5_80b/model64.png').convert('RGBA')
vel = Image.new('RGB', (4 * 522, 30 + 512 + 30 + 12 * 30 + 40 + 2 * 74 + 30), 'white'); d = ImageDraw.Draw(vel)
for i, (t, im) in enumerate([('r7 (oog b) 8x', R7), ('r8 p1 (pupil 1 links) 8x', P1), ('r8 p2 (1 links + 1 omlaag) 8x', P2), ('model panelen_80b verkleind 8x', M)]):
    vel.paste(op(im).resize((512, 512), Image.NEAREST), (i * 522, 30)); d.text((i * 522, 10), t, fill='black')
y0 = 30 + 512 + 30
xx = 0
for t, box in [('lijf/lens', (10, 17, 40, 47)), ('antennes/bolletjes', (20, 6, 52, 23))]:
    for nm, im in (('r7', R7), ('r8 p1', P1)):
        c = op(im.crop(box)).resize(((box[2] - box[0]) * 12, (box[3] - box[1]) * 12), Image.NEAREST)
        vel.paste(c, (xx, y0)); d.text((xx, y0 - 14), '%s %s 12x' % (nm, t), fill='black'); xx += c.width + 10
y1 = y0 + 12 * 30 + 40
reeks = [('r7', R7), ('r8 p1', P1), ('r8 p2', P2), ('magnemite', ref('magnemite')), ('metang', ref('metang')), ('claydol', ref('claydol'))]
for j, bg in enumerate([(248, 248, 248), (40, 40, 48)]):
    for k, (t, im) in enumerate(reeks):
        vel.paste(op(im, bg), (k * 74, y1 + j * 74))
        if j == 1: d.text((k * 74, y1 + 2 * 74), t, fill='black')
vel.save('vel.png')
