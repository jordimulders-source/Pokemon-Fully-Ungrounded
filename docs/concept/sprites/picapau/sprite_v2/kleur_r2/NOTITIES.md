# Picapau sprite_v2 kleur r2: notities (maker, 5 nov)

Vanaf `kleur_r1/raster.txt`, alleen de vier opdrachtpunten. `teken.py` = de handwijzigingen als (rij, x, tekens) op r1 → `raster.txt`; `bouw.py` (palet = r1) → `picapau.png`, `normal.pal`; `controle.py` → `controle_uitvoer.txt`; `vel.py` → `vel.png` (8x: render | r1 | r2 | Taillow | Pikachu; onder 1x en 2x).

## Bevroren (diff met r1 = 0, met script)
kuiftoppen r3–8 (384 px), oog (16), wang (20), vleugel + schubben (544, per rij vanaf de eerste vleugelpixel), staart (380): **alle 0 px**. In totaal 88 px gewijzigd t.o.v. r1.

## Wat er veranderde
1. **Licht**: kop één ronde vlek op de bol (x24–29 r14–16); borst één licht op de bolling linksboven (r29–33), dat naar rechtsonder in de basis overloopt; de lichtvlek op de buik is weg. Buik/dij: basis links, brede schaduwsikkel langs de onderkant en rechts (r37–44, 7–14 px breed), het tapse dijlijntje blijft.
2. **Snavel**: punt 2 px verder (x13 r16), ±8 px lang van punt tot gezicht; bleke hoorn `h` in het midden (3 px aan de basis), bovenrand `g`, onderrand donkergrijs `G` (geen zwart), korte lijn `4` (x20 r19–21) waar hij in het gezicht zit. De onderrand volgt de render (schuin naar x19 r23), dus de basis is stevig.
3. **Voetjes**: tenen in de pootkleur `g`, onderkant `G`; zwart alleen aan de schaduwkant van het loopbeen, de buikrand tussen de poten en als klauwhaakjes (x24 r48, x33 r49, x38 r49). Verre poot rechts erachter in `G`/zwart.
4. **Achterste kuifpunten**: punt A (r12–14) 3 px aan de basis, gevuld; punt B (r16–19) aan de basis 3 px gemaakt (+1 px (38,16)), bovenrand goudbruin, taps naar de punt (41,18).

## Controle
- Lichte kleur op de buitenrand 0, losse pixels 0; kleine tintclusters alleen nog in de r5-schubben (textuur), de snavelpunt en (33,9) uit de r5-kuif.
- **Buiten het silhouet: 36 px**: kuiftoppen 6 (r5), snavel 6 ((13,16) (14,16) (14,17) (16,17) (18,18)), kuifpunten 4 ((40,12) (38,16) (41,18) (40,19)), buikboog 3 ((39–41,47), render-label Y), poten/tenen/klauwen 17 (r45–49). Leeg gelaten: (32,46) en (33,47), lucht tussen de poten.
- 852 px, 15 kleuren + transparant.

## Jordi's zes punten (eerlijk, r2)
1. **"volledig 2d"**: beter dan r1: geen losse lichtvlakken meer; borst-licht plus brede buiksikkel geven een ronde romp. Nog **half**: de romp leest ronder, maar minder dan de render (geen zachte overgang mogelijk met 3 tinten; de voorrand is het rechte bevroren silhouet).
2. **"geen drie kwart"**: ok: één oog, lange snavel schuin omhoog aan de voorkant, verre oog piept, verre poot achter.
3. **"perspectief"**: ok-ish: vleugel over het lijf, staart erachter, verre poot donker en rechts.
4. **"klauwen afgeknapt"**: beter: tenen steken uit met haakjes. Op 8x lezen de nabije tenen nog wat als een plankje (lange teen naar links + teen vooruit op één rij); op 1x twee kleine voetjes, klauwen net zichtbaar. **half**.
5. **"shading"**: beter: licht linksboven, één lichtvlek per volume, sikkels rechts/onder. ok-ish.
6. **"snavel weg"**: ok: op 1x een duidelijke bleke punt schuin omhoog met donkere onderkant.

## Zwakke punten (melden)
- Nabije poot op 8x: de tenen liggen vlak naast elkaar (plankje); "grijpen om iets heen" lukt pas als de tenen aan het eind krommen (1 px omlaag bij de punten).
- Romp: de voorrand blijft recht (bevroren silhouet), waardoor de borst minder bol oogt dan in de render.

## Lessen
- Wijzigingen als (rij, x, tekens) bovenop het vorige raster maken de diff van bevroren delen triviaal te bewijzen, en laten het vorige werk staan.
- Snavel: een dunne bleke strook leest als een naald; de onderrand moet de render volgen (schuin tot de kin), zodat de basis massa heeft.
