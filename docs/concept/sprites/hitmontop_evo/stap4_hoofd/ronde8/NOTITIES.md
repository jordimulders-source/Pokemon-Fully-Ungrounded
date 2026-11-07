# Stap 4 hoofd, ronde 8 (6 nov): bron is Hitmontops overworld-kop (rechtop, van voren)

Jordi's recept: de V naar achteren, een knot als rondje met een witte band zoals zijn handen, en een kleinere stekel. Erbij: "zorg ervoor dat het wel een stekel wordt en niet een ingedeukt weetikveelwat" en "zorg dat de bovenkant van het hoofd smooth blijft, ondanks de lijnen". Referentie: `hitmontop_3d.webp`. Script: `stap4_r8.py`, met de hulpbestanden `ow.py` en `hulp.py`. Draaien vanuit de repo-root.

## Stappen
Bestanden: `stap1`–`stap7*.png`, samen in `vel_stappen.png`.

1. **Uitsnede:** de kop uit `overworld.png` (frame 1), met de regel van `KOP_OW` in `stap3b.py`. Het OW-palet is omgezet naar het frontpalet en de buitenrand is zwart.
2. **Groter:** kolommen 7, 9, 15, 21 en 23 en rijen 13–15 zijn verdubbeld. Resultaat: 24 px breed.
3. **Glad en frontgezicht.**
   - De trapjes van het verdubbelen zijn weg; de koepelomtrek is per rij vastgelegd (`KOEPEL`).
   - De ogen zijn Hitmontops frontsprite-oog, 1:1. Het OW-oog is 3 px en leest uitvergroot niet. De mond is een recht streepje van 6 px in de donkerste huidtint.
   - Licht linksboven, en een schaduwsikkel rechtsonder.
   - De flappen hangen in deze stap nog opzij, en de V staat vlak boven de ogen.
4. **V naar achteren:** de flappen hangen niet meer opzij. De V-lijn ligt binnen de kop in de donkerste huidtint (5, met de uiteinden in 4), 3 rijen hoger. Het voorhoofd is vrij, en de omtrek van de koepel blijft één ronde lijn.
5. **Knot:** Hitmontops linkerhand (`anim_front` x9–16, y28–35), 1:1, achter de kop. Zijn polsband (wit midden, grijs aan de randen, omlijnd) zit tussen knot en kop, ook achter de kop, zodat de omtrek niet vervormt.
   - Variant 1: knot achter op de kruin, linksboven.
   - Variant 2: knot achterop/opzij, laag achter de wang.
6. **Stekel kleiner:** dezelfde rechte kegel met een spitse tip van 1 px. Breedtes per rij, van tip naar voet: groot 1-3-3-3-5-5-7, klein 1-3-3-5-5. Licht links.
7. **Gedraaid, 12° tegen de klok in.** De pixels zijn niet gedraaid. Op de gedraaide vorm zijn opnieuw gelegd:
   - omtrek, licht en schaduw;
   - ogen en hand 1:1;
   - V en mond als rechte lijnstukken;
   - band en knot achter de kop.

## Opgeleverd
- `hoofd_1_rechtop.png`, `hoofd_1_gedraaid.png`, `hoofd_2_rechtop.png`, `hoofd_2_gedraaid.png`: elk 64×64.
- `vel_hoofd.png`: 8×, 2× en 1× naast de overworld-sprite, de frontsprite en de 3D-referentie.
- `controle.txt`: de "open randen" daarin zijn de bruine (5) lichtrand van Hitmontops hand en de grijze bandrand. Die zitten zo in zijn eigen hand; de kop zelf heeft geen open randen.

## Zwakke punten (eigen blik)
- **Bolvorm:** de kop is een brede, ronde koepel van 22×20 met een punt. Dat komt dichter bij de 3D-koepel dan de "boon" van ronde 7, maar leest nog als bol met een stekel. De 3D-kop is hoger en loopt meer kegelvormig naar de stekel.
- **Kammen niet zichtbaar:** "naar achteren gekamd" zie je alleen aan de hoge V. Van voren is er geen haarmassa die naar de knot loopt.
- **Knot leest verkeerd:** variant 1 leest op 1× als een bolletje/oortje linksboven (Mickey-oor), variant 2 als een bal tegen de wang. De band is op 1× maar een grijs puntje.
- **Weinig eigen pixels:** behalve de ogen en de hand zijn de pixels vooral met de hand gelegd naar de verdubbelde OW-vorm, niet de OW-pixels zelf; die zijn te grof voor deze maat.
- **Schaduw nog niet per pixel nagewerkt:** die is per regel gelegd (sikkel), met een brede 4/5-band rechtsonder.
- Niet onafhankelijk gekeurd.
