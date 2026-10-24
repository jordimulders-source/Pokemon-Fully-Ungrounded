#!/usr/bin/env python3
"""Olinguito fase 1, herbouw op Zigzagoon (graphics/pokemon/zigzagoon/anim_front.png) als onderlaag.
Met de hand getekend als tekst-raster: per onderdeel rijen (y, x, tekens) op de coordinaten van de basis.
'.' = niets zetten (laat de onderliggende laag staan), '0' = transparant maken.
Palet (ronde 23): 1 omlijning, 2 donkerbruin/masker, 3 schaduw, 4 vacht, 5 hooglicht, 6 creme-schaduw,
7 creme, 8 licht creme, 9/A/B/C klauw (grijs-wit), D goud, E oranje, F rood.
Gebruik: python3 bouw.py [uitmap]"""
import os, sys
from PIL import Image

H = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(H, '..')


def leeg():
    return [[0] * 64 for _ in range(64)]


def zet(g, rijen, dx=0, dy=0):
    for y, x, s in rijen:
        for i, c in enumerate(s):
            if c == '.':
                continue
            g[y + dy][x + i + dx] = int(c, 16)


# ---- onderdelen (frame 1). Volgorde = tekenvolgorde (ver -> nabij) ----
# Romp: Zigzagoon-romp zonder stekels; rug als boog op de basislijn van de stekels, bil x48.
# Segmenten (y, x, tekens); meerdere per rij.
ROMP = [
    (24, 35, "222"),
    (25, 32, "222"), (25, 35, "555"), (25, 38, "222"),
    (26, 30, "22"), (26, 32, "555555"), (26, 38, "444"), (26, 41, "222"),
    (27, 29, "2"), (27, 30, "55555"), (27, 35, "444444444"), (27, 44, "3"), (27, 45, "11"),
    (28, 28, "5555"), (28, 32, "4444444444444"), (28, 45, "33"), (28, 47, "1"),
    (29, 28, "55"), (29, 30, "444444444444444"), (29, 45, "33"), (29, 47, "1"),
    (30, 28, "44444444444444444"), (30, 45, "333"), (30, 48, "1"),
    (31, 28, "4444444444444444"), (31, 44, "3333"), (31, 48, "1"),
    (32, 28, "4444444444444444"), (32, 44, "3333"), (32, 48, "1"),
    (33, 28, "4444444444444444"), (33, 44, "3333"), (33, 48, "1"),
    (34, 28, "444444444444444"), (34, 43, "33333"), (34, 48, "1"),
    (35, 28, "4444444444"), (35, 38, "3"), (35, 39, "44444"), (35, 44, "3333"), (35, 48, "1"),
    (36, 27, "44444444444"), (36, 38, "3"), (36, 39, "555"), (36, 42, "44"), (36, 44, "3333"), (36, 48, "1"),
    (37, 27, "4444444444"), (37, 37, "3"), (37, 38, "555"), (37, 41, "444"), (37, 44, "333"), (37, 47, "1"),
    (38, 27, "444444444"), (38, 36, "33"), (38, 38, "55"), (38, 40, "4444"), (38, 44, "333"), (38, 47, "1"),
    (39, 26, "33"), (39, 28, "44444444"), (39, 36, "3"), (39, 37, "4444444"), (39, 44, "33"), (39, 46, "1"),
    (40, 25, "1"), (40, 26, "333"), (40, 29, "444444"), (40, 35, "33"), (40, 37, "4444444"), (40, 44, "3"), (40, 45, "1"),
    (41, 23, "11"), (41, 25, "333"), (41, 28, "444443"), (41, 34, "3"), (41, 35, "44444433"), (41, 43, "1"),
    (42, 22, "211"), (42, 25, "3333"), (42, 29, "333"), (42, 32, "33"), (42, 34, "4444433"), (42, 41, "1"),
    (43, 27, "1333"), (43, 31, "11"),
    (44, 28, "111"),
]

# Verre achterpoot: stompje achter de nabije, hoger en in schaduwtint (zoals Linoone).
VER_ACHTER = [
    (41, 42, "331"),
    (42, 41, "23331"),
    (43, 41, "22331"),
    (44, 41, "22231"),
    (45, 41, "1221"),
    (46, 42, "111"),
]

# Staart: hangende J aan de bovenkant van de bil (waar Zigzagoons staart aansluit); hangt vrij boven de grond,
# krult onderaan terug omhoog naar een ronde lichte punt. Lucht tussen bil en steel en in de haak.
STAART = [
    (25, 44, "222"),
    (26, 44, "55522"),
    (27, 45, "555422"),
    (28, 45, "5544442"),
    (29, 45, "54444442"),
    (30, 46, "44444441"),
    (31, 47, "44444331"),
    (32, 47, "444443331"),
    (33, 48, "134443331"),
    (34, 49, "1344331"),
    (35, 50, "1344331"),
    (36, 51, "144331"),
    (37, 52, "144331"),
    (38, 52, "144431"),
    (39, 53, "14431"),
    (40, 48, "11"), (40, 53, "1441"),
    (41, 47, "1651"), (41, 53, "1431"),
    (42, 47, "1651"), (42, 52, "14331"),
    (43, 47, "1544"), (43, 51, "11331"),
    (44, 48, "14433331"),
    (45, 49, "133311"),
    (46, 50, "111"),
]

# Nabije achterpoot: dij als bolling in de romp, onderbeen met hak naar achteren.
ACHTER = [
    (43, 33, "23444433"),
    (44, 33, "25444331"),
    (45, 34, "2544331"),
    (46, 34, "254431"),
    (47, 33, "2441331"),
    (48, 33, "111.11"),
]

# Verre voorpoot: reikt onder de kin naar voren (Linoone/Zigzagoon), schaduwtint, voet hoger dan de nabije.
VER_VOOR = [
    (41, 17, "13333"),
    (42, 16, "133333"),
    (43, 15, "1433333"),
    (44, 14, "1433331"),
    (45, 13, "143331"), (45, 20, "1"),  # dicht gaatje tussen de voorpoten (omlijning)
    (46, 13, "233321"),
    (47, 14, "1111"),
]

# Kop (Zigzagoon-kopconstructie: lange snuit naar links, een oog, neus x6-9 y33-34). Vanaf x5.
#        x5   x10  x15  x20  x25  x30
KOP5 = [
    (20, ".................222"),
    (21, "........22......25441"),
    (22, ".......24622...2587431"),
    (23, ".......246322222477631"),
    (24, "......24332555544633311"),
    (25, ".....24555444444443333 1"),
    (26, "....2455544444444444333 1"),
    (27, "....24444447774444443331"),
    (28, "...244444472227444443331"),
    (29, "...2444422222222444433331"),
    (30, "..24422222222222224433331"),
    (31, "..24222222111112222243331"),
    (32, ".222222222EEC1E2222243331"),
    (33, ".1B1122222DD11D2222243331"),
    (34, ".2111777222DDD2222777631"),
    (35, "..2777777722222277777631"),
    (36, "..2777717777222777776631"),
    (37, "..1111177777777776666631"),
    (38, "...17777777666666666331"),
    (39, "....116666666666666311"),
    (40, "......11166666666311"),
    (41, ".........11166311"),
    (42, "............111"),
]
KOP = [(y, 5, s.replace(' ', '')) for y, s in KOP5]

# Nabije voorpoot: uit de schouder onder de achterkant van de kop, licht aan de voorkant, voet licht gekanteld.
VOOR = [
    (40, 23, "255431"),
    (41, 22, "2554431"),
    (42, 22, "254431"),
    (43, 21, "2544331"),
    (44, 21, "254431"),
    (45, 21, "25441"),
    (46, 20, "254431"),
    (47, 20, "2444431"),
    (48, 20, "1333111"),
    (49, 21, "111"),
]

# Klauwen, Sandslash-stijl: licht blad (B/C), grijze bovenrand, donkere onderrand; punt buigt omlaag.
KLAUW_VOOR = [
    (45, 17, "999"),
    (46, 16, "9BCC"),
    (47, 15, "1A111"),
    (48, 16, "9BCC"),
    (49, 15, "9A111"),
    (50, 15, "11"),
]
KLAUW_VER = [
    (44, 10, "999"),
    (45, 9, "9ABB"),
    (46, 8, "1A111"),
    (47, 9, "9ABB1"),
    (48, 8, "9A111"),
    (49, 8, "11"),
]


def staart(d):
    """Frame 2: voet van de staart blijft aan de bil; het hangende deel (vanaf y36) zakt 1 px, rij 35 rekt mee."""
    if not d:
        return STAART
    r = [(y, x, s) for y, x, s in STAART if y < 36]
    r += [(36, x, s) for y, x, s in STAART if y == 35]
    r += [(y + 1, x, s) for y, x, s in STAART if y >= 36]
    return r


def frame(f):
    """Frame 2: kop zakt 1 px (ademhaling), staart zwaait na; romp en poten blijven staan."""
    g = leeg()
    d = 0 if f == 0 else 1
    zet(g, VER_ACHTER)
    zet(g, ROMP)
    zet(g, staart(d))
    zet(g, ACHTER)
    zet(g, VER_VOOR)
    zet(g, KLAUW_VER)
    zet(g, VOOR)
    zet(g, KOP, dy=d)
    zet(g, KLAUW_VOOR)
    return g


def pal():
    p = []
    for regel in open(os.path.join(H, '..', 'normal.pal')).read().split('\n')[3:19]:
        p += [int(v) for v in regel.split()]
    return p


def main():
    g1, g2 = frame(0), frame(1)
    im = Image.new('P', (64, 128), 0)
    im.putpalette(pal())
    for y in range(64):
        for x in range(64):
            im.putpixel((x, y), g1[y][x])
            im.putpixel((x, y + 64), g2[y][x])
    im.save(os.path.join(OUT, 'anim_front.png'), transparency=0)
    print('ok', os.path.join(OUT, 'anim_front.png'))


if __name__ == '__main__':
    main()
