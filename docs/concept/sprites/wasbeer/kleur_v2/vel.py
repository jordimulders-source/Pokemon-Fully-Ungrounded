"""Vel kleur: sprite 1x en 4x op licht en donker | render (onderlaag) | fase 1 en 2 | 3 Gen 3-referenties (1x en 2x).
Draaien: python3 docs/concept/sprites/wasbeer/kleur_v2/vel.py ronde1.png vel_ronde1.png"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '../../../../..')
LICHT, DONKER = (236, 236, 228), (40, 44, 52)


def rgba(p):
    return Image.open(p).convert('RGBA').crop((0, 0, 64, 64))


def gen3(n):
    im = Image.open(os.path.join(ROOT, f'graphics/pokemon/{n}/anim_front.png'))
    pal = [tuple(int(v) for v in l.split()) for l in open(os.path.join(ROOT, f'graphics/pokemon/{n}/normal.pal')).read().split('\n')[3:19]]
    im.putpalette(sum(pal, ())); im.info['transparency'] = 0
    return im.convert('RGBA').crop((0, 0, 64, 64))


def op(im, bg, k):
    b = Image.new('RGB', (64, 64), bg); b.paste(im, (0, 0), im)
    return b.resize((64 * k, 64 * k), Image.NEAREST)


def main(src, uit):
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    sp = rgba(os.path.join(HERE, src))
    W = Image.new('RGB', (12 + 256 * 3 + 40 + 140, 300 + 170 + 170), 'white'); d = ImageDraw.Draw(W)
    d.text((12, 6), f'{src}: 4x licht | 4x donker | render (onderlaag S1a) | 1x licht/donker', font=F, fill=(30, 30, 30))
    W.paste(op(sp, LICHT, 4), (12, 26)); W.paste(op(sp, DONKER, 4), (12 + 266, 26))
    W.paste(Image.open(os.path.join(HERE, '../silhouet_v2/onderlaag_s1a_256.png')).convert('RGB'), (12 + 532, 26))
    W.paste(op(sp, LICHT, 1), (12 + 798, 26)); W.paste(op(sp, DONKER, 1), (12 + 798, 100))
    W.paste(op(sp, LICHT, 2), (12 + 798, 174)) if False else None
    y = 300
    d.text((12, y), '1x en 2x naast de lijn (fase 1 olinguito, fase 2 Coathief) en Gen 3 (zangoose, sneasel, linoone)', font=F, fill=(30, 30, 30))
    rij = [('wasbeer', sp), ('olinguito', rgba(os.path.join(HERE, '../referenties/fase1_olinguito.png'))),
           ('coathief', rgba(os.path.join(HERE, '../referenties/fase2_coathief.png')))] + [(n, gen3(n)) for n in ('zangoose', 'sneasel', 'linoone')]
    for i, (n, im) in enumerate(rij):
        x = 12 + i * 150
        W.paste(op(im, LICHT, 2), (x, y + 20)); W.paste(op(im, LICHT, 1), (x, y + 152)); W.paste(op(im, DONKER, 1), (x + 68, y + 152))
        d.text((x, y + 222), n, font=F, fill=(60, 60, 60))
    W.save(os.path.join(HERE, uit))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
