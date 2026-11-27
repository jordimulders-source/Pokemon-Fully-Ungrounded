# Eindkeuring ek3 (DC, verse keurder, 27 nov)

Getoetst: `sprite/r15/r15.png`, alleen de gewijzigde zones (koepel, nabije arm, beide benen). Diff met ek2 = 138 px, alle binnen die zones; palet gelijk aan ek2 (15 kleuren + index 0).

**Oordeel: PASS.** `ek3.png` = r15, pixelgelijk (0 px gerepareerd).

## Per zone
- **Koepel:** toprij 5 px, daarna trapjes 2-2-2-1-1-1 (links) en 2-2-1-1 (rechts): geleidelijk aflopend, geen lange rechte lijn meer, geen spijkertje. Hooglicht linksboven sluit aan op ek2.
- **Arm (nabij):** rechterrand nu zwart (schaduwkant) in 1-px trapjes, taps naar de pols; geen rechte band meer. Lange linkerwand van de romp/bovenarm is ongewijzigd (model ook recht, buiten opdracht).
- **Trapbeen:** 4 ringen van 3 rijen (volle rij met ramp licht→donker, ingekeepte rij, donkere scheidingsboog), buitenrand bolletje/inkeping per ring, links selout, rechts zwart. Leest op 1× en 2× als geribbeld Hitmonlee-been (zelfde bouw als de spiraal van de Gen 3-Hitmonlee: segmenten van ±3 px, licht links, donkere scheiding). Aansluiting voet (rij 11) en doorschijnend deel in de romp netjes.
- **Standbeen:** 3½ ringen in dezelfde bouw, loopt 1 px naar rechts zoals het model; aansluiting onder de romp en op de enkel netjes.
- **Kleur/licht:** licht links, schaduw rechts, tinten uit het bestaande palet; past bij de rest van het glas.

## Open (geen FAIL)
1. Trapbeen rechterrand springt rij 15→16 2 px in (48→46): inkeping valt samen met de knik naar links. Leest als ribbel, niet als slordige lijn; verschuiven verplaatst de 2-px sprong alleen naar links.
2. Ringaantal lager dan het model (trapbeen 4 i.p.v. ±6, standbeen 3½ i.p.v. ±5) en trapbeen iets kraleriger/dunner op de inkepingen: bewuste keuze van r15 (modelaantal past op 64 px alleen als 1-px ladder). Jordi beslist.
3. Ringen iets roder/donkerder dan ek2 (minder crème); glas leest nog, gloed zit in de romp.

Bestanden: `ek3.png`, `ek3_8x.png`, `vel3.png` (ek2 | ek3 | model | Gen 3-Hitmonlee op 8×, plus 1×/2× licht en donker).
