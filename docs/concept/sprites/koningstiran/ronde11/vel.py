"""vel.png ronde 11: 4x en 1x licht/donker naast ronde 10; 4x naast Armarouge, Corviknight, Kilowattrel; kop 8x en staf 8x naast ronde 10. Draaien vanuit de repo-root."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(HERE); R = os.path.abspath(os.path.join(D, '..', '..', '..', '..')) + '/'
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12); INK = (20, 20, 24)
def on(im, c, size):
    b = Image.new('RGBA', size, c + (255,)); b.alpha_composite(im.resize(size, Image.NEAREST)); return b.convert('RGB')
def ref(n):
    p = R + f'graphics/pokemon/{n}/'
    im = Image.open(p + ('anim_front.png' if os.path.exists(p + 'anim_front.png') else 'front.png')).crop((0, 0, 64, 64)); im.info['transparency'] = 0
    return im.convert('RGBA')
sp = Image.open(os.path.join(HERE, 'sapa_inca.png')).convert('RGBA')
r10 = Image.open(os.path.join(D, 'ronde10/sapa_inca.png')).convert('RGBA')
W = Image.new('RGB', (1080, 1150), (236, 232, 222)); d = ImageDraw.Draw(W)
for i, (im, lab) in enumerate(((r10, 'ronde 10'), (sp, 'ronde 11'))):
    for j, c in enumerate(((248, 248, 240), (40, 44, 52))):
        x = 10 + (i * 2 + j) * 266
        W.paste(on(im, c, (256, 256)), (x, 10)); W.paste(on(im, c, (64, 64)), (x, 270))
    d.text((10 + i * 532, 338), lab + ': 4x en 1x, licht en donker', font=F, fill=INK)
for i, (im, lab) in enumerate(((sp, 'ronde 11'), (ref('armarouge'), 'armarouge'), (ref('corviknight'), 'corviknight'), (ref('kilowattrel'), 'kilowattrel'))):
    W.paste(on(im, (248, 248, 240), (256, 256)), (10 + i * 266, 360)); d.text((10 + i * 266, 618), lab + ' 4x', font=F, fill=INK)
kc = (17, 17, 37, 32); sc = (10, 18, 22, 50)
for i, (im, lab) in enumerate(((r10, 'ronde 10'), (sp, 'ronde 11'))):
    W.paste(on(im.crop(kc), (248, 248, 240), (160, 120)), (10 + i * 175, 640)); d.text((10 + i * 175, 764), 'kop 8x ' + lab, font=F, fill=INK)
    W.paste(on(im.crop(sc), (248, 248, 240), (96, 256)), (380 + i * 110, 640)); d.text((380 + i * 110, 900), 'staf 8x ' + lab, font=F, fill=INK)
W = W.crop((0, 0, 1080, 920)); W.save(os.path.join(HERE, 'vel.png'))
