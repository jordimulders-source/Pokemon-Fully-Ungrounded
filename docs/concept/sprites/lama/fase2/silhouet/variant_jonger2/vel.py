"""Vel jonger2 (alleen kijken). Rij 1 (4x): silhouet ronde 2 | silhouet jonger2 | PROEF jonger2 | alpaca | fase 3Y (ontwerp).
Rij 2 (2x): kleur ronde 3 | PROEF jonger2 | Charmander -> Charmeleon | Mudkip -> Marshtomp (verhoudingsmaatstaf).
Rij 3 (1x): ronde 2 | jonger2 | kleur 2c | kleur ronde 3 | PROEF jonger2 | alpaca | Charmander | Charmeleon | Mudkip | Marshtomp."""
import os
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); L = os.path.join(H, '../../../..'); G = os.path.join(L, '../../../graphics/pokemon')
C = (108, 58, 32, 255)
def sil(p):
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    for y, r in enumerate([l.rstrip('\n') for l in open(p)][:64]):
        for x, c in enumerate(r[:64]):
            if c == '#': im.putpixel((x, y), C)
    return im
def fr(p):
    im = Image.open(p)
    if im.mode == 'P': im.info['transparency'] = 0
    return im.convert('RGBA').crop((0, 0, 64, 64))
r2 = sil(os.path.join(H, '../ronde2.txt')); j2 = sil(os.path.join(H, 'variant_jonger2.txt')); pr = fr(os.path.join(H, 'proef_lama.png'))
alp = fr(os.path.join(L, 'alpaca/ronde17/variant_kop/anim_front.png'))
c2 = fr(os.path.join(L, 'lama/fase2/kleur/ronde2c/lama.png')); c3 = fr(os.path.join(L, 'lama/fase2/kleur/ronde3/lama.png'))
pk = {n: fr(os.path.join(G, n, 'anim_front.png')) for n in ('charmander', 'charmeleon', 'mudkip', 'marshtomp')}
f3 = Image.open(os.path.join(L, 'lama/ontwerp/lijn_ronde2.png')).convert('RGBA').crop((610, 50, 880, 380))
f3 = f3.resize((int(f3.width * 256 / f3.height), 256), Image.LANCZOS)
BG = (240, 238, 230, 255)
W = Image.new('RGBA', (4 * 266 + f3.width + 16, 22 + 256 + 22 + 128 + 22 + 70), BG); d = ImageDraw.Draw(W)
d.text((8, 4), '4x: silhouet ronde 2 (1278 px) | silhouet jonger2 (1350 px) | PROEF jonger2 (ruw, niet afgewerkt) | alpaca fase 1 | ontwerp fase 3Y', fill=(0, 0, 0))
x = 8
for im in (r2, j2, pr, alp):
    z = im.resize((256, 256), Image.NEAREST); W.paste(z, (x, 22), z); x += 266
W.paste(f3, (x, 22), f3)
y = 22 + 256 + 6
d.text((8, y), '2x: kleur ronde 3 | PROEF jonger2 | Charmander -> Charmeleon | Mudkip -> Marshtomp', fill=(0, 0, 0)); y += 16
x = 8
for im in (c3, pr, pk['charmander'], pk['charmeleon'], pk['mudkip'], pk['marshtomp']):
    z = im.resize((128, 128), Image.NEAREST); W.paste(z, (x, y), z); x += 136
y += 128 + 6
d.text((8, y), '1x: ronde 2 | jonger2 | kleur 2c | kleur ronde 3 | PROEF jonger2 | alpaca | Charmander | Charmeleon | Mudkip | Marshtomp', fill=(0, 0, 0)); y += 16
x = 8
for im in (r2, j2, c2, c3, pr, alp, pk['charmander'], pk['charmeleon'], pk['mudkip'], pk['marshtomp']):
    W.paste(im, (x, y), im); x += 72
W.save(os.path.join(H, 'vel.png'))
