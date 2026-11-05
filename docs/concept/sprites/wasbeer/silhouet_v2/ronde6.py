"""Wasbeer silhouet v2 ronde 6: alleen zone 1 (verre klauw, x 4-19, y 30-41) op ronde2.txt, naar Jordi's schets over de Sneasel-klauw:
Sneasel-klauw als vorm, het stuk binnen zijn rode boog (links onder in de klauw) weggehaald zodat de klauw een haak wordt, klauwen 1-2 px groter.
Pols en steel van ronde 2 blijven (y 33 x 10-15, y 34 x 8-15). Kop x 7-12, y 35-37 (massief, klauwen tegen elkaar), rechterkant x 10-12 omlaag,
holte (7-9,38), (7-8,39), (7,40) open naar links; punt = gladde schuine band van 3 px (x 10-12/9-11/8-10, y 38-40) naar (7-8,41) linksonder. Geen spleet, niet terug naar rechts.
Draaien: python3 docs/concept/sprites/wasbeer/silhouet_v2/ronde6.py"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '../../../../..')
ZONE = (4, 30, 19, 41)
AAN = [(7, 35), (11, 35), (12, 35), (7, 36), (11, 36), (12, 36), (7, 37), (11, 37), (12, 37),
       (10, 38), (11, 38), (12, 38), (9, 39), (10, 39), (11, 39), (8, 40), (9, 40), (10, 40),
       (7, 41), (8, 41)]
UIT = []
SNEASEL_WEG = [(7, 38), (8, 38), (9, 38), (8, 39), (9, 39), (8, 40)]  # stuk binnen Jordi's boog (sneasel-coordinaten)


def lees(p):
    return np.array([[c != '.' for c in r.rstrip('\n')] for r in open(p) if r.strip() and not r.startswith('#')])


def raster8(rgb, box, K=8):
    x0, y0, x1, y1 = box; w, h = x1 - x0 + 1, y1 - y0 + 1
    im = rgb.crop((x0, y0, x1 + 1, y1 + 1)).resize((w * K, h * K), Image.NEAREST); d = ImageDraw.Draw(im)
    for t in range(0, w * K + 1, K): d.line((t, 0, t, h * K), fill=(190, 190, 215))
    for t in range(0, h * K + 1, K): d.line((0, t, w * K, t), fill=(190, 190, 215))
    return im


def sil(a, fg, bg):
    im = Image.new('RGB', (64, 64), bg); p = im.load()
    for y, x in zip(*np.nonzero(a)): p[int(x), int(y)] = fg
    return im


def main():
    R2 = lees(os.path.join(HERE, 'ronde2.txt')); B = R2.copy()
    for x, y in AAN:
        assert not R2[y, x]; B[y, x] = True
    for x, y in UIT:
        assert R2[y, x]; B[y, x] = False
    open(os.path.join(HERE, 'ronde6.txt'), 'w').write('\n'.join(''.join('#' if c else '.' for c in r) for r in B) + '\n')
    im = Image.new('P', (64, 64), 0); im.putpalette([255, 255, 255, 40, 34, 34] + [0] * 762)
    im.putdata([1 if c else 0 for c in B.flatten()]); im.save(os.path.join(HERE, 'ronde6_1x.png'), transparency=0)
    d = np.argwhere(R2 != B)
    buiten = [p for p in d if not (ZONE[0] <= p[1] <= ZONE[2] and ZONE[1] <= p[0] <= ZONE[3])]
    print(f'zone 1: {len(d)} px t.o.v. ronde2 ({len(AAN)} aan, {len(UIT)} uit), buiten zone 1: {len(buiten)}, totaal {B.sum()} px')
    # vel
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    sn = Image.open(os.path.join(ROOT, 'graphics/pokemon/sneasel/anim_front.png')).convert('RGB').crop((0, 0, 64, 64))
    t1 = raster8(sn, (4, 30, 21, 43)); dd = ImageDraw.Draw(t1)
    for x, y in SNEASEL_WEG:
        dd.rectangle(((x - 4) * 8, (y - 30) * 8, (x - 4) * 8 + 7, (y - 30) * 8 + 7), outline=(230, 0, 0), width=2)
    t2 = raster8(sil(B, (40, 34, 34), (255, 255, 255)), (4, 30, 21, 43))
    licht, donker = sil(B, (40, 34, 34), (255, 255, 255)), sil(B, (225, 220, 210), (40, 44, 52))
    V = Image.new('RGB', (10 + 2 * (t1.width + 12) + 3 * 140 + 80, max(20 + t1.height + 20, 170)), 'white'); dr = ImageDraw.Draw(V)
    dr.text((10, 2), 'sneasel klauw 8x (rood = weggehaald) | onze klauw 8x | 1x licht/donker | 2x licht | 2x donker', font=F, fill=(30, 30, 30))
    V.paste(t1, (10, 22)); V.paste(t2, (22 + t1.width, 22)); x = 34 + 2 * t1.width
    V.paste(licht, (x, 22)); V.paste(donker, (x, 96)); x += 76
    V.paste(licht.resize((128, 128), Image.NEAREST), (x, 22)); x += 140
    V.paste(donker.resize((128, 128), Image.NEAREST), (x, 22))
    V.save(os.path.join(HERE, 'vel_ronde6_klauw.png'))


if __name__ == '__main__':
    main()
