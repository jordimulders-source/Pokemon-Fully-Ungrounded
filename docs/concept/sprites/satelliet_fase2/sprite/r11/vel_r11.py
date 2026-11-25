# vel r11: r10 | var_a | var_b | var_c op 8x; close-ups 12x van bovenkant en koepel/lens naast het model; 1x op licht/donker
import numpy as np; from PIL import Image, ImageDraw
M = Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB'); k = 12.703
def mx(x): return 103 + x * k
def my(y): return 143 + (y - 7) * k
SP = [('r10', '../r10/sprite.png'), ('var_a', 'var_a.png'), ('var_b', 'var_b.png'), ('var_c', 'var_c.png')]
ims = [(n, Image.open(p).convert('RGBA')) for n, p in SP]
def on(im, bg):
    b = Image.new('RGBA', im.size, bg + (255,)); b.alpha_composite(im); return b.convert('RGB')
def big(im, f): return im.resize((im.width * f, im.height * f), Image.NEAREST)
def mcrop(x0, y0, x1, y1, f):
    return M.crop((int(mx(x0)), int(my(y0)), int(mx(x1)), int(my(y1)))).resize(((x1 - x0) * f, (y1 - y0) * f), Image.LANCZOS)
W = 4 * 520 + 10
crops = [((12, 12, 42, 24), 'bovenkant'), ((8, 25, 32, 46), 'koepel/lens')]
hs = [(c[3] - c[1]) * 12 + 30 for c, _ in crops]
out = Image.new('RGB', (W, 540 + sum(hs) * 3 + 120), (205, 205, 205)); d = ImageDraw.Draw(out)
for i, (n, im) in enumerate(ims):
    out.paste(big(on(im, (255, 255, 255)), 8), (i * 520, 0)); d.text((i * 520 + 4, 516), n + ' 8x', fill=(0, 0, 0))
y = 540
for (x0, y0, x1, y1), naam in crops:
    f = 12; w = (x1 - x0) * f; h = (y1 - y0) * f
    # rij: model | r10 | a | b | c  (per crop twee rijen als het niet past)
    tiles = [('model', mcrop(x0, y0, x1, y1, f))] + [(n, big(on(im.crop((x0, y0, x1, y1)), (255, 255, 255)), f)) for n, im in ims]
    per = max(1, W // (w + 10))
    for j, (n, t) in enumerate(tiles):
        r, c = divmod(j, per)
        px, py = c * (w + 10), y + 14 + r * (h + 20)
        out.paste(t, (px, py)); d.text((px + 2, py - 12), '%s 12x %s (x%d-%d, y%d-%d)' % (naam, n, x0, x1, y0, y1), fill=(0, 0, 0))
    rows = (len(tiles) + per - 1) // per
    y += rows * (h + 20) + 20
for i, (n, im) in enumerate(ims):
    for j, bg in enumerate(((255, 255, 255), (40, 40, 48))):
        out.paste(on(im, bg), (10 + i * 150 + j * 70, y + 14))
    d.text((10 + i * 150, y), n + ' 1x', fill=(0, 0, 0))
out = out.crop((0, 0, W, y + 90)); out.save('vel.png'); print('vel.png', out.size)
