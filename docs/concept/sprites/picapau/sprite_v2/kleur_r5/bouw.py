"""raster.txt (één teken per paletindex, met de hand) -> picapau.png + normal.pal. Palet = kleur_r5 (zelfde tekens).
Gebruik: python3 bouw.py"""
from PIL import Image
PAL = [
 ('.', (152, 208, 160)),  # 0 transparant
 ('k', (24, 20, 16)),     # 1 omlijning zwart (schaduwkant)
 ('1', (255, 248, 192)),  # 2 roomgeel licht
 ('2', (244, 218, 108)),  # 3 roomgeel basis
 ('3', (218, 180, 72)),   # 4 roomgeel schaduw
 ('4', (112, 64, 16)),    # 5 goudbruin: selout lichtkant / binnenlijn
 ('d', (78, 46, 24)),     # 6 donkerbruin (vleugel schaduw, binnenlijn)
 ('b', (126, 76, 38)),    # 7 bruin (vleugel basis, staart schaduw)
 ('r', (186, 96, 44)),    # 8 roodbruin (staart)
 ('c', (232, 82, 58)),    # 9 wang
 ('C', (178, 42, 34)),    # 10 wang schaduw
 ('l', (200, 130, 72)),   # 11 licht roodbruin (vleugelschouder, staartlicht)
 ('w', (255, 255, 255)),  # 12 glans
 ('g', (150, 140, 116)),  # 13 hoorn donker / poot licht
 ('G', (64, 64, 72)),     # 14 poot schaduw / iris / kuiftop
 ('h', (240, 232, 184)),  # 15 hoorn licht (snavel)
]
IDX = {c: i for i, (c, _) in enumerate(PAL)}
def lees(fn='raster.txt'):
    rows = [l.rstrip('\n') for l in open(fn)][:64]
    assert len(rows) == 64 and all(len(r) == 64 for r in rows), [len(r) for r in rows]
    return [[IDX[c] for c in r] for r in rows]
if __name__ == '__main__':
    g = lees()
    im = Image.new('P', (64, 64)); im.putpalette([v for _, c in PAL for v in c])
    im.putdata([v for r in g for v in r])
    im.save('picapau.png', transparency=0)
    with open('normal.pal', 'w') as f:
        f.write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join(f'{c[0]} {c[1]} {c[2]}\r\n' for _, c in PAL))
    print('ok', sum(v != 0 for r in g for v in r), 'px')
