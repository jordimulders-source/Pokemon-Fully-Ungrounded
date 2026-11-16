# Strenge Gen 3-keuring r24 → r25 (16 nov, verse eindkeurder)

Gekeurd: `af/spooktrein.png` (= `sprite_r24/sprite.png`). Model: `model/model.webp` en `model/natief.png`. Gelezen: SPRITE_KERN, FAKEMON_CHECKLIST, SPRITING, de DFC Spriting Guide (txt) en GEMINI.md vanaf Octillery. Vergeleken met Forretress, Skarmory, Steelix, Magcargo, Claydol, Gengar, Haunter en Koffing (bovenste 64×64); als extra maatstaf voor de zwartmeting ook Metang, Aggron, Golem en Dusclops.
Vel: `keuring_vel.png`. Bovenaan op 8×: r25 | r24 | model. Daaronder op 2× en op 1× (licht en donker): beide naast de acht soorten. Onderaan op 16×: de drie reparatiezones (r25 boven, r24 onder).
Coördinaten zijn (x,y). Paletindexen: 1 zwart, 7 plaatlicht, 8 roest, 9 roestdonker, 10 plaatgrijs, 11 donkergrijs, 12 donkerst grijs, 14 lichtbruin; 2–6 en 13 zijn groen/wit (bevroren).

## Oordeel
- **r24: FAIL.** Drie harde regels zijn gemeten geschonden: een contraststap van 14, een dambord van twee bijna gelijke tinten en zwarte klonten met zwart en donker om en om. Zie MOET.
- **r25: PASS.** De reparaties zijn 8 px plus één paletwaarde. Binnen dit mandaat is geen harde fout meer over. Er blijven wel drie restpunten die niet met kleine reparaties op te lossen zijn (zie onderaan); Jordi moet die kennen.

## 5. Hoofdvraag (eerst bekeken, 1× en 2×)
- **r25 tegenover r24: iets beter, nergens slechter.**
  - Op de kop leest de lichte plaat linksboven nu echt als hooglicht, dus er is meer bol.
  - De schoorsteenlip is rustig in plaats van korrelig.
  - De zwarte balk die in r24 in de wolken staken (achter de wagen) is nu een grijze as.
  - Op 1× is het verschil klein.
- **Naast de echte soorten:** op 1× leest hij meteen, ook op donker. Je ziet een pompoenkop met grijns, een schoorsteengeest, wielen en een rookspoor. Op 2× is hij duidelijk drukker dan Forretress, Steelix en Claydol, zij hebben grote vlakke metaalvlakken. Hij zit dichter bij de schelp van Magcargo. Die drukte komt uit het model (veel kleine platen en kieren) en mag niet weg (eis 1).
- **Het zwakste punt is de waardescheiding tussen de materialen.** Zie R1.

## Per onderdeel

### Kop (x2–28, y19–44)
1. **Schaduw:**
   - Het licht valt linksboven. Van licht naar donker: plaatlicht 7 linksboven, lichtbruin 14 op het voorhoofd en de neus, roest 8 in het midden, en 9/12 rechts als sikkel langs de rand naar het lijf.
   - Pillow shading: nee, want de linker rand is licht met een gekleurde selout.
   - Banding: nee.
   - De band van roest 8 boven de grijns (y37–38, x4–19) is effen over 16 px. Dat is een vlak vlak, maar het staat zo in het model (de wangplaat). Geen blokkade.
2. **Kleuren:**
   - Roest 14→8→9: lum 142/114/77, stappen 28 en 37, goed.
   - Plaat 7→10: in r24 was dat 159/145, een stap van **14 → FOUT**. In r25 is 7 lichter (lum 182), de stap is nu 37.
   - Hue-shift: de roest schuift naar rood in de schaduw (24°→21°→16°), de grijzen zijn licht warm. Dat is Gen 3-achtig.
   - Er zijn nog losse 1-px-tintjes: 11 op (16,25), 10 op (8,35) en 9 op (22,37). Het zijn er weinig, ze vallen op 2× niet op. Dat is een MAG.
3. **Lijnen:**
   - De vrije buitenrand ligt aan de lichtkant (linksboven) en heeft een gekleurde selout 9: 7 % zwart. Dat is in orde: Haunter en Koffing meten 3–7 %.
   - De curve van de linkerbovenkant loopt 3-1-1-1-1, dan 2-2-4. Dat is geleidelijk, zonder spijkers.
   - **(28–30,33–34) was een zwart blok van 3×2**, op de plek waar de kopomlijning en de omlijning van de kier samenkomen → FOUT (klont). In r25 is (29,33–34) plaattint 12, zodat er twee lijnen van 1 px zijn die bij y35 samenkomen.
   - De wenkbrauwen (5–6,30–31) en (19–20,30–31) zijn blokjes zwart van 2×2. Dat zijn de dikke boze brauwen van het model, en het gezicht is daarom niet aangeraakt (MAG).
   - De linkerrand op y35–39 (x2) is donkergroen 6 naast roest 8. Dat is een omlijning in de verkeerde kleurgroep. Het is groen en dus bevroren: zie R3.

### Koeienvanger (x2–26, y45–58), door Jordi goedgekeurde vorm: niet aangeraakt
- Zwart aan de lichtkant 29 %, aan de schaduwkant 60 %. Gen 3 meet 7–53 % en 52–100 %, dus dit is goed.
- De klonten (13–14,49–50) en (12–14,52–53) zijn de modelspleet bij de middentand en Jordi's lijnen. Laten.
- Door de lichtere 7 lichten de plaatranden langs Jordi's V iets meer op. Er verandert geen pixel. Diff in de zone x0–30/y44–60 is 0 (assert).

### Lijf en platen (x23–46, y17–44)
- Het licht klopt: het lijf achter de kop en de schoorsteen ligt in slagschaduw (12/9), en de middelste lichte plaat (x36–39, y35–37) staat in het licht.
- **De zwarte as (46–53,39–41) was een blok van 8×2, met 11 op (50,40) tussen het zwart → FOUT** (een klont, en zwart en donker om en om). Het model heeft hier een donkergrijze as. In r25 is (47–50,40) nu 12, binnen een lijn van 1 px.
- (33–35,43–44) is zwart 2×2 aan de schaduwkant onder de plaat. Echte metaalsoorten hebben er meer: Forretress 73, Steelix 50, Golem 16. Dat is een MAG.

### Schoorsteen (x12–25, y14–20)
- **Op (14–16,15–18) stond een dambord van 7 en 10, twee tinten die maar 14 lum verschilden.** Dat is ruis zonder functie → FOUT. In r25 zijn (15,16) en (14,17) nu 7: een lichte lip linksboven met 10 eronder.
- De omlijning is 40 % zwart. De selout 12 zit linksboven (de lichtkant), zwart zit rechts. Goed.

### Kleine geest, wolken en geestwielen (groen, bevroren sinds r9)
- Ze hebben geen zwarte omlijning: wolken 2–3 % zwart, wielen 0–3 %, geest 0 %. Dat past bij Gen 3-gas (Koffing-gas en het vuur van Magcargo hebben een gekleurde omlijning) en Jordi koos het zo.
- Ze zijn niet aangeraakt: groen-diff 0 (assert).
- Zie R2 en R3.

## 4. Dragonfly Cave / FAKEMON_CHECKLIST
- **DFC, nooit vergroot/verkleind in het eindbeeld:** ja.
- **DFC, ≤16 kleuren:** 14 plus transparant.
- **DFC, 3 tinten per groep plus lijn:**
  - Roest: 3.
  - Metaal: 4 (7/10/11/12). Dat mag, zoals Metang met een extra schaduwtint.
  - Groen: twee ladders met een gedeelde schaduw. De verzadigde ladder is 2→3→6 met stappen 46 en 46, de bleke is 4→5→6 met stappen 31 en 45.
- **DFC, geen buitenste anti-aliasing:** er staan 0 lichte metaalpixels op de buitenrand.
- **DFC, licht linksboven:** ja.
- **DFC, de omlijning 1 px breed:** na r25 zijn de klonten alleen nog in model- en Jordi-zones of in de brauwen.
- **DFC, elke lijn scheidt vlakken (rots/staal):** ja.
- **A1 silhouet:** leest als trein met geest. **A2 het kenmerk breekt de omtrek:** de schoorsteengeest en de rook doen dat. **A3 diagonaal:** de kop staat linksonder en de rook loopt naar rechtsboven. **A4 soliditeit** is 0,83, iets boven de richtlijn, en dat komt door de rookmassa (model). **A5 symmetrie:** 0,74. **A6:** de rechte koeienvangerrand is Jordi's keuze.
- **B1 3/4:** ja. **B3 verre oog:** het linkeroog (x4–9) is kleiner en zit tegen de omtrek, goed. **B7 gezicht compleet:** ja.
- **D1 oppervlak:** 2515 px valt binnen fase 3 (1700–2600).
- **D2 kophoogte:** ±40 %, boven de richtlijn van 20–30 %. Dat volgt uit het model (eis 1 gaat voor).
- **E3 donker:** 0,11, binnen de band.

## MOET (r24) → toegepast in r25 (`af/streng_fix.py`)
| # | Pixels | Oud → nieuw | Reden |
|---|---|---|---|
| M1 | palet 7 | (178,153,138) → (204,175,158) | contraststap 7/10 was 14 lum, nu 37 (tint en verzadiging gelijk) |
| M2 | (15,16), (14,17) | 10 → 7 | dambord 7/10 op de schoorsteenlip |
| M3 | (47,40), (48,40), (49,40) | 1 → 12 | zwarte klont in de as |
| M3 | (50,40) | 11 → 12 | donker tussen zwart in |
| M4 | (29,33), (29,34) | 1 → 12 | zwart blok bij de aansluiting van kop en kier |

Asserts: groen ongewijzigd, silhouet gelijk, koeienvanger-zone diff 0, buiten de lijst diff 0, geen nieuwe index.
Ik heb ook een variant geprobeerd met een donkerder 12 (lum 52) voor R1. Die maakte het lijf zwaar en bijna zwart, dus die heb ik verworpen.

## Restpunten (geen blokkade binnen dit mandaat; Jordi moet ze kennen)
- **R1 waardescheiding metaal.** Op 20 % van de tintgrenzen in het metaal is het verschil < 20 lum (r24: 30 %). Bij Gen 3 is dat 0–9 % (Magcargo 8 %, Forretress 9 %, Steelix 0 %).
  - Het grootste deel komt van 9 naast 12 (lum 77 tegen 69, 44 grenzen) en van 10 naast 14 (145 tegen 142, 13 grenzen).
  - Ze verschillen wel in tint (bruin tegen grijs), maar zijn even donker. Daardoor oogt het lijf op 2× "modderig".
  - Oplossen vraagt een kleurronde, geen pixelreparatie.
- **R2 groen (apart gemeld, niet gewijzigd).**
  - Groen 3 en 5 zijn even licht (148 en 147) en raken elkaar 23 keer. Waar wiel en wolk samenkomen, smelten ze daardoor samen.
  - Groen 6 naast roest 8 en grijs 11 (102 tegen 114 en 99) zit op 68 grenzen.
  - Het is geen harde fout, wel de grootste bron van de modderigheid.
- **R3 groen als omlijning van de bruine kop** (2,35–39). Dat is een omlijning in een andere kleurgroep. Het groen is bevroren en het staat zo in het model, dus het is niet gewijzigd.
