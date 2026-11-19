# Vel r5: r5 | r4b | model (8x, zelfde hoogte) · close-ups 12x: model op spriteraster | r5 | r4b (rug/achterwerk, kop/kuif) · 1x/2x licht en donker
import os, numpy as np
from PIL import Image, ImageDraw
from naast import model_raster, sprite
from meet import a as MA, bg as MBG
from palet import PAL
r5 = np.load('stap4.npy'); r4b = np.array(Image.open('../../r4/lama_b.png'))
P4 = [tuple(int(v) for v in l.split()) for l in open('../../r4/normal.pal').read().split('\n')[3:19]]
def rgba(p): return Image.open(p).convert('RGBA')
s5 = rgba('../lama.png'); s4 = rgba('../../r4/lama_b.png')
K = 8; H = 62 * K
ys, xs = np.nonzero(~MBG); m = MA.copy().astype('uint8'); m[MBG] = 255
mi = Image.fromarray(m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]); mi = mi.resize((int(mi.width * H / mi.height), H), Image.LANCZOS)
def groot(im): b = im.crop(im.getbbox()); return b.resize((b.width * K, b.height * K), Image.NEAREST)
top = [(groot(s5), 'r5 (8x)'), (groot(s4), 'r4b (8x)'), (mi, 'model_v3')]
cl = [('rug/achterwerk x24-52 y24-49', (24, 53, 24, 49)), ('kop/kuif x9-27 y4-28', (9, 28, 4, 28))]
Z = 12
hs = [H + 30] + [(c[1][3] - c[1][2]) * Z + 30 for c in cl] + [170]
Wd = max(sum(i.width for i, _ in top) + 60, max(3 * (c[1][1] - c[1][0]) * Z + 60 for c in cl))
W = Image.new('RGBA', (Wd, sum(hs) + 20), (255, 255, 255, 255)); d = ImageDraw.Draw(W)
y = 20; x = 0
for im, t in top:
    b = Image.new('RGBA', im.size, (235, 235, 240, 255)); b.alpha_composite(im.convert('RGBA')); W.paste(b, (x, y)); d.text((x + 2, y - 14), t, fill=(0, 0, 0)); x += im.width + 30
y += H + 30
for t, (x0, x1, y0, y1) in cl:
    ims = [(model_raster(x0, x1, y0, y1, Z), 'model'), (sprite(r5, PAL, x0, x1, y0, y1, Z), 'r5'), (sprite(r4b, P4, x0, x1, y0, y1, Z), 'r4b')]
    xx = 0
    for im, n in ims:
        W.paste(im, (xx, y)); d.text((xx + 2, y - 14), n + ', ' + t, fill=(0, 0, 0)); xx += im.width + 30
    y += (y1 - y0) * Z + 30
for j, bgc in enumerate([(248, 248, 248, 255), (40, 40, 48, 255)]):
    x0 = j * 420; d.rectangle([x0, y, x0 + 410, y + 150], fill=bgc)
    for k, im in enumerate([s5, s4]): W.paste(im, (x0 + 10 + k * 70, y + 10), im)
    for k, im in enumerate([s5, s4]):
        z = im.resize((128, 128), Image.NEAREST); W.paste(z, (x0 + 150 + k * 130, y + 10), z)
d.text((2, y - 14), '1x (r5, r4b) en 2x (r5, r4b) op licht en donker', fill=(0, 0, 0))
W.save('../vel.png'); print(W.size)
