"""compare.png ronde 4: ronde 3 en 4 (f1, f2) naast Gen 3-viervoeters en de Hoenn-starters
(GBA-sprites), op 3x en 1x, in kleur en als silhouet.  python3 compare4.py <uit.png>"""
import sys
sys.path.insert(0, '/home/user/projectgrounded/tools/concept/sprites')
import numpy as np
from PIL import Image, ImageDraw
import spritelib as L
R = '/home/user/projectgrounded/docs/concept/sprites/alpaca/'
def own(path, k):
    a, pal = L.load_png(path); return L.rgb_img(a[k * 64:(k + 1) * 64], pal)
def mon(sp):
    fr, pal = L.load_front(sp, 'gba'); return L.rgb_img(fr[0], pal)
items = [('ronde 3 f1', own(R + 'ronde3/anim_front.png', 0)), ('ronde 3 f2', own(R + 'ronde3/anim_front.png', 1)),
         ('ronde 4 f1', own(R + 'ronde4/anim_front.png', 0)), ('ronde 4 f2', own(R + 'ronde4/anim_front.png', 1))]
items += [(s, mon(s)) for s in ('mareep', 'ponyta', 'growlithe', 'skitty', 'electrike', 'houndour',
                                'poochyena', 'girafarig', 'torchic', 'mudkip', 'treecko')]
def sil(im):
    a = np.array(im); a[a[..., 3] > 0, :3] = (24, 24, 24); return Image.fromarray(a)
Z, S = 3, 192
W = len(items) * (S + 4) + 4
H = 14 + 2 * (S + 16) + 20 + 2 * 70
sh = Image.new('RGB', (W, H), (244, 242, 234)); d = ImageDraw.Draw(sh)
for i, (n, im) in enumerate(items):
    x = 4 + i * (S + 4)
    d.text((x, 2), n, fill=(120, 20, 20) if n.startswith('ronde') else (0, 0, 0))
    for j, img in enumerate((im, sil(im))):
        bg = L.checker_bg(S, S, 4 * Z); bg.alpha_composite(L.scaled(img, Z))
        sh.paste(bg.convert('RGB'), (x, 14 + j * (S + 16)))
y = 14 + 2 * (S + 16) + 6
d.text((4, y - 2), '1x (echte grootte), kleur en silhouet; referenties = GBA-sprites (Gen 3)', fill=(0, 0, 0))
for j in range(2):
    for i, (n, im) in enumerate(items):
        img = im if j == 0 else sil(im)
        bg = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); bg.alpha_composite(img)
        sh.paste(bg.convert('RGB'), (4 + i * 68, y + 12 + j * 68))
sh.save(sys.argv[1]); print(sys.argv[1], sh.size)
