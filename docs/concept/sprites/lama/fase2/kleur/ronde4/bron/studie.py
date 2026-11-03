"""Studievel ronde 4 (Game Freak, alleen kijken): wol (Mareep, Flaaffy), poten en hoeven (Girafarig, Ponyta),
droog oog (Numel, Slakoth, Camerupt), elk op 8x met pixelraster, plus het gebruikte palet per kleurgroep.
Draaien: python3 docs/concept/sprites/lama/fase2/kleur/ronde4/bron/studie.py"""
import os
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(OUT, '../../../../../../..'))

def gp(n):
    p = [tuple(int(v) for v in x.split()) for x in open(f'{REPO}/graphics/pokemon/{n}/normal.pal').read().split('\n')[3:19]]
    im = Image.open(f'{REPO}/graphics/pokemon/{n}/anim_front.png').crop((0, 0, 64, 64)); px = im.load()
    out = Image.new('RGBA', (64, 64), (255, 255, 255, 255))
    for y in range(64):
        for x in range(64):
            if px[x, y]: out.putpixel((x, y), p[px[x, y]] + (255,))
    return out, p

def zoom(im, box, z):
    x0, y0, x1, y1 = box
    c = im.crop(box).resize(((x1 - x0) * z, (y1 - y0) * z), Image.NEAREST); d = ImageDraw.Draw(c)
    for x in range(x1 - x0 + 1): d.line([(x * z, 0), (x * z, c.size[1])], fill=(205, 205, 205))
    for y in range(y1 - y0 + 1): d.line([(0, y * z), (c.size[0], y * z)], fill=(205, 205, 205))
    return c

items = [  # naam, uitsnede, palet-indexen die bekeken zijn, wat het laat zien
    ('mareep', (8, 12, 44, 46), [7, 8, 2, 5, 6], 'wol: licht 28% > midden 20% > schaduw 10%, omlijning bruin 9c6220 rondom, zwart alleen gezicht/poten'),
    ('flaaffy', (10, 2, 44, 34), [2, 4, 1, 3], 'wol: wit + lichte blauwgrijze omlijning aan de lichtkant, donkerder alleen onder; krul als lijntje'),
    ('girafarig', (10, 34, 48, 64), [8, 7, 6, 13, 14, 4, 1], 'poten: verre poot eigen donkere tint, 2 rijen hoef (blauwgrijs), zwarte omlijning alleen aan de schaduwkant'),
    ('ponyta', (12, 34, 50, 64), [3, 4, 5, 6, 13, 14, 1], 'poten 3-4 px incl. omlijning; nabij licht, ver bruin; hoef 2 rijen met 1 lichte px'),
    ('numel', (16, 18, 32, 34), [2, 1, 11, 12], 'oog: middenbruin ovaal, alleen voorrand zwart, glans als verticaal streepje laag'),
    ('slakoth', (2, 14, 30, 34), [3, 6, 1, 2, 10], 'lui: oog in een afhangende bruine vlek; het hangen zit in de vorm'),
    ('camerupt', (10, 30, 28, 46), [6, 4, 5, 12, 13], 'oog: dik lid in donkerrood (geen zwart), pupil tegen het lid, wit onder'),
]
tiles = []
for n, box, idx, txt in items:
    im, p = gp(n); z = 8 if (box[2] - box[0]) <= 20 else 6
    t = zoom(im, box, z)
    w = max(t.size[0], 300); tile = Image.new('RGB', (w, t.size[1] + 64), (250, 250, 250)); tile.paste(t, (0, 0)); d = ImageDraw.Draw(tile)
    for i, k in enumerate(idx):
        d.rectangle([i * 30, t.size[1] + 4, i * 30 + 26, t.size[1] + 22], fill=p[k], outline=(0, 0, 0))
    d.text((0, t.size[1] + 26), n + ': ' + txt[:52], fill=(0, 0, 0)); d.text((0, t.size[1] + 40), txt[52:], fill=(0, 0, 0))
    tiles.append(tile)
W = 1300; x = y = 0; rowh = 0; pos = []
for t in tiles:
    if x + t.size[0] > W: x = 0; y += rowh + 10; rowh = 0
    pos.append((x, y)); x += t.size[0] + 12; rowh = max(rowh, t.size[1])
c = Image.new('RGB', (W, y + rowh), (250, 250, 250))
for t, p in zip(tiles, pos): c.paste(t, p)
c.save(os.path.join(OUT, 'studie.png')); print('studie.png', c.size)
