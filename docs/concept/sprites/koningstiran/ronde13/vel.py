"""vel.png ronde 13: 4x en 1x licht/donker naast ronde 12; kop, flank en staf op 10x naast ronde 12. Draaien vanuit de repo-root."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(HERE)
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12); INK = (20, 20, 24)
def on(im, c, size):
    b = Image.new('RGBA', size, c + (255,)); b.alpha_composite(im.resize(size, Image.NEAREST)); return b.convert('RGB')
sp = Image.open(os.path.join(HERE, 'sapa_inca.png')).convert('RGBA')
r12 = Image.open(os.path.join(D, 'ronde12/sapa_inca.png')).convert('RGBA')
W = Image.new('RGB', (1080, 900), (236, 232, 222)); d = ImageDraw.Draw(W)
for i, (im, lab) in enumerate(((r12, 'ronde 12'), (sp, 'ronde 13'))):
    for j, c in enumerate(((248, 248, 240), (40, 44, 52))):
        x = 10 + (i * 2 + j) * 266
        W.paste(on(im, c, (256, 256)), (x, 10)); W.paste(on(im, c, (64, 64)), (x, 270))
    d.text((10 + i * 532, 338), lab + ': 4x en 1x, licht en donker', font=F, fill=INK)
x = 10
for (x0, y0, x1, y1), naam in (((19, 17, 35, 30), 'kop'), ((26, 33, 40, 52), 'flank'), ((10, 16, 21, 50), 'staf')):
    w, h = (x1 - x0) * 10, (y1 - y0) * 10
    for i, (im, lab) in enumerate(((r12, 'ronde 12'), (sp, 'ronde 13'))):
        W.paste(on(im.crop((x0, y0, x1, y1)), (248, 248, 240), (w, h)), (x, 360)); d.text((x, 362 + h), f'{naam} 10x {lab}', font=F, fill=INK); x += w + 8
    x += 10
W = W.crop((0, 0, max(1080, x), 360 + 340 + 30)); W.save(os.path.join(HERE, 'vel.png'))
