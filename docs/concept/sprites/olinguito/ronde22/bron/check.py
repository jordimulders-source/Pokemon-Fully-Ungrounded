#!/usr/bin/env python3
"""Controles ronde 22: pixeldiff tegen ronde 21b (basis) en ronde 20 (goedgekeurde kop) buiten de pootzone,
kop/oren/staart/kaak apart, open randen, formaat, palet, transparency.
Pootzone = y >= 40 (frame 2: >= 39), 12 <= x <= 48, zonder staartpixels (zelfde zone als ronde 21/21b)."""
from PIL import Image
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(H, '..', '..')
sys.path.insert(0, os.path.join(R, 'ronde21', 'bron'))
import bouw_ronde21 as B
b = Image.open(os.path.join(R, 'ronde22', 'anim_front.png'))
r20 = Image.open(os.path.join(R, 'ronde20', 'anim_front.png'))   # echte staartpixels = staartmasker en niet leeg in ronde 20
OUT = {1, 2, 9}
def open_edges(im, f):
    res = []
    for y in range(64):
        for x in range(64):
            v = im.getpixel((x, y + 64 * f))
            if v and v not in OUT:
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    X, Y = x + dx, y + dy
                    if not (0 <= X < 64 and 0 <= Y < 64) or im.getpixel((X, Y + 64 * f)) == 0:
                        res.append((x, y)); break
    return res
for naam in ('ronde21b', 'ronde20'):
    a = Image.open(os.path.join(R, naam, 'anim_front.png'))
    print('== tegen', naam)
    for f in (0, 1):
        up = -1 if f else 0
        kaak = {(x0 + i, y + up) for y, (x0, s) in B.KAAK.items() for i in range(len(s))}
        diff = [(x, y) for y in range(64) for x in range(64)
                if a.getpixel((x, y + 64 * f)) != b.getpixel((x, y + 64 * f))]
        buiten = [p for p in diff if not B.in_zone(p[0], p[1], f) and p not in kaak]
        kop = [p for p in diff if p[1] + f < 64 and B.B20.head_mask(p[0], p[1] + f) and p not in kaak]
        staart = [p for p in diff if B.tail_px(p[0], p[1], f) and r20.getpixel((p[0], p[1] + 64 * f))]
        ears = [p for p in diff if 19 + up <= p[1] <= 25 + up and (15 <= p[0] <= 21 or 29 <= p[0] <= 38)]
        kd = [p for p in diff if p in kaak]
        zone = [p for p in diff if B.in_zone(p[0], p[1], f) and p not in kaak]
        print('frame %d: buiten pootzone (excl. kaak) %d | kop %d | oren %d | staart %d | kaaklijn %d | pootzone gewijzigd %d px'
              % (f + 1, len(buiten), len(kop), len(ears), len(staart), len(kd), len(zone)))
    print('palet gelijk:', a.getpalette()[:48] == b.getpalette()[:48])
for f in (0, 1):
    ob = open_edges(b, f)
    px = [(x, y) for y in range(64) for x in range(64) if b.getpixel((x, y + 64 * f))]
    xs = [p[0] for p in px]; ys = [p[1] for p in px]
    print('frame %d: open randen %d %s | %d px, box %dx%d (x%d-%d, y%d-%d)' % (f + 1, len(ob), ob, len(px),
          max(xs)-min(xs)+1, max(ys)-min(ys)+1, min(xs), max(xs), min(ys), max(ys)))
print('transparency', b.info.get('transparency'), '| mode', b.mode, b.size)
