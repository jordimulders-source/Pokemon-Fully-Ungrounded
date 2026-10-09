#!/usr/bin/env python3
"""Project Grounded: objecten voor het Mega Forest (Zacian/Zamazenta-hint en roadblock).

- rusted_sword_ow.png (16x32): het roestige zwaard, punt in de grond (kleuren uit graphics/items/icons/rusted_sword.png).
- rusted_shield_ow.png (16x32): het roestige schild, rechtop tegen de grond (kleuren uit rusted_shield.png).
- giant_log.png (16x32): een omgevallen boomstam (Ekat, Haunted Woods), noord-zuid in de opening;
  het roadblock tussen het Mini Forest en het Mega Forest.
Alle drie delen één palet (graphics/object_events/palettes/mega_forest.pal).
Gebruik: python3 tools/grounded/mega_forest_sprites.py [voorbeeld.png]"""
import math, os, sys
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
os.chdir(ROOT)
PAL = [(115, 197, 164),                                          # 0 transparant
       (40, 32, 32),                                             # 1 omlijning
       (72, 72, 80), (128, 128, 136), (184, 180, 176),           # 2-4 staal (donker → licht)
       (80, 40, 40), (120, 56, 56), (152, 72, 72), (200, 96, 96),  # 5-8 roest
       (56, 40, 24), (96, 64, 40), (136, 96, 56),                # 9-11 schors / aarde
       (184, 144, 96), (216, 184, 136),                          # 12-13 hout (jaarringen)
       (56, 96, 40), (104, 152, 64)]                             # 14-15 mos
SWORD = """
................
................
................
......1111......
.....178871.....
.....165561.....
......1111......
......1ab1......
......1a91......
......1ba1......
......1a91......
..11..1111..11..
..186655556681..
..111165561111..
......1441......
......1431......
......1471......
......1431......
......1631......
......1431......
......1461......
......1751......
......1431......
......1431......
......1761......
......1431......
......1471......
....e.1631.e....
...efe1431efe...
..e9a9a11a9a9e..
...99aa99aa99...
................
"""


def grid(raster):
    rows = raster.strip('\n').split('\n')
    assert all(len(r) == 16 for r in rows), [len(r) for r in rows]
    return [[0 if c == '.' else int(c, 16) for c in r] for r in rows]


def shield():
    g = [[0] * 16 for _ in range(32)]
    cx, cy, rx, ry = 7.5, 19.5, 7.0, 8.6
    for y in range(32):
        for x in range(16):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if d > 1:
                continue
            if d > 0.80:
                c = 1
            elif d > 0.58:
                c = 4 if (x + y) < 22 else 3 if y < 22 else 2           # stalen rand, licht van linksboven
            else:
                c = 7 if (x - cx) + (y - cy) < -2 else 6
                if abs(x - cx) < 1 and abs(y - cy) < 6 or abs(y - cy + 1) < 1 and abs(x - cx) < 4:
                    c = 3                                              # kruisembleem in het midden
                if (x * 7 + y * 3) % 11 == 0:
                    c = 5                                              # roestvlekken
                if (x * 5 + y * 13) % 17 == 0:
                    c = 8
            g[y][x] = c
    g[19][7] = g[19][8] = 4                                            # knop
    for x in range(2, 14):                                             # grond eronder
        if g[28][x] == 0:
            g[28][x] = 9
    for x, c in zip(range(3, 13), (9, 10, 10, 9, 10, 10, 9, 10, 10, 9)):
        g[29][x] = c if g[29][x] == 0 else g[29][x]
    for x in (1, 2, 13, 14):
        g[27][x] = 14
    g[26][1] = g[26][14] = 15
    return g


WOOD = [1, 9, 10, 11, 12, 13]


def log():
    """Liggende stam (noord-zuid) uit Ekat's Haunted Woods (graphics/grounded/tilesets/ekat/haunted_woods_log.png,
    16x48), ingekort tot 16x32 (bovenste en onderste 16 px) en naar het gedeelde palet omgezet. Past precies in de
    opening van 1 tegel breed (Jordi: de eerste, zelfgetekende versie was te veel van bovenaf gezien)."""
    src = Image.open('graphics/grounded/tilesets/ekat/haunted_woods_log.png').convert('RGBA')
    rows = list(range(0, 16)) + list(range(32, 48))
    g = [[0] * 16 for _ in range(32)]
    for yy, y in enumerate(rows):
        for x in range(16):
            r, gg, b, a = src.getpixel((x, y))
            if a < 128:
                continue
            lum = 0.3 * r + 0.59 * gg + 0.11 * b               # op helderheid naar de hout-ramp (geen roestkleuren)
            g[yy][x] = min(WOOD, key=lambda i: abs(0.3 * PAL[i][0] + 0.59 * PAL[i][1] + 0.11 * PAL[i][2] - lum))
    return g


def image(g):
    h, w = len(g), len(g[0])
    im = Image.new('P', (w, h), 0)
    px = im.load()
    for y in range(h):
        for x in range(w):
            px[x, y] = g[y][x]
    flat = [v for c in PAL for v in c]
    im.putpalette(flat + [0] * (768 - len(flat)))
    return im


def main():
    ims = {'rusted_sword_ow': image(grid(SWORD)), 'rusted_shield_ow': image(shield()), 'giant_log': image(log())}
    for n, im in ims.items():
        im.save('graphics/object_events/pics/misc/%s.png' % n)
    with open('graphics/object_events/palettes/mega_forest.pal', 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for c in PAL:
            f.write('%d %d %d\n' % c)
    if len(sys.argv) > 1:
        sheet = Image.new('RGB', (64, 32), PAL[0])
        sheet.paste(ims['rusted_sword_ow'].convert('RGB'), (0, 0))
        sheet.paste(ims['rusted_shield_ow'].convert('RGB'), (16, 0))
        sheet.paste(ims['giant_log'].convert('RGB'), (32, 0))
        sheet.resize((512, 256), Image.NEAREST).save(sys.argv[1])


if __name__ == '__main__':
    main()
