# Regionale Poliwag – sprite r2 (aanvulling op `../sprite_r1/NOTITIES.md`)

Opdracht (Claude, na r1 op 8×/12×): alleen spiraal, ogen en controle van de zwarte vlekken op de kop. Uitvoer `poliwag_regional_r2.png` (zelfde palet als r1), `vel.png` (r2 | r1 | model op 8×, ver/nabij oog en buik op 12× naast het model, 1× licht/donker, naast Poliwag/Ninjask/Dundragoon). Bouw: `build.py`; bewijs: `diff_r1.py`.

## Diff t.o.v. r1 (`diff_r1.py`)
spiraal (x3–16, y19–32): 9 px · ver oog (x2–7, y7–14): 6 px · nabij oog (x13–20, y7–14): 12 px · **buiten deze zones: 0 px**.

## 1. Spiraal
Pad opnieuw uit de **roodfractie per modelcel** (≥ ±45 % rood/roze), nu met de trapjes van het model: bovenboog (6,21)(7,21) → (8–10,20) → (11,21)(12,21) → (13,22)(14,23)(14,24); tweede winding boven (7,24)(8–10,23)(11,24); midden (9,25)(10,26)(10,27) in plaats van het rechthoekige haakje. Rechte stukken > 2 px alleen waar het model ze heeft: links col 4 (rij 23–27), rechts col 15 (rij 25–28), tweede winding col 12 (rij 25–28), onderbalk (7–10,30). Windingen (±2,5) en buiteneinde rechtsonder (12,31) onveranderd. Weg t.o.v. r1: (7,20), (7,23), (11,23), (6,24), (12,24), (8,25), (10,25); erbij: (7,21) roze, (7,24), (11,24). (7,20) was een grijze ruiscel in het model → ijs.

## 2. Ogen (cel voor cel = kleur in het midden van elke modelcel)
- **Nabij oog:** ronde omtrek (rij 8: x15–18, rij 9–12: x14–20, rij 13: x15–20, rij 14: x16–18), zwarte pupil x15–17 met grijze onderkant (rij 12), ijsring rechts/rechtsboven, witte ring rechtsonder. **Glans op de modelplek (14,10)(15,10)(15,11)**; daardoor staat de linker omlijning op rij 10 open (wit grenst aan geel (13,10)) – gemeld, niet dichtgezet. Ijsstipje (15,9) uit het model. Afwijkend van de modelcel: (14,13) geel-donker i.p.v. zwart (cel 60/40, voor de ronde hoek), (20,13) zwart i.p.v. geel en (19,14) ijs-donker i.p.v. geel (onderrand rechts dicht, het model heeft daar een dunne zwarte/blauwgrijze lijn), (18,14) zwart (cel gemengd). = 4 cellen.
- **Ver oog:** (5–7,8) zwart, (5,9) ijs, (6,9) blauwgrijs, glans (6,10) wit, pupil (5,10)(6,11)(5,12) zwart met (5,11) grijs, ring links (4,10)(4,11) blauwgrijs, (4,12) lichtijs, onder (4,13)(5,13) wit. Afwijkend: (4,10) ijs-donkerst i.p.v. blauwgrijs (buitenrand tegen lucht), (7,9) en (3,12) zwart i.p.v. donkergrijs (de grijze modelrand als omlijning). = 3 cellen.

## 3. Zwarte vlekken op de gele kop
Gecontroleerd tegen het model (8× en per cel): bovenvlek rechts (x15–20, y4–9, sluit aan op het nabije oog), vlek rechts in het geel (x21–26, y9–12), insnijding rechtsonder (x25–27, y15–18) en het zwarte masker om het verre oog (x1–7). Alle kop- en lijfpixels hebben 0 materiaalwissels t.o.v. de kale reductie (`afwijking.py`, zone "rest": 0), dus vorm en plek komen uit het model; niets gecorrigeerd.

## Zwakke punten
- Nabij oog: de open linkerrand bij de glans (modelplek) kan als "kapotte" omtrek lezen; alternatief = (14,10) zwart en glans alleen (15,10)(15,11) (zoals r1-variant).
- Ver oog blijft klein met een kleine pupil: zo staat het in het model (vooral ring zichtbaar in de draai).
