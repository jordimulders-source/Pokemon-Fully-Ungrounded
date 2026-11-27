# Sneeuwmonster fase 1 (Ice) frontsprite, ronde 2

Basis = r1 (bevroren), plus vier benoemde reparaties, alles uit het model. Silhouet-diff t.o.v. r1: **0**.
Bestanden: `sneeuwmonster_r2.png` (ogen LB+RB), oogvarianten `oog_LA_RA.png`, `oog_LA_RB.png`, `oog_LB_RA.png` (alleen oogpixels anders: 4/2/2 px), `mond_shroomish.png`, `mond_chinchou.png` (zelfde mondpixels en regel als r1), `vel.png` (r2 8× | r1 8× | model / close-ups kop en lijf 12× naast het model / 1× licht+donker / monden 8× / oogvarianten 12× + model), `bouw.py`, `maakvel.py`.
Bouwen: `cd sneeuwmonster && python3 sprite_r2/bouw.py && for v in "LA RA" "LA RB" "LB RA"; do python3 sprite_r2/bouw.py $v; done && python3 sprite_r2/maakvel.py`.

## Afwijkingen t.o.v. r1: 129 px
Per zone (`zones.py`): **sneeuwpluk 5, kop 36, ogen 18, lijf+armpjes 54, knopen 16 (alleen sneeuwtint rond de knopen, de steentjes zelf ongewijzigd), voetjes 0.** Per stap: volume 119, sneeuwpluk 5, armstompje 3, ogen 4 (de oogzone telt ook volumepixels rond de ogen mee).

## 1. Ogen (opnieuw gemeten op het 1024-model)
Dekking per spritepixel van donker (L < 160, verzadiging < 45) + wit hooglicht in het oog:
- rechts (x30–33, y23–26): .30 .73 .67 .13 / .79 .72 .98 .36 / .84 1.0 1.0 .32 / .43 .94 .74 .10 → ±3,3 breed × 3,8 hoog
- links (x22–24, y22–26): – .47 .23 / .39 .38 .96 / .54 .76 1.0 / .39 .98 .80 / – .29 .12 → ±2,5 breed × 3,8 hoog
De meting valt tussen twee maten, dus varianten (vel, onderste rij, 12×):
- **RB (gekozen):** 3×4 (dekking ≥ .40; de rechterkolom .32–.36 valt weg), linkerhoeken eraf. **RA:** rond 4×4-steentje (≥ .30, vier hoeken eraf).
- **LB (gekozen):** 2 breed × 4 hoog, (23,22) als top (.47). **LA:** 3 breed × 4 hoog (≥ .38, drie hoeken eraf); raakt dan de buitenlijn van het gezicht (x21), terwijl het model daar ±1 px sneeuw heeft. Daarom LB.
- Tint per pixel uit de gemiddelde helderheid van de donkere modelpixels: < 48 zwart, < 76 steen donker, anders steen midden (lichtere rand bovenaan en onder in het oog, zoals het model). Glans op het zwaartepunt van het witte modelhooglicht: rechts (31,24) binnen het oog; links valt het zwaartepunt (22,8; 23,4) buiten LB, dus de dichtstbijzijnde oogpixel met ≥ 2 oogburen, (23,23).
- r1-oogpixels buiten de nieuwe vorm → sneeuwtint uit het model.

## 2. Sneeuwpluk
Binnenlijnen (natieve sneeuwlijnpixels van het model gemapt, 1 px, 8-samenhangend aan de buitenlijn vast):
- A links|midden: model (46,19) (46,20) (47,21) → (30,13) (31,14); sluit aan op (29,13).
- B midden|rechts: model (52,20) (51,21) → (34,13) (33,14); sluit aan op het zwart (34,12).
- C onderkant linkerbolletje: model (43,24) (44,25) → (28,16) (28,17); sluit aan op het zwart (27,15).
Randen in de modeltint: (28,12), (35,13) en (36,13) zijn in het model blauw (natief (43–44,18) en (54–56,19)) en waren in r1 zwart door de buitenlijn-/om-en-om-regel; nu sneeuwlijn.

## 3. Armstompje rechts
Model-binnenboog natief (56,56) → (67,65) gemapt en gedund tot 1 px: (36,36) (37,37) (37,38) (38,39) (38,40) (39,41) (40,42) (41,43) (42,43), aansluitend op (43,42). Gebroken r1-stukjes die niet op de boog liggen ((39,40) en (41,42)) → sneeuwtint uit het model.

## 4. Volume
**Meting:** de lichte sneeuw in het model is vlak (L 240–245, ruis ±2; 602 natieve px op 243–245 en 295 op 240–242, verspreid). Een subtiele gradiënt van licht naar linksboven is er dus niet; de enige helderheidsinformatie is de schaduw (L ±200) en de smalle overgang (212–236).
**Werkwijze (geen handwerk):**
- Schaduw (3) = modelpixels met L < 212, precies zoals in het model. Modelovergang 212–236 = midden (4), nooit lichter.
- Licht (5) of midden (4) voor de lichte modelpixels: de modelhelderheid per pixel, verzacht over het eigen vlak (genormaliseerde gauss, σ = 2 px, alleen sneeuwpixels van hetzelfde vlak; omlijning, steen en achtergrond tellen niet mee). Dicht bij de modelschaduw zakt die waarde, ver ervan blijft hij hoog. De grens volgt dus de vorm van de modelschaduw: gebogen, licht als bolling linksboven op de kop, midden als overgang naar de sikkel rechts/onder.
- **Drempels:** kop (y18–31) licht als verzacht ≥ **236**, lijf (y32–46) ≥ **235**; sneeuwpluk en voetjes blijven r1. Ontkorreld binnen de vlakken (vlekjes < 3 px).
- Resultaat: kop licht 95 / midden 70 / schaduw 64 px, lijf licht 97 / midden 112 / schaduw 81 px.

## Controle (`controle.py`)
64×64, P, transparency 0, 9 kleuren incl. transparant (palet ongewijzigd t.o.v. r1). Geen lichte buitenrand, geen losse zwarte pixels, zwart 10,9 %. Kleine vlekjes: sneeuwlijn 6× (lijnstukjes uit het model), steen (ogen/knopen), wit (31,24) = glans, (20,36) wit en (19,38) midden in het linkerarmpje, (43,35) schaduw tussen armlijn en buitenlijn: allemaal modelplekken.

## Twijfels (eerlijk)
- **Volume is afgeleid, niet gemeten:** het model heeft geen lichtgradiënt; de middentint is de verzachte afstand tot de modelschaduw. Op het lijf ligt het licht daardoor als bolling in het midden-links (niet tegen de linkerrand): de linkerrand onderaan wordt midden door de eigen schaduw van het linkerarmpje in het model, de bovenkant door de schaduw onder de kop. Op 8× leest het als volume, maar het is randje pillow-achtig. Wordt het afgewezen, dan kan ik terug naar de r1-tinten of de drempel per vlak verlagen (minder midden).
- **Glans linkeroog:** ligt, zoals in het model, linksboven tegen het witte gezicht en leest op 8× als hoekje uit het oog, niet als glans (r1-twijfel blijft).
- **Sneeuwpluk:** de drie bolletjes zijn nu gescheiden door lijntjes, maar op deze schaal blijven het bolletjes van 3–4 px; het rechterbolletje is midden-tint (zoals het model, in de schaduw).
