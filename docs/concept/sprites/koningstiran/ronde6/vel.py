"""vel.png ronde 6: 4x licht/donker, hele lijf 6x naast ronde 5b, overlay van Jordi's krabbel, 1x naast ronde 5b en Honchkrow/Staraptor. Draaien vanuit de repo-root."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(HERE); R = os.path.abspath(os.path.join(D, '..', '..', '..', '..')) + '/'
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12); INK = (20, 20, 24)
sp = Image.open(os.path.join(HERE, 'sapa_inca.png')).convert('RGBA')
r5 = Image.open(os.path.join(D, 'ronde5b/sapa_inca.png')).convert('RGBA')
def ref(n):
    im = Image.open(R + f'graphics/pokemon/{n}/anim_front.png').crop((0, 0, 64, 64)); im.info['transparency'] = 0
    return im.convert('RGBA')
def on(im, c, size):
    b = Image.new('RGBA', size, c + (255,)); b.alpha_composite(im.resize(size, Image.NEAREST)); return b.convert('RGB')
W = Image.new('RGB', (1260, 900), (236, 232, 222)); d = ImageDraw.Draw(W)
for i, c in enumerate(((248, 248, 240), (40, 44, 52))):
    W.paste(on(sp, c, (256, 256)), (10 + i * 266, 10)); d.text((10 + i * 266, 270), 'ronde 6, 4x ' + ('licht' if i == 0 else 'donker'), font=F, fill=INK)
body = (8, 26, 44, 63)
for i, (im, lab) in enumerate(((r5, 'ronde 5b'), (sp, 'ronde 6'))):
    W.paste(on(im.crop(body), (248, 248, 240), (216, 222)), (552 + i * 230, 10)); d.text((552 + i * 230, 236), 'lijf 6x ' + lab, font=F, fill=INK)
ov = Image.open(os.path.join(HERE, 'overlay.png')).convert('RGB')
W.paste(ov, (10, 300)); d.text((10, 300 + ov.height + 2), 'overlay: rode lijnen van Jordi (uitgelijnd, 8,25 px per spritepixel)', font=F, fill=INK)
x = 10; y0 = 300 + ov.height + 24
for im, lab in [(sp, 'ronde 6'), (r5, 'ronde 5b'), (ref('honchkrow'), 'honchkrow'), (ref('staraptor'), 'staraptor')]:
    for j, c in enumerate(((248, 248, 240), (40, 44, 52))):
        W.paste(on(im, c, (64, 64)), (x + j * 68, y0))
    d.text((x, y0 + 68), lab + ' 1x', font=F, fill=INK); x += 160
W = W.crop((0, 0, 1260, y0 + 90)); W.save(os.path.join(HERE, 'vel.png'))
