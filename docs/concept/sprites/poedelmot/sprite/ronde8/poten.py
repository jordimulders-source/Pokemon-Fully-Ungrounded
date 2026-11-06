"""Ronde 8: alleen de achterpoten (+ de onderrand van het lijf waar ze aan vastzitten), vanuit ronde 6.
Zoals Giratina's frontsprite: links (verre kant) geen poot naast het lijf; alleen een stukje van de verre achterpoot
komt onder de buik uit, tussen de voorpoten, half achter de rechtervoorpoot. Rechts (nabije kant) loopt het lijf door
in een achterlijf onder de vleugel, waaruit S (achter de rechtervoorpoot) en R1 (daarachter, hoger) als korte stompjes
komen, zonder naad. De voorpoten van ronde 6 blijven pixel voor pixel gelijk. Schrijft raster.txt."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
R6 = [list(l.rstrip('\n')) for l in open(os.path.join(HERE, '../ronde6/raster.txt'))][:64]
R = [r[:] for r in R6]
# 1. de achterpoten van ronde 6 wissen (P links, S/R1 rechts, met hun omlijning), behalve (37,51): hoek van de rechterarm
for l in open(os.path.join(HERE, '../ronde6/achterpoten_masker.txt')):
    x, y = map(int, l.split())
    if (x, y) != (37, 51): R[y][x] = '.'
# 2. nieuwe pixels per rij: (x0, tekens); elk teken is een pixel (hex-index of 'b')
NIEUW = {
 # rechts: achterlijf onder de vleugel, achter de rechterarm (x<=39 op rij 46-49 = armomlijning, blijft)
 45: [(39, "22")],
 46: [(40, "522")],
 47: [(40, "5542")],
 48: [(40, "54441")],
 49: [(40, "444331")],
 50: [(39, "4443331")],
 # links: flanklob sluit onderaan af; rechts: achterlijf loopt door
 51: [(10, "24333"), (38, "44333331")],
 52: [(11, "21111"), (24, "33333"), (37, "344332331")],
 # midden: verre achterpoot onder de buik uit (x23-29); rechts S (x36-40) en R1 (x42-44) uit het achterlijf
 53: [(24, "14433"), (36, "33443133" + "1")],
 54: [(25, "2433"), (36, "34433123" + "1")],
 55: [(26, "2331"), (36, "34331"), (42, "121")],
 56: [(26, "121"), (36, "2331"), (42, "b"), (44, "b")],
 57: [(26, "b"), (28, "b"), (37, "121")],
 58: [(37, "b"), (39, "b")],
}
for y, segs in NIEUW.items():
    for x0, s in segs:
        for i, c in enumerate(s): R[y][x0 + i] = c
open(os.path.join(HERE, 'raster.txt'), 'w').write('\n'.join(''.join(r) for r in R) + '\n')
