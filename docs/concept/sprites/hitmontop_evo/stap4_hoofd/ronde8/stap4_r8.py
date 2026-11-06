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
# omtrek per rij (links, rechts) na het gladmaken (stap 3), naar de verdubbelde OW-kop: ronde koepel, stekel als
# smallere punt erbovenop (holle overgang, zoals in hitmontop_3d.webp), wangen recht omlaag naar een ronde kin.
KOEPEL = {1: (5, 16), 2: (3, 18), 3: (2, 19), 4: (1, 20), 5: (0, 21), 6: (0, 21), 7: (0, 21), 8: (0, 21), 9: (0, 21),
          10: (0, 21), 11: (0, 21), 12: (0, 21), 13: (0, 21), 14: (0, 21), 15: (1, 20), 16: (1, 20), 17: (2, 19),
          18: (3, 18), 19: (5, 16)}
STEKEL_GROOT = {0: (7, 14), -1: (8, 13), -2: (9, 12), -3: (9, 12), -4: (9, 12), -5: (10, 11)}   # OW: 1, 3, 3, 3, breder
STEKEL_KLEIN = {0: (8, 13), -1: (9, 12), -2: (10, 11)}                                           # middelste rijen eruit


def koepel(stekel):
    rij = dict(KOEPEL); rij.update(stekel)
    d = {}
    for y, (a, b) in rij.items():
        for x in range(a, b + 1): d[(x, y)] = 3
    for (x, y) in list(d):
        if any(q not in d for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))): d[(x, y)] = 15
    # licht linksboven als sikkel langs de omtrek; schaduw (4) als sikkel rechtsonder, 5 diep rechtsonder
    for (x, y) in list(d):
        if d[(x, y)] != 3: continue
        rand = [q for q in ((x - 1, y), (x, y - 1), (x - 1, y - 1)) if d.get(q) == 15]
        if rand and x <= 9 and y <= 8: d[(x, y)] = 2
        onder = [q for q in ((x + 1, y), (x, y + 1), (x + 1, y + 1)) if d.get(q) == 15]
        if onder and (x >= 13 or y >= 16): d[(x, y)] = 4
    for (x, y) in list(d):
        if d[(x, y)] == 3 and any(d.get(q) == 4 for q in ((x + 1, y), (x, y + 1))) and x + y >= 31: d[(x, y)] = 4
    for (x, y) in list(d):
        if d[(x, y)] == 4 and x + y >= 34 and any(d.get(q) == 15 for q in ((x + 1, y), (x, y + 1))): d[(x, y)] = 5
    return d


def gezicht(d, v_y=None):
    for (ex, ey) in ((5, 10), (13, 10)):
        for j, r in enumerate(OOG):
            for i, c in enumerate(r):
                if c != '.': d[(ex + i, ey + j)] = CH.index(c)
    for x in range(8, 14): d[(x, 16)] = 5                      # mondstreepje
    return d


# V (voorrand van de flappen): in Hitmontop vlak boven de ogen met de punt ertussen; hier per rij (x, kleur)
V_OUD = {(10, 9): 15, (11, 9): 15, (9, 8): 5, (12, 8): 5, (8, 8): 5, (13, 8): 5, (7, 9): 5, (14, 9): 5,
         (6, 9): 5, (15, 9): 5, (5, 9): 4, (16, 9): 4}                             # flapranden boven de ogen
V_NIEUW = {(10, 5): 15, (11, 5): 15, (9, 4): 5, (12, 4): 5, (8, 3): 5, (13, 3): 5, (7, 3): 5, (14, 3): 5,
           (6, 2): 4, (15, 2): 4}                                                  # naar achteren getrokken


def hoofd(stap, var=1):
    d = koepel(STEKEL_KLEIN if stap >= 6 else STEKEL_GROOT)
    gezicht(d)
    if stap < 4:
        # Hitmontop: flappen hangen opzij (breed), V boven de ogen
        for y in range(6, 15):
            for x in (-1, -2, 22, 23):
                d[(x, y)] = 15 if (x in (-2, 23) or y in (6, 14)) else 4
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
    if var == 1: hx, hy, band = -4, -4, [(x, y) for x in (2, 3) for y in range(-1, 3)]
    else:        hx, hy, band = -6, 11, [(x, y) for x in (-1, 0) for y in range(13, 17)]
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
