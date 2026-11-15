"""vel.png: bovenaan mondcrops van de refs (artwork, 3D, pixel-ref, Haunter G3 12x);
daaronder per rij gezicht 12x | hele sprite 6x | 1x voor v7, R, S."""
from PIL import Image, ImageDraw
import os
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, '..', '..', '..', '..', '..')
REF = os.path.join(H, '..', 'referenties'); TMP = '/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/931d0048-d45a-55a4-a2ad-8ad05568e8ad/scratchpad/t.png'
def rgba(p):
    im = Image.open(p)
    if im.mode == 'P':
        im.crop((0, 0, 64, 64)).save(TMP, transparency=0); im = Image.open(TMP)
    return im.convert('RGBA')
BG = (200, 200, 210, 255); RH = 200
refs = [('artwork', Image.open(os.path.join(REF, 'haunter_artwork.png')).convert('RGBA').crop((600, 1040, 1120, 1340))),
        ('3D', Image.open(os.path.join(REF, 'haunter_3d.png')).convert('RGBA').crop((180, 255, 330, 335))),
        ('pixel-ref', Image.open(os.path.join(REF, 'haunter_pixel_ref.png')).convert('RGBA').crop((370, 320, 650, 470))),
        ('Haunter G3', rgba(os.path.join(R, 'graphics', 'pokemon', 'haunter', 'anim_front.png')).crop((14, 35, 36, 47)))]
rijen = [('v7', '../sprite_v7/hauntflare_v7.png')] + [(k, f'kandidaat_{k}.png') for k in 'RS']
W = 1560; vel = Image.new('RGBA', (W, RH + 30 + len(rijen) * (18 * 12 + 30)), BG); d = ImageDraw.Draw(vel)
x = 0
for n, im in refs:
    s = RH / im.height; im = im.resize((int(im.width * s), RH), Image.NEAREST if n == 'Haunter G3' else Image.LANCZOS)
    d.text((x + 2, 2), n, fill=(0, 0, 0, 255)); vel.alpha_composite(im, (x, 14)); x += im.width + 10
y = RH + 30
for n, p in rijen:
    im = rgba(os.path.join(H, p)); d.text((2, y), n, fill=(0, 0, 0, 255))
    f = im.crop((14, 24, 40, 42)).resize((26 * 12, 18 * 12), Image.NEAREST); vel.alpha_composite(f, (0, y + 12))
    g = im.resize((384, 384), Image.NEAREST).crop((0, 100, 384, 100 + 18 * 12)); vel.alpha_composite(g, (26 * 12 + 20, y + 12))
    vel.alpha_composite(im, (26 * 12 + 420, y + 60))
    y += 18 * 12 + 30
vel.save(os.path.join(H, 'vel.png'))
