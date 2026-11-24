# vel r16: (a) r16 | modelraster64 op hetzelfde raster met rasterlijnen/coordinaten, (b) r15 | r16 | model 8x, (c) 1x licht/donker.
# Telt ook per zone de afwijkingen t.o.v. modelraster64 (familie: zwart / wit-grijs / paars / paneel / teal / leeg; tintverschil binnen een familie telt niet).
import numpy as np
from PIL import Image, ImageDraw
k = 12.703
M = Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB')
R15 = Image.open('../r15/sprite.png').convert('RGBA'); R16 = Image.open('sprite.png').convert('RGBA')
MR = Image.open('modelraster64.png').convert('RGBA')
def on(im, bg):
    b = Image.new('RGBA', im.size, bg + (255,)); b.alpha_composite(im.convert('RGBA')); return b.convert('RGB')
def raster(im, X0, X1, Y0, Y1, Z, titel):
    c = on(im, (255, 255, 255)).crop((X0, Y0, X1, Y1)).resize(((X1 - X0) * Z, (Y1 - Y0) * Z), Image.NEAREST)
    o = Image.new('RGB', (c.width + 30, c.height + 34), (255, 255, 255)); o.paste(c, (30, 20)); d = ImageDraw.Draw(o)
    d.text((30, 2), titel, fill=(0, 0, 0))
    for x in range(X0, X1 + 1):
        d.line([(30 + (x - X0) * Z, 20), (30 + (x - X0) * Z, 20 + c.height)], fill=(230, 0, 0) if x % 5 == 0 else (200, 200, 200))
        if x % 5 == 2: d.text((32 + (x - X0) * Z, 22 + c.height), str(x), fill=(200, 0, 0))
    for y in range(Y0, Y1 + 1):
        d.line([(30, 20 + (y - Y0) * Z), (30 + c.width, 20 + (y - Y0) * Z)], fill=(230, 0, 0) if y % 5 == 0 else (200, 200, 200))
        if y % 5 == 1: d.text((4, 22 + (y - Y0) * Z), str(y), fill=(200, 0, 0))
    return o
A1 = raster(R16, 2, 46, 6, 52, 16, 'sprite r16')
A2 = raster(MR, 2, 46, 6, 52, 16, 'model, per pixel de meest voorkomende kleur (modelraster64.png)')
# (b) 8x
box = (round(103 + 0 * k), round(143 + (0 - 7) * k), round(103 + 64 * k), round(143 + (64 - 7) * k))
B = [on(R15, (255, 255, 255)).resize((512, 512), Image.NEAREST), on(R16, (255, 255, 255)).resize((512, 512), Image.NEAREST),
     Image.new('RGB', (512, 512), (255, 255, 255))]
mc = M.crop((box[0], max(0, box[1]), min(1024, box[2]), min(1024, box[3])))
B[2].paste(mc.resize((round(mc.width * 512 / (64 * k)), round(mc.height * 512 / (64 * k))), Image.LANCZOS), (0, round((max(0, box[1]) - box[1]) * 512 / (64 * k))))
W = A1.width + A2.width + 10
out = Image.new('RGB', (max(W, 3 * 522), A1.height + 30 + 512 + 30 + 100), (215, 215, 215)); d = ImageDraw.Draw(out)
out.paste(A1, (0, 0)); out.paste(A2, (A1.width + 10, 0))
y = A1.height + 10; d.text((4, y), '(b) r15 | r16 | model (8x)', fill=(0, 0, 0))
for i, im in enumerate(B): out.paste(im, (i * 522, y + 16))
y += 16 + 512 + 10; d.text((4, y), '(c) 1x op licht en donker: r15 | r16', fill=(0, 0, 0))
for j, bg in enumerate(((255, 255, 255), (40, 40, 48))):
    for i, im in enumerate((R15, R16)): out.paste(on(im, bg), (4 + i * 70 + j * 150, y + 16))
out.save('vel.png'); print(out.size)
# ---- afwijkingen per zone t.o.v. modelraster (kaal.npy = modelraster op het palet, wit binnen het lijf terug).
# Telt vorm, geen kleurmapping: silhouet (leeg/niet leeg), lijnen (zwart/niet zwart) en vlakfamilie (licht 2-5,F / paars 6-12 / teal).
K = np.load('kaal.npy'); a = np.load('r16.npy'); r15 = np.array(Image.open('../r15/sprite.png'))
def fam(v): return np.select([v == 0, v == 1, np.isin(v, (2, 3, 4, 5, 15)), np.isin(v, (13, 14))], ['leeg', 'zwart', 'licht', 'teal'], 'paars')
fk, fa, f15 = fam(K), fam(a), fam(r15)
yy, xx = np.mgrid[0:64, 0:64]
lens = np.hypot(xx + .5 - 19, yy + .5 - 35) <= 6.05
bol = (xx >= 26) & (xx <= 33) & (yy >= 14) & (yy <= 21)
Z = {'bol (x26-33, y14-21)': bol, 'lens (schijf x13-24, y29-40)': lens,
     'kap/voorvlak boven (y19-31, x13-37)': (yy >= 19) & (yy <= 31) & (xx >= 13) & (xx <= 37) & ~lens & ~bol,
     'onderkant (y32-47, x12-29)': (yy >= 32) & (yy <= 47) & (xx >= 12) & (xx <= 29) & ~lens}
for nm, z in Z.items():
    print(nm)
    for soort, A, B in (('silhouet', fa == 'leeg', fk == 'leeg'), ('lijn', fa == 'zwart', fk == 'zwart')):
        d16 = (A != B) & z
        d15 = (((f15 == 'leeg') if soort == 'silhouet' else (f15 == 'zwart')) != B) & z
        print('   %-9s r16 %3d (r15 %3d): %s' % (soort, d16.sum(), d15.sum(), ' '.join('(%d,%d)%s' % (x, y, '+' if A[y, x] else '-') for y, x in zip(*np.nonzero(d16)))))
    rest = (fa != fk) & z & (fa != 'leeg') & (fk != 'leeg') & (fa != 'zwart') & (fk != 'zwart')
    r15r = (f15 != fk) & z & (f15 != 'leeg') & (fk != 'leeg') & (f15 != 'zwart') & (fk != 'zwart')
    print('   %-9s r16 %3d (r15 %3d): %s' % ('vlak', rest.sum(), r15r.sum(), ' '.join('(%d,%d)%s>%s' % (x, y, fk[y, x], fa[y, x]) for y, x in zip(*np.nonzero(rest)))))
