"""Vel voor Jordi (SPRITE_WERKWIJZE stap 2): onderlaag | silhouet 4x | silhouet over de onderlaag | 1x naast echte sprites.
Draaien: python3 docs/concept/sprites/wasbeer/silhouet_v2/vel.py <ronde.txt> <uit.png>"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '../../../../..')


def lees(p):
    return np.array([[c != '.' for c in r.rstrip('\n')] for r in open(p) if r.strip() and not r.startswith('#')])


def sprite_sil(naam):
    im = Image.open(os.path.join(ROOT, f'graphics/pokemon/{naam}/anim_front.png'))
    a = np.array(im)[:64, :64] != 0
    return a


def tegel(a, k, kleur=(40, 34, 34)):
    im = Image.new('RGB', (64 * k, 64 * k), 'white'); d = ImageDraw.Draw(im)
    for y, x in zip(*np.nonzero(a)):
        d.rectangle((x * k, y * k, x * k + k - 1, y * k + k - 1), fill=kleur)
    for i in range(0, 64 * k + 1, k * 8):
        d.line((i, 0, i, 64 * k), fill=(225, 225, 235)); d.line((0, i, 64 * k, i), fill=(225, 225, 235))
    return im


def vel(txt, uit, onder='onderlaag_256.png'):
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    a = lees(txt)
    under = Image.open(os.path.join(HERE, onder)).convert('RGB')
    im = Image.new('RGB', (12 + 266 * 4 + 12, 330 + 150), 'white'); d = ImageDraw.Draw(im)
    ys, xs = np.nonzero(a)
    d.text((12, 8), f'{os.path.basename(txt)}: {a.sum()} px, box {xs.max() - xs.min() + 1}x{ys.max() - ys.min() + 1}', font=F, fill=(30, 30, 30))
    im.paste(under, (12, 30)); d.text((12, 290), 'onderlaag (3D-ontwerp E2)', font=F, fill=(60, 60, 60))
    im.paste(tegel(a, 4), (12 + 266, 30)); d.text((12 + 266, 290), 'silhouet 4x', font=F, fill=(60, 60, 60))
    ov = under.copy(); px = ov.load()
    for y, x in zip(*np.nonzero(a)):
        for dy in range(4):
            for dx in range(4):
                r, g, b = px[x * 4 + dx, y * 4 + dy]; px[x * 4 + dx, y * 4 + dy] = ((r + 230) // 2, (g + 40) // 2, (b + 40) // 2)
    im.paste(ov, (12 + 266 * 2, 30)); d.text((12 + 266 * 2, 290), 'silhouet over de onderlaag', font=F, fill=(60, 60, 60))
    one = tegel(a, 1); im.paste(one.resize((128, 128), Image.NEAREST), (12 + 266 * 3, 30)); im.paste(one, (12 + 266 * 3 + 140, 30))
    d.text((12 + 266 * 3, 290), '1x en 2x', font=F, fill=(60, 60, 60))
    for i, n in enumerate(('weavile', 'sneasel', 'zangoose', 'gumshoos', 'sneasler', 'lucario', 'raticate')):
        try:
            s = sprite_sil(n)
        except Exception:
            continue
        t = tegel(s, 2, (90, 90, 100)); x = 12 + 140 * i
        im.paste(t, (x, 320)); d.text((x, 452), f'{n} {s.sum()} px', font=F, fill=(60, 60, 60))
    im.save(uit)


if __name__ == '__main__':
    vel(*sys.argv[1:4])
