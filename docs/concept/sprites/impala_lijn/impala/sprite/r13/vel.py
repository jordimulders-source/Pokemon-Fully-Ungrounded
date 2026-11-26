# vel.png r13: r13 | r13 variant B | r12 | model (8x); close-up poten 12x naast het model; Gen 3-poten (Stantler, Girafarig, Skarmory) op 12x.
# Draaien vanuit sprite/: python3 r13/vel.py
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
m0 = Image.open('../referenties/model_r5.png').convert('RGB'); m = Image.new('RGB', (3072, 3072), (255, 255, 255)); m.paste(m0, (1024, 1024))
p = 15.126984126984127
def modcrop(x0, y0, x1, y1, size):
    bx = 196 + 1024 + (x0 - 10) * p; by = 39 + 1024 + (y0 - 1) * p
    return m.crop((int(bx), int(by), int(bx + (x1 - x0) * p), int(by + (y1 - y0) * p))).resize(size, Image.LANCZOS).convert('RGBA')
def wit(im, box=(0, 0, 64, 64), z=8):
    c = im.crop(box); t = Image.new('RGBA', c.size, (255, 255, 255, 255)); t.paste(c, (0, 0), c)
    return t.resize((c.width * z, c.height * z), Image.NEAREST)
A = rgba('r13/impala_r13.png'); B = rgba('r13/variant_B/impala_r13_B.png'); R12 = rgba('r12/impala_r12.png')
BG = (236, 236, 236, 255)
rows = []
top = [wit(A), wit(B), wit(R12), modcrop(0, 0, 64, 64, (512, 512))]
T = Image.new('RGBA', (4 * 522 + 10, 532), BG); d = ImageDraw.Draw(T)
for i, im in enumerate(top): T.paste(im, (10 + i * 522, 10)); d.text((14 + i * 522, 12), ['r13 (A)', 'r13 variant B', 'r12', 'model r5'][i], fill=(200, 0, 0))
rows.append(T)
box = (17, 43, 54, 64)
cl = [wit(A, box, 12), wit(B, box, 12), wit(R12, box, 12), modcrop(*box, (37 * 12, 21 * 12))]
C = Image.new('RGBA', (2 * (37 * 12 + 10) + 10, 2 * (21 * 12 + 10) + 10), BG); dc = ImageDraw.Draw(C)
for i, im in enumerate(cl): C.paste(im, (10 + (i % 2) * (37 * 12 + 10), 10 + (i // 2) * (21 * 12 + 10))); dc.text((14 + (i % 2) * (37 * 12 + 10), 12 + (i // 2) * (21 * 12 + 10)), ['A', 'B', 'r12', 'model'][i], fill=(200, 0, 0))
rows.append(C)
g3 = [wit(gba('stantler'), (40, 46, 62, 64), 12), wit(gba('girafarig'), (16, 40, 50, 61), 12), wit(gba('skarmory'), (22, 46, 46, 64), 12)]
Gm = Image.new('RGBA', (sum(g.width + 10 for g in g3) + 10, max(g.height for g in g3) + 20), BG); x = 10
for g in g3: Gm.paste(g, (x, 10)); x += g.width + 10
rows.append(Gm)
O = Image.new('RGBA', (max(r.width for r in rows), sum(r.height for r in rows)), BG); y = 0
for r in rows: O.paste(r, (0, y)); y += r.height
O.save('r13/vel.png'); print(O.size)
