# Keuring olinguito ronde 15 (onafhankelijk, 23 okt)

Onafhankelijke keuring van `anim_front.png` (2 frames, 64×64) en `normal.pal`, naast `SPRITING.md` (§0 en de olinguito-secties), `FAKEMON_DESIGN.md`, de *Spriting Guide* (Outlining, Shading, Shine, Splices), `ontwerp/olinguito/ONTWERP.md` + `concept_B.png` en de olinguito-punten in `FEEDBACK.md`. Opdracht: benoemen wat Jordi "niet kan aanwijzen".

Vellen (in `keuring/`):
- `vel1_1x.png`: 1× op licht en donker, frame 1 en 2, naast 20 echte sprites (Poochyena, Mightyena, Zigzagoon, Linoone, Sentret, Furret, Sneasel, Meowth, Skitty, Zangoose, Absol, Seviper, Teddiursa, Aipom, Ursaring, Treecko, Torchic, Mudkip, Cyndaquil, Totodile).
- `vel2_3x.png`: hetzelfde op 3×.
- `vel3_probleemplekken.png`: uitsneden op 8–14× met rode kaders (kop, ogen, staart, achterpoten, klauwen) naast de Gen 3-oplossing (vel-nummer 1–5 = punt 2, 3, 4, 5 en 7 hieronder).
- `vel4_paletvoorstel.png`: alleen het palet één stap lichter (index 3/4/5), naast Sentret en Ursaring, 3× en 1×. Geen pixel veranderd; ter illustratie van punt 1.

Coördinaten: (x, y) in frame 1, y = 0 bovenaan. Indexen volgens `normal.pal`.

## Eindoordeel: **technisch schoon, maar nog geen Gen 3-Pokémon; vier aanwijsbare oorzaken**
De techniek klopt: geen open randen (beide frames nagemeten), geen anti-aliasing buiten, 14 kleuren, licht van linksboven, de romp en de pootstand van ronde 15 zijn natuurlijk. Wat Jordi voelt maar niet kan aanwijzen, zit in vier dingen. Geen ervan is een pixelfout. Het zijn **waarde- en vormkeuzes** waarin hij afwijkt van élke referentie op het vel:
1. **Hij is één toonstap te donker over de hele linie.** De basistint is de schaduwtint van Sentret/Ursaring, de meest gebruikte kleur is de schaduw, en de omlijning aan de lichte kant is bijna zwart. Op 1× is hij de donkerste en vlakste sprite van de 21 (vel1). Het masker valt daardoor weg in de kop.
2. **De kop is een doos:** een vlakke bovenkant, een verticale achterkant, een rechte kin en oortjes van 3 px.
3. **Het gezicht bestaat uit horizontale banden** (wenkbrauwen / zwarte balk / crème snuit) met **rechthoekige ogen in een zwarte lijst**, de felste kleur bovenaan. Dat leest als een skibril of vizier (Jordi zei in ronde 2 al "masker als skibril"; de vorm is veranderd, de banden zijn gebleven).
4. **De staart is een buis**, even breed van voet tot punt, met een haakje van 3 px dat op 1× niet leest.

Punt 1 kost bijna niets (palet, vel4). Punt 2–4 zijn elk één lichaamsdeel opnieuw tekenen, terwijl romp, poten, armen en pose blijven staan.

## Meting naast Gen 3 (frame 1)

| | oppervlak | gem. luma | aandeel licht (luma > 150) | rand bijna-zwart (luma < 45) | binnen bijna-zwart | meest gebruikte vulkleur (luma) |
|---|---|---|---|---|---|---|
| **olinguito r15** | **1049** | **64** | **0,08** | **0,90** | **0,21** | **schaduw (68,44,38) = 51** |
| Ursaring (donkerste bruine Gen 3) | 2258 | 96 | 0,12 | 0,56 | 0,03 | basis (144,80,32) = 94 |
| Sentret | 982 | 106 | 0,15 | 0,77 | 0,05 | basis (189,131,90) = 144 |
| Zigzagoon (masker) | 1127 | 118 | 0,44 | 0,50 | 0,14 | basis (148,123,106) = 129 |
| Linoone | 1089 | 133 | 0,50 | 0,58 | 0,05 | |
| Teddiursa | 756 | 127 | 0,46 | 0,46 | 0,08 | |
| Poochyena (Dark) | 989 | 105 | 0,46 | 0,81 | 0,06 | basis (144,152,160) = 150 |
| Mightyena (Dark, zwarte vacht) | 1647 | 74 | 0,14 | 0,86 | 0,40 | |
| Sneasel (Dark) | 976 | 88 | 0,09 | 0,41 | 0,06 | basis (56,144,168) = 120 |
| Fase 1-starters Gen 2–3 (6) | 602–903, gem. 798 | 111–168 | 0,22–0,64 | 0,24–0,58 | ≤ 0,11 | |

Gebruik per index: schaduw 3 = 283 px, basis 4 = 220, hooglicht 5 = 60 (6%). R/S-stijl doet het omgekeerde: veel basis en hooglicht (SPRITING §5).

## Puntenlijst

### Nodig

**1. Palet één stap te donker; omlijning aan de lichte kant bijna zwart**
- *Wat:* de bruine ramp is 136 / 98 / 68 / 44 (luma 104 / 73 / 51 / 33). De basis (98,64,50) is precies de schaduw van Sentret (98,65,49) en Ursaring (96,64,40). Index 2 (44,28,28), luma 33, is tegelijk masker, omlijningsbasis en naadkleur. Daardoor zijn de 62 randpixels aan de lichte kant (kruin y 22–25, rug (39–47, 32–33), linkerrand van de staart (49–56, 20–33)) feitelijk zwart: van de 115 randpixels die naar linksboven wijzen is er geen enkele lichter dan luma 33. Het masker (index 2) valt weg tegen de kop in schaduw (index 3), zodat het hele hoofd één donkere vlek met twee gouden gleuven wordt.
- *Regel:* R/S gebruikt veel hooglicht, te weinig maakt een sprite te donker (§5); omlijning per kleurgroep met de omlijningsbasis of schaduwtint aan de belichte kant (§8, Outline Shading).
- *Goed bij:* **Ursaring** leest in de game als "donkerbruin" met een basis van luma 94 en een verzadiging van 0,78. **Zigzagoon** heeft een masker dat 1–2 stappen lichter is dan de zwarte oogrand, zodat het oog in het masker leesbaar blijft.
- *Oplossing:* (a) een paletwissel zonder pixelwerk: 5 → (188,132,88), 4 → (144,92,56), 3 → (100,66,50); 2 en 1 blijven (vel4: masker en ogen springen er meteen uit en hij blijft donkerbruin). (b) Daarna aan de lichte kant randpixels van index 2 naar 3 (de nieuwe 100,66,50): oortoppen en kruin (16–32, 22–24), rugtop (39–47, 32–33) en linkerrand van de staart (49–56, 20–31). Index 2 blijft alleen voor masker en schaduwkant. Een vrije paletplek vind je bij punt 7 (klauwen).

**2. Kop is een doos**
- *Wat:* de bovenkant ligt op y 24 vlak van x 17 tot 37; de oren steken maar 2 rijen uit (ver (16–20, 22–23), nabij (29–33, 22–23)). De achterkant van de schedel is verticaal: x = 37, 37, 37, 37, 38, 37, 38, 39, 39 voor y 24–32 (recht én besluiteloos, §3). De kin is een rechte zwarte lijn op y 40, x 23–32 (10 px), met y 39 x 20–22 en 32–33 als harde hoeken. Op 1× is het silhouet van de kop een rechthoek met een snuit.
- *Regel:* geen rechte lijnen waar het dier rond is; segmentlengtes geleidelijk op- en aflopend (§3, §12). Ontwerp: "ronde teddykop met kleine ronde oren" (FEEDBACK ronde 9, ONTWERP.md).
- *Goed bij:* **Teddiursa** (schedel als boog, oren als cirkels van ±7 px die deels achter de schedel staan), **Zigzagoon** en **Poochyena** (kop breekt aan de achterkant en de kaak uit in een wangpluk die naar achter-onder wijst).
- *Oplossing:* teken alleen de schedel opnieuw; masker, ogen en snuit blijven op hun plek. Bovenkant als boog: y 23 x 21–31, y 24 x 18–34, y 25 x 16–36, y 26 x 15–37 (runs 11 → 3,3 → 2,2 → 1,1). Achterkant bolt 1–2 px uit: x 38 voor y 27–28, x 39 voor y 29–32, x 38 voor y 33–34, en dan met runs 1,1,2,3 terug naar de nek. Kin: breek y 40 tot een curve die naar de keel stijgt (y 39 x 20–25, y 40 x 26–30) en zet een wangpluk van 2–3 punten naar achter-onder op (33–37, 36–39). Oren 5 rijen hoog en rond (ver ±4×4, half achter de schedel; nabij ±5×5 met 2 px crème (7) binnenin, niet roze, §15), toppen y 19–20.

**3. Gezicht in banden en brilogen**
- *Wat:* de bovenrand van het masker is een kaarsrechte rij index 2 op y 28, x 13–31 (19 px). Direct daarboven liggen de crème wenkbrauwen op y 27 (x 17–19 en 23–27). Daaronder loopt de crème snuit bijna horizontaal (y 34–36). Op 1× leest dat als drie strepen: een bril. De ogen zijn lijstjes. Nabij (23–28, 29–34) heeft zwarte zijkanten op x 23 en x 28 over 4 rijen, een zwart bovenlid van 4 px en een zwarte onderrand: een rechthoek met overal dezelfde zwarte rand. De felste kleur (goud 13) ligt als volle rij bovenaan (y 30, x 24–27; ver y 30, x 17–19), en de pupil ligt rechtsonder. Bij Gen 3 is het precies andersom: het lid werpt schaduw, dus de iris is bovenin het donkerst en onderin het lichtst (Jigglypuff-les, nachtaap-keuring punt 2). Het verre oog (16–19, 29–33) heeft dezelfde lijst.
- *Regel:* tekeningen volgen de vorm en krijgen licht en schaduw (Textures; nachtaap punt 7); ogen geïntegreerd, omlijning naast de pupil in maskerkleur, niet zwart (§11b, §12); geen identieke delen (Splices 1).
- *Goed bij:* **Zigzagoon** (het masker is een band die om het oog heen buigt en naar de wang afloopt; het oog is een kraal zonder lijst), **Poochyena** en **Sneasel** (schuin amandeloog: zwaar lid boven, onderkant open, voor een Dark-blik).
- *Oplossing:*
  - *Masker:* laat de bovenrand de schedel volgen. Een neusbrug van 2 px kopkleur tussen de ogen (x 20–22, y 28–29) maakt van de balk twee lobben. Boven de ogen y 28; achter het nabije oog stijgt de rand naar y 27 op x 31–33 en loopt dan uit in een punt naar het oor. De onderrand achter het nabije oog zakt naar een punt op (31–33, 35): het klassieke wasbeermasker als vleugel, niet als balk.
  - *Ogen:* alleen het bovenlid zwart (1), nabij 5 px op y 29 met 1 px flick omhoog aan de buitenhoek (29, 28). Zijkanten en onderrand in maskerkleur (2), niet in zwart. Iris: oranje (14) als eerste rij onder het lid, goud (13) eronder. Pupil tegen het lid, met de glans (12) linksboven in de pupil. Hoeken afronden (rijen 4-5-5-3). Ver oog: 3 px breed, 1 rij lager, glans 1 px.
  - *Wenkbrauwen:* geen rechte rijen, maar twee boogjes van 3 px die de bovenrand van het masker volgen, met 1 rij kopkleur ertussen (§17).

**4. Staart is een buis zonder haak**
- *Wat:* van y 21 tot y 36 is de staart overal 5–6 px breed (4 vul), met dezelfde strepen in de lengte (2 | 5 | 4 | 4 | 3 | 3 | 1). De linkerrand verspringt 1,1,0,1,1,0,0,0,1,0,1,0 (wiebelig, §3). De haak bovenaan is 3 px ((55–57, 20), (58, 21)). Op 1× leest het als een rechtopstaande kattenstaart. Ontwerp B draait juist om die staart ("vraagteken", "dief in de staart"), en de olinguito heeft een pluimstaart.
- *Regel:* organische delen buigen en verjongen, geen buizen (§12; nachtaap punt 6); het kenmerk van het concept moet op 1× lezen (fakemon-gids: silhouet).
- *Goed bij:* **Sentret** (dikke staart met ringen die mee buigen), **Linoone** (pluim die naar de punt uitwaaiert), **Aipom** en **Mew** (haak/krul met lucht eromheen).
- *Oplossing:* staartvoet breder en pluimig (7 vul op y 32–38, x 48–57), dan geleidelijk smaller naar 3 vul bij y 22. Laat de punt over 4–5 px naar links terugkrullen tot een leesbare haak (y 16–21, x 50–57), met ≥ 1 px lucht in de bocht. Gebruik linkerrand-runs die regelmatig oplopen (bijv. 3,2,2,1,1,1). Optioneel, als het ontwerp het wil: 2 schuine ringbanden in index 3 (y ±25 en ±30) die de buiging volgen (coati-ringen uit concept B).

### Polijsten

**5. Achterpoten: paal met identieke hoeven**
- *Wat:* de nabije poot is van y 47 t/m 51 een rechte kolom van 6 px (x 44–49) onder een ronde dij: een kippenpoot. De voet steekt aan beide kanten 1 px uit (x 43 en x 50) en leest als een hoef. De verre voet (35–42, 51–52) is pixel voor pixel dezelfde rij `12312331` / `11 111` als de nabije (43–50, 53–54): even breed en even donker.
- *Regel:* twee poten verschillend maken in hoek, lengte, dikte, tint en voetmaat (§18); geen kopieën (Splices 1); verre poot kleiner en donkerder (§12).
- *Goed bij:* **Poochyena** (poot verjongt, de hiel steekt naar achteren uit, de tenen wijzen naar links-voor).
- *Oplossing:* nabije poot verjongen van 6 naar 5 px. Hiel 1 px naar achteren op (50, 49–50). Voet alleen naar links uit (tenen x 42–45, hiel x 49), met een zwarte onderrand. Verre voet 6 px (x 36–41), alleen in index 2/3, twee teenpixels.

**6. Naad om de dij**
- *Wat:* de dij is omlijnd met index 2 (bijna zwart): bovenrand y 38 x 47–51 (5 px recht), linkerrand x 44–45 voor y 39–46. Samen met punt 1 leest de dij als een losse lap op de romp (binnenaandeel bijna-zwart 0,21; Gen 3-bruin 0,03–0,14).
- *Regel:* vormen binnen één kleurgroep scheiden met de schaduwtint, niet met omlijning (Shading). Poochyena scheidt dij en flank met zijn schaduwgrijs.
- *Oplossing:* bovenrand van de dij in index 3, linkerrand in 3 met 1 px 2 alleen op de diepste plek (44, 44–45). Hooglicht (5) linksboven op de dij laten staan.

**7. Klauwen: tweede lichte kleurgroep, en de voorpoot staat op zijn tenen**
- *Wat:* de klauwen gebruiken een eigen grijze groep (9 / 10 / 11, plus wit 12) met middengrijs (118,110,114) als rand aan de buitenkant. Aan de schaduwkant ontbreekt het zwart, en de punten zijn losse grijze pixels ((15, 55), (20, 54), (13, 46)): op licht vervagen ze, op donker lichten ze op als losse streepjes. De nabije hand eindigt op y 48. De klauwen (y 49–55) zijn het enige wat de grond raakt, dus de poot staat 6 px boven de grond op zijn nagels, als op hakken.
- *Regel:* omlijning per kant, zwart in de schaduw (§8); "klauw als deel van de hand" (§11b); simpel palet (fakemon-gids: 2–3 hoofdkleuren; het ontwerp zegt "crème: snuit, buik, klauwen").
- *Goed bij:* **Ursaring** en **Sneasel** (lichte klauw, zwart aan de onderkant, de voet van de klauw in een donkerder tint die in de vingers overloopt), **Sandshrew/Zangoose** (de handpalm raakt de grond of de klauwen wijzen naar voren).
- *Oplossing:* zet de klauwen in de crème groep (6/7/8). Dan komen 9, 10 en 11 vrij, voor bijvoorbeeld een aparte omlijningstint (punt 1b) of een lichtere kopbasis. Zwart aan de rechter- en onderkant van elke klauw, 6 alleen aan de bovenkant. De nabije hand 2–3 px lager (handpalm op y 51–52), met klauwen die schuin naar links-voor over de grond wijzen (runs 2,2,1) in plaats van recht omlaag. Lengte behouden (Jordi wil lange klauwen). Ver handje: klauwen 1 tint donkerder.

**8. Formaat**
- *Wat:* 1049 px. De fase 1-starters van Gen 2–3 liggen op 602–903 (gemiddeld 798); Linoone (fase 2) is 1089. Ronde 15 werd al iets kleiner, maar is nog 30% groter dan het gemiddelde. Een dikkere staart (punt 4) maakt hem nog groter.
- *Regel:* §0.6; pre-evoluties kleiner en eenvoudiger (§10).
- *Oplossing:* knip 2–3 kolommen uit de romp tussen de verre achterpoot en de armen (x ±36–38, geen kenmerken; §15), en houd de staart smal aan de punt. Doel ≤ 950.

## §0-checklist (eigen controle)
1. Diagonaal: ✔ (kop 3/4, verre kant links-hoger en in schaduw).
2. Geteld en verbonden: ✔ (2 oren, 2 ogen, 4 poten, 4 klauwen, staart). Geen open randen in frame 1 en 2 (nagemeten).
3. Geen rechte lijnen: ✗ kop (punt 2), maskerrand en ogen (punt 3), staart (punt 4), dijnaad (punt 6).
4. Ogen geïntegreerd: ✗ (punt 3).
5. Silhouet op 1×: leest als "bruin marterachtig dier dat sluipt"; het concept (pluim-/haakstaart, teddykop) leest niet (punt 2 en 4).
6. Formaat: ✗ licht (punt 8).
7. Pose niet stijf: ✔ voor de romp; de voorpoot op nagels is het enige onnatuurlijke steunpunt (punt 7).

## Ontwerpnotities voor Jordi (smaak, geen pixelpunten)
- **Hij is weggedreven van concept B naar het silhouet van zijn eigen evolutie.** Gekozen was B: hij zit rechtop met gevouwen klauwen, een geringde vraagteken-staart, oranjebruin en crème, "het donker zit alleen in de tekening". Ronde 15 staat op vier poten, horizontaal, met een rechte staart omhoog. Dat is bijna precies de fase 2-schets (coati) op `concept_B.png`. Gevolg: de coati moet straks met dezelfde houding "groter en meer" worden. Een fase 1 is volgens de gids juist kleiner, ronder en eenvoudiger dan zijn evolutie. Keuze: sluiphouding houden en de coati duidelijk anders maken (hoger op de poten, lange snuit, staf-staart), of fase 1 terug richting B. Dit is waarschijnlijk een deel van het "niet perfect"-gevoel: hij oogt als een jong roofdier, niet als een starter-baby.
- **"Donker" is bij Gen 3 een accent, geen totaaltint.** Poochyena, Sneasel en Houndour zijn Dark door zwart plus één fel accent op een gewone basis. De olinguito is donker gemaakt door de hele ramp te verlagen. Vel4 laat zien dat hij met één stap lichter nog steeds donkerbruin leest (Ursaring-niveau), maar met een masker dat werkt.
- **Er is maar één licht vlak** (de crème snuit; 8% licht tegen 22–64% bij de starters). Een crème keel of borstvlek (onder de kin, 26–32, 41–44) of crème ringen in de staart zouden de 1×-lezing en de "teddy"-kant helpen. Het ontwerp noemde crème voor snuit, buik en klauwen.
- **Blik:** de pupil rechtsonder in een rechthoek leest nu als nors of onderzoekend. Een schuin, half gesloten amandeloog (punt 3) geeft de "sluwe dief" die het concept noemt, zonder dat hij boos wordt.
