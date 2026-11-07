# Hitmontop-evolutie, sprite ronde 3 (reparatieronde, 5 nov)

Opdracht: NODIG 1–6 uit `../sprite_r2/sprite.png.keuring.md`, plus POLIJSTEN behalve de frons. De opbouw (pose, lijf, benen) uit ronde 2 is gebleven. Alles is rij voor rij met de hand in `kleur.py` geschreven; de silhouetbereiken staan per rij in `pose.py`.

## Bestanden
- `sprite.png` (64×64, 4-bit, 16 kleuren), `normal.pal`, `raster.txt` (bron), `bouw.py`.
- `pose.py` → `pose_silhouet.png` / `.txt` (pose naast de gespiegelde foto); `kleur.py` → `raster.txt`.
- `bevroren.py` / `bevroren.txt` / `bewijs_bevroren.txt` en `verschil_r2_r3.png` (rood = gewijzigd t.o.v. ronde 2).
- `kop_stap1.png`: Hitmontop gespiegeld | ronde 2 | ronde 3. `vel_r3.png` (+ keurvel-sjabloon): 8× en 1× naast Hitmontop en ronde 2, met close-ups van kop/arm en voeten.

## Palet
Index c (was lichtgrijs, alleen voor de klauwen en de polsband gebruikt) is nu haar licht (98,58,36). Index e is haar donker (50,28,18). Het haar heeft daarmee een eigen, donkere chocoladetint die op 1× los van de huid leest. De klauwen gebruiken nu wit 1 + grijs d.

## Bewijs bevroren (`bewijs_bevroren.txt`)
- **Bevroren, gelijk aan ronde 2:** gezicht met mond en wenkbrauwen, steunarm en cordão: 301 pixels, 0 verschillen, zowel in het raster als in de png-indexen. Geen enkel bevroren pixel gebruikt c of e, dus de paletwissel raakt ze niet.
- **Buiten de opdrachtzones:** 0 verschillen tussen ronde 2 en ronde 3. De zones zijn haar+hoorn, vrije arm/hand, voeten+benen, romprand, linkeroog, polsband+staartje.

## Per NODIG-punt
1. **Haar:**
   - De lokken zijn naar achteren getrokken in drie dikke strengen over de schedel; ze stappen naar voren één rij omlaag (de koepel van de kop).
   - Ze zijn opgebonden met een rood bandje achter op de kruin. Daaruit komen drie dreads die naar achteren buigen en met de zwaartekracht omlaag hangen achter de kop, met de punten op verschillende lengte (rij 31, 33, 35).
   - Het plukje in huidkleur op x29–33, y28–32 is weg.
   - Alles staat in de eigen haartint en alleen op de schedel. De bundel valt naar achteren en omlaag, niet opzij: de kop is ±2 px breder geworden.
2. **Hoorn:** 4 rijen hoog. Het is pixel voor pixel Hitmontops hoorntop (zijn gespiegelde rijen 1–4: `ff / f45f / f345 / f3344f`) in de huidtinten, en hij staat op het haar.
3. **Vrije arm:**
   - De bovenarm (met prajiad en een hangend eindje) komt van achter de borstflank omhoog.
   - De elleboog zit onder het dijbeen. Daarna loopt een zichtbare onderarm schuin omlaag naar de ronde hand op de heup.
   - In de elleboogholte zit een open gaatje, en er is een binnenlijn (5) waar de arm tegen het lijf ligt.
4. **Voeten:**
   - Eigen voetvorm: rond, licht boven en schaduw onder.
   - Een donkerblauwe zoom vormt de enkelovergang.
   - Klauwen van 2 px (wit 1 + grijs d), aan de buitenkant omlijnd.
   - Nabije voet in zijaanzicht (tenen links); verre voet gestrekt in het verlengde van het been (klauwen boven).
   - Marge: de bovenste pixels (omlijning van de klauwen) staan op rij 1, de voeten zelf vanaf rij 2–3.
5. **Banding:**
   - Benen: licht en schaduw wisselen nu van breedte: smal bij de enkel, een lichte bult bij de knie, breed licht op de dij. De verre been-schaduw verbreedt naar de heup.
   - Romprand: de lichte baan (2) zit alleen nog bij de borst, daarbuiten selout 5 + 3.
   - **De steunarm zelf heb ik niet aangepast:** die is bevroren. Alleen de polsband en het staartje zijn vrijgegeven, dus de gelijke rijen daar blijven.
6. **Ogen:** het linkeroog staat 1 px naar rechts en is los van de buitenlijn (er zit huid tussen). Beide ogen zijn nu exact Hitmontops oog (4×4: `.ff. / f1ff / ffff / .ff.`), dus even groot.

**POLIJSTEN:**
- Polsband weg (huid zoals de arm erboven) en het prajiad-staartje van de steunarm weg.
- De glans op de vrije hand is kleiner (lichtste huidtint 2, geen wit).
- De frons is niet veranderd. Het kantelen van de kop en de selout om de kop heb ik niet gedaan: de kop moet rechtop blijven en het gezicht is bevroren.

## Anatomiecontrole op 8×
- **Haar alleen op de schedel, valt logisch:** ja. Kruin rij 24–31, bundel achter op het hoofd, dreads hangen recht omlaag achter de kop (x29–35, tot rij 36). Niets op gezicht, wang, keel of schouder: tot de vrije bovenarm en de borstflank zit 1 px lucht, en de neknaad (rij 38) is vrij.
- **Kop met een nek op de romp:** ja, de nek loopt van de kaak naar de schouderlijn (rij 38–43).
- **Gewrichten en aantallen:**
  - 2 armen: steunarm aan de nabije schouder; vrije arm met bovenarm–elleboog–onderarm–hand (het schoudergewricht zit achter de borstflank).
  - 2 handen, beide rond.
  - 2 benen uit de heup, 2 voeten aan de enkels.
- **Losse stukken:** script-gecontroleerd: 1 samenhangend deel (4- en 8-buren), geen zwevende pixels. Tintclusters < 3 px: 32.
- **Dubbele lijnen:** geen nieuwe. Rest uit ronde 2: het kleine donkere cluster bij de knoop.
- **Koordjes:** cordão bevroren en ongewijzigd (om de taille, knoop, twee hangende einden). Prajiad om de steunarm (band, nu zonder staartje) en om de vrije bovenarm (met een eindje dat omlaag hangt).
- **Marge:** x 8–62, y 1–62.

## Zwakke punten (eerlijk)
1. **Haar:** de strengen over de kruin lezen als dikke, glad naar achteren liggende lokken, met horizontale lijnen. De dreads lezen vooral in de hangende bundel achterop. Een volle Eddy Gordo-bos is het niet.
2. **De kop oogt groter dan het lijf:** ±27 px breed tegen een romp van ±15 px. Het gezicht is bevroren en de kop moet rechtop blijven, dus dat kon ik in deze ronde niet oplossen.
3. **Steunarm:** de rij-voor-rij gelijke shading (banding) is gebleven omdat die arm bevroren is.
4. **Benen:** de variatie in licht en schaduw is subtiel. Op 8× zie je de lange evenwijdige randlijnen nog.
5. **Frons:** blijft liggen bij Jordi.
6. **Cluster bij de knoop:** handbal, tailleband en flank raken elkaar daar nog.

Niet gecommit.
