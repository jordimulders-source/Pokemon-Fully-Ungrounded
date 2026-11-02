"""Vel silhouet: onderlaag | silhouet 4x | silhouet over de onderlaag | 1x, + echte Gen 3-silhouetten (1x en 4x).
Draaien vanuit de repo-root: python3 docs/concept/sprites/lama/fase2/silhouet/vel.py [ronde1]"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../../../../..'))
stem = sys.argv[1] if len(sys.argv) > 1 else 'ronde1'
DARK = (40, 32, 48)
REFS = ['mightyena', 'girafarig', 'rapidash', 'stantler', 'absol']

def load(p):
    return np.array([[c == '#' for c in l.rstrip('\n')] for l in open(p) if l.strip()], dtype=bool)

def sil_img(sil, s, bg=(255, 255, 255)):
    a = np.zeros(sil.shape + (3,), np.uint8); a[:] = bg; a[sil] = DARK
    return Image.fromarray(a).resize((64 * s, 64 * s), Image.NEAREST)

def ref_sil(name):
    d = os.path.join(ROOT, 'graphics/pokemon', name)
    p = os.path.join(d, 'anim_front_gba.png') if os.path.exists(os.path.join(d, 'anim_front_gba.png')) else os.path.join(d, 'anim_front.png')
    im = Image.open(p); a = np.array(im)[:64]
    return a != 0

sil = load(os.path.join(HERE, stem + '.txt'))
under = Image.open(os.path.join(HERE, 'onderlaag_256.png')).convert('RGB')
over = under.copy(); d = ImageDraw.Draw(over, 'RGBA')
for y, x in zip(*np.nonzero(sil)):
    d.rectangle([x * 4, y * 4, x * 4 + 3, y * 4 + 3], fill=(40, 32, 160, 110))
# rand van het silhouet in rood voor de pose-check
edge = sil & ~(np.roll(sil, 1, 0) & np.roll(sil, -1, 0) & np.roll(sil, 1, 1) & np.roll(sil, -1, 1))
for y, x in zip(*np.nonzero(edge)):
    d.rectangle([x * 4, y * 4, x * 4 + 3, y * 4 + 3], outline=(220, 0, 0, 200))
pad = 12
W = 4 * 256 + 64 + pad * 6
H1 = 256 + 40
H2 = 64 + 4 + 256 + 40
img = Image.new('RGB', (max(W, len(REFS) * (256 + pad) + 256 + pad * 2), H1 + H2 + pad), (255, 255, 255))
dr = ImageDraw.Draw(img)
x = pad
for lab, im in [('onderlaag', under), (stem + ' 4x', sil_img(sil, 4)), ('over onderlaag', over)]:
    img.paste(im, (x, 24)); dr.text((x, 6), lab, fill=(0, 0, 0)); x += 256 + pad
img.paste(sil_img(sil, 1), (x, 24)); dr.text((x, 6), '1x', fill=(0, 0, 0))
ys, xs = np.nonzero(sil)
dr.text((x, 100), f'{sil.sum()} px\nbox {xs.max()-xs.min()+1}x{ys.max()-ys.min()+1}', fill=(0, 0, 0))
# rij 2: lama + referenties, 1x boven en 4x onder
y0 = H1 + pad; x = pad
for lab, s in [('lama', sil)] + [(n, ref_sil(n)) for n in REFS]:
    ys, xs = np.nonzero(s)
    dr.text((x, y0), f'{lab} {s.sum()}px', fill=(0, 0, 0))
    img.paste(sil_img(s, 1), (x, y0 + 14)); img.paste(sil_img(s, 4), (x, y0 + 14 + 68))
    x += 256 + pad
img.save(os.path.join(HERE, 'vel_' + stem + '.png'))
print('vel_' + stem + '.png', img.size)
