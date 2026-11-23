# Gnometrotter Ice hybride – r2 (B), 23 nov

Opnieuw afgeleid: `hybride_r2.py` begint bij `../sprite_hybride/gnometrotter_ice_hybride_gatdicht.png` en voert dan uit: (0) alles buiten het lijfmasker (`deel_r2.npy`, delen 2–8, 10–13, 20) = A r3 (`../sprite_r3/`); B1–B6 uit `../keuring/KEURING.md`; een slotronde voor vlekjes < 3 px.
Uitvoer: `gnometrotter_ice_hybride.png` + `_8x.png`.

**Diff t.o.v. de oude B: 129 px. Silhouet: 0 px.** Buiten het lijf is B gelijk aan A r3 (0 px verschil). In de baard-box (x16–31, y22–41) wijkt B op 16 px af van A, en dat zijn allemaal roze lijfpixels.

| punt | px | wat |
|---|---|---|
| buiten lijf = A r3 | 57 | A1, A2 en A4 (baard, notch en stok vallen buiten het lijfmasker) |
| B1 baardrand terug | 9 | (31,29–32), (29,32), (30,33), (27,35–36), (26,36) = A: de rand in 2 en (26,36) D |
| B2 hand R | 9 | zoals A5 (valt binnen het masker) |
| B2 pegel (hybride model, smaller) | 16 | ijs (21,42) C, (21,43) D, (20,44) D, (21,44) C, (20,45) D, (21,45) C (6 px) + rand in 2 tegen blauw (10 px) |
| B3 arm L | 8 | (13–17,31–33) = A: bovenrij 6, midden 8, onderrij 7; het dambord is weg |
| B4 rechterdij | 10 | (41–44,48) 9→B; (47–48,48) en (45–48,49) 9→A; (49,48) blijft 9 |
| B5 linkerdij | 8 | (21–24,47) 9→A; (25,44), (26,45), (25,46) en (20,47) naar de meerderheid van de buren. (22,42–43) vallen onder de pegelrand |
| B6 lijfvlekjes | 8 | (48,25), (49,26), (48,27), (40,26), (41,27), (40,25) en (33,21) naar de meerderheid van de buren. (54,30) lag ingesloten tussen 6: (53,30) 6→8 (model 183, geen naad), daardoor hoort hij nu bij het 8-facet |
| slotronde vlekjes | 4 | (32,23–24), (51–52,29) |

## Pixels die niet rechtstreeks uit het model komen
- Meerderheid-van-de-buren bij B5 en B6 (regel, niet gemeten).
- De verdeling van de tinten en de 2-rand van de pegel (zelfde regel als bij A).

## Restpunten (niet aangepast)
- Vlekjes in tint 8 van 1 px: (48,25), (49,26) en (48,27). Hier is de 7 opgenomen in 8, maar die 8-pixels liggen tussen naden in 6.
- Vlekjes in tint A van 1 px: (49,36), (42,40) en (47,41).
- Arm L (17,30) staat in 6 en in A in 8 (buiten de keuringsbox rij 31–33).
