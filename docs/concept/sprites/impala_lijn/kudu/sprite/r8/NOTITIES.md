# Kudu sprite ronde 8: manen als één vorm met licht gerafelde rand (maker)
Start: `r6/grid.json` + oog K4 (Jordi; oogvlak 1-op-1 uit `r6/kudu_r6_oogK4.png`). Model manenvorm: `r3/model_A3.png` (= de r6-haarpixels).
Scripts: `sprite/r8lib.py` (gereedschap, klasse `Vorm`), `sprite/r8.py` (varianten), `sprite/vel8.py` (pngs, vel, telling, bronnen).
Rastercoördinaten (beeld x = raster x + 6).

## Wat Jordi zei (letterlijk, via Claude)
- Over r7: "wel goed, je kijkt naar de andere pokemon en doet vervolgens compleet iets anders"; "met allemaal rechte pixellijnen, want ja dat hebben alle pokemon".
- "wat andere pokemon doen is geen banen, meer gewoon de vorm een beetje gerafeld".
- "pyroar heeft bijv ook manen maar dat is gewoon een lang hangend kapsel" (vrouwtje); daarna "nee hij moet de pyroar niet nadoen"; "het is meer van dat soort manieren kunnen er allemaal zijn".
- Eerder: "het moet los van het lichaam zitten"; bron Growlithe/Arcanine; Ponyta, Rapidash, Furfrou niet.
- **Pyroar: niets overgenomen** (geen pixels, geen vorm).

## Methode (alle drie de varianten)
1. **Vorm** = het r6-haar (model A3: achter de oren, kam over de hals, over de schouder, keelfranje onder de keel). De halsstrook (2 px M) is beschermd: geen enkele pixel ervan is veranderd (script-bewezen). Losse r6-lijnpixels midden in het haar horen bij de vorm.
2. **Vlak (Gen 3-schaduw)** = de vultinten van de Arcanine-rugpluk (`arcanine/anim_front_gba.png` x33-60, y2-26), 1-op-1 geplaatst met linksboven op (7,23); omgekleurd 7/8→l, 9→m. Alleen vultinten, géén Arcanine-lijnen (dus geen banen). Licht linksboven, m-sikkel rechtsonder zoals in de pluk. Haarpixels die de pluk niet dekt krijgen de tint van de dichtstbijzijnde pluk-pixel ("veld-herhaald": A 11, B 19, C 8 px).
3. **Rand licht gerafeld** = kleine randstukken 1-op-1 uit Arcanine/Growlithe (vorm + vultinten), herhaald/verschoven waar nodig: de pixels van het stuk komen erbij (punt steekt max. 1 px buiten het haar), de achtergrond rond het stuk snijdt max. 1-2 px in (inkeping). Niets zelf getekend.
4. **Omtrek** per regel zoals de Arcanine-kraag: rand aan licht/boven = d (donkerste manentint, selout), rand rechts/onder = 0 (zwart). Geen extra lijn waar de manen tegen een bestaande donkere lijn (kop/kaak) liggen.
5. **Los van het lijf**: zwarte schaduwkant tegen de schouder + lijf direct rechts daarvan D (de slagschaduw die Arcanine/Growlithe naast de kraag hebben, e/d resp. c/d). Weggesneden haar toont achtergrond of lijf (M/D, bij de poten D).

## Gebruikte randstukken (gba-sprites, omgekleurd 7/8/1→l, 9 (Growlithe ook 8)→m, a→d, f→0)
| Code | Bron | Wat |
|---|---|---|
| A_UP2 | Arcanine (14,4)-(17,6) | puntje bovenop de kopmanen, schuin naar rechtsboven |
| A_LEFT | Arcanine (4,37)-(7,42) | pluk links aan de borstkraag, punt naar links |
| A_DOWN | Arcanine (19,47)-(23,51) | punt onderaan de borstkraag |
| A_RIGHT | Arcanine (54,16)-(59,23) | rechterrand rugpluk met twee punten |
| A_BUMP | Arcanine (54,17)-(58,20) | kleine bult uit diezelfde rechterrand (ook gespiegeld) |
| G_UP | Growlithe (25,12)-(29,14) | puntje kuif |
| G_LEFT | Growlithe (18,36)-(22,41) | borstpluk, punt naar links |
| G_DOWN | Growlithe (23,43)-(28,46) | onderrand borstpluk |

## Varianten (plek = linksboven van het stuk in het raster; per pixel de bron in `bronnen.txt`)
**A – pluizige kraag met puntjes (Arcanine).** Kampunten A_UP2 op (22,25), (26,26), (29,28); franjeplukken A_LEFT op (7,33) en (7,39); nekrandplukken A_LEFT op (15,27), (15,32) (inkepingen langs de halsstrook); onderpunten A_DOWN op (8,41), (12,42), (16,42); punt onder de kam over de rug A_DOWN (25,27); schouderpunten A_RIGHT (21,31), (19,36); schouderbult A_BUMP (22,31); inkeping franje rechts A_BUMP (9,31). 250 px anders dan r6+K4.
**B – lang hangend kapsel, licht gerafelde onderrand.** Zijkanten zo glad mogelijk, punten vooral onderaan: A_DOWN op (8,41), (11,42), (14,42), (17,42); één kampunt A_UP2 (26,26); onder de kam A_DOWN (25,27); onderste schouderlok A_RIGHT (19,36); alleen kleine A_BUMP-bulten/inkepingen om rechte stukken te breken: (23,31), (9,31), gespiegeld (7,30), (8,37), (15,29). 242 px.
**C – zachte plukken (Growlithe).** Kampunten G_UP (21,25), (26,26); franjeplukken G_LEFT (7,32), (7,37); nekrandpluk G_LEFT (15,29); onderrand G_DOWN (9,42), (14,42); schouder/kam uit Arcanine: A_RIGHT (21,31), A_DOWN (25,27), A_BUMP (22,31), (27,27), (9,31). 233 px.

## Controle (`telling.txt`)
- Buiten de manenzone (r6-haar + 1 px ring): **0 px** anders, alle varianten. Oogvlak = K4, 0 px anders. Halsstrook: 0 px anders.
- Rechte lijnstukken (d/0) > 3 px in de manenzone, horizontaal of verticaal: **geen**, alle varianten.
- Palet ongewijzigd (15 kleuren incl. transparant); manen l/m/d + 0.

## Eigen zwakke punten
- De gerafelde rand is subtiel: punten steken maar 1 px uit (meer kan niet binnen de zone van het model) en inkepingen zijn 1-2 px. Op 1x leest het vooral als één vorm met een onrustige rand, niet als duidelijke plukken.
- Het vlak is de Arcanine-pluk, dus de m-vlek ligt waar die in de pluk ligt (midden-rechts van de nekmanen) en de franje is bijna helemaal licht. Een keurder moet zeggen of dat als Gen 3-sikkel leest of als vlek.
- Lijnen langs de halsstrook zijn alleen gebroken door inkepingen; de halsstrook zelf blijft een rechte strook (niet aangeraakt).
- De slagschaduw (D) naast de schouderlijn ligt binnen de ring; verder naar rechts op de schouder kon niet (buiten de zone).
