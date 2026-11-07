"""Vel: silhouet 4x en 1x naast echte Gen 3/4-silhouetten (Natu, Togepi, Pichu, Fletchling, Taillow) en de eindvorm."""
from PIL import Image, ImageDraw, ImageFont
R = '../../../../../../graphics/pokemon/'
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
BG, INK = (236, 236, 230), (40, 30, 60)
def mask(p):
    im = Image.open(p)
    o = Image.new('L', (64, 64), 0)
    if im.mode == 'P':
        a = im.crop((0, 0, 64, 64)); o.putdata([255 if v else 0 for v in a.getdata()])
    else:
        o = im.convert('RGBA').crop((0, 0, 64, 64)).split()[3].point(lambda v: 255 if v else 0)
    return o
def sil(p):
    m = mask(p); s = Image.new('RGB', (64, 64), BG); s.paste(INK, mask=m); return s, sum(1 for v in m.getdata() if v)
items = [('pre-evo r1', 'silhouet_1x.png'), ('natu', R + 'natu/anim_front.png'), ('togepi', R + 'togepi/anim_front.png'),
         ('pichu', R + 'pichu/anim_front.png'), ('fletchling', R + 'fletchling/anim_front.png'), ('taillow', R + 'taillow/anim_front.png'),
         ('eindvorm', '../../../kolibrie/af/kolibrie.png')]
out = Image.new('RGB', (64 * 4 + 40 + 6 * 210, 64 * 4 + 120), 'white'); d = ImageDraw.Draw(out)
s, n = sil(items[0][1])
out.paste(s.resize((256, 256), Image.NEAREST), (20, 40)); d.text((20, 10), f'pre-evo silhouet r1, 4x ({n} px)', fill='black', font=FB)
for i, (name, p) in enumerate(items):
    s, n = sil(p); x = 300 + (i - 1) * 210 if i else 20
    if i:
        out.paste(s.resize((192, 192), Image.NEAREST), (x, 40)); d.text((x, 20), f'{name} {n} px (3x)', fill='black', font=F)
for i, (name, p) in enumerate(items):  # rij 1x
    s, n = sil(p); out.paste(s, (20 + i * 90, 64 * 4 + 50))
d.text((20, 64 * 4 + 120 - 16), '1x op ware grootte, zelfde volgorde', fill='black', font=F)
out.save('vel.png')
