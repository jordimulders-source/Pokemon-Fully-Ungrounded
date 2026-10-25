# Olinguito v2: kleursprite ronde 4 (kleine reparaties)

Basis: kleur ronde 3. Jordi: "dit begint echt al goed in de buurt te komen, de klauwen zijn nog niet helemaal mooi gelijnd, net als het oor, maar dit is het beste olinguito ontwerp wat ik tot nu toe heb gezien". Daarbij de keuring `../ronde3/KEURING.md`.

Dit zijn alleen gerichte reparaties. Hetzelfde palet, dezelfde helderheid, het masker niet herontworpen, de snoet niet lichter.

**Bestanden:**
- `olinguito.png`
- `vel.png`: ronde 4 en ronde 3 op 4× en 1×, op licht en op donker, plus het ontwerp en de referenties.
- `bron/reparaties.py`: alle wijzigingen per punt, als met de hand geschreven pixelreeksen.
- `bron/raster_grid.txt`
- `bron/bouw.py`
- `bron/vel.py`

**Bewijs:**
- alpha-diff 0 tegen het silhouet van ronde 5;
- **53 pixels gewijzigd** tegenover ronde 3;
- 0 randpixels zonder omlijningstint (gescand).

## Per punt (aantal gewijzigde pixels)
| # | punt | px | wat |
|---|---|---|---|
| 1 | Klauwen | 10 | Twee Linoone-haakjes die aan elkaar vastzitten. Per klauw licht (`w`) linksboven en schaduw (`n`) rechtsonder. Een donkere scheidingslijn loopt eerst schuin (x 20→18) en buigt dan naar verticaal (x 17, 17), zodat beide klauwen bovenaan diagonaal lopen en onderaan als haak omlaag eindigen. Ze zijn rondom gesloten omlijnd, ook bij (17,53) en (17–18,58). |
| 2 | Oor | 3 | Gesloten rand in de donkere oortint (`#4A3324`), zwart alleen rechts. De binnenkant (`#8A6C55`) is een gelijkmatige ronde vlek (2-4-2 px). De open randen bij (24,18) en (18,18) zijn dicht. |
| 3 | Kop | 20 | Zie hieronder. |
| 4 | Verre voorpoot | 9 | De dubbele zwarte scheiding is vervangen. De nabije poot (selout, 2× licht, midden) wordt gescheiden met één rij omlijningsbasis (`d`), daarna volgt de verre poot (2 px: middentint `b` + schaduw `d`) met zwart aan de buitenkant, tot een donkerroze pootje. Op 1× is er nu een tweede, donkerdere voorpoot te zien. |
| 5 | Dij | 5 | Het hooglicht is een gebogen kap in plaats van een strook van gelijke breedte. Per rij: 7, 6, 4 en 3 px, met de linkerrand 38 → 36 → 35 → 34. Breed bovenaan, smal uitlopend. |
| 6 | Open randen en losse pixels | 6 | Onderkant van de snoet (19–21,39), binnenkant van de staartkrul (49–50,7) en voorkant van de achterpoot (38,46) zijn nu zwart. De overige open randen zijn opgelost in punt 1 en 2. De losse pixels (25,30) en (24,37) zitten in punt 3. |

**Punt 3, kop, in detail:**
- **Bruin lijntje boven het masker** (y 31, x 10–17): weg. Die pixels zijn maskertint geworden, zodat de band niet dunner wordt en de vorm uit het ontwerp blijft. De rand op x 9 is zwart.
- **Naad tussen grijs en kruin:** de rechte 1-op-1-diagonaal is nu een boog. De grens ligt per rij op x 19, 20, 21, 22, 24, 24, 25 en 26, steil bovenaan en vlakker naar achteren, en volgt zo de schedel.
- **Verticale banden achteraan:**
  - de donkere kruinrand loopt nu breder uit naar onderen (1 → 2 → 3 px);
  - de kopschaduw achter het masker begint op x 26, 26, 25, 25, 25 en 24, in plaats van een rechte kolom.
- **Masker:** alleen de achterrand op x 24 is afgerond, met 2 px (boven- en onderhoek). De dikte en de rechte band blijven.
- **Losse pixels:** (25,30) en (24,37) zijn opgenomen in de kopschaduw.

## Toets op 1×
- Twee voorpoten tellen: de verre is een donkere strook naast de nabije, geen zwarte streep meer.
- De klauwen lezen als twee lichte haakjes en niet als eetstokjes. Het oor is een rond, netjes omlijnd oortje.
- De kop leest boller doordat de rechte naden weg zijn. Het masker is dezelfde zwarte band als in ronde 3, zonder het bruine randje.

## Bewust niet gedaan (voor Jordi)
- **Masker:** dikte, schuinte en ronde oogvlek blijven gelijk (keuring A wilde dunner en schuiner).
- **Helderheid en snoet:** niet aangepast.

## Lessen
- **Een "lijntje weg" naast een vorm die bevroren is:** vul het met de tint van die vorm (hier het masker), niet met de achtergrondtint, anders wordt de vorm dunner.
- **Klauwen in een silhouet dat 1 px per rij verspringt** lijken pas gebogen als de scheidingslijn onderaan verticaal wordt. Laat de punten recht omlaag eindigen, dan worden het haakjes.
- **Scan op open randen per kleurgroep** (randpixel naast transparant zonder omlijningstint); dat vond alle 11 punten van de keuring en bewijst dat er 0 over zijn.
