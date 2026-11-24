# vel r14: kap x12-42/y8-30 op 20x: r14 | model op hetzelfde raster | 50/50 ; daaronder r13 | r14 op 8x ; 1x op licht en donker
import numpy as np
from PIL import Image, ImageDraw
M = Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB'); k = 12.703
def mb(x0, y0, x1, y1): return (int(round(103 + x0 * k)), int(round(143 + (y0 - 7) * k)), int(round(103 + x1 * k)), int(round(143 + (y1 - 7) * k)))
def on(im, bg):
    b = Image.new('RGBA', im.size, bg + (255,)); b.alpha_composite(im.convert('RGBA')); return b.convert('RGB')
R13 = Image.open('../r13/sprite.png').convert('RGBA'); R14 = Image.open('sprite.png').convert('RGBA')
X0, X1, Y0, Y1, Z = 12, 42, 8, 30, 20; w, h = (X1 - X0) * Z, (Y1 - Y0) * Z
spr = on(R14, (255, 255, 255)).crop((X0, Y0, X1, Y1)).resize((w, h), Image.NEAREST)
mod = M.crop(mb(X0, Y0, X1, Y1)).resize((w, h), Image.LANCZOS)
mix = Image.blend(spr, mod, 0.5)
def raster(t):
    d = ImageDraw.Draw(t)
    for i in range(X1 - X0 + 1): d.line([(i * Z, 0), (i * Z, h)], fill=(255, 0, 0) if (X0 + i) % 5 == 0 else (190, 190, 190))
    for j in range(Y1 - Y0 + 1): d.line([(0, j * Z), (w, j * Z)], fill=(255, 0, 0) if (Y0 + j) % 5 == 0 else (190, 190, 190))
    return t
W = 3 * w + 20; out = Image.new('RGB', (max(W, 1040), 16 + h + 20 + 512 + 20 + 160), (205, 205, 205)); d = ImageDraw.Draw(out)
d.text((4, 2), 'kap: r14 (x12-42, y8-30) | model op hetzelfde raster | 50/50 over elkaar; rode lijnen elke 5 px', fill=(0, 0, 0))
for i, t in enumerate((spr, mod, mix)): out.paste(raster(t), (i * (w + 10), 16))
y = 16 + h + 20
for i, (n, im) in enumerate((('r13 8x', R13), ('r14 8x', R14))):
    out.paste(on(im, (255, 255, 255)).resize((512, 512), Image.NEAREST), (i * 528, y)); d.text((i * 528 + 4, y + 500), n, fill=(0, 0, 0))
y += 532; d.text((4, y), '1x op licht en donker: r13 | r14', fill=(0, 0, 0))
for j, bg in enumerate(((255, 255, 255), (40, 40, 48))):
    for i, im in enumerate((R13, R14)): out.paste(on(im, bg), (4 + i * 70 + j * 150, y + 16))
out = out.crop((0, 0, out.width, y + 90)); out.save('vel.png'); print(out.size)
