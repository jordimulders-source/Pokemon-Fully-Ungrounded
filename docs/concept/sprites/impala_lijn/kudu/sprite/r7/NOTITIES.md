# Kudu sprite ronde 7: manen als losse lokken (maker)
Start: `r6/grid.json` (oog B). Model: `r3/model_A3.png`. Script `sprite/r7.py` (bouwt `r7/kudu_r7.png`, `grid.json`, `telling.txt`); vellen `sprite/vel7.py`.
Rastercoördinaten (beeld x = raster x + 6). Jordi: "nekharen zijn een grote pixel blur" · "echt nekhaar dat over de schouders valt" · "het moet los van het lichaam zitten" · bron "growlithe, arcanine".

## Studie (`studie_manen.png`, 6x)
- **Growlithe en Arcanine (Jordi's bron, bovenaan), gemeten op de indexen:**
  - Kraag/plukken zijn een eigen vorm óver het lijf, met een eigen omtrek.
  - Lichtkant: selout in de donkerste eigen tint (Arcanine a, lum 112; Growlithe a, lum 95). Schaduw-/onderkant: zwart (f).
  - Per pluk 2 vultinten: licht (7/8) als groot vlak links/boven, één tint donkerder (9) aan de onder-/rechterkant. Harde grenzen, geen gemiddelden.
  - Binnenlijn alleen waar pluk over pluk valt, in de lijntint (a), niet zwart.
  - Plukken eindigen in punten (zigzag aan de onderrand).
  - Waar de kraag over het oranje lijf valt: zwarte lijn, en het lijf ernaast krijgt een donkere lijftint (Growlithe c/d, rij 37-43; Arcanine e/d, rij 23-29). **Daardoor leest de kraag als los.**
- **Aanvullend, alleen voor de vorm** (Jordi: alle gens; Ponyta/Rapidash en Furfrou niet):
  - Sawsbuck: creme nekkraag rondom omlijnd over de bruine hals/borst.
  - Mudsdale: manen in lokken van 4-5 px langs de hals met 1-px lijnen ertussen; ze eindigen op de schouder.
  - Lycanroc: kraag met punten over schouder en borst.
  - Stoutland: mantel als aparte vorm met eigen omtrek.

## Hoe "los" is overgenomen
1. **Eigen omtrek rond de manen.** Schaduwkant zwart (0), lichtkant selout d, zoals de Arcanine-kraag:
   - Schouderkant: zwarte lijn van (27,33) via x26-25 naar de lokpunt (22,42).
   - Onderrand van de kam over de rug: (26-27,32) en (28-31,31).
   - Keelfranje tegen de halsstrook: zwart op x12 (rij 31-34) → x13 → x14 → x15 → x16 (rij 40).
   - Nekmanen tegen de halsstrook: selout d op x15 (rij 25-35) → x16 → x18.
2. **De halsstrook** (M, 2 px, r6) is niet aangeraakt. Hij ligt nu ingeklemd tussen de twee omtrekken, dus de hals leest onder de manen door.
3. **Lok over lok:** binnenlijn d (donkerste manentint), nooit zwart. Voorbeelden: de lijn tussen de kam en de schouderlok, en de lijnen tussen de lokken.

## Lokken (zie `lijnkaart_lokken.png`: rood = d, blauw = 0, over het model)
Lijnposities zijn per rij gemeten op het model (aandeel lijnpixels lum < 100, per halve cel). Vulling volgens de Arcanine-regel: licht l aan de lichtkant, m aan de schaduwkant en in de schaduw onder kop/kam.

| Lok | Plek (raster) | Modelbron | Vulling |
|---|---|---|---|
| KA keelfranje buiten | x9-11, rij 31-42 | lichte lok x10 (model L, rij 33-40), punt links (8,35-36) | l l, onderaan m |
| KB keelfranje binnen | x11-14, rij 35-40 | donkere lok tegen de hals (model d) | m |
| K-onder | x11-20, rij 41-46 | donkere onderkant onder de halsstrook, lijnen (14,44), (16,44), (16,45); punten (15,45), (17,45), (19-20,46) | m, lijnen d |
| M1 | x16-18, rij 25-38 | tussen de halsrand x15 en streng B (x18 → x19 vanaf rij 31) | boven m (schaduw kop), dan l l m |
| M2 | x19-21, rij 26-42 | tussen streng B en streng C (x22 rij 29-36 → x21 rij 37-41) | l l / l m; punt (20,42) |
| M3 schouderlok | x22-26, rij 32-42 | brede lichte lok over de schouder (model L x24-25), omtrek x26 | bovenaan m (onder de kam), dan l l l m; punt (22,42) |
| kam A-D | x21-31, rij 26-32 | liggende lokken met punten naar rechtsboven (model y ≈ 25, 27, 29, 31,5) | per band boven l, onder m; lijnen d ertussen |

**Afwijking van de meting:** de zwakke modellijn D (x23, rij 33-36) is weggelaten. Anders werden M3 en de schouderlok allebei 1 px breed; nu is het één brede lok van 3-4 px, zoals de plukken van Arcanine.

## Pixels
- 127 px anders dan r6, allemaal binnen de manenzone. **Buiten de manenzone: 0** (bewezen in `r7.py`, `telling.txt`).
- Manenzone = de r6-haarpixels (l/m/d, rij 23-47) plus 1 px ring, plus (22,43) (omtrek onder de lokpunt; model rij 42-43 x22-23 lijn).
- Oogpixels (alle varianten in `oog4.py`): niet geraakt.
- Palet: ongewijzigd, 15 kleuren incl. transparant. Manen l/m + d (lijn); zwart 0 alleen op de omtrek aan de schaduwkant.

## Eigen zwakke punten
- **Lokken zijn vrij lange rechte verticale banen** (x15, x19, x22). Dat volgt het model, maar het is regelmatiger dan bij Arcanine. Een keurder moet zeggen of het als haar of als streepjes leest.
- **Geen slagschaduw op het lijf naast de manen.** Growlithe en Arcanine hebben die wel (donkere lijftint naast de kraag). Hier zou dat D op de schoudervacht naast de zwarte omtrek zijn (x27-28, rij 33-41). Dat ligt buiten de manenzone en is dus niet gedaan; het is een voorstel voor een volgende stap.
- **De kampunten** volgen nog het r6-silhouet (trapjes). De punten naar rechtsboven uit het model zijn alleen via de binnenlijnen aangegeven.
- **K-onder (rij 41-45)** is een vrij groot m-vlak met weinig lijnen. Het model is daar ook donker en vlak.
