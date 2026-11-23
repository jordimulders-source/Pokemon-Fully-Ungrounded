# Pinsir-evolutie v2, frontsprite r5 (23 nov)

Jordi bij r4 (letterlijk): "r4 is al wat netter maaar het hoofd is nog te recht, niet de juiste vorm, de arm is niet goed te zien, de benen zijn niet goed"; aanvulling: "is echt nog lang niet klaar", "maar dat is veel wederom belijning, kleur, schadduw".

Bouwen vanuit `docs/concept/sprites/pinsir_evo/`:
`python3 sprite_v2_r5/meet.py && python3 sprite_v2_r5/bouw.py && python3 sprite_v2_r5/vellen.py`

- Start = `sprite_v2_r4/pinsir_evo_v2_r4_B.png`, pixelgelijk. Het script stopt met een fout als er buiten de opgegeven zones iets verandert.
- Palet r4 ongewijzigd, 15 kleuren, index 0 transparant. Er is geen zwarte kleur of zwarte lijn bij gekomen, behalve waar het model zwart heeft (rechter- en onderrand van de onderarm).
- 411 px gewijzigd, waarvan hoofd 123, nabije arm 108 + 8 slagschaduw, verre arm 6, nabije been 84, verre been 63 en buiklijnen 19 (buiten de opdracht, zie 4).
- Silhouet: 2 px erbij, (32,21) en (34,20), en 2 px eraf, (23,12) en (24,12). Alle vier gaan naar het modelmasker.

## Meten (geen tekenwerk op gevoel)
- `meet.py` meet in het origineel (1024 px) per spritepixel twee dingen. DF = het deel van de pixel dat zwarte lijn is (L < 50). ML = de mediaan van de helderheid zonder de lijn. De positie gaat zoals in r1–r4: natieve cel × 64/91, OY 9. Gecontroleerd op de ogen: het linkeroogzwaartepunt valt in (14,22).
- `toon.py x0 x1 y0 y1` drukt model en sprite per rij naast elkaar af. Elke rij in `bouw.py` is daarvan overgenomen.
- Tinten: model-L onder 90 → 3, 90–115 → 4, 115–141 → 5, daarboven 14. Dat zijn dezelfde drempels als in r3.
- `kijk.py` legt het model op het spriteraster voor de vellen.

## 1. Hoofd: "te recht, niet de juiste vorm"
Per rij, r4 tegen het model:
- **y13–14, bovenrand tussen de stekels.**
  - r4 was hier licht (5/14), dus een vlak verlicht blok.
  - In het model is deze rand donkerder (83–108), met lichte stekelflanken op x19 en x27.
  - Nu: 4, met 5 op de flanken. Het dal tussen de middelste en de rechterstekel ligt in het model op y13. In r4 lag het op y12: (23,12) en (24,12) zijn nu transparant en (21–24,13) zwart. Daardoor leest het schild gewelfd: een donkere bovenrand, een lichte middenband en een donkere onderkant.
- **y15–19, middenband.**
  - Het model is licht (130–155), met een hooglicht op x14–18, y15–17.
  - r4 had een schuine hooglichtstreep over de hele breedte, en dat is banding. Nu is het hooglicht één vlek van 11 px op die plek.
- **Rechterhelft.**
  - In het model ligt de rechterhelft in de schaduw achter een schuine grens: (27,16) → (25,18) → (22,19).
  - r4 was licht tot x30 en had een lichte horizontale streep op y18, x26–30. Die streep staat niet in het model.
  - Nu: 4 achter de schuine grens, met een vouw 2 op (28–29,16) en (22,19), en een lichte randstreep langs de rechteronderrand op de modelplek: (34,18), (32–33,19) en (26–28,20).
- **y19–20, de donkere band.**
  - In r4 liep hier een donkere band (4) van x9 tot x33. Dat was het "rechte" bij uitstek.
  - In het model is de linkerhelft licht tot aan de onderrand (129–140). Nu: 5, en het losse zwarte pixel (12,19) is weg.
- **Onderrand van het schild.**
  - r4 had rechts een horizontale lijn op y21 (x24–31).
  - Het model loopt schuin omhoog naar de punt: (24–28,22) → (29–32,21) → (33–34,20). Zo staat het er nu. Eronder ligt de nek in 4, met schaduw 3 op (30,22).
- **Voorhoofd en wenkbrauwen.**
  - Het model heeft een lichte wig tussen boze V-wenkbrauwen: (14–19,20) en (15–18,21), met hooglicht op (16–17,21).
  - r4 had hier een dambord 4/5/4/5. Nu: 5 met een hooglicht van 2 px.
  - De zwarte balk onder het voorhoofd: in het model is (16–18,22) alleen een deellijn (20–30 %). Die drie pixels zijn nu lijnbruin 2 in plaats van zwart. Zwart blijft op (14–15,22) en (19–21,22).

Niet uit het model:
- Ogen, mond, tanden, kaken en kin zijn r4, pixelgelijk. Het gezicht is goedgekeurd door de keurder en Jordi noemde het niet. De ogen staan wel ±1 rij hoger dan in het model.
- Rij 14 is vereenvoudigd tot 4 met twee flankpixels 5. Het model is hier onrustig: 3, 14, 4, 14 door elkaar.

## 2. Armen: "de arm is niet goed te zien"
**Nabije arm.** Het model heeft koepel → bovenarm → onderarm → hand:
- **Koepel.** In het model ligt die op x33–37 en y30–35. r4 had hem 1 px te ver links, met lijnen die niet op de modelplek lagen. Nu:
  - een rand van lijnbruin 2: links x32, bovenhoeken (32,30) en (37,30), rechts (37,31) → (38,32) → (39,33–34) → (40,35);
  - hooglicht 14 linksboven, vlak 5 en een schaduwsikkel 4/3 rechtsonder;
  - onderrand (33–37,36) in 2.
- **Rechterrand van de arm.**
  - In het model loopt die van (41,36) → (42,37) → (43,38–40) → (42,41–42) → (41,43).
  - r4 had de lijn 2–3 px verder rechts. Dat is de rugnaad (44,36) → (45,38), en die blijft. Daardoor viel de arm samen met het lijf.
  - Nu staat de rand op de modelplek in zwart: dat is de schaduwkant en het model is daar zwart.
- **Onderrand.** (37–41,44) en (40–41,45) zwart, zoals in het model.
- **Onderarm.**
  - Het model heeft een lichte rug (121–139) diagonaal van de elleboog (41,38) naar de pols (35,41).
  - r4 had het licht juist links, op x33–37, y37–39. Daar is het model donker (±90).
  - Nu: een rug van 14/5 met schaduw 3 rechtsonder. Een lijn 2 scheidt hem van de bovenarm: (38,37–38), (37,39), (36,40).
- **Bovenarm.**
  - Het model meet hier ±90, op de grens van 3 en 4. Gekozen: 4 met een lichte linkerrand 5 (32,37–38) en schaduw 3 tegen de onderarmlijn.
  - Dat wijkt af van het model: met volledig 3 werd het een donker gat. Kleur mag afwijken.
- **Slagschaduw.** Het lijf rechts van en onder de arm, (43–45, 40–42) en (44–45,40), is van 4/5 naar 3 gegaan. Het model meet daar 82–89. Daardoor komt de arm los van het lijf.
- **Hand.** Blijft r4: dat was het klauwrecept van de keurder en het ligt al op de modelplek. Alleen (38,45) is nu 6, een kleine roompunt uit het model (160).
- **Buikrand links van de arm.** Blijft de doorlopende lijn 2 van r4. Tegen room plus de bovenarm leest die als eigen donkere rand.

**Verre arm.** Vijf pixels:
- (10,42) en (12,42) worden 2, de scheiding hand/onderarm uit het model;
- de lichte bovenkant van de onderarm wordt (13–14,42) en (14,43) in 5;
- de schaduwkant (15–17,42), (13–14,44) en (12,45) wordt 3/4.

## 3. Benen: "de benen zijn niet goed"
**Nabije been.** In r4 was de dij donker (3/4, ±100). Het model is hier licht (±125).
- **Dij:** nu 5, met hooglicht 14 op (34,47) en (34,49).
- **Heuplijn:** (37–41,48) → (42–43,49) → (44,50), uit het model. Daarboven ligt een donkere heupstrook 4/3.
- **Knie-ring zoals het model:**
  - links open, want lichte dij en knieschijf lopen in elkaar over;
  - bovenrechts (40,51) en (41–42,52), rechts (43,53–54) in 3, rechtsonder (42,55), onder (38–41,56) en links (37,55);
  - de knieschijf heeft hooglicht 14 op (36–37,52) en (37,53), en schaduw 4/3 rechtsonder.
- **Rechterrand van het been** (44,50–54) en (45,55) in 2, uit het model.
- **Scheen:**
  - lichtkant 14/5 op x36–38, midden 4, schaduw 3 op x43–45;
  - r4 had 5 alleen op x36–37 en verder effen 4.
- **Voet:**
  - teenlijn (37–38,59);
  - klauw links (37–38,60–62) in 7/6, met (36,61) 6; klauw rechts (44–45,61–62);
  - de klauwen staan nu op de modelplek. In r4 stond de rechterklauw 1 rij hoger, op (44–45,60).

**Verre been.** Het hele been is een stap donkerder dan het nabije. Gemeten: dij 98 en scheen 87, tegen 119 en 103 bij het nabije been. Het model heeft 107 en 95.
- **Knieschijf** x15–17, y51–53 (5 → 4 → 3), ring (16–17,50) en (18,51–53) in 2, onderkant (17–18,54) en (16–17,55) in 2. In het model zijn deze lijnen een deellijn of zwart.
- **Buik/dij-lijn:** (21,48) → (22,49–50) → (23,51), uit het model. r4 had hier een zachte overgang 3 → 6 zonder lijn. (22,48) wordt buik 6.
- **Dij:** licht 5 bovenaan (18–19,47) en (17–18,48), schaduw 3 onder de buik, x19–23 y49–53.
- **Scheen:** randlicht 5 links (16,56), midden 4, schaduw 3 rechts. r4 had een effen 4-blok met een donkere band (3) over y58: dat was banding.
- **Voet:**
  - teenlijnen (16,58) en (19,58);
  - klauw 1 = (14–16,59), met (16,59) 6 erbij uit het model (158);
  - klauw 2 = (18,59) en (17–19,60). In r4 stond die op (17–18,59) en (17,60).

Niet uit het model (benen):
- Het licht/schaduwverloop binnen dij, scheen en knieschijf. Het model is daar vrijwel effen (±95–125). Het volume is toegevoegd naar Gen 3: randlicht links, sikkel rechts.
- De stap donkerder voor het verre been is een opdracht, geen modelmeting.

## 4. Buiten de opdracht (met dezelfde blik over de hele sprite)
- **Buiklijnen uit het model** (19 px, in 14):
  - horizontaal op y41, x21–26 → (27–28,40);
  - verticaal op x23, y42–46;
  - horizontaal op y47, x22–27.
  - Het model heeft deze plaatlijnen (L 131–143 op room). In r2–r4 waren ze weg, waardoor de buik een effen vlek was naast Tyranitar.
- **Opschonen:** 28 losse 1-px-vlekjes in 3 of 4 binnen de gewijzigde zones nemen de meest voorkomende buurtint (lijst `OPGESCHOOND` in de uitvoer van `bouw.py`). Lichtranden (5/14) blijven bewust klein.

## Zelf gezien / zwakke punten (onder Tyranitar/Aggron/Pinsir, niet gerepareerd)
- **Rug B is banding.** Onder elke naad ligt een lichte rij en erboven een donkere rij. Zo ontstaan evenwijdige strepen langs de rugrand, en dat is op 2× de drukste plek van de sprite. Reparatie volgens het model: per rugplaat één lichte kant (linksboven) en één schaduwkant, niet per naad. Dat is een eigen ronde.
- **Nabije arm op 1×.** De arm leest nu als koepel + onderarm + hand, maar minder hard dan in het model. Het lijf eromheen (rug) is net zo druk als de arm.
- **Kleur.** De hele sprite blijft donkerder en roder dan het model (palet r4, volgens de opdracht). Het model is grijzer en lichter, met meer contrast tussen lijn en vlak.
- **Ogen.** Ze staan ±1 rij hoger dan in het model. Niet aangeraakt: het gezicht is goedgekeurd.
- **Geen keurder gebruikt.**

## Bestanden
- `pinsir_evo_v2_r5.png`: de sprite. Geïndexeerd, index 0 transparant, 15 kleuren.
- `bouw.py`: de opbouw. Elke rij heeft een commentaar met de modelmeting.
- `meet.py`, `toon.py`, `kijk.py` en `kaal.py`: meetgereedschap. `kaal.py` maakt een kale modelreductie in het r4-palet, alleen als meetlaag. `DF.npy`, `ML.npy`, `RG.npy` en `dekking.npy` zijn de metingen.
- `onderdelen.png`: hoofd op 16×, nabije en verre arm op 12×, benen op 12×. Telkens r5 | r4 | model op het spriteraster.
- `vel.png`: r5 | r4 | model op 6×, daaronder 1× en 2× naast Tyranitar, Aggron en Pinsir (Gen 3), op wit en op donker.
