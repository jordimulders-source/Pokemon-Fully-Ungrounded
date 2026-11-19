# Vel r3: model | r3 | r1 (8x, zelfde hoogte) · close-ups 12x: model op spriteraster | r3 (kop, lijf, poten) · 1x en 2x op licht en donker
import os, json, numpy as np
from PIL import Image, ImageDraw
from naast import model_raster, sprite
from meet import a as MA, bg as MBG
HIER = os.path.dirname(os.path.abspath(__file__)); R3 = os.path.dirname(HIER); SP = os.path.dirname(R3)
r3 = np.load(os.path.join(HIER, 'lama_idx.npy')); pal = [tuple(c) for c in json.load(open(os.path.join(HIER, 'palet.json')))]
def rgba(p):
    im = Image.open(p); im.load()
    return im.convert('RGBA')
s3 = rgba(os.path.join(R3, 'lama.png')); s1 = rgba(os.path.join(SP, 'r1', 'lama.png'))
def box(im):
    b = im.getbbox(); return im.crop(b)
K = 8; H = 62 * K
# model: uitsnede van de inhoud, zelfde hoogte als 62 spritepixels
ys, xs = np.nonzero(~MBG); m = MA.copy().astype('uint8'); m[MBG] = 255
mi = Image.fromarray(m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]); mi = mi.resize((int(mi.width * H / mi.height), H), Image.LANCZOS)
p3 = box(s3); p3 = p3.resize((p3.width * K, p3.height * K), Image.NEAREST)
p1 = box(s1); p1 = p1.resize((p1.width * K * 62 // p1.height, H), Image.NEAREST)
cl = [('kop x9-27 y1-27', (9, 28, 1, 28)), ('lijf x10-53 y26-48', (10, 54, 26, 49)), ('poten x10-53 y46-63', (10, 54, 46, 64))]
Z = 12
rows_h = [H + 30] + [(c[1][3] - c[1][2]) * Z + 30 for c in cl] + [170]
Wd = max(mi.width + p3.width + p1.width + 60, max(2 * (c[1][1] - c[1][0]) * Z + 30 for c in cl))
W = Image.new('RGBA', (Wd, sum(rows_h) + 20), (255, 255, 255, 255)); d = ImageDraw.Draw(W)
y = 20; x = 0
for im, t in [(mi, 'model_v3'), (p3, 'r3 (8x)'), (p1, 'r1 (8x, afgekeurd)')]:
    bgp = Image.new('RGBA', im.size, (235, 235, 240, 255)); bgp.alpha_composite(im.convert('RGBA'))
    W.paste(bgp, (x, y)); d.text((x + 2, y - 14), t, fill=(0, 0, 0)); x += im.width + 30
y += H + 30
for t, (x0, x1, y0, y1) in cl:
    A = model_raster(x0, x1, y0, y1, Z); B = sprite(r3, pal, x0, x1, y0, y1, Z)
    W.paste(A, (0, y)); W.paste(B, (A.width + 30, y))
    d.text((2, y - 14), 'model op spriteraster, ' + t, fill=(0, 0, 0)); d.text((A.width + 32, y - 14), 'r3, ' + t, fill=(0, 0, 0))
    y += (y1 - y0) * Z + 30
for j, bgc in enumerate([(248, 248, 248, 255), (40, 40, 48, 255)]):
    x0 = j * 420; d.rectangle([x0, y, x0 + 410, y + 150], fill=bgc)
    for k, im in enumerate([s3, s1]):
        W.paste(im, (x0 + 10 + k * 70, y + 10), im)
    z = s3.resize((128, 128), Image.NEAREST); W.paste(z, (x0 + 160, y + 10), z)
    z = s1.resize((128, 128), Image.NEAREST); W.paste(z, (x0 + 290, y + 10), z)
d.text((2, y - 14), '1x (r3, r1) en 2x (r3, r1) op licht en donker', fill=(0, 0, 0))
W.save(os.path.join(R3, 'vel.png')); print(W.size)
