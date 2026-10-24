"""Stap 2: silhouet op spritegrootte uit het 3D-poppetje (52°), naast echte Gen 3-sprites.
Draaien vanuit de repo-root: python3 docs/concept/ontwerp/olinguito_v2/scripts/silhouet.py"""
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pop3d

OUT = os.path.join(HERE, '..')
REFS = ['linoone', 'zigzagoon', 'growlithe', 'poochyena', 'rattata', 'sentret', 'mudkip', 'torchic']
SIL = (70, 66, 84)


def mask_of(img):
    a = np.array(img.convert('RGB')).astype(int)
    return (a.sum(2) < 740)


def sprite_sil(target_area):
    big = pop3d.view(pop3d.olinguito(), 52, size=250)
    m = Image.fromarray((mask_of(big) * 255).astype(np.uint8))
    lo, hi = 20, 64
    for _ in range(20):                       # zoek de maat die het doeloppervlak geeft
        s = (lo + hi) / 2
        small = np.array(m.resize((round(s), round(s)), Image.BOX)) > 127
        if small.sum() < target_area:
            lo = s
        else:
            hi = s
    s = round((lo + hi) / 2)
    small = np.array(m.resize((s, s), Image.BOX)) > 127
    ys, xs = np.nonzero(small)
    small = small[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    out = np.zeros((64, 64), bool)
    h, w = small.shape
    y0, x0 = 64 - h - 4, (64 - w) // 2
    out[y0:y0 + h, x0:x0 + w] = small
    return out


def ref_sil(name):
    p = os.path.join('graphics/pokemon', name, 'anim_front.png')
    im = Image.open(p)
    im = im.crop((0, 0, 64, 64))
    a = np.array(im)
    return a != 0 if a.ndim == 2 else a[..., 3] > 0


def tile(m, k):
    im = Image.new('RGB', (64, 64), 'white')
    arr = np.array(im)
    arr[m] = SIL
    return Image.fromarray(arr).resize((64 * k, 64 * k), Image.NEAREST)


def main():
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14)
    ols = [(f'olinguito {a} px', sprite_sil(a)) for a in (850, 950)]
    refs = [(n, ref_sil(n)) for n in REFS]
    allm = ols + refs
    W = 12 + len(allm) * 76
    im = Image.new('RGB', (max(W, 12 + 2 * 204), 30 + 80 + 20 + 204 + 20), 'white')
    d = ImageDraw.Draw(im)
    d.text((10, 6), 'Olinguito: silhouet op spritegrootte (1x, en 3x hieronder), naast echte Gen 3-sprites', font=FB, fill=(30, 30, 30))
    for i, (n, m) in enumerate(allm):
        im.paste(tile(m, 1), (12 + i * 76, 32))
        d.text((12 + i * 76, 100), f'{n.split()[0][:9]}', font=F, fill=(80, 80, 80))
        d.text((12 + i * 76, 112), f'{int(m.sum())} px', font=F, fill=(80, 80, 80))
    for i, (n, m) in enumerate(ols):
        im.paste(tile(m, 3), (12 + i * 204, 132))
    im.save(os.path.join(OUT, 'silhouet.png'))
    for n, m in ols:
        Image.fromarray((m * 255).astype(np.uint8)).save(os.path.join(OUT, f'silhouet_{n.split()[1]}.png'))


main()
