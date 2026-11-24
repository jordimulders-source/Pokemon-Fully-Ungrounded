# vel r12: var_a 8x | r12 8x | model 8x ; close-ups 12x (rode lijn, koepel, bovenkant) var_a | r12 | model ; 1x licht/donker naast Magnemite/Claydol
import numpy as np; from PIL import Image, ImageDraw
G = '../../../../../../graphics/pokemon/'
M = Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB'); k = 12.703
def mb(x0, y0, x1, y1): return (int(103 + x0 * k), int(143 + (y0 - 7) * k), int(103 + x1 * k), int(143 + (y1 - 7) * k))
m64 = M.crop(mb(0, 0, 64, 64)).resize((64, 64), Image.BOX)
A = Image.open('../r11/var_a.png').convert('RGBA'); R = Image.open('sprite.png').convert('RGBA')
def on(im, bg):
    b = Image.new('RGBA', im.size, bg + (255,)); b.alpha_composite(im.convert('RGBA')); return b.convert('RGB')
def big(im, f): return im.resize((im.width * f, im.height * f), Image.NEAREST)
def gba(n):
    im = Image.open(G + n + '/anim_front.png').convert('RGBA'); im = im.crop((0, 0, 64, 64)); px = np.array(im)
    bgc = px[0, 0, :3].copy(); px[(px[:, :, :3] == bgc).all(2), 3] = 0; return Image.fromarray(px)
crops = [((4, 14, 26, 34), 'rode lijn'), ((8, 25, 32, 48), 'koepel'), ((12, 5, 44, 24), 'bovenkant')]
H = 540 + sum((c[3] - c[1]) * 12 + 34 for c, _ in crops) + 120
W = max(3 * 520, max(3 * ((c[2] - c[0]) * 12 + 10) for c, _ in crops))
out = Image.new('RGB', (W, H), (205, 205, 205)); d = ImageDraw.Draw(out)
for i, (n, im) in enumerate((('var_a 8x', on(A, (255, 255, 255))), ('r12 8x', on(R, (255, 255, 255))), ('model 8x (verkleind, BOX)', m64))):
    out.paste(big(im, 8), (i * 520, 0)); d.text((i * 520 + 4, 516), n, fill=(0, 0, 0))
y = 540
for (x0, y0, x1, y1), naam in crops:
    w = (x1 - x0) * 12
    tiles = [('var_a', big(on(A.crop((x0, y0, x1, y1)), (255, 255, 255)), 12)), ('r12', big(on(R.crop((x0, y0, x1, y1)), (255, 255, 255)), 12)),
             ('model', M.crop(mb(x0, y0, x1, y1)).resize((w, (y1 - y0) * 12), Image.LANCZOS))]
    for j, (n, t) in enumerate(tiles):
        out.paste(t, (j * (w + 10), y + 14)); d.text((j * (w + 10) + 2, y), '%s 12x %s (x%d-%d, y%d-%d)' % (naam, n, x0, x1, y0, y1), fill=(0, 0, 0))
    y += (y1 - y0) * 12 + 34
d.text((10, y), '1x: var_a | r12 | Magnemite | Claydol | Magneton, op licht en donker', fill=(0, 0, 0))
for i, im in enumerate((A, R, gba('magnemite'), gba('claydol'), gba('magneton'))):
    for j, bg in enumerate(((255, 255, 255), (40, 40, 48))):
        out.paste(on(im, bg), (10 + i * 150 + j * 70, y + 16))
out = out.crop((0, 0, W, y + 90)); out.save('vel.png'); print(out.size)
