"""Vel kleur ronde 3+: per onderdeel 8x-uitsneden van echte Gen 3-sprites naast de wasbeer, plus de hele sprite 1x/2x
naast 6 echte sprites. Draaien: python3 docs/concept/sprites/wasbeer/kleur_v2/vel3.py ronde3.png vel_ronde3.png"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '../../../../..')
BG = (236, 236, 228)
K = 8
RIJEN = [  # onderdeel, [(sprite, box 16x16)], wasbeer-box
    ('klauw', [('sneasel', (4, 28)), ('zangoose', (2, 38)), ('sandslash', (10, 32))], [(18, 22), (4, 31)]),
    ('onderarm', [('zangoose', (6, 28)), ('ursaring', (0, 10))], [(20, 18)]),
    ('staartringen', [('linoone', (46, 22)), ('sentret', (16, 46)), ('furret', (6, 44)), ('zigzagoon', (40, 20))], [(42, 16), (40, 30)]),
    ('volume', [('zangoose', (16, 20)), ('ursaring', (14, 22)), ('teddiursa', (32, 12))], [(12, 14), (24, 34)]),
    ('oog op masker', [('zigzagoon', (6, 28)), ('linoone', (4, 26))], [(8, 4)]),
    ('buidel', [], [(30, 13)]),
]


def gen3(n):
    im = Image.open(os.path.join(ROOT, f'graphics/pokemon/{n}/anim_front.png'))
    pal = [tuple(int(v) for v in l.split()) for l in open(os.path.join(ROOT, f'graphics/pokemon/{n}/normal.pal')).read().split('\n')[3:19]]
    im.putpalette(sum(pal, ())); im.info['transparency'] = 0
    return op(im.convert('RGBA').crop((0, 0, 64, 64)))


def op(im):
    b = Image.new('RGB', im.size, BG); b.paste(im, (0, 0), im); return b


def uit(im, xy):
    x, y = xy
    return im.crop((x, y, x + 16, y + 16)).resize((16 * K, 16 * K), Image.NEAREST)


def main(src, out):
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
    sp = op(Image.open(os.path.join(HERE, src)).convert('RGBA'))
    T = 16 * K
    W = Image.new('RGB', (12 + 6 * (T + 8), 20 + len(RIJEN) * (T + 22) + 190), 'white'); d = ImageDraw.Draw(W)
    y = 6
    for naam, refs, eigen in RIJEN:
        d.text((12, y), f'{naam}: wasbeer ({src}) | ' + ', '.join(n for n, _ in refs), font=F, fill=(30, 30, 30)); y += 16
        x = 12
        for xy in eigen:
            W.paste(uit(sp, xy), (x, y)); d.rectangle((x, y, x + T - 1, y + T - 1), outline=(200, 0, 0)); x += T + 8
        for n, xy in refs:
            W.paste(uit(gen3(n), xy), (x, y)); x += T + 8
        y += T + 6
    d.text((12, y), 'hele sprite 2x en 1x naast 6 echte sprites', font=F, fill=(30, 30, 30)); y += 16
    for i, (n, im) in enumerate([('wasbeer', sp)] + [(n, gen3(n)) for n in ('zangoose', 'sneasel', 'linoone', 'ursaring', 'furret', 'sandslash')]):
        x = 12 + i * 136
        W.paste(im.resize((128, 128), Image.NEAREST), (x, y)); W.paste(im, (x + 64, y + 130 - 64 + 64)) if False else W.paste(im, (x, y + 132))
    W.save(os.path.join(HERE, out))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
