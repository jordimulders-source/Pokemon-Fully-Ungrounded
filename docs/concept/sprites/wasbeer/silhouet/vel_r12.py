"""Wasbeer ronde 12: vergelijkingsvel. Silhouet = ronde12.txt (met de hand gelegd), onderlaag = onderlaag_r12.py.
Draaien: python3 docs/concept/sprites/wasbeer/silhouet/vel_r12.py -> vel_ronde12.png, ronde12_1x.png"""
import os
import numpy as np
from PIL import Image, ImageDraw
from onderlaag_r12 import onderlaag
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, '../../../../..')
REF = os.path.join(HERE, '../referenties')
BG = (236, 233, 226)


def load_txt(p):
    return np.array([[c == '#' for c in l.rstrip('\n')[:64].ljust(64, '.')] for l in open(p)][:64])


def sprite(name):
    im = Image.open(os.path.join(REPO, 'graphics/pokemon', name, 'anim_front.png')).convert('RGB').crop((0, 0, 64, 64))
    a = np.array(im); m = (a != a[0, 0]).any(2)
    out = np.zeros((64, 64, 4), np.uint8); out[..., :3] = a; out[..., 3] = m * 255
    return Image.fromarray(out)


def sil_img(m, col=(30, 30, 30)):
    out = np.zeros((64, 64, 4), np.uint8); out[m] = col + (255,)
    return Image.fromarray(out)


if __name__ == '__main__':
    m = load_txt(os.path.join(HERE, 'ronde12.txt'))
    Image.fromarray(np.where(m, 0, 255).astype(np.uint8)).convert('1').save(os.path.join(HERE, 'ronde12_1x.png'))
    ys, xs = np.nonzero(m)
    info = '%d px, bbox %dx%d' % (m.sum(), xs.max() - xs.min() + 1, ys.max() - ys.min() + 1)
    under, kop = onderlaag()
    ov = np.full((64, 64, 3), 255, np.uint8)
    ov[under] = (235, 160, 235); ov[kop] = (140, 210, 235)
    ov[m & ~(under | kop)] = (90, 90, 90)
    ov[m & (under | kop)] = (40, 40, 40)
    ov = Image.fromarray(ov)
    # alleen de omtrek van het silhouet over de onderlaag
    ov2 = np.full((64, 64, 3), 255, np.uint8); ov2[under] = (235, 160, 235); ov2[kop] = (140, 210, 235)
    edge = m & ~(np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1))
    ov2[edge] = (20, 20, 20); ov2 = Image.fromarray(ov2)
    cells = [('silhouet ronde 12 (4x)', sil_img(m)), ('omtrek over onderlaag (roze=foto 10, blauw=kop r11)', ov2),
             ('Gumshoos', sprite('gumshoos')), ('Weavile', sprite('weavile'))]
    W = Image.new('RGB', (4 * 290 + 140, 300 + 290), BG); d = ImageDraw.Draw(W)
    for i, (t, im) in enumerate(cells):
        x = 10 + i * 290
        d.text((x, 6), t, fill=(40, 40, 40))
        big = im.resize((256, 256), Image.NEAREST)
        W.paste(big, (x, 24), big if big.mode == 'RGBA' else None)
    x = 10 + 4 * 290
    d.text((x, 6), '1x', fill=(40, 40, 40))
    for j, im in enumerate([sil_img(m), sprite('gumshoos'), sprite('weavile')]):
        W.paste(im, (x, 30 + j * 70), im)
    d.text((x, 240), info, fill=(40, 40, 40))
    x = 10
    for f, t in [('foto10_staand_reikend.jpg', 'foto 10 gespiegeld'), ('foto11_driekwart_kop.webp', 'foto 11'),
                 ('foto15_dief_met_zak.png', 'foto 15 gespiegeld')]:
        im = Image.open(os.path.join(REF, f)).convert('RGB')
        if 'foto10' in f or 'foto15' in f:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        im.thumbnail((380, 260))
        d.text((x, 300), t, fill=(40, 40, 40)); W.paste(im, (x, 318)); x += im.width + 20
    W.save(os.path.join(HERE, 'vel_ronde12.png'))
    print(info)
