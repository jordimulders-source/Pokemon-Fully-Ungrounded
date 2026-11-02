"""Handgetekende sikkel (Jordi's referentie: dik midden, tapse scherpe punten, ronde holte; punten omlaag).
Alleen maanpixels; ogen, omlijning en omtrek van ronde 3 blijven."""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
src = Image.open(os.path.join(HERE, '..', 'ronde3', 'nachtaap.png')); pal = src.getpalette(); A0 = np.array(src)
W = {  # rij: lijst (x0, x1) wit, inclusief
 'E': {38: [(9, 18)], 39: [(7, 20)], 40: [(6, 21)], 41: [(5, 10), (17, 22)], 42: [(5, 7), (20, 22)],
       43: [(5, 6), (21, 22)], 44: [(5, 5), (21, 22)], 45: [(5, 5), (21, 21)], 46: [(5, 5), (21, 21)]},
 'F': {38: [(9, 18)], 39: [(7, 20)], 40: [(6, 21)], 41: [(5, 9), (18, 22)], 42: [(5, 7), (20, 22)],
       43: [(5, 6), (21, 22)], 44: [(5, 5), (21, 22)], 45: [(5, 5), (21, 21)]},
 'G': {37: [(10, 17)], 38: [(8, 19)], 39: [(7, 20)], 40: [(6, 10), (17, 21)], 41: [(5, 8), (19, 22)],
       42: [(5, 6), (21, 22)], 43: [(5, 5), (21, 22)], 44: [(5, 5), (21, 21)], 45: [(5, 5), (21, 21)], 46: [(5, 5)]},
}
def build(spec):
    a = A0.copy()
    zone = np.zeros((64, 64), bool); zone[36:49, 4:24] = True
    a[zone & np.isin(a, [7, 8])] = 4            # oude maan -> vacht
    a[zone & (a == 6)] = 4
    for y, runs in spec.items():
        for x0, x1 in runs:
            for x in range(x0, x1 + 1):
                if a[y, x] in (3, 4, 5, 6, 7, 8):
                    a[y, x] = 8
    m = a == 8
    # schaduwkant: rechts en onder in zilverlila; een paar lichtpixels bovenaan blijven wit
    edge = (m & ~np.roll(m, -1, 1)) | (m & ~np.roll(m, -1, 0))
    yy, xx = np.mgrid[0:64, 0:64]
    a[edge & zone & ((xx >= 14) | (yy >= 42))] = 7
    # violet direct boven/naast de maan aan de lichtkant iets lichter (5), zodat de maan los van de rand staat
    return a
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
def img(a):
    im = Image.fromarray(a.astype(np.uint8), 'P'); im.putpalette(pal); rgba = im.convert('RGBA')
    al = np.array(rgba); al[a == 0, 3] = 0; return Image.fromarray(al)
items = [('ronde 3 (nu)', A0)] + [(k, build(v)) for k, v in W.items()]
o = Image.new('RGB', (4 * 330, 380), (235, 235, 240)); d = ImageDraw.Draw(o)
for k, (n, a) in enumerate(items):
    im = img(a); bg = Image.new('RGBA', (64, 64), (235, 235, 240, 255)); bg.alpha_composite(im)
    o.paste(bg.crop((0, 30, 30, 58)).resize((300, 280), Image.NEAREST), (10 + 330 * k, 10))
    o.paste(bg.convert('RGB'), (10 + 330 * k, 300)); o.paste(bg.convert('RGB').resize((128, 128), Image.NEAREST).crop((0, 50, 128, 128)), (90 + 330 * k, 300))
    d.text((10 + 330 * k, 290), n, font=F, fill=(30, 30, 30))
    if k: im.save(os.path.join(HERE, f'variant_{n}.png'))
o.save(os.path.join(HERE, 'maanvarianten_hand.png'))
