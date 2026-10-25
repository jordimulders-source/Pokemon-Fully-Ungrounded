# Olinguito v2: kleursprite ronde 2

Basis: kleur ronde 1. De rijen 17–42 (kop, oor, masker, snoet, lijf en borst) zijn met de hand herschreven, en het palet is opnieuw opgebouwd vanuit de ontwerpkleuren (`pop3d.py`). De staart en de poten (rij 43 en lager) zijn de pixels van ronde 1, in het nieuwe palet.

**Bestanden:**
- `olinguito.png`: 64×64, geïndexeerd, 16 kleuren, index 0 transparant.
- `vel.png`, met:
  - ronde 2 op 4× op licht en op donker;
  - ronde 1 op 4×;
  - het gekozen ontwerp;
  - beide rondes op 1× op licht en op donker;
  - Linoone, Zigzagoon, Poochyena, Sentret en Furret op 4× en 1×, op licht en op donker (nu echt transparant).
- `bron/nieuw.txt`: de met de hand herschreven rijen.
- `bron/merge.py`: legt die rijen over ronde 1, controleert ze tegen het silhouet en schrijft de PNG.
- `bron/raster_grid.txt`
- `bron/vel.py`

**Alpha-bewijs:** `merge.py` meldt 0 fouten; een losse controle (index ≠ 0 tegen het silhouet van ronde 5) geeft **alpha-diff 0**.

## Palet (vanuit de ontwerpkleuren)
| # | letter | kleur | uit het ontwerp | gebruik |
|---|---|---|---|---|
| 0 | . | 98d0a0 | | transparant |
| 1 | k | 1a0f0b | pupil | omlijning, schaduwkant |
| 2 | m | 241712 | mask | masker (bijna zwart) |
| 3 | d | 4c3121 | far | lijf schaduw, selout van het lijf, verre poten |
| 4 | b | 6a4630 | fur, crown | lijf basis; de kruin vloeit hierin over |
| 5 | l | 8a603e | | lijf hooglicht (rug, schouder, borst, dij) |
| 6 | g | 6b5442 | head | kop basis, wang, bovenkant snoet |
| 7 | h | 8a6c55 | earin | voorhoofd licht, binnenkant oor |
| 8 | s | 54443c | muzzle | snoet, kopschaduw (keel, achterwang) |
| 9 | e | 4a3324 | ear | oorrand, selout van de kop, bovenrand van het masker |
| 10 | r | 6e2418 | | oog (donker roodbruin) |
| 11 | i | a8462a | | iris licht (tegenover de glans) |
| 12 | w | f2ead6 | claw / glint | klauwen, glans in het oog |
| 13 | n | b0a28a | | klauwschaduw |
| 14 | p | c08a80 | paw | voeten, licht op de neus |
| 15 | q | 8e4f58 | nose | neus, voetschaduw, verre voeten |

Voor de oogglans en de binnenkant van het oor is een kleur gedeeld (glans = klauwlicht, binnenkant oor = voorhoofdlicht), zodat alles in 16 kleuren past.

## Per punt
1. **Kop als één warme massa:**
   - Grijsbruin `#6B5442`, iets lichter en grijzer dan het lijf, zonder koel grijs.
   - De kruin achteraan gaat met een gekartelde grens van 2–3 rijen geleidelijk over in het lijfbruin (`b` tussen `g`). Er is geen diagonale kleurrand meer.
   - Het volume komt uit licht en schaduw: een lichtvlek op het voorhoofd linksboven (`h`), de basis op de wang, schaduw (`s`) achter op de kop, op de keel en onder de kaak.
   - De selout aan de lichtkant is warm (`e`), zwart alleen onder en rechts.
2. **Masker:**
   - Een duidelijke, bijna zwarte band (`#241712`) over het oog, van de snuitrug tot net achter het oog (x 9–24, y 30–34).
   - De bovenrand is één iets lichtere tint (`e`), zoals bij Zigzagoon maar donkerder.
   - Het oog blijft klein: glans linksboven, donker roodbruin, een lichtere iris rechtsonder. In de zwarte band leest het als rood kraaloog.
3. **Lijf: rustige vlakken in plaats van spikkels.**
   - Eén breed hooglichtvlak op rug en schouder (y 28–33), een middentint, en schaduw op de buik, de onderkant van de borst, de nek (slagschaduw van de kop) en de achterkant.
   - Bolle borst: hooglicht aan de voorkant van de borst (x 23–25, y 38–41), net boven de voorpoot.
   - Ronde dij: een donkere contourboog met een hooglichtkap linksboven (x 34–43, y 34–39).
   - Alle losse plukjes uit ronde 1 zijn weg; de enige textuur zit in de gekartelde randen van de vlakken.
4. **Wangen en snoet:**
   - De snoet is donker grijsbruin (`#54443C`) met een lichtere, ronde bovenkant (`g`) direct onder het masker en een oudroze neus vooraan.
   - De wang heeft de middentint van de kop (`g`), schaduw alleen op keel en kaakrand.
   - Er zit een klein donker mondstreepje achter de neus.
5. **Oor:** donkere rand `#4A3324` met een lichtere binnenkant `#8A6C55`, warm, met zwart aan de buitenkant rechts.
6. **Verre voorpoot:** ongewijzigd, als strook in de schaduwtint achter de nabije voorpoot.

## Toets op 1×
- **Naast het ontwerp:** dezelfde warme bruine kop met een zwarte band, het rode oogje, het ronde oor, het donkerbruine lijf, lichte klauwen, roze voeten en de staartboog. De helm-indruk is weg.
- **Naast Linoone en Zigzagoon:** dezelfde opbouw (3 tinten per groep, selout, licht linksboven, rustige vlakken). Hij oogt donkerder, wat bij Dark past (vergelijk Poochyena).

## Eerlijk: aandachtspunten
- **Het masker is één rechte band**, zoals in het ontwerp. Op 4× is de onderrand een vrij rechte lijn van ±15 px; op 1× leest dat als band, wat de bedoeling is.
- **De staart en de poten** zijn alleen opnieuw ingekleurd, niet opnieuw geschaduwd. Ze passen bij het nieuwe palet, maar de staart heeft nog de smalle lichtstrook van ronde 1.

## Lessen
- **Bouw het palet vanuit de ontwerpkleuren** en geef elke kleur er één lichtere en één donkerdere tint bij. Dan lijkt de sprite vanzelf op het ontwerp; eigen "mooie" kleuren (koel grijs) maakten van de kop een helm.
- **Twee aangrenzende kleurgroepen (kop en kruin) laat je in elkaar overvloeien** met een gekartelde grens van 2–3 rijen, niet met een rechte grens.
- **Plukjes in het lijf lezen op 4× als ruis.** Game Freak zet hooguit een paar plukjes aan de rand; vul het lijf met grote vlakken.
