# Keuring kolibrie ronde 3 (24 okt, onafhankelijke keurder, herkeuring)

## Wat ik keurde
- **(a)** `kolibrie.png`: hoofdversie op het bevroren silhouet, 1016 px, box 63×61.
- **(b)** `kolibrie_variant_sleep.png`: zelfde sprite met een slepende staart, 997 px, box 63×53.

Beide zijn 64×64, P-modus, 16 kleuren, index 0 transparant, met hetzelfde palet.

## Waarmee ik vergeleek
Dezelfde 14 referenties als in ronde 2 (eerste frame met `normal.pal`), op 1× en 6×, licht en donker: Swellow, Yanma, Ninjask, Beautifly, Crobat, Fearow, Articuno, Honchkrow, Venomoth, Murkrow, Mismagius, Drifblim, Ho-Oh en Talonflame.

Vel: `keuring_vergelijking.png`.
- Boven: (a) en (b) op 6×, licht en donker.
- Onder: 1× (2× weergegeven) naast Swellow, Yanma, Ninjask, Beautifly, Crobat, Fearow en Articuno, op licht en donker.

## Pixeldiff
- **(a) t.o.v. `silhouet_v6_groot_1x.png`:** 64 erbij, 34 eraf. Alles ligt binnen 1 px, op één pixel na: (30,40) ligt 2 px weg. Dat is de buikboog die ik zelf voorstelde, gemeld. **PASS.**
- **(b) t.o.v. (a):** 279 pixels verschillen, allemaal in de staartzone. Buiten de zone (x < 42, of x < 36 vanaf rij 41) is de diff 0, en het palet is identiek. Ik heb dat zelf nagemeten; het klopt met NOTITIES.

## Totaaloordeel
- **(a) hoofdversie: NIET GOED.** Op 1× hangen de drie slierten nog als poten met voetjes onder het lijf, vooral op donker. De maker schrijft zelf "niet goed genoeg", en een zelfgenoemd zwak punt is een automatische fail. Binnen het bevroren silhouet is dit niet te repareren.
- **(b) variant sleep: NIET GOED, maar dichtbij.** De hoofdvraag is opgelost: hij leest op 1× op licht en op donker overduidelijk als kolibrie, niet als insect. Er resten vier pixelfouten van samen ±40 px, zie de reparatielijst. Na die reparatie is hij in mijn ogen GOED en klaar voor Jordi.

---

## 1. Reparatiepunten uit ronde 2, per punt
| # | punt | (a) | (b) | toelichting |
|---|---|---|---|---|
| 1 | Slierten als lint, niet als poten | **FAIL** | **deels** | Gelukt: geen zwart meer aan de lichtkant, bogen in plaats van recht-knik-recht, en vervagend naar bleek. Nieuwe fout in beide: de **schaduwkant is lichter dan de lichtkant**. Het patroon `5 7/8 6` heeft de omlijningsbasis `5` (80,46,118, luma ±64) aan de lichtkant en de schaduwtint `6` (100,58,146, luma ±80) aan de schaduwkant. De waarde is dus nog steeds omgekeerd. In (a) lezen de slierten bovendien nog als poten (zie §2). |
| 2 | Sliert 2 los van racket A/B | PASS | n.v.t. | (a): kolom x 55, rij 48–51, is lucht, en B hangt aan een steeltje. In (b) raken de slierten elkaar niet. |
| 3 | Vlammetjes als vlam | **FAIL** | **FAIL** | (a): de vormen zijn nu vlammen (punt omhoog, ronde voet), maar op 1× zitten ze als witte voetjes onder aan de "poten". (b): S1 (x 59–63, rij 26–32) is een goede vlam. **S2** (x 57–63, rij 38–42) en **S3** (x 57–62, rij 48–53) zijn ruiten met een punt naar boven, beneden én opzij: op 1× op donker lezen ze als **glinstersterretjes**, niet als vlam. De maker schreef die les zelf op ("een kruis- of ruitvorm leest als glinstering"). |
| 4 | Vleugels doorschijnend à la Venomoth/Yanma | PASS | PASS | Fluweel alleen op de wortel, daarna lila en bleek, met doorlopende pennen `b` tot aan de rand en een gesloten rand. Naast Yanma en Venomoth leest dit op 1× en 6× als doorschijnend. |
| 5 | Segmentatie weg | PASS | PASS | Violet gedempt (134,84,198; verzadiging 0,58, Crobat-niveau). De kop gaat via `6` in de keel over in de borst. Blauwgroen is een smal glansje (x 17–24, rij 24–27). Op 1× leest dat als één vogel met een donkere kap; het mug-segment is weg. |
| 6 | Kop leesbaar op donker | PASS | PASS | Het koele randlicht `4` op kruin, gezicht, snavelrug en de voorrand van de vleugelwortels werkt zoals bij Murkrow en Honchkrow. Kop en snavel blijven op donker zichtbaar. |
| 7 | Buik rond, franje met veerpunten | buik PASS, franje **FAIL** | buik PASS, franje **FAIL** | De buik is een boog met looplengtes 3-4-7-5-4. De franje heeft inkepingen bij (48,36) en (49,38), maar op 1× leest er geen staartveer. In (a) is dat erg (er is geen staart, alleen poten). In (b) is het minder erg, omdat de slierten de staart dragen. Nieuw in (b): de onderkant van de staartbasis, rij 40 x 42–50, is een **rechte zwarte lijn van 9 px** (zie §3, A6). |
| 8 | Kuif als drie veren | **FAIL (laag)** | **FAIL (laag)** | Inkeping (13,16) toegevoegd, en op 6× zijn er nu drie punten. Maar de veren komen nog samen in één steel (rij 17–19, x 12–17: `515751`, `1551`, `121`). Op 1× is het een paars kuifje met drie lichte stipjes. Leest niet fout, maar ook niet als drie veren. De vorm is bevroren en Jordi was akkoord ("de jeguaka is goed"). Vindt Jordi hem zo goed, dan is dit punt gesloten. |
| 9 | Open randen | **FAIL** | **FAIL** | De punten uit ronde 2 zijn dicht. Nieuw: **schaduwtint `6` naast transparant**, 25 px in beide versies: (a) onder meer (50–57,36–37), (60–62,38–41), (44–47,41–45), (18,37); (b) onder meer (50–56,36), (47–54,41), (45–53,42–46), (18,37). Daarnaast in (a) 15 px bleek `d` op de slierteinden zonder rand ((59–61,45–47), (52–53,48–52), (40–45,52–57)). |
| 10 | Polijsten (hooglicht, oog) | PASS | PASS | De hooglichten liggen als één band langs de bovenflank (rij 34). Oog: glans (10,26), reflectie (11,27), bovenlid zwart. Klein en geïntegreerd. |

## 2. Hoofdvraag: leest hij op 1× als kolibrie, ook op donker?
- **(a): FAIL.** Kop, kuif, vleugels en lijf lezen nu als kolibrie, een grote verbetering. Maar onder de buik hangen drie bijna verticale slierten met lichte vlammetjes onderaan. Op donker zijn het drie poten met lichtgevende voetjes; op licht drie gebogen poten. Naast Yanma (zelfde rij) is de insectlezing nog steeds te zien. Kleur lost dit binnen ±1 px niet op (lees de NOTITIES van de maker).
- **(b): PASS.** Op licht een paarse kolibrie met een lange staart die naar achteren sleept (zelfde gebaar als de staartveren van Swellow). Op donker is het dezelfde vogel, met drie lichtpuntjes aan het eind van de staart. Onder de buik is het leeg, dus er is geen poot- of muglezing meer. Met Yanma en Ninjask ernaast is het verschil nu duidelijk: vogel, geen insect.

## 3. Alle eisen en richtlijnen opnieuw

### SPRITE_NORM
| # | eis | (a) | (b) | waar / reparatie |
|---|---|---|---|---|
| 1 | Leest op 1× als Pokémon van het bouwtype | **FAIL** | PASS | Zie §2. |
| 2 | 3/4 links-voor | PASS | PASS | |
| 3 | Delen vast | PASS | PASS | Elke sliert in (b) komt uit de staartbasis (x 42–50, rij 33–42). |
| 4 | Geen Escher | PASS | PASS | S1 (ver) ligt boven, S3 (dichtbij) onder, met lucht ertussen. |
| 5 | Curven, geen rechte lijnen ≥ 4 px waar rond | PASS | **FAIL** | (b): (1) de onderkant van de staartbasis, rij 40 x 42–50, is 9 px zwart en recht. (2) S1 loopt horizontaal tot x 57 en knikt in een rechte hoek omhoog (L-hoek bij (56–59,33–36)); dat is een hoek in een curve (§3). Reparatie: (1) laat de lijn naar rechts oplopen in stappen van 3-3-3 (staartbasis wordt smaller); (2) laat S1 vanaf x 54 met treden 3-2-1-1 omhoog buigen naar de voet van het vlammetje. S3 (helling 2 px per rij) is een rechte veer; dat mag, zoals bij Swellow. |
| 6 | Kop | PASS | PASS | 23% van de hoogte. |
| 7 | Ogen geïntegreerd | PASS | PASS | |
| 8 | Kenmerken leesbaar op 1×, geen klodders of harken | **FAIL** | **FAIL** | (a): de vlammetjes lezen als voetjes. (b): S2 en S3 lezen als sterretjes (punt 3). Reparatie: zie §5, punt 2. |
| 9 | Omlijning: zwart/donkerst aan de schaduwkant, geen open randen | **FAIL** | **FAIL** | De schaduwkant van de slierten is `6`, lichter dan de lichtkant `5`; en `6` grenst aan transparant (punt 1 en 9). |
| 10 | Geen Chernobyl | PASS | PASS | |

### FAKEMON_CHECKLIST (vogel)
| # | (a) | (b) | toelichting |
|---|---|---|---|
| A1 silhouet leest als soort | **FAIL** | PASS | Zie §2. |
| A2 dominant kenmerk | PASS | PASS | Snavel en staart. |
| A3 diagonale compositie | PASS | PASS | (b): de vleugels rechtsboven en de staart rechts in balans; kop links. |
| A4 negatieve ruimte | PASS | PASS | |
| A5 niet symmetrisch | PASS | PASS | |
| A6 geen bouwblokken | PASS | **FAIL** | (b): de rechte onderkant van de staartbasis (rij 40). |
| B1, B2, B7 | PASS | PASS | Eén oog en een profielsnavel, zoals bij Swellow. |
| C1 alles geteld | PASS | PASS | |
| C7 één houding | PASS | PASS | (b): de slepende staart past beter bij een zwevende vogel dan hangende slierten. |
| C8 staart sluit aan en buigt | **FAIL** | PASS | (a): de slierten hangen omlaag. (b): ze sluiten aan in het verlengde van de rug- en buiklijn en waaieren uit. |
| D1/D2 formaat | PASS | PASS | Zie §4. |
| E1 verre kant donkerder | PASS | polijsten | (b): S1 (ver) heeft het felste hooglicht `8` (x 51–55, rij 34), feller dan S3 (dichtbij). Beter: S1 1 tint donkerder (`8` → `7`). |
| E2 overlap met omlijning | PASS | PASS | |
| E3 donker-aandeel | PASS | PASS | Het zelfgenoemde zwakke punt "kop verdwijnt op donker" is opgelost. |

### SPRITING §0–§8
| punt | (a) | (b) | toelichting |
|---|---|---|---|
| §0.1–0.2, 0.4, 0.7 | PASS | PASS | |
| §0.3 geen rechte lijnen | PASS | **FAIL** | Rij 40 en de L-hoek van S1. |
| §0.5 silhouet leest | **FAIL** | PASS | |
| §0.6 formaat | PASS | PASS | Zie §4. |
| §1–§2 handwerk per onderdeel | PASS | PASS | |
| §3 curven | PASS | **FAIL** | De L-hoek van S1. |
| §4 palet | PASS | PASS | 16 kleuren. Vier groepen (fluweel, violet, glans, geestlicht), samenhangend en niet te fel. |
| §5 licht linksboven, shading met vorm | **FAIL** | **FAIL** | Lijf en kop goed (randlicht linksboven, slagschaduw onder de vleugel, geen kussen). Alleen de slierten: de schaduwkant is lichter dan de lichtkant. |
| §6 glans | PASS | PASS | |
| §7 texturen | PASS | PASS | |
| §8 omlijning | **FAIL** | **FAIL** | Open randen in `6` (en `d` in (a)). De kuif valt onder pseudo-omlijning en mag. |

### FAKEMON_DESIGN en SPEC
| punt | (a) | (b) | toelichting |
|---|---|---|---|
| Simpel, geen ruis | PASS | PASS | Gaas, vlekjes en badge zijn weg. |
| Beperkt palet, één geheel, geen hybride | PASS | PASS | Geen kop-borststuk-achterlijf meer. |
| Ghost-sfeer: mystiek, niet eng | **FAIL** | PASS | (a): de lichtpuntjes zitten op de plek van voeten. (b): de linten vervagen naar geestlicht met lichtende punten, zacht en niet eng. Op licht subtiel, op donker duidelijk. |
| SPEC vleugels doorzichtig | PASS | PASS | |
| SPEC staart: Articuno-dynamiek | **FAIL** | PASS | (b): uitwaaierend, S1 krult omhoog en S2 golft. |
| SPEC racket = zielvlammetjes | **FAIL** | **FAIL** | (b): S2 en S3 zijn sterretjes. |
| SPEC kuif | FAIL (laag) | FAIL (laag) | Punt 8 in §1: een beslissing voor Jordi. |
| SPEC kop, palet | PASS | PASS | |

## 4. Formaat: echt een fail?
Gemeten:
- **vulling** = pixels / boxoppervlak;
- **kern** = pixels die nog over zijn na 2× eroderen, met een 3×3-buurt. Dat is de massa die op 1× als "lijf" leest, zonder dunne delen.

| sprite | px | box | vulling | kern |
|---|---|---|---|---|
| kolibrie (a) | 1016 | 63×61 | 0,26 | 315 |
| kolibrie (b) | 997 | 63×53 | 0,30 | 317 |
| Crobat (eindvorm) | 1096 | 64×54 | 0,32 | 348 |
| Yanma | 966 | 64×34 | 0,44 | 327 |
| Murkrow | 937 | 43×36 | 0,61 | 418 |
| Swellow (eindvorm) | 1432 | 56×51 | 0,50 | 717 |
| Ninjask | 1338 | 57×45 | 0,52 | 771 |
| Beautifly | 1514 | 58×50 | 0,52 | 902 |

**Conclusie: geen fail. Ik trek de D1-fail uit ronde 2 in.**
- Pixeltelling alleen is hier misleidend: een kolibrie is in werkelijkheid een van de kleinste vogels, en een slank zwevend ontwerp hoort weinig massa en veel lucht te hebben.
- De echte maatstaf is **Crobat**, een eindvorm met bijna dezelfde vulling en kernmassa (0,32 / 348 tegen 0,30 / 317). Op het 1×-vel hebben Crobat en de kolibrie vergelijkbare aanwezigheid: beide vullen de box tot de rand met vleugels.
- Swellow, Ninjask en Beautifly zijn twee keer zo dicht, omdat ze een gedrongen romp of grote dichte vleugelvlakken hebben. Dat past niet bij dit ontwerp.
- Groter maken kan alleen door het lijf dikker te maken (een silhouetwijziging). Dat zou de kolibrie-elegantie kosten. Geen reparatie nodig. Wel een kanttekening voor Jordi: naast Swellow oogt hij lichter, en dat is bewust.

## 5. Geprioriteerde reparatielijst

### Variant (b), het advies aan Jordi
Alles klein, alleen in de staartzone. Kop, lijf en vleugels blijven bevroren (diff 0).
1. **Slierten S1–S3: omlijning in de juiste waarde** (eis 9, §5, §8; ±25 px). De schaduwkant (onder/rechts, nu `6`) wordt `1` of `5`. De lichtkant (boven/links, nu `5`) mag `5` blijven of op het meest belichte stuk `6` worden. Regel: de schaduwrand is altijd donkerder dan de lichtrand. Daarmee zijn ook de open randen in `6` weg, inclusief (50–56,36) aan de franje-onderkant en (18,37) onder de keel (die wordt `1`).
2. **Vlammetjes S2 en S3 als liggende vlam, niet als ster** (eis 8, SPEC; ±10 px). Ronde voet aan de kant van de sliert (links, 3–4 rijen hoog), aflopend naar één punt van 1 px naar achteren (rechts). Weg met de losse punt boven en onder: S2 (59–60,38) en (59–60,42); S3 het topje bij rij 48–49 en het staartje bij (58–59,53). De kern `f` blijft in de voet. S1 is goed: niet aanraken.
3. **Onderkant staartbasis niet recht** (eis 5, A6; ±6 px). Rij 40 x 42–50 wordt een oplopende lijn: x 42–44 op rij 40, x 45–47 op rij 39/40 en x 48–50 een rij hoger, in het verlengde van de buikboog.
4. **L-hoek van S1 als boog** (§3; ±4 px). Bij (54–59,33–36) treden 3-2-1-1 omhoog in plaats van horizontaal en dan verticaal.
5. *Polijsten:* het hooglicht `8` op S1 (ver) één tint terug, zodat S3 (dichtbij) het helderst is (E1).
6. *Voor Jordi:* de kuif (één gezamenlijke steel). Alleen aanpassen als hij erom vraagt; de vorm is door hem goedgekeurd.

### Hoofdversie (a)
Niet verder repareren. De poot-lezing zit in het bevroren silhouet (drie slierten verticaal onder het lijf), en dat erkent de maker zelf. Kiest Jordi tóch voor het silhouet, pas dan dezelfde punten 1 en 5 toe, sluit de bleke randen van de slierteinden met `c`, en geef hem eerlijk mee dat hij op donker als poten leest.

### Voor de coördinator en Jordi
- Leg Jordi (b) voor **na** reparatie 1–4, met (a) ernaast als het bevroren alternatief. Vermeld dat de staart van (b) een silhouetwijziging is, zijn beslissing.
- Formaat: geen probleem (§4).
