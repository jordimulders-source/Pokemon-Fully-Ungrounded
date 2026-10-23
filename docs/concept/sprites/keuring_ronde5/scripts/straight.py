"""Hoekigheid van de buitencontour: aandeel randpixels in rechte runs van >= 5 px."""
import sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from sheet import *
import numpy as np


def straight(p, run=5):
    a = np.array(load(p, 0))[:, :, 3] > 0
    H, W = a.shape
    pad = np.pad(a, 1)
    edge = a & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    inrun = np.zeros_like(edge)
    for arr, T in ((edge, False), (edge.T, True)):
        m = np.zeros_like(arr)
        for i in range(arr.shape[0]):
            j = 0
            while j < arr.shape[1]:
                if arr[i, j]:
                    k = j
                    while k < arr.shape[1] and arr[i, k]:
                        k += 1
                    if k - j >= run:
                        m[i, j:k] = True
                    j = k
                else:
                    j += 1
        inrun |= m.T if T else m
    return round(float(inrun.sum() / edge.sum()), 2)


items = [('alpaca r4', S + 'alpaca/ronde4/anim_front.png'), ('alpaca r5', S + 'alpaca/ronde5/anim_front.png'),
         ('olinguito r4', S + 'olinguito/ronde4/anim_front.png'), ('olinguito r5', S + 'olinguito/ronde5/anim_front.png'),
         ('nachtaap r3', S + 'nachtaap/ronde3/anim_front.png'), ('nachtaap r4', S + 'nachtaap/ronde4/anim_front.png'), ('nachtaap r5', S + 'nachtaap/ronde5/anim_front.png'),
         ('cuyby A', S + 'cuyby/ronde1/anim_front.png'), ('dj rotom', S + 'dj_rotom/ronde1/anim_front.png')]
refs = [(n, G + n + '/anim_front_gba.png') for n in ['treecko', 'torchic', 'mudkip', 'chikorita', 'cyndaquil', 'totodile', 'bulbasaur', 'charmander', 'squirtle', 'mareep', 'ponyta', 'growlithe', 'zigzagoon', 'teddiursa', 'aipom', 'skitty', 'sentret']]
rot = [('rotom ' + f, G + 'rotom/' + f + '/anim_front.png') for f in ['heat', 'wash', 'frost', 'fan', 'mow']]
for n, p in items:
    print('%-14s %s' % (n, straight(p)))
v = [straight(p) for _, p in refs]
print('Gen3 gemiddeld', round(sum(v) / len(v), 2), 'min', min(v), 'max', max(v))
v = [straight(p) for _, p in rot]
print('Rotom-vormen', v)
