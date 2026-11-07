"""Vel silhouet ronde 2: onderlaag | foto 1 | ronde 2 4x | ronde 1b 4x | 1x, + Girafarig, Stantler, alpaca (silhouet en kleur, 1x en 4x)."""
import os
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, *['..'] * 6)); L = os.path.join(ROOT, 'docs/concept/sprites/lama')
DARK = (40, 32, 48)
def load(p): return np.array([[c == '#' for c in l.rstrip('\n')] for l in open(p) if l.strip()])
def sil(a, s):
    im = np.full(a.shape + (3,), 255, np.uint8); im[a] = DARK
    return Image.fromarray(im).resize((64 * s, 64 * s), Image.NEAREST)
def spr(p, s):
    im = Image.open(p).convert('RGBA').crop((0, 0, 64, 64)); b = Image.new('RGBA', (64, 64), (236, 236, 236, 255)); b.alpha_composite(im)
    return b.convert('RGB').resize((64 * s, 64 * s), Image.NEAREST)
def mask(p):
    im = Image.open(p); a = np.array(im)[:64, :64]
    return (a != 0) if im.mode == 'P' else (np.array(im.convert('RGBA'))[:64, :64, 3] > 0)
def gf(n):
    d = os.path.join(ROOT, 'graphics/pokemon', n); p = os.path.join(d, 'anim_front_gba.png')
    return p if os.path.exists(p) else os.path.join(d, 'anim_front.png')
r2, r1 = load(os.path.join(HERE, 'ronde2.txt')), load(os.path.join(HERE, 'ronde1b.txt'))
f1 = Image.open(os.path.join(L, 'referenties/foto1_lama_driekwart_POSE.png')).convert('RGB'); f1 = f1.resize((int(f1.width * 256 / f1.height), 256))
und = Image.open(os.path.join(HERE, 'onderlaag_256.png')).convert('RGB')
items = [('onderlaag', und), ('foto 1', f1), ('ronde 2 4x', sil(r2, 4)), ('ronde 1b 4x (vorige)', sil(r1, 4))]
W = sum(i.width for _, i in items) + 64 * 2 + 16 * 7
img = Image.new('RGB', (W, 24 + 256 + 40 + 64 + 8 + 256 + 20), (255, 255, 255)); d = ImageDraw.Draw(img)
x = 12
for t, im in items: img.paste(im, (x, 22)); d.text((x, 6), t, fill=(0, 0, 0)); x += im.width + 16
img.paste(sil(r2, 1), (x, 22)); d.text((x, 6), '1x', fill=(0, 0, 0)); img.paste(sil(r1, 1), (x, 96)); d.text((x, 164), 'ronde 1b 1x', fill=(0, 0, 0))
d.text((x, 184), f'ronde 2: {r2.sum()} px', fill=(0, 0, 0))
y = 22 + 256 + 30; x = 12
refs = [('lama r2', r2, None), ('girafarig', mask(gf('girafarig')), gf('girafarig')), ('stantler', mask(gf('stantler')), gf('stantler')),
        ('alpaca (fase 1)', mask(os.path.join(L, 'referenties/fase1_alpaca.png')), os.path.join(L, 'referenties/fase1_alpaca.png'))]
for t, m, p in refs:
    d.text((x, y - 14), t, fill=(0, 0, 0)); img.paste(sil(m, 1), (x, y))
    if p: img.paste(spr(p, 1), (x + 70, y))
    img.paste(sil(m, 4), (x, y + 72)); x += 256 + 30
img.save(os.path.join(HERE, 'vel_ronde2.png')); print(img.size)
