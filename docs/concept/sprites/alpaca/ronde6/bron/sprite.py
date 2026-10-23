"""Alpaca fase 1 (Wolvuist), Gen 3-frontsprite, met de hand per pixel (ronde 6).
Raster = 38 breed x 45 hoog, linksboven op (OX, OY) in het 64x64-vak. Elk teken is
één pixel (legenda = PAL); er zit geen automatische schaduw of omlijning in.
Draaien vanuit de repo-root (schrijft anim_front.png, normal.pal en f1.png):
    python3 docs/concept/sprites/alpaca/ronde6/bron/sprite.py docs/concept/sprites/alpaca/ronde6
"""
import sys
from PIL import Image

OX, OY = 13, 8

PAL = [
    ('.', (152, 208, 136)),  # 0 transparant
    ('A', (255, 250, 222)),  # 1 wol licht
    ('B', (255, 234, 150)),  # 2 wol basis
    ('C', (232, 196, 98)),   # 3 wol schaduw
    ('D', (200, 146, 62)),   # 4 wol diepe schaduw / lichte omlijning
    ('O', (128, 80, 36)),    # 5 wol omlijning
    ('r', (255, 140, 112)),  # 6 vuist licht
    ('R', (226, 58, 52)),    # 7 vuist basis
    ('s', (166, 34, 38)),    # 8 vuist schaduw / lichte omlijning
    ('S', (98, 22, 26)),     # 9 vuist plooi
    ('k', (246, 172, 98)),   # 10 vacht licht
    ('K', (214, 124, 60)),   # 11 vacht basis
    ('m', (162, 80, 34)),    # 12 vacht schaduw
    ('M', (100, 48, 28)),    # 13 vacht donker / iris
    ('w', (255, 255, 255)),  # 14 oogglans
    ('#', (24, 16, 16)),     # 15 omlijning
]
IDX = {c: i for i, (c, _) in enumerate(PAL)}

F1 = """
..................##..................
.................#K#..................
................MkM#..................
...##...........MkM#..................
...MK#....DDDD.MKMK#..................
...MmDDDDOAABBOOOMm#..................
...DAABBDABBBBDABCO...................
..DABBBBCBBBBBCBBBCO..................
.DABBBBBBBBBBBBBBBCO..................
.DABBBBBBBBBBBBBBCCO..................
.ODDBBBBBBBBBBBBBCDO..................
..DABBBBBBBBBBBBBCCCO.................
.DABBBBBBBBBBBBBBCCCO.................
.DBBBBBBBBBBBBBBCCCDO.................
.OCCBBBBBBBBBCCCCDO...................
..OOOOOCBBCCDOOOOOO...................
..Mmm##OCBBC####mm#...................
.MkKKw#KOCCOww##KK#DD.................
.MkKK#MKKOOK##M#KK#ABO................
.MkKKMMKKKKK#MM#Km#ABBO...............
.#MMB##mKKKKm##mKm#ABBCO..............
DAABBBBCmKKKKKKKm#ABBBCO.DDDD.DDDDAO..
DABBBBBCmKKKKKKm#ABBBBCOAABBDAABDAB#..
#B#BB#BCmKKKKKm#ABBBBBCCBAABBBBAABC#..
.#C##CC#mmmm##ABBBBBBCBBBBBBBBBBBB#...
..##########ABBBBBBCBBBBBBBBBCBBBCC#..
..........DABBBBBBBCACBBBBBBBCCBBCC#..
..........DABBCBBBCBBBCBCBBBBBBDBCC#..
...........DBBBBCCBBBBBBBCDCBBBBBC#...
..........OCDBBBCBBBBBBBBBBBBBBBBC#...
..........O#kKK#CBBBBCBBBBCBBBBBBC#...
...........#kKm#CDBBBBCCCBBBBBCBC#....
...........#kKm#CCBBBBBBBBBBBDCCC#....
...........#rRs#DCCBBBBDBBBBBBCCD#....
.....sss.ssrRRsS#DCCCBBBBBBBCCDD#.....
....srrRSrrRRRRsS#DCCCCCCCCCCDD#......
...srrRRRRRRSrRsS#DD#DD#DDD#mKK#......
..srrRRRRRRRSRRsS#rRRRRRs#kKKm#Km#....
..srRRRRRRRRsRRs#rrrRRRRs#kKm#KKm#....
..sRRRRRsssRRsS#RRRRRRsRs#kKm#KKm#....
..#RRssRRRRRRs#RRRRRssRs#MMMM#MMM#....
...#sRRsRRRRs#sRRRRRRRs######.###.....
....#sssssss#.#sRRRRRs#...............
.....#######...#sssss#................
................#####.................
"""


def grid(txt):
    rows = [r for r in txt.strip('\n').split('\n')]
    for i, r in enumerate(rows):
        if len(r) != 38:
            print('rij', i, 'lengte', len(r), file=sys.stderr)
    return rows


def to_img(rows):
    im = Image.new('P', (64, 64), 0)
    pal = []
    for _, c in PAL:
        pal += c
    im.putpalette(pal)
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != '.':
                im.putpixel((OX + x, OY + y), IDX[ch])
    return im


def frame2(rows):
    """Tweede frame: een kleine duik (hurken voor de stoot). Alles boven de
    voeten zakt 1 px; de rij midden in de vuisten/poten valt weg."""
    return ['.' * 38] + rows[0:38] + rows[39:]


def sheet(rows1, rows2):
    im = Image.new('P', (64, 128), 0)
    pal = []
    for _, c in PAL:
        pal += c
    im.putpalette(pal)
    im.paste(to_img(rows1), (0, 0))
    im.paste(to_img(rows2), (0, 64))
    return im


def write_pal(path):
    with open(path, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for _, c in PAL:
            f.write('%d %d %d\n' % c)


if __name__ == '__main__':
    import os
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    rows = grid(F1)
    sheet(rows, frame2(rows)).save(os.path.join(out, 'anim_front.png'))
    write_pal(os.path.join(out, 'normal.pal'))
    to_img(rows).save(os.path.join(out, 'f1.png'))
    print('area', sum(ch != '.' for r in rows for ch in r))
