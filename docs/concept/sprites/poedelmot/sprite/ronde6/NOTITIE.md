# Poedelmot sprite ronde 6 (6 nov): alleen de twee voorpoten, vanuit ronde 5

Jordi (letterlijk): "beter, de achterpoten zijn wel nog steeds losse aanhangels zonder verbinding. De voorpoten zien er beter uit, maar mogen meer naar het midden en lijken aan de uiteinden nog steeds niet goed op waar ik naar toe wil, vanaf de 'elleboog' moet het aflopen richting uiteinde van de poot en 2 hele minimale klauwtjes aan vast zitten. We gaan nog geleidelijker aan, eerst de voorpoten fixen, daarna pas achterpoten"

Deze ronde: alleen de voorpoten. De achterpoten komen in een latere ronde.

## Wat ik op de foto's zie, vanaf de "elleboog" (vóór het tekenen; `paneel_voorpoten.png`)
- **vilt_poten_LEIDRAAD:**
  - Na de knik loopt de onderpoot gelijkmatig smaller naar de vinger toe.
  - Er is geen verbreding en geen aparte voet: de wol wordt dunner en de poot eindigt in een smal eindje.
  - Op dat eindje zitten twee piepkleine klauwtjes, nauwelijks te zien.
- **zijdemot_blad_frontaal:**
  - Vanaf het gewricht loopt het onderbeen af naar een dunne punt.
  - De lange haren hangen langs het onderbeen omlaag. Daardoor lijkt het onderaan breder, maar de poot zelf wordt smaller.
  - Op de punt zit een heel klein donker klauwtje, vast aan de punt.
- **zijdemot_vinger:** hetzelfde: de onderpoot wordt naar de punt toe smaller en eindigt in een smal puntje met een minuscuul donker klauwtje.
- **Samengevat:** vanaf de elleboog smaller wordend naar het uiteinde. Geen pluk die eerst breder wordt (dat deed ronde 5), geen bol, geen driehoek. Aan de punt zitten twee minimale klauwtjes vast.

## Wat er gedaan is
- **De elleboog is rij 51**, waar de poot onder het lijf vandaan komt. Die rij en alles daarboven is onveranderd.
- **Linkervoorpoot:**
  - Van 7 px breed op y51-52 loopt hij af naar een punt van 3 px op y57: x16-22 → x17-22 → x18-22 → x18-21 → x19-21.
  - Hij smalt vooral aan de buitenkant en schuift zo naar het midden. De punt zat op x16-17 en zit nu op x19-21.
- **Rechtervoorpoot:**
  - Van 8 px op y52 loopt hij af naar een punt van 3 px op y58: x29-36 → … → x31-33.
  - De punt zat op x35-36 en zit nu op x31-33, ook meer naar het midden.
  - De binnenrand loopt in een boog (x29 → x31) en sluit aan op Jordi's lijn van ronde 5.
- **2 klauwtjes per voorpoot:** 1 px elk, in donkerbruin (b), elk direct onder een omlijningspixel van de punt. Ze zitten dus vast, met 1 px ruimte ertussen, zodat het er twee zijn en geen blokje. Links op x19 en x21, y58; rechts op x31 en x33, y59.
- **De achterpoten zijn pixel voor pixel ronde 5:**
  - Dat zijn P/Q en S/R1, met de omlijningspixels van de oude voorpoot die direct aan een achterpoot grenzen. Die pixels sluiten de rand van de achterpoot en zijn dus ook onveranderd gebleven.
  - Het masker staat in `achterpoten_masker.txt`.
- **Controle** (`controle.txt`): pixeldiff tegen ronde 5 is 110 px, waarvan 0 buiten de voorpootzone en 0 in de achterpoten. Er zijn 0 lichte pixels op de buitenrand en 13 kleuren.

## Bestanden
- `poten.py` → `raster.txt` + `achterpoten_masker.txt`;
- `teken.py` → `anim_front.png`, `normal.pal`, `sprite_8x.png`;
- `controle.py` → `controle.txt`;
- `paneel.py` → `paneel_voorpoten.png`: ronde 5 en ronde 6 op 16× naast LEIDRAAD, zijdemot blad en zijdemot vinger;
- `keurvel.png`: het keurvel.py-vel met ronde 5, LEIDRAAD, zijdemot blad, Mightyena en een close-up op 16×, met het paneel eronder. De keuring staat in `keurvel.png.keuring.md`.

## Zwakke punten (eerlijk)
1. **Achterpoten:**
   - Doordat de voorpoten naar het midden zijn geschoven, is de ruimte tussen voor- en achterpoten groter. Daardoor lijken de achterpoten nu nog losser: "losse aanhangels".
   - Rechts staat de oude omlijning van de voorpoot (x37-39, y52-57) nog als linkerrand van S.
   - Dit is bewust ronde 5 gebleven en hoort bij de volgende ronde.
2. **Punt:**
   - De punt is 3 px breed, met een grijze middenpixel (tint 2) tussen de twee klauwtjes. Smaller kan niet als er twee losse klauwtjes vast moeten zitten.
   - Of dat "hele minimale klauwtjes" is, moet Jordi zeggen.
3. **Wol:** de onderpoten hebben gladde randen. De haarpuntjes van ronde 5 zaten aan de pluk die nu weg is.
4. Een onafhankelijke keurder is nog niet geweest.
