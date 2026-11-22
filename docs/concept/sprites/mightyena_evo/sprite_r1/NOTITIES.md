# Mightyena-evolutie (Dark/Fighting) frontsprite, ronde 1

Bestanden: `mightyena_evo_r1.png` (64×64, geïndexeerd, index 0 transparant, 13 kleuren incl. transparant), `kaal.png` (kale reductie, zelfde palet), `bouw.py`, `vel.png` (r1 8× | kaal 8× | model op dezelfde schaal 8× / close-ups 12× kop+bek+oog, opgeheven poot, manen, poten naast het model op schaal / 1× op wit, licht, donker naast Mightyena 1× + model 1×).
Gereedschap (`../gereedschap/`, gekopieerd van Dundragoon en aangepast): `pitch.py`, `natief.py` (→ `natief.png`), `gemeen.py` (modelklassen, palet, opslaan), `schrap.py`, `vel.py`, `controle.py`, `zones.py`, `kopraster.py` (kop van sprite en 1024-model op hetzelfde raster), `kijk.py` (8× naast Mightyena).
Bouwen: `cd mightyena_evo && python3 sprite_r1/bouw.py` (`kaal` toont alleen de kale reductie, `toon` print het raster).

## Metingen
- **Rasterpitch:** randsterkte per kolom/rij: kam **10,24 px** (1024/100), fase 9,20 in x en y (niet ±12; visueel bevestigd: blokjes ±10 px op een uitvergroting van de kop). Natief raster 99×99, figuur x15–88, y14–83 = **74×70**.
- **Schaal 64/74 (0,865).** Volgens GEMINI.md (Gengas, 74→64: "schrappen, niet hertekenen") is verkleind door **10 kolommen en 9 rijen weg te laten** in plaats van te middelen: elke spritepixel is een echte modelpixel (dus "dichtstbijzijnde kleur uit het model" exact, zonder blur). Eén schrapping per gelijk stuk (verhoudingen blijven), binnen het stuk de rij/kolom die het meest op zijn buur lijkt; verschil in oog/bek/tand weegt 10×.
  - Nooit geschrapt: rijen 13–28 (ogen, snuit, bek) en 62–69 (klauwen), kolommen 0–14 (ogen, snuit, bek). Het gezicht staat dus pixel voor pixel als in het model (sprite x,y = natief x, y in de kopzone).
  - Geschrapt (natieve uitsnede): rijen 5, 11 (oren/voorhoofd), 29, 32, 35, 42, 52, 58, 61; kolommen 15, 18, 21, 24 (achterhoofd/nek), 33, 43, 50, 55, 63, 71.
- **Figuur in de sprite: x0–63, y2–62 = 64×61, 2087 px** (Mightyena 58×56 / 1663 px: +25 %; Houndoom 54×54 / 1477). Niet gespiegeld (kijkt al naar links). Silhouet = kale reductie (diff 0); modelgaten (tussen de poten, onder de opgeheven poot, tussen voor- en middenpoot) open.
- Modelklassen (natief): zwart L<20, bijna-zwart 20–46, donkergrijs 46–96 (gesplitst op 70), middengrijs 96–135, lichtgrijs ≥135, geel/rood (oog), bek donker/midden, tand (wit; ingesloten wit in de bek = tand, geen gat).

## Palet (index: kleur)
0 transparant · 1 zwart (16,16,24) · vacht 2 (40,40,54) 3 (66,70,92) 4 (100,106,132; ook gekleurde selout van het grijs) · grijs 5 schaduw (128,124,146) 6 midden (164,162,178) 7 licht (200,200,212) · 9 geel (248,208,64) 10 rood (216,48,40) · bek 11 donker (88,36,40) 12 tong (160,92,96) 13 tand (248,248,248). (8 klauwtip staat in het palet maar is ongebruikt.)
Kleur wijkt bewust af van het neutrale grijs van het model (Jordi: "Je mag met kleur altijd van het model afwijken"): koel blauwgrijs zoals de Gen 3-Mightyena (vacht 32/49/74, grijs 148/172), iets lichter zodat de zwarte vacht intern leest.

## Pixels die afwijken van de kale reductie: 273 van 2087 px (13 %), silhouet-diff 0
Per zone (`zones.py`): **kop (oren, voorhoofd) 34, ogen 17, bek/snuit 30, manen/staart/vacht 68, grijs lijf (vlekken) 87, opgeheven poot 10, poten 27.** Per stap (`bouw.py`):
- **buitenlijn 59 + controle 6:** randpixels van de vacht zwart; grijs/bek aan de schaduwkant (achtergrond rechts/onder) zwart, aan de lichtkant (alleen links/boven) selout 4; een losse seloutpixel tussen zwart wordt zwart (geen om en om).
- **lichtkant selout 16:** zwarte modelrand van een grijs deel aan de lichtkant (oren, schedel links) → selout 4, zodat zwart en selout niet om en om staan. Gezicht (y14–28, x≤14) uitgezonderd.
- **ontkorrelen vacht 19, grijs 25, kop 18:** losse 1-px tintjes in de vacht en tintvlekjes < 3 px in het grijs nemen de buurtint aan; oog, wenkbrauw, ooglijnen en bek blijven.
- **grijs: D naar vlek/schaduw 18:** donkergrijze modelpixels in het grijze lijf: naast een vlek → vlek (2), anders schaduw (5).
- **vlekken 4:** 1-px vlekjes die in het model 2–4 px waren (rest weggeschrapt) krijgen hun tweede pixel terug aan de kant van het modelcluster: (28,28), (24,32), (40,33), (37,34) e.o.; geen nieuwe vlekken.
- **losse zwarte pixels 3:** losse modelstipjes midden in een vlak: (10,31) opgeheven poot → vacht 2; (18,39), (24,41) lijf → schaduw 5.
- **bek: hoektanden 20 + 1** (de enige toegestane vormafwijking, Jordi "ga maar los"): de kleine modeltandjes vallen weg; vier witte hoektanden van 1×2 px zoals Mightyena frame 2: boven voor (3,22–23), boven achter (7,22–23), onder voor (5,26–27), onder achter (10,25–26). Overige tandpixels van het model krijgen de bekbinnenkant zodat de bekopening de modelvorm houdt: (8,22) (9,21) (10,21) (10,23) (12,23) (11,24) (4,23) (5,23) (5,25) (6,27) (7,27) → donker 11; (8,23) (9,26) → tong 12; bovenlip tussen de hoektanden (2,22) (4,22) (5,22) (6,22) → snuittint 3; onderlipje (4,24) → zwart. Los wit modelpixeltje onder de kaak (12,28) → vacht 2 (op 1× een losse witte stip). Bekvorm, tong en binnenkant verder = model.
- **volume (licht linksboven) 75 — niet uit het model, kleur:** het model is op het lijf één vlak lichtgrijs. Per lijfdeel (gescheiden door de zwarte modellijnen) geblurd masker → normaal → licht van linksboven: lichtkant van schouder, rug onder de manen en dij → hooglicht 7, schaduwkant → 5. Kop uitgezonderd (gezicht = model). Vlekken en lijnen blijven.
- **manen: lichtkant strengen 39 — niet uit het model, kleur:** strengpixels (3) met donker/zwart erboven of links ervan → 4, zodat de zwarte manen intern drie tinten hebben zoals Mightyena's vacht. Strengen zelf = model.
- Verder geen pixels die niet uit het model komen. Ogen (geel/rood) en wenkbrauw/ooglijnen: 0 pixels veranderd; alleen de randpixel links van het verre oog (1,16) werd zwart (buitenlijn).

## Controle (`controle.py`)
64×64, mode P, transparency 0, 13 kleuren incl. transparant (≤16). Per groep ≤ 3 tinten + lijn (vacht 2/3/4, grijs 5/6/7, bek 11/12 + tand). Zwart 19,2 % van de figuur (Gen 3 ±12–19 %; Mightyena 17,7 %). Geen lichte kleur op de buitenrand; geen losse seloutpixels tussen zwart. Losse zwarte pixels alleen in het gezicht, uit het model: (3,15) tussen geel en rood van het verre oog, (6,19) en (4,20) neusgat/snuit, (11,21) bekhoek. Tintvlakjes < 3 px die over zijn: oog (geel/rood), tanden, bek (bewust), strengen en vlekken (lijnen, 8-samenhangend); grijs: (2,18) snuit, (54,44) en (36,55) poot-overgang, klauwtjes (50,56) (52,56) (23,59).

## Resterende twijfels (eerlijk)
- **Hooglicht op de rug** volgt de onderrand van de manen als een band van ±1–2 px; leest als licht van boven, maar kan op 8× als streep langs de manen lezen. Zonder: vlak lichtgrijs zoals het model.
- **Kleur:** blauwgrijs (Mightyena-familie) i.p.v. het neutrale grijs van het model; de bek (11/12) is model-bruinroze, niet Mightyena-rood.
- **Snuit** is op 64 px een donker vlak in vachttinten met de modeltextuur (neusgat, mondlijn); leest op 1× als donkere hyenasnuit, op 8× wat onrustig.
- **Vlekken** zijn de modelvlekken (2–5 px); niet samengevoegd tot grotere vormen, want ze staan al op hun modelplek en lezen op 1× als vlekken, niet als ruis.
