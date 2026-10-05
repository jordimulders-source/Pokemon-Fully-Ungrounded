#!/usr/bin/env python3
"""Project Grounded: Team Rocket (Safari-sidequest, hideout in Fortree Jungle).

Bronnen (graphics/grounded/trainers/rocket/):
- rocket_grunt_m/f_frlg_bron.png + .pal: pret/pokefirered graphics/trainers/front_pics/rocket_grunt_*_front_pic.png en
  graphics/trainers/palettes/rocket_grunt_*.pal (al 64x64, 16 kleuren) -> trainerfoto's met het FRLG-palet.
- rocket_m/f_ow_frlg_bron.png: pret/pokefirered graphics/object_events/pics/people/rocket_*.png (9 frames 16x32,
  palet npc_white) -> overworlds met een eigen palet (OBJ_EVENT_PAL_TAG_ROCKET).
- petrel_hgss_bron.png: Petrel uit de HG/SS-sheet van Dann-The-Yoshi (graphics/d2dp76j-...png, cel x 800, y 720,
  80x80, 15 kleuren). Trainerfoto = bovenste 64 rijen van de figuur, gespiegeld (kijkt naar links), onderkant
  geditherd weg (zoals de DS-foto's in het Stadium).
- Petrel-overworld: de FRLG-grunt met de pet in Petrels paars (zijn haar), eigen palet (OBJ_EVENT_PAL_TAG_PETREL).
Gebruik: python3 tools/grounded/rocket_sprites.py [voorbeeld.png]"""
import os, sys
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SRC = os.path.join(ROOT, 'graphics/grounded/trainers/rocket/')
FRONT = os.path.join(ROOT, 'graphics/trainers/front_pics/')
OW = os.path.join(ROOT, 'graphics/object_events/pics/people/')
OWPAL = os.path.join(ROOT, 'graphics/object_events/palettes/')
SHEET = os.path.join(ROOT, 'graphics/d2dp76j-69085d1e-fccf-4833-baaa-745f7b3a1827.png')
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def read_pal(path):
    return [tuple(int(v) for v in l.split()) for l in open(path).read().split('\n')[3:19] if l.strip()]


def write_pal(path, cols):
    with open(path, 'w', newline='\r\n') as fh:
        fh.write('JASC-PAL\n0100\n16\n')
        for c in cols:
            fh.write('%d %d %d\n' % tuple((v >> 3) << 3 for v in c))


def flat(cols):
    out = [v for c in cols for v in c]
    return out + [0] * (768 - len(out))


def fade_bottom(out, rows=8):
    for i in range(rows):
        y = 63 - i
        t = (rows - i) / (rows + 1)
        for x in range(64):
            if out.getpixel((x, y)) and BAYER[y % 4][x % 4] < t * 16:
                out.putpixel((x, y), 0)


def grunt_pics():
    for g in 'mf':
        im = Image.open(SRC + 'rocket_grunt_%s_frlg_bron.png' % g).copy()
        im.putpalette(flat(read_pal(SRC + 'rocket_grunt_%s_frlg_bron.pal' % g)))
        im.save(FRONT + 'rocket_grunt_%s.png' % g)


def petrel_pic():
    src = SRC + 'petrel_hgss_bron.png'
    if not os.path.exists(src):
        Image.open(SHEET).convert('RGBA').crop((800, 720, 880, 800)).save(src)
    cell = Image.open(src).convert('RGBA')
    x0, y0, x1, y1 = cell.getbbox()
    cols = []
    for y in range(cell.height):
        for x in range(cell.width):
            p = cell.getpixel((x, y))
            if p[3] >= 128 and p[:3] not in cols:
                cols.append(p[:3])
    assert len(cols) <= 15, len(cols)
    cols.sort(key=lambda c: -(c[0] * 3 + c[1] * 6 + c[2]))
    out = Image.new('P', (64, 64), 0)
    w = x1 - x0
    px = (64 - w) // 2
    for y in range(64):
        for x in range(w):
            p = cell.getpixel((x0 + x, y0 + y)) if y0 + y < cell.height else (0, 0, 0, 0)
            if p[3] >= 128:
                out.putpixel((63 - (px + x), y), cols.index(p[:3]) + 1)     # gespiegeld: kijkt naar links
    fade_bottom(out)
    out.putpalette(flat([(115, 197, 164)] + cols + [(0, 0, 0)] * (15 - len(cols))))
    out.save(FRONT + 'petrel.png')


# Petrel: zijn paarse kuif in de vorm van de grunt-pet (rijen 0-18), de rest blijft het zwarte uniform
PETREL_HAIR = [(200, 136, 232), (144, 88, 192), (80, 40, 120)]


def overworlds():
    pal = list(Image.open(SRC + 'rocket_m_ow_frlg_bron.png').getpalette()[:48])
    pal = [tuple(pal[i:i + 3]) for i in range(0, 48, 3)]
    for g in 'mf':
        im = Image.open(SRC + 'rocket_%s_ow_frlg_bron.png' % g).copy()
        im.putpalette(flat(pal))
        im.save(OW + 'rocket_%s.png' % g)
    write_pal(OWPAL + 'rocket.pal', pal)
    im = Image.open(SRC + 'rocket_m_ow_frlg_bron.png').copy()
    px = im.load()
    for f in range(9):
        for y in range(19):
            for x in range(16):
                p = px[f * 16 + x, y]
                px[f * 16 + x, y] = {11: 5, 12: 6, 13: 7}.get(p, p)
    ppal = pal[:5] + PETREL_HAIR + pal[8:]
    im.putpalette(flat(ppal))
    im.save(OW + 'petrel.png')
    write_pal(OWPAL + 'petrel.pal', ppal)


def main():
    grunt_pics()
    petrel_pic()
    overworlds()
    if len(sys.argv) > 1:
        W = Image.new('RGB', (64 * 3 + 144 + 16, 96), (255, 255, 255))
        for i, n in enumerate(('rocket_grunt_m', 'rocket_grunt_f', 'petrel')):
            W.paste(Image.open(FRONT + n + '.png').convert('RGB'), (i * 64, 0))
        for i, n in enumerate(('rocket_m', 'rocket_f', 'petrel')):
            W.paste(Image.open(OW + n + '.png').convert('RGB'), (64 * 3 + 8, i * 32))
        W.resize((W.width * 4, W.height * 4), Image.NEAREST).save(sys.argv[1])
    print('klaar')


if __name__ == '__main__':
    main()
