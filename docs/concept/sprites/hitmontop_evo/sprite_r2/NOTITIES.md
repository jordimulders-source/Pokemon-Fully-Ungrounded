# Hitmontop-evolutie, sprite ronde 2 (5 nov)

Opdracht: de NODIG-lijst 1–10 uit `../sprite_r1/sprite.png.keuring.md` (FAIL). Bevroren: gezicht, steunarm met hand, cordão. De rest is opnieuw opgebouwd vanaf de posefoto (gespiegeld), eerst als silhouet en daarna rij voor rij met de hand. Er is geen hulpscript voor de vlakken gebruikt.

## Bestanden
- `sprite.png`: 64×64, 4-bit, 16 kleuren. `normal.pal`: hetzelfde palet als ronde 1.
- `raster.txt`: de sprite als tekst; `python3 bouw.py` maakt er de png en het palet van.
- `pose.py` → `pose_silhouet.png` / `pose_silhouet.txt`: stap A, de pose als silhouet. Per rij staan de bereiken (x_van, x_tot) per onderdeel met de hand opgegeven. Het vel toont de gespiegelde foto, het silhouet op 8×, de onderdelen in kleur op 8×, en 1×/2×.
- `kleur.py`: stap B, de kleur per onderdeel per rij als met de hand geschreven strings (de lengte wordt tegen het silhouet gecontroleerd), plus een paar losse pixels. Daarna gaan de bevroren delen er onveranderd overheen. Schrijft `raster.txt`.
- `bevroren.py`, `bevroren.txt`, `bewijs_bevroren.txt`: het bewijs van de bevroren delen (zie hieronder).
- `kop_stap1.png`: Hitmontop | gespiegeld (skelet) | ronde 1 | ronde 2.
- `vel_r2.png` (+ keurvel-sjabloon): 8× en 1× naast Hitmontop en ronde 1, met close-ups van de kop en van benen/heup.

## Bevroren (pixeldiff 0)
- **Masker:** 368 pixels.
  - Gezicht: ogen, wenkbrauwen, mond/plooi en gezichtsvlak (lokale kop-rijen 11–21) plus de kleine hoorn.
  - Steunarm met prajiad, witte pols en hand (r1 rijen 46–63).
  - Cordão: knoop, twee hangende einden en het zichtbare eind van de tailleband.
- **Verschuiving:** de hele sprite is 1 px omhoog geschoven voor de marge onderaan (NODIG 10). Bevroren betekent hier: elk pixel gelijk aan ronde 1 op (x, y−1).
- **Uitkomst:** `bewijs_bevroren.txt`: 0 verschillen op het tekstraster, 0 verschillen bij de controle direct op de beide png's, en het palet is gelijk.
- **Niet gedaan, botst met "bevroren":** de kin en de onderlijn van de kop (NODIG 8: rond) vallen buiten het masker en zijn wel nieuw. Twee POLIJSTEN-punten horen bij de bevroren steunarm en zijn daarom **niet** veranderd: het zijwaartse staartje van de prajiad en de grijs-witte polsmanchet. Graag een beslissing of die bevriezing daar mag wijken.

## Wat er per NODIG-punt is gedaan
1. **V-split:** het nabije been loopt ±40° schuin naar linksboven (heup ±(48,14) → enkel (35,3)). Het verre been loopt ±56° naar rechtsboven (heup → (59,7)). Het silhouet is nu een Y: de wijde V boven, de steunarm als steel onder.
2. **Geen zwaan:** de verre voet is klein en gestrekt in het verlengde van het been, met twee kleine klauwtjes aan de punt en een donkerblauwe zoom als enkel. Het verre been is een rechte schuine buis zonder knik of "kop".
3. **Nabije voet:** in zijaanzicht, de tenen wijzen naar links met twee klauwtjes, zool onder, zoom bij de enkel. Geen frontale schijf meer.
4. **Voeten kleiner:** nabij ±9×6, ver ±6×6, naar Hitmontops vorm (blauw, licht boven, klauwen in c/d, zwarte omlijning). Hitmontops voeten zijn ±15×13.
5. **Broek aansluitend:** de heup is een smalle, ronde broekheup tussen de tailleband en de twee benen (±9 px dik). Een contourlijn laat het nabije dijbeen vóór de verre heup lopen; geen trechter meer.
6. **Haar:** alleen op de schedel, glad naar achteren gezet, met één scheidingslijn naar achteren. Een rood bandje achter op het hoofd en twee dreads die daaruit recht omlaag hangen, achter de kop. Geen bruin meer langs wang of kaak (de linkerkant stopt op de slaap, rij 31) en geen streeppatroon. Een zwarte lijn onder de hoorn maakt hem los van het haar (polijsten).
7. **Vrije arm:**
   - De bovenarm komt van achter de bovenflank van de borst omhoog en heeft een prajiad met een kort eindje dat omlaag hangt (zwaartekracht, over de borst).
   - De elleboog zit onder het nabije dijbeen, met een open wig ertussen.
   - De onderarm gaat omlaag naar de ronde hand (Hitmontop-hand) op de heup, net naast het cordão.
8. **Nek:** een korte nek tussen de onderkaak en de schouderlijn, met de kaaklijn als binnenlijn. De onderkant van de kop is rond (kin rij 42–44), geen rechte 20-px-lijn meer.
9. **Romp:** schouder (deltoïde boven de steunarm) → bredere borst → smallere taille → tailleband. Licht linksboven met een sikkelschaduw (4) langs de onderflank. De schuine strepen zijn weg.
10. **Marge:** de figuur loopt van x 8–62 en y 1–62; niets op rij 0/63 of kolom 0/63.

## Anatomiecontrole op 8× (per punt)
- **Haar alleen op de schedel, valt logisch:** ja. Kruin rij 25–31. De twee dreads hangen recht omlaag achter de kop (x 28–32, tot rij 34), rechts van de gezichtsrand. Niets op gezicht, wang, keel of schouder; tot de vrije bovenarm is er 1–2 px lucht.
- **Kop met een nek op de romp:** ja. De nek (rij 38–43) loopt van de kaak naar het midden van de schouderlijn.
- **Gewrichten en aantallen:** 2 armen, 2 handen, 2 benen, 2 voeten.
  - Steunarm aan de nabije schouder.
  - Vrije arm: schouder–elleboog–pols–hand. Het schoudergewricht zelf zit achter de borstflank verborgen; de bovenarm komt daar zichtbaar te voorschijn.
  - Beide benen uit de heup, voeten aan de enkels.
- **Geen zwevende of losse stukken, geen restpixels:** met een script gecontroleerd: 1 samenhangend deel (4- en 8-buren). Tintclusters < 3 px: 37 (ronde 1: 70, Hitmontop: 87).
- **Geen dubbele omlijning op naden:** de kaaklijn, de contourlijn dijbeen/heup en de binnenlijn arm/borst zijn enkele lijnen. Rest: bij de knoop raken de handbal, de tailleband en de onderflank elkaar nog in een klein donker cluster (x 48–52, y 26–29).
- **Koordjes echt om broek en arm:** het cordão (bevroren) loopt van onder de hand over de taille naar de knoop, en de einden hangen recht omlaag. Prajiad om de steunarm (bevroren) en om de vrije bovenarm, met een hangend eindje.

## Zwakke punten (eerlijk)
1. **Haar is nog matig Eddy Gordo:** het leest als glad achterovergekamd haar met een klein staartje van twee korte dreads, niet als een volle bos dreads. Voor langere dreads is achter de kop geen plaats zonder dat ze de vrije arm of schouder raken.
2. **De benen zijn kort** (±18 en ±12 px) en het verre been is erg steil. Dat komt doordat de V binnen het vak moet passen boven de vastgezette heup/cordão-plek; de SPEC vraagt "langere benen".
3. **Vrije arm:** het schoudergewricht is niet te zien. Elleboog plus onderarm vormen een vrij kleine bult boven de handbal.
4. **Verre voet** is erg klein. Op 1× leest hij als een punt, nauwelijks als een Hitmontop-voet.
5. **Kleine donkere clusters:** bij de knoop (zie hierboven) en de twee grijze klauwpixels aan de voetpunten.
6. **Gezicht** is (bevroren) Hitmontops frons, niet ouder gemaakt.

Niet gedaan (bewust): frame 2, rug, icoon, shiny, naam/data. Niet gecommit.
