# Eindkeuring lama fase 2, kleur ronde 4h (verse keurder, 4 nov)

Gekeurd: `lama.png` + `normal.pal`. Vel: `eindkeuring_vel.png`. Daarop staat de lama op 1× naast Mareep, Flaaffy, Girafarig, Ponyta, Rapidash, Numel, Camerupt, Stantler en Houndour (de `anim_front_gba`-frames), op een lichte en een donkere achtergrond. Daaronder staat hij op 2× naast Mareep, Flaaffy, Girafarig en Stantler, en onderaan een detail van de handschoenen op 8×. Ik heb eerst zelf geoordeeld en pas daarna AFGEKEURD.md, de keuring van ronde 4 en de notities gelezen.

## Oordeel: **AF NA KLEINE REPARATIES** (2 punten, samen 6 px, geen silhouetwijziging)

Technisch is de sprite schoon. Op 1× leest hij als lama, ook naast echte Gen 3-viervoeters. De twee reparaties hieronder zijn randzaken bij de handschoenen. Doet Jordi ze niet, dan kan de sprite ook zo af.

## 1. Technisch (met script gecontroleerd)
| Punt | Uitslag |
|---|---|
| Formaat | 64×64, PNG mode P, 4-bit, PLTE met 16 kleuren, tRNS op index 0. `normal.pal` is gelijk aan de PNG-palet. ok |
| Kleuren | alle 16 indexen worden gebruikt, index 0 is transparant (152,208,160). ok |
| Samenhang | 1 component van 1184 px. Er zijn geen losse of zwevende delen. ok |
| Gaten | Er is één ingesloten transparant gebied: x21–23, y49–58, tussen de voorpoten. Het is ingesloten omdat de handschoenen elkaar raken; dat is een eigenschap van het model en staat in SPEC. Het is negatieve ruimte en geen fout. ok |
| Halfdoorzichtig | niet mogelijk (geïndexeerd, alleen index 0 is transparant). ok |
| Losse pixels | 39 pixels hebben geen buur van dezelfde kleur. Ik heb ze allemaal bekeken: het zijn bewuste details (oog, neusgat (15,15), wolvlekjes en -haakjes, pompons, kwasten, hoef- en nagelpixels, poot- en buiklijntjes). Geen ervan leest op 1× als vuil, behalve de nagels in R1. ok |
| Open randen | Er zijn 24 pixels zonder omlijning tegen transparant. De meeste mogen zo blijven: de donkerrode rand van de kwasten en de doek (`9` is de omlijningstint van de rode groep), de donkergrijze achterhoef (`A`), en de pseudo-omlijning van het oor van 2 px op (17,3), (17,7) en (17,8), wat SPRITING §8 toestaat. Niet in orde zijn de 3 lichtgrijze nagelpixels aan de onderrand, zie R1. |
| Zwart aan de lichtkant | Zwart ligt aan de lichtkant vooral op oortoppen, wimper en hoef, en dat is in orde. Bij de nabije handschoen loopt het zwart ook langs de lichte linkerkant, zie R2. Aan de lichtkant gebruikt de wol overal donkerbruin `2`. ok |
| Ruimte | De bbox is x12–52 en y1–62 (41×62 px). Hij is hoog, maar Girafarig, Rapidash en Stantler gebruiken ook de volle hoogte. Er zit 1 px lucht boven en onder. ok |

## 2. Leesbaarheid op 1× (licht en donker)
- **Lama:** direct herkenbaar door de lange rechte hals, de kop met lange oren en het wollige lijf. Naast Girafarig en Stantler is het duidelijk een ander dier, geen giraf en geen hert. ok
- **Oog:** leest als een half geloken, donker oog onder een zwaar lid, ook op een donkere achtergrond. ok
- **Staart:** leest als een klein rechtopstaand plukje op het achterwerk. Hij is klein maar wel een eigen vorm (zie "voor Jordi"). ok
- **Poten en handschoenen:** de twee voorpoten met rode handschoenen lezen als twee afzonderlijke handschoenen, dankzij de zwarte scheiding op x22–23. Achter lees je maar één poot. Dat komt door het model en is bekend. ok
- **Accessoires:** de halsband in drie banen met pompons, de doek met roze zoom en blauw-rode plooi, en de oorkwasten lezen op 1× allemaal. ok
- **Licht:** komt overal van linksboven (hals, wolbollen, doek, handschoen-hooglicht `7`). Er is geen pillow shading. De enige banding is de halsband, en die is bewust gestreept. ok

## Reparaties (klein, coördinaten x,y)
1. **Nagels onder de handschoenen** (3 px). (14,62), (16,62) en (24,61) zijn lichtgrijs (`F`) aan de onderrand, tegen transparant. Dat is de schaduwkant, en daar zou het een open rand zijn. Op 1× lezen ze als grijze stofjes onder de handschoenen. Reparatie: `F` → `A` (donkergrijs). De vorm blijft gelijk, de rand is dan dicht en het blijft een hoefpuntje.
2. **Zwart aan de lichtkant van de nabije handschoen** (3 px). (15,58), (14,59) en (14,60) zijn `1`, terwijl de lichtkant de omlijningstint van de eigen kleurgroep moet hebben. Reparatie: `1` → `9` (donkerrood). Laat de zwarte scheiding tussen de handschoenen (x21–23) en de onderrand (y61–62) zwart.

Totaal 6 px, alpha-diff 0. Lever op met een pixeldiff die bewijst dat er buiten deze 6 px niets veranderd is.

## Voor Jordi (geen reparatie, alleen ter info)
- De staartpluim is klein (±5×4 px). Hij leest als een eigen vorm, maar valt op 1× minder op dan bij Ponyta of Girafarig. Groter maken is een silhouetwijziging, en het silhouet is bevroren.
- Achter is maar één poot te lezen; de verre achterpoot is een smalle donkere strook. Dit is bekend (model, SPEC) en alleen op te lossen door het silhouet te veranderen.
- De sprite is hoog en smal (41×62). Dat past bij een lama, maar in gevecht staat hij iets hoger in beeld dan de meeste fase-2-sprites.

## Samenvatting
- Oordeel: **AF NA KLEINE REPARATIES**: 2 punten, 6 px, geen silhouetwijziging.
- Techniek in orde: 4-bit geïndexeerd, 16 kleuren, index 0 transparant, 1 component, geen gaten (behalve de bewuste ruimte tussen de voorpoten), palet gelijk aan `normal.pal`.
- R1: 3 lichtgrijze nagelpixels aan de onderrand (14,62), (16,62), (24,61) worden `A`.
- R2: 3 zwarte pixels aan de lichtkant van de handschoen (15,58), (14,59), (14,60) worden `9`.
- Op 1× leest hij als lama naast 9 echte Gen 3-sprites, op licht en donker. Oog, handschoenen, halsband, doek en kwasten zijn leesbaar.
- Licht komt consequent van linksboven, zonder pillow shading of ongewenste banding.
- Voor Jordi: de kleine staart, de ene leesbare achterpoot en de hoogte zijn modeleigenschappen en vallen buiten deze keuring.
