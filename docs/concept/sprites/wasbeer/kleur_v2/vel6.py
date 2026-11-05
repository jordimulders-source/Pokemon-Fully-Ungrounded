"""Vel kleur ronde 6 (kop): kop op 8x van ronde 6 en ronde 5 naast de koppen van Zigzagoon, Linoone, Teddiursa, Zangoose;
hele sprite 4x licht/donker en 2x/1x naast olinguito en Coathief.
Draaien: python3 docs/concept/sprites/wasbeer/kleur_v2/vel6.py"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from vel3 import gen3  # noqa: E402
LICHT, DONKER = (236, 236, 228), (40, 44, 52)
K = 7


def op(im, bg, k):
    b = Image.new('RGB', (64, 64), bg); b.paste(im, (0, 0), im); return b.resize((64 * k, 64 * k), Image.NEAREST)


def kop(im, box):
    x, y = box
    return op(im, LICHT, 1).crop((x, y, x + 25, y + 25)).resize((25 * K, 25 * K), Image.NEAREST)


def main():
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    r6 = Image.open(os.path.join(HERE, 'ronde6.png')).convert('RGBA'); r5 = Image.open(os.path.join(HERE, 'ronde5.png')).convert('RGBA')
    T = 25 * K
    koppen = [('ronde 6', r6, (8, 0)), ('ronde 5', r5, (8, 0)), ('zigzagoon', gen3('zigzagoon').convert('RGBA'), (4, 24)),
              ('linoone', gen3('linoone').convert('RGBA'), (2, 22)), ('teddiursa', gen3('teddiursa').convert('RGBA'), (22, 8)),
              ('zangoose', gen3('zangoose').convert('RGBA'), (12, 4))]
    W = Image.new('RGB', (12 + 6 * (T + 8), 30 + T + 300 + 160), 'white'); d = ImageDraw.Draw(W)
    d.text((12, 6), 'kop 7x: ronde 6 | ronde 5 | zigzagoon | linoone | teddiursa | zangoose', font=F, fill=(30, 30, 30))
    for i, (n, im, box) in enumerate(koppen):
        W.paste(kop(im, box), (12 + i * (T + 8), 26))
    y = 26 + T + 14
    d.text((12, y), 'ronde 6 4x licht | donker', font=F, fill=(30, 30, 30))
    W.paste(op(r6, LICHT, 4), (12, y + 18)); W.paste(op(r6, DONKER, 4), (12 + 266, y + 18))
    y += 18 + 266
    d.text((12, y), '2x en 1x: ronde 6, ronde 5, olinguito, Coathief', font=F, fill=(30, 30, 30))
    rij = [r6, r5] + [Image.open(os.path.join(HERE, f'../referenties/{f}')).convert('RGBA').crop((0, 0, 64, 64)) for f in ('fase1_olinguito.png', 'fase2_coathief.png')]
    for i, im in enumerate(rij):
        x = 12 + i * 140
        W.paste(op(im, LICHT, 2), (x, y + 18)); W.paste(op(im, LICHT, 1), (x + 132 - 64 if False else x, y + 18 + 132)) if False else None
        W.paste(op(im, LICHT, 2), (x, y + 18))
    for i, im in enumerate(rij):
        W.paste(op(im, LICHT, 1), (12 + 560 + i * 70, y + 18)); W.paste(op(im, DONKER, 1), (12 + 560 + i * 70, y + 88))
    W.save(os.path.join(HERE, 'vel_ronde6.png'))


if __name__ == '__main__':
    main()
