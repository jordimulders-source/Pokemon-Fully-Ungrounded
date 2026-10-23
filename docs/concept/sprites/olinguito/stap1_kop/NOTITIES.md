# Olinguito stap 1: kop in Galar-Linoone-constructie

Basis: `ronde18/anim_front.png`, palet `ronde18/normal.pal` (byte voor byte gelijk). Leidraad: `referenties/galar_linoone_front.png`.
Bouw: `bron/bouw_stap1.py` (met de hand per rij uitgeschreven, kolommen x9–23), vergelijking en bewijs: `bron/vergelijk.py`.

## Wat er veranderde (34 px per frame)
- **Verre oog weg** (ronde 18: x16–18, y30–32): het zit nu achter de neusbrug.
- **Verre maskerlob en verre wenkbrauw worden de neusbrug**: bruin voorhoofd (basis 4, hooglicht 5 langs de bovenrand, licht van linksboven), dat schuin van het voorhoofd naar de neuspunt loopt. De brug reikt tot net boven de neus (x11, y31), zodat de neus aan het eind van de snuit zit en er niet los op plakt.
- **Masker = band zoals bij Galar-Linoone**: de lob rond het nabije oog loopt onder de brug door tot aan de neus. De bovenrand van de band zakt in een curve van het oog naar de neus (x22 → x18 → x16 → x15, y29–32).
- Er komt **geen crème bij**; er gaat juist crème weg (verre wenkbrauw 77/7/6).
- De snuit gebruikt het silhouet van ronde 18, dat al schuin van voorhoofd naar neus liep. De kop blijft een eigen, ronde kop op dezelfde plek met de aanzet op het lijf (nuance van Jordi: geen kop-als-verlengstuk zoals bij Linoone; van Linoone komt alleen de gezichtsconstructie).

## Bevroren delen: pixeldiff-bewijs (`python3 bron/vergelijk.py`)
```
frame 1 gewijzigd 34 buiten kopzone x9-23 y25-32: 0
frame 2 gewijzigd 34 buiten kopzone x9-23 y24-31: 0
palet gelijk: True transparency 0
silhouet gelijk (beide frames): True; gewijzigde randpixels: []
```
- Gewijzigde pixels: bbox x11–22, y26–32 (frame 2: y25–31, de kop staat daar al 1 rij hoger).
- Pixel voor pixel ronde 18: **oren** (x15–36, y19–24), **nabij oog** (x24–28), nabije maskerlob vanaf x23 (alleen x22–23 op y29 werden masker, dus het masker werd groter, niet kleiner), nabije wenkbrauw, neus, grijns, kaak, lijf, poten, klauwen en staart.

## Checklist SPRITING §0
1. Diagonaal 3/4: ok. Het lijf staat zoals in ronde 18; de kop leest nu als 3/4 (één oog, snuit naar links-onder) in plaats van een frontaal gezicht met twee ogen.
2. Ledematen/oren/ogen: ok, alles uit ronde 18. Eén oog is bewust (snuitdier); het verre oog zit achter de brug.
3. Geen rechte lijnen: de silhouetlijn is ongewijzigd; de maskerband heeft een curve (1-3-2-1), geen rechte rand.
4. Ogen geïntegreerd: ok (nabij oog van ronde 16: bovenlid zwart, goud, glans).
5. Silhouet 1×: gelijk aan ronde 18. Het gezicht leest op 1× nu als een snuitdier in 3/4.
6. Formaat: ongewijzigd (kop niet opgeblazen of verkleind).
7. Pose: niet aangeraakt (stap 2/3).

## FAKEMON_CHECKLIST sectie B
- B1 kop meer naar de kijker dan het lijf: ok. De kop staat 3/4 en het lijf 3/4–profiel, zoals in ronde 18.
- B2 snuitlengte → ogen: ok. De snuit loopt ±15 px voorbij het oog (ongeveer de helft van de kop), dus één oog; de neus is het meest linkse punt van de kop (x9).
- B3 twee ogen: n.v.t. (één oog).
- B4 snuit één vorm in de kijkrichting: ok. De brug loopt schuin van het voorhoofd naar de neus links-onder, in dezelfde richting als de oog-as.
- B5 oren volgen de draai: ok (ronde 16: het verre oor is kleiner en ligt lager/achter).
- B6 kop overlapt het lijf: ok (ronde 18, ongewijzigd).
- B7 gezicht compleet: ok. Er zijn een oog, een neus en een grijns (klein, uit de mondhoek, zonder tong).

## Opdrachtpunten
- Eén oog: ok. Neus aan het uiteinde van de snuit: ok. Masker duidelijk als band: ok. Oren letterlijk ronde 16: ok (diff 0). Grijns zonder tong: ok.
- Verboden punten: geen nieuw beige of crème, het masker rond het oog is niet kleiner, de wenkbrauw blijft op de maskerrand (nabije wenkbrauw ongewijzigd, de verre is weg), geen schaling en het palet is ongewijzigd: ok.

## Zelfcheck (compare.png: 1×, 3×, kop 6×; onderlaag.png)
- Op 1× en 3× is het beter dan ronde 18: het "brilgezicht" met twee ogen in één band is weg. Het leest als een wasbeerachtig snuitdier dat 3/4 naar links-voor kijkt, en de neus hoort bij de snuit.
- Nog niet perfect: de maskerband tussen oog en neus is een vrij groot donker vlak. Een eventuele volgende stap is een rij schaduw (3) als overgang tussen brug en band, maar alleen als Jordi dat vraagt. De onderlaag (Linoone-gezicht 2× op de kop, oog op oog) is grof, want Linoone heeft een veel kleinere kop; ze diende alleen voor de plek van oog, brug en neus.

## Lessen
- **Eén oog bij een bestaande 3/4-kop:** vaak loopt het silhouet al schuin naar de neus. Dan volstaat het om het verre oog en de verre maskerlob om te zetten in een bruine brug en de nabije lob als band door te trekken. Aan de omtrek hoef je niets te doen (34 px in plaats van een herbouw).
- **Rijstrings met `.` = ongemoeid:** tel de startkolom na met een printout. Een verschoven string overschreef hier eerst de omlijning (open rand op x15/y26 en x12/y30), wat alleen een randcheck (gewijzigde pixels naast transparant) ving.
