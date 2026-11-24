# vel r19: (a) r18 | r19 | model 16x voor de rechteruitsnede (x28-46, y16-40) en de linkeruitsnede (x4-24, y20-48),
# (b) r18 | r19 | model 8x, (c) 1x licht/donker r18 | r19.
from PIL import Image, ImageDraw
k = 12.703
M = Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB')
R18 = Image.open('../r18/sprite.png').convert('RGBA'); R19 = Image.open('sprite.png').convert('RGBA')
def on(im, bg):
    b = Image.new('RGBA', im.size, bg + (255,)); b.alpha_composite(im.convert('RGBA')); return b.convert('RGB')
def grid(c, X0, X1, Y0, Y1, Z, t):
    o = Image.new('RGB', (c.width + 30, c.height + 34), (255, 255, 255)); o.paste(c, (30, 20)); d = ImageDraw.Draw(o); d.text((30, 2), t, fill=(0, 0, 0))
    for x in range(X0, X1 + 1):
        d.line([(30 + (x - X0) * Z, 20), (30 + (x - X0) * Z, 20 + c.height)], fill=(230, 0, 0) if x % 5 == 0 else (190, 190, 190))
        if x % 2 == 0: d.text((32 + (x - X0) * Z, 22 + c.height), str(x), fill=(200, 0, 0))
    for y in range(Y0, Y1 + 1):
        d.line([(30, 20 + (y - Y0) * Z), (30 + c.width, 20 + (y - Y0) * Z)], fill=(230, 0, 0) if y % 5 == 0 else (190, 190, 190))
        if y % 2 == 0: d.text((4, 22 + (y - Y0) * Z), str(y), fill=(200, 0, 0))
    return o
def sp(im, X0, X1, Y0, Y1, Z, t): return grid(on(im, (255, 255, 255)).crop((X0, Y0, X1, Y1)).resize(((X1 - X0) * Z, (Y1 - Y0) * Z), Image.NEAREST), X0, X1, Y0, Y1, Z, t)
def md(X0, X1, Y0, Y1, Z, t):
    return grid(M.crop((round(103 + X0 * k), round(143 + (Y0 - 7) * k), round(103 + X1 * k), round(143 + (Y1 - 7) * k))).resize(((X1 - X0) * Z, (Y1 - Y0) * Z), Image.LANCZOS), X0, X1, Y0, Y1, Z, t)
rijen = []
for (X0, X1, Y0, Y1, n) in ((28, 46, 16, 40, 'rechts'), (4, 24, 20, 48, 'links')):
    rijen.append([sp(R18, X0, X1, Y0, Y1, 16, '(a) %s r18' % n), sp(R19, X0, X1, Y0, Y1, 16, 'r19'), md(X0, X1, Y0, Y1, 16, 'model')])
mc = M.crop((103, 0, min(1024, round(103 + 64 * k)), min(1024, round(143 + 57 * k))))
m8 = Image.new('RGB', (512, 512), (255, 255, 255)); m8.paste(mc.resize((round(mc.width * 8 / k), round(mc.height * 8 / k)), Image.LANCZOS), (0, round(-(143 - 7 * k) * 8 / k)))
C = [on(R18, (255, 255, 255)).resize((512, 512), Image.NEAREST), on(R19, (255, 255, 255)).resize((512, 512), Image.NEAREST), m8]
W = max(max(sum(b.width for b in r) + 20 for r in rijen), 3 * 522)
Hh = sum(r[0].height + 10 for r in rijen) + 14 + 512 + 10 + 14 + 64 + 20
out = Image.new('RGB', (W, Hh), (215, 215, 215)); d = ImageDraw.Draw(out); y = 0
for r in rijen:
    x = 0
    for b in r: out.paste(b, (x, y)); x += b.width + 10
    y += r[0].height + 10
d.text((4, y), '(b) r18 | r19 | model (8x)', fill=(0, 0, 0))
for i, im in enumerate(C): out.paste(im, (i * 522, y + 14))
y += 14 + 512 + 10; d.text((4, y), '(c) 1x op licht en donker: r18 | r19', fill=(0, 0, 0))
for j, bg in enumerate(((255, 255, 255), (40, 40, 48))):
    for i, im in enumerate((R18, R19)): out.paste(on(im, bg), (4 + i * 70 + j * 150, y + 14))
out.save('vel.png'); print(out.size)
