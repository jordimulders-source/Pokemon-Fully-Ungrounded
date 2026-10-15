#!/usr/bin/env python3
"""Kleine sprite-ingrepen voor de varianten: pixels die een paletindex delen met een
ander onderdeel (Charizards ogen met zijn vleugels, Grovyles armbladeren met zijn
hoofdblad) krijgen een eigen index met dezelfde kleur in normal.pal en shiny.pal, zodat
de gewone sprite er hetzelfde uitziet. Eén keer per sleutel (bijgehouden in
sprite_fixes_done.txt; 'sceptile2' = tweede ingreep op dezelfde map): python3 tools/grounded/variants/sprite_fixes.py

Soorten ingrepen:
  ('pixels', bestand, van, naar, [(x, y), ...])
  ('merge', van, naar)              alle pixels van index van -> naar (twee bijna gelijke tinten)
  ('fill', bestand, [(x, y), ...], {indexen}, {oud: nieuw})   vlakvulling vanaf zaadpixels
  ('box', bestand, [(x0, y0, x1, y1), ...], {oud: nieuw})      binnen rechthoeken (incl.)
  ('pal', {doel: bron})             normal/shiny: kleur doel := kleur bron (vóór de ingrepen)
"""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from variants import ROOT, read_pal, write_pal  # noqa: E402

DONE = os.path.join(os.path.dirname(__file__), 'sprite_fixes_done.txt')
PICS = ('anim_front.png', 'back.png')

FIXES = {
    # ogen deelden index 11 met de vleugels
    'charizard': [('pal', {10: 11}),
                  ('pixels', 'anim_front.png', 11, 10, [(8, 31), (15, 85)])],
    # armbladeren deelden 1/2/3 met hoofdblad en staart; 13 (randtint) gaat op in 5
    'grovyle': [('pal', {13: 3, 15: 2}),
                ('merge', 13, 5),
                ('fill', 'anim_front.png', [(9, 32), (46, 33), (12, 99), (17, 100), (45, 100), (51, 101), (48, 103)],
                 {1, 2, 3}, {2: 15, 3: 13})],
    # rechteroog eigen indexen (8 -> 15, 7 -> 6), zodat de edelstenen elk een eigen kleur kunnen krijgen;
    # paarse lijftint 6 gaat op in 5
    'sableye': [('pal', {6: 7, 15: 8}),
                ('merge', 6, 5),
                ('fill', 'anim_front.png', [(31, 23), (29, 90)], {7, 8, 9, 11}, {8: 15, 7: 6})],
    # staartstukje tussen de benen (lijftint 4) -> eigen index 15 (de staart is van achteren niet te zien)
    'sceptile': [('pal', {15: 4}),
                 ('merge', 15, 6),
                 ('box', 'anim_front.png', [(29, 47, 46, 54), (46, 44, 62, 53), (30, 112, 45, 119), (40, 104, 62, 117)],
                  {4: 15})],
    # tanden (wit 1/2/3, gedeeld met de bovenkant) -> eigen indexen 8/6/7, zodat ze wit blijven
    # als de hele bal een kleur krijgt (Cherish Ball)
    'electrode': [('pal', {6: 2, 7: 3, 8: 1}),
                  ('box', 'anim_front.png', [(16, 42, 40, 48), (24, 110, 42, 115)], {1: 8, 2: 6, 3: 7})],
}


def apply(folder, fixes):
    d = os.path.join(ROOT, 'graphics/pokemon', folder.rstrip('0123456789'))
    ims = {p: Image.open(os.path.join(d, p)) for p in PICS}
    pal_fix = {}
    for fix in fixes:
        kind = fix[0]
        if kind == 'pal':
            pal_fix.update(fix[1])
        elif kind == 'pixels':
            _, pic, src, dst, pixels = fix
            px = ims[pic].load()
            for xy in pixels:
                if px[xy] == src:
                    px[xy] = dst
        elif kind == 'merge':
            _, src, dst = fix
            for im in ims.values():
                px = im.load()
                for y in range(im.size[1]):
                    for x in range(im.size[0]):
                        if px[x, y] == src:
                            px[x, y] = dst
        elif kind == 'fill':
            _, pic, seeds, over, remap = fix
            im = ims[pic]
            px = im.load()
            w, h = im.size
            seen, stack = set(seeds), list(seeds)
            while stack:
                x, y = stack.pop()
                v = px[x, y]
                if v in remap:
                    px[x, y] = remap[v]
                for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= n[0] < w and 0 <= n[1] < h and n not in seen and px[n] in over:
                        seen.add(n)
                        stack.append(n)
        elif kind == 'box':
            _, pic, boxes, remap = fix
            px = ims[pic].load()
            for x0, y0, x1, y1 in boxes:
                for y in range(y0, y1 + 1):
                    for x in range(x0, x1 + 1):
                        if px[x, y] in remap:
                            px[x, y] = remap[px[x, y]]
    for p, im in ims.items():
        pal = im.getpalette()
        for dst, src in pal_fix.items():
            pal[dst * 3:dst * 3 + 3] = pal[src * 3:src * 3 + 3]
        im.putpalette(pal)
        im.save(os.path.join(d, p))
    for name in ('normal.pal', 'shiny.pal'):
        pp = os.path.join(d, name)
        pal = read_pal(pp)
        for dst, src in pal_fix.items():
            pal[dst] = pal[src]
        write_pal(pp, pal)


def main():
    done = set(open(DONE).read().split()) if os.path.exists(DONE) else set()
    for folder, fixes in FIXES.items():
        if folder in done:
            continue
        apply(folder, fixes)
        done.add(folder)
        print('toegepast:', folder)
    with open(DONE, 'w') as f:
        f.write('\n'.join(sorted(done)) + '\n')


if __name__ == '__main__':
    main()
