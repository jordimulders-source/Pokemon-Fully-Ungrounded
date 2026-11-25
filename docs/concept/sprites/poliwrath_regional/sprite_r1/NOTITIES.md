# Regionale Poliwrath (Ice/Poison) – sprite r1 (maker)

Model: `../referenties/gemini_gekozen_v2.png` (bevroren, Jordi 25 nov), **horizontaal gespiegeld** (Jordi: "gespiegeld uiteraard he").
Uitvoer: `poliwrath_regional_r1_{O1S1,O1S2,O2S1,O2S2}.png` (64×64, geïndexeerd, index 0 transparant), `vel.png`.
Beest: **62×60 px** op x 1–62, y 2–61 (2157 px). Ter vergelijking: regionale Poliwhirl 50×47 (1250 px), Gen 3-Poliwrath 50×47 (1488 px).
Varianten: **O1** = modelogen, **O2** = ogen Gen 3-Poliwrath naar verhouding; **S1** = modelspiraal, **S2** = spiraal regionale Poliwhirl (af).

## Aanpak (overnemen, niet hertekenen)
1. `meet.py`: natief Gemini-raster periode **10,24 px** (x en y), fase 9,25.
2. `natief.py`: per natieve cel de mediaan van de binnenste 6×6 modelpixels → `natief.npz` (beest 75×72 cellen). Lucht = bijna-wit verbonden met de rand.
3. `schrap.py`: **spiegelen**, dan 75×72 → 62×60 met de Gengas-methode (geen resampling): 13 kolommen en 12 rijen geschrapt die het meest op hun buur lijken, ≥3 uit elkaar, niet door de kop (rijen 7–19: ogen, neusgaten, mond), de spiraal (rijen 28–42, kolommen 25–46) en de ogen (kolommen 20–28, 39–47). Geschrapt (gespiegelde natieve coördinaten): rijen 0, 5, 23, 26, 43, 47, 51, 54, 57, 62, 65, 68; kolommen 0, 4, 8, 13, 16, 48, 52, 55, 60, 64, 67, 70, 73. Elke cel is een echte modelcel. (75→62 is ±17 %: tussen Gengas 13 % (goed) en Hauntflare 22 % (mis). Zelf gecontroleerd op `geschrapt_8x.png`: geen afgekapte uiteinden; de benen zijn het meest ingekort, 8 van de 12 rijen.)
4. `mat.py`: materiaal per cel uit de celkleur (geel incl. olijf, rood, ijs incl. oogwit-grijs, donker).
5. `basis.py`: A tinten uit de modelhelderheid per cel (lijf σ 1,0 gladgestreken zoals bij de Poliwhirl, geel σ 0,6 zodat de olijfschaduwlijnen van het model blijven, ijs en rood per cel); B omlijning zoals de Poliwhirl (lijf 1; geel 7 lichtkant / 1 schaduwkant; vuisten 11 / 1; kristallen 11 / 15; rood 14 / 1), lichtkant per pixel uit de 3×3-luchtburen, **licht van linksboven opnieuw bepaald na het spiegelen**; C reparaties (zie onder).
6. `varianten.py`: mond, ogen en spiraal als bovenlaag. `uitvoer.py`: png's, diffbewijs, afwijkingen. `vel.py`, `controle.py`.

## Spiegelen en licht
Het model is eerst gespiegeld, daarna is alles gereduceerd. De omlijning (selout lichtkant / zwart schaduwkant) is na het spiegelen per pixel berekend met licht van linksboven. De binnentinten komen uit de gespiegelde modelhelderheid; gemeten of dat licht na spiegelen verkeerd valt (gem. helderheid per helft van het onderdeel): vuist links L 198 / R 175, boven 199 / onder 176; vuist rechts L 194 / R 184, boven 202 / onder 176; lijf L 35 / R 41; geel kop L 185 / R 192 (de linkerkant is daar donkerder door de olijfschaduw onder het oog en de zwarte band, geen lichtval). De grote ijsvlakken zijn na spiegelen dus al licht linksboven; daarom is er binnen de vlakken niets herbelicht.
Ogen O2 en spiraal S2 komen ongespiegeld uit hun bron (beide kijken/draaien al goed; de Poliwrath-ogen zijn per oog op de gespiegelde modelpositie gezet, links op links, rechts op rechts).

## Palet: identiek aan de regionale Poliwhirl (af) (`palet.py`, 15 kleuren + transparant)
1 omlijning · 2/3/4 lijf · 5/6/7 geel · 8/9/10/11/15 ijs · 12/13/14 rood. Alle vier de varianten gebruiken alle 16.
Drempels (uit de histogrammen van het model): geel ≥196 → 5, ≥156 → 6, anders 7; lijf ≥56 → 4, ≥30 → 3, anders 2; ijs ≥222 → 8, ≥195 → 9, ≥150 → 10, anders 11; rood ≥125 → 12, ≥92 → 13, anders 14.

## Toegestane afwijkingen (Jordi)
- **Mond:** modelglimlach (rode cellen rijen 12–17) terug naar geel met de meest voorkomende geeltint van de buren; rechte rode lijn (13) op **rij 16** (= het middenstuk van de modelmond, x 20–32 in het model) van **x 15 tot 41** (mondhoek tot mondhoek van het model; bijna de hele kopbreedte). 26 px.
- **O1 (modelogen):** de cellen van de modelogen (linkervenster y 5–10, x 16–20; rechts y 4–10, x 32–40) opgeschoond: ijs/grijs → 8 (≥200) of 9, donker (<40) → 1. Het linkeroog is in het model een smal ver-oog tegen de kopband.
- **O2 (Gen 3-Poliwrath):** bron `graphics/pokemon/poliwrath/anim_front_gba.png`, linkeroog venster x 21–28, y 14–19; rechteroog x 38–46, y 14–19. Verhouding gemeten: Poliwrath oog 8 px op 33 px lijfbreedte op ooghoogte; kop hier 29 px op ooghoogte → 7,0 px (links) en 9·29/33 = 7,9 → 8 (rechts); hoogte 6 · 0,88 = 5,3 → 5. Dus per oog **1 kolom en 1 rij uit het eigen oog geschrapt** (links kolom 23, rechts kolom 44, beide rij 17; niet door de pupil). Omzetting: wit 1 → 8, grijs 2/3 → 9, pupil a → 1, lijn e → 1, en de blauwe c-pixels die direct aan het oogwit grenzen → 1 (anders is de onderrand open). Geplaatst met de **buitenrand op de buitenrand van het modeloog** (links x 16, rechts x 40), bovenrij 5.
- **S1:** de modelspiraal uit de reductie, niets veranderd (alleen tinten per cel).
- **S2:** modelrood in de buik → geel uit de omgeving; daarna de spiraal van `poliwhirl_regional/af/` 1-op-1 (rood x 24–35, y 31–41 in de af-sprite; per rij van het eerste tot het laatste rood, met het geel ertussen; tinten 5/6/7/12/13/14 letterlijk), midden (29,5; 36) op het midden van de modelspiraal (29; 31,5). Hij past zonder bijknippen; hij is wel kleiner (12×11) dan de modelspiraal (18×13), dus rechtsonder blijft meer effen buikgeel.

## Bewijs: varianten verschillen alleen in oog- en spiraalzone (`uitvoer.py`)
O1↔O2: 53 px, alle in de oogzone; S1↔S2: 123 px, alle in de spiraalzone; **0 px erbuiten** voor alle zes de paren. Silhouet: 0 px verschil met de geschrapte reductie in alle vier.

## Afwijkingen t.o.v. de kale reductie (andere index / ander materiaal)
| zone | O1S1 | O1S2 | O2S1 | O2S2 |
|---|---|---|---|---|
| ogen | 89 / 2 | 89 / 2 | 96 / 26 | 96 / 26 |
| spiraal | 28 / 0 | 151 / 98 | 28 / 0 | 151 / 98 |
| mond (rij 12–17) | 54 / 31 | idem | idem | idem |
| rest | 339 / 7 | idem | idem | idem |
"Andere index" buiten ogen/spiraal/mond is tint (σ-gladstrijken lijf/geel) en omlijning; de 7 materiaalwissels in de rest zijn allemaal omlijning (1) op de silhouetrand.

**Pixels die niet uit de reductie komen (buiten de toegestane oog/mond/spiraal-lagen):**
- Neusgat links (22,13) → 7: modelcel donker-olijf (lum 58) viel in de lijfklasse (werd lijf 4, blauwgrijs); nu 7 zoals het rechterneusgat en de Poliwhirl.
- Ruis: 15 losse tintpixels in lijf 3/4 en geel 5/6 naar de buurtint: (39,1), (43,8), (47,12), (48,13), (38,19), (24,23), (31,23), (56,31), (44,45), (45,46), (11,54), (51,55), (53,55), (50,56), (51,57).
Verder niets.

## Eigen zwakke punten
1. **Beenlengte:** 8 van de 12 geschrapte rijen vallen in de benen (kop en spiraal beschermd); de benen zijn daardoor iets korter dan in het model (verhouding kop/romp/benen niet exact 1-op-1).
2. **Kleine tintclusters (<3 px): 267–287**, grotendeels in de kristallen en vuisten (facetten van het model, niet gladgestreken), plus binnenlijnen 2/7. Geen lichte pixels op de buitenrand (controle.py).
3. **Lijfzwart leest blauwgrijs** (palet van de lijn, zoals bij Poliwhirl gekozen), het model is bijna zwart.
4. **O2-ogen** hebben een zware zwarte onderrand (Poliwraths blauwe c-ring omgezet naar 1); **O1-linkeroog** is smal (zoals het model), op 1× weinig wit.
5. **S2** is kleiner dan de modelspiraal en zit, net als in het model, tegen de linkerbuikrand; rechtsonder in de buik blijft effen geel.
6. Geel van de kop is grotendeels 5 (modelgeel lum ±200 is vlak); volume op de kop komt alleen uit de olijfschaduw van het model (onder de ogen, kin). Geen eigen schaduw toegevoegd (regel: schaduw uit de modelhelderheid). Voor een eindkeuring (DC) een aandachtspunt.
