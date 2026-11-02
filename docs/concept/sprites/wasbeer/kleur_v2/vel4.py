"""Vel kleur ronde 4: 4x licht/donker (ronde 4 en ronde 3), 1x/2x naast olinguito, Coathief en 6 Gen 3-sprites.
Draaien: python3 docs/concept/sprites/wasbeer/kleur_v2/vel4.py ronde4.png ronde3.png vel_ronde4.png"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from vel3 import gen3  # noqa: E402
LICHT, DONKER = (236, 236, 228), (40, 44, 52)


def op(im, bg, k):
    b = Image.new('RGB', (64, 64), bg); b.paste(im, (0, 0), im); return b.resize((64 * k, 64 * k), Image.NEAREST)


def main(nieuw, oud, uit):
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    a = Image.open(os.path.join(HERE, nieuw)).convert('RGBA'); b = Image.open(os.path.join(HERE, oud)).convert('RGBA')
    W = Image.new('RGB', (12 + 4 * 266, 300 + 250), 'white'); d = ImageDraw.Draw(W)
    d.text((12, 6), f'{nieuw} 4x licht | donker  ||  {oud} 4x licht | donker', font=F, fill=(30, 30, 30))
    for i, im in enumerate((op(a, LICHT, 4), op(a, DONKER, 4), op(b, LICHT, 4), op(b, DONKER, 4))):
        W.paste(im, (12 + i * 266, 26))
    y = 300
    d.text((12, y), '2x en 1x (licht/donker): wasbeer r4, r3, olinguito, Coathief, zangoose, sneasel, linoone, ursaring, furret, sentret', font=F, fill=(30, 30, 30))
    rij = [a, b] + [Image.open(os.path.join(HERE, f'../referenties/{f}')).convert('RGBA').crop((0, 0, 64, 64)) for f in ('fase1_olinguito.png', 'fase2_coathief.png')]
    rij += [gen3(n).convert('RGBA') for n in ('zangoose', 'sneasel', 'linoone', 'ursaring', 'furret', 'sentret')]
    for i, im in enumerate(rij):
        x = 12 + i * 107
        W.paste(op(im, LICHT, 1) if False else Image.new('RGB', (1, 1)), (0, 0)) if False else None
        W.paste(op(im, LICHT, 1).resize((128, 128), Image.NEAREST).crop((0, 0, 104, 128)) if False else op(im, LICHT, 1).resize((96, 96), Image.NEAREST), (x, y + 20))
        W.paste(op(im, LICHT, 1), (x, y + 122)); W.paste(op(im, DONKER, 1), (x, y + 188))
    W.save(os.path.join(HERE, uit))


if __name__ == '__main__':
    main(*sys.argv[1:4])
