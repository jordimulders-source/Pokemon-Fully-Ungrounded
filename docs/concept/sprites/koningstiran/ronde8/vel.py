"""vel.png ronde 8: stafkop 10x naast variant B van ronde 7, sprite 4x licht/donker, 1x naast ronde 7b en variant B. Draaien vanuit de repo-root."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(HERE)
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12); INK = (20, 20, 24)
sp = Image.open(os.path.join(HERE, 'sapa_inca.png')).convert('RGBA')
vb = Image.open(os.path.join(D, 'ronde7/variant_top_zon.png')).convert('RGBA')
r7 = Image.open(os.path.join(D, 'ronde7b/sapa_inca.png')).convert('RGBA')
def on(im, c, size):
    b = Image.new('RGBA', size, c + (255,)); b.alpha_composite(im.resize(size, Image.NEAREST)); return b.convert('RGB')
W = Image.new('RGB', (10 + 2 * 266 + 2 * 170 + 20, 400), (236, 232, 222)); d = ImageDraw.Draw(W)
for i, c in enumerate(((248, 248, 240), (40, 44, 52))):
    W.paste(on(sp, c, (256, 256)), (10 + i * 266, 10)); d.text((10 + i * 266, 270), 'ronde 8, 4x ' + ('licht' if i == 0 else 'donker'), font=F, fill=INK)
tc = (8, 17, 24, 39)
for i, (im, lab) in enumerate(((vb, 'ronde 7 variant B'), (sp, 'ronde 8'))):
    W.paste(on(im.crop(tc), (248, 248, 240), (160, 220)), (552 + i * 170, 10)); d.text((552 + i * 170, 236), '10x ' + lab, font=F, fill=INK)
x = 10
for im, lab in ((sp, 'ronde 8'), (vb, 'ronde 7 variant B'), (r7, 'ronde 7b')):
    for j, c in enumerate(((248, 248, 240), (40, 44, 52))):
        W.paste(on(im, c, (64, 64)), (x + j * 68, 300))
    d.text((x, 368), lab + ' 1x', font=F, fill=INK); x += 200
W.save(os.path.join(HERE, 'vel.png'))
