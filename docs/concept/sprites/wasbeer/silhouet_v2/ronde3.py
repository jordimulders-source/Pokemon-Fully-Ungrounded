"""Wasbeer silhouet v2 ronde 3: alleen zone 1 (verre klauw, x 4-19, y 30-41), drie varianten op ronde2.txt.
Alles buiten zone 1 = ronde2.txt (door Jordi goedgekeurd). Pols van ronde 2 blijft (steel 2 px: y 33 x 10-15, y 34 x 8-15).
Elke variant als expliciete pixellijst (x, y) aan/uit t.o.v. ronde2.txt. Schrijft ronde3_X.txt, ronde3_X_1x.png en vel_ronde3_klauw.png.
Draaien: python3 docs/concept/sprites/wasbeer/silhouet_v2/ronde3.py"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '../../../../..')
ZONE = (4, 30, 19, 41)

# ronde 2: eindstuk x 8-10, y 35-37 (dicht blok).
VAR = {
    # A: punt van ronde 1 terug: tanden (8,37) en (10,37), V van 1 px op (9,37).
    'A': dict(aan=[], uit=[(9, 37)]),
    # B: eindstuk 1 rij langer (y 35-38), tanden 1x2 (x 8 en x 10, y 37-38), inkeping (9,37)-(9,38) 2 diep.
    'B': dict(aan=[(8, 38), (10, 38)], uit=[(9, 37)]),
    # C: eindstuk 4 breed x 4 hoog (x 7-10, y 35-38), bocht schuin (buitenhoek (7,34) blijft leeg),
    #    linkertand (7-8,37)+(7,38), rechtertand (10,37)-(10,38), V-inkeping (9,37), (8,38), (9,38): 2 diep.
    'C': dict(aan=[(7, 35), (7, 36), (7, 37), (7, 38), (10, 38)], uit=[(9, 37)]),
}


def lees(p):
    return np.array([[c != '.' for c in r.rstrip('\n')] for r in open(p) if r.strip() and not r.startswith('#')])


def in_zone(x, y):
    return ZONE[0] <= x <= ZONE[2] and ZONE[1] <= y <= ZONE[3]


def maak():
    R2 = lees(os.path.join(HERE, 'ronde2.txt'))
    uit = {}
    for k, v in VAR.items():
        B = R2.copy()
        for x, y in v['aan']:
            assert not R2[y, x] and in_zone(x, y); B[y, x] = True
        for x, y in v['uit']:
            assert R2[y, x] and in_zone(x, y); B[y, x] = False
        open(os.path.join(HERE, f'ronde3_{k}.txt'), 'w').write('\n'.join(''.join('#' if c else '.' for c in r) for r in B) + '\n')
        im = Image.new('P', (64, 64), 0); im.putpalette([255, 255, 255, 40, 34, 34] + [0] * 762)
        im.putdata([1 if c else 0 for c in B.flatten()]); im.save(os.path.join(HERE, f'ronde3_{k}_1x.png'), transparency=0)
        d = np.argwhere(R2 != B); buiten = [p for p in d if not in_zone(p[1], p[0])]
        print(f'variant {k}: {len(d)} px t.o.v. ronde2 ({len(v["aan"])} aan, {len(v["uit"])} uit), buiten zone 1: {len(buiten)}, totaal {B.sum()} px')
        uit[k] = B
    return uit


def sil(a, k, fg, bg):
    im = Image.new('RGB', (64, 64), bg); p = im.load()
    for y, x in zip(*np.nonzero(a)): p[int(x), int(y)] = fg
    return im.resize((64 * k, 64 * k), Image.NEAREST)


def zone8(a, under):
    x0, y0, x1, y1 = 2, 26, 21, 41; w, h = x1 - x0 + 1, y1 - y0 + 1; K = 8
    u = under.crop((x0 * 4, y0 * 4, (x1 + 1) * 4, (y1 + 1) * 4)).resize((w * K, h * K), Image.NEAREST)
    s = Image.new('RGB', (w * K, h * K), 'white'); d = ImageDraw.Draw(s)
    for y in range(h):
        for x in range(w):
            if a[y0 + y, x0 + x]: d.rectangle((x * K, y * K, x * K + K - 1, y * K + K - 1), fill=(40, 34, 34))
    for t in range(0, w * K + 1, K): d.line((t, 0, t, h * K), fill=(205, 205, 225))
    for t in range(0, h * K + 1, K): d.line((0, t, w * K, t), fill=(205, 205, 225))
    out = Image.new('RGB', (2 * w * K + 6, h * K), 'white'); out.paste(u, (0, 0)); out.paste(s, (w * K + 6, 0))
    return out


def vel(var):
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    under = Image.open(os.path.join(HERE, 'onderlaag_256.png')).convert('RGB')
    rijen = [('ronde 1', lees(os.path.join(HERE, 'ronde1.txt'))), ('ronde 2', lees(os.path.join(HERE, 'ronde2.txt')))] + \
            [(f'ronde 3 {k}', a) for k, a in var.items()]
    RH = 140; W = 1000
    im = Image.new('RGB', (W, 20 + RH * len(rijen) + 170), 'white'); d = ImageDraw.Draw(im)
    d.text((10, 4), 'per rij: 1x licht | 1x donker | 2x licht | 2x donker | klauwzone 8x: onderlaag | silhouet', font=F, fill=(30, 30, 30))
    for i, (naam, a) in enumerate(rijen):
        y = 22 + i * RH
        d.text((10, y), naam, font=F, fill=(30, 30, 30))
        im.paste(sil(a, 1, (40, 34, 34), (255, 255, 255)), (90, y + 10))
        im.paste(sil(a, 1, (225, 220, 210), (40, 44, 52)), (160, y + 10))
        im.paste(sil(a, 2, (40, 34, 34), (255, 255, 255)), (230, y))
        im.paste(sil(a, 2, (225, 220, 210), (40, 44, 52)), (364, y))
        im.paste(zone8(a, under), (500, y))
    y = 22 + len(rijen) * RH
    d.text((10, y), 'referentie 8x (frame 1): sneasel, weavile, sandslash', font=F, fill=(30, 30, 30))
    for j, (n, box) in enumerate((('sneasel', (4, 28, 20, 44)), ('weavile', (16, 28, 32, 44)), ('sandslash', (10, 32, 26, 48)))):
        s = Image.open(os.path.join(ROOT, f'graphics/pokemon/{n}/anim_front.png')).convert('RGB').crop(box).resize((128, 128), Image.NEAREST)
        im.paste(s, (10 + j * 140, y + 20))
    im.save(os.path.join(HERE, 'vel_ronde3_klauw.png'))


if __name__ == '__main__':
    vel(maak())
