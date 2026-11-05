"""Wasbeer ronde 14 (armzone + borstvoorkant opnieuw): vergelijkingsvel + diffbewijs.
Draaien: python3 docs/concept/sprites/wasbeer/silhouet/vel_r14.py -> vel_ronde14.png, ronde14_1x.png"""
import os
import numpy as np
from PIL import Image, ImageDraw
from onderlaag_r12 import onderlaag
from vel_r12 import load_txt, sprite, sil_img, BG, REF
HERE = os.path.dirname(os.path.abspath(__file__))
ZONE = (0, 22, 18, 44)   # armzone + 3 kolommen borstvoorkant, x0, y0, x1, y1 (exclusief)

if __name__ == '__main__':
    m12 = load_txt(os.path.join(HERE, 'ronde12.txt')); m = load_txt(os.path.join(HERE, 'ronde14.txt'))
    x0, y0, x1, y1 = ZONE
    zone = np.zeros((64, 64), bool); zone[y0:y1, x0:x1] = True
    diff = m12 != m
    print('diff binnen armzone', (diff & zone).sum(), 'buiten armzone', (diff & ~zone).sum())
    Image.fromarray(np.where(m, 0, 255).astype(np.uint8)).convert('1').save(os.path.join(HERE, 'ronde14_1x.png'))
    ys, xs = np.nonzero(m)
    info = '%d px, bbox %dx%d' % (m.sum(), xs.max() - xs.min() + 1, ys.max() - ys.min() + 1)
    under, kop = onderlaag()
    ov2 = np.full((64, 64, 3), 255, np.uint8); ov2[under] = (235, 160, 235); ov2[kop] = (140, 210, 235)
    edge = m & ~(np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1))
    ov2[edge] = (20, 20, 20); ov2 = Image.fromarray(ov2)
    cmp = np.full((64, 64, 3), 255, np.uint8); cmp[m12 & m] = (60, 60, 60); cmp[m12 & ~m] = (230, 120, 120); cmp[m & ~m12] = (60, 160, 230)
    cmp = Image.fromarray(cmp)
    cells = [('silhouet ronde 14 (4x)', sil_img(m)), ('omtrek over onderlaag (foto 10/kop r11)', ov2),
             ('r12 vs r14 (rood=weg, blauw=nieuw)', cmp), ('Gumshoos', sprite('gumshoos')), ('Weavile', sprite('weavile')),
             ('Sneasel', sprite('sneasel'))]
    W = Image.new("RGB", (6 * 270 + 120 + 900, 680), BG); d = ImageDraw.Draw(W)
    for i, (t, im) in enumerate(cells):
        x = 10 + i * 270
        d.text((x, 6), t, fill=(40, 40, 40))
        big = im.resize((256, 256), Image.NEAREST)
        W.paste(big, (x, 24), big if big.mode == 'RGBA' else None)
    x = 10 + 6 * 270
    d.text((x, 6), '1x', fill=(40, 40, 40))
    for j, im in enumerate([sil_img(m12), sil_img(m), sprite('gumshoos'), sprite('sneasel')]):
        W.paste(im, (x, 24 + j * 66), im)
    d.text((10, 284), info + '   (1x: r12, r14, Gumshoos, Sneasel)', fill=(40, 40, 40))
    # zoom 8x op kop + armen
    zm = sil_img(m).crop((0, 2, 32, 46)).resize((256, 352), Image.NEAREST)
    d.text((10, 300), 'zoom 8x kop+armen', fill=(40, 40, 40)); W.paste(zm, (10, 316), zm)
    x = 290
    for f, t in [('foto10_staand_reikend.jpg', 'foto 10 gespiegeld'), ('foto11_driekwart_kop.webp', 'foto 11'),
                 ('foto15_dief_met_zak.png', 'foto 15 gespiegeld')]:
        im = Image.open(os.path.join(REF, f)).convert('RGB')
        if 'foto10' in f or 'foto15' in f:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        im.thumbnail((440, 270))
        d.text((x, 300), t, fill=(40, 40, 40)); W.paste(im, (x, 316)); x += im.width + 16

    # 8x: alleen de armen naast Sneasels gestrekte arm en Gumshoos' hangende arm
    y0b = 400
    d.text((1300, 300), '8x armen r14 | Sneasel-arm | Gumshoos-arm', fill=(40, 40, 40))
    xx = 1300
    for im, box in [(sil_img(m), (0, 21, 19, 44)), (sprite('sneasel'), (6, 30, 26, 45)), (sprite('gumshoos'), (8, 38, 26, 52))]:
        c = im.crop(box); c = c.resize((c.width * 8, c.height * 8), Image.NEAREST)
        if xx + c.width > W.width:
            break
        W.paste(c, (xx, 316), c); xx += c.width + 10
    W.save(os.path.join(HERE, 'vel_ronde14.png'))
    print(info)
