"""Kroonvarianten Sapa Inca (alleen hercoloreren van de kroon op ronde 4; rest 0 px). Jordi 7 nov:
"de hoofdtooi moet nog een iets ander design, misschien de zwarte pixels daar geel maken oid, maar misschien kan je
wat variaties tonen". Draaien vanuit de repo-root."""
import os
import numpy as np
from collections import Counter
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'ronde4', 'sapa_inca.png')
L = '.KdmlrRopvagybwt'
I = {c: i for i, c in enumerate(L)}
ORANJE = {I['o'], I['R'], I['r']}
RAND = {I['p'], I['v']}
KROON = ORANJE | RAND | {I['K']}

im = Image.open(SRC)
a = np.array(im)
H, W = a.shape


def nb(y, x):
    return [a[y + dy, x + dx] for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)) if 0 <= y + dy < H and 0 <= x + dx < W]


spots_oranje, spots_rand, band = [], [], []
for y in range(1, 22):
    for x in range(W):
        if a[y, x] == I['K']:
            n = nb(y, x)
            if 0 in n or any(v not in KROON for v in n):
                continue  # omlijning of grens met kop
            if sum(v in ORANJE for v in n) >= sum(v in RAND for v in n):
                spots_oranje.append((y, x))
            else:
                spots_rand.append((y, x))
        elif a[y, x] in ORANJE and any(v in RAND for v in nb(y, x)):
            band.append((y, x))


def vul(b, pts):  # stip weg: meest voorkomende oranje buurkleur
    for y, x in pts:
        c = Counter(v for v in nb(y, x) if v in ORANJE).most_common(1)
        b[y, x] = c[0][0] if c else I['R']


V = {}
V['0 origineel (ronde 4)'] = a.copy()
b = a.copy(); [b.__setitem__(p, I['g']) for p in spots_oranje]; V['A gouden stippen'] = b
b = a.copy(); [b.__setitem__(p, I['y']) for p in spots_oranje]; [b.__setitem__(p, I['g']) for p in spots_rand]; V['B lichtgoud + gouden randvlekken'] = b
b = a.copy(); vul(b, spots_oranje); V['C geen stippen, zwarte randvlekken'] = b
b = a.copy(); vul(b, spots_oranje); [b.__setitem__(p, I['g']) for p in band]; V['D gouden band voor de rand'] = b
b = a.copy(); [b.__setitem__(p, I['g']) for p in spots_oranje]; [b.__setitem__(p, I['g']) for p in band]; V['E gouden stippen + gouden band'] = b

import math
b = a.copy(); vul(b, spots_oranje); [b.__setitem__(p, I['g']) for p in band]
cx, cy = 30.5, 22.0
for k in range(9):   # één gouden vlek per veer, in één boog binnen de band (dichter bij de echte vogel)
    t = math.radians(200 + 140 * k / 8)
    x, y = int(round(cx + math.cos(t) * 14)), int(round(cy + math.sin(t) * 14))
    for (yy, xx, c) in ((y, x, 'y'), (y, x + 1, 'g'), (y + 1, x, 'g')):
        if 0 <= yy < 22 and a[yy, xx] in ORANJE:
            b[yy, xx] = I[c]
V['F gouden band + 1 gouden vlek per veer'] = b
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
S, cw = 6, 50 * 6 + 12
sheet = Image.new('RGB', (4 * cw + 12, 2 * (30 * S + 30 + 70) + 10), (236, 232, 222))
d = ImageDraw.Draw(sheet)
for k, (name, arr) in enumerate(V.items()):
    p = Image.fromarray(arr.astype(np.uint8), 'P'); p.putpalette(im.getpalette())
    p.info['transparency'] = 0
    if k:
        p.save(os.path.join(HERE, name.split()[0] + '.png'), transparency=0)
    rgba = p.convert('RGBA')
    bg = Image.new('RGBA', rgba.size, (250, 248, 240, 255)); bg.alpha_composite(rgba)
    x, y = 6 + (k % 4) * cw, 6 + (k // 4) * (30 * S + 100)
    sheet.paste(bg.crop((6, 0, 56, 30)).resize((50 * S, 30 * S), Image.NEAREST), (x, y))
    sheet.paste(bg, (x, y + 30 * S + 4))
    d.text((x + 70, y + 30 * S + 24), name, fill='black', font=F)
sheet.save(os.path.join(HERE, 'kroon_varianten.png'))
print(len(spots_oranje), len(spots_rand), len(band))
