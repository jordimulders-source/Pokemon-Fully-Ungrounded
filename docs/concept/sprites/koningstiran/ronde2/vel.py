"""vel.png: sprite 4x en 1x op licht en donker, naast de onderlaag en Honchkrow/Noctowl/Empoleon. Draaien vanuit de repo-root."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(HERE); R = os.path.abspath(os.path.join(D, '..', '..', '..', '..')) + '/'
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
sp = Image.open(os.path.join(HERE, 'sapa_inca.png')).convert('RGBA')
def ref(n):
    im = Image.open(R + f'graphics/pokemon/{n}/anim_front.png').crop((0, 0, 64, 64)); im.info['transparency'] = 0
    return im.convert('RGBA')
W = Image.new('RGB', (10 + 3 * 266, 10 + 256 + 30 + 64 + 40), (236, 232, 222)); d = ImageDraw.Draw(W)
for i, c in enumerate(((248, 248, 240), (40, 44, 52))):
    b = Image.new('RGBA', (256, 256), c + (255,)); b.alpha_composite(sp.resize((256, 256), Image.NEAREST)); W.paste(b.convert('RGB'), (10 + i * 266, 10))
    d.text((10 + i * 266, 270), '4x ' + ('licht' if i == 0 else 'donker'), font=F, fill=(20, 20, 24))
W.paste(Image.open(os.path.join(D, 'silhouet_v1_vel.png')).crop((10, 36, 266, 292)), (542, 10))
d.text((542, 270), 'onderlaag (poppetje)', font=F, fill=(20, 20, 24))
x = 10
for im, lab in [(sp, 'Sapa Inca'), (ref('honchkrow'), 'honchkrow'), (ref('noctowl'), 'noctowl'), (ref('empoleon'), 'empoleon')]:
    for j, c in enumerate(((248, 248, 240), (40, 44, 52))):
        b = Image.new('RGBA', (64, 64), c + (255,)); b.alpha_composite(im); W.paste(b.convert('RGB'), (x + j * 68, 292))
    d.text((x, 360), lab + ' 1x', font=F, fill=(20, 20, 24)); x += 200
W.save(os.path.join(HERE, 'vel.png'))
