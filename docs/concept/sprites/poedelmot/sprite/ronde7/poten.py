"""Ronde 7: alleen de achterpoten, vanuit ronde 6. Voorpoten pixel voor pixel ronde 6.
Links (verre kant, Jordi: "links zitten ze meer aan de onderkant dan rechts"): de omlijning onder de flanklob (y51) verdwijnt; P loopt recht onder de flank door; Q komt onder de buik uit.
een punt met 2 klauwtjes; Q komt als donkerdere poot achter P vandaan. Rechts: de lijfrand onder de vleugel krijgt een
heup (x39-42, y48-51) die doorloopt in achterpoot S; R1 komt achter S vandaan. Schrijft raster.txt."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
R6 = [list(l.rstrip('\n')) for l in open(os.path.join(HERE, '../ronde6/raster.txt'))][:64]
R = [r[:] for r in R6]
LINKS = (7, 14, 51, 58)    # x0, x1, y0, y1 (achterpootvak links)
RECHTS = (39, 45, 48, 59)  # achterpootvak rechts (plus x37-38 op y52-57, de oude rand van S)
for y in range(LINKS[2], LINKS[3] + 1):
    for x in range(LINKS[0], LINKS[1] + 1): R[y][x] = '.'
for y in range(RECHTS[2], RECHTS[3] + 1):
    for x in range(RECHTS[0], RECHTS[1] + 1):
        if not (y in (48, 49) and x == 39 and y == 49): R[y][x] = '.'
for y in range(52, 59):
    for x in (37, 38): R[y][x] = '.'
NIEUW = {
 # heup rechts (onder de vleugel, achter de rechtervoorpoot): S en R1 komen uit de zijkant
 48: [(39, "31")],
 49: [(39, "131")],
 50: [(39, "3431")],
 # links (verre kant, meer aan de onderkant): P recht onder de flanklob, Q onder de buik
 51: [(10, "24443"), (38, "144431")],
 52: [(10, "24541"), (23, "33"), (37, "1344331")],
 53: [(10, "24541"), (23, "341"), (37, "1454131")],
 54: [(10, "24431"), (23, "331"), (38, "254131")],
 55: [(10, "2431"), (23, "231"), (38, "244131")],
 56: [(10, "2431"), (23, "121"), (38, "243121")],
 57: [(11, "121"), (23, "b.b"), (39, "231"), (42, "b")],
 58: [(11, "b.b"), (39, "121")],
 59: [(39, "b.b")],
}
for y, segs in NIEUW.items():
    for x0, s in segs:
        for i, c in enumerate(s):
            if c != '.': R[y][x0 + i] = c
open(os.path.join(HERE, 'raster.txt'), 'w').write('\n'.join(''.join(r) for r in R) + '\n')
