#!/usr/bin/env python3
"""compare.png voor stap 1b + pixeldiff-bewijs (t.o.v. stap 1 en ronde 18) + metingen."""
from PIL import Image, ImageDraw
import os
H = os.path.dirname(os.path.abspath(__file__)); P = lambda *a: os.path.join(H, '..', *a)
r18 = Image.open(P('../ronde18/anim_front.png')); st1 = Image.open(P('../stap1_kop/anim_front.png'))
st1b = Image.open(P('anim_front.png')); lin = Image.open(P('../referenties/galar_linoone_front.png'))
BG = (200, 200, 200, 255)
def rgba(im, box=None):
    im = im.convert('RGBA'); return im.crop(box) if box else im
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
cols = [('ronde 18', r18, (6, 16, 42, 40)), ('stap 1', st1, (6, 16, 42, 40)),
        ('stap 1b', st1b, (6, 16, 42, 40)), ('Galar-Linoone', lin, (0, 24, 36, 48))]
CW = 36 * 8 + 16
out = Image.new('RGBA', (4 * CW, 20 + 128 + 10 + 192 + 30 + 24 * 8 + 10), BG); d = ImageDraw.Draw(out)
for i, (naam, im, box) in enumerate(cols):
    x = i * CW
    d.text((x, 4), naam + ' (1x, 3x, kop 8x)', fill=(0, 0, 0, 255))
    a = rgba(im); out.paste(a, (x, 20), a)
    f1 = up(rgba(im, (0, 0, 64, 64)), 3); out.paste(f1, (x, 158), f1)
    k = up(rgba(im, box), 8); out.paste(k, (x, 380), k)
out.save(P('compare.png'))
# pixeldiff: gezichtszone x11-34, y26-32 (frame 2: y25-31)
def diff(a, b, f):
    return [(x, y - f) for y in range(f, f + 64) for x in range(64) if a.getpixel((x, y)) != b.getpixel((x, y))]
for naam, ref in (('stap 1', st1), ('ronde 18', r18)):
    for f in (0, 64):
        dd = diff(ref, st1b, f); o = (f > 0)
        buiten = [p for p in dd if not (11 <= p[0] <= 34 and 26 - o <= p[1] <= 32 - o)]
        print('t.o.v. %s, frame %d: gewijzigd %d, buiten gezichtszone x11-34 y%d-%d: %d'
              % (naam, 1 + f // 64, len(dd), 26 - o, 32 - o, len(buiten)))
print('palet gelijk:', st1.getpalette()[:48] == st1b.getpalette()[:48], '| transparency', st1b.info.get('transparency'))
sil = all((st1.getpixel((x, y)) == 0) == (st1b.getpixel((x, y)) == 0) for y in range(128) for x in range(64))
rand = [(x, y) for (x, y) in diff(st1, st1b, 0) + [(x, y + 64) for x, y in diff(st1, st1b, 64)]
        if any(0 <= x + dx < 64 and 0 <= y + dy < 128 and st1b.getpixel((x + dx, y + dy)) == 0
               for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
print('silhouet gelijk:', sil, '| gewijzigde pixels naast transparant (open-randcheck):', rand)
