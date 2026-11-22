# Onweerswolk-Altaria r13: eindkeuring (21 nov)

Jordi: "Als je dat gedaan hebt mag die naar de eindkeuring, zorg er ook voor dat de nek netjes aansluit op de wolk en dan lijnen, kleurtinten, schaduw eindkeuring".
Getoetst: `altaria_r13.png` tegen r11A (kop "perfect"), r9 (wolk bevroren), de Gen 3-Altaria-kop en de Swablu (`../../af/swablu.png`). Geen herontwerp: kop, kuifvorm en wolkvormen blijven.

## Bevindingen r13
- **Kop en kuif** zijn foutloos 2 px verschoven (alle violette pixels van r11A staan op x+2; diff 0 binnen de laag).
- **Vulstrook links van de hals** (Y30–40) volgt netjes de wolkbanden (3 / 5 / 6 / 4); geen tussentinten, geen losse pixels. Links van de kop: zakje lucht tussen vleugelrand en kop (Y19–23), loopt als V dicht; acceptabel.
- **Fout 1 (hals):** de navy selout links van de hals stopt op Y38, terwijl de hals tot Y40 doorloopt (bij (24,39)/(25,40) violet direct tegen teal); en op Y32 een dikke L-hoek (24,32)+(25,32)+(24,33).
- **Fout 2 (kuif over de rechtervleugel, door de schuif):** ingesloten transparant gaatje (46,20) (wordt in-game de achtergrondkleur) en de kuifpunt (55,18)=10 loopt zonder lijn over in vleugeltint 6 op (56,18) (in r11A eindigde hij tegen de vleugelselout).
- **Lijnen:** gekleurde selout overal (2 wolk, 8 kop/kuif, lichtere 10 als selout linksboven op de kop zoals in de Gen 3-Altaria); zwart (1) alleen in de 5 pupilpixels. **Tinten:** 13 kleuren + transparant, heldere vlakken. **Schaduw:** licht linksboven op kop (12 linksboven, 8/9 rechts), hals (11 links, 9 rechts), kuif en wolk; consistent, geen pillow shading.

## MOETEN (toegepast in `proef_eindkeuring.png`, 5 px, geïndexeerd, zelfde palet, transparency=0)
Zone hals (aansluiting op de wolk):
- (24,32) 2 → 5: L-hoek weg; selout wordt een schone diagonaal (25,32)→(24,33), vul = bandtint 5 van die rij.
- (23,39) 5 → 2: selout links van de hals loopt door.
- (24,40) 4 → 2: idem, tot de voorste wolkkwab (Y41); de hals verdwijnt nu met lijn achter de wolk.

Zone kuifstreng over de rechtervleugel:
- (46,20) 0 → 8: ingesloten gaatje dicht; sluit de onderrand van de streng (46,19)–(45,21).
- (56,18) 6 → 2: kuifpunt eindigt weer tegen de vleugelselout (zoals in r11A).

Zelf gecontroleerd op 8× (wit) en 1× op wit/crème/grijsblauw/zwart: hals heeft een doorlopende rand van kin tot wolk, geen gaatjes, geen nieuwe tinten.

## ZOU KUNNEN (niet nodig voor PASS)
- (46,21) 10 → 2: het onderste kuifpixel ligt op de oude vleugelrand en raakt teal (47,21)/(46,22) zonder lijn; met 2 is de vleugeldiagonaal (47,20)–(45,22) weer heel (kost 1 kuifpixel).
- Onderkant hals (Y39–40) tegen de voorste wolkkwab heeft geen bovenlijn op de kwab; bevroren wolk (r9), alleen op Jordi's verzoek.
- Dubbele 8-diagonaal rechtsboven op de kop (32–33,18)/(31–32,19) komt 1-op-1 uit de Gen 3-Altaria; laten staan.

## Oordeel
r13 zoals hij is: **FAIL** (2 technische fouten door de schuif + onderbroken halsrand).
Na de 5 MOETEN (`proef_eindkeuring.png`): **PASS**.
