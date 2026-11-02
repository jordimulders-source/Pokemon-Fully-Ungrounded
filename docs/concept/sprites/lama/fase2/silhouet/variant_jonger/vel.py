"""Vel variant jonger (alleen kijken/bouwen): variant_jonger.txt -> variant_jonger_1x.png en vel.png.
Rij 1 (4x): silhouet ronde 2 | variant jonger | alpaca fase 1 | ontwerp fase 3Y (lijn_ronde2.png, uitsnede).
Rij 2 (1x): ronde 2 | variant | kleur 2c | kleur ronde 3 | alpaca."""
import os
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); L = os.path.join(H, '../../../..')
C = (108, 58, 32, 255)
def sil(p):
    rows = [l.rstrip('\n') for l in open(p)][:64]
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    for y, r in enumerate(rows):
        for x, c in enumerate(r[:64]):
            if c == '#': im.putpixel((x, y), C)
    return im, sum(r.count('#') for r in rows)
def fr(p):
    im = Image.open(p)
    if im.mode == 'P': im.info['transparency'] = 0
    return im.convert('RGBA').crop((0, 0, 64, 64))
r2, n2 = sil(os.path.join(H, '../ronde2.txt')); vj, nj = sil(os.path.join(H, 'variant_jonger.txt'))
pal = Image.new('P', (64, 64)); pal.putpalette([152, 208, 160, 108, 58, 32] + [0] * 762)
pal.putdata([1 if vj.getpixel((x, y))[3] else 0 for y in range(64) for x in range(64)]); pal.save(os.path.join(H, 'variant_jonger_1x.png'), transparency=0)
alp = fr(os.path.join(L, 'alpaca/ronde17/variant_kop/anim_front.png'))
c2 = fr(os.path.join(L, 'lama/fase2/kleur/ronde2c/lama.png')); c3 = fr(os.path.join(L, 'lama/fase2/kleur/ronde3/lama.png'))
f3 = Image.open(os.path.join(L, 'lama/ontwerp/lijn_ronde2.png')).convert('RGBA').crop((610, 50, 880, 380))
f3 = f3.resize((int(f3.width * 256 / f3.height), 256), Image.LANCZOS)
BG = (240, 238, 230, 255)
W = Image.new('RGBA', (3 * 268 + f3.width + 24, 20 + 256 + 30 + 70 + 20), BG); d = ImageDraw.Draw(W)
d.text((8, 4), f'4x: silhouet ronde 2 ({n2} px) | variant jonger ({nj} px) | alpaca fase 1 | ontwerp fase 3Y', fill=(0, 0, 0))
x = 8
for im in (r2, vj, alp):
    z = im.resize((256, 256), Image.NEAREST); W.paste(z, (x, 20), z); x += 268
W.paste(f3, (x, 20), f3)
y = 20 + 256 + 10
d.text((8, y), '1x: ronde 2 | variant jonger | kleur 2c | kleur ronde 3 | alpaca', fill=(0, 0, 0)); y += 16
x = 8
for im in (r2, vj, c2, c3, alp):
    W.paste(im, (x, y), im); x += 76
W.save(os.path.join(H, 'vel.png'))
print(n2, nj)
