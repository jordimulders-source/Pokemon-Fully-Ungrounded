"""Olinguito v2 sprite met de hand: delen als (y, x, pixels) in absolute coördinaten, achter naar voor.
Onderlaag/maatvoering: pixel-over van het 3D-poppetje (sprite.py -> raster.txt). '.' = laat staan.
Draaien vanuit de repo-root: python3 docs/concept/ontwerp/olinguito_v2/scripts/teken.py"""
import os
import sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sprite import PAL, checks, dump, save_indexed, sheet, DIR

PARTS = {}


def part(name, rows):
    PARTS[name] = rows


# --- staart (achter) ---
part('staart', [
    (11, 42, 'BBBBK'),
    (12, 40, 'BBhhbbK'),
    (13, 39, 'BhbKKKsbK'),
    (14, 38, 'BhbK'), (14, 45, 'BhbK'),
    (15, 38, 'BhbK'), (15, 45, 'BhbK'),
    (16, 38, 'BhK'), (16, 46, 'BhbK'),
    (17, 38, 'BhK'), (17, 46, 'BhbK'),
    (18, 38, 'BbK'), (18, 46, 'BhbK'),
    (19, 38, 'KbK'), (19, 46, 'BhbK'),
    (20, 39, 'K'), (20, 47, 'BhbK'),
    (21, 47, 'BhbK'), (22, 47, 'BhbK'), (23, 47, 'BhbK'),
    (24, 46, 'BhbbK'), (25, 46, 'BhbbK'),
    (26, 45, 'BhbbK'), (27, 45, 'BhbbK'),
    (28, 44, 'BhbbK'), (29, 44, 'BhbbK'),
])
for n in PARTS:
    for y, x, px in PARTS[n]:
        pass

G = np.full((64, 64), '_')


def draw(name):
    for y, x, px in PARTS[name]:
        for k, ch in enumerate(px):
            if ch != '.':
                G[y, x + k] = '_' if ch == '_' else ch


exec(open(os.path.join(DIR, 'delen.py')).read())

for name in ORDER:
    draw(name)
for r in checks(G):
    print(r)
dump(G, os.path.join(DIR, 'raster.txt'))
save_indexed(G, os.path.join(DIR, 'front.png'))
sheet(G, os.path.join(DIR, 'vel.png'))
