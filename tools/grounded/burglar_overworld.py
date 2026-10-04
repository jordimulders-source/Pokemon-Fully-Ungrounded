#!/usr/bin/env python3
"""Project Grounded: overworld van de Burglar (inbreker-event in de steden).
Basis: FRLG Rocket-grunt (graphics/grounded/trainers/burglar/rocket_m_frlg_bron.png, 9 frames 16x32),
omgekleurd naar de trainerfoto (burglar_gen3.png): blauwe pet, zwart masker, lichte kleding en een bruine
buitzak op de rug. Uitvoer: graphics/object_events/pics/people/burglar.png + palettes/burglar.pal.
Gebruik: python3 tools/grounded/burglar_overworld.py [voorbeeld.png]"""
import os, sys
from PIL import Image
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

PAL = [(115, 197, 164),                                  # 0 transparant
       (255, 213, 180), (246, 189, 148), (222, 148, 115), (123, 65, 65),   # 1-4 huid
       (98, 139, 222), (49, 74, 156),                   # 5-6 pet (blauw)
       (41, 41, 41),                                     # 7 haar
       (189, 131, 74), (131, 82, 41), (82, 49, 16),      # 8-a buitzak
       (222, 222, 230), (164, 164, 180), (90, 90, 106),  # b-d kleding (licht)
       (255, 255, 255), (0, 0, 0)]                       # e-f

FRONT, BACK, SIDE = (0, 3, 4), (1, 5, 6), (2, 7, 8)

SACK_BACK = ["..aaaa..",
             ".a8888a.",
             "a888889a",
             "a888899a",
             "a888899a",
             ".a8899a.",
             "..aaaa.."]
SACK_PEEK = [".aa...",
             "a88a..",
             "a889a.",
             "a8899a",
             "a8899a",
             ".a899a",
             "..aaa."]

def paste(px, ox, fx, fy, art, behind):
    for dy, row in enumerate(art):
        for dx, ch in enumerate(row):
            if ch == '.': continue
            x, y = ox + fx + dx, fy + dy
            if behind and px[x, y] != 0: continue
            px[x, y] = int(ch, 16)

def main():
    src = Image.open(os.path.join(ROOT, 'graphics/grounded/trainers/burglar/rocket_m_frlg_bron.png'))
    im = src.copy(); px = im.load()
    for f in range(9):
        ox = f * 16
        for y in range(32):
            for x in range(16):
                p = px[ox + x, y]
                if p == 0: continue
                if y <= 18:                                   # pet
                    p = {0xc: 5, 0xd: 6, 7: 6 if (y <= 16 or f in SIDE) else 7}.get(p, p)
                elif f in SIDE and y == 19:                   # haar onder de pet
                    p = {0xd: 7}.get(p, p)
                elif f in BACK and y <= 21:                   # haar achterop
                    p = {6: 7}.get(p, p)
                elif y >= 21 or (f in SIDE and y >= 22):      # kleding
                    p = {0xc: 0xb, 0xd: 0xc, 8: 0xb, 9: 0xc, 0xa: 0xd, 6: 0xc}.get(p, p)
                    if y >= 28 and p == 0xb: p = 0xd          # schoenen donker
                px[ox + x, y] = p
        if f in FRONT:                                        # masker over de ogen
            for x in range(4, 12): px[ox + x, 19] = 0xf
            px[ox + 6, 19] = px[ox + 9, 19] = 0xe
            paste(px, ox, 10, 17, SACK_PEEK, True)
        elif f in BACK:
            paste(px, ox, 4, 21, SACK_BACK, False)
        else:
            for x in range(3, 8): px[ox + x, 20] = 0xf
            px[ox + 4, 20] = 0xe
            paste(px, ox, 9, 20, SACK_PEEK, True)
    flat = [v for c in PAL for v in c] + [0] * (768 - 48)
    im.putpalette(flat)
    im.save(os.path.join(ROOT, 'graphics/object_events/pics/people/burglar.png'))
    with open(os.path.join(ROOT, 'graphics/object_events/palettes/burglar.pal'), 'w') as fh:
        fh.write('JASC-PAL\n0100\n16\n')
        for c in PAL: fh.write(f'{c[0]} {c[1]} {c[2]}\n')
    if len(sys.argv) > 1:
        im.convert('RGB').resize((im.width * 8, im.height * 8), Image.NEAREST).save(sys.argv[1])
    print('burglar overworld klaar')

if __name__ == '__main__':
    main()
