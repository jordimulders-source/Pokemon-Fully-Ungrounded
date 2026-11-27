# Uku Pacha r6: notitie van de maker

Jordi over r5 (letterlijk): "zie je wel dat dit zou lukken. de tong van links vertaalt nog niet super en de pupil van rechts mag 1 pixel meer naar links, daarnaast is zijn mond nog niet helemaal duidelijk en de streep op zijn hoofd nog niet helemaal af, die mag met een lichtere lijn hersteld worden, daarna mag die naar de eindkeuring".

**Bestand:** `uku_pacha_r6.png` (64×64, geïndexeerd, index 0 = transparant, 16 kleuren incl. transparant, palet identiek aan r5). Script: `koppen6.py` (op `../r5/raster_af.txt`, controleert per pixel de oude waarde) → `raster2png.py raster_af.txt uku_pacha_r6.png` → `check.py`, `vel.py`. Hulp: `near.py` (dichtstbijzijnde paletkleur van het model per spritepixel).
**Vel:** `vel.png` (r6 | r5 | model op 8×; linkerkop + tong en rechterkop op 12×, tong op 20×, telkens r6 | r5 | model; r6 op 1×/2× licht en donker).
**Diff r5 → r6: 13 pixels**, alleen in de koppen; alpha-diff 0; verder niets veranderd. Geen lijn weggehaald: twee lijnpixels zijn 1 px verschoven naar de modelplek (zie 3a en de tong).

## 1. Tong linkerkop (2 px)
Model (natieve cellen): steel (12–15,39) → (11–12,40) → vork bij (11,41); linkertip (9–10,41–42), ondertip (12,41–43); zwart tussen de tips (10–11,42). Geprojecteerd naar de sprite: steel (6–7,24) → (5,25) → (4,26), linkertip (3,26), ondertip (5,27), zwart ertussen (4,27).
- r5 had op (4,26) een K, die de steel van de tips afknipte, zodat de tong als losse paarse spikkels las. Nu: (4,26) K → P, (5,26) P → K. Het model is daar overwegend zwart (K 1,17 van 2,1 cel); daarmee wordt het een V-vork.
- De tong is nu één doorlopende paarse streng van de bek naar linksonder, met de vork (3,26) | (5,27). Het silhouet is ongewijzigd.

## 2. Pupil rechteroog (2 px)
(40,5) K → Y en (39,5) Y → K. De pupil staat nu tegen de zwarte rand (38,5), zoals de spleet in het model links in het gele oog staat.

## 3. Welke kop en welke streep
Volgens de coördinator (en de volgorde in Jordi's zin) gaat het om de rechterkop. Gemeten in het model:
- **Mond** = de lijn (50–52,16) (53–54,17) (55–56,18) (57–60,17) (61–66,18) (67,19).
- **Streep op zijn kop** = de lijn die bij de zwarte wenkbrauw boven het oog (63–65,10) begint en over rij 10 (53–57, lum 97–111) naar de bovenrand van de snuit (52,10) loopt. Erboven (rij 9) en eronder (rij 11, lum 180) is het model licht.

Het korte stuk onder het oog (model (53,14)–(56,13)–(61,13)) heb ik niet als "de streep" gekozen. Het ligt niet bovenop de kop en is in het model zelf onderbroken (57–59,13 medium). Het blijft zoals in r5.

### 3a. Mond (3 px)
- Het gat tussen (32,8) en (34,9) is dicht: (33,9) h → n. Model (53,17) is lum 78.
- De knik in het model ligt bij (55–56,18) (zwart), één rij lager dan de rest. Daarom (35,9) n → b (model daar 129–131, zelfde vlak) en (35,10) s → n. Dit lijnpixel is 1 px naar de modelplek verschoven.
- De mondlijn loopt nu (31–32,8) (33–34,9) (35,10) (36–38,9) (39–42,10) (43,10).

### 3b. Streep over de kop (6 px)
- Doorgetrokken van het ooglid (38,5) en de wenkbrauw (40–41,4) naar de bovenrand (33,4): (37,5), (36,4), (35,4), (34,4) worden **s**. Dat is lichter dan de n/K-lijnen; het model heeft daar lum 97–111.
- In r5 waren dit twee m-pixels en een gat in h/b.
- Onder de streep (35–36,5) m → h: het model is daar licht (180), zodat de streep tussen twee lichte vlakken ligt zoals in het model.

## Controle
- Pupillen: linkeroog (10,16–17) en rechteroog (39,5) zijn K.
- 2×2-lijnklonten: alleen de bekende (5,22) (mond linkerkop) en (41,39–40) (vleugelklauw).
- Losse lijnpunten: (35,6) stond al in r5 los. Het is het stukje onder het oog (zie 3) en is niet aangeraakt.

## Zelfgenoemde zwakke punten
1. De pupil rechts zit nu tegen de zwarte oogrand (38,5); samen lezen ze als een zwart blokje van 2 px links in het gele oog. Dat is wat Jordi vroeg en wat het model doet. Het gele deel is nu (40–41,5) en (39–40,6).
2. In het model is de tong langer en roziger, met lichte glans. Met één paarse tint en het bevroren silhouet zit hij in de sprite op 5 px plus de vork.
