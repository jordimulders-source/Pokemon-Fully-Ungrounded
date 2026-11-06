"""Ronde 7: alleen de achterpoten, vanuit ronde 6. Voorpoten pixel voor pixel ronde 6.
Links: de horizontale omlijning onder de flanklob (y51) verdwijnt; de flank loopt door in achterpoot P, die afloopt naar
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
 # heup rechts (onder de vleugel, achter de rechtervoorpoot)
 48: [(39, "31")],
 49: [(39, "131")],
 50: [(39, "3431")],
 51: [(9, "244433"), (38, "144431")],
 52: [(8, "2454431"), (37, "1344431")],
 53: [(8, "245431"), (37, "1454431")],
 54: [(8, "245431"), (38, "2454431")],
 55: [(8, "24431" "21"), (39, "244431")],
 56: [(8, "2431" "231"), (39, "2431" "431")],
 57: [(8, "121" ".121"), (40, "231" "231")],
 58: [(8, "b.b"), (13, "b"), (40, "121" "11")],
 59: [(40, "b.b")],
}
for y, segs in NIEUW.items():
    for x0, s in segs:
        for i, c in enumerate(s):
            if c != '.': R[y][x0 + i] = c
open(os.path.join(HERE, 'raster.txt'), 'w').write('\n'.join(''.join(r) for r in R) + '\n')
