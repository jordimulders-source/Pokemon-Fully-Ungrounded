# Gnometrotter Ice – sprite r9 (23 nov)

Basis: `../sprite_r8/gnometrotter_ice.png`. Jordi: "ijs is geen onderscheid meer tussen muts en rugijs, haar mag ook net iets meer. Lichaam moet nog ietsje meer ijsvorm". Bouwen: `python3 r9.py` → `gnometrotter_ice.png`, `_8x.png`, `r9_log.txt`. `python3 vel.py` → `vel.png` (model | r8 | r9, 8×).

## Telling t.o.v. r8 (69 px; silhouet 0)
| zone | px | wat |
|---|---|---|
| rugijs | 34 | rugkam rechts van de mutsgrens een tint donkerder (5→4, 4→3; schaduw achter de muts); lichte facetribbe 4 schuin van (47,10) naar (45,20), zoals de heldere rand in het model |
| muts | 8 | scheidingslijn in 2 (donkerste ijstint, niet zwart) op de mutsrand: x44 rij 9–14, x43 rij 15–17 (grens gemeten in het model: mutspunt eindigt rechts op x≈44 en buigt onder rij 15 naar links) |
| haar L | 7 | plukje: E linksboven, D midden, C schaduwkant rechtsonder |
| haar R | 12 | idem; de lichte E-band midden in het plukje (rij 17) is weg |
| romp | 8 | één extra facetgrens in het effen 7-vlak rechtsonder, als lichte naad 8 langs de modelbarst (39,34)→(46,30); het onderste facet heeft nu 8/7/6 |
| rest | **0** | indexen 0, 1, 6–11, 15 alleen in de romp (naad 8) gebruikt |

## Twijfels
- Het rugijs is nu grotendeels 3; het leest als schaduw achter de muts, maar het is een vrij effen donker vlak met één lichte ribbe.
- De grens zit 1–2 px links van waar hij in het model op de Rock-geometrie valt, omdat de sprite daar smaller is dan het model.
