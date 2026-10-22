"""Ondertekening voor ronde 4 (3/4-aanzicht): vormen + schaduw als halve maan rechtsonder,
uitgevoerd als ASCII (base_f1.txt). Daarna is alles met de hand bijgewerkt in f1.txt/f2.txt;
dit script is alleen de eerste stap en wordt door build.py niet gebruikt.
python3 base.py > base_f1.txt
Tekens: . transparant, 1-4 vacht, 5-7 zilver, 8 9 a roze, b c d maan, e wit, X zwart."""
import sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../../../../tools/concept/sprites'))
from layerlib import ellipse, stroke, stroke_var, bezier, spiral, XX, YY


def shift(m, dx, dy):
    out = np.zeros_like(m); H, W = m.shape
    ys = slice(max(0, dy), H + min(0, dy)); yd = slice(max(0, -dy), H + min(0, -dy))
    xs = slice(max(0, dx), W + min(0, dx)); xd = slice(max(0, -dx), W + min(0, -dx))
    out[ys, xs] = m[yd, xd]; return out


tail = bezier((38, 50), (46, 56), (50, 48)) + bezier((50, 48), (53, 42), (52, 38))[1:] + \
    spiral(49.5, 32.5, 6.0, 1.6, 75, 75 - 470, 120)
radii = list(np.linspace(1.9, 1.2, len(tail)))
L = [  # (masker, onderdeel, schaduwverschuiving)
    (stroke_var(tail, radii), 'v', (1, 1)),
    (ellipse(40, 18.5, 2.6, 2.8), 'v', (1, 1)),
    (ellipse(36.5, 51, 5.5, 4.6), 'v', (3, 2)),
    (ellipse(40.5, 56, 4.0, 1.8), 'v', (2, 1)),
    (ellipse(28, 47.5, 9.0, 8.0) | ellipse(27.5, 41, 6.5, 5), 'v', (3, 3)),
    (ellipse(21, 51.5, 6.5, 4.8), 'v', (3, 2)),
    (ellipse(15.5, 56, 5.0, 2.0), 'v', (2, 1)),
    (stroke_var([(34, 40), (35.5, 44.5), (31.5, 47)], [1.8, 1.8, 1.6]), 'v', (1, 1)),
    (ellipse(27, 26.5, 13.5, 11), 'v', (4, 4)),
    (ellipse(14, 21, 2.8, 3.0), 'v', (1, 1)),
    (stroke_var([(20.5, 40), (18.5, 44.5), (22.5, 47)], [1.9, 1.9, 1.7]), 'v', (1, 1)),
    (ellipse(22.5, 33.2, 4.2, 2.7), 'z', (1, 1)),
]
idx = np.full((64, 64), '.', object); zb = np.full((64, 64), -1)
for z, (m, p, k) in enumerate(L):
    zb[m] = z
for z, (m, p, k) in enumerate(L):
    V = zb == z
    base, sh, dk = ('2', '3', '4') if p == 'v' else ('6', '7', '7')
    idx[V] = base
    idx[V & ~shift(m, -k[0], -k[1])] = sh
pz = np.pad(zb, 1, constant_values=-1)
for y in range(64):
    for x in range(64):
        z = zb[y, x]
        if z < 0: continue
        dk = '4' if L[z][1] == 'v' else '7'
        n = {(dx, dy): pz[1 + y + dy, 1 + x + dx] for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))}
        out = [d for d, v in n.items() if v < 0]
        beh = [d for d, v in n.items() if 0 <= v < z]
        if out:
            ox = sum(d[0] for d in out); oy = sum(d[1] for d in out)
            idx[y, x] = dk if (oy < 0 or (ox < 0 and oy <= 0)) else 'X'
        elif beh:
            idx[y, x] = dk
for y in range(64):
    print(''.join(idx[y]))
