# Pitahaya-draak fase 2, sprite r5 (maker): de bek als vier delen

Op `pitahaya2_r4.png`. Script `maak_r5.py` (aanroep `python3 maak_r5.py`), vel `vel5.py`. Per pixel staan de wijzigingen met de modelmeting in `pitahaya2_r5_afwijkingen.txt`.
Meting: `natief.png` (pitch 5,076), 3×3-blok per spritepixel (X → nx 2+3X..4+3X, Y → ny 3(Y−13)..+2), klassen uit `groepen.py` (r1).
**Bewijs (asserts in het script):** de diff buiten de zone x 2–22, y 40–56 is **0**, het silhouet is gelijk (0 px) en er zijn 23 px gewijzigd t.o.v. r4, alle binnen x 9–17, y 42–48. Palet: 13 + 1 = **14 kleuren incl. transparant**. Nieuw is v (155,154,159), een donkergrijs dat in het model gemeten is: de pitrand in de wig, natief (36,93) en (40,94). Het grijs telt daarmee 3 tinten: v/w/W.

## Gen 3-studie (`studie_open_bek.png`, frame 1 op 8×; Carvanha geschrapt, die heeft een dichte bek)
- **Bovenlip en tanden:** de kaaklijn is 1 px zwart en loopt door. De tanden zijn 1–2 px wit, hangen direct onder de lijn en hebben zwart ernaast. Ze staan tegen het donkere binnenste (Croconaw, Gyarados, Salamence, Sharpedo).
- **Binnenkant:** de donkerste tint van de bek zit bovenin en achterin, onder de bovenkaak (Croconaw donkerrood, Gyarados bordeaux, Exploud donkerpaars rechtsboven). De tong of onderkaak is lichter en het lichtst vooraan links. Gehemelte en tong zijn gescheiden door een toonsprong van minstens 2 stappen, en bij Exploud ook door een donkere lijn waar de tong overlapt. Per vlak gebruiken ze 2–3 tinten.
- **Onderkaak:** een lipband van 1–2 px in de lipkleur, met een zwarte buitenlijn (Croconaw geel, Gyarados beige, Exploud lila).
- **Mondhoek:** de boven- en onderlijn komen samen in een donker punt of een korte donkere lijn.

## Per band gemeten
**1 Bovenlip met kaaklijn (contour, 4 px).** Het middenpad van de zwarte modellijn per spritekolom:
- X 3–11: ny 88–89,5 → Y 42;
- X 12–13: ny 90,5–91,5 → Y 43;
- X 14–16: ny 93,5 → Y 44;
- daarna loopt de lijn bij de mondhoek omhoog naar (17,43)–(18,43). Dat stond al zo in r4.

Wijzigingen: (11,42) r→K (blok 1 zwart, het pad op ny 89,5), (12,43) w→K (3 zwart), (13,43) r→K (2 zwart), (14,44) d→K (2 zwart + 6 donkerroze D).
De kaaklijn zakt nu vanaf de tweede tand schuin naar rechtsonder. Daarboven blijft het roze van de bovenlip staan: (14–16,43) r, zoals in het model.
Tanden en tandvlees (4,42/43) en (8,42/43) zijn ongewijzigd uit r4.

**2 Grijze wig (7 px).** Gemeten: dit is het vleesblok onder de kaaklijn en boven de verre lip, met 8–9/9 vlees: (10,43) (11,43) (10,44) (11,44) (12,44) (13,44) (11,45).
- Het model heeft hier hetzelfde grijs als de bovenkant van de tong (mediaan 187 tegen 194).
- **Afwijking naar Gen 3:** de wig is nu donkergrijs v, de schaduw onder de bovenkaak, zoals bij Croconaw en Gyarados. Zo is de wig te onderscheiden van de tong.
- Eén pit, op (11,44): de sterke modelcomponent 856. De pit op (10,43) (component 798) is niet gezet, omdat hij 8-naast (11,44) ligt.

**3 Verre lip (contour, 4 px gewijzigd).** Het middenpad van de roze modelband:
- nx 32 ny 100,5 → (10,46);
- nx 36 ny 99,5 → (11,46);
- nx 38–40 ny 98–97,5 → (12,45);
- nx 42 ny 96 → (13,45);
- nx 44 ny 95,5 → sluit aan op de kaaklijn (14,44).

Links is de band breder, want X 9–10, Y 45–47 is in het model roze. De toon is het gemiddelde van de roze modelpixels:
- (10,45) w→p (4 roze);
- (11,46) d→r en (12,45) d→r (5 roze; de r4-schaduwtint was de "donkere diagonaal");
- (13,45) w→r (4 roze).

(9,45) r, (10,46) r en (10,47) r stonden al goed. **Gemeten dikte:** het model heeft deze band ±3 natieve px dik, dus 1 spritepixel. Alleen links bij de voorste tand (X 9–10) is hij 2 px. Hij is niet dikker gemaakt dan het model.

**4 Onderkaak / tong (9 px).**
- Pitten van r4 die weg zijn: (11,47) en (13,46), allebei direct onder de verre lip. Ze worden vlees.
- **Afwijking naar Gen 3 (licht vooraan links, schaduw achterin):** (12,46), (13,46), (11,47), (12,47) en (13,47) zijn w→W. Het model is daar grijs (188–198). Het grijs w blijft achterin (X 14–16, Y 45–48), waar het model ook grijs is. Zo ligt het witte vlees direct tegen de roze verre lip.
- Mondhoek en binnenrand van de lipband: (17,44) p→r (9/9 roze, gemiddelde (161,71,96)), (17,46) p→r en (17,47) p→r. Dit is de donkere D-rand op nx 54 in het model, tussen het grijze vlees en de lichte lipband.
- Pit (10,48) W→s: de grootste modelpit (6 natieve px). Hij ligt in de hoek van de lipband, op de plek van het model.
- De pitten (9,51), (14,49), (12,50) en (15,47) blijven, dus de bek heeft in totaal 6 pitten. Geen twee pitten raken elkaar en er staat geen pit op een band.
- De lipband van de onderkaak (X 7–17, Y 48–55) is gecontroleerd tegen het model, per blok: de punt naar linksonder, P binnen, r en een donkere buitenlijn. Die stond in r4 al op het modelpad, dus daar is niets gewijzigd.

## Let op voor Claude
De opdracht beschreef de verre lip als een band "van ±2 spritepx" die het grijze bovenste vlees van het witte onderste vlees scheidt. Gemeten op het model:
- de band is 1 px, alleen links 2 px;
- hij scheidt de **kleine wig** van de **tong**. De tong is in het model bovenin ook grijs en gaat zonder lijn over in wit (ny 104–107).

Ik heb het model gevolgd. De scheiding komt van de Gen 3-opbouw: een donkere wig en een lichte tong vooraan.

## Zelf getoetst (`vel.png`: bek op 12× model | r5 | r4; sprite op 8× r5 | r4; 1× en 2× licht en donker)
- **12× en 8×:** vier delen zijn te lezen:
  - zwarte bovenlip die schuin zakt, met 2 witte tanden;
  - een donkergrijze wig met 1 pit;
  - een roze verre lip;
  - een witte tong met pitten in een roze lipband.
- **2×:** wig (donker) en tong (wit) zijn duidelijk gescheiden. De roze verre lip is dun, maar zichtbaar als roze tussen donker en wit.
- **1×:** de bek is een witte tong met een donkere bovenhoek. De verre lip valt op 1× weg in de toonsprong.
- **Zwak:** de verre lip is op 1× niet als band te zien, omdat hij 1 px is (modeldikte). De bovenkant van de grijze tong achterin (X 14–16) heeft maar 1 pit. Meer pitten raakten de band of elkaar.
