# Cuyby-evolutie ronde 3: diagonaal, ruiger en met een wilde kruin

Feedback van Jordi op ronde 2: "beter, maar waarom zet je hem niet diagonaal? Echt geen enkele Pokémon kijkt volledig zijwaarts." Tijdens het werk kwamen er nog aanvullingen bij:
- de vacht mag pluiziger en grassiger (ichu-graspol), met fijne punten en sprietjes in de omtrek;
- geen achtergekamde kuif, maar een wilde, onverzorgde pluk;
- geen krullen en geen rechte lijnen: zacht gebogen, natuurlijk vallende sprieten;
- de tweede referentiefoto is de maatstaf voor de vachtval, de pose en het silhouet (`../../../ontwerp/cuyby_evo/referentie_langhaarcavia_2.png`), met meer haar over één oog;
- kleur, schaduwwerk en het hoofd uit ronde 2 behouden.

De sprite is opnieuw getekend in de 3/4-pose. Uit ronde 2 komen alleen het palet (ongewijzigd), de manier van schaduwen en het oog met de vlek en het oortje. Alles is met de hand geschreven als rijen op een absolute x (`bron/delen_rle.txt`), per deel en van achter naar voor:

> lijf → lokken → streepjes → gordijn → achterlokken → gezicht → kruinpunten → kruinvoet → pony

Er zijn geen vormfuncties, geen automatische schaduw en geen automatische omlijning gebruikt.

## Bouwen (vanuit de repo-root)
```
python3 docs/concept/sprites/cuyby_evo/ronde3/bron/rle3.py        # delen_rle.txt -> delen.txt (met knippen)
python3 docs/concept/sprites/cuyby_evo/ronde3/bron/bouw9.py docs/concept/sprites/cuyby_evo/ronde3
python3 docs/concept/sprites/cuyby_evo/ronde3/bron/vel.py         # compare.png + metingen
```
- `rle3.py` is `rle.py` uit ronde 2, met één uitbreiding: naast `3h` mag een token ook letterlijke pixels bevatten (`rhhsd`, waarbij `.` 'laat staan' betekent).
- Na het tekenen knipt `rle3.py` twee kolommen (x 37 en 46) en twee rijen (y 23 en 44) weg. De eerste opzet was 1543 px. De coördinaten in de bron zijn dus van vóór het knippen.

## Bestudeerde sprites (Gen 3, Mamoswine Gen 4)
| sprite | wat ik eruit overnam |
|---|---|
| **Mareep** | Het lijf als ovaal dat schuin naar rechtsachter loopt. De kop zit linksvoor, de verre pootjes staan hoger en zijn kleiner, en de rug loopt naar achteren toe af. Dit is het skelet van de pose. |
| **Linoone/Furret** | De diagonaal: de voorkant is groot en dichtbij, de achterkant kleiner en hoger. Zo ontstaat diepte zonder perspectieflijnen. |
| **Piloswine/Swinub** | Hangende vacht tot de grond, met korte donkere strengen die niet doorlopen, en een zoom van punten met inhammen waar de pootjes net uit komen. |
| **Mamoswine** | Hoe een gezicht ín een vachtmassa zit: de vacht omlijst het gezicht en loopt aan de verre kant verder. |
| **Ninetales** | Lokken met een lichte punt en een inham eronder (de achterlokken en de zoom). De wilde kuif bracht me op een onregelmatige waaier in plaats van één kam. |
| **Teddiursa** | Ter controle van de oogmaat en de ronde snuit in een 3/4-gezicht. |

## Ontwerp in de sprite
- **Pose (foto 2, gespiegeld):**
  - Het gezicht zit linksboven in het midden van de vacht, niet meer tegen de linkerrand zoals in ronde 2.
  - Aan de verre kant hangt een gordijn van haar tot op de grond. Dat gordijn begint als pony over het verre oog.
  - Een schuine scheiding loopt over de rug van de kruin (x27,y21) naar de romp: daaronder ligt de nabije flank, daarboven de verre flank als smalle schaduwband met korte sprieten in de omtrek.
  - De rug loopt naar achteren af en de zoom stijgt naar achteren. Die twee lijnen lopen naar elkaar toe, zodat de romp kleiner en verder weg leest.
- **Vier pootjes:**
  - Verre voorpoot (x10, in P) links van en hoger dan de nabije voorpoot (x18, roze).
  - Verre achterpoot (x37) links van en hoger dan de nabije achterpoot (x41).
  - Dat volgt uit de draaiing: bij een dier dat naar links-voor kijkt, schuift de verre kant naar links en naar achteren.
- **Gezicht (Cuyby-kenmerken):**
  - Zwarte vlek rond het nabije oog met een lichte rand (g) en een 4×4-oog: witte glans linksboven, bruine weerkaatsing rechtsonder.
  - Zwart rozenblad-oortje met één roze pixel.
  - Een witte bles naast de vlek, die overloopt in een ronde witte snuit linksonder met een roze neusje en een wit kinnetje.
  - De verre wang ligt onder de pony; de snuit wijst schuin naar links-voor.
- **Kruin:** een wilde ichu-pluk. Vijf sprieten van 1–4 px breed steken uit een volle voet links-omhoog, recht omhoog, rechts-omhoog en naar achteren, plus twee dunne halmpjes. De punten buigen zacht naar buiten. Er is geen kam en geen knot.
- **Vacht:**
  - Scheidingen lopen van de rugscheiding steil omlaag. Ze golven licht, liggen ongelijk ver uit elkaar (x34, 39, 44, 50 en twee korte) en zijn op een paar plekken onderbroken.
  - Elke scheiding is een drietal 'donkerder | lijn | lichter': bovenaan zacht (d), in het midden r, bij de zoom zwart, en in de schaduwzone q|r|s.
  - Daartussen staan losse streepjes in de haarrichting (h in het licht, d in de schaduw).
  - De zoom bestaat uit punten van ongelijke lengte die naar achteren hoger eindigen. De romp heeft een lok die naar achteren uitsteekt, met een inham eronder.
  - In de omtrek steken fijne sprietjes uit: aan de pony, op de rug en rechtsboven.
- **Frame 2:** de kruinsprieten wuiven 1 px naar achteren; de voet blijft staan.

## Wat er met de zwakke punten van ronde 2 gebeurde
| zwak punt | ronde 3 |
|---|---|
| Kruin las als knotje of hengsel | Er is geen overhangende lok meer, maar een open waaier van sprieten die verschillende kanten op wijzen (Jordi: wild, niet gekamd). |
| Scheidingen regelmatig (pissebed) | Vier lange en twee korte lijnen, ongelijk verdeeld, golvend en onderbroken, met losse streepjes ertussen. Er zijn geen even ver uit elkaar liggende segmenten van kop tot staart meer. |
| Pony glad | De pony bestaat uit drie lokken met punten op verschillende hoogte (x17,y32 en x13,y35) en een sprietje aan de buitenrand. De buitenste lok loopt door als gordijn. |

## §0-checklist (SPRITING.md)
| # | punt | stand |
|---|---|---|
| 1 | Lichaam én blik diagonaal | **Ok.** Het hele dier staat 3/4 naar links-voor. Het gezicht zit binnen de vacht met de snuit naar links-voor. De rug daalt en de zoom stijgt naar achteren. Er is een schuine rugscheiding met de verre flank als schaduwband, en de verre pootjes staan links van en hoger dan de nabije. |
| 2 | Ledematen, oren, ogen geteld en verbonden | **Ok.** 4 pootjes (2 nabij roze, 2 ver in P). 1 zichtbaar oor (het verre oor zit onder de kruin). Het nabije oog is zichtbaar en het verre zit onder de pony (Jordi's wens). Neus en mond zijn er. `bouw9` meldt geen open randen. |
| 3 | Geen rechte lijnen in de omtrek | **Ok.** `bouw9` meldt geen rechte randstukken van meer dan 4 px. De sprieten buigen zacht en de linkerrand is onderbroken door een sprietje en een lokpunt. |
| 4 | Ogen geïntegreerd | **Ok.** Het oog is dat van ronde 2: bovenlid en rand in g binnen de vlek, glans en gekleurde weerkaatsing. Het verre oog is geen kopie, want het is bedekt. |
| 5 | Silhouet op 1× | **Ok, met twijfel.** Op 1× leest het als een langharige cavia met het gezicht linksvoor, naast foto 2. Door de kruin is het silhouet onrustiger dan in ronde 2. |
| 6 | Formaat | **Ok.** 1399 px, 49×44. Dat ligt tussen Linoone (1357) en Piloswine (1515), net als ronde 2 (1385). |
| 7 | Pose niet stijf | **Ok.** De voorkant is laag en dichtbij en de romp hoger. De pootjes staan versprongen en de zoom heeft ongelijke punten. |

Verder: het palet heeft 16 kleuren (index 0 transparant) en is ongewijzigd uit ronde 2. Het zwart-aandeel in de buitenrand is 0,49 (ronde 2: 0,58), doordat belichte sprietjes en punten bovenaan r krijgen.

## Metingen (frame 1)
| | oppervlak | b×h | zwart in de buitenrand |
|---|---|---|---|
| **ronde 3** | 1399 | 49×44 | 0,49 |
| ronde 2 | 1385 | 52×39 | 0,58 |
| Cuyby ronde 3 | 789 | 31×32 | 0,53 |
| Piloswine | 1515 | 42×48 | 0,43 |
| Mareep | 893 | 38×33 | 0,49 |
| Linoone | 1357 | 51×60 | 0,56 |
| Furret | 1191 | 41×50 | 0,43 |

## Eigen oordeel
- **Beter dan ronde 2:**
  - Het dier staat echt diagonaal: het gezicht kijkt de kijker schuin aan en het lijf loopt de diepte in.
  - De vacht valt zoals op foto 2: steil, rommelig en tot op de grond, met een gordijn aan de verre kant.
  - De kruin is wild in plaats van gekamd.
- **Twijfel:**
  - De kruinsprieten zijn dun en staan los. Op 1× kunnen ze aan een kroontje doen denken. Een voller, warriger pluk (meer overlap, één lichte lok erin, zoals in de derde referentie) is een optie.
  - De witte snuit is vrij groot ten opzichte van het oog, zoals bij Cuyby. Als dat te 'snavelig' leest, kan hij 1 px smaller.
  - De nabije flank heeft veel kleine tintwissels (lijnen plus streepjes). Op 3× is dat rommelig, op 1× leest het als haar.
