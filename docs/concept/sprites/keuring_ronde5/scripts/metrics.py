"""Meetbare kenmerken per sprite (frame 1)."""
import sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from sheet import *
import numpy as np


def lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def metrics(path, frame=0):
    sp = np.array(load(path, frame))
    a = sp[:, :, 3] > 0
    H, W = a.shape
    ys, xs = np.nonzero(a)
    bw = xs.max() - xs.min() + 1
    bh = ys.max() - ys.min() + 1
    area = a.sum()
    rgb = sp[:, :, :3].astype(int)
    cols = set(tuple(rgb[y, x]) for y, x in zip(ys, xs))
    # outer outline: opaque pixels adjacent to transparent
    edge = []
    inner_edges = 0
    isolated = 0
    for y, x in zip(ys, xs):
        nb = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
        outer = any(not (0 <= j < H and 0 <= i < W) or not a[j, i] for j, i in nb)
        if outer:
            edge.append(lum(rgb[y, x]))
        c = tuple(rgb[y, x])
        diff = 0
        same = 0
        for j, i in nb:
            if 0 <= j < H and 0 <= i < W and a[j, i]:
                if tuple(rgb[j, i]) != c:
                    diff += 1
                else:
                    same += 1
        inner_edges += diff
        if same == 0:
            isolated += 1
    edge = np.array(edge)
    dark_edge = (edge < 60).mean()
    # inner black lines: pixels with lum<45 not on outer edge
    blackinner = 0
    for y, x in zip(ys, xs):
        nb = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
        outer = any(not (0 <= j < H and 0 <= i < W) or not a[j, i] for j, i in nb)
        if not outer and lum(rgb[y, x]) < 45:
            blackinner += 1
    # symmetry: mirror the bbox and compare alpha
    box = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    sym = (box == box[:, ::-1]).mean()
    # colour usage: share of most used colour
    vals, cnt = np.unique(rgb[a].reshape(-1, 3), axis=0, return_counts=True)
    top = cnt.max() / area
    # saturation mean
    hsv = []
    for c in rgb[a]:
        mx, mn = max(c), min(c)
        hsv.append(0 if mx == 0 else (mx - mn) / mx)
    return dict(w=int(bw), h=int(bh), area=int(area), cols=len(cols),
                darkedge=round(float(dark_edge), 2),
                detail=round(inner_edges / area, 2),
                isol=int(isolated), blackin=round(blackinner / area, 3),
                sym=round(float(sym), 2), top=round(float(top), 2),
                sat=round(float(np.mean(hsv)), 2))


if __name__ == '__main__':
    groups = {
        'KANDIDATEN': [('alpaca r4', S + 'alpaca/ronde4/anim_front.png'), ('alpaca r5', S + 'alpaca/ronde5/anim_front.png'),
                       ('olinguito r4', S + 'olinguito/ronde4/anim_front.png'), ('olinguito r5', S + 'olinguito/ronde5/anim_front.png'),
                       ('nachtaap r2', S + 'nachtaap/ronde2/anim_front.png'), ('nachtaap r3', S + 'nachtaap/ronde3/anim_front.png'),
                       ('nachtaap r4', S + 'nachtaap/ronde4/anim_front.png'), ('nachtaap r5', S + 'nachtaap/ronde5/anim_front.png'),
                       ('cuyby A', S + 'cuyby/ronde1/anim_front.png'), ('cuyby B', S + 'cuyby/ronde1/B/anim_front.png'),
                       ('dj rotom', S + 'dj_rotom/ronde1/anim_front.png')],
        'GEN3 (gba)': [(n, G + n + '/anim_front_gba.png') for n in
                       ['treecko', 'torchic', 'mudkip', 'chikorita', 'cyndaquil', 'totodile', 'bulbasaur', 'charmander', 'squirtle',
                        'mareep', 'ponyta', 'growlithe', 'eevee', 'electrike', 'skitty', 'zigzagoon', 'sentret', 'poochyena',
                        'teddiursa', 'sneasel', 'aipom', 'abra', 'natu', 'ralts', 'spoink', 'smoochum', 'rattata', 'whismur']],
        'DS': [(n, G + n + '/anim_front.png') for n in ['chimchar', 'piplup', 'turtwig', 'snivy', 'tepig', 'oshawott', 'pachirisu', 'bidoof', 'lillipup']]
            + [('rotom ' + f, G + 'rotom/' + f + '/anim_front.png') for f in ['heat', 'wash', 'frost', 'fan', 'mow']] + [('rotom', G + 'rotom/anim_front.png')],
    }
    keys = ['w', 'h', 'area', 'cols', 'darkedge', 'detail', 'isol', 'blackin', 'sym', 'top', 'sat']
    print('%-14s' % 'naam' + ''.join('%9s' % k for k in keys))
    for g, items in groups.items():
        print('--', g)
        allm = []
        for n, p in items:
            m = metrics(p)
            allm.append(m)
            print('%-14s' % n + ''.join('%9s' % m[k] for k in keys))
        if g != 'KANDIDATEN':
            print('%-14s' % 'gemiddeld' + ''.join('%9s' % round(float(np.mean([m[k] for m in allm])), 2) for k in keys))
