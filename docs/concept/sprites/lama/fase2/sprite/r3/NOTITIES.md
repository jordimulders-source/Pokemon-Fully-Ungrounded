# Llamauler r3 (19 nov): verkleining van model_v3 (Palpaca-aanpak)

Opdracht: `../OPDRACHT_v2.md`. Model: `../../gemini/poten/model_v3.png` (bevroren). r1 (plat, glad, lijntjespoten) is afgekeurd; r3 is opnieuw vanaf het model gebouwd, niets uit r1 overgenomen.

## Bestanden
- `lama.png` (64×64, geïndexeerd, index 0 transparant), `normal.pal` (JASC, 16 regels, 15 kleuren in gebruik).
- `onderlaag.png` = kale reductie (stap 1), `stap2.png` = + technische regels (buitenlijn, ruis), `lama.png` = + handreparaties.
- `vel.png`: model | r3 | r1 (8×, zelfde hoogte) · close-ups 12× model op spriteraster | r3 (kop, lijf, poten) · 1× en 2× op licht en donker.
- Scripts (vanuit `scripts/`): `python3 bouw.py && python3 opschonen.py && python3 repareer.py && python3 vel.py`. Hulpjes: `meet.py` (meting per spritepixel; `python3 meet.py x0 x1 y0 y1` drukt gem./min. helderheid), `naast.py` (uitsnede model op spriteraster naast de sprite), `check.py` (losse pixels, vlakjes, kleuren), `afwijking.py` (telling per zone), `toon.py`.

## Werkwijze
1. **Raster**: model y 28–1003 → 62 rijen (S = 15,74 modelpx per spritepixel), rij 2–63; kolommen gecentreerd op het midden van de modelinhoud. De witte naad van het plakwerk (y ±815, `model_v3.py`) is technisch dichtgezet (witte pixel met model ≤ 6 px erboven én eronder krijgt de kleur erboven).
2. **Silhouet = modelalfa**: blok gevuld bij ≥ 45 % niet-wit; niet gladgestreken. Alfa-diff onderlaag → lama = 0 (assert in `repareer.py`). De wolbogen van rug, romp en buik blijven als schulpen/inkepingen.
3. **Binnenkant uit het model** (`bouw.py`): per blok de klasse met de meeste modelpixels (wol / verre poot / rood / geel / groen / blauw / grijs).
   - Wol: gem. helderheid van de wolpixels zonder lijn → licht (≥ 162) / basis (≥ 146) / schaduw (≥ 118) / diep.
   - Binnenlijnen: waar ≥ 12 % van het blok modellijn is (helderheid < 100, niet aan de buitenrand), uitgedund tot 1 px loodrecht op de lijnrichting (alleen de cel met het meeste lijn houdt hem). Zo komen kuif-, been-, buik- en romplijnen uit het model.
   - Kleed: aandeel lichte draden (rood ≥ 105) per blok → rood licht/midden/donker; onderaan (y ≥ 35) alleen de lichte strepen die het model daar heeft (kol 34 en 39). Handschoenen: rood op gem. helderheid.
   - Verre poten: 3 (lichte kant) / 2 (lijf), geen binnenlijnen (2–3 px breed); donkerder dan de nabije poten zoals in het model.
4. **Technisch** (`opschonen.py`): buitenlijn 1 px (richting van de lege buren in 5×5: lichtkant links/boven → zachte modellijn 2, elders donker 1; daarna gladgestreken zodat 1 en 2 niet om en om staan); losse wol-/lijnpixels naar de buur.
5. **Hand** (`repareer.py`, elk punt met de modelmeting erbij): oog, kwastjes, halsband + pompons (toegestane afwijking), hoefnagels.

## Palet (gemeten in het model, mediaan van de modelpixels per helderheidsband/klasse)
| idx | rol | RGB | bron |
|---|---|---|---|
| 0 | transparant | 152 208 160 | |
| 1 | lijn donker (schaduwkant, oogleden, pupil, polsband) | 55 21 22 | wolpixels helderheid < 45 (donkerste modellijn) |
| 2 | zachte lijn (lichtkant), verre poot | 105 60 37 | 45–75 (modelomlijning) |
| 3 | binnenlijn / diepe schaduw, verre poot licht | 135 81 53 | 75–100 (binnenlijnen) |
| 4 | wol schaduw | 179 114 75 | 100–125 |
| 5 | wol basis | 217 157 102 | 145–165 |
| 6 | wol licht (wolbollen) | 231 181 128 | 175–200 |
| 7 | oogwit, hoefnagels | 244 234 226 | oogwit (meest voorkomend in het oog) |
| 8 | iris | 80 56 56 | iris |
| 9 | rood donker | 115 34 42 | rood, laagste kwartiel |
| 10 | rood | 166 54 59 | rood, derde kwartiel |
| 11 | rood licht | 206 83 77 | rood, hoogste kwartiel |
| 12 | geel | 251 222 98 | geel van band/pompon |
| 13 | groen | 56 106 61 | groen (blokmediaan) |
| 14 | blauw | 58 84 144 | blauw (blokmediaan) |
| 15 | grijs (polsband, verre hoefnagels) | 87 82 86 | grijs, hoogste kwartiel |

Geen kleur afgeweken van de meting. Contrast wol: licht 180 / basis 159 / schaduw 123 / diep 90 / lijn 67 (helderheid).

## Afwijkingen van de kale reductie (per zone, px)
| zone | px | buitenlijn | ruis | hand |
|---|---|---|---|---|
| kop | 223 | 57 | 7 | 15 |
| hals + halsband | 219 | 26 | 8 | 66 |
| lijf + kleed | 695 | 71 | 8 | 0 |
| voorpoten | 162 | 44 | 1 | 4 |
| achterpoten | 110 | 55 | 1 | 0 |
| totaal | 1409 | 253 | 25 | 85 |

Hand (85 px), elk naar het model:
- **Oog (7)**: zwaar vlak ooglid 1 op (16–19,14) (model x 15,8–19,8, y 14,0–14,4); rij 15: oogwit 7 (16) en (19), pupil 1 (17), iris 8 (18) (model iris x 17,0–18,3, wit links en rechts). Oog 4×2 zoals het model (2 px hoog).
- **Kwastjes (8)**: links (11,5) knoop, (11,6) licht, (11,7–8) rood (model x 9,7–12,3, y 4,2–9,0); rechts (23,5) knoop, (23,6) licht, (24,6), (23–24,7–8) rood/donker (model x 22,8–26,2).
- **Halsband (30)**: rood/geel/groen elk 1 px op de gemeten middenlijn (kol 13–20 geel op rij 30, kol 21 op 29, kol 22–23 op 28).
- **Pompons (37)**: 2×2 op het gemeten kleurzwaartepunt, rand zacht 2 links/boven en donker 1 rechts/onder: rood links (11–12, 32–33), rood rechts (24–25, 29–30), geel (14–15, 33–34) met touwtje (15,32), groen (18–19, 33–34), blauw (22–23, 31–32); resten van de reductie ernaast → rand.
- **Hoeven (4)**: crème nagels (13,62) en (15,62) onder de nabije handschoen, grijze (23,61) en (25,61) onder de verre (modelposities).
- Kleedkwastjes niet aangeraakt: de reductie zet ze al op de modelplek ((32,41)–(32,42) en (42,41)).

## Maat
Box 44×62 (x 10–53, y 2–63), 1409 px (oude Llamauler 41×62, 1184 px; r1 44×62, 1379 px). 15 kleuren + transparant.

## Zwakke punten (nog open)
- Halsband en pompons zijn met 3 strepen van 1 px en 2×2-stippen met rand dikker en feller dan in het model (± 1,7 px band); dat is de afgesproken afwijking, maar op 1× trekt de band veel aandacht.
- Kleed: het aguayo-motief van het model (ruiten) valt op 1× weg; het patroon is nu gevlekt rood boven en donker met 2 lichte strepen onder (gemeten, niet getekend).
- Wol: de bollen komen uit de toonbanden en zijn deels gevlekt (kleine lichte plekjes in hals en romp); de binnenlijnen van het model zijn op deze schaal maar deels aaneengesloten (been-/buiklijnen wel, kleine wolkrulletjes niet).
- Nabije polsband: grijs alleen links boven, rest zwart (zoals het model, maar op 1× een donker blok); verre polsband volledig zwart.
- Niet gekeurd door een onafhankelijke keurder.
