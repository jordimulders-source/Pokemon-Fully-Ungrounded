# Poedelmot sprite ronde 11 (6 nov): alleen de achterpoten, vanuit ronde 10, binnen Jordi's vormen

Jordi op ronde 10 (letterlijk): "ja die lus is expres smal, omdat het design anders niet klopt. De benen zijn nu wel te dik en ik zie er maar 1 ipv 2, de benen moeten dus smaller, linksonder zie je van het achterste been maar een heel klein beetje, en van rechtsonder ook een klein beetje. Plus ik wil dat rechts aangesloten wordt op het lijf, ik heb nog geen enkele sprite gezien waar die poten ook echt vast lijken te zitten aan het lichaam en niet er half aan geplakt"

## Wat ik zie: hoe een poot vastzit
Zie de onderste rij van `paneel.png`.
- **Giratina, nabije achterpoten (16×, x42-62, y38-60):**
  - Het grijs van het achterlijf loopt zonder lijn door in de bovenkant van de poot.
  - Waar lijf en poot elkaar raken, staat alleen een **donkergrijze schaduwvlek** (een tint van het vlak), geen zwart.
  - Zwart staat alleen aan de buitenrand, en verticaal waar de rechtervoorpoot vóór de achterpoot valt.
  - Je ziet **twee** achterpoten: de voorste helemaal en de achterste maar half, als een stukje voet ernaast.
- **Giratina, verre achterpoten (x14-36, y48-60):** tussen de voorpoten komt een donker stuk voet onder de buik uit; het donker van de buik loopt erin door. Daarachter staat een tweede, nog kleiner stukje.
- **Tak-foto's:** de wol van de flank loopt door in de poot, zonder naad of lichte rand. De achterste poten zie je maar als een plukje achter de voorste.
- **Wat in ronde 10 "half eraan geplakt" was:** rechts liep de zwarte rand van de arm (x38-39, y45-49) als een lijn tussen lijf en achterpoot door, van boven tot onder. Daardoor leek de poot een losse strook die tegen het lijf was geplakt.

## Wat er gedaan is
- **Aansluiting rechts:** de zwarte rand tussen arm/flank en achterpoot (x38 y45, x39 y46-49) is donkere wol geworden (tint 3), zoals Giratina's donkergrijs. De flank loopt nu zonder lijn door in de twee achterpoten. Lager blijft de zwarte rand van de rechtervoorpoot staan (x38 y50, x37 y51, x36 y52 en verder), op de plek waar die vóór de achterpoot valt.
  - **Let op:** die 5 pixels zijn de bovenste rand van de rechterarm (boven rij 52). Het onderste deel van de voorpoten (rijen 52-59) is ongewijzigd.
- **Rechts, twee poten binnen de lus:**
  - **S**, de middenpoot: smal, max. 4 px breed inclusief omlijning, met een punt en 2 klauwtjes op y56.
  - **A2**, de achterste poot: een klein stukje rechts naast S, 2 px, met 1 klauwtje op y56.
- **Linksonder (verre kant, binnen de U), twee poten:**
  - **M1**, de middenpoot: smal, max. 5 px breed inclusief omlijning, punt met 2 klauwtjes op y57. Hij komt uit de buik, zonder lijn ertussen.
  - **A1**, de achterste poot: een klein stukje van 1 px tussen M1 en de rechtervoorpoot, met 1 klauwtje op y56.
  - M1's linkerkant is donkere wol tegen de zwarte rand van de linkervoorpoot, zodat daar geen dubbele zwarte lijn staat.

## Meting (`controle.txt`)
- **Pootpixels buiten de vormen:** M1 0, A1 0, S 0, A2 0. In de hele pootzone: rechts 0, midden 0. De buikrand uit ronde 6 op (23-24, 52) staat apart, zoals in ronde 10.
- **Zichtbare achterpoten:** linksonder/midden 2 (M1 en een stukje A1), rechts 2 (S en een stukje A2).
- **Breedte (max., inclusief omlijning):** M1 5 px, A1 1 px, S 4 px, A2 2 px. Ter vergelijking ronde 10: midden 7 px, rechts 6 px.
- **Overig:**
  - links 0 pixels voorbij de lijn;
  - voorpoten (rijen 52-59) 0 gewijzigd;
  - 43 px diff tegen ronde 10;
  - buitenrand 0, gaten 0, 13 kleuren.

## Zwakke punten (eerlijk)
1. **Aansluiting rechts:** die heb ik gemaakt door 5 pixels van de zwarte armrand (boven rij 52) in donkere wol te veranderen. Jordi moet zeggen of dat mag, want het is de rand van de rechtervoorpoot.
2. **A1 en A2** zijn heel klein: 1 en 2 px plus een klauwtje. Op 1× lezen ze vooral als extra klauwtjes. Dat is "een heel klein beetje", maar het is de vraag of je ze nog als poot herkent.
3. **Midden:** M1 hangt onder de donkere buik, en de buikrand op (23-24, 52) blijft een zwart stukje links erboven.
4. Een onafhankelijke keurder is nog niet geweest.

## Bestanden
- `poten.py` → `raster.txt`, `poten.txt` (de cellen per poot);
- `teken.py` → `anim_front.png`, `normal.pal`, `sprite_8x.png`;
- `controle.py` → `controle.txt`, `diff.png`;
- `masker.py` en `overlay.py` (zoals in ronde 10);
- `paneel.py` → `paneel.png`: schets en masker over ronde 10 en 11 en ronde 11 los op 8×, de onderkant op 16×, en de aansluiting op 16× naast Giratina. Het paneel staat ook onder in `keurvel.png`.
