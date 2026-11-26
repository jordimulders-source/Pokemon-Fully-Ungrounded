# Regionale Poliwhirl – sprite r4 (maker): oogpositie
Basis `r3_E6.npy`. Alleen de oogzone verandert: 54 px verschil, **0 erbuiten** (`uitvoer5.py`). E6-ogen ongewijzigd (24 px per oog, uit Poliwhirls 37). Bouwen: `python3 uitvoer5.py && python3 vel5.py`.

Modelogen gemeten op de zwarte BUITENRAND (afgelezen op het model met spriteraster, in cellen, ±0,2): links x 13,6–18,0, y 2,6–7,4 (midden 15,8; 5,0); rechts x 26,8–31,5, y 1,9–7,5 (midden 29,2; 4,7).
Plaatsing E6 (6×6) op die middens: links x 13–18, y 2–7 (was 14–19, 3–8), rechts x 26–31, y 2–7 (was 27–32, 2–7). Het linkeroog vormt nu het silhouet: +2 px buiten de kop (13,4), (13,5), witte oogring tegen de lucht (zoals het model daar het oog als rand heeft, maar zonder zwarte buitenlijn: Poliwhirls oog heeft die niet).
Vrijgekomen kop: uit het model (`MODELOOG`), modelwit buiten het nieuwe oog → buurtint.

| (cellen) | model | r3_E6 | r4 |
|---|---|---|---|
| middens | (15,8; 5,0) (29,2; 4,7) | (17; 6) (30; 5) | (16; 5) (29; 5) |
| afstand tussen de ogen | 13,4 | 13 | 13 |
| oogmidden → neusgaten | 3,6 | 3,0 | 3,5 |
| oogmidden → mond | 5,7 | 5,0 | 5,5 |
| linkeroog t.o.v. linker koprand | 0,3 erbuiten | 1 erbinnen | 0 (oog = silhouet) |
| rechteroog → rechterrand silhouet | 2,6 | 1 | 2 |

Zwak punt: het linkeroog heeft geen zwarte buitenrand tegen de lucht (2 lichte randpixels), omdat de E6-pixels ongewijzigd moeten blijven.
