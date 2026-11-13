"""vel.png: r4 | r2 | model (zelfde uitsnede) op 8x ; 1x en 2x op licht en donker (r4 en r2) ; r4 op 2x naast Gen 3-studie en familie."""
import os
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, '..', '..')
G = '/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
k = 16.648; X0, Y0 = 69 - k*5, 240 - k*29
src = Image.open(os.path.join(H, '..', 'referenties', 'model_gekozen.png')).convert('RGB')
big = Image.new('RGB', (int(64*k)+40, int(64*k)+40), (254, 254, 254)); big.paste(src, (int(-X0), int(-Y0)))
LI, DO = (232, 232, 224, 255), (40, 40, 56, 255)
def spr(p, col=LI):
    b = Image.new('RGBA', (64, 64), col); b.alpha_composite(Image.open(p).crop((0, 0, 64, 64)).convert('RGBA')); return b.convert('RGB')
def up(im, z): return im.resize((im.width*z, im.height*z), Image.NEAREST)
A = os.path.join(H, 'poesrups.png'); B = os.path.join(H, '..', 'kleur_r2', 'poesrups.png'); bx = (2, 26, 62, 63)
V = Image.new('RGB', (1480, 900), (255, 255, 255)); d = ImageDraw.Draw(V)
d.text((4, 2), 'poesrups kleur_r4 (8x)', fill=0); V.paste(up(spr(A).crop(bx), 8), (0, 16))
d.text((490, 2), 'kleur_r2 (8x)', fill=0); V.paste(up(spr(B).crop(bx), 8), (490, 16))
d.text((980, 2), 'model, zelfde uitsnede (8x)', fill=0)
V.paste(big.crop((int(bx[0]*k), int(bx[1]*k), int(bx[2]*k), int(bx[3]*k))).resize((480, 296), Image.LANCZOS), (980, 16))
y = 330; d.text((4, y), 'r4: 1x en 2x op licht en donker   |   r2: idem', fill=0); y += 16
x = 0
for p in (A, B):
    for c in (LI, DO): V.paste(spr(p, c), (x, y)); x += 70
    for c in (LI, DO): V.paste(up(spr(p, c), 2), (x, y)); x += 134
    x += 30
y += 140; d.text((4, y), 'r4 op 2x naast Gen 3 (silcoon, dewgong, seel, altaria, swablu, castform) en familie (poedellarve, poesrups r4, poedelmot)', fill=0); y += 16
x = 0
for p in (A, G+'silcoon/anim_front_gba.png', G+'dewgong/anim_front_gba.png', G+'seel/anim_front_gba.png', G+'altaria/anim_front_gba.png',
          G+'swablu/anim_front_gba.png', G+'castform/front_gba.png'):
    V.paste(up(spr(p), 2), (x, y)); x += 134
y += 140; x = 0
for p in (os.path.join(S, 'poedellarve/af/poedellarve.png'), A, os.path.join(S, 'poedelmot/af/poedelmot.png')):
    for c in (LI, DO): V.paste(up(spr(p, c), 2), (x, y)); x += 134
y += 134
V.crop((0, 0, 1470, y)).save(os.path.join(H, 'vel.png'))
up(spr(A), 8).save(os.path.join(H, 'poesrups_8x.png'))
