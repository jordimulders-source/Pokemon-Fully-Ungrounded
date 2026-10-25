# Olinguito v2: proef met splicen (25 okt, parallel aan dreamy-clarke)

Doel (Jordi): onderzoeken welke methode het beste werkt; deze map test splicen (DC-gids sectie G) naast het
handwerk op silhouet ronde 5 in `claude/dreamy-clarke-uuvynm`.

## Wat gedaan is
- **Basis Linoone** (Jordi: "pose als linoone", "iets minder recht, alsof hij van een tak naar beneden klimt"):
  - Linoone's palet-indexen zijn per rol omgezet (zie `stap1.py`), zodat zijn omlijning en schaduwvlakken blijven en de
    strepen één vachtkleur worden. Hooglicht komt binnen 3 px onder de bovenrand.
  - De kolommen zijn naar links steeds iets verder omlaag geschoven (1 px per 7 kolommen). Verticale lijnen blijven
    recht; horizontale lijnen worden gelijkmatige trapjes.
- **Kop** met de hand (Jordi: "het hoofd moet ronder"), geleid door het 3D-model op 20°: masker zoals Zigzagoon,
  donkerrood oog, warme grijzen van Zigzagoon, bruine kruin die in de nek overloopt.
- **Staart:** dun, omhoog met een haak bovenin. **Klauwen:** Sandslash-opbouw, kleiner ("klauw kan je van sandslash
  pakken maar kleiner"). **Voeten:** oudroze.
- **Op silhouet ronde 5** (bevroren): eerst Zigzagoon's kop erin gelegd (`sp1.py`), daarna een gladde kop (`sp2.py`).

## Bevindingen
1. **Splicen werkt alleen als onderdelen hun eigen vorm meenemen.** Op de Linoone-basis zijn de omlijning, de
   schaduwvlakken en de pootstanden direct van spritekwaliteit. Het ontwerp moet dan wel naar het onderdeel toe buigen.
   De kop wordt kleiner en het lijf langer dan in het B2-ontwerp.
2. **Op een vast, eigen silhouet past geen bestaand onderdeel.** Zigzagoon's kop neemt zijn stekelvacht en zijn
   vlekmasker mee en leest als Zigzagoon. Een gladde olinguitokop heeft geen broertje. Splicen wordt dan gewoon met de
   hand pixelen: dezelfde route als dreamy-clarke.
3. **Wat wél overdraagbaar is:**
   - per rol omkleuren (index → rol): dat geeft goede omlijning en schaduwvlakken zonder rekenregels;
   - kleuren uit echte sprites (Sentret-bruin, Zigzagoon-grijs, Poochyena-rood);
   - klein werk zoals klauwen of een masker in de opbouw van een echte sprite.

## Oordeel Jordi (25 okt)
"ja dit is niet goed nee, geen lelijke sprite maar een heel ander dier, plus hoofd niet zo mooi"
- Afgekeurd: de Linoone-basis maakt er een ander dier van (lang, laag, wezelachtig). Niet herhalen.
- De handgetekende kop (helm met masker) is niet mooi genoeg.
- Wat wel werkte: de pixels zelf ("geen lelijke sprite"). Per rol omkleuren levert spritekwaliteit, maar het lijf
  van een ander dier als basis nemen niet.
