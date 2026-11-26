# vel.png voor r11: r11 | r9 | model (8x); 1x op licht/donker naast de maatstaf-sprites en Gen 3-viervoeters (_gba);
# close-ups kop+hoorns en buik+poten op 12x: r11 | r9 | model. Draaien vanuit sprite/: python3 r11/vel.py
import numpy as np
from PIL import Image, ImageDraw
G = '/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'; S = '/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/'
def rgba(f):
    im = Image.open(f).crop((0, 0, 64, 64)); a = np.array(im)
    c = np.array(im.convert('RGB').convert('RGBA')); c[a == 0, 3] = 0; return Image.fromarray(c)
def gba(n):
    im = Image.open(G + n + '/anim_front_gba.png').crop((0, 0, 64, 64))
    pal = [int(v) for l in open(G + n + '/normal_gba.pal').read().split('\n')[3:19] for v in l.split()]
    im.putpalette(pal); a = np.array(im); c = np.array(im.convert('RGB').convert('RGBA')); c[a == 0, 3] = 0
    return Image.fromarray(c)
r11 = rgba('r11/impala_r11.png'); r9 = rgba('r9/impala_r9.png')
m0 = Image.open('../referenties/model_r5.png').convert('RGB'); m = Image.new('RGB', (3072, 3072), (255, 255, 255)); m.paste(m0, (1024, 1024))
p = 15.126984126984127; OX, OY = 10, 1
def modcrop(x0, y0, x1, y1, size):
    bx = 196 + 1024 + (x0 - OX) * p; by = 39 + 1024 + (y0 - OY) * p
    return m.crop((int(bx), int(by), int(bx + (x1 - x0) * p), int(by + (y1 - y0) * p))).resize(size, Image.LANCZOS)
def wit(im, box=(0, 0, 64, 64), z=8, bg=(255, 255, 255, 255)):
    c = im.crop(box); t = Image.new('RGBA', c.size, bg); t.paste(c, (0, 0), c)
    return t.resize((c.width * z, c.height * z), Image.NEAREST)
BG = (236, 236, 236, 255)
V = Image.new('RGBA', (3 * 522 + 10, 522), BG); d = ImageDraw.Draw(V)
for i, im in enumerate([wit(r11), wit(r9), modcrop(0, 0, 64, 64, (512, 512)).convert('RGBA')]):
    V.paste(im, (10 + i * 522, 10))
for i, s in enumerate(['r11', 'r9 (= r10)', 'model r5']): d.text((14 + i * 522, 12), s, fill=(200, 0, 0))
# 1x licht/donker + maatstaf
refs = [rgba(S + 'skinguin/af/skinguin.png'), rgba(S + 'dundragoon/af/dundragoon.png'), rgba(S + 'viscacha/af/viscacha.png'), rgba(S + 'awki/af/awki.png')] + [gba(n) for n in ('stantler', 'rapidash', 'ponyta', 'girafarig', 'absol')]
R1 = Image.new('RGBA', (V.width, 2 * 76 + 10), BG); xx = 10
for bg in [(248, 248, 248, 255), (40, 40, 48, 255)]:
    for j, r in enumerate([r11, r9] + refs):
        t = Image.new('RGBA', (72, 72), bg); t.paste(r, (4, 4), r); R1.paste(t, (10 + j * 78, 5 + (0 if bg[0] > 100 else 76)))
# 3x naast Gen 3
R3 = Image.new('RGBA', (V.width, 200), BG)
for j, r in enumerate([r11] + refs[4:]):
    R3.paste(wit(r, z=3, bg=(248, 248, 248, 255)), (10 + j * 200, 4))
# close-ups 12x
def close(box):
    a = wit(r11, box, 12); b = wit(r9, box, 12); c = modcrop(*box, a.size).convert('RGBA')
    C = Image.new('RGBA', (a.width * 3 + 40, a.height + 20), BG)
    for i, im in enumerate([a, b, c]): C.paste(im, (10 + i * (a.width + 10), 10))
    return C
K = close((9, 0, 35, 34)); P = close((18, 30, 54, 64))
H = V.height + R1.height + R3.height + K.height + P.height
W = max(V.width, K.width, P.width)
O = Image.new('RGBA', (W, H), BG); y = 0
for im in (V, R1, R3, K, P): O.paste(im, (0, y)); y += im.height
O.save('r11/vel.png'); print(O.size)
