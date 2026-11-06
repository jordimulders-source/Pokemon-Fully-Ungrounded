"""Ronde 5: alleen de poten, vanuit ronde 4. Zone = rijen 45-63 plus het vak x26-38, y41-44
(de aanzet van de rechtervoorpoot, waar Jordi's lijnen liggen). Met de hand getypte stukken (x0, tekens);
rijen 45-50 zijn ronde 4 met alleen de rechtervoorpoot aangepast, rijen 51-59 opnieuw getekend.
Schrijft raster.txt."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
R = [list(l.rstrip('\n')) for l in open(os.path.join(HERE, '../ronde4/raster.txt'))][:64]
# rechtervoorpoot tussen Jordi's twee lijnen (licht), rechts van de rechterlijn de flank (schaduw)
AANPASSING = {
 41: [(26, "5543653343311")],
 42: [(26, "5536554334331")],
 43: [(26, "5436554334331")],
 44: [(26, "4443655433431")],
 45: [(28, "33655433431")],
 46: [(30, "3655433431")],
 47: [(30, "3565543431")],
 48: [(30, "3556544331")],
 49: [(30, "3556544431")],
 50: [(29, "3355644431")],
}
# rijen 51-59 opnieuw: P = achterpoot links, S = achterpoot rechts
NIEUW = {
 51: [(9, "221111" "2565431" "1" "33333" "11" "25564431" "11221")],
 52: [(9, "254331" "255441"), (23, "11111"), (30, "25654431" "25431")],
 53: [(9, "25431"), (15, "255431"), (31, "2554431" "35431")],
 54: [(8, "254431" "2456431"), (31, "25654431" "5431")],
 55: [(7, "245431" "24554431"), (31, "255544331" "5431")],
 56: [(7, "244313" "1244431"), (31, "124544331" "4431")],
 57: [(7, "1311"), (12, "1"), (13, "1"), (15, "1331"), (31, "1"), (33, "144311" "243131")],
 58: [(8, "b"), (12, "b"), (16, "bb"), (34, "1331"), (39, "131"), (43, "1")],
 59: [(35, "bb"), (40, "b")],
}
for y, segs in AANPASSING.items():
    for x0, s in segs:
        for i, c in enumerate(s): R[y][x0 + i] = c
for y in range(51, 64):
    for x in range(64): R[y][x] = '.'
for y, segs in NIEUW.items():
    for x0, s in segs:
        for i, c in enumerate(s):
            if c != '.': R[y][x0 + i] = c
open(os.path.join(HERE, 'raster.txt'), 'w').write('\n'.join(''.join(r) for r in R) + '\n')
