# vel.png: r7 8x | r6 8x | model verkleind; daaronder 1x op licht en donker naast Regirock/Registeel (gba) en Regiaqua (af).
import numpy as np
from PIL import Image, ImageDraw
def rgba_p(path):
    im = Image.open(path); a = np.array(im); r = np.array(im.convert('RGBA')); r[a == 0, 3] = 0   # index 0 zelf transparant
    return Image.fromarray(r)
def gba(n):
    a = np.array(Image.open(f'../../../../graphics/pokemon/{n}/anim_front_gba.png'))[:64]
    pal = [list(map(int, l.split())) for l in open(f'../../../../graphics/pokemon/{n}/normal_gba.pal').read().split('\n')[3:19]]
    r = np.zeros(a.shape + (4,), np.uint8)
    for i, p in enumerate(pal): r[a == i, :3] = p; r[a == i, 3] = 0 if i == 0 else 255
    return Image.fromarray(r)
def op(im, bg, k=1):
    b = Image.new('RGBA', im.size, bg + (255,)); b.alpha_composite(im)
    return b.resize((im.width*k, im.height*k), Image.NEAREST)
r7 = rgba_p('sprite/r7/regicosmo_r7.png'); r6 = rgba_p('sprite/r6/regicosmo_r6.png')
op(r7, (255, 255, 255), 8).convert('RGB').save('sprite/r7/regicosmo_r7_8x.png')
# model: inhoud bijsnijden en op dezelfde maat als de sprite-inhoud (8x) zetten
m = Image.open('model.png').convert('RGB'); ma = np.array(m).astype(int)
ys, xs = np.nonzero((ma < 235).any(2)); m = m.crop((xs.min(), ys.min(), xs.max()+1, ys.max()+1))
sa = np.array(Image.open('sprite/r7/regicosmo_r7.png')); sy, sx = np.nonzero(sa)
mw, mh = (sx.max()-sx.min()+1)*8, (sy.max()-sy.min()+1)*8
m8 = Image.new('RGB', (512, 512), (255, 255, 255)); m8.paste(m.resize((mw, mh), Image.LANCZOS), (sx.min()*8, sy.min()*8))
G = 16; V = Image.new('RGB', (3*512 + 4*G, 512 + 2*64*2 + 6*G + 30), (235, 235, 235)); d = ImageDraw.Draw(V)
for i, (im, t) in enumerate([(op(r7, (255, 255, 255), 8), 'r7 (eindkeuring)'), (op(r6, (255, 255, 255), 8), 'r6'), (m8, 'model (verkleind)')]):
    V.paste(im.convert('RGB'), (G + i*(512+G), G+14)); d.text((G + i*(512+G), 2), t, fill=(0, 0, 0))
y0 = 512 + 2*G + 14
rij = [r7, r6, gba('regirock'), gba('registeel'), rgba_p('../regiaqua/af/regiaqua.png')]
for j, bg in enumerate([(255, 255, 255), (40, 44, 52)]):
    for i, im in enumerate(rij):
        V.paste(op(im, bg, 2).convert('RGB'), (G + i*(128+G), y0 + j*(128+G)))
d.text((G, y0 + 2*(128+G)), '2x (1x-pixels): r7 | r6 | Regirock | Registeel | Regiaqua - op licht en donker; 1x hiernaast', fill=(0, 0, 0))
for j, bg in enumerate([(255, 255, 255), (40, 44, 52)]):
    for i, im in enumerate(rij):
        V.paste(op(im, bg, 1).convert('RGB'), (G + 5*(128+G) + 20 + i*(64+6), y0 + j*(128+G)))
V.save('sprite/r7/vel.png')
