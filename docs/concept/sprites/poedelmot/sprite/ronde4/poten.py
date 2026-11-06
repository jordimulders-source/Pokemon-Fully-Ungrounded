"""Ronde 4: alleen de poten, vanuit ronde 3 variant B. Pootzone = rijen 45-63 (de schouders in rijen 40-44 blijven).
Met de hand getypte stukken (x, tekens). Rechts in beeld = nabije kant: alle poten rechts net wat groter en lager.
Voeten: wolpluk die naar onder spits toeloopt, met 1 px donkere klauwtjes (V) onder de punt. Schrijft raster.txt."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
R = [list(l.rstrip('\n')) for l in open(os.path.join(HERE, '../ronde3/variant_B/raster.txt'))][:64]
def zone(x, y): return y >= 45
NIEUW = {
 45: [(12, "2236555544355444333", "65554431")],
 46: [(11, "24356555443334443333", "565554431")],
 47: [(10, "24435555443334333333", "3555544431")],
 48: [(10, "2444355544", "3344333333", "3555444331")],
 49: [(10, "2444355443", "334433333", "35554443331")],
 50: [(10, "24433355431", "33433333", "2554443331")],
 51: [(8, "222", "1111", "255431", "1333331", "1", "25544431", "11", "2221")],
 52: [(8, "25543", "33", "254431"), (22, "11111"), (29, "25554431", "2", "255441")],
 53: [(9, "2431", "1", "26655441"), (28, "2665554431", "4", "4431")],
 54: [(10, "11"), (14, "25554431"), (28, "2555544331", "1", "231")],
 55: [(9, "1"), (12, "1"), (15, "244431"), (29, "25544431"), (40, "1")],
 56: [(16, "2431"), (30, "244431"), (39, "1"), (41, "1")],
 57: [(17, "11"), (31, "2431")],
 58: [(16, "1"), (19, "1"), (32, "11")],
 59: [(31, "1"), (34, "1")],
}
for y in range(45, 64):
    for x in range(64): R[y][x] = '.'
    for x0, *delen in NIEUW.get(y, []):
        for i, c in enumerate(''.join(delen)): R[y][x0 + i] = c
open(os.path.join(HERE, 'raster.txt'), 'w').write('\n'.join(''.join(r) for r in R) + '\n')
