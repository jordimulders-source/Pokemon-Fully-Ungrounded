"""raster.txt (één teken per paletindex, met de hand getekend) -> picapau.png + normal.pal.
Gebruik: python3 bouw.py"""
from PIL import Image
PAL = [  # teken, kleur, rol
 ('.', (152, 208, 160), 'transparant'),
 ('k', (24, 20, 16), 'omlijning zwart (schaduwkant)'),
 ('2', (255, 246, 180), 'geel hooglicht'),
 ('3', (246, 222, 100), 'geel basis'),
 ('4', (222, 168, 50), 'geel schaduw'),
 ('5', (160, 98, 26), 'geel selout (lichtkant) / binnenlijn'),
 ('w', (255, 255, 255), 'oogglans'),
 ('d', (64, 64, 72), 'donkergrijs: oogreflectie, kuiftop, verre poot'),
 ('g', (123, 123, 139), 'grijs: poot'),
 ('r', (230, 90, 65), 'wang'),
 ('R', (190, 36, 28), 'wang schaduw'),
 ('n', (228, 214, 170), 'snavel / schubben'),
 ('N', (160, 144, 108), 'snavel schaduw / schubben schaduwkant'),
 ('b', (122, 76, 40), 'vleugel basis / staart schaduw'),
 ('B', (78, 46, 24), 'vleugel schaduw / binnenlijn'),
 ('t', (190, 104, 48), 'staart roodbruin'),
]
IDX = {c: i for i, (c, _, _) in enumerate(PAL)}
def lees(fn='raster.txt'):
    rows = [l.rstrip('\n') for l in open(fn) if not l.startswith('#')]
    assert len(rows) == 64 and all(len(r) == 64 for r in rows), [len(r) for r in rows]
    return [[IDX[c] for c in r] for r in rows]
if __name__ == '__main__':
    g = lees()
    im = Image.new('P', (64, 64)); im.putpalette([v for _, c, _ in PAL for v in c])
    im.putdata([v for r in g for v in r]); im.info['transparency'] = 0
    im.save('picapau.png', transparency=0)
    with open('normal.pal', 'w') as f:
        f.write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join(f'{c[0]} {c[1]} {c[2]}\r\n' for _, c, _ in PAL))
    print('ok', sum(v != 0 for r in g for v in r), 'px')
