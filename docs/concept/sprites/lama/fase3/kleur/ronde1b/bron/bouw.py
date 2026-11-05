"""Kleur ronde 1 lama fase 3: bouwt ronde1b.txt (64x64 letters) en lama3.png + normal.pal uit de met de hand getypte
segmenten (segmenten.txt: 'y x0 pixels'). Alleen plaatsen en controleren, geen tint- of vormlogica.
Controles: letters geldig, geen dubbele pixels, alpha-diff met het bevroren silhouet (silhouet/ronde2.txt) = 0,
open randen (vulkleur naast transparant), losse pixels (pixel zonder gelijke 4-buur). Draaien: python3 bouw.py"""
import os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
SIL = os.path.join(HERE, '../../../silhouet/ronde2.txt')
LET = '.kHCSdRUBDrmpyGg'
PAL = [(152, 208, 160),  # . transparant
       (40, 28, 32),     # k omlijning schaduwkant, bombín, pupil, vlecht, hoef
       (252, 246, 226),  # H crème licht / hooglicht goud
       (232, 212, 178),  # C crème basis
       (192, 166, 132),  # S crème schaduw / verre poten / lichtje bombín en vlecht
       (138, 88, 56),    # d bruin: omlijningsbasis crème, schaduw goud, staart, knot
       (232, 108, 100),  # R rood licht
       (100, 140, 206),  # U blauw licht
       (58, 92, 164),    # B blauw (worstelpak)
       (32, 50, 96),     # D blauw donker / omlijningsbasis blauw / schaduw groen
       (200, 56, 66),    # r rood
       (120, 34, 66),    # m wijnrood: schaduw rood, cape, voering
       (148, 66, 124),   # p paars (cape)
       (214, 168, 64),   # y goud
       (128, 192, 116),  # G groen licht
       (56, 136, 86)]    # g groen    # g groen
OUTLINE = set('kdDm')   # mogen naast transparant
grid = [['.'] * 64 for _ in range(64)]; seen = {}
for ln, line in enumerate(open(os.path.join(HERE, 'segmenten.txt')), 1):
    if line.startswith('#') or not line.strip(): continue
    y, x0, px = line.split(); y, x0 = int(y), int(x0)
    for i, c in enumerate(px):
        x = x0 + i
        if c not in LET[1:]: sys.exit(f'regel {ln}: onbekende letter {c!r}')
        if (x, y) in seen: sys.exit(f'regel {ln}: pixel x{x} y{y} dubbel (ook regel {seen[(x, y)]})')
        seen[(x, y)] = ln; grid[y][x] = c
open(os.path.join(OUT, 'ronde1b.txt'), 'w').write('\n'.join(''.join(r) for r in grid) + '\n')
G = np.array(grid); A = G != '.'
S = np.array([[c == '#' for c in l.rstrip('\n')] for l in open(SIL) if l.strip()])
print(f'px {int(A.sum())} | silhouet {int(S.sum())} | alpha-diff: +{int((A & ~S).sum())} -{int((S & ~A).sum())}')
for y, x in zip(*np.nonzero(A ^ S)): print(f'   {"+" if A[y, x] else "-"} x{x} y{y}')
openr = []
for y, x in zip(*np.nonzero(A)):
    if G[y, x] in OUTLINE: continue
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        v, u = y + dy, x + dx
        if not (0 <= v < 64 and 0 <= u < 64) or not A[v, u]: openr.append((x, y, G[y, x])); break
print(f'open randen (vulkleur naast transparant): {len(openr)}')
for x, y, c in openr: print(f'   x{x} y{y} {c}')
los = [(x, y, G[y, x]) for y, x in zip(*np.nonzero(A)) if not any(0 <= y+dy < 64 and 0 <= x+dx < 64 and G[y+dy, x+dx] == G[y, x] for dy, dx in ((-1,0),(1,0),(0,-1),(0,1)))]
print(f'losse pixels (geen gelijke 4-buur): {len(los)}')
print('   ' + ' '.join(f'{c}@x{x},y{y}' for x, y, c in los))
idx = np.vectorize(LET.index)(G).astype(np.uint8)
im = Image.fromarray(idx, 'P'); flat = [v for c in PAL for v in c]; im.putpalette(flat + [0] * (768 - len(flat)))
im.save(os.path.join(OUT, 'lama3.png'), transparency=0)
open(os.path.join(OUT, 'normal.pal'), 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join(f'{r} {g} {b}\r\n' for r, g, b in PAL))
used = sorted(set(G[A].ravel())); print('kleuren gebruikt:', len(used), ''.join(used))
