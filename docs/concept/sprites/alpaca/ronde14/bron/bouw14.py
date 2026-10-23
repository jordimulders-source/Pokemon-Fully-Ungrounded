"""Ronde 14: ronde 13 pixel voor pixel + één evolutiehint per variant (A, B, C) en D = alle drie.
Gebruik (vanuit de repo-root): python3 docs/concept/sprites/alpaca/ronde14/bron/bouw14.py
Leest bron/palet.txt, bron/r13_f1.txt, bron/r13_f2.txt (kopie van de ronde-13-rasters) en de hints
hieronder; schrijft variant_X/anim_front.png + normal.pal + bron/variant_X_f1.txt en controleert
open randen en het aantal gewijzigde pixels.
Hints: rijen 'y x pixels' (absolute coördinaten frame 1, '.' = laten staan). In frame 2 zakt de kop
(rij <= 22) 1 px; de hals (rij >= 24) blijft staan, net als in ronde 13.
"""
import os
from PIL import Image

D = 'docs/concept/sprites/alpaca/ronde14'
B = os.path.join(D, 'bron')

HINTS = {
    # A: bombín-zaadje. Smal randje onder de pompon (rij 9), oudroze met mauve aan de uiteinden,
    # zodat de bol van de pompon op een 'rand' lijkt te staan. Silhouet ongewijzigd.
    'A': [
        (9, 21, 'uvvvvvvu'),
    ],
    # B: vlechtpuntjes. Onder elk oor hangt een smal wolplukje langs de kop, met een eigen
    # omlijning, zodat het als los kwastje leest en niet als bolle wang. De kopomtrek blijft staan.
    'B': [
        # verre oor (links): plukje op x15-16, rij 9-12, tegen de kopomtrek x17
        (9, 16, 'V'),
        (10, 15, 'VW'),
        (11, 15, 'Vw'),
        (12, 16, 'K'),
        # nabije oor (rechts): plukje op x33-35, rij 10-13, tegen de kopomtrek
        (10, 33, 'VwK'),
        (11, 34, 'wK'),
        (12, 35, 'K'),
    ],
    # C: aguayo-streepje in de halswol (zelfde weefsel als de manchet: magenta, geel, turquoise),
    # 4 px in de hals; het rechter pixel in de schaduw-magenta (s) zodat het om de hals draait.
    # Eronder een rij oudroze (v): het streepje ligt in de wol en werpt schaduw, geen sticker.
    'C': [
        (26, 24, 'MYTs'),
        (27, 24, 'vvv'),
    ],
}
HINTS['D'] = HINTS['A'] + HINTS['B'] + HINTS['C']

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
                g[y][x + i] = c
    return g


def beeld(g):
    im = Image.new('P', (64, 64))
    flat = [v for _, rgb in PAL for v in rgb]
    im.putpalette(flat + [0] * (48 - len(flat)))
    im.putdata([IDX[c] for r in g for c in r])
    return im


def open_randen(g):
    lek = []
    for y in range(64):
        for x in range(64):
            if g[y][x] != '.' and g[y][x] not in RAND and any(
                    not (0 <= u < 64 and 0 <= v < 64) or g[v][u] == '.'
                    for u, v in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))):
                lek.append((x, y, g[y][x]))
    return lek


f1, f2 = lees('r13_f1.txt'), lees('r13_f2.txt')
for naam, hints in HINTS.items():
    a, b = toepas(f1, hints, 0), toepas(f2, hints, 1)
    gewijzigd = sum(a[y][x] != f1[y][x] for y in range(64) for x in range(64))
    opp = sum(c != '.' for r in a for c in r)
    print('variant %s: %d px gewijzigd, oppervlak %d, open randen f1 %s f2 %s'
          % (naam, gewijzigd, opp, open_randen(a) or 'geen', open_randen(b) or 'geen'))
    uit = os.path.join(D, 'variant_' + naam)
    os.makedirs(uit, exist_ok=True)
    im = Image.new('P', (64, 128))
    im.putpalette(beeld(a).getpalette())
    im.paste(beeld(a), (0, 0)); im.paste(beeld(b), (0, 64))
    im.save(os.path.join(uit, 'anim_front.png'), transparency=0)
    with open(os.path.join(uit, 'normal.pal'), 'w', newline='\r\n') as fh:
        fh.write('JASC-PAL\n0100\n16\n')
        for i in range(16):
            fh.write('%d %d %d\n' % PAL[i][1])
    with open(os.path.join(B, 'variant_%s_f1.txt' % naam), 'w') as fh:
        fh.write('\n'.join(''.join(r) for r in a) + '\n')
