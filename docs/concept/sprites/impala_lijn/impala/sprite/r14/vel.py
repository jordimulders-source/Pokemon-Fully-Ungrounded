# vel.png r14: r14 | r12 | model (8x); close-up poten 12x: r14 | r12 | Kirlia-poot (x26-37, y44-60) op 12x. Vanuit sprite/: python3 r14/vel.py
import numpy as np
from PIL import Image, ImageDraw
G = '/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def rgba(f):
    im = Image.open(f).crop((0, 0, 64, 64)); a = np.array(im)
    c = np.array(im.convert('RGB').convert('RGBA')); c[a == 0, 3] = 0; return Image.fromarray(c)
def gba(n):
    im = Image.open(G + n + '/anim_front_gba.png').crop((0, 0, 64, 64))
    pal = [int(v) for l in open(G + n + '/normal_gba.pal').read().split('\n')[3:19] for v in l.split()]
    im.putpalette(pal); a = np.array(im); c = np.array(im.convert('RGB').convert('RGBA')); c[a == 0, 3] = 0
    return Image.fromarray(c)
def wit(im, box=(0, 0, 64, 64), z=8):
    c = im.crop(box); t = Image.new('RGBA', c.size, (255, 255, 255, 255)); t.paste(c, (0, 0), c)
    return t.resize((c.width * z, c.height * z), Image.NEAREST)
m0 = Image.open('../referenties/model_r5.png').convert('RGB'); m = Image.new('RGB', (3072, 3072), (255, 255, 255)); m.paste(m0, (1024, 1024))
p = 15.126984126984127
mod = m.crop((int(196 + 1024 - 10 * p), int(39 + 1024 - p), int(196 + 1024 + 54 * p), int(39 + 1024 + 63 * p))).resize((512, 512), Image.LANCZOS).convert('RGBA')
A = rgba('r14/impala_r14.png'); R = rgba('r12/impala_r12.png'); K = gba('kirlia')
BG = (236, 236, 236, 255)
top = [wit(A), wit(R), mod]
T = Image.new('RGBA', (3 * 522 + 10, 532), BG); d = ImageDraw.Draw(T)
for i, im in enumerate(top): T.paste(im, (10 + i * 522, 10)); d.text((14 + i * 522, 12), ['r14', 'r12', 'model r5'][i], fill=(200, 0, 0))
box = (17, 43, 54, 64)
cl = [wit(A, box, 12), wit(R, box, 12), wit(K, (26, 40, 38, 60), 12), wit(K, (0, 0, 64, 64), 3)]
C = Image.new('RGBA', (sum(c.width + 10 for c in cl) + 10, max(c.height for c in cl) + 20), BG); x = 10; dc = ImageDraw.Draw(C)
for i, c in enumerate(cl): C.paste(c, (x, 10)); dc.text((x + 4, 12), ['r14', 'r12', 'Kirlia x26-37', 'Kirlia 3x'][i], fill=(200, 0, 0)); x += c.width + 10
O = Image.new('RGBA', (max(T.width, C.width), T.height + C.height), BG); O.paste(T, (0, 0)); O.paste(C, (0, T.height))
O.save('r14/vel.png'); print(O.size)
