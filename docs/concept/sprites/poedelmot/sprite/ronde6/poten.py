"""Ronde 6: alleen de twee voorpoten, vanuit ronde 5. Rij 51 (de 'elleboog', waar de poot onder het lijf vandaan komt)
blijft; daaronder lopen beide onderpoten af naar een smalle punt, meer naar het midden, met 2 klauwtjes van 1 px vast
aan de punt. De achterpoten (P/Q links, S/R1 rechts) blijven pixel voor pixel ronde 5, net als de omlijningspixels
die eraan grenzen (die sluiten hun rand). Schrijft raster.txt en achterpoten_masker.txt (voor controle.py)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
R5 = [list(l.rstrip('\n')) for l in open(os.path.join(HERE, '../ronde5/raster.txt'))][:64]
R = [r[:] for r in R5]
# achterpoten in ronde 5 (rij: x-bereiken)
ACHTER = {51: [(9, 14), (38, 42)], 52: [(9, 14), (38, 42)], 53: [(9, 13), (38, 42)], 54: [(8, 13), (39, 42)],
          55: [(7, 12), (40, 43)], 56: [(7, 12), (40, 43)], 57: [(7, 10), (12, 12), (39, 44)],
          58: [(8, 8), (12, 12), (39, 41), (43, 43)], 59: [(40, 40)]}
H = {(x, y) for y, rs in ACHTER.items() for a, b in rs for x in range(a, b + 1) if R5[y][x] != '.'}
vast = set(H)
for y in range(51, 60):
    for x in range(64):
        if (x, y) not in H and R5[y][x] == '1' and any((x + dx, y + dy) in H for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            vast.add((x, y))
# onderpoten wissen (rij 52-59), behalve de vaste pixels
for y in range(52, 60):
    for x in range(64):
        if (x, y) not in vast: R[y][x] = '.'
# rij 52 van de buik (onderrand) terugzetten
for x in range(23, 28): R[52][x] = R5[52][x]
NIEUW = {
 52: [(16, "2565431"), (29, "25655431")],
 53: [(17, "255431"), (29, "2555431")],
 54: [(17, "254431"), (29, "2564431")],
 55: [(18, "25431"), (30, "255431")],
 56: [(18, "2431"), (30, "25431")],
 57: [(19, "121"), (31, "2431")],
 58: [(19, "b"), (21, "b"), (31, "121")],
 59: [(31, "b"), (33, "b")],
}
for y, segs in NIEUW.items():
    for x0, s in segs:
        for i, c in enumerate(s): R[y][x0 + i] = c
open(os.path.join(HERE, 'raster.txt'), 'w').write('\n'.join(''.join(r) for r in R) + '\n')
open(os.path.join(HERE, 'achterpoten_masker.txt'), 'w').write('\n'.join('%d %d' % p for p in sorted(vast)) + '\n')
