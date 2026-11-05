"""Vel silhouet ronde 3: onderlaag | foto 1 | ronde 3 4x | ronde 3 over de onderlaag | 1x;
rij 2: silhouetten op 1x en 2x van Flaaffy, Mareep, Girafarig, Ponyta, alpaca (fase 1) en ronde 3. Schrijft ook ronde3_1x.png.
Draaien: python3 vel.py"""
import os
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, *['..'] * 6)); L = os.path.join(ROOT, 'docs/concept/sprites/lama')
DARK = (40, 32, 48)
def load(p): return np.array([[c == '#' for c in l.rstrip('\n')] for l in open(p) if l.strip()])
def sil(a, s, bg=(255, 255, 255)):
    im = np.full(a.shape + (3,), bg, np.uint8); im[a] = DARK
    return Image.fromarray(im).resize((64 * s, 64 * s), Image.NEAREST)
def mask(p):
    im = Image.open(p); a = np.array(im)[:64, :64]
    return (a != 0) if im.mode == 'P' else (np.array(im.convert('RGBA'))[:64, :64, 3] > 0)
def gf(n): return os.path.join(ROOT, 'graphics/pokemon', n, 'anim_front.png')
r3 = load(os.path.join(HERE, 'ronde3.txt'))
# ronde3_1x.png: P-modus, index 0 transparant, 1 = silhouet
p = Image.fromarray(r3.astype(np.uint8), 'P'); p.putpalette([255, 255, 255, *DARK] + [0] * 762); p.save(os.path.join(HERE, 'ronde3_1x.png'), transparency=0)
f1 = Image.open(os.path.join(L, 'referenties/foto1_lama_driekwart_POSE.png')).convert('RGB'); f1 = f1.resize((int(f1.width * 256 / f1.height), 256))
und = Image.open(os.path.join(HERE, 'onderlaag_256.png')).convert('RGBA'); ub = Image.new('RGBA', und.size, 'white'); ub.alpha_composite(und); und = ub.convert('RGB')
# overlay: onderlaag + silhouet half doorzichtig + 64-raster
ov = und.copy().convert('RGBA'); lay = Image.new('RGBA', ov.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
for y, x in zip(*np.nonzero(r3)): d.rectangle([x * 4, y * 4, x * 4 + 3, y * 4 + 3], fill=(40, 40, 170, 110))
for i in range(0, 65, 8): d.line([(i * 4, 0), (i * 4, 256)], fill=(255, 0, 0, 70)); d.line([(0, i * 4), (256, i * 4)], fill=(255, 0, 0, 70))
ov.alpha_composite(lay); ov = ov.convert('RGB')
items = [('onderlaag (poppetje r3)', und), ('foto 1 (DE lama)', f1), ('ronde 3, 4x', sil(r3, 4)), ('ronde 3 over de onderlaag', ov)]
W = sum(i.width for _, i in items) + 64 + 16 * 6
refs = [('Flaaffy', mask(gf('flaaffy'))), ('Mareep', mask(gf('mareep'))), ('Girafarig', mask(gf('girafarig'))), ('Ponyta', mask(gf('ponyta'))),
        ('alpaca (fase 1)', mask(os.path.join(L, 'referenties/fase1_alpaca.png'))), ('lama ronde 3', r3)]
H2 = 128 + 64 + 40
img = Image.new('RGB', (max(W, 12 + len(refs) * 144), 24 + 256 + 30 + H2 + 10), (255, 255, 255)); d = ImageDraw.Draw(img)
x = 12
for t, im in items: img.paste(im, (x, 22)); d.text((x, 6), t, fill=(0, 0, 0)); x += im.width + 16
img.paste(sil(r3, 1), (x, 22)); d.text((x, 6), '1x', fill=(0, 0, 0)); img.paste(sil(r3, 1, (120, 160, 120)), (x, 96))
d.text((x, 170), f'{int(r3.sum())} px', fill=(0, 0, 0)); d.text((x, 184), 'fase 1: 1019', fill=(0, 0, 0))
y = 22 + 256 + 26; x = 12
for t, m in refs:
    img.paste(sil(m, 2), (x, y + 14)); img.paste(sil(m, 1), (x + 34, y + 14 + 128 + 6))
    d.text((x, y), f'{t} ({int(m.sum())})', fill=(0, 0, 0)); x += 144
img.save(os.path.join(HERE, 'vel_ronde3.png')); print(img.size)
