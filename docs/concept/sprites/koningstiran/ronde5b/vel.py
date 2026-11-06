"""vel.png ronde 5b: 4x, gezicht 10x en linkerkant 6x naast ronde 5, 1x naast ronde 5 en referenties. Draaien vanuit de repo-root."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(HERE); R = os.path.abspath(os.path.join(D, '..', '..', '..', '..')) + '/'
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
INK = (20, 20, 24)
sp = Image.open(os.path.join(HERE, 'sapa_inca.png')).convert('RGBA')
r3 = Image.open(os.path.join(D, 'ronde5/sapa_inca.png')).convert('RGBA')
def ref(n):
    im = Image.open(R + f'graphics/pokemon/{n}/anim_front.png').crop((0, 0, 64, 64)); im.info['transparency'] = 0
    return im.convert('RGBA')
def on(im, c, size):
    b = Image.new('RGBA', size, c + (255,)); b.alpha_composite(im.resize(size, Image.NEAREST)); return b.convert('RGB')
W = Image.new('RGB', (1210, 700), (236, 232, 222)); d = ImageDraw.Draw(W)
for i, c in enumerate(((248, 248, 240), (40, 44, 52))):
    W.paste(on(sp, c, (256, 256)), (10 + i * 266, 10)); d.text((10 + i * 266, 270), 'ronde 5b, 4x ' + ('licht' if i == 0 else 'donker'), font=F, fill=INK)
fc = (20, 18, 35, 30)
for i, (im, lab) in enumerate(((r3, 'ronde 5'), (sp, 'ronde 5b'))):
    W.paste(on(im.crop(fc), (248, 248, 240), (150, 120)), (552 + i * 160, 10)); d.text((552 + i * 160, 134), 'gezicht 10x ' + lab, font=F, fill=INK)
lc = (8, 22, 38, 63)
for i, (im, lab) in enumerate(((r3, 'ronde 5'), (sp, 'ronde 5b'))):
    W.paste(on(im.crop(lc), (248, 248, 240), (180, 246)), (552 + i * 190, 160 + 0)); d.text((552 + i * 190, 410), 'linkerkant 6x ' + lab, font=F, fill=INK)
W.paste(Image.open(os.path.join(D, 'poppetje_staf_256.png')).convert('RGB').resize((180, 180)), (940, 160)); d.text((940, 345), 'onderlaag (alleen plaats)', font=F, fill=INK)
x = 10
for im, lab in [(sp, 'ronde 5b'), (r3, 'ronde 5'), (ref('honchkrow'), 'honchkrow'), (ref('staraptor'), 'staraptor'), (ref('braviary'), 'braviary')]:
    for j, c in enumerate(((248, 248, 240), (40, 44, 52))):
        W.paste(on(im, c, (64, 64)), (x + j * 68, 440))
    d.text((x, 508), lab + ' 1x', font=F, fill=INK); x += 160
W = W.crop((0, 0, 1210, 530)); W.save(os.path.join(HERE, 'vel.png'))
