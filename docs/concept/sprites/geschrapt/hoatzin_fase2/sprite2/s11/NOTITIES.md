# Hoatzin fase 2, ontwerp 2, s11 (20 nov): hoofd, poten en verre vleugel

Jordi op s10: "eindelijk wat vooruitgang ... Vooral hoofd en poten moeten nog beter." Daarbij: de verre vleugel leest nog vlak.
`sh alles.sh` (bouw11.py op s10). Silhouet = s10 (0 px anders, assert); oog: zwart + 6 rood gelijk (assert). 189 px anders dan s10
(verre vleugel ±125, kop ±40, poten ±35; plus de paletwijziging van index 4, zie onder). Per zone een tekstraster in bouw11.py.

## Studie (graphics/pokemon, 8-14x)
**Hoofd**
- **Spearow-kuif:** stekels licht oranje linksboven, middentint, donkerbruine lijnen tussen de stekels; de bovenrand is donkerbruin (selout), zwart alleen onder en rechts. Daardoor leest het als haar, niet als helm.
- **Murkrow-snavel (haaksnavel van ±5 px):** licht op de bovenrug, midden eronder, donkerste tint in de mondhoek/punt, zwarte lijn rondom.
- **Mandibuzz/Vullaby (kale gekleurde kop):** grote lichte vlakken, middentint aan de rand rechtsonder, zwarte lijn scheidt kop van veren.
- **Tranquill/Pidgeot:** kleine kop leesbaar door een zwarte lijn tussen kuif en gezicht en een donkere band onderaan de kuif.

**Poten**
- **Dodrio/Doduo (beste voorbeeld, dunne vogelpoten):** scheen 1-2 px: aan de lichtkant een donkere selout (geen zwart), dan de kleur, zwart aan de schaduwkant. Teen = selout boven, kleur, zwart onder. Klauw = lichte pixel ingesloten door lijn (zwart eronder/ervoor).
- **Skarmory/Unfezant:** lijn aan beide kanten van de scheen; verre poot donkerder; de scheen begint donker onder de veren.

**Verre vleugel**
- **Pidgeot/Fearow:** elke veer een lichte linkerrand naast een donkere penlijn; veertoppen lichter dan de basis.
- **Honchkrow/Murkrow:** achterste deel donker, lichte randen alleen aan de veertoppen.

## Toegepast
- **Kuif:** lichte bovenband en linkerrand (11), middentint (12), donkere streng van (10,24) naar (12,26) die twee lobben scheidt, donkere band onder (13) boven de zwarte lijn naar het gezicht. Bovenrand en de lange stekel rechts kregen een donkerbruine selout (13) in plaats van zwart (Spearow); links en onder blijft zwart. Hoge stekel: licht aan de punt, midden eronder, zwart aan de schaduwkant.
- **Snavel:** bovenrug licht (8), haakpunt middengrijs (7, was donker en verdween in de lijn), onderkant midden, mondhoek zwart (was een losse paarse pixel); onderkaak licht aan de punt. Keel onder het gezicht nu crème (6) in plaats van grijs, zodat kaak en keel loskomen. De twee navy pixels in de nek onder de kuif (13-14,30) zijn nu crèmeschaduw.
- **Nabije poot:** scheen licht (8) met middengrijze selout links (7) en zwart rechts; bovenaan donkerder onder de veren; enkel 2 px licht. Voorteen: selout boven, licht, zwart onder (de twee zwarte pixels onder de teen werden teenkleur); klauw crème (5) ingesloten door een zwarte punt. Achterteen midden met crème klauwpunt.
- **Verre poot (in schaduw):** scheen middengrijs (7) met navy selout (3), gat in de scheen (rij 52) gedicht met kleur; tenen 7 met selout 3, klauwen lichtgrijs (8) ingesloten.
- **Verre vleugel:** veertoppen boven licht (2), daaronder per veer een penlijn (4) vanuit de inkepingen naar rechtsonder (richting van de veren in het model) met rechts ervan een lichte rand (2); sikkel (4) rechts; onderste deel achter kop en nek een donkere zone (4), waardoor de kuif er beter tegen afsteekt.

## Paletbudget (15 + transparant = 16)
| # | kleur | gebruikt voor |
|---|---|---|
| 1 | (16,14,24) | lijn |
| 2 | (96,108,170) | navy licht, gezicht schaduw |
| 3 | (64,60,104) | navy midden, gezicht diepe schaduw, krop donker, selout verre poot |
| 4 | (40,38,68) | navy donker (was (32,30,54), bijna zwart): verre vleugel schaduwzone, penlijnen, sikkels |
| 5-6 | (244,236,212) (208,198,172) | crème licht/midden; 5 ook klauwen nabije poot |
| 7 | (146,144,136) | crèmeschaduw = grijs midden (snavel, poten) |
| 8 | (192,192,188) | grijs licht (snavel, nabije poot, klauwen verre poot); eigen grijs, niet de nekkleur |
| 9-10 | | krop licht/midden (ongewijzigd) |
| 11-13 | (200,126,78) (150,80,54) (96,42,32) | kuif licht/midden/donker (iets meer contrast dan s10) |
| 14 | (196,60,52) | oogrood (ongewijzigd) |
| 15 | (116,158,204) | gezicht licht (iets lichter) |
Index 4 is iets lichter gemaakt zodat hij naast 3 en 1 echt een eigen tint is (in s10 was hij nauwelijks van zwart te onderscheiden). Dat raakt ook de penlijnen/sikkels van nabije vleugel, lijf en staart: die worden een fractie zachter, verder ongewijzigd. Geen extra grijs nodig: 3 dient als koele schaduw van de grijze delen.

## Controle
dambord 0 · om-en-om 0 · zwarte klonten 0 · barcode 0 · losse tintpixels 27 (s10: 39; het zijn klauwen, de haakpunt, de kaakpunt en oude penlijnstapjes in de nabije vleugel).
`vel.png`: s11 | s10 | model op 8x, daaronder per onderdeel de voorbeelden naast s11 en s10.

## Eerlijk, wat nog zwak is
- **Kuif** blijft van boven vrij recht (het silhouet is bevroren); de selout en streng maken hem haariger, maar de rafelige punten van het model zitten niet in de vorm.
- **Verre vleugel**: de penlijnen in 4 hebben weinig contrast met 3; de veren lezen op 8x, op 1x is het vooral licht boven en donker onder. Het onderste deel is één donker vlak (bewust, achter de kop).
- **Tenen** zijn op sommige plekken maar 2 px hoog: daar ontbreekt de lijn boven (voorteen bij x22, achterteen nabije poot). De nabije voet heeft maar één voorteen in de vorm (model: drie).
- **Verre voet**: de navy selout leest op 1x wat paars.
- **Gezicht** is nauwelijks veranderd (ring licht linksboven, schaduw rechtsonder); geen eigen hooglicht door het paletbudget.
