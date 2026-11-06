"""vel.png ronde 10: 1x en 4x (licht/donker) en uitsneden op 8x (kop, lijf, vleugel) naast de kandidaat. Draaien vanuit de repo-root."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(HERE)
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12); INK = (20, 20, 24)
def on(im, c, size):
    b = Image.new('RGBA', size, c + (255,)); b.alpha_composite(im.resize(size, Image.NEAREST)); return b.convert('RGB')
ka = Image.open(os.path.join(D, 'kandidaat/sapa_inca.png')).convert('RGBA')
sp = Image.open(os.path.join(HERE, 'sapa_inca.png')).convert('RGBA')
W = Image.new('RGB', (1120, 1210), (236, 232, 222)); d = ImageDraw.Draw(W)
for i, (im, lab) in enumerate(((ka, 'kandidaat'), (sp, 'ronde 10'))):
    for j, c in enumerate(((248, 248, 240), (40, 44, 52))):
        W.paste(on(im, c, (256, 256)), (10 + (i * 2 + j) * 266, 10))
        W.paste(on(im, c, (64, 64)), (10 + (i * 2 + j) * 266, 272))
    d.text((10 + i * 532, 340), lab + ': 4x en 1x, licht en donker', font=F, fill=INK)
y = 362
for (x0, y0, x1, y1), naam in (((8, 14, 40, 34), 'kop + stafkop'), ((8, 30, 42, 63), 'lijf, hand, poten'), ((32, 14, 56, 36), 'opgeheven vleugel')):
    w, h = (x1 - x0) * 8, (y1 - y0) * 8
    if y + h + 20 > W.height: break
    for i, (im, lab) in enumerate(((ka, 'kandidaat'), (sp, 'ronde 10'))):
        W.paste(on(im.crop((x0, y0, x1, y1)), (248, 248, 240), (w, h)), (10 + i * (w + 20), y))
        d.text((10 + i * (w + 20), y + h + 2), f'{naam} 8x, {lab}', font=F, fill=INK)
    y += h + 22
W = W.crop((0, 0, 1120, y)); W.save(os.path.join(HERE, 'vel.png'))
