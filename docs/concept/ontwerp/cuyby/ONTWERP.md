# Cuyby (fase 1, Normal-cavialijn): ontwerpronde (geen sprite)

Helemaal opnieuw begonnen (Jordi: "Cuyby mag je helemaal opnieuw beginnen"). Ronde 1 las als een kawaii-sticker van een echte cavia: een liggend broodje, stipoogjes, blosjes, een spiraal-sticker en een muts. Elk concept hieronder heeft daarom **één overdreven kenmerk uit de anatomie dat het silhouet bepaalt**. Ze zitten rechtop, in 3/4 naar de speler, met voorpootjes, ogen met glans en vorm, een mondlijn en geen blosjes. Het formaat is dat van een vroege route (op 1× 670–840 px oppervlak, tussen Whismur en Sentret).

| | concept | in één zin | evolutie (silhouetschets) |
|---|---|---|---|
| A | **Rozetkruin** (`concept_A.png`) | De rozetten van de Abessijnse cavia staan als puntige waaiers rechtop (kruin, schouder, heup) en breken het silhouet zoals Zigzagoons vacht; agouti-bruin met crème punten. | rechtop met een grotere kroon en schouderrozetten → forse cavia met een krans van rozetten om de kop |
| B | **Fluitsnuit** (`concept_B.png`) | Het 'wheeken' als lichaamsdeel: twee opgeblazen wangzakken, breder dan de kop, met een ronde fluitmond ertussen; rood (de 'red'-cavia) met crème. | grotere wangzakken → snorharen als holle buizen van een **siku** (panfluit) die opzij uitwaaieren |
| C | **Langhaarbol** (`concept_C.png`) | De Peruaanse langhaarcavia: het lijf is één bol vacht met lokken die door hun gewicht omlaag vallen; de driekleur in strakke grafische vlakken (wit, oranje rug, zwart om één oog en oor). | bredere bol op vier stompe pootjes → wandelende hooiberg (het ichu-gras van de puna) |

`vergelijking.png` zet de concepten, verkleind tot spriteformaat, naast Sentret, Zigzagoon, Skitty, Whismur (Gen 3) en Bidoof (alleen DS), op 2× en 1×, met de silhouetten op 1× en een blinde rij. Het fluiten en de popcornsprongetjes zijn in alle drie de natuurlijke frame 2: wangen opgeblazen of een sprongetje met de mond open.

## Eigen keuring (criteria uit KEURING_RONDE5)
- **Afgekeurd en vervangen tijdens deze ronde:**
  - Een eerste C (Peruaanse 'vachtklok' met een zwarte kap) las als een spook onder een laken met een hoedje.
  - Een tweede C (een vachtrol als kussen om de nek) las als een zwemband of opgepompte armen.
  - Bij A las een kroon van oranje punten als een vlam (Fire), en de rozetten met een spiraalschijf waren weer stickers. Nu zijn de rozetten alleen puntige waaiers in agouti/crème, zonder schijf.
- **Spullen:** in geen van de drie.
- **Silhouet op 1×:** C (bol met puntige rand) en A (stekelige kroon) zijn het duidelijkst. B leest op 1× vooral als een brede kop; in frame 2 (wangen vol) wordt dat sterker.
- **Risico's:**
  - C zit het dichtst bij een echt dier: een Peruaanse cavia ziet er ongeveer zo uit. De Pokémon-twist (het lijf is alleen nog vacht, de driekleur als grafische vlakken) moet in de pixels heel strak blijven, anders is het weer een sticker.
  - A kan als egel lezen. De cavia zit in de snuit en de hangoortjes, dus die moeten in de sprite goed overkomen.
  - B is verwant aan Whismur (geluid, rond, rechtop). Het verschil is dat de cavia geluid maakt met de wangen en snuit in plaats van met de oren.

## Voorkeur: B
B heeft de duidelijkste Pokémon-twist: een echt cavia-gedrag (wheeken) wordt een lichaamsdeel, net zoals Whismurs oren of Rattata's tanden. Het geeft de lijn ook een eigen gevechtsrol (Normal met geluidsmoves) en een sterke eindvorm. De siku-snorharen brengen het Andesmotief via de anatomie in plaats van via een muts. Als Jordi een knuffeliger, 'cuy'-achtiger beestje wil, is C de tweede keus. Daarvoor moeten de grafische driekleurvlakken wel het uitgangspunt blijven.

Daarna (volgens de keuring): de gekozen tekening wordt de vaste modeltekening, Whismur (B) of Skitty is het skelet, het palet volgt de rampopbouw van de skeletsprite, en de schaduw wordt met de hand gezet.

Scripts: `../scripts/` (`cuyby.py` tekent de concepten en de silhouetten, `sheets.py` maakt de vellen).
