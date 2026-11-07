# Poedelmot sprite ronde 3 (6 nov): variant B (achterpoten weggestopt) + voorpoten naar de foto's

Alleen variant B. Variant A vervalt (Jordi: "stop de achterste poten maar weg als bij giratina, maakt niet uit dat je ze maar half ziet").

Jordi's woorden (letterlijk):
- Op ronde 2: "beter maar het klopt nog niet. Het lichaam mag groter om het niet deflated eruit te laten zien, of de poten moeten weggestopt worden zoals bij giratina, kijk maar naar giratinas backsprite en tel de poten. Verder komen de voorste poten gewoon niet lekker uit het lijf, je hehbt daarvoor niet goed naar de foto's gekeken en je doet gokwerk"
- "stop de achterste poten maar weg als bij giratina, maakt niet uit dat je ze maar half ziet" / "ah ze staan niet op giratinas backsprite" / "wacht"
- Bij het officiële artwork van Giratina (Altered Forme): "hier zie je duidelijk 6 poten" / "die achterste 4 functioneren zoals we hier willen"
- "die twee voorpoten moeten echt netjes uit het lijf komen en niet als rechte lijnen"
- "silk moths kunnen ook als inspiratie bron dienen" (`zijdemot_vinger.png`, `zijdemot_blad_frontaal.webp`, `zijdemot_closeup_kop.png`). Bij de close-up: "alleen worden onze poten minder insect like" / "maar het geeft een goed beeld waar ze uit komen"

## Wat ik op de foto's zie (vóór het tekenen)
- **vilt_poten_LEIDRAAD / vilt_hand:**
  - De voorpoten komen uit de zijkanten van de borst, net onder de ooghoogte, links en rechts van de borstwol. Ze komen dus niet uit het midden.
  - Tussen de poten hangt een witte bef van borstwol, die iets naar voren uitsteekt.
  - Het bovenbeen gaat vanaf de schouder schuin naar beneden en is daar het dikst, met wol die naar beneden valt.
  - Ongeveer op een derde zit de knie, iets naar buiten. Daarna gaat de onderpoot naar beneden en iets naar binnen, en wordt naar de enkel toe smaller.
  - Het voetje is klein, en de voeten staan dichter bij elkaar dan de schouders.
- **zijdemot_blad_frontaal / zijdemot_closeup_kop** (alleen voor de plek, niet voor de vorm):
  - De poten ontspringen direct onder en naast de kop, aan de buitenkant van het gezicht.
  - Ze gaan eerst kort schuin naar buiten en beneden. Na de knie gaat de onderpoot bijna recht naar beneden.
  - De borst tussen de poten is een bolle wolmassa onder het gezicht. Het lijf zit erachter, en tussen de poten zie je onderaan de ondergrond.
- **foto_tak_katoen_2:**
  - Dezelfde aanzet: de schouders liggen naast en onder de ogen.
  - De bovenbenen zijn dik en wollig en buigen naar buiten. Daaronder hangen lange plukken wol naar beneden, zoals de pompons.
- **zijdemot_vinger (zijaanzicht):** de voorpoten komen vooraan het borststuk uit, direct achter en onder de kop. De andere poten zitten onder het lange lijf.

## Giratina (`graphics/pokemon/giratina/anim_front.png`, frame 1): poten tellen
- Jordi zei: "ah ze staan niet op giratinas backsprite". De backsprite is dus niet gebruikt.
- Op de frontsprite zijn de poten zelf bijna niet te zien. Onder de rand van het grijze lijf (y52-63) staan vijf groepjes gele klauwen:
  - twee vooraan onder de borst: links op x10-22 en in het midden op x24-34;
  - drie verder naar rechts onder het achterlijf: x40-48, x50-56 en x56-62. Die zijn klein en half verborgen.
- Er is geen dij of knie te zien: alleen voeten die onder de buik uitsteken. De zesde poot zit achter een andere.
- Toegepast op onze vier achterpoten: per kant twee pompons, die half onder de buikrand en half achter een voorpoot uitkomen (P en Q links, R1 en S rechts). Geen poot is helemaal te zien, zoals Jordi toestond.
- Onze poten blijven wollig met pompons (SPEC); de klauwvorm van Giratina is niet overgenomen.

## Bestanden
- `variant_B/poten.py` maakt `variant_B/raster.txt`: neemt ronde 2 en vervangt alleen de pootzone (rijen 40-44 voor x≤33, rijen 45-63) door stukken die met de hand getypt zijn.
- `variant_B/teken.py` maakt `anim_front.png`, `normal.pal` en `sprite_8x.png`.
- `variant_B/controle.py` maakt `controle.txt`:
  - **pixeldiff tegen ronde 2 is 529 px, waarvan 0 buiten de pootzone**;
  - 0 lichte pixels op de buitenrand;
  - clusters < 3 px: alleen glanspixels;
  - 13 kleuren.
- `paneel.py` maakt twee panelen:
  - `paneel_voorpoten.png`: de close-up van de voorpoten op 16× naast de LEIDRAAD, zijdemot blad, zijdemot close-up, tak, vilt-hand en zijdemot vinger, allemaal even hoog;
  - `paneel_achterpoten.png`: de achterpoten op 16× naast Giratina op 8× en de onderkant van Giratina.
- `keurvel.png`: het vel van `tools/grounded/keurvel.py` (B naast ronde 2, Giratina, LEIDRAAD en drie zijdemot-foto's, plus close-ups). De twee panelen zijn eronder geplakt. De keuring staat in `keurvel.png.keuring.md`.

## Wat er gedaan is
- **Voorpoten (L dichtbij, R ver):**
  - De schouders beginnen op y40-41, links op x16-21 en rechts op x29-33, direct onder de zijkanten van de kop.
  - Er is geen naad: het bovenbeen gaat over in de borstwol. Alleen een zachte schaduwlijn (tint 4/3) scheidt poot en bef, en die buigt mee.
  - Het bovenbeen buigt naar buiten tot de knie (L x13, y46-47; R x36, y45-47). De onderpoot gaat daarna terug naar binnen en wordt smaller tot de enkel (L x15-20, y50-52).
  - Onder de enkel zit een pompon: L x13-22 tot y60, R x28-35 tot y58.
  - Geen contour loopt langer dan 3 rijen recht door.
- **Borst:** een lichte bef tussen de poten (x23-28, y40-46). Daaronder ligt de buik in schaduw, met een bolle onderrand (y49-50). Onder die rand zit een opening tussen de voorpoten, zoals op de blad-foto.
- **Achterpoten:** het lijf loopt door tot een buikrand op y50-51. Daaronder komen vier korte pompons half tevoorschijn, zoals de voeten van Giratina:
  - links P (x6-11), helemaal zichtbaar, en Q (x12-14), half achter L;
  - rechts R1 (x36-37), half achter R, en S (x38-44).

## Zwakke punten (eerlijk)
1. **De voorpoten lezen nog niet scherp als poten.** Het bovenbeen valt op 8× weg in het grijs van de borst en de flank. Vooral de verre poot R mengt rechts met het lijf. Je ziet de poten vooral aan de opening en de pompons. Op de foto's laten wolrichting en schaduw de poot duidelijk los van de bef komen.
2. De bef is een vlek zonder plukjes wol, en ook rond de poten ontbreekt de wol.
3. De achterpompons links (P en Q) en rechts (R1 en S) vormen samen met de voorpompons één rij voeten onderaan. Dat leest wat druk.
4. Links en rechts zijn nog vrij symmetrisch.
5. Er is nog geen onafhankelijke keurder geweest.

Vraag aan Jordi: is dit de goede plek en richting voor de voorpoten? Zo ja, dan maak ik ze in de volgende stap duidelijker los van de borst, met schaduw en wolplukjes zoals op de foto's.
