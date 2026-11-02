"""8x-uitsneden ronde 1: per zone onderlaag | direct.txt | ronde1.txt | ronde1 over de onderlaag.
Draaien: python3 docs/concept/sprites/wasbeer/silhouet_v2/zone_ronde1.py"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
K = 8


def lees(p):
    return np.array([[c != '.' for c in r.rstrip('\n')] for r in open(p) if r.strip() and not r.startswith('#')])


def raster(a, box, under=None):
    x0, y0, x1, y1 = box; w, h = x1 - x0 + 1, y1 - y0 + 1
    im = under.crop((x0 * 4, y0 * 4, (x1 + 1) * 4, (y1 + 1) * 4)).resize((w * K, h * K), Image.NEAREST) if under else Image.new('RGB', (w * K, h * K), 'white')
    d = ImageDraw.Draw(im)
    for y in range(h):
        for x in range(w):
            if a[y0 + y, x0 + x]:
                if under:
                    d.rectangle((x * K + 2, y * K + 2, x * K + K - 3, y * K + K - 3), fill=(210, 30, 30))
                else:
                    d.rectangle((x * K, y * K, x * K + K - 1, y * K + K - 1), fill=(40, 34, 34))
    for t in range(0, w * K + 1, K): d.line((t, 0, t, h * K), fill=(205, 205, 225))
    for t in range(0, h * K + 1, K): d.line((0, t, w * K, t), fill=(205, 205, 225))
    return im


def main():
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
    under = Image.open(os.path.join(HERE, 'onderlaag_256.png')).convert('RGB')
    A, B = lees(os.path.join(HERE, 'direct.txt')), lees(os.path.join(HERE, 'ronde1.txt'))
    zones = [('verre klauw x4-23 y26-41', (4, 26, 23, 41)), ('buidel/staart x33-56 y15-40', (33, 15, 56, 40)),
             ('nabije klauw x18-30 y21-31 (silhouet ongewijzigd)', (18, 21, 30, 31))]
    tiles = []
    for naam, box in zones:
        row = [raster(np.zeros_like(A), box, under), raster(A, box), raster(B, box), raster(B, box, under)]
        tiles.append((naam, row))
    W = 10 + 4 * (24 * K + 10); H = sum(t[1][0].height + 24 for t in tiles) + 10
    im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im); y = 6
    for naam, row in tiles:
        d.text((10, y), f'{naam}:  onderlaag | direct | ronde1 | ronde1 over de onderlaag', font=F, fill=(30, 30, 30)); y += 18
        x = 10
        for t in row:
            im.paste(t, (x, y)); x += t.width + 10
        y += row[0].height + 6
    im.save(os.path.join(HERE, 'zone_ronde1.png'))


if __name__ == '__main__':
    main()
