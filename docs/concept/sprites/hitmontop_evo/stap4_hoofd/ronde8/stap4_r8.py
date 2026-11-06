"""Stap 4 hoofd, ronde 8 (6 nov). Bron: Hitmontops OVERWORLD-sprite (frame 1): de kop staat daar rechtop en van voren,
zoals referenties/hitmontop_3d.webp (koepel, stekel bovenop, flappen opzij, V boven de ogen).
 1 uitsnede (regel van stap3b KOP_OW), OW-palet -> frontpalet, buitenrand zwart
 2 groter met de hand: kolommen 7, 9, 15, 21, 23 en rijen 13-15 verdubbeld (vlakke delen) -> 24 px breed
 3 glad + frontsprite-gezicht: trapjes van het verdubbelen weg (koepelomtrek), ogen = Hitmontops frontsprite-oog 1:1
   (zwart rondje, wit puntje), mond = Hitmontops streepje; licht linksboven, sikkel rechtsonder
 4 Jordi's recept: V naar achteren (flappen naar achteren gekamd, voorhoofd vrij) -> 5 knot = Hitmontops hand 1:1 +
   polsband, band tussen knot en kop -> 6 stekel kleiner -> 7 licht tegen de klok in, met de hand nagewerkt.
Varianten: 1 = knot achter op de kruin (linksboven achter de koepel), 2 = knot achterop/opzij (achter het oor).
Draaien vanuit de repo-root: python3 docs/concept/sprites/hitmontop_evo/stap4_hoofd/ronde8/stap4_r8.py"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from hulp import *
from ow import stap1, dubbel
from PIL import Image, ImageDraw

OX, OY = 22, 10          # plek van het hoofd (x0,y0 van het raster hieronder) in het 64-vak
OOG = [".ff.", "f1ff", "ffff", ".ff."]       # Hitmontops frontsprite-oog (anim_front), pixel voor pixel
# omtrek per rij (links, rechts) van de koepel na het gladmaken (stap 3); y0 = bovenkant koepel (onder de stekel)
OMTREK = {0: (5, 16), 1: (3, 18), 2: (2, 19), 3: (1, 20), 4: (1, 20), 5: (0, 21), 6: (0, 21), 7: (0, 21), 8: (0, 21),
          9: (0, 21), 10: (0, 21), 11: (0, 21), 12: (0, 21), 13: (1, 20), 14: (1, 20), 15: (2, 19), 16: (3, 18), 17: (5, 16)}
STEKEL_GROOT = [(10, ['ff']), (9, ['f34f']), (9, ['f34f']), (8, ['f3234f']), (8, ['f3334f']), (7, ['f333344f'])]
STEKEL_KLEIN = [(10, ['ff']), (9, ['f34f']), (8, ['f3234f'])]


def koepel(stekel):
    d = {}
    for y, (a, b) in OMTREK.items():
        for x in range(a, b + 1): d[(x, y)] = 3
    for y, (a, b) in OMTREK.items():          # omtrek: zwart, ook boven/onder
        for x in range(a, b + 1):
            if (x, y - 1) not in d or (x, y + 1) not in d or x in (a, b): d[(x, y)] = 15
    # licht linksboven (sikkel), schaduw rechtsonder
    for p in [(6, 1), (7, 1), (8, 1), (9, 1), (4, 2), (5, 2), (6, 2), (7, 2), (3, 3), (4, 3), (5, 3), (2, 4), (3, 4), (2, 5)]: d[p] = 2
    for y in range(4, 15): d[(20 if y < 13 else 19, y)] = 4 if d[(20 if y < 13 else 19, y)] != 15 else 15
    for (x, y) in list(d):
        if d[(x, y)] == 3 and ((x >= 19 and 6 <= y <= 14) or (y == 16 and x >= 5) or (y == 15 and x >= 14) or (x == 18 and 12 <= y <= 15)):
            d[(x, y)] = 4
    for p in [(13, 16), (14, 16), (15, 16), (16, 16), (17, 15), (18, 15)]: d[p] = 5
    # stekel op de koepel (rij -n boven y0); voet loopt zonder lijn in de koepel over
    n = len(stekel)
    for j, (x0, r) in enumerate(stekel):
        y = j - n + 1 if False else j - n
        for i, c in enumerate(r[0]): d[(x0 + i, y + 1)] = CH.index(c)
    for x in range(8, 14): d[(x, 0)] = 3 if x < 13 else 4
    return d


def gezicht(d, v_y=None):
    for (ex, ey) in ((5, 8), (13, 8)):
        for j, r in enumerate(OOG):
            for i, c in enumerate(r):
                if c != '.': d[(ex + i, ey + j)] = CH.index(c)
    for x in range(8, 14): d[(x, 14)] = 5                      # mondstreepje
    return d


# V (voorrand van de flappen): in Hitmontop vlak boven de ogen met de punt ertussen; hier per rij (x, kleur)
V_OUD = {(10, 7): 15, (11, 7): 15, (9, 6): 5, (12, 6): 5, (8, 6): 5, (13, 6): 5, (7, 7): 5, (14, 7): 5,
         (6, 7): 5, (15, 7): 5, (5, 7): 4, (16, 7): 4}                             # flapranden boven de ogen
V_NIEUW = {(10, 5): 15, (11, 5): 15, (9, 4): 5, (12, 4): 5, (8, 3): 5, (13, 3): 5, (7, 3): 5, (14, 3): 5,
           (6, 2): 4, (15, 2): 4}                                                  # naar achteren getrokken


def hoofd(stap, var=1):
    d = koepel(STEKEL_KLEIN if stap >= 6 else STEKEL_GROOT)
    gezicht(d)
    if stap < 4:
        # Hitmontop: flappen hangen opzij (breed), V boven de ogen
        for y in range(5, 13):
            for x in (-1, -2, 22, 23):
                d[(x, y)] = 15 if (x in (-2, 23) or y in (5, 12)) else 4
        d.update(V_OUD)
        return d
    d.update(V_NIEUW)
    if stap >= 5: knot(d, var)
    return d


SRCD = top_idx()
HAND = {(x - 9, y - 28): SRCD[(x, y)] for x in range(9, 17) for y in range(28, 36) if (x, y) in SRCD
        and not (x == 16 and y in (28, 29))}       # Hitmontops linkerhand (anim_front x9-16, y28-35), 1:1
BAND = ['c11c', 'dccd']                              # zijn polsband (wit midden, grijs randen)


def knot(d, var):
    """knot achter de koepel: hand eerst (achter), koepel eroverheen; band tussen knot en kop, zichtbaar."""
    if var == 1: hx, hy, band = -6, -4, [(x, y) for x in (-1, 0) for y in range(-2, 2)]
    else:        hx, hy, band = -8, 4, [(x, y) for x in (-2, -1) for y in range(5, 9)]
    for (x, y), i in HAND.items():
        q = (hx + x, hy + y)
        if q not in d: d[q] = i
    xs = sorted({p[0] for p in band}); ys = sorted({p[1] for p in band})
    for j, x in enumerate(xs):
        for k, y in enumerate(ys): d[(x, y)] = CH.index(BAND[j][k])
    for x in xs: d[(x, ys[0] - 1)] = 15; d[(x, ys[-1] + 1)] = 15
    # band sluit aan op de koepelomtrek: gat tussen band en omtrek dicht met kopkleur
    for y in ys:
        x = xs[-1] + 1
        while (x, y) not in d or d[(x, y)] == 15 and (x + 1, y) not in d:
            d[(x, y)] = 3 if (x + 1, y) in d else 15; x += 1
            if x > 5: break
    return d


def schuif(d, dx=OX, dy=OY): return {(x + dx, y + dy): i for (x, y), i in d.items()}


if __name__ == '__main__':
    S = '/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/ae45fa98-ab2a-515e-b35e-9c539e2bda6f/scratchpad/'
    for k, d in {'h3': hoofd(3), 'h4': hoofd(4), 'h6a': hoofd(6, 1), 'h6b': hoofd(6, 2)}.items():
        raster8(schuif(d), S + k + '.png', Z=14)
