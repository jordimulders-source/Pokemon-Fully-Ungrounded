"""vel.png r3: r3 | af (r2 gespiegeld) | gespiegeld model op 8x; 1x/2x op licht en donker; r3 naast poedelmot af op 8x."""
import os
from PIL import Image, ImageDraw, ImageOps
H = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(H, '..')
k = 13.55; X0, Y0 = 236 - k*12, 346 - k*33
src = Image.open(os.path.join(P, 'referenties', 'model_gekozen.png')).convert('RGB')
mod = ImageOps.mirror(src.crop((int(X0), int(Y0), int(X0+64*k), int(Y0+64*k))).resize((512, 512), Image.LANCZOS))
mod1 = ImageOps.mirror(src.crop((int(X0), int(Y0), int(X0+64*k), int(Y0+64*k))).resize((64, 64), Image.BOX))
def sprite(path, col=(152, 208, 160, 255)):
    p = Image.open(path).convert('RGBA'); b = Image.new('RGBA', p.size, col); b.alpha_composite(p); return b.convert('RGB')
r3 = os.path.join(H, 'poedellarve.png'); af = os.path.join(P, 'af', 'poedellarve.png')
mot = os.path.join(P, '..', 'poedelmot', 'af', 'poedelmot.png')
V = Image.new('RGB', (3*528, 24+512+40+150+24+512), 'white'); d = ImageDraw.Draw(V)
for i, (im, t) in enumerate([(sprite(r3).resize((512, 512), Image.NEAREST), 'kleur_r3 (8x)'), (sprite(af).resize((512, 512), Image.NEAREST), 'af = r2 gespiegeld (8x)'), (mod, 'model gespiegeld (8x)')]):
    V.paste(im, (i*528, 24)); d.text((i*528+4, 6), t, fill=(0, 0, 0))
y = 24+512+16; d.text((4, y), 'r3 1x en 2x op licht en donker, naast het gespiegelde model (BOX)', fill=(0, 0, 0)); y += 18
x = 0
for col in [(232, 232, 224, 255), (40, 40, 56, 255)]:
    V.paste(sprite(r3, col), (x, y)); x += 72
V.paste(mod1, (x, y)); x += 80
for col in [(232, 232, 224, 255), (40, 40, 56, 255)]:
    V.paste(sprite(r3, col).resize((128, 128), Image.NEAREST), (x, y)); x += 136
V.paste(mod1.resize((128, 128), Image.NEAREST), (x, y))
y += 150; d.text((4, y), 'r3 naast poedelmot (af) op 8x', fill=(0, 0, 0)); y += 18
V.paste(sprite(r3).resize((512, 512), Image.NEAREST), (0, y)); V.paste(sprite(mot).resize((512, 512), Image.NEAREST), (528, y))
V.save(os.path.join(H, 'vel.png'))
