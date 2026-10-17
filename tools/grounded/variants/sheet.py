#!/usr/bin/env python3
"""Contactvel van kleurvarianten: per soort een rij normaal | shiny | variant 1..6.

Gebruik: python3 tools/grounded/variants/sheet.py uit.png bulbasaur charmander ...
(mapnamen onder graphics/pokemon/, ook submappen zoals 'pikachu/alola_cap')
"""
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from variants import ROOT, read_pal  # noqa: E402

CHANCES = ['75%', 'shiny', '10%', '6%', '4%', '3%', '1,5%', '0,5%']
SCALE = 2
CELL = 64 * SCALE + 8
LABEL_W = 110


def sprite_with(folder, pal):
    pic = os.path.join(folder, 'anim_front.png')
    if not os.path.exists(pic):
        pic = os.path.join(folder, 'front.png')
    im = Image.open(pic)
    im = im.crop((0, 0, 64, 64))
    flat = [v for c in pal for v in c] + [0] * (768 - len(pal) * 3)
    im.putpalette(flat)
    rgba = im.convert('RGBA')
    px = rgba.load()
    idx = im.load()
    for y in range(64):
        for x in range(64):
            if idx[x, y] == 0:
                px[x, y] = (0, 0, 0, 0)
    return rgba.resize((64 * SCALE, 64 * SCALE), Image.NEAREST)


def palettes(folder):
    normal = read_pal(os.path.join(folder, 'normal.pal'))[:16]
    shiny_path = os.path.join(folder, 'shiny.pal')
    shiny = read_pal(shiny_path)[:16] if os.path.exists(shiny_path) else normal
    var = read_pal(os.path.join(folder, 'variants.pal'))
    return [normal, shiny] + [var[i * 16:(i + 1) * 16] for i in range(len(var) // 16)]


def main():
    out, names = sys.argv[1], sys.argv[2:]
    sheet = Image.new('RGBA', (LABEL_W + CELL * len(CHANCES), 20 + CELL * len(names)), (232, 232, 224, 255))
    d = ImageDraw.Draw(sheet)
    for i, c in enumerate(CHANCES):
        d.text((LABEL_W + i * CELL + 4, 4), c, fill=(40, 40, 40))
    for row, name in enumerate(names):
        folder = os.path.join(ROOT, 'graphics/pokemon', name)
        y = 20 + row * CELL
        d.text((4, y + CELL // 2 - 6), name, fill=(40, 40, 40))
        for col, pal in enumerate(palettes(folder)):
            sheet.alpha_composite(sprite_with(folder, pal), (LABEL_W + col * CELL + 4, y + 4))
    sheet.save(out)


if __name__ == '__main__':
    main()
