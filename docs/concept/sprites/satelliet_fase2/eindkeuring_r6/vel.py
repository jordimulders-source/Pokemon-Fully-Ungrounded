# vel: r6 8x | r7 8x (omgetinte lijnpixels gemarkeerd) | model verkleind 8x, plus 1x naast Gen 3 op licht en donker.
# Draaien vanuit eindkeuring_r6/:  python3 vel.py
import numpy as np
from PIL import Image, ImageDraw
from omlijning import plan
Z = 8; G = '../../../../../graphics/pokemon/'
REF = ['magnemite', 'magneton', 'beldum', 'metang', 'claydol', 'lunatone']

def groot(pad, bg=(255, 255, 255)):
    im = Image.open(pad).convert('RGBA'); b = Image.new('RGBA', im.size, bg + (255,)); b.alpha_composite(im)
    return b.convert('RGB').resize((im.width * Z, im.height * Z), Image.NEAREST)

for n in ('sprite', 'oog_b'):
    groot('r7/%s.png' % n).save('r7/%s_8x.png' % n)
nieuw = plan(np.array(Image.open('../sprite/r6/sprite.png')))
panelen = [('r6 8x', groot('../sprite/r6/sprite.png')), ('r7 8x (omgetint gemarkeerd: groen)', groot('r7/sprite.png')),
           ('model panelen_80b verkleind 8x', Image.open('../keuring_r5_80b/model64.png').convert('RGB').resize((512, 512), Image.NEAREST))]
vel = Image.new('RGB', (3 * 522, 512 + 40 + 2 * 84 + 20), 'white'); d = ImageDraw.Draw(vel)
for i, (t, p) in enumerate(panelen):
    ox = i * 522; vel.paste(p, (ox, 30)); d.text((ox, 8), t, fill='black')
for (x, y) in nieuw:
    d.rectangle([522 + x * Z, 30 + y * Z, 522 + x * Z + Z - 1, 30 + y * Z + Z - 1], outline=(0, 200, 0))
def ref(n):
    a = Image.open(G + n + '/anim_front.png').convert('RGBA').crop((0, 0, 64, 64)); arr = np.array(a)
    arr[np.all(arr[:, :, :3] == arr[0, 0, :3], axis=2), 3] = 0
    return Image.fromarray(arr)
reeks = [('r6', Image.open('../sprite/r6/sprite.png').convert('RGBA')), ('r7', Image.open('r7/sprite.png').convert('RGBA')),
         ('r7 oog b', Image.open('r7/oog_b.png').convert('RGBA'))] + [(n, ref(n)) for n in REF]
y0 = 512 + 50
for j, bg in enumerate([(248, 248, 248), (40, 40, 48)]):
    for k, (t, im) in enumerate(reeks):
        b = Image.new('RGBA', (64, 64), bg + (255,)); b.alpha_composite(im)
        vel.paste(b.convert('RGB'), (k * 70, y0 + j * 84))
        if j == 0: d.text((k * 70, y0 - 10 + 2 * 84 + 2), t, fill='black')
vel.save('vel.png')
