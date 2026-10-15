#!/usr/bin/env python3
"""Kleine sprite-ingrepen voor de varianten: pixels die een paletindex delen met een
ander onderdeel (bijv. Charizards ogen met zijn vleugels) krijgen een eigen, ongebruikte
index met dezelfde kleur in normal.pal en shiny.pal. Zonder variant ziet alles er dus
precies hetzelfde uit. Idempotent: python3 tools/grounded/variants/sprite_fixes.py"""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from variants import ROOT, read_pal, write_pal  # noqa: E402

# map: [(bestand, van-index, naar-index, [(x, y), ...])]
FIXES = {
    'charizard': [('anim_front.png', 11, 10, [(8, 31), (15, 85)])],  # ogen (deelden index met de vleugels)
}


def main():
    for folder, fixes in FIXES.items():
        d = os.path.join(ROOT, 'graphics/pokemon', folder)
        for pic, src, dst, pixels in fixes:
            p = os.path.join(d, pic)
            im = Image.open(p)
            px = im.load()
            for xy in pixels:
                if px[xy] in (src, dst):
                    px[xy] = dst
                else:
                    print('let op: %s %s heeft index %d' % (folder, xy, px[xy]))
            im.save(p, optimize=False)
            for palname in ('normal.pal', 'shiny.pal'):
                pp = os.path.join(d, palname)
                pal = read_pal(pp)
                pal[dst] = pal[src]
                write_pal(pp, pal)


if __name__ == '__main__':
    main()
