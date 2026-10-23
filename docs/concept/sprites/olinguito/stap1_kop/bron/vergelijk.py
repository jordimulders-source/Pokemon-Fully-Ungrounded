#!/usr/bin/env python3
"""compare.png en onderlaag.png voor stap 1 + pixeldiff-bewijs."""
from PIL import Image, ImageDraw
import os
H = os.path.dirname(os.path.abspath(__file__)); P = lambda *a: os.path.join(H, '..', *a)
r18 = Image.open(P('../ronde18/anim_front.png')); st1 = Image.open(P('anim_front.png'))
lin = Image.open(P('../referenties/galar_linoone_front.png'))
BG = (200, 200, 200, 255)
def rgba(im, box=None):
    im = im.convert('RGBA'); return im.crop(box) if box else im
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
# compare: rij 1 = 1x (frame 1+2), rij 2 = 3x frame 1, rij 3 = kop 6x
cols = [('ronde 18', r18, (6, 16, 44, 44)), ('stap 1', st1, (6, 16, 44, 44)),
        ('Galar-Linoone', lin, (0, 18, 38, 46))]
W = 64 * 3 * 3 + 40; out = Image.new('RGBA', (W, 20 + 128 + 10 + 192 + 10 + 28 * 6 + 10), BG)
d = ImageDraw.Draw(out)
for i, (naam, im, box) in enumerate(cols):
    x = i * (192 + 20)
    d.text((x, 4), naam, fill=(0, 0, 0, 255))
    a = rgba(im); out.paste(a, (x, 20), a)
    f1 = rgba(im, (0, 0, 64, 64)); out.paste(up(f1, 3), (x, 158), up(f1, 3))
    k = rgba(im, box); out.paste(up(k, 6), (x - 0 if i == 0 else x, 360), up(k, 6))
# kop 6x past niet naast elkaar in 192 breed: aparte regel met eigen breedte
out2 = Image.new('RGBA', (3 * (38 * 6 + 20), 28 * 6 + 20), BG); d2 = ImageDraw.Draw(out2)
for i, (naam, im, box) in enumerate(cols):
    k = up(rgba(im, box), 6); out2.paste(k, (i * (38 * 6 + 20), 20), k); d2.text((i * (38 * 6 + 20), 4), naam + ' (kop 6x)', fill=(0, 0, 0, 255))
top = out.crop((0, 0, W, 360)); fin = Image.new('RGBA', (max(W, out2.width), 360 + out2.height), BG)
fin.paste(top, (0, 0)); fin.paste(out2, (0, 360)); fin.save(P('compare.png'))
# onderlaag: alleen Linoone's gezicht (oog, snuit, masker), 2x zodat oog->neus ongeveer klopt
# met onze kop (Linoone oog (8,36) neus (1,37); wij oog (26,31) neus (10,33)), oog op oog gelegd.
gez = rgba(lin, (0, 30, 14, 42)); gez = up(gez, 2)              # 28x24, oog op (16,12)
k = 6; kop = rgba(r18, (0, 14, 44, 44)); ox, oy = 26 - 16, 31 - 14 - 12
over = up(kop, k).copy(); g = up(gez, k); g.putalpha(g.getchannel('A').point(lambda v: v * 150 // 255))
over.alpha_composite(g, (ox * k, oy * k))
res = up(rgba(st1, (0, 14, 44, 44)), k); lk = up(rgba(lin, (0, 18, 30, 50)), k)
ond = Image.new('RGBA', (lk.width + over.width + res.width + 40, max(lk.height, over.height) + 20), BG)
dd = ImageDraw.Draw(ond)
for i, (naam, im, x) in enumerate((('Galar-Linoone kop', lk, 0), ('onderlaag: Linoone-gezicht 2x op ronde 18 (oog op oog)', over, lk.width + 20),
                                    ('resultaat stap 1', res, lk.width + over.width + 40))):
    ond.paste(im, (x, 20), im); dd.text((x, 4), naam, fill=(0, 0, 0, 255))
ond.save(P('onderlaag.png'))
# pixeldiff
for f in (0, 64):
    d = [(x, y - f) for y in range(f, f + 64) for x in range(64) if r18.getpixel((x, y)) != st1.getpixel((x, y))]
    zone = (9, 25 - (f > 0), 23, 32 - (f > 0))
    buiten = [p for p in d if not (zone[0] <= p[0] <= zone[2] and zone[1] <= p[1] <= zone[3])]
    print('frame', 1 + f // 64, 'gewijzigd', len(d), 'buiten kopzone x9-23 y%d-%d:' % zone[1::2], len(buiten))
print('palet gelijk:', r18.getpalette()[:48] == st1.getpalette()[:48], 'transparency', st1.info.get('transparency'))
