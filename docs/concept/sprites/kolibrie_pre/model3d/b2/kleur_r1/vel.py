"""Vel: kleur r1 1x en 4x op licht en donker, naast onderlaag, r10, Taillow, Starly."""
import os, numpy as np
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(D, *['..'] * 7))
def rgba(p, top=True):
    im = Image.open(p).convert('RGBA')
    if im.size[1] == 128 and top: im = im.crop((0, 0, 64, 64))
    return im
def mon(n):
    im = Image.open(os.path.join(R, 'graphics', 'pokemon', n, 'anim_front.png')).crop((0, 0, 64, 64))
    return im.convert('RGBA') if im.info.get('transparency') is not None else _idx0(im)
def _idx0(im):
    a = np.array(im); rgb = np.array(im.convert('RGBA')); rgb[a == 0, 3] = 0; return Image.fromarray(rgb)
LICHT, DONKER = (236, 236, 240), (48, 52, 64)
def op(im, s, bg):
    im = im.resize((64 * s, 64 * s), Image.NEAREST); b = Image.new('RGBA', im.size, bg + (255,)); b.alpha_composite(im); return b.convert('RGB')
ik = rgba(os.path.join(D, 'kolibrie_pre.png'))
items = [('kleur r1', ik), ('onderlaag B2', Image.open(os.path.join(D, '..', 'onderlaag_64.png')).convert('RGBA')),
         ('r10 (afgekeurd)', rgba(os.path.join(D, '..', '..', '..', 'maker', 'kleur_r10', 'kolibrie_pre.png'))),
         ('Taillow', mon('taillow')), ('Starly', mon('starly'))]
W = 5 * 270 + 10; H = 30 + 256 + 10 + 256 + 40 + 64 * 2 + 30
vel = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(vel)
for k, (t, im) in enumerate(items):
    x = 10 + k * 270
    d.text((x, 8), t + ' 4x', fill=(0, 0, 0))
    vel.paste(op(im, 4, LICHT), (x, 30)); vel.paste(op(im, 4, DONKER), (x, 30 + 266))
    y1 = 30 + 532 + 20
    d.text((x, y1 - 14), '1x licht / donker', fill=(0, 0, 0))
    vel.paste(op(im, 1, LICHT), (x, y1)); vel.paste(op(im, 1, DONKER), (x + 74, y1))
vel.save(os.path.join(D, 'vel.png')); print(vel.size)
