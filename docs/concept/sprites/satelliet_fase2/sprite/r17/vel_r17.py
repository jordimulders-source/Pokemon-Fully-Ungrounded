# vel r17: (a) r17 | modelraster64 met rasterlijnen/coordinaten, (b) close-up 16x bovenkant x12-40/y12-24: r16 | r17 | model,
# (c) r16 | r17 | model 8x, (d) r17 2x naast Glalie/Magneton/Claydol, (e) 1x licht/donker.
import numpy as np
from PIL import Image, ImageDraw
k = 12.703
M = Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB')
R16 = Image.open('../r16/sprite.png').convert('RGBA'); R17 = Image.open('sprite.png').convert('RGBA')
MR = Image.open('../r16/modelraster64.png').convert('RGBA')
def on(im, bg):
    b = Image.new('RGBA', im.size, bg + (255,)); b.alpha_composite(im.convert('RGBA')); return b.convert('RGB')
def grid(c, X0, X1, Y0, Y1, Z, titel):
    o = Image.new('RGB', (c.width + 30, c.height + 34), (255, 255, 255)); o.paste(c, (30, 20)); d = ImageDraw.Draw(o)
    d.text((30, 2), titel, fill=(0, 0, 0))
    for x in range(X0, X1 + 1):
        d.line([(30 + (x - X0) * Z, 20), (30 + (x - X0) * Z, 20 + c.height)], fill=(230, 0, 0) if x % 5 == 0 else (190, 190, 190))
        if x % 5 == 2: d.text((32 + (x - X0) * Z, 22 + c.height), str(x), fill=(200, 0, 0))
    for y in range(Y0, Y1 + 1):
        d.line([(30, 20 + (y - Y0) * Z), (30 + c.width, 20 + (y - Y0) * Z)], fill=(230, 0, 0) if y % 5 == 0 else (190, 190, 190))
        if y % 5 == 1: d.text((4, 22 + (y - Y0) * Z), str(y), fill=(200, 0, 0))
    return o
def sp(im, X0, X1, Y0, Y1, Z, t):
    return grid(on(im, (255, 255, 255)).crop((X0, Y0, X1, Y1)).resize(((X1 - X0) * Z, (Y1 - Y0) * Z), Image.NEAREST), X0, X1, Y0, Y1, Z, t)
def md(X0, X1, Y0, Y1, Z, t):
    c = M.crop((round(103 + X0 * k), round(143 + (Y0 - 7) * k), round(103 + X1 * k), round(143 + (Y1 - 7) * k))).resize(((X1 - X0) * Z, (Y1 - Y0) * Z), Image.LANCZOS)
    return grid(c, X0, X1, Y0, Y1, Z, t)
A = [sp(R17, 2, 46, 6, 52, 14, '(a) sprite r17'), sp(MR, 2, 46, 6, 52, 14, 'model op het 64-raster (modelraster64.png)')]
Bb = [sp(R16, 12, 40, 12, 24, 16, '(b) r16'), sp(R17, 12, 40, 12, 24, 16, 'r17'), md(12, 40, 12, 24, 16, 'model')]
box = (round(103), round(143 - 7 * k))
mc = M.crop((box[0], 0, min(1024, round(103 + 64 * k)), min(1024, round(143 + 57 * k))))
m8 = Image.new('RGB', (512, 512), (255, 255, 255)); m8.paste(mc.resize((round(mc.width * 8 / k), round(mc.height * 8 / k)), Image.LANCZOS), (0, round(-box[1] * 8 / k)))
C = [on(R16, (255, 255, 255)).resize((512, 512), Image.NEAREST), on(R17, (255, 255, 255)).resize((512, 512), Image.NEAREST), m8]
D = [on(R17, (255, 255, 255)).resize((128, 128), Image.NEAREST)]
for n in ('glalie', 'magneton', 'claydol'):
    g = Image.open('../../../../../../graphics/pokemon/%s/anim_front.png' % n).convert('RGBA'); g = g.crop((0, 0, 64, 64))
    px = np.array(g); bgc = px[0, 0].copy(); m = (px[..., :3] == bgc[:3]).all(-1); px[m, 3] = 0
    D.append(on(Image.fromarray(px), (255, 255, 255)).resize((128, 128), Image.NEAREST))
W = max(A[0].width + A[1].width + 10, sum(b.width for b in Bb) + 20, 3 * 522)
H = A[0].height + 20 + Bb[0].height + 20 + 512 + 30 + 128 + 40 + 80
out = Image.new('RGB', (W, H), (215, 215, 215)); d = ImageDraw.Draw(out)
out.paste(A[0], (0, 0)); out.paste(A[1], (A[0].width + 10, 0)); y = A[0].height + 10
x = 0
for b in Bb: out.paste(b, (x, y)); x += b.width + 10
y += Bb[0].height + 10; d.text((4, y), '(c) r16 | r17 | model (8x)', fill=(0, 0, 0))
for i, im in enumerate(C): out.paste(im, (i * 522, y + 14))
y += 14 + 512 + 10; d.text((4, y), '(d) 2x: r17 | Glalie | Magneton | Claydol', fill=(0, 0, 0))
for i, im in enumerate(D): out.paste(im, (4 + i * 138, y + 14))
y += 14 + 128 + 10; d.text((4, y), '(e) 1x op licht en donker: r16 | r17', fill=(0, 0, 0))
for j, bg in enumerate(((255, 255, 255), (40, 40, 48))):
    for i, im in enumerate((R16, R17)): out.paste(on(im, bg), (4 + i * 70 + j * 150, y + 14))
out.save('vel.png'); print(out.size)
