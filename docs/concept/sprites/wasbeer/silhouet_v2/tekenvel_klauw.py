"""Tekenvel klauwzone (Coathief-methode): de arm van ronde 2 zonder klauw op een genummerd raster, zodat Jordi de klauw
zelf in de cellen kan aftekenen. Naast: Sneasel-klauw en ronde 4 op hetzelfde raster, en de koevoetfoto.
Draaien: python3 docs/concept/sprites/wasbeer/silhouet_v2/tekenvel_klauw.py"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '../../../../..')
X0, X1, Y0, Y1, K = 2, 22, 26, 44, 34


def lees(p):
    return np.array([[c != '.' for c in r.rstrip('\n')] for r in open(os.path.join(HERE, p)) if r.strip() and not r.startswith('#')])


def raster(a, titel, kleur=(40, 34, 34), wis_klauw=False):
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
    w, h = (X1 - X0) * K + 40, (Y1 - Y0) * K + 60
    im = Image.new('RGB', (w, h), 'white'); d = ImageDraw.Draw(im)
    d.text((40, 4), titel, font=F, fill=(20, 20, 20))
    for y in range(Y0, Y1):
        for x in range(X0, X1):
            px, py = 40 + (x - X0) * K, 40 + (y - Y0) * K
            vol = a[y, x] if not callable(kleur) else False
            if wis_klauw and x <= 15 and y >= 33:
                vol = False
            if callable(kleur):
                c = kleur(x, y)
                if c:
                    d.rectangle((px, py, px + K, py + K), fill=c)
            elif vol:
                d.rectangle((px, py, px + K, py + K), fill=kleur)
            d.rectangle((px, py, px + K, py + K), outline=(190, 190, 205))
    for x in range(X0, X1):
        d.text((40 + (x - X0) * K + 9, 24), str(x), font=F, fill=(90, 90, 90))
    for y in range(Y0, Y1):
        d.text((6, 40 + (y - Y0) * K + 10), str(y), font=F, fill=(90, 90, 90))
    return im


r2 = lees('ronde2.txt'); r4 = lees('ronde4.txt')
leeg = raster(r2, 'TEKENVEL: arm zonder klauw (x <= 15, y >= 33 leeg). Teken de klauw in de cellen.', wis_klauw=True)
vier = raster(r4, 'ronde 4 (ter vergelijking)')
sn = Image.open(os.path.join(ROOT, 'graphics/pokemon/sneasel/anim_front.png')).convert('RGB').crop((0, 0, 64, 64))
sn = sn.crop((2, 26, 22, 44)).resize((20 * K, 18 * K), Image.NEAREST)
foto = Image.open(os.path.join(HERE, '../referenties/foto16_koevoet.webp')).convert('RGB').transpose(Image.FLIP_LEFT_RIGHT)
foto.thumbnail((400, 300))
W = leeg.width + vier.width + 30
out = Image.new('RGB', (W, leeg.height + max(sn.height, foto.height) + 40), 'white')
out.paste(leeg, (0, 0)); out.paste(vier, (leeg.width + 30, 0))
d = ImageDraw.Draw(out); F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
y = leeg.height + 10
d.text((40, y), 'Sneasel (x 2-21, y 26-43, zelfde schaal)', font=F, fill=(20, 20, 20)); out.paste(sn, (40, y + 18))
d.text((leeg.width + 70, y), 'koevoet (foto 16, gespiegeld)', font=F, fill=(20, 20, 20)); out.paste(foto, (leeg.width + 70, y + 18))
out.save(os.path.join(HERE, 'tekenvel_klauw.png'))
