# Regionale Poliwhirl – sprite r3 (maker): kleinere ogen
Basis = `../sprite_r2/r2_S2.npy` (spiraal S2, Jordi "spiraal prima"). Alleen de oogzone (x 11–21 en 24–34, y 0–9) verandert: E6 55 px, E5 63 px, EM 69 px verschil met r2_S2, **0 erbuiten** (`uitvoer4.py`). Bouwen: `python3 uitvoer4.py && python3 vel4.py`.
Kop rond het oog: uit het model (r1/r2-basis met het modeloog, `MODELOOG`); modelwit dat niet onder het nieuwe oog valt → buurtint uit de kop.
Modelplek opnieuw gemeten op de witte oogring in het model: links (15,7; 5,1) → 16 gebruikt (anders steekt het oog 1 kolom in de lucht), rechts (29,2; 4,8). Dat is ±0,5 rij lager dan in r2.

## E6: Poliwhirl-oog 6×6 (24 px per oog, bron 37)
Weggehaald uit Poliwhirls eigen oog: de middelste rij en kolom (rel. rij 3 en kolom 3 van het 7×7-oog). Daardoor blijft zijn eigen rand rondom dicht (de randpixels zelf blijven staan), niets getekend.
Weg uit gba links: (23,13) (23,14) (23,15) (20–26,16) (23,17) (23,18) (23,19); rechts: (41,13) (41,14) (41,15) (38–44,16) (41,17) (41,18) (41,19). Geplakt op x 14–19 y 3–8 en x 27–32 y 2–7.

## E5: Poliwhirl-oog 5×5 (15 px per oog)
Weg: rel. rijen 1 en 3, kolommen 3 en 4. Links: (23,13) (24,13) (21–25,14) (23,15) (24,15) (20–26,16) (23,17) (24,17) (23,18) (24,18) (23,19) (24,19); rechts hetzelfde, 18 kolommen verder (38–44). Glanspixel en zwarte onderkant van de pupil blijven. Geplakt op x 14–18 en 27–31, y 3–7.

## EM: modeloog, kale reductie (42 px samen, ±21 per oog)
Per cel het meerderheidsmateriaal van de modelpixels (`modeloog.py`: zwart L<70 → 1, wit/lichtgrijs → 8, grijs → 10, geel = kop laten staan), op het spriteraster, cellen x 13–18 / 26–31, y 2–7. Technisch: wit op de silhouetrand → 1: (26,2), (14,3), (14,4), (14,5). De zuiverheid van de modelogen is maar 0,7 (Gemini tekende ze op een fijner raster dan de rest), dus de reductie is grof: de witte ring wordt een halve maan.

## Zwakke punten
1. Het linkeroog ligt in het model op de silhouetrand. Bij E6 en E5 komt Poliwhirls witte ring daardoor tegen de lucht: lichte randpixels (14,5) en (14,6) bij E6, (14,4) en (14,5) bij E5. Niet veranderd, omdat het oog 1-op-1 moet blijven.
2. E5 (15 px) leest als ruitje; E6 is nog een rond Poliwhirl-oog.
3. EM is grof en ongelijk links/rechts (meerderheid per cel van een fijner getekend oog).
