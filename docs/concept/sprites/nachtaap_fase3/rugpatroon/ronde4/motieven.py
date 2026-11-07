"""Rugpatroon ronde 4 (Claude, 5 nov): ruwe proeven met Nazca- en Andesmotieven binnen het vlak dat Jordi omcirkelde
(midden van de romp, ±x22-40, r30-41), meegebogen met de bolling (Jordi: "als je er rekening mee houdt dat het lichaam
dus een klein beetje naar boven afbuigt" / "kunnen we geen nazca of andes motieven maken? probeer eens wat dingen").
Motief in eigen coördinaten (u langs het lijf, v dwars), dan per kolom verschoven met een boog (midden hoger)."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__))
src = Image.open(os.path.join(H, '../../kleur/ronde7c/nachtaap_fase3.png')); A0 = np.array(src); pal = src.getpalette()
L, S = 13, 14
def vacht(a, x, y): return 0 <= x < 64 and 0 <= y < 64 and a[y, x] in (3, 4, 5) and not (31 <= x <= 38 and y < 33)
def plaats(bitmap, x0, y0, boog=0.05):
    a = A0.copy(); rows = [r for r in bitmap.strip('\n').split('\n')]
    w = max(len(r) for r in rows); uc = (w - 1) / 2
    for v, r in enumerate(rows):
        for u, ch in enumerate(r):
            if ch != '#': continue
            x = x0 + u; y = y0 + v + int(round(boog * (u - uc) ** 2))
            if vacht(a, x, y): a[y, x] = S if A0[y, x] == 3 else L
    return a
MOTIEVEN = {
 'A trapband (escalonado)': ("""
##....##....##....
###..####..####..#
.######.####.#####
..##....##....##..
""", 22, 33),
 'B chakana (Andeskruis)': ("""
...###...
...#.#...
.###.###.
##.....##
#...#...#
##.....##
.###.###.
...#.#...
...###...
""", 26, 31),
 'C Nazca-spiraal (hoekig)': ("""
#########
#.......#
#.#####.#
#.#...#.#
#.#.#.#.#
#.#.###.#
#.#.....#
#.#######
""", 26, 31),
 'D tocapu-rij': ("""
#####.#####.#####
#...#.#.#.#.#...#
#.#.#.#...#.#.#.#
#...#.#.#.#.#...#
#####.#####.#####
""", 23, 33),
 'E Nazca-zigzag (dubbel)': ("""
#...#...#...#...#
.#.#.#.#.#.#.#.#.
..#...#...#...#..
#...#...#...#...#
.#.#.#.#.#.#.#.#.
..#...#...#...#..
""", 23, 32),
}
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
items = [('7c zonder patroon', A0)] + [(n, plaats(b, x, y)) for n, (b, x, y) in MOTIEVEN.items()]
v = Image.new('RGB', (3 * 300 + 10, 2 * 290 + 10), 'white'); d = ImageDraw.Draw(v)
for i, (n, arr) in enumerate(items):
    im = Image.fromarray(arr, 'P'); im.putpalette(pal)
    if n != '7c zonder patroon': im.save(os.path.join(H, n.split()[0] + '.png'), transparency=0)
    r = np.array(im.convert('RGBA')); r[arr == 0, 3] = 0; b = Image.new('RGBA', (64, 64), 'white'); b.alpha_composite(Image.fromarray(r)); t = b.convert('RGB')
    x = 10 + (i % 3) * 300; y = 10 + (i // 3) * 290
    d.text((x, y), n, font=F, fill='black')
    v.paste(t.resize((192, 192), Image.NEAREST), (x, y + 18)); v.paste(t.crop((18, 26, 46, 46)).resize((84, 60), Image.NEAREST), (x + 200, y + 18)); v.paste(t, (x + 200, y + 90))
v.save(os.path.join(H, 'vel_motieven.png'))
