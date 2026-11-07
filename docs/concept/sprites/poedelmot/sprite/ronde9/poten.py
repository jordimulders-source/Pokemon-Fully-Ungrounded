"""Ronde 9: de onderkant volgens Jordi's rode vormen (referenties/jordi_schets_ronde8_vormen.png, ronde 8 op 10x,
verschoven -9,-51 px: sprite-x = (px+9)/10, sprite-y = (py+51)/10), vanuit ronde 8.
- links (kruis, x10-15 y45-51): geen uitstulpsel; de linkerrand loopt glad door (x14) tot aan de linkervoorpoot;
- midden (U-vormen, x22-31 y50-58): de ruimte tussen linkervoorpoot en rechtervoorpoot onder de buik gevuld (verre achterpoot);
- rechts (lus x38-41 y42-56 + onderstreep x35-41 y56): de inham onder de vleugel gevuld, S als kolom uit het lijf tot de grond.
Voorpoten blijven gelijk (ook onder de tweede U-lus, x29-31: daar staat de rechtervoorpoot vóór de verre poot). Schrijft raster.txt."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
R = [list(l.rstrip('\n')) for l in open(os.path.join(HERE, '../ronde8/raster.txt'))][:64]
NIEUW = {
 # rechts: inham tussen arm en vleugel dicht (binnen de lus)
 41: [(39, "111")],
 42: [(39, "333")],
 43: [(39, "3433")],
 44: [(39, "44333")],
 45: [(39, "45432")],
 46: [(40, "5441")],
 47: [(40, "55441")],
 # links: glad, geen uitstulpsel
 # (rij 45-52; x10-13 leeg, x14 selout)
 # midden: verre achterpoot vult de U tussen de voorpoten
 52: [(23, "3")],
 53: [(23, "344333")],
 54: [(23, "343333")],
 55: [(23, "333333"), (40, "31")],
 56: [(22, "13333331"), (35, "1333331")],
 57: [(23, "112111"), (36, "11211")],
 58: [(24, "b.b")],
}
LINKS = {45: (12, "..2"), 46: (11, "...2"), 47: (10, "....2"), 48: (10, "....2"), 49: (10, "....25"),
         50: (10, "....23"), 51: (10, "....."), 52: (11, ".....")}
for y, (x0, s) in LINKS.items(): NIEUW.setdefault(y, []).append((x0, s))
for y, segs in NIEUW.items():
    for x0, s in segs:
        for i, c in enumerate(s): R[y][x0 + i] = c
open(os.path.join(HERE, 'raster.txt'), 'w').write('\n'.join(''.join(r) for r in R) + '\n')
