# Poedelmot sprite ronde 2 (6 nov): alleen de poten

Opdracht: alleen de poten, de rest pixel voor pixel gelijk. Bronnen, met Jordi's woorden letterlijk:
- "ok hier kunnen we in elk geval mee gaan beginnen. Zit nog erg ver van het eindresultaat af, maar dat komt goed. De poten hebben vrij willekeurige posities. Ik heb het concepteeul proberen te tekenen, plus hier nog twee fotos, de voorste poten mag je behandelen alsof het poten zijn van een zoogdier. Die komen ook wat hoger uit het boven lichaam en zijn niet echt stelten. De vier achterpoten functioneren als achterpoten alleen zijn het er 4 ipv 2, en die komen wat meer uit de zijkant"
- "kijk ook naar andere pokemon sprites van niet insecten hiervoor"
- "en het gaat vooral om de positie waar de poten uit komen, die zitten vrij ver naar voren, bijna op borsthoogte waar ze uit komen"
- "zie vooral deze foto als leidraad" (`referenties/vilt_poten_LEIDRAAD.png`, voor de poten boven de andere bronnen)

## Bestanden
- `poten.py` → `raster.txt`: neemt `ronde1/raster.txt` en vervangt alleen de pootzone door segmenten die met de hand getypt zijn. De pootzone is rijen 42-44 voor x≤33 (de aanzet in de borst) plus rijen 45-63.
- `teken.py` → `anim_front.png`, `normal.pal`, `sprite_8x.png` (zelfde palet als ronde 1).
- `controle.py` → `controle.txt`: **pixeldiff tegen ronde 1 = 511 px, waarvan 0 buiten de pootzone**; 0 lichte randpixels; 13 kleuren.
- `studie_poten.py` → `studie_poten.png`: niet-insecten op 8× (frame 1, raster per 8 px).
- `paneel.py` → `schets_overlay.png` (Jordi's lijnen over ronde 1 en ronde 2) en `pootpaneel.png` (close-up, de LEIDRAAD groot, de studie).
- `keurvel.png`: het vel van `tools/grounded/keurvel.py` (werk, ronde 1, LEIDRAAD, beide foto's, Eevee, Vulpix, close-up 4,42,46,63). Daaronder zijn de overlay en het pootpaneel aangeplakt. De keuring staat in `keurvel.png.keuring.md`.

## Jordi's schets (vak "ronde 1 + Jordi's lijnen" op het vel)
Uitlijning: ik heb gezocht naar de kleinste kleurafwijking tussen de schets en de close-up van ronde 1. Schaal 8,1, verschuiving (7,3), dus schetspixel (u,v) = spritepixel ((u−7)/8,1+4, (v−3)/8,1+42). Er staan zeven rode lijnen in, van links naar rechts (begin → eind, in spritecoördinaten):
1. (19,43) → (10,52): een boog naar linksonder, die eindigt op het linker stompje van ronde 1.
2. (22,45) → (16,53): schuin naar linksonder, eindigt boven op de linkerpoot van ronde 1.
3. (25,46) → (24,57): bijna verticaal, eindigt op de pompon van de middelste poot.
4. (29,45) → (27,58): bijna verticaal, iets naar links, eindigt rechts op die middelste poot.
5. (30,48) → (34,55): schuin naar rechtsonder, eindigt op de rechterpoot.
6. (35,45) → (39,53): twee bijna evenwijdige streken, schuin naar rechtsonder, op de rechterpoot.
7. (38,44) → (42,52): schuin naar rechtsonder, eindigt op het rechter stompje.
Wat ik eruit lees, zonder iets toe te voegen: alle lijnen beginnen hoger (y43-48) en meer naar het midden dan de poten van ronde 1. De twee middelste lopen recht naar beneden. De lijnen links en rechts lopen schuin naar buiten.
**Vraag aan Jordi:** rechts staan vier streken, waarvan twee dubbel. Bedoel je daar twee poten (zo heb ik het getekend) of meer?

## Pootstudie (`studie_poten.png`): wat ik van welke sprite gebruik
- **Eevee, Vulpix:** de voorpoten staan recht onder de borst, direct onder de kop, als korte kolommen. De verre voorpoot staat iets rechts en hoger, met een donkere lijn ertussen. Gebruikt voor de twee voorpoten naast elkaar.
- **Growlithe, Teddiursa:** de dikke, ronde voorpoten met een eenvoudige voet, zonder geleding. Gebruikt voor de dikte (6 px) en de pompon als voet.
- **Mightyena, Absol:** hun achterpoten komen uit een heup aan de zijkant van het lijf, met een donkere sikkel onder de heup. Gebruikt voor de heup links en rechts en voor de zwarte heuplijn waaronder de poten uitkomen.
- **Skitty, Ponyta:** alleen bekeken. Ponyta heeft dunne stelten, dus juist niet zo.

## Wat er gedaan is
- **Voorpoten:** twee kolommen van 6 px (x20-25 en x26-31) die direct onder de kin uit de borstwol komen. Hun contour begint op y43-45, in ronde 1 was dat y46-48. Ze gaan recht naar beneden, de verre staat iets rechts en hoger, met een donkere lijn ertussen. De pompons zijn 9-10 px (onderkant y60 en y56). Lijnen 3 en 4 van de schets vallen erop.
- **Vier achterpoten:** links en rechts een heup (de flank, vanaf y44-45) met een zwarte sikkel eronder. Per kant twee poten dicht bij elkaar: de buitenste schuin naar buiten en hoger, de binnenste eronder. Dat volgt lijnen 1-2 en 5-7.
- Kop, oren, ogen, vleugels en de bovenkant van het lijf zijn onveranderd (diff 0).

## Zwakke punten (eerlijk)
1. **De achterpoten spreiden zijwaarts** en lezen op 8× als peddels of octopusarmen, niet als dragende achterpoten. Op de LEIDRAAD-foto zijn geen achterpoten te zien, dus daar is geen bron voor. Vraag: moeten ze meer onder het lijf staan, of is schuin naar buiten (zoals je lijnen) goed?
2. De voorpoten zijn ±17 px lang (y43-60) en lezen samen nog als een zuil. Op de LEIDRAAD zijn ze korter en pluiziger.
3. Links en rechts zijn bijna spiegelbeeldig, terwijl de pose 3/4 is.
4. De heupen en poten zijn gladde vlakken, zonder plukjes wol aan de rand. Dat geldt voor het hele draft.
5. Er is nog geen onafhankelijke keurder geweest.
