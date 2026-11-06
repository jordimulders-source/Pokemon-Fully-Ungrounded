"""Ronde 11: alleen de achterpoten, vanuit ronde 10, binnen Jordi's vormen. Jordi: "de benen zijn nu wel te dik en ik zie er
maar 1 ipv 2, de benen moeten dus smaller, linksonder zie je van het achterste been maar een heel klein beetje, en van
rechtsonder ook een klein beetje. Plus ik wil dat rechts aangesloten wordt op het lijf".
- midden (verre kant, binnen de U): middenpoot M1 (smal, punt + 2 klauwtjes op y57; linkerkant donkere wol tegen de zwarte rand van de linkervoorpoot, geen dubbele zwarte lijn) en daarachter een klein stukje
  van de achterste poot A1 (x28, 1 klauwtje op y56);
- rechts (nabije kant, binnen de lus): middenpoot S (smal, punt + 2 klauwtjes op y56) en daarachter een klein stukje
  van de achterste poot A2 (x40, 1 klauwtje op y56);
- aansluiting rechts: de zwarte armrand tussen lijf en poot (x38 y45, x39 y46-49) wordt donkere wol (tint 3), zodat
  de flank doorloopt in de poten (zoals Giratina: donkergrijs, geen zwart, tussen lijf en achterpoot).
Onderste voorpoten (rijen 52-59, pixels van ronde 6) ongewijzigd. Schrijft raster.txt en poten.txt (cellen per poot)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
R = [list(l.rstrip('\n')) for l in open(os.path.join(HERE, '../ronde10/raster.txt'))][:64]
# oude achterpootpixels wissen: midden x23-28 y53-58, rechts x36-41 y52-57 (voorpootpixels vallen hier niet in)
for y in range(53, 59):
    for x in range(23, 29): R[y][x] = '.'
R[55][29] = '.'; R[56][29] = '.'; R[56][22] = '.'
for y in range(52, 58):
    for x in range(36, 42):
        if not (x == 36 and y == 52): R[y][x] = '.'
POOT = {
 'M1': {53: (23, "34433"), 54: (23, "34431"), 55: (23, "3431"), 56: (23, "121"), 57: (23, "b.b")},
 'A1': {53: (28, "3"), 54: (28, "3"), 55: (28, "1"), 56: (28, "b")},
 'S':  {52: (37, "343"), 53: (36, "3431"), 54: (36, "3431"), 55: (36, "121"), 56: (36, "b.b")},
 'A2': {52: (40, "31"), 53: (40, "31"), 54: (40, "21"), 55: (40, "1"), 56: (40, "b")},
}
cellen = []
for naam, rijen in POOT.items():
    for y, (x0, s) in rijen.items():
        for i, c in enumerate(s):
            if c != '.': R[y][x0 + i] = c; cellen.append('%s %d %d' % (naam, x0 + i, y))
# aansluiting rechts: zwarte armrand naast de flank -> donkere wol
R[45][38] = '3'
for y in range(46, 50): R[y][39] = '3'
open(os.path.join(HERE, 'raster.txt'), 'w').write('\n'.join(''.join(r) for r in R) + '\n')
open(os.path.join(HERE, 'poten.txt'), 'w').write('\n'.join(cellen) + '\n')
