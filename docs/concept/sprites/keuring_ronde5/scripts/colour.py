"""Kleurstructuur: aandeel dominante kleurfamilie, lichtheidscontrast, verzadiging."""
import sys, colorsys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from sheet import *
import numpy as np

def stats(p):
    sp = np.array(load(p, 0))
    a = sp[:, :, 3] > 0
    rgb = sp[:, :, :3][a].astype(float) / 255
    hsv = np.array([colorsys.rgb_to_hsv(*c) for c in rgb])
    L = 0.299 * rgb[:, 0] + 0.587 * rgb[:, 1] + 0.114 * rgb[:, 2]
    col = (hsv[:, 1] > 0.12) & (hsv[:, 2] > 0.2)
    h = hsv[col, 0]
    hist, _ = np.histogram(h, bins=24, range=(0, 1))
    k = hist.argmax()
    near = np.minimum(np.abs(h - (k + 0.5) / 24), 1 - np.abs(h - (k + 0.5) / 24)) < 30 / 360
    dom = near.sum() / len(L)
    return dict(dominant=round(float(dom), 2), Lstd=round(float(L.std()), 3), Lmean=round(float(L.mean()), 2),
                sat_col=round(float(hsv[col, 1].mean()), 2), neutral=round(float((~col).mean()), 2))

items = [('alpaca r4', S + 'alpaca/ronde4/anim_front.png'), ('alpaca r5', S + 'alpaca/ronde5/anim_front.png'),
         ('olinguito r4', S + 'olinguito/ronde4/anim_front.png'), ('olinguito r5', S + 'olinguito/ronde5/anim_front.png'),
         ('nachtaap r3', S + 'nachtaap/ronde3/anim_front.png'), ('nachtaap r5', S + 'nachtaap/ronde5/anim_front.png'),
         ('cuyby A', S + 'cuyby/ronde1/anim_front.png'), ('dj rotom', S + 'dj_rotom/ronde1/anim_front.png')]
items += [(n, G + n + '/anim_front_gba.png') for n in ['treecko', 'torchic', 'mudkip', 'chikorita', 'cyndaquil', 'totodile', 'mareep', 'aipom', 'abra', 'sneasel', 'poochyena', 'teddiursa', 'zigzagoon', 'sentret', 'skitty', 'rattata']]
items += [('rotom ' + f, G + 'rotom/' + f + '/anim_front.png') for f in ['heat', 'wash', 'frost']]
print('%-14s dominant  Lstd  Lmean sat_col neutral' % 'naam')
for n, p in items:
    s = stats(p)
    print('%-14s %6s %6s %6s %6s %6s' % (n, s['dominant'], s['Lstd'], s['Lmean'], s['sat_col'], s['neutral']))
