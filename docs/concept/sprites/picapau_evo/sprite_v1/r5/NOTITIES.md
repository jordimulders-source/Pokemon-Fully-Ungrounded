# Picapau-evolutie: sprite r5 (nieuwe pose R2 uit r7pose)

## Jordi letterlijk
- Over sprite r4: **"dit is geen driekwart aanzicht, laten we daar mee beginnen. Zijn mond is gewoon een rode wolk, de kuif staat teveel rechtop, die mag meer naar beneden buigen. Maar het begint met het driekwart aanzicht wat niet klopt en de hele sprite mag wat meer achterover leunen zoals raichu in gen 1"**
- **"ik kies p3, en hij mag nog iets meer naar rechts draaien, net als gen 1 raichu beide ogen in beeld, of gaat het niet passen om ook de linkervleugel in de sprite te krijgen lichtjes? Zijn er vogel sprites die dat hebben?"**
- **"ja pidgeot toont hoe het moet"**
- **"ga gewoon een sprite maken aub"**
- **"r2 trouwens, onderste, alleen snavel moet nog licht open"** → de bron is R2 uit `../../blender/r7pose/` (de render in de onderste rij van `vel_pose.png`), en de snavel is licht open in plaats van wijd.

## Werkwijze (zoals r3/r4)
- `bron/renders.py` rendert, in dezelfde stand en hetzelfde kader als `R2_8x.png`:
  - `labels.png`: een labelkaart;
  - `wit.png`: een witte toonkaart.
- `bron/bron.py` → `bron_labels.txt`, `bron_toon.txt`, `overtrekvel.png`.
- **`tekening.txt` is de sprite, helemaal opnieuw met de hand getypt voor de nieuwe pose.** De omtrek is cel voor cel overgetrokken, en kleur en schaduw zijn pixel voor pixel ingetypt.
  - Uit r3/r4 heb ik alleen de werkwijze, het palet, het oog van Picapau en de manier van tekenen (spiraal, poten, steunstaart) meegenomen. Er is niets geknipt of geplakt.
- `zet.py` → `raster.txt`, `bouw.py` → `picapau_evo.png` en `normal.pal`. Het palet is gelijk aan r4.
- `controle.py` → `controle_uitvoer.txt`.
- `vel.py` → `vel.png`: 1× en 8× naast r4, Pidgeot, Picapau, Taillow, Raichu Gen 1 en de R2-render.
- Draaien: `python3.11 zet.py && python3.11 bouw.py && python3.11 controle.py && python3.11 vel.py`

## Hoofdvraag: 3/4 zoals Pidgeot, achterover zoals Raichu Gen 1?
- **3/4: ja.** Borst en buik zie je van voren. De verre vleugel steekt links achter kop en borst omhoog als smalle waaier, de nabije vleugel staat groot open rechts, en de poten staan in perspectief. Op 1× leest dat veel meer als Pidgeot dan r4 (profiel).
- **Achterover: ja.** De buik komt omhoog en naar voren, met de kop erboven.
- **Beide ogen in beeld:** het nabije oog vooraan, het verre oog als half oog aan de linkerrand van de kop.

## Per punt
- **Mond ("een rode wolk"):** de snavel is licht open.
  - Grijs zoals Picapau: de bovensnavel heeft een G-rand en een lichte bovenkant (a/g), de ondersnavel g/G met een zwarte onderrand. Beide delen zijn ≥ 2 px.
  - Ertussen loopt een smalle donkere spleet van 1 px (k). Rood (C) zit alleen als 3 px in de mondhoek bij de snavelbasis.
- **Kuif:** zwart en naar achteren-omlaag in plaats van rechtop.
  - Nabije oor: een korte voet met G-glans, die horizontaal naar achteren loopt en overgaat in een spiraal van 1 px met een gat (zoals Gen 1), die onder de punt hangt.
  - Verre oor: een klein zwart haakje linksboven op de kop.
- **Verre vleugel:** ±7 px breed (de render ±4–5) en drie pennen met veerlijnen (4) en een lichte streep (3). De omlijning is 4 aan de lichtkant (linksboven) en zwart aan de onderkant.
- **Verre oog:** een half oog (4 px k) aan de linkerrand van de kop, achter de kopwelving.
- **Bliksem:** breed (tot 8 px) en vlak naar de kijker. Hij staat lager en verder naar links dan in de render, als zigzag met een plank (rij 37–38), van de framerand linksboven tot de staartschacht.
- **Buik:** één vloeiende curve van keel tot dijen, met de voorrand x 16 → 9 → 14 in stappen van 1. De crème is het grootste lichte vlak: licht linksboven tegen de belichte rand, sikkel e rechts en onder.
- **Wat in r4 goed was, is teruggebracht:**
  - nabije poot met een loopbeen van 3 px (g g G), een voet met teenscheiding en zwarte klauwen;
  - verre poot hoger en links, alleen G;
  - vleugel met een lichte voorrand (2), kleine dekveren (3), grote dekveren (v), en handpennen in een waaier met lichte bovenranden;
  - dijen als eigen vorm met een binnenlijn (4) en een sikkel;
  - kop-licht als smalle rand linksboven.
- **Stippen:** groter. Vier ronde stippen van 3×3 zonder hoeken (zoals Picapau) en vier van 2×2.
  - Een poging om de hoeken met b te vullen gaf losse pixels van 1 px; die heb ik teruggedraaid.

## Controle (`controle_uitvoer.txt`)
- Geen lichte kleur op de buitenrand.
- Geen losse pixels.
- Geen tintclusters kleiner dan 3 px.
- 15 kleuren + transparant, 1707 px.
- 1 px is alleen diagonaal verbonden; dat is de spiraallijn.

## Eerlijke zwakke punten
1. **Poten.**
   - De verre voet is een grijze balk van 2 rijen links onder de buik, vlak naast de bliksem.
   - De nabije voet leest als voet met klauwen, maar niet als losse tenen zoals bij Pidgeot.
   - De ruimte onder de buik is krap: bliksem, staartschacht, steunstaart en twee poten zitten op 15 rijen.
2. **Stippen op 1×.** De 3×3-stippen zijn kruisjes. Op 8× lezen ze als "+" (sterretjes) in plaats van rond. Rond zonder kleine clusters lukt alleen met 4×4 (te groot) of met een tweede stiptint in het palet.
3. **Kop.**
   - Het verre oog is op 1× een donkere vlek aan de rand van de kop, niet duidelijk als oog.
   - Het verre oortje lijkt op een sprietje.
4. **Flank.** Het oranje tussen buik en vleugel is smal (2–4 px). Daardoor lijkt de buik bijna los voor het lijf te hangen; dat volgt de render.
5. **Vleugel.** Op 1× is het nog steeds een groot donker vlak. De lagen lees je vooral aan de lichte voorrand en de stippen.

Er is niets gecommit en niets verwijderd. Ik heb ook geen modelwerk gedaan: alleen de label- en toonkaart van R2 zijn gerenderd.
