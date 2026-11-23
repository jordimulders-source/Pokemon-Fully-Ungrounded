# Gnometrotter Ice – sprite r7 (23 nov)

Basis: `../sprite_r6/gnometrotter_ice.png`; alleen de benen zijn opnieuw opgebouwd. Lijnwerk en delen zijn gemeten op r5, omdat r6 de 9-lijnen al had omgekleurd. Bouwen: `python3 r7.py` → `gnometrotter_ice.png`, `_8x.png`, `r7_log.txt`. `python3 vel.py` → `vel.png` (model | r5 | r6 | r7, 12×, alleen de benen).

## Telling t.o.v. r6
| zone | px |
|---|---|
| benen | 68 |
| rest | **0** (silhouet 0) |

## Wat
- Per dij één facetgrens: de duidelijkste lichte barst uit het model, als één doorlopende lijn die meebuigt met de bol. Linkerdij (22,9;43,6)→(23,8;50); rechterdij (44,5;41,5)→(45,6;47,2)→(47;50). De lijn is 11, met 1 px schaduwkant rechts.
- Geen barsten meer in voetballen en kruis, alleen volume per bol: 11 linksboven, 10 midden, 9 als sikkel rechtsonder en langs de zwarte rand.
- Opgeschoond: geen tintvlakjes kleiner dan 3 px in de benen. Bestaand 9-lijnwerk (buitenrand, riem, baard, zolen, zitnaad kruis) blijft.
