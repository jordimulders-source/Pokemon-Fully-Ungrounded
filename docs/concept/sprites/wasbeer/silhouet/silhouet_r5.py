"""Wasbeer silhouet ronde 5 = ronde 4 met een nieuwe kop (Jordi: "het hoofd lijkt nergens op, met die enorme neus";
kop naar zijn illustratie, kop_illustratie.py, verhoudingen gecontroleerd met foto 11/kop11.py).
Ronde 4 (Jordi, 2 nov): "Kijk maar wat je kan doen voor nu met sandslash als skelet, maar echt
de vormen en kenmerken van wat we afgesproken hebben" + "de crab eating raccoon is sws een stuk dunner dan een
normale wasbeer". Skelet = houding van de Gen 3-Sandslash (gehurkt op de achterpoten, voorover, driekwart naar
links, nabije poot laag vooruit, staart rechts); vormen = wasbeer: driekwart kop van foto 6 (kop6.py) met snuit,
dun lijf, lange poten (foto 10), koevoeten (2 klauwen = 1 steel + J-bocht), geringde haakstaart.
Alles in spritecoördinaten (64x64). Draaien: python3 silhouet_r4.py -> ronde5.txt, ronde5_1x.png, vel_ronde5.png"""
import os
import numpy as np
from PIL import Image, ImageDraw
import kop_illustratie as KI
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../../../..'))
SS = 8

# kop: foto 6 (kijkt al driekwart naar links), ±17 px breed
KS, KX, KY = 0.054, 5.0, 3.0
def kp(p): return (KX + (p[0] - 192) * KS, KY + (p[1] - 15) * KS)
SNOUT = [(690, 500, 62), (630, 540, 54), (575, 575, 44), (525, 600, 34)]   # wig naar de neus (coatilijn: snuit)

# buizen: (x, y, straal) in spritepixels
TORSO = [(24, 25, 5.0), (27, 31, 4.9), (30, 37, 4.8), (33, 42, 5.4)]   # rechter onder de borst (Sandslash-buik)          # dun, schuin voorover (Sandslash-as)
LEG_NEAR = [(31, 43, 4.6), (24, 49, 3.6), (29, 55, 2.6), (28, 59, 2.3)]
FOOT_NEAR = [(28, 60, 2.4), (22, 60.5, 2.1)]
LEG_FAR = [(37, 42, 4.2), (42, 48, 3.2), (43, 55, 2.4), (43, 58.5, 2.2)]
FOOT_FAR = [(43, 59.5, 2.2), (38, 60, 1.9)]
ARM_NEAR = [(22, 29, 3.2), (18, 37, 2.7), (11, 38, 2.4)]                    # laag vooruit, zoals Sandslash
CROW_NEAR = [(10, 39, 1.5), (6, 40, 1.4), (3, 42, 1.3), (2, 46, 1.2), (4, 48, 1.1)]
ARM_FAR = [(29, 31, 2.8), (28, 39, 2.5), (22, 42, 2.2)]
CROW_FAR = [(21, 43, 1.4), (17, 45, 1.3), (15, 48, 1.2), (17, 50, 1.1)]
TAIL = [(36, 44, 4.0), (44, 46, 3.7), (51, 45, 3.4), (57, 41, 3.0), (60, 35, 2.7), (58, 30, 2.4), (54, 30, 2.1), (53, 34, 1.9)]
NECK = [(23, 23, 4.4), (19, 17, 4.2)]


def tube(d, pts):
    for (x0, y0, r0), (x1, y1, r1) in zip(pts, pts[1:]):
        for i in range(13):
            t = i / 12
            x, y, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            d.ellipse([(x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS], fill=255)


def build():
    im = Image.new('L', (64 * SS, 64 * SS), 0)
    d = ImageDraw.Draw(im)
    for t in (TAIL, LEG_FAR, FOOT_FAR, ARM_FAR, CROW_FAR, TORSO, NECK, LEG_NEAR, FOOT_NEAR, ARM_NEAR, CROW_NEAR):
        tube(d, t)
    for poly in (KI.HEADI, KI.EARI_FAR, KI.EARI_NEAR):
        d.polygon([(kp(p)[0] * SS, kp(p)[1] * SS) for p in poly], fill=255)
    return np.array(im.resize((64, 64), Image.BOX)) >= 128


def sprite(name):
    r = Image.open(os.path.join(ROOT, 'graphics/pokemon', name, 'anim_front.png')).convert('RGBA').crop((0, 0, 64, 64))
    a = np.array(r); bg = a[0, 0, :3].copy(); m = ~(a[..., :3] == bg).all(-1); a[~m, 3] = 0
    return Image.fromarray(a), m


if __name__ == '__main__':
    a = build()
    open(os.path.join(HERE, 'ronde5.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in row) for row in a) + '\n')
    blk = Image.new('RGBA', (64, 64), (34, 30, 30, 255)); blk.putalpha(Image.fromarray((a * 255).astype(np.uint8)))
    blk.save(os.path.join(HERE, 'ronde5_1x.png'))
    sand, sm = sprite('sandslash')
    S = 4
    ov = np.full((64, 64, 4), (236, 234, 228, 255), np.uint8)
    ov[sm] = (240, 200, 60, 255); ov[a] = (34, 30, 30, 200); ov[a & sm] = (120, 60, 140, 255)
    ovi = Image.fromarray(ov).resize((64 * S, 64 * S), Image.NEAREST)
    f10 = Image.open(os.path.join(HERE, '../referenties/foto10_staand_reikend.jpg')).convert('RGB').transpose(Image.FLIP_LEFT_RIGHT).resize((256, 192))
    W = 20 + (64 * S + 20) * 3 + 256 + 20 + 90
    sheet = Image.new('RGB', (W, 64 * S + 60), (236, 234, 228))
    d = ImageDraw.Draw(sheet)
    x = 20
    for lab, img in (('skelet: Sandslash (Gen 3)', sand.resize((64 * S, 64 * S), Image.NEAREST)),
                     ('silhouet ronde 5 (4x)', blk.resize((64 * S, 64 * S), Image.NEAREST)),
                     ('over Sandslash (geel = alleen Sandslash)', ovi), ('foto 10 (verhoudingen)', f10)):
        sheet.paste(img, (x, 40), img if img.mode == 'RGBA' else None); d.text((x, 20), lab, fill=(30, 30, 30)); x += img.width + 20
    sheet.paste(blk, (x, 40), blk); d.text((x, 110), f'1x ({int(a.sum())} px)', fill=(30, 30, 30))
    sheet.save(os.path.join(HERE, 'vel_ronde5.png'))
    print(int(a.sum()))
