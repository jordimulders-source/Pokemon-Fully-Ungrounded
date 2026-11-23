# Gnometrotter Ice – sprite r8 (23 nov)

Basis: `../sprite_r7/gnometrotter_ice.png`. Uitgevoerd: precies de punten 1–3 uit `../keuring_r7/KEURING.md`. Bouwen: `python3 r8.py` → `gnometrotter_ice.png`, `_8x.png`, `r8_log.txt`. `python3 vel.py` → `vel.png` (r7 | r8, 8×).

## Telling t.o.v. r7 (27 px; silhouet 1 px = (55,30))
| zone | px | wat |
|---|---|---|
| schouder (punt 1) | 2 | (54,30) 1→7, (55,30) 0→1 |
| barst L (punt 2+3, x22–25, y43–50) | 16 | (23,44) 9→11; lijn (23;43)→(24;46)→(25,2;49,9): x23 rij 43–45, x24 rij 46–48, x25 rij 49, met 9-schaduwkant rechts ernaast (ook (24,44)) |
| barst R (punt 3, x43–48, y41–50) | 9 | lijn (43,8;41)→(46,6;47,9): x44 rij 41–43, x45 rij 44–45, x46 rij 46–47, met schaduwkant rechts |
| rest | **0** | |

Geen rechte kolom > 3 px meer in de barsten. Ze lopen in dezelfde richting als de modelbarsten (naar rechtsonder) en verspringen 1 px per 2–3 rijen. Eén lijn per dij.

## Twijfel
- Bij de rechterbarst valt het bovenste stuk (x44, rij 41–43) in het lichte 11-vlak; daar is alleen de schaduwkant zichtbaar.
- (46,48) 9→10: het schaduwpixel uit r7 viel binnen de zone en is meegenomen, zodat er geen 9-kolom van 4 px ontstaat.
