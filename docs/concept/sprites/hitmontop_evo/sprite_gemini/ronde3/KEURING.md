# Keuring Hitmongroove ronde 3: `capoeira.png` (torso c)

Keurder: vers en onafhankelijk (7 nov). Getoetst zijn alleen de twee eisen: (1) trouw aan `referenties/gemini_gekozen_capoeira.png` met de toegestane afwijkingen uit de SPEC, (2) Gen 3 / Dragonfly Cave-techniek. Vergeleken op 8× naast het verkleinde model (`gereedschap/model_derde.png` met `kader.json`) en naast Hitmontop, Hitmonchan en Hitmonlee (bovenste 64×64-frame van `anim_front.png`).

Hulpplaatje: `keuring.png`. Links r3 c met de reparatiepixels omkaderd en genummerd. In het midden een proefversie van de keurder met alle reparaties toegepast, alleen om te laten zien dat ze werken; de maker voert ze zelf uit in `raster.txt`. Rechts het model. Onderaan 1× en 2×, voor en na.

Coördinaten zijn (x,y), met 0 linksboven. Tinten volgen het raster: 1 zwart, 2/3/4/5 huid (licht → donker), 6 wit, 7 grijs, 8/9/A geel (licht → donker), B/C/D groen (licht → donker), E/F blauw.

## Metingen
- **Selout:** van de randpixels aan de lichtkant (leeg links of boven) is maar **22%** gekleurd (39 van 180; de rest is zwart). Bij de drie Gen 3-Hitmons is dat **55–75%**:
  - Hitmontop: 72 bruine randpixels tegen 37 zwarte;
  - Hitmonlee en Hitmonchan zitten in dezelfde orde.

  Dit is het grootste verschil met Gen 3: de sprite leest daardoor als "zwart omlijnd plaatje".
- **Tintstappen in helderheid:**

  | Kleurgroep | Tinten | Stappen | Oordeel |
  |---|---|---|---|
  | Huid | 199 / 161 / 116 / 78 | 38, 45, 38 | Goed |
  | Groen | 157 / 106 / 69 | 51, 37 | Goed |
  | Blauw | 134 / 85 | 49 | Goed |
  | Geel | 232 / 207 / 142 | 25, 65 | Ongelijk; zie ter info |

- **Kleine vlakjes:** deze zijn bedoeld:
  - de vlecht en de koorden;
  - de witte banden in de benen;
  - de glimpjes op de vuisten en de arm.

  Eén echt ruisgeval: de koordband om de steunarm (zie reparatie 6).
- **Torso c:**
  - de glans 2 is een los ovaal midden in de basistint (24–27,30 / 23–28,31 / 23–27,32 / 24–26,33), aan alle kanten omringd door 3;
  - linksboven in de torso, de lichtkant, staat een schaduwvlek in tint 4: (20,30), (21,30) en (20,31);
  - de schaduwsikkel rechts is op rij 31–35 precies 2 px breed, evenwijdig aan de rand (banding), en wordt pas daarna breder.

  Een glans in het midden met donker aan de lichtkant is precies de "bulge" (pillow-achtig). Bij Hitmonlee (kop) ligt de glans als sikkel tegen de bovenlinkerrand, met 1 px basistint ertussen.

## Oordeel per zone
| Zone | Oordeel | Kort |
|---|---|---|
| Kop | **PASS** | Ogen zijn pixel voor pixel Hitmontop (glans linksboven, past bij het licht) en staan binnen ±0,5 px van de modelogen. Mond, V-lijn, flappen en knot met witte band volgen het model; door Jordi goedgekeurd. Alleen een kleine bandingrest: zie reparatie 8, optioneel. |
| Torso | **FAIL** | Glans als los ovaal in het midden, schaduw aan de lichtkant, sikkel met constante breedte (reparaties 3, 4 en 5). Silhouet en grote schaduwmassa rechtsonder kloppen met het model. |
| Vrije arm + vuist | **PASS** (kleinigheid) | De vuistbal is goed geschaduwd (glans linksboven, selout 5 aan de lichte kant). De band volgt het model. Eén pixel selout ontbreekt aan de bovenkant van de bovenarm, (17,26); die zit bij reparatie 2. |
| Steunarm + banden + hand | **FAIL** | De linkerkant van de arm is zwart naast de lichtste tint 2. De koordband is een 8/9-dambord (ruis), wat in Gen 3 niet voorkomt (reparaties 2 en 6). Lengte (een derde korter), koordband (toegestaan) en ronde steunvuist kloppen. De vuistbal zelf is goed: sikkel rechtsonder, glans linksboven. |
| Koord (heupband + hangende koorden) | **PASS** | De gedraaide diagonalen 8-9-A lezen als koord en lopen zoals in het model. Zie ter info over selout. |
| Benen | **FAIL** (klein) | Wit met grijze schaduwkant: Jordi's opmerking is opgelost, en het wit als spiraalband is toegestaan. Maar de linkerbeen-lichtkant is zwart, terwijl het rechterbeen aan dezelfde lichtkant wel selout D heeft: dat is inconsistent (reparatie 1). In het kruis staat een binnenlijn D van 2 px breed en 4 rijen recht; Gen 3 gebruikt 1 px (reparatie 7). |
| Voeten | **PASS** | Donkere zool bovenop volgt het model. De witte tenen zijn zwart omlijnd aan de lichtkant; reparatie 9 is optioneel. |
| Algemeen | **FAIL** | De selout aan de lichtkant ontbreekt grotendeels (reparaties 1, 2 en 9). Leest goed op 1× en 2×; pose en silhouet trouw aan het model (43 px verschil, gelijk aan r1/r2). |

**Aantal FAIL: 4 zones** (torso, steunarm, benen, algemeen).

## Reparaties (belangrijkste eerst)
Buiten deze pixels geldt diff 0.

**3. Torsoglans als sikkel linksboven** (tegen de bulge; de kern van Jordi's opmerking)
- Weg, dus naar 3: (27,30) · (26,31), (27,31), (28,31) · (25,32), (26,32), (27,32) · (24,33), (25,33), (26,33).
- Nieuw 2: (25,29), (26,29), (27,29) · (23,30) · (22,31) · (22,32) · (22,33), (23,33).
- Resultaat per rij:

  | Rij | Glans 2 (kolommen) |
  |---|---|
  | 29 | 25–27 |
  | 30 | 23–26 |
  | 31 | 22–25 |
  | 32 | 22–24 |
  | 33 | 22–23 |

  Dat is een sikkel die de bovenlinkerrand volgt, met 1 px basistint 3 tot de buitenlijn of de band. Hij loopt taps naar rechtsboven en naar beneden.

**4. Geen schaduw aan de lichtkant van de torso**
- (20,30), (21,30) en (20,31): van 4 naar 3.

**5. Sikkel rechts taps laten beginnen** (banding)
- (35,31) en (35,32): van 4 naar 3.
- De sikkel wordt dan per rij 1, 1, 2, 2, 2, 3, 4, 4, 5, 5 px breed, in plaats van vijf rijen gelijk.

**2. Selout armen**
- Steunarm, linkerkant: (30,47), (30,48), (30,49): van 1 naar 5.
- Koordband steunarm, linkerkant: (28,43), (28,44): van 1 naar A.
- Witte manchet steunarm: (30,51), (30,52): van 1 naar 7.
- Bovenarm van de vrije arm: (17,26): van 1 naar 5. Zo sluit hij aan op de 5-rij (14–16,26).

**6. Koordband steunarm: dambord eruit, gedraaid koord erin** (zelfde stijl als de band om de vrije arm: twee diagonale A-lijntjes, licht links, donker rechts)

| Rij | x = 29 | 30 | 31 | 32 | 33 | 34 |
|---|---|---|---|---|---|---|
| 43 | 8 | 8 | 9 | A | 9 | A |
| 44 | 8 | 9 | A | 9 | A | A |
| 45 | – | A | 9 | A | A | – |

**1. Selout linkerbeen** (lichtkant, zoals het rechterbeen al heeft)
- (19,11), (20,12), (21,13): van 1 naar A (naast het geel).
- (22,14), (23,16), (24,17), (25,18), (26,19), (26,20), (27,21), (28,22), (27,23): van 1 naar D (naast het groen).
- (22,15): van 1 naar 7 (naast het wit).

**7. Kruisnaad 1 px**
- (35,21), (35,22), (35,23), (35,24): van D naar C.
- Wat blijft is één D-lijn in kolom 36 (rij 21–25), zoals een Gen 3-binnenlijn.

**8. (Optioneel) Schaduwstrook rechts van de kop taps**
- (24,38) en (24,39): van 4 naar 3.
- De strook begint dan bij 0 en loopt via 1 naar 2 px, in plaats van 8 rijen 2 px breed.

**9. (Optioneel) Witte tenen selout**
- (12,4), (11,5), (10,6), (53,6), (54,6): van 1 naar 7.

Daarna controleren:
- 16 kleuren, geen nieuwe tint;
- geen open randen;
- diff 0 buiten deze pixels.

## Ter info voor Jordi (geen FAIL, ontwerp- of paletkeuzes)
- **Torsoglans:** reparatie 3 verplaatst de glans van het midden (c) naar de bovenlinkerrand, zoals Gen 3 het doet (Hitmonlee).

  Jordi koos c omdat die "het minst op een bulge" lijkt. De keurder verwacht dat de sikkel nog minder bulge leest, omdat licht in het midden met donker rondom juist het bolle kussen geeft (zie het middelste paneel in `keuring.png`). Wil Jordi de glans toch midden houden, dan blijven alleen 4 en 5 over.
- **Geel:** de stap 8→9 is klein (25) en 9→A is groot (65). A (184,140,40) iets lichter, bijvoorbeeld rond (200,156,56), maakt de stappen gelijkmatiger.

  Dat raakt alle koorden en banden, dus het is een paletkeuze en geen reparatie.
- **Hangende koorden:** die zijn nu aan beide kanten zwart omlijnd. Gen 3 zou de lichtkant in A zetten, maar bij 1 px dikke strengen versmelt dat met de A-schakels van de vlecht.

  Advies: zo laten.
- **Oog 2 tegen de V-lijn** (17,44): zoals de maker meldt, klopt dat met het model. Geen actie.
