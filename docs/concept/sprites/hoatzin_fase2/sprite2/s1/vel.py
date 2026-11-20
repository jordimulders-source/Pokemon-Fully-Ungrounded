# vel.py: s1 | model verkleind | onderlaag (8x); kop 12x naast model-kop; 1x/2x op licht en donker
from PIL import Image, ImageDraw
def plak(bg, im, xy):
    im = im.convert('RGBA'); bg.paste(im, xy, im)
s1 = Image.open('hoatzin.png'); ond = Image.open('onderlaag.png')
mod = Image.open('../../MODEL.png').convert('RGB')
W = 512 * 3 + 40; V = Image.new('RGB', (W, 512 + 20 + 300 + 20 + 140), (255, 255, 255))
plak(V, s1.resize((512, 512), Image.NEAREST), (0, 0))
V.paste(mod.resize((512, 512), Image.LANCZOS), (532, 0))
plak(V, ond.resize((512, 512), Image.NEAREST), (1064, 0))
# kop 12x: spritevak x0-22, y15-40 (22x25) -> 264x300; model dezelfde uitsnede
X0, Y0, s = 97, 125, 833 / 62
kx0, ky0, kx1, ky1 = 0, 15, 24, 40
kop = s1.crop((kx0, ky0, kx1, ky1)).resize(((kx1 - kx0) * 12, (ky1 - ky0) * 12), Image.NEAREST)
mk = mod.crop((int(X0 + (kx0 - 1) * s), int(Y0 + (ky0 - 5) * s), int(X0 + (kx1 - 1) * s), int(Y0 + (ky1 - 5) * s))).resize(kop.size, Image.LANCZOS)
ok = ond.crop((kx0, ky0, kx1, ky1)).resize(kop.size, Image.NEAREST)
y = 532; plak(V, kop, (0, y)); V.paste(mk, (kop.width + 20, y)); plak(V, ok, (2 * kop.width + 40, y))
# 1x en 2x op licht en donker
y = 852
for i, bgc in enumerate([(255, 255, 255), (232, 240, 248), (48, 56, 64)]):
    vak = Image.new('RGB', (64 * 3 + 20, 128), bgc)
    plak(vak, s1, (0, 32)); plak(vak, s1.resize((128, 128), Image.NEAREST), (84, 0))
    V.paste(vak, (i * 230, y))
V.save('vel.png')
