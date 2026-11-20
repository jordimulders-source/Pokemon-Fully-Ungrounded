# vel.py: s1 | s2 | model (8x); kop 12x: s1 | s2-A | s2-B | model; 1x en 2x van A en B op licht en donker
from PIL import Image
def plak(bg, im, xy):
    im = im.convert('RGBA'); bg.paste(im, xy, im)
s1 = Image.open('../s1/hoatzin.png'); s2 = Image.open('hoatzin.png')
A = Image.open('hoatzin_oogA.png'); B = Image.open('hoatzin_oogB.png')
mod = Image.open('../../MODEL.png').convert('RGB')
V = Image.new('RGB', (532 * 3, 512 + 20 + 300 + 20 + 140), (255, 255, 255))
plak(V, s1.resize((512, 512), Image.NEAREST), (0, 0)); plak(V, s2.resize((512, 512), Image.NEAREST), (532, 0))
V.paste(mod.resize((512, 512), Image.LANCZOS), (1064, 0))
X0, Y0, s = 97, 125, 833 / 62
kx0, ky0, kx1, ky1 = 0, 15, 24, 40
def kop(im): return im.crop((kx0, ky0, kx1, ky1)).resize(((kx1 - kx0) * 12, (ky1 - ky0) * 12), Image.NEAREST)
mk = mod.crop((int(X0 + (kx0 - 1) * s), int(Y0 + (ky0 - 5) * s), int(X0 + (kx1 - 1) * s), int(Y0 + (ky1 - 5) * s))).resize(kop(s1).size, Image.LANCZOS)
y = 532
for n, im in enumerate([s1, A, B]): plak(V, kop(im), (n * 308, y))
V.paste(mk, (3 * 308, y))
y = 852
for n, (im, bgc) in enumerate([(A, (255, 255, 255)), (B, (255, 255, 255)), (A, (48, 56, 64)), (B, (48, 56, 64))]):
    vak = Image.new('RGB', (64 * 3 + 20, 128), bgc)
    plak(vak, im, (0, 32)); plak(vak, im.resize((128, 128), Image.NEAREST), (84, 0))
    V.paste(vak, (n * 230, y))
V.save('vel.png')
