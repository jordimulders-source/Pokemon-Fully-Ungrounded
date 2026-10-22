"""Vergelijkingsvel ronde 2: ronde 1 en ronde 2 naast Dark-dieven en de Hoenn-starters.
Rij 1: 3x; rij 2: 1x; rij 3: silhouet 2x; rij 4: silhouet 1x.
python3 compare.py <ronde2/anim_front.png> <ronde1/anim_front.png> <uit.png>"""
import sys
sys.path.insert(0, '/home/user/projectgrounded/tools/concept/sprites')
import numpy as np
from PIL import Image, ImageDraw
import spritelib as L

r2, r1, out = sys.argv[1:4]


def own(path, k):
    a, pal = L.load_png(path)
    return L.rgb_img(a[64 * k:64 * (k + 1)], pal)


def mon(sp):
    for w in ('gba', 'new'):
        try:
            fr, pal = L.load_front(sp, w)
            return L.rgb_img(fr[0], pal)
        except Exception:
            pass


cols = [('ronde 1', own(r1, 0)), ('ronde 2 f1', own(r2, 0)), ('ronde 2 f2', own(r2, 1))]
for sp in ['nickit', 'purrloin', 'sneasel', 'zigzagoon/galar', 'impidimp', 'treecko', 'torchic', 'mudkip']:
    cols.append((sp, mon(sp)))


def sil(im):
    a = np.array(im); a[a[..., 3] > 0, :3] = (24, 24, 24); return Image.fromarray(a)


z = 3; S = 64 * z; G = 6
W = len(cols) * (S + G) + G
H = 14 + S + 14 + 64 + 14 + 128 + 14 + 64 + 20
sheet = Image.new('RGB', (W, H), (244, 242, 236)); d = ImageDraw.Draw(sheet)
y = 2
for i, (n, im) in enumerate(cols):
    x = G + i * (S + G)
    d.text((x, y), n, fill=(150, 20, 20) if n.startswith('ronde 2') else (0, 0, 0))
    sheet.paste(L.checker_bg(S, S, 4 * z).convert('RGB'), (x, y + 12))
    bg = L.checker_bg(S, S, 4 * z); bg.alpha_composite(L.scaled(im, z)); sheet.paste(bg.convert('RGB'), (x, y + 12))
y += 12 + S + 4
d.text((G, y), 'op 1x (zoals in de game)', fill=(0, 0, 0)); y += 12
for i, (n, im) in enumerate(cols):
    b = Image.new('RGBA', (64, 64), (248, 248, 248, 255)); b.alpha_composite(im)
    sheet.paste(b.convert('RGB'), (G + i * 70, y))
y += 64 + 4
d.text((G, y), 'silhouettest (2x en 1x): leest ronde 2 nog als Sentret/eekhoorn?', fill=(0, 0, 0)); y += 12
for i, (n, im) in enumerate(cols):
    b = Image.new('RGBA', (64, 64), (248, 248, 248, 255)); b.alpha_composite(sil(im))
    sheet.paste(b.convert('RGB').resize((128, 128), Image.NEAREST), (G + i * 134, y))
y += 128 + 4
for i, (n, im) in enumerate(cols):
    b = Image.new('RGBA', (64, 64), (248, 248, 248, 255)); b.alpha_composite(sil(im))
    sheet.paste(b.convert('RGB'), (G + i * 70, y))
sheet.save(out); print(out, sheet.size)
