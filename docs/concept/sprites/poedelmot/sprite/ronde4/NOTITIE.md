# Poedelmot sprite ronde 4 (6 nov): alleen de poten, vanuit ronde 3 variant B

Jordi (letterlijk): "wederom vooruitgang. De rechterarm mag net wat groter. De poten mogen nog wat meer weggestopt. Daarnaast zijn de uiteinden van de poten geen bollen, maar meer puntig, kijk goed in het bronmateriaal. met hele kleine klauwtjes. Op zich goede pose dat 1 kant groter dan de ander is, alleen zou dan rechts net wat groter dan links moeten zijn volgens het perspectief toch? of kan het ook op deze manier qua hoek?"

Opdracht van de coördinator: rechts in beeld is de nabije kant (de kop kijkt naar links, de nabije vleugel staat rechts). Alle poten rechts worden dus net wat groter dan links. De klauwtjes zijn 1 px, donker.

## Wat ik op de bronfoto's aan de pootuiteinden zie (vóór het tekenen)
- **zijdemot_blad_frontaal:**
  - De onderpoot is een wollige koker. Bij de enkel waaiert de wol iets uit tot een pluk.
  - Die pluk loopt naar beneden spits toe, omdat de haren naar één punt samenkomen.
  - Op de punt zitten heel kleine donkere klauwtjes (bruinzwart), die net onder de wol uitsteken.
  - Er is geen bol of rond voetje.
- **vilt_hand:**
  - De poot wordt naar onderen dunner, tot een smal puntje.
  - Op het puntje zitten twee piepkleine zwarte klauwtjes, die als een V uit elkaar staan.
- **vilt_poten_LEIDRAAD:** dezelfde dunner wordende, wollige onderpoot. De voet is een smalle punt, de klauwtjes zijn op deze uitsnede nauwelijks te zien.
- **foto_tak_katoen_2:**
  - Aan de voeten hangen lange plukken wol, die naar beneden in punten uitlopen, als een kwast.
  - Op één voet is onder de pluk een klein donker klauwtje te zien.
- **zijdemot_vinger:** de voorpoot loopt smal toe naar een punt, met een klein donker klauwtje op de vinger.
- **Samengevat:** het pootuiteinde is een wolpluk die naar onderen spits toeloopt, met onder de punt twee piepkleine donkere klauwtjes.

## Wat er gedaan is
- **Voeten:** de bollen zijn vervangen door wolpluk-punten. Bij de enkel loopt de pluk iets breder uit en daarna over 4 à 5 rijen spits toe.
- **Klauwtjes (ronde 4b):** onder elke punt zitten twee klauwtjes van 1 px in tint 1 (donker). Ze zitten vast aan de omlijning van de voetpunt, als een uitstulping van 1 px naar beneden (onderste rij: klauw, punt, klauw). In de eerste versie van ronde 4 zweefden ze diagonaal los. Er staat geen enkele losse pixel meer in de omtrek; elke pixel heeft een buur boven, onder, links of rechts (gecontroleerd met een script).
- **Rechts groter (nabije kant):**
  - De rechtervoorpoot is breder (bovenbeen x30-38, voet 10 px breed) en lager: punt op y58, klauwtjes op y59.
  - De linkervoorpoot is kleiner: voet 8 px breed, punt op y57, klauwtjes op y58.
  - Rechts is de achterpoot S groter dan P links.
- **Meer weggestopt:**
  - De buik loopt nu door tot y52, in ronde 3 was dat y50. Daardoor is de opening tussen de voorpoten kleiner en zie je minder poot.
  - Van de achterpoten komen alleen nog kleine, spitse puntjes onder de buikrand en de voorpoten uit:
    - P en S zijn met klauwtjes;
    - Q en R1 zijn smalle reepjes, voor het grootste deel verborgen.
- Schouders, borst, kop, vleugels en oren zijn onveranderd.
- **Pixeldiff tegen ronde 3 B: 226 px, waarvan 0 buiten de pootzone (rijen 45-63)** (`controle.txt`). Er zijn 0 lichte pixels op de buitenrand en 13 kleuren.

## Bestanden
- `poten.py` → `raster.txt`;
- `teken.py` → `anim_front.png`, `normal.pal`, `sprite_8x.png`;
- `controle.py` → `controle.txt`;
- `paneel.py` → `paneel_uiteinden.png` (de pootuiteinden op 16× naast uitsneden van de voeten op zijdemot blad, vilt-hand, LEIDRAAD, tak en zijdemot vinger) en `paneel_poten.png` (ronde 3 B en ronde 4 op 16× naast elkaar);
- `keurvel.png`: keurvel.py-vel met ronde 3 B, Giratina, LEIDRAAD, zijdemot blad en vilt-hand. Beide panelen zijn eronder geplakt. De keuring staat in `keurvel.png.keuring.md`.

## Zwakke punten (eerlijk)
1. De klauwtjes zitten nu vast (4b), maar op 1× lezen ze als een donker randje onder de punt. Of dat "hele kleine klauwtjes" zijn, moet Jordi zeggen.
2. Q en R1 zijn bijna onzichtbaar. Van de vier achterpoten lezen er eigenlijk twee (P en S).
3. Het verschil tussen links en rechts is klein, ongeveer 1-2 px. "Net wat groter" heb ik letterlijk genomen.
4. Rechts loopt de voorpoot nog over in het lijf, waardoor die kant grijs en druk leest.
5. Er is nog geen onafhankelijke keurder geweest.
