"""vel.png ronde 14: 4x en 1x licht/donker naast ronde 13; de zones op 12x naast ronde 13. Draaien vanuit de repo-root."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(HERE)
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12); INK = (20, 20, 24)
def on(im, c, size):
    b = Image.new('RGBA', size, c + (255,)); b.alpha_composite(im.resize(size, Image.NEAREST)); return b.convert('RGB')
sp = Image.open(os.path.join(HERE, 'sapa_inca.png')).convert('RGBA')
r13 = Image.open(os.path.join(D, 'ronde13/sapa_inca.png')).convert('RGBA')
zones = [((12, 42, 24, 52), 'overgang staf/lijf'), ((11, 14, 19, 24), 'stafpunt'), ((20, 52, 36, 63), 'poten'),
         ((20, 21, 34, 28), 'kop (verre oog)'), ((38, 15, 52, 26), 'kroonrand rechts')]
Z = 12
rowh = max((y1 - y0) for (x0, y0, x1, y1), _ in zones) * Z + 24
W = Image.new('RGB', (1240, 360 + 2 * rowh + 40), (236, 232, 222)); d = ImageDraw.Draw(W)
for i, (im, lab) in enumerate(((r13, 'ronde 13'), (sp, 'ronde 14'))):
    for j, c in enumerate(((248, 248, 240), (40, 44, 52))):
        x = 10 + (i * 2 + j) * 266
        W.paste(on(im, c, (256, 256)), (x, 10)); W.paste(on(im, c, (64, 64)), (x, 270))
    d.text((10 + i * 532, 338), lab + ': 4x en 1x, licht en donker', font=F, fill=INK)
x, y = 10, 360
for (x0, y0, x1, y1), naam in zones:
    w, h = (x1 - x0) * Z, (y1 - y0) * Z
    if x + 2 * w + 30 > W.width:
        x, y = 10, y + rowh
    for i, (im, lab) in enumerate(((r13, '13'), (sp, '14'))):
        W.paste(on(im.crop((x0, y0, x1, y1)), (248, 248, 240), (w, h)), (x, y)); d.text((x, y + h + 2), f'{naam} 12x, ronde {lab}', font=F, fill=INK); x += w + 8
    x += 16
W = W.crop((0, 0, 1240, y + rowh + 10)); W.save(os.path.join(HERE, 'vel.png'))
