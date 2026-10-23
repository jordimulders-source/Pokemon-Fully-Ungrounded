#!/usr/bin/env python3
"""Controles ronde 21: pixeldiff met ronde 20 buiten de pootzone (kop, masker, oren, staart, romp),
kaaklijn apart, open randen, formaat, palet, transparency."""
from PIL import Image
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import bouw_ronde21 as B
R = os.path.join(H, '..', '..')
a = Image.open(os.path.join(R, 'ronde20', 'anim_front.png'))
b = Image.open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(R, 'ronde21', 'anim_front.png'))
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
for f in (0, 1):
    up = -1 if f else 0
    kaak = {(x0 + i, y + up) for y, (x0, s) in B.KAAK.items() for i in range(len(s))}
    diff = [(x, y) for y in range(64) for x in range(64)
            if a.getpixel((x, y + 64 * f)) != b.getpixel((x, y + 64 * f))]
    buiten = [p for p in diff if not B.in_zone(*p) and p not in kaak]
    kop = [p for p in diff if p[1] + f < 64 and B.B20.head_mask(p[0], p[1] + f) and p not in kaak]
    staart = [p for p in diff if B.tail_px(p[0], p[1], f)]
    ears = [p for p in diff if 19 + up <= p[1] <= 25 + up and (15 <= p[0] <= 21 or 29 <= p[0] <= 38)]
    kd = [p for p in diff if p in kaak]
    zone = [p for p in diff if B.in_zone(*p) and p not in kaak]
    ob = open_edges(b, f)
    px = [(x, y) for y in range(64) for x in range(64) if b.getpixel((x, y + 64 * f))]
    xs = [p[0] for p in px]; ys = [p[1] for p in px]
    print('frame %d: buiten pootzone (excl. kaak) %d | kop %d | oren %d | staart %d | kaaklijn %d px %s | pootzone gewijzigd %d px'
          % (f + 1, len(buiten), len(kop), len(ears), len(staart), len(kd), sorted(kd), len(zone)))
    print('  open randen %d %s | %d px, box %dx%d (x%d-%d, y%d-%d)' % (len(ob), ob, len(px),
          max(xs)-min(xs)+1, max(ys)-min(ys)+1, min(xs), max(xs), min(ys), max(ys)))
print('palet gelijk:', a.getpalette()[:48] == b.getpalette()[:48], '| transparency', b.info.get('transparency'))
