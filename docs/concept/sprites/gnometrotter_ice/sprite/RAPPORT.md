# Gnometrotter (Ice, zelfde pose) – frontsprite r1 (maker-agent, 23 nov)

Model (bevroren): `../r3/gemini_r3_lijf.png`. Lever: `gnometrotter_ice.png` (64×64, P, index 0 transparant, 16 kleuren), `gnometrotter_ice_8x.png`, `vel.png` (sprite | model op schaal 8×; 1× op 6 achtergronden; 1× en 2× naast Rock, Gnomini, Gnomad). Pijplijn: `./bouw.sh` (fam → zones → reductie → maak → meet → ijs → dc → tel/controle), daarna `vel.py`.

## Gedeelde reductie (GEDEELD.md, ongewijzigd)
- Zelfde geometrie als Rock: P = 8,1, model y 523 → spriterand 60, model x 512 → spriterand 32, 64×64, drempel 0,5 (stok 0,35). Script `reductie_gedeeld.py` is gekopieerd; `reductie_ice.py` gebruikt exact die `bron()`.
- **Enige aanpassing: het figuurmasker** (`masker.py`). De gedeelde regel "achtergrond = min(R,G,B) ≥ 235" gooit het ijswit van muts, baard en zolen weg. Ice: achtergrond = het met de beeldrand verbonden neutrale bijna-wit (min ≥ 236, max−min ≤ 6), plus het ingesloten gat tussen de mutspunt-ijspegels en de rugkam (model x 555–586, y 120–164; Rock heeft daar ook een gat).
- Resultaat: figuur x 3–61, y 0–59, 2011 px (Rock x 3–60, y 0–59, 1981 px); silhouetverschil met Rock 62 px, vooral de extra ijskristallen van de rugkam en de dunnere ijspegelstok (zit zo in het model). Voetlijn gelijk (rij 59).
- Palet: 0, 1, 6–11 en 15 exact gelijk aan Rock (zelfde indexen, gecontroleerd). Eigen materiaal: 2 ijs-outline base (64,88,122); 3–5 ijsblauw (124,160,196) (176,206,232) (222,238,250) voor muts, rugkam, stok; 12–14 sneeuw/ijspegelwit (170,192,214) (214,228,240) (246,249,252) voor baard, haar, riem, zolen. Kleur afgestemd op Gen 3-volume, niet op het model (mag).
- Onderdelen: de Rock-zones zijn de plaatsgids (`zones.py`); elke modelpixel houdt zijn Rock-zone als die bij zijn kleurfamilie past, anders de dichtstbijzijnde passende (zo groeit de ijspegelbaard over het Rock-lijf).

## Wat er op de kale reductie gebeurt (alleen regels, gestuurd door modelmetingen)
- `maak.py` (= Rock): buitenlijn 1 px (outline base lichtkant, zwart schaduwkant), binnenlijnen niet zwart, oogstrook dicht met mutskleur (Jordi "1 akkoord"; 7 px gemeten, 4 anders dan kaal), ronde delen (neus, hand R, arm R) rand in 6 met zwarte boog linksonder, ruisfilter.
- `ijs.py` (nieuw, Ice):
  - **A. gat** (2 px transparant, 20 px rand in 2): spritepixels met ≥ 45 % modelgat worden transparant; de ijspegel die in het model in het gat hangt (kolom 39) blijft staan. Rand in ijs-outline base i.p.v. zwart, zodat het niet als oog leest (Rock r1 las als oog met pupil).
  - **B. vlaktint met Gen 3-volume:** per onderdeel modelhelderheid (zonder modellijnen, 3×3 geëffend binnen het onderdeel) + lichtrichting linksboven + sikkel aan de schaduwkant, → 3 tinten op percentielen.
  - **C. baard (ijspegels):** modelhelderheid verticaal geëffend + horizontaal contrast (pegels als verticale banden); **pegelspleten** = de donkere omlijning tussen de pegels in het model (aandeel modellijn ≥ 0,14, horizontaal maximum), alleen als doorlopende verticale lijnen ≥ 3 px in tint 2 (20 px: x 24 y 25–31, x 27 y 26–29, x 18 y 25–28 e.a.). Geen losse donkere pixels.
  - **D. facetten:** roze = de donkere platen-naden van het model (aandeel ≥ 0,22, lokaal maximum) in 6; blauw = barsten + naden in 9 (21 px samen). Nooit zwart.
  - **E.** ruis < 3 px weg.
- `dc.py` (= Rock): Dragonfly Cave-ronde: om-en-om weg (4 px), outline highlights binnen de lijn (5 px: muts (22,6) (19,11) (51,16), vuist (15,31) (5,30)), gesp.

## Afwijking t.o.v. de kale reductie (`tel.py`)
| zone | anders / zone | lijn | oogstrook | DC + gesp | vlaktint (volume) |
|---|---|---|---|---|---|
| muts+rugkam | 367 / 470 | 90 | 4 | 5 | 268 |
| haar L | 34 / 39 | 18 | 0 | 1 | 15 |
| haar R | 32 / 38 | 19 | 0 | 0 | 13 |
| baard | 151 / 190 | 48 | 0 | 0 | 103 |
| neus | 23 / 56 | 15 | 0 | 0 | 8 |
| lijf | 122 / 281 | 16 | 0 | 0 | 106 |
| arm L+hand | 41 / 71 | 19 | 0 | 1 | 21 |
| arm R | 20 / 30 | 11 | 0 | 0 | 9 |
| hand R | 38 / 66 | 17 | 0 | 0 | 21 |
| riem | 170 / 208 | 47 | 0 | 19 | 104 |
| stok | 85 / 92 | 40 | 0 | 0 | 45 |
| broek/benen | 226 / 352 | 121 | 0 | 0 | 105 |
| zool L | 49 / 60 | 28 | 0 | 0 | 21 |
| zool R | 47 / 58 | 26 | 0 | 0 | 21 |
| **totaal** | **1407 / 2011** | | | | |

Het grote aantal "vlaktint" komt doordat het kale palet-kwantiseren (dichtstbijzijnde kleur) het ijs op één middentint zet; de volume-regel verdeelt het over 3 tinten. Vorm, lijnen en plekken blijven van het model. Silhouet: 7 px anders dan kaal (5 erbij aan de stok zodat hij niet breekt: (10,41) (10,42) (10,43) (6,49) (7,56); 2 weg = het gat).

## Pixels die niet rechtstreeks uit het model komen
- **Gesp** (18 px): zelfde rechthoek als Rock (x 24–29, y 39–41, zwarte rand, binnen tint 4); de gesp staat in Ice r3 op dezelfde plek (zelfde omtrek).
- **Oogstrook** (Jordi "1 akkoord"): 4 px anders dan kaal, dicht met mutskleur.
- **Outline highlights** (5 px, zie dc.py).
- Verder niets met de hand; alles hierboven is een regel op modelmetingen.

## Controle (`controle.py`)
64×64, P, transparantie 0, 16 kleuren in gebruik, zwart 9,2 %. Geen losse zwarte pixels. Lichte kleur op de buitenrand alleen de 2 outline highlights van de vuist. Vlekjes < 3 px die overblijven: lijnstukjes (naden/facetten in 2/6/9 die aan een lijn vastzitten), 1 glans (15) en (25,42) tint 13 in de riem.

## Eigen zwakke punten (voor Claude/keurder)
- **Lijf**: de roze platen lezen als licht midden + donkere rand met een paar naden; de witte barsten in de platen van het model zijn niet overgenomen (alleen de donkere naden, anders werd het een dambord). Schouderbal rechts leest als bol, maar de zwarte modellijn tussen bal en borst is hier 6.
- **Muts**: grote vlakken in 3 tinten met de hoofdlijnen; de fijne ijsfacetten van het model zijn weggelaten (bewust, les Rock r1).
- **Gat bij de mutspunt** leest op 1× als een witte V/inkeping (zo staat het in het model: pegels met een opening).
- **Linkerhaar**: de hangende pegeltjes zijn 1 px en daardoor lijnpixels.
- **Broek**: de witte barsten van het model zijn als donkerblauwe facetten (9) gezet, zoals opgedragen; de bovenrand onder de riem is donkerder (model).
