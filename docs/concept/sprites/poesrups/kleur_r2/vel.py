"""vel.png: sprite 8x | model zelfde uitsnede 8x ; 1x/2x op licht en donker + model (BOX) ; familie op 2x ; 3 oogvarianten (close-up 8x, 1x, 2x)."""
import os
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, '..', '..')
k = 16.648; X0, Y0 = 69 - k*5, 240 - k*29
src = Image.open(os.path.join(H, '..', 'referenties', 'model_gekozen.png')).convert('RGB')
big = Image.new('RGB', (int(64*k)+40, int(64*k)+40), (254, 254, 254)); big.paste(src, (int(-X0), int(-Y0)))
LI, DO = (232, 232, 224, 255), (40, 40, 56, 255)
def spr(p, col=LI):
    b = Image.new('RGBA', (64, 64), col); b.alpha_composite(Image.open(p).convert('RGBA')); return b.convert('RGB')
def up(im, z): return im.resize((im.width*z, im.height*z), Image.NEAREST)
A = os.path.join(H, 'poesrups.png'); bx = (2, 26, 62, 63)
V = Image.new('RGB', (1480, 1150), (255, 255, 255)); d = ImageDraw.Draw(V)
d.text((4, 2), 'poesrups kleur_r2 (8x)', fill=0); V.paste(up(spr(A).crop(bx), 8), (0, 16))
d.text((490, 2), 'kleur_r1 (8x)', fill=0); V.paste(up(spr(os.path.join(H, '..', 'kleur_r1', 'poesrups.png')).crop(bx), 8), (490, 16))
d.text((980, 2), 'model, zelfde uitsnede (8x)', fill=0)
V.paste(big.crop((int(bx[0]*k), int(bx[1]*k), int(bx[2]*k), int(bx[3]*k))).resize((480, 296), Image.LANCZOS), (980, 16))
y = 330; d.text((4, y), '1x en 2x op licht en donker; rechts het model verkleind (BOX) op 1x/2x', fill=0); y += 16
mod1 = big.crop((0, 0, int(64*k), int(64*k))).resize((64, 64), Image.BOX)
x = 0
for c in (LI, DO): V.paste(spr(A, c), (x, y)); x += 70
V.paste(mod1, (x, y)); x += 80
for c in (LI, DO): V.paste(up(spr(A, c), 2), (x, y)); x += 134
V.paste(up(mod1, 2), (x, y))
y += 140; d.text((4, y), 'familie op 2x: poedellarve | poesrups | poedelmot', fill=0); y += 16
x = 0
for p in (os.path.join(S, 'poedellarve/af/poedellarve.png'), A, os.path.join(S, 'poedelmot/af/poedelmot.png')):
    V.paste(up(spr(p), 2), (x, y)); x += 134
y += 140
for nm, p, t in (('A', A, 'A (in de sprite): Weedle 2x2, witte glans; ver oog 1x2 zwart'),
                 ('B', os.path.join(H, 'poesrups_oogB.png'), 'B: Sewaddle 4x4 rond met glans; ver oog Weedle 2x2'),
                 ('C', os.path.join(H, 'poesrups_oogC.png'), 'C: Snom 2x2, glans lichtgrijs; ver oog 1x2 zwart')):
    d.text((4, y), 'oog ' + t, fill=0); y += 16
    V.paste(up(spr(p).crop((5, 48, 27, 62)), 8), (0, y)); V.paste(spr(p), (190, y)); V.paste(spr(p, DO), (260, y))
    V.paste(up(spr(p), 2), (330, y)); V.paste(up(spr(p, DO), 2), (464, y)); y += 134
V.crop((0, 0, 1470, y)).save(os.path.join(H, 'vel.png'))
up(spr(A), 8).save(os.path.join(H, 'poesrups_8x.png'))
