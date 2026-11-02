"""Vergelijkingsvel ronde 2c (alleen kijken): rij 1 = 2c op 4x licht + donker, 2b op 4x ernaast;
rij 2 = 1x en 3x licht/donker: 2c, 2b, alpaca (fase 1), Flaaffy, Stantler, Ponyta."""
import os
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
R = os.path.join(HERE, '../../../../../../../..')
def fr(p):
    im = Image.open(p)
    if im.mode == 'P': im.info['transparency'] = 0
    return im.convert('RGBA').crop((0, 0, 64, 64))
c = fr(os.path.join(OUT, 'lama.png')); b = fr(os.path.join(OUT, '../ronde2b/lama.png'))
alp = fr(os.path.join(HERE, '../../../../../alpaca/ronde17/variant_kop/anim_front.png'))
refs = [(n, fr(os.path.join(R, f'graphics/pokemon/{n.lower()}/anim_front.png'))) for n in ('Flaaffy', 'Stantler', 'Ponyta')]
L, D = (240, 238, 230, 255), (38, 38, 54, 255)
W = Image.new('RGBA', (6 * 196 + 8, 18 + 256 + 10 + 2 * (16 + 192 + 8) + 2 * 74), L)
d = ImageDraw.Draw(W)
def put(im, s, x, y, bg):
    W.paste(Image.new('RGBA', (64 * s, 64 * s), bg), (x, y)); z = im.resize((64 * s, 64 * s), Image.NEAREST); W.paste(z, (x, y), z)
y = 2
d.text((12, y), '4x: ronde 2c (licht) | ronde 2c (donker) | ronde 2b (licht)', fill=(0, 0, 0)); y += 16
put(c, 4, 12, y, L); put(c, 4, 280, y, D); put(b, 4, 548, y, L); y += 256 + 10
row = [('2c', c), ('2b', b), ('alpaca', alp)] + refs
for bg in (L, D):
    d.text((12, y), '3x: ' + ' | '.join(n for n, _ in row), fill=(0, 0, 0)); y += 16
    x = 4
    for n, im in row:
        put(im, 3, x, y, bg); x += 196
    y += 192 + 8
for bg in (L, D):
    W.paste(Image.new('RGBA', (W.width, 70), bg), (0, y)); x = 12
    for n, im in row:
        W.paste(im, (x, y + 3), im); x += 72
    y += 74
W.save(os.path.join(OUT, 'vel.png'))
