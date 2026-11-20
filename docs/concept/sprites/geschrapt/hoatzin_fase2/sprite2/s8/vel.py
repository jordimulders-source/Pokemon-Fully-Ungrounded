# vel.py [vorige]: sN | sN-1 | model (8x); kop 12x: sN | sN-1 | model; 1x/2x op licht en donker
import sys
from PIL import Image
def plak(bg, im, xy):
    im = im.convert('RGBA'); bg.paste(im, xy, im)
nu = Image.open('hoatzin.png'); vor = Image.open(sys.argv[1] if len(sys.argv) > 1 else '../s2/hoatzin.png')
mod = Image.open('../../MODEL.png').convert('RGB')
V = Image.new('RGB', (532 * 3, 512 + 20 + 300 + 20 + 140), (255, 255, 255))
plak(V, nu.resize((512, 512), Image.NEAREST), (0, 0)); plak(V, vor.resize((512, 512), Image.NEAREST), (532, 0))
V.paste(mod.resize((512, 512), Image.LANCZOS), (1064, 0))
X0, Y0, s = 97, 125, 833 / 62
kx0, ky0, kx1, ky1 = 0, 15, 24, 40
def kop(im): return im.crop((kx0, ky0, kx1, ky1)).resize(((kx1 - kx0) * 12, (ky1 - ky0) * 12), Image.NEAREST)
mk = mod.crop((int(X0 + (kx0 - 1) * s), int(Y0 + (ky0 - 5) * s), int(X0 + (kx1 - 1) * s), int(Y0 + (ky1 - 5) * s))).resize(kop(nu).size, Image.LANCZOS)
plak(V, kop(nu), (0, 532)); plak(V, kop(vor), (308, 532)); V.paste(mk, (616, 532))
for n, (im, bgc) in enumerate([(nu, (255, 255, 255)), (nu, (232, 240, 248)), (nu, (48, 56, 64)), (vor, (255, 255, 255))]):
    vak = Image.new('RGB', (64 * 3 + 20, 128), bgc)
    plak(vak, im, (0, 32)); plak(vak, im.resize((128, 128), Image.NEAREST), (84, 0))
    V.paste(vak, (n * 230, 852))
V.save('vel.png')
