#!/usr/bin/env python3
"""Controles ronde 20: open randen, pixeldiff van bevroren delen (kop, oren, staart), formaat."""
from PIL import Image
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
from bouw_ronde20 import head_mask, tail_mask, TAIL_DX, MASKER
R = os.path.join(H, '..', '..')
a = Image.open(os.path.join(R, 'stap1b_kop', 'anim_front.png'))
b = Image.open(os.path.join(R, 'ronde20', 'anim_front.png'))
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
mask_px = set()
for y, (x0, s) in MASKER.items():
    for i in range(len(s)):
        mask_px.add((x0 + i, y))
for f in (0, 1):
    ob, oa = open_edges(b, f), open_edges(a, f)
    print('frame %d: open randen ronde20 %d (stap1b %d): %s' % (f + 1, len(ob), len(oa), ob))
    # kop: zelfde frame, zelfde plek; alleen de maskercorrectie mag verschillen
    hd = [(x, y) for y in range(64) for x in range(64)
          if y + f < 64 and head_mask(x, y + f) and (x, y + f) not in mask_px
          and a.getpixel((x, y + 64 * f)) != b.getpixel((x, y + 64 * f))]
    md = [(x, y) for (x, y) in mask_px if a.getpixel((x, y - f + 64 * f)) != b.getpixel((x, y - f + 64 * f))]
    # oren apart (x15-21 en x29-38, y19-25 in frame 1)
    ears = [(x, y) for y in range(19, 26) for x in list(range(15, 22)) + list(range(29, 39))
            if a.getpixel((x, y - f + 64 * f)) != b.getpixel((x, y - f + 64 * f))]
    td = [(x, y) for y in range(64) for x in range(64)
          if y - f >= 0 and tail_mask(x, y - f) and a.getpixel((x, y + 64 * f)) != b.getpixel((x + TAIL_DX, y + 64 * f))]
    print('  kop (zonder maskerzone) pixeldiff = %d; oren = %d; staart (na dx %d) = %d; maskerzone gewijzigd %d px'
          % (len(hd), len(ears), TAIL_DX, len(td), len(md)))
    px = [(x, y) for y in range(64) for x in range(64) if b.getpixel((x, y + 64 * f))]
    xs = [p[0] for p in px]; ys = [p[1] for p in px]
    print('  %d px, box %dx%d (x%d-%d, y%d-%d)' % (len(px), max(xs)-min(xs)+1, max(ys)-min(ys)+1, min(xs), max(xs), min(ys), max(ys)))
light = lambda im: sum(1 for y in range(64) for x in range(64) if head_mask(x, y) and im.getpixel((x, y)) in (6, 7, 8))
print('creme/beige in kop: stap1b %d, ronde20 %d' % (light(a), light(b)))
print('palet gelijk:', a.getpalette()[:48] == b.getpalette()[:48], '| transparency', b.info.get('transparency'))
