#!/usr/bin/env python3
"""Project Grounded: overworld-sprites voor het strandresort (ZEE_PLAN.md).

- Cynthia: uit `cynthia.png` (root van de repo, RMXP-sheet 4x4, op 2x getekend: cellen 32x48 = 16x24 op 1x).
  Halveren geeft precies het originele pixelraster terug; elke cel gaat met de voeten op rij 31 in een 16x32-frame
  (Gen 3-volgorde, 9 frames; rechts = gespiegeld links). Eigen palet (de 12 kleuren van de sheet).
- Drol (OBJ_EVENT_GFX_TURD): 16x16, met de hand getekend (ASCII hieronder), eigen palet. Voor Birch op het strand.

Gebruik: python3 tools/grounded/resort_sprites.py [voorbeeldmap]
"""
import os, sys
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
BG = (115, 197, 164)


def gba(c):
    return tuple((v >> 3) << 3 for v in c[:3])


def write_pal(path, cols):
    cols = [BG] + list(cols)
    cols += [(0, 0, 0)] * (16 - len(cols))
    with open(path, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for c in cols:
            f.write('%d %d %d\n' % c)


def save_png(path, img, cols):
    flat = list(BG)
    for c in cols:
        flat += c
    flat += [0] * (768 - len(flat))
    img.putpalette(flat)
    img.save(path)


# ---------------------------------------------------------------------------------------------------------- Cynthia
def cynthia():
    src = Image.open(os.path.join(ROOT, 'cynthia.png'))
    assert src.size == (128, 192) and src.mode == 'P'
    half = src.resize((64, 96), Image.NEAREST)                       # 2x -> 1x (pixelparen zijn exact gelijk)
    spal = src.getpalette()
    used = sorted({i for i in half.get_flattened_data()} - {0})
    remap = {old: new + 1 for new, old in enumerate(used)}
    cols = [gba(spal[i * 3:i * 3 + 3]) for i in used]
    assert len(cols) <= 15
    cells = {}
    for r, d in enumerate(('down', 'left', 'right', 'up')):
        for c in range(4):
            cell = half.crop((c * 16, r * 24, c * 16 + 16, r * 24 + 24))
            ys = [y for y in range(24) for x in range(16) if cell.getpixel((x, y))]
            out = Image.new('P', (16, 32), 0)
            dy = 31 - max(ys)
            for y in range(24):
                for x in range(16):
                    v = cell.getpixel((x, y))
                    if v and 0 <= y + dy < 32:
                        out.putpixel((x, y + dy), remap[v])
            cells[(d, c)] = out
    order = [('down', 0), ('up', 0), ('left', 0), ('down', 1), ('down', 3), ('up', 1), ('up', 3), ('left', 1), ('left', 3)]
    sheet = Image.new('P', (16 * len(order), 32), 0)
    for i, k in enumerate(order):
        sheet.paste(cells[k], (16 * i, 0))
    save_png(os.path.join(ROOT, 'graphics/object_events/pics/people/cynthia.png'), sheet, cols)
    write_pal(os.path.join(ROOT, 'graphics/object_events/palettes/cynthia.pal'), cols)
    return sheet


# ---------------------------------------------------------------------------------------------------------- drol
TURD_COLS = [(48, 24, 8), (96, 56, 24), (136, 88, 40), (184, 128, 64), (224, 176, 112)]
TURD = """
................
................
................
.......11.......
......1541......
.....143321.....
....11111111....
...1443333221...
...1433333321...
..111111111111..
.14543333333221.
.14333333332221.
.13333333322221.
..111111111111..
................
................
"""


def turd():
    rows = [r for r in TURD.strip('\n').split('\n')]
    assert len(rows) == 16 and all(len(r) == 16 for r in rows)
    img = Image.new('P', (16, 16), 0)
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != '.':
                img.putpixel((x, y), int(ch))
    save_png(os.path.join(ROOT, 'graphics/object_events/pics/misc/turd.png'), img, TURD_COLS)
    write_pal(os.path.join(ROOT, 'graphics/object_events/palettes/turd.pal'), TURD_COLS)
    return img


def main():
    out = {'cynthia': cynthia(), 'turd': turd()}
    if len(sys.argv) > 1:
        for k, im in out.items():
            im = im.convert('RGB')
            im.resize((im.width * 6, im.height * 6), Image.NEAREST).save(os.path.join(sys.argv[1], k + '_6x.png'))
    print('resort-sprites geschreven')


if __name__ == '__main__':
    main()
