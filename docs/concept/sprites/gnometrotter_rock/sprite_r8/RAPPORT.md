# Gnometrotter Rock: sprite r8 (23 nov), alleen belijning, tinten en schaduw

Basis: `sprite_r7b/gnometrotter_rock.png` (kopie: `r7b_basis.png`). Jordi: "het gaat nu echt om belijning, kleuren en schaduwen" · "de vorm laat je intact vanaf nu".
Werkwijze: met de hand per pixel in `grid.txt` (hex per pixel); de stappen per onderdeel staan in `stappen/*.txt` (regel = `y x0 pixels`). `zet.py` weigert elke wijziging aan het silhouet, `bouw.py` maakt de png, `scan.py` en `tinten.py` zijn de controles, `vel.py` maakt het vel.
Bestudeerd op 8×/12×: Gnomad, Gnomini, welp (`steenmozaiek/af/welp.png` + eindkeuring), steenjaguar, bloedmaan, Solrock-corona, Regirock, Golem, Graveler.

## Controles (scan.py, tinten.py)
- Silhouet (alpha) diff met r7b: **0**.
- Losse pixels (geen 8-buur met dezelfde index): **0** (r7b had er 19-plus, o.a. de "willekeurige pixels" in de muts).
- Buitenrand met een vlakkleur: **0**. Zwart en lijnkleur om en om op één rand: **0**.
- Vultinten per onderdeel (zonder lijnkleur): muts 3/4/5 · rots 3/4/5 + glans D · haar L en R 5/D/E · baard 5/D/E · neus 7/8/F · lijf 7/8/F · vuist+arm L 7/8/F · arm R 7/8/F · hand R 7/8/F · riem 3/4/5 · stok 3/4/5 · broek A/B + nieuw hooglicht (12), met 9 als schaduw en lijn · schoenen 3/4/5. Overal ≥ 3.
- 515 pixels anders dan r7b, waarvan 55 alleen door de paletsamenvoeging (baard C → 5, zelfde plek, bijna dezelfde kleur).

## Paletwijziging (16 kleuren, alle andere indexen ongewijzigd)
- **Index 12**: was baardschaduw (166,163,158); de baard gebruikt daarvoor nu index 5 (158,153,145), die er 10 helderheid onder zit (stappen baard: 5 → D 36 → E 30).
- **Index 12 is nu blauw hooglicht (170,216,244)**, dezelfde kleur als in de goedgekeurde Gnomini. Blauw heeft daarmee 9 (schaduw + lijn, zoals Gnomad), A, B en een hooglicht.
- Roze (6, 7, 8, 15) en blauw (9, 10, 11) zijn exact de Gnomad-kleuren gebleven.

## Per onderdeel
- **Muts (76 px):** de 5 en 3 lagen in r7b direct tegen elkaar en er zaten losse 4/5-pixels in de rand en de vouw. Nu: licht 5 linksboven, een sikkel van 4 die de kegel volgt, schaduw 3 rechts tegen de vouw. Rechts van de vouw een klein licht vlak 4 op de bovenkant van de punt, daaronder 3. Rand: lichtkant 2, schaduwkant 1, één overgang. Onder de vouwlijn de rand van de muts: bovenrand 5, daaronder 4, rechts 3. Onder de rand een lijn 2 die naar links dunner wordt en ophoudt, dan de schaduwstrook 3 (oogstrook blijft mutskleur).
- **Mutspunt en rugrots (44 px):** de punt (x 41–43) heeft nu links 4 en midden 3, met lijn 2 tussen punt en rots. Daardoor lopen ze niet meer in elkaar over. (44,13) was vlak en is nu die lijn. De rots heeft een voorkant met glans D linksboven → 5 → 4, de knik 2 en een zijkant 3. Het lagere rotsdeel onder de punt is 5/4/3, het rotsstuk achter de schouder 5/4/3, met 2 onderaan.
- **Haar L (7 px) en R (16 px):** bovenkant E, midden D, onderkant/rechts 5 als sikkel, dus niet meer drie rechte banden. Lijnen in 2 waar het haar tegen de muts en het lijf ligt. Een losse D bovenaan is E geworden.
- **Neus (14 px):** de F liep in r7b als band langs de linkerrand. Nu zit er een hooglicht van 4 px binnen linksboven, het vlak is 8 en er loopt een schaduwsikkel 7 rechts en onder. De rand volgt de Popplio-regel en was al goed: zwart van linksmidden tot onder-midden, verder 6.
- **Snor en baard (104 px, waarvan 55 de paletsamenvoeging):** licht E links, D midden, 5 rechts. Onder de snor ligt een slagschaduw 5 en daaronder één naad 4. Die was op rij 27–28 twee pixels dik; nu één rij lijn met schaduw eronder. Rand: links 4 (lichtkant), rechts en onder **zwart**, zoals Gnomad de baard rechts afsluit. In r7b lag de baard op rij 23–28 zonder lijn direct tegen het roze. Daar zijn de buitenste baardpixels nu de zwarte lijn. Op rij 29–30 lag de baard links zonder lijn tegen de arm; daar staat nu lijn 4. Onderste punten 5, met naden in 4.
- **Lijf en schouderschijf (±60 px):** het lijf was grotendeels effen 8. Nu heeft elke plaat F of 8 linksboven, 8 in het midden en 7 rechtsonder. Rechts van de baard ligt een slagschaduw 7/6. Het lijf is links licht en rechts (schaduwkant) donkerder, en onder de bolling ligt een rij 7 boven de riem. De schouderschijf liep in r7b als vlakke F in 8 over. Nu: hooglicht F linksboven, 8, en een sikkel 7 rechtsonder. Volgens de Popplio-regel loopt er zwart van linksmidden tot onder-midden ((40,23) → (44,26)), verder 6. De rechterrand van de schijf was grijs 2 en is nu 6. Een losse grijze pixel (38,21) in de plaat onder het haar is roze 7 geworden.
- **Vuist en arm L (13 px):** de F-band langs de linkerrand is nu een hooglicht binnen linksboven, met 8 en een sikkel 7 onderaan. De knokkelnaden 6 blijven. De arm is boven F, midden 8, onder 7. De bovenkant van de stok onder de vuist is slagschaduw 4/3.
- **Arm R (6 px) en hand R (18 px):** de armsegmenten hebben F linksboven, 8 en 7. De hand had een F-band langs de rand en heeft nu een hooglicht binnenin, 8 en een sikkel 7. Rand volgens Popplio: zwart van linksmidden tot onder-midden, de rechterkant en rechtsonder van zwart naar 6.
- **Riem (47 px):** de rand linksboven lichtte op in vlakkleur 5/4 en is nu 2. Onder de baard liep de lijn als zwart/2/zwart/2 en is nu één zwart stuk (baard, schaduwkant), daarna 2 (bovenrand riem): één overgang. De slagschaduw onder de baard is 3. Daarnaast licht 5 op de bovenkant voor, 4 midden en 3/2 rechtsonder. Rechts is de schuine bovenrand doorgetrokken waar de riem zonder lijn tegen het roze lag ((43,34), (44,34) → 2), met een rij 4 eronder; dubbele lijnpixel (47,33) is vlak 4 geworden (`stappen/riem_rechts.txt`).
- **Broek (94 px):** B liep als band langs de linkerranden en is nu een licht vlak linksboven op elke bal (dij L, dij R, voet L, voet R). Daarin zit het nieuwe hooglicht (3 px per bal). A is het midden, 9 de sikkel rechts/onder en de naden. Een dubbele lijn onder de riem (rij 42 + 43 links) is één lijn geworden: rij 43 is vlak. Een losse grijze pixel (25,43) in de broek is A geworden. De naad op rij 45 is aan beide uiteinden taps.
- **Schoenen (11 px):** bovenkant 5, voorkant links 4 → rechts 3, onder rechts 2. In r7b zat aan de schaduwkant van de rechterschoen 4: dat is nu 3.
- **Stok:** ongewijzigd (had al 5/4/3 met lijn 2 links en zwart rechts), op de slagschaduw onder de vuist na.

## Afwijkingen van de vormregel (ter controle)
- Twee losse grijze pixels zijn vlakkleur van het onderdeel eromheen geworden: (38,21) 2 → 7 in het lijf en (25,43) 2 → A in de broek. Het waren 1-pixelspikkels zonder vorm. Wil je ze terug, dan zijn het 2 regels in `grid.txt`.
- Lijnpixels zijn soms van lijnkleur gewisseld (bijv. 6 ↔ 1, 2 ↔ 6, 4 ↔ 6). De grens tussen de onderdelen is nergens verschoven.

## Eigen kanttekeningen
- De broek is iets donkerder dan in r7b (meer A, B alleen linksboven). Op 1× naast Gnomad vergelijkbaar, maar lichter dan het model.
- Het lijf leest nu als stenen platen met volume. Op 2× is het wat drukker dan Gnomad, omdat elke plaat zijn eigen 8/7 heeft (de platen zelf zijn vorm uit het model).
