# Keuring welp p3, 15 nov

Onafhankelijke keurder, eerst blind: 8× naast r11 en het model, lijf op 12–16× met raster, 1× naast Seviper, Growlithe, Vulpix en de volwassen steenjaguar. Daarna p2/keuring.md nagelopen.
Palet = r11: 1 zwart, 2 donkerste bruin (lijn), 3/4/5 bruin donker/mid/licht, 6/7/8 lila donker/mid/licht, 9 crème-schaduw, 11 crème.

## Oordeel: **FAIL** (heel dichtbij; 7 pixels in de schouderspiraal)

### Gemeten
- Alpha-diff tegen r11 = 0; diff 196 px, alleen x 24–48, y 32–55 (lijfzone). Kop, oog, poten, silhouet identiek aan r11. Lijf niet bol, geen dikke belijning.
- Patroonpixels (6/7/8/9/11) 237 (r11: 175): meer bedekt, schouderspiraal ±12×13 px.

### Wat goed is
- Leest als **ingekleurd patroon**, niet meer als lijntjes: crème band met lila vulling en een bruine (3) groef. Precies de richting van Jordi's "het is echt inkleuren".
- De crème ring volgt de facetten (9 waar het lijf in schaduw ligt, linksboven onder de kop en rechts; 11 op het lichte deel): het 3D-idee blijft. Borstfacet (5, x 22–24, y 40–42) en heupfacet (5, y 47–48) staan er nog.
- **Heup:** crème spiraal waarvan het hart (44,52) via (44,53) aan de onderste winding vastzit, dus een echte spiraal, geen schietschijf; lila boog rechts/onder en lila streepje linksboven zoals het model.
- **Rugkrul** (x 38–41, y 38–42): de rugband loopt rechts omlaag, onderlangs en naar binnen; leest als kleine (hoekige, Chavín-achtige) krul aan het eind van de rugstreep.

### p2 MOET-punten
1. Haak naar rechts, krul naar links en omhoog naar binnen: **opgelost** exact zoals voorgeschreven ((33,49)…(29,50), tip (30,50)=9, vast aan de ring, oude steel weg). Geen losse "J" meer.
2. Ring onderaan open met lila buitenwinding: **opgelost** ((28–31,47)=7, (29–31,46) groef 3).
3. (26,43)=11: **opgelost**.
- MAG-punten (schijfvolume 7, heup taps, rugkrul groter) zijn ook uitgevoerd.

### MOET
1. **Losse stip in het hart van de schouderspiraal = oog/doelwit.** (30,43) en (31,43) zijn index 4, rondom ingesloten door lila; de bruine groef is een C die nergens naar het midden loopt. Op 1× leest de schouder daardoor als een bleek ei/oog met pupil, niet als de meerwindige spiraal van het model.
   - (29,43) = **3**, (30,43) = **3** (groef loopt van (29,42) naar binnen en eindigt in het hart), (31,43) = **8** (lila). Lila blijft één doorlopende winding (via (28,43)/(28,44) naar buiten).
2. **Schouderring heeft rechte zijkanten (afgeronde rechthoek, "sticker").** Rechts staat x 36 (9) zeven rijen recht (y 39–45), links x 25 ook zeven rijen (y 39–45). Het model is rond.
   - (25,39), (25,45), (36,39), (36,45) terug naar basisbruin **3** (= `p1/basis.npy`). Rechte stukken worden dan 5 px met 1-stappen op de hoeken; de ring blijft gesloten ((26,39)=9, (26,45)=11, (35,39)=11, (35,45)=11 staan er al).

Proef in de scratchpad met precies deze 7 pixels: de schouder leest daarna op 8× én 1× als spiraal ("@" met staartkrul) en ronder; niets anders verandert. Daarna diff tegen p3 = 7 px tonen.

### MAG
- Rugband (x 33–37, y 33–37): een 1 px diagonale rij 7 tussen 4 en de 8-band is licht banding (parallel aan de rand). Mag hier en daar 8 of 4 worden zodat de 7 geen doorlopende lijn is.
- Staartkrul (29–31, 50–52) is klein en leest op 12× een tikje als vinkje; in het model is het eind een iets ronder krulletje. Alleen als het zonder de beenlijn (x 34, index 2) te raken kan: (31,50) = 9.
- Heup rechts: (47,50)–(47,52) = 8 is licht op de schaduwkant; mag 7 worden (dan (48,51)/(48,52) = 6) voor licht linksboven.

### Hoofdvraag eigenaar
Zou Jordi dit mooi vinden? Bijna. Het is eindelijk een ingekleurd patroon dat het lijf bedekt, het lijf en het 3D-gevoel zijn intact, en de heup, rugkrul en staartkrul kloppen met het model. Wat hem nu nog stoort, verwacht ik: de grote schouder springt op 1× als een **bleek ei met een stip** naar voren (oog/doelwit), terwijl het model daar een duidelijke spiraal heeft. Met de 7 pixels hierboven zou ik hem wél trots laten zien; daarna kort hercontroleren (geen volledige ronde nodig als de diff precies deze 7 px is).
