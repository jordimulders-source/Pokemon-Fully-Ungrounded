"""compare.png voor de alpaca ronde 2: ronde 1, ronde 2 (f1, f2) naast schattige
Fighting-soorten en de Hoenn-starters; vergroot, op 1x, en als silhouet in het zwart.
  python3 compare2.py <uit.png>"""
import sys
sys.path.insert(0, '/home/user/projectgrounded/tools/concept/sprites')
import numpy as np
from PIL import Image, ImageDraw
import spritelib as L

R = '/home/user/projectgrounded/docs/concept/sprites/alpaca/'
def own(path, k):
    a, pal = L.load_png(path)
    return L.rgb_img(a[k * 64:(k + 1) * 64], pal)
def mon(sp):
    for w in ('gba', 'new'):
        try:
            fr, pal = L.load_front(sp, w); return L.rgb_img(fr[0], pal)
        except Exception:
            pass
items = [('ronde 1', own(R + 'anim_front.png', 0)), ('ronde 2 f1', own(R + 'ronde2/anim_front.png', 0)),
         ('ronde 2 f2', own(R + 'ronde2/anim_front.png', 1))]
items += [(s, mon(s)) for s in ('stufful', 'bewear', 'makuhita', 'riolu', 'clobbopus', 'treecko', 'torchic', 'mudkip')]
def sil(im):
    a = np.array(im); a[a[..., 3] > 0, :3] = (24, 24, 24); return Image.fromarray(a)
Z, S = 3, 64 * 3
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
d.text((4, y - 2), '1x (echte grootte), kleur en silhouet; Hoenn-soorten als GBA-sprite, Gen 7+ als in-game sprite', fill=(0, 0, 0))
for j in range(2):
    for i, (n, im) in enumerate(items):
        img = im if j == 0 else sil(im)
        bg = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); bg.alpha_composite(img)
        sh.paste(bg.convert('RGB'), (4 + i * 68, y + 12 + j * 68))
sh.save(sys.argv[1]); print(sys.argv[1], sh.size)
