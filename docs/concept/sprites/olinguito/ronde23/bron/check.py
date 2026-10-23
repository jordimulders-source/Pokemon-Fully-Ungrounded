#!/usr/bin/env python3
"""Controles ronde 23 tegen ronde 22: pixeldiff buiten de zone van de verre voorpoot, kop (masker ronde 20),
open randen, palet, transparency, formaat, rechte lijnen en dikte van de nieuwe poot."""
from PIL import Image
import os, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, '..', '..')
sys.path.insert(0, os.path.join(R, 'ronde21', 'bron'))
import bouw_ronde21 as B
a = Image.open(os.path.join(R, 'ronde22', 'anim_front.png')); b = Image.open(os.path.join(R, 'ronde23', 'anim_front.png'))
def zone(x, y):  # frame-1-coördinaten: vak links van de nabije poot, onder de kin
    return 8 <= x <= 24 and 39 <= y <= 54
OUT = {1, 2, 9}
for f in (0, 1):
    dy = 64 * f - f
    diff = [(x, y) for y in range(64) for x in range(64) if a.getpixel((x, y + 64 * f)) != b.getpixel((x, y + 64 * f))]
    buiten = [p for p in diff if not zone(p[0], p[1] + f)]
    kop = [p for p in diff if p[1] + f < 64 and B.B20.head_mask(p[0], p[1] + f)]
    print('frame %d: gewijzigd %d px | buiten pootzone %d %s | kop-masker %d %s' % (f + 1, len(diff), len(buiten), buiten, len(kop), kop))
print('palet gelijk:', a.getpalette()[:48] == b.getpalette()[:48])
for f in (0, 1):
    ob = []
    for y in range(64):
        for x in range(64):
            v = b.getpixel((x, y + 64 * f))
            if v and v not in OUT:
                for dx, dyy in ((1,0),(-1,0),(0,1),(0,-1)):
                    X, Y = x + dx, y + dyy
                    if not (0 <= X < 64 and 0 <= Y < 64) or b.getpixel((X, Y + 64 * f)) == 0:
                        ob.append((x, y)); break
    px = [(x, y) for y in range(64) for x in range(64) if b.getpixel((x, y + 64 * f))]
    xs = [p[0] for p in px]; ys = [p[1] for p in px]
    print('frame %d: open randen %d %s | %d px, box %dx%d' % (f + 1, len(ob), ob, len(px), max(xs)-min(xs)+1, max(ys)-min(ys)+1))
print('transparency', b.info.get('transparency'), '| mode', b.mode, b.size)
# poot (frame 1): per rij linker- en rechterrand, dikte; rechte lijnen = >= 4 rijen dezelfde x of dezelfde stap
L, Rr = {}, {}
for y in range(39, 50):
    xs = [x for x in range(8, 24) if b.getpixel((x, y)) not in (0, 9, 10, 12)]
    L[y] = min(xs); Rr[y] = max(xs)
    # rechterrand x23 grenst op y40-43 aan de nabije poot (x24): poot loopt erachter door
print('rij: links-rechts (dikte incl. omlijning)')
for y in L: print('  y%d: x%d-%d (%d)' % (y, L[y], Rr[y], Rr[y] - L[y] + 1))
def runs(seq):
    best, cur = 1, 1
    for i in range(1, len(seq)):
        cur = cur + 1 if seq[i] == seq[i-1] else 1; best = max(best, cur)
    return best
def steps(seq):  # langste reeks gelijke stappen (regelmatige diagonaal), in pixels
    d = [seq[i+1] - seq[i] for i in range(len(seq) - 1)]
    best, cur = 1, 1
    for i in range(1, len(d)):
        cur = cur + 1 if d[i] == d[i-1] and d[i] != 0 else 1; best = max(best, cur)
    return best + 1
for naam, d, ys in (('voorrand', L, range(40, 50)), ('achterrand (vrij deel)', Rr, range(44, 50))):
    seq = [d[y] for y in ys]
    print('%s: %s | langste verticale run %d | langste regelmatige diagonaal %d' % (naam, seq, runs(seq), steps(seq)))
print('minste dikte y40-49:', min(Rr[y] - L[y] + 1 for y in range(40, 50)))
