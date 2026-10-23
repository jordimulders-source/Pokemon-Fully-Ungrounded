#!/usr/bin/env python3
"""Variant C9: ronde 21, maar kop + masker + oren letterlijk KOP_DY px omlaag (geknipt en geplakt, niet hertekend).
De kopzone (head_mask van ronde 20, incl. de kaaklijn van ronde 21) wordt uit ronde 21 geknipt en lager geplakt;
de vrijgekomen plek achter de kop wordt romp (NEK, met de hand)."""
from PIL import Image
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
R21 = os.path.join(H, '..', '..')
sys.path.insert(0, os.path.join(R21, 'bron'))
import bouw_ronde21 as B
KOP_DY = 2

def kop_px(x, y, f):
    """Kopzone in frame f (frame 2 staat 1 rij hoger), plus de kaaklijnpixel onder de zone."""
    up = -1 if f else 0
    if y + f < 64 and B.B20.head_mask(x, y + f):
        return True
    return any((x0 + i, yy + up) == (x, y) for yy, (x0, s) in B.KAAK.items() for i in range(len(s)))

NEK = {}   # wordt hieronder ingevuld na bekijken

def bouw():
    src = Image.open(os.path.join(R21, 'anim_front.png'))
    out = Image.new('P', (64, 128), 0)
    out.putpalette(src.getpalette())
    for f in (0, 1):
        g = {(x, y): src.getpixel((x, y + 64 * f)) for y in range(64) for x in range(64)}
        kop = {(x, y): v for (x, y), v in g.items() if kop_px(x, y, f)}
        for p in kop:
            g[p] = 0
        B.paint(g, NEK, -1 if f else 0)
        for (x, y), v in kop.items():
            if v and y + KOP_DY < 64:
                g[(x, y + KOP_DY)] = v
        for (x, y), v in g.items():
            if v:
                out.putpixel((x, y + 64 * f), v)
    return src, out

if __name__ == '__main__':
    src, out = bouw()
    out.save(os.path.join(H, '..', 'anim_front.png'), transparency=0)
    for f in (0, 1):
        n = sum(1 for y in range(64) for x in range(64) if out.getpixel((x, y + 64 * f)))
        print('frame %d: %d px' % (f + 1, n))
