"""Picapau kleur ronde 4: tekstraster (raster.txt, met de hand) -> picapau.png (64x64, geindexeerd, index 0 transparant) + normal.pal.
Draaien vanuit de repo-root of deze map: python3 bouw.py"""
import os
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
# teken: (naam, RGB) ; volgorde = palette-index
PAL = [
    ('.', (152, 208, 160)),  # 0 transparant
    ('k', (24, 20, 16)),     # 1 omlijning zwart (schaduwkant)
    ('1', (255, 248, 192)),  # 2 roomgeel licht
    ('2', (244, 218, 108)),  # 3 roomgeel basis
    ('3', (218, 180, 72)),   # 4 roomgeel schaduw
    ('4', (112, 64, 16)),   # 5 goudbruin: selout lichtkant / diepe schaduw
    ('d', (78, 46, 24)),     # 6 donkerbruin (vleugel schaduw, binnenlijn)
    ('b', (126, 76, 38)),    # 7 bruin (vleugel basis)
    ('r', (186, 96, 44)),    # 8 roodbruin (staart, slagpenranden)
    ('c', (232, 82, 58)),    # 9 wangvlek
    ('C', (178, 42, 34)),    # 10 wangvlek schaduw
    ('l', (168, 114, 62)),   # 11 lichtbruin (vleugelschouder); snavel licht = 1
    ('w', (255, 255, 255)),  # 12 glans
    ('g', (150, 140, 116)),  # 13 hoorn donker / poot licht (warm grijs)
    ('G', (64, 64, 72)),     # 14 poot schaduw / iris
    ('h', (240, 232, 184)),  # 15 hoorn licht (snavel)
]
IDX = {c: i for i, (c, _) in enumerate(PAL)}

def lees(pad):
    rows = [r.rstrip('\n') for r in open(pad)][:64]
    assert len(rows) == 64 and all(len(r) == 64 for r in rows), 'raster moet 64x64 zijn'
    return rows

def bouw(rows):
    im = Image.new('P', (64, 64), 0)
    im.putpalette([v for _, rgb in PAL for v in rgb])
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            im.putpixel((x, y), IDX[ch])
    return im

if __name__ == '__main__':
    rows = lees(os.path.join(D, 'raster.txt'))
    bouw(rows).save(os.path.join(D, 'picapau.png'), transparency=0)
    print('picapau.png:', sum(ch != '.' for r in rows for ch in r), 'px')
    with open(os.path.join(D, 'normal.pal'), 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for _, (r, g, b) in PAL:
            f.write(f'{r} {g} {b}\n')
