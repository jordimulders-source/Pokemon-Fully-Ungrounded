# Hauntflare v8: tanden (maker, 15 nov)

Uitgangspunt `../sprite_v7/hauntflare_v7.png` (ogen en mond goedgekeurd). Alleen tanden in de opening; mondomtrek, positie, ogen ongemoeid.
Reproduceren: `python3 tanden.py` (pngs, rasters x18-35 y32-38 in het script) · `python3 controle.py` · `python3 vel.py` (vel.png: v7 | I | J | K | Haunter G3; gezicht 12x, sprite 6x, 1x).

## Bouw (alle kandidaten)
- Tanden = pixels van de opening (10 donkerrood / 5 tong) omgezet naar bolroze: **8 (licht) met 7 aan de schaduwkant** (rechts), dezelfde tinten als de huid boven de mond (rij 31-32: 8 en 7). Licht linksboven, net als de bol.
- Bovenlip y33 x24-30 nu één doorlopende zwarte lijn: (27,33) 8->1 (het oude 1-px tandje uit v7 zat ín de lip en las als een gat).
- V-vorm zoals Haunter G3 (3 breed -> 1 punt): dichtbij-tand 3 breed, verre tand 2 breed (perspectief, links kleiner).
- Achter de boventanden blijft donkerrood (y35 links en rechts 5->10), zodat de tanden loskomen; de tong begint daardoor midden op y35 en is op y36 heel (Haunter: donkere band achter de tanden, roze tong eronder).

## Kandidaten (diff t.o.v. v7)
- **I** (11 px): 2 boventanden. (25,34)8 (26,34)7 punt (25,35)8 · (28,34)8 (29,34)8 (30,34)7 punt (29,35)8 · donkerrood (23,35)(24,35)(30,35) · (27,33)->1.
- **J** (15 px): I + 2 ondertanden uit de onderlip (W-rij, tussen de bovenpunten in): (27,36)8 met voet (27,37)8 (sluit aan op de kin), (30,36)8 · onderlip (28,37) 5->1.
- **K** (13 px): 3 boventanden (ver -> dichtbij groter): (24,34)8 · (26,34)8 (27,34)7 punt (26,35)8 · (29,34)8 (30,34)8 (31,34)7 punt (30,35)8 · donkerrood (23-25,35)(29,35) · (27,33)->1.

## Controle (`controle.py`)
Alle drie: diff buiten de mond (x19-33, y32-38) **0**, silhouet 0, palet gelijk aan v7, P-modus, transparantie index 0.

## Afgevallen (zelf beoordeeld op 12x/1x)
- Tanden met doorbroken lip en zwarte V-rand rond elke tand (Haunter-bouw letterlijk): de 3-rijen-opening wordt een zwart kluwen, tong weg.
- Tanden in alleen 7: vallen weg tegen de tong (5), mond leest dicht.
- Ondertand 3 breed + punt (zigzag over de hele tongrij): mond loopt vol met roze, geen opening meer.

## Favoriet
**J**: het enige met wat de referenties tonen (V-tanden boven die naar beneden hangen + een golvende rij die van de onderlip omhoog komt), en op 1x nog leesbaar als open mond met tong. **I** is de rustigste en leest op 1x het scherpst (twee duidelijke hoektanden); kies I als de ondertanden op 1x te druk zijn. K (3 boventanden) is het drukst: de verre 1-px tand leest op 1x niet.
Zwak punt J: de ondertand op (30,36) is 1 px op de tong (leest als punt, niet als V; ruimte ontbreekt in de 3 rijen hoge opening).
