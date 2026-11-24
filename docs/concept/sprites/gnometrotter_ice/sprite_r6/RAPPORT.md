# Gnometrotter Ice – sprite r6 (23 nov)

Basis: `../sprite_r5/gnometrotter_ice.png` (zelfde palet en indexen). Bouwen: `python3 r6.py` → `gnometrotter_ice.png`, `_8x.png`, `r6_log.txt` (elke gewijzigde pixel, zone, oud → nieuw). `python3 vel.py` → `vel.png` (model | r5 | r6, 8×).

## Telling t.o.v. r5
| zone | px | wat |
|---|---|---|
| sikkel (keuring 1) | 8 | de 8 genoemde pixels 7 → 6 |
| neusklont (keuring 2) | 4 | (14,20),(14,21),(15,21),(15,22) → 0 (= de 4 silhouetpixels) |
| benen | 147 | zie hieronder |
| rest | **0** | muts, baard, rechterhand, zolen, romp, schouder onaangeroerd |

## Benen
- Vijf delen: linkerdij, kruis, rechterdij, linkervoetbal, rechtervoetbal. Bestaand lijnwerk in 9 blijft: 9 tegen buitenrand, riem, baard, zool of een ander deel, en de zitnaad van het kruis. Silhouet en zolen zijn gelijk.
- Volume per deel als Gen 3-bol: 11 linksboven, 10 midden, 9 als sikkel rechtsonder, en 1 px 9/10 langs de zwarte buitenrand rechts/onder. Daarmee zijn de horizontale banden over de hele breedte weg.
- Facetgrenzen = barsten uit het model als lichte naad (11), op de modellijnen. Lijnen: linkerdij (18,4;45,9)→(23;47,3)→(27,5;47,3) en (22,9;43,6)→(23,5;50); rechterdij (44,5;41,5)→(45,6;47,2), (38,5;47,6)→(45,9;47,2), (45,9;47,2)→(49,9;44,9), (45,9;47,2)→(47;50); voetballen (19,6;51,3)→(19,9;54,4) en (47,1;51,2)→(48;55,7). Ze worden per rij of per kolom gerasterd, dus ze buigen mee en zijn niet kaarsrecht.
- Steile barsten krijgen rechts ernaast 1 px schaduwkant (een tint donkerder), zodat ze als ribbe lezen. Vlakke barsten krijgen die niet, want anders ontstaat weer een band.

## Twijfels
- De lijncoördinaten zijn op het model afgelezen (op de Rock-geometrie, ±1 px). Van de twee barsten in de rechtervoetbal is er maar één gebruikt: twee gaven evenwijdige strepen.
- Op een paar plekken staan nog losse tintpixels (bijvoorbeeld (44,40) A tussen 9, en de 11|9-ribbe op de linkerdij x23–24). De benen blijven wat drukker dan de romp.
