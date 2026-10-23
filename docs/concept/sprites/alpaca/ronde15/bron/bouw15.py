"""Ronde 15: ronde 13 pixel voor pixel + B (vlechtpuntjes, iets groter, met knoopje) + C (aguayo-band,
iets breder, twee rijtjes) + het verre oog als smalle zwarte streep op de neusbrug
+ reparatie linkervoorpoot (smaller, los van de verre voorpoot).
Gebruik (vanuit de repo-root): python3 docs/concept/sprites/alpaca/ronde15/bron/bouw15.py
Leest bron/palet.txt, bron/r13_f1.txt, bron/r13_f2.txt (kopie van ronde 13) en de overlay hieronder;
schrijft anim_front.png + normal.pal + bron/r15_f1.txt/r15_f2.txt en controleert open randen.
Overlay: rijen 'y x pixels' (absolute coordinaten frame 1, '.' = laten staan). In frame 2 zakt de kop
(rij <= 22) 1 px; de hals (rij >= 24) blijft staan, net als in ronde 13.
"""
import os
from PIL import Image

D = 'docs/concept/sprites/alpaca/ronde15'
B = os.path.join(D, 'bron')

# Verre oog (x19-20, y14-17, 7 px zwart) wordt een smalle streep langs de neusbrug: eerst wol (w)
# op de oude plek, dan een 1-px lijn die de neusbrug volgt (curve 2-1-2: verticaal, neutraal, horizontaal).
# Proeven S1-S8 lazen als dichtgeknepen oog/knipoog zolang de streep op de oogplek bleef; S7 (1 px
# naar de omtrek toe en doorlopend tot boven op de snuit) leest als neusbrug.
STREEP = [
    (14, 19, 'ww'), (15, 19, 'ww'), (16, 19, 'ww'), (17, 20, 'w'),
    # neusstreep weggehaald op verzoek van Jordi (ronde 15b): alleen wol op de oude oogplek
]
VLECHT = [
    # verre oor: kwastje x15-16, y9-13, knoopje rode wol op y12, onderkant op y14
    (9, 16, 'V'),
    (10, 15, 'VW'),
    (11, 15, 'Vw'),
    (12, 15, 'Sr'),
    (13, 15, 'Vw'),
    (14, 15, 'K'),
    # nabije oor: plukje x34 y10-11 (ronde 14), daarna een strengetje x35 y12-14 tegen de kop
    (10, 33, 'VwK'),
    (11, 34, 'wK'),
    (12, 35, 'vK'),
    (13, 35, 'rK'),
    (14, 35, 'vK'),
    (15, 35, 'K'),
]
# Reparatie linkervoorpoot (Jordi, 23 okt: "zit vast aan een ander en is breder"): de nabije voorpoot
# x17-24 y41-43 wordt 4 px breed (V W v K) zoals de verre voorpoot, schuin 1 px per rij naar de manchet,
# rij 43 1 px breder (VWwvK) zoals de verre poot uitloopt in zijn manchet. '_' = transparant maken;
# daardoor ligt 3 kolommen lucht tussen de poten. Vuist en manchet (y44-54) onveranderd.
POOT = [
    (41, 19, 'VWvK_'),
    (42, 18, 'VWvK___'),
    (43, 17, 'VWwvK___'),
]
# Reparatie na keuring (KEURING.md, nodig 1 en 2). 1: open randen dicht met K, silhouet gelijk: buik tussen
# de voorpoten, kaak (frame 2 zakt mee), kont-hoek (nieuwe pixel) en de onderkant van de staart, die zo
# vastzit aan de kont. 2: de verre achtervoet krijgt een eigen afgerond hoefje (x38-41) met een kolom
# lucht op x37 vanaf y44, los van de nabije achterpoot.
KEURING = [
    (22, 19, 'K'),
    (30, 43, 'KKK'),
    (37, 42, 'K'),
    (39, 25, 'KK'),
    (46, 37, '_K'),
    (47, 37, '__KK'),
]
AGUAYO = [
    (26, 23, 'MYTYTs'),
    (27, 23, 'vMMMs'),
    (28, 24, 'vvv'),
]

PAL, RAND = [], set()
for r in open(os.path.join(B, 'palet.txt'), encoding='utf-8'):
    p = r.split('#')[0].split()
    if p:
        PAL.append((p[0], tuple(int(v) for v in p[1:4])))
        if 'omlijning' in p[4:] or 'zwart' in p[4:]:
            RAND.add(p[0])
IDX = {c: i for i, (c, _) in enumerate(PAL)}


def lees(n):
    return [list(r) for r in open(os.path.join(B, n)).read().split()]


def toepas(g, hints, f2):
    g = [r[:] for r in g]
    for y, x, px in hints:
        if f2 and y <= 22:
            y += 1
        for i, c in enumerate(px):
            if c != '.':
                g[y][x + i] = '.' if c == '_' else c
    return g


def beeld(g):
    im = Image.new('P', (64, 64))
    flat = [v for _, rgb in PAL for v in rgb]
    im.putpalette(flat + [0] * (48 - len(flat)))
    im.putdata([IDX[c] for r in g for c in r])
    return im


SCHADUW = {'v', 'u'}  # vachtschaduw: als rand alleen aan de lichtkant (boven/links), niet aan de schaduwkant


def open_randen(g):
    def leeg(u, v):
        return not (0 <= u < 64 and 0 <= v < 64) or g[v][u] == '.'
    lek = []
    for y in range(64):
        for x in range(64):
            c = g[y][x]
            if c == '.':
                continue
            if c in SCHADUW:
                buren = ((x + 1, y), (x, y + 1))  # schaduwkant: rechts en onder hoort K
            elif c not in RAND:
                buren = ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
            else:
                continue
            if any(leeg(u, v) for u, v in buren):
                lek.append((x, y, c))
    return lek


def bouw(hints, uit):
    f1, f2 = lees('r13_f1.txt'), lees('r13_f2.txt')
    a, b = toepas(f1, hints, 0), toepas(f2, hints, 1)
    gewijzigd = sum(a[y][x] != f1[y][x] for y in range(64) for x in range(64))
    opp = sum(c != '.' for r in a for c in r)
    print('%s: %d px gewijzigd, oppervlak %d, open randen f1 %s f2 %s'
          % (uit, gewijzigd, opp, open_randen(a) or 'geen', open_randen(b) or 'geen'))
    im = Image.new('P', (64, 128))
    im.putpalette(beeld(a).getpalette())
    im.paste(beeld(a), (0, 0)); im.paste(beeld(b), (0, 64))
    return im, a, b


im, a, b = bouw(VLECHT + AGUAYO + STREEP + POOT + KEURING, 'ronde15')
im.save(os.path.join(D, 'anim_front.png'), transparency=0)
with open(os.path.join(D, 'normal.pal'), 'w', newline='\r\n') as fh:
    fh.write('JASC-PAL\n0100\n16\n')
    for i in range(16):
        fh.write('%d %d %d\n' % PAL[i][1])
for n, g in (('r15_f1.txt', a), ('r15_f2.txt', b)):
    with open(os.path.join(B, n), 'w') as fh:
        fh.write('\n'.join(''.join(r) for r in g) + '\n')
