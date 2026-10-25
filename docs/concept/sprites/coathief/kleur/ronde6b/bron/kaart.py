"""Kaart (labels_voorpoten.txt) naast ronde 6b, met per pixel een markering waar de kleur afwijkt van het label.
Ook de uitsnede onderlaag | ronde 6 | ronde 6b op 8x (licht en donker)."""
import os, sys
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
from bouw import ORDER
S = os.path.join(H, '../../../silhouet')
lab = {}
for ln in open(os.path.join(S, 'labels_voorpoten.txt')):
    p = ln.rstrip('\n').split(' ', 1)
    if len(p) == 2 and p[0].isdigit():
        for i, ch in enumerate(p[1]): lab[(8 + i, int(p[0]))] = ch
co = Image.open(os.path.join(H, '../coathief.png')); px = co.load()
GROEP = {'N': set('kmzyY'), 'F': set('kmzyY'), 'c': set('cwnx'), 'v': set('dblhk'), 'k': None}
afw = []
for (x, y), l in sorted(lab.items()):
    if l in GROEP and GROEP[l] is not None:
        ch = ORDER[px[x, y]]
        if ch == '.' or ch not in GROEP[l]: afw.append((x, y, l, ch))
print('afwijkingen van de kaart:', afw)
LIGHT = (236, 236, 230, 255); DARK = (40, 40, 52, 255); Z = 12
KL = {'N': (90, 90, 160), 'F': (60, 60, 90), 'c': (240, 225, 180), 'v': (170, 100, 50), 'k': (120, 120, 120)}
W, Hh = 26 * Z, 15 * Z
o = Image.new('RGBA', (2 * W + 20, Hh + 20), LIGHT); d = ImageDraw.Draw(o)
for (x, y), l in lab.items():
    if l in KL: d.rectangle([(x - 8) * Z, (y - 48) * Z, (x - 7) * Z - 1, (y - 47) * Z - 1], fill=KL[l])
b = Image.new('RGBA', (64, 64), LIGHT); b.alpha_composite(co.convert('RGBA'))
o.paste(b.crop((8, 48, 34, 63)).resize((W, Hh), Image.NEAREST), (W + 20, 0))
for x, y, l, ch in afw:
    for ox in (0, W + 20):
        d.rectangle([ox + (x - 8) * Z, (y - 48) * Z, ox + (x - 7) * Z - 1, (y - 47) * Z - 1], outline=(255, 0, 0), width=2)
d.text((0, Hh + 4), 'kaart (N nabij, F ver, c klauw, v vacht, k kop)', fill=(30, 30, 30)); d.text((W + 20, Hh + 4), 'ronde 6b (rood = afwijking)', fill=(30, 30, 30))
o.save(os.path.join(H, '../kaart_vs_r6b.png'))
# uitsnede onderlaag | 6 | 6b
ond = Image.open(os.path.join(S, 'onderlaag_b1c_256.png')).convert('RGBA')
r6 = Image.open(os.path.join(H, '../../ronde6/coathief.png')).convert('RGBA')
W, Hh = 27 * 8, 16 * 8
v = Image.new('RGBA', (3 * (W + 10), 2 * Hh + 110), LIGHT); dv = ImageDraw.Draw(v)
wb = Image.new('RGBA', (W, Hh), (255, 255, 255, 255)); wb.alpha_composite(ond.crop((32, 192, 140, 256)).resize((W, Hh)))
v.paste(wb, (0, 0)); dv.text((0, Hh + 4), 'onderlaag', fill=(30, 30, 30))
for i, (n, im) in enumerate((('ronde 6', r6), ('ronde 6b', co.convert('RGBA')))):
    for j, bg in enumerate((LIGHT, DARK)):
        bb = Image.new('RGBA', (64, 64), bg); bb.alpha_composite(im)
        v.paste(bb.crop((8, 48, 35, 64)).resize((W, Hh), Image.NEAREST), ((i + 1) * (W + 10), j * (Hh + 10)))
        v.paste(bb, ((i + 1) * (W + 10) + j * 70, 2 * Hh + 30))
    dv.text(((i + 1) * (W + 10), 2 * Hh + 14), n, fill=(30, 30, 30))
v.save(os.path.join(H, '../onderlaag_r6_r6b_voorpoten.png'))
