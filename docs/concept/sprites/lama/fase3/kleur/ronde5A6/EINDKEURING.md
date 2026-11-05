# Eindkeuring lama fase 3, kleur ronde 5A6 (verse keurder, 5 nov)

Gekeurd: `lama3.png` + `normal.pal` (raster `ronde5A6.txt`). Vel: `eindkeuring_vel.png`, op een lichte en een donkere achtergrond. Het vel toont:
- de lama op 1× naast fase 2 en 12 echte Gen 3-sprites (Entei, Arcanine, Tauros, Hariyama, Machamp, Girafarig, Stantler, Slaking, Camerupt, Swampert, Raikou, Rapidash);
- de lama op 2× en 4× naast fase 2, Entei en andere referenties;
- een uitsnede van de poten op 8× met raster, coördinaten en gekleurde kaders om elke reparatie (R1–R7);
- de poten op 4× naast die van fase 2, Entei, Arcanine, Tauros en Girafarig.

Ik heb eerst zelf geoordeeld. Pas daarna heb ik SPEC.md (fase 3), de eindkeuring van fase 2 en NOTITIES.md gelezen. Daarna heb ik twee reparatievoorstellen ingetrokken, omdat ze Jordi's goedgekeurde verre achterpoot raakten (zie Poten, P3).

Rasterletters → index: `.`0 `k`1 `H`2 `C`3 `S`4 `d`5 `R`6 `U`7 `B`8 `D`9 `r`10 `m`11 `p`12 `y`13 `G`14 `g`15.

## Oordeel: **AF NA KLEINE REPARATIES** (7 punten, samen 28 px)

Technisch is de sprite schoon: er is geen enkele open rand en het palet klopt. Op 1× leest hij als een stompige lama met bombín, blauw pak, cape, riem en rok. De fouten zitten bijna allemaal in de afwerking van de voorpoten:
- de verre voorpoot is één vlak schaduwvlak (hetzelfde punt dat Jordi bij de verre achterpoot afkeurde);
- de voorhoeven hebben geen hoefkleur, de achterhoeven wel;
- er staat zwart aan de lichtkant van het verre windsel;
- er zit een inkeping in de omtrek bij de bovenste manchet;
- er zijn drie kleine plekken met een korrel of klont.

Twee alpha-wijzigingen (R1 en R7, samen 3 px) vullen inkepingen in de omtrek op. De rest is alleen kleur.

## 1. Richtlijnen (PASS/FAIL; twijfel = FAIL)
| Richtlijn | Uitslag | Toelichting |
|---|---|---|
| Formaat 64×64, PNG mode P, index 0 transparant (tRNS) | PASS | De palet is gelijk aan `normal.pal` (16 kleuren). |
| Kleurgebruik ≤ 16 incl. transparant | PASS | Alle 16 indexen worden gebruikt. |
| Eén component, geen zwevende delen | PASS | 1403 px, bbox x14–50 en y1–63. |
| Open randen (niet-omlijning tegen transparant) | PASS | 0 pixels gevonden (script: alles naast transparant is `k`, `d`, `D` of `m`). |
| Gekleurde omlijning aan de schaduwkant | PASS (met noot) | Onderaan liggen `d`-pixels tegen transparant (hoefranden y56–62) en rechts `D` aan de rok (x49–50, y42–46). `D` is bijna zwart, dus dat is in orde. Waar het een korrel is, is het opgenomen in R4/R7. |
| Zwart aan de lichtkant | **FAIL** | Het verre voorwindsel heeft links (x18, y50–56) 7 px `k`, terwijl de poot erboven en eronder `d` heeft. Dezelfde fout als R2 bij fase 2. → R2 |
| Korrels/inkepingen in de omtrek | **FAIL** | (31,52) is een 1-px inkeping met een uitsteeksel eronder op (31,53). (50,42) is een inkeping rechts in de rok. (36,26) is een putje in de rugcontour. → R1, R7 |
| Losse pixels / ruis | **FAIL** (klein) | (26,41) is een losse rode bies-pixel; de bies heeft een gat op x25. (21,46) is een opening in de zoomlijn boven de verre voorpoot. De overige pixels zonder gelijke buur zijn bewust: oog, vlechtglans, aguayo-patroon, pompons, hoeflichtje. → R5 |
| Klonten zwart / omlijning 1 px | **FAIL** | Er zit 2–3 px zwart tussen de nabije voorpoot en de gouden ruche (x32–34, y42–45). → R6 |
| Licht linksboven consequent | PASS | Kop, pak (U → B → D), cape, ruches en poten hebben hun lichtkolom links. |
| Banding / pillow shading | PASS | Er is geen pillow shading. De verticale `p/m`-strepen in de cape (x29–34, y32–38) lezen als plooien. De horizontale strepen in de windsels en de halsband zijn ontwerp (aguayo). |
| Ruimte voor reflectie en lichtje (§6) | PASS | Het oog is bevroren (5A3) en hoort niet bij deze keuring. |
| Leesbaarheid op 1× (licht en donker) | PASS | Je ziet een lama met bombín, vlechten (donkere strook langs de hals), blauw pak, paarse cape, gouden riem, rok in drie ruches en gestreepte windsels. Naast Tauros en Camerupt leest hij als een zware viervoeter. |
| Vier poten op 1× | PASS (silhouet bevroren) | De voorpoten lezen als één blok met twee windsels, en dat heeft Jordi geaccepteerd. Achter lees je twee poten. |
| Diagonaal / 3/4 naar links-voor | PASS | Dat is pose C2. |
| Geen rechte lijnen waar rond | PASS (voor Jordi) | De poten hebben rechte flanken (10 px). Dat komt uit het silhouet (W3) en hoort niet bij deze keuring. |
| Geen Chernobyl / misvormingen | PASS | |

## 2. Poten (Jordi: "laat de eindkeuring ook zeker nog meer naar die poten kijken")
Elke poot is apart bekeken: op 8× (licht en donker) en op 4× naast Entei, Arcanine, Tauros, Girafarig en fase 2.

| Punt | P1 nabije voorpoot (x22–31) | P2 verre voorpoot (x18–22) | P3 verre achterpoot (x32–41), door Jordi goedgekeurd | P4 nabije achterpoot (x40–48) |
|---|---|---|---|---|
| Volume (cilinder, licht- en schaduwkant) | PASS: `H` links, `C` midden, `S` rechts, `k` erbuiten | **FAIL**: x19–21 is één vlak `S` (y45–49 en y57–59), dus geen lichtkolom → R3 | PASS: lichte kolom links, donker rechts, schaduwsikkel onder de rok | PASS: `H`, `C`, `S`, `k` |
| Scheiding nabij/ver | PASS: de `d`-kolom op x22 scheidt de poten | **FAIL** (klein): op y58 ligt verre `S` (21,58) direct tegen nabije `H` (22,58), zonder scheiding → R4 | PASS: de `dd` op x40–41 is een bewuste donkere rand (5A5) | PASS: eigen `d`-omlijning op x41 |
| Knie/hak | FAIL, voor Jordi: de flanken zijn recht (silhouet). Het windsel dekt de pijp. | FAIL, voor Jordi (zelfde reden) | PASS: hak (5A5) | FAIL, voor Jordi: de knik rechts op y53 is maar 1 px |
| Hoef | **FAIL**: geen hoefkleur, alleen crème met losse `d`-puntjes (25,62) en (28,62) → R4 | **FAIL**: de crème loopt door tot de `kk` → R4 | PASS: bruine hoef met lichtje (36,57), bewust | PASS: `dddd` + `kkkk` (x42–47, y59–60) |
| Omlijning en selout | **FAIL**: inkeping (31,52) en uitsteeksel (31,53) → R1; klont x32–34 y42–45 → R6 | **FAIL**: zwart aan de lichtkant x18 y50–56 → R2; zoomlijn open op (21,46) → R5 | PASS. Noot: (35,58) `d` in de zwarte onderrand. Ik doe geen voorstel, want de poot is goedgekeurd en het leest op 1× niet. | PASS |
| Windsel: banden | PASS: goud, rood, blauw, groen, goud, rood, goud (y52–58), schaduwtint rechts | PASS: dezelfde volgorde (y50–56), 2 rijen hoger (perspectief), in middentinten (verre kant) | n.v.t. | n.v.t. |
| Windsel: even netjes afgewerkt | PASS na R1/R2: zelfde volgorde en zelfde opbouw. Alleen de randen verschillen (R1 rechts, R2 links). | | | |
| Windsel: banden buigen om de poot | **FAIL**, voor Jordi: alle banden zijn kaarsrecht. Entei's ringen buigen (onderrand donker en gebogen). Op 1× valt het weg. Echt buigen kost ±25–30 px herteken van beide windsels, en dat is geen kleine reparatie. | **FAIL**, voor Jordi (zelfde) | | |
| Windsel: gouden manchetten | PASS: boven y52 en onder y58 goud, met lichtje `H` links | PASS: boven y50 en onder y56 goud | | |

## 3. Reparaties (x,y; huidige → voorgestelde index)
**R1. Inkeping bij de bovenste manchet, nabije voorpoot** (2 px, waarvan 1 alpha). Nu loopt de rechtercontour van de poot x31 (y51) → x30 (y52) → x31 (y53). Dat is een korrel, en de gouden manchet is smaller dan de band eronder.
- (31,52): `.`0 → `k`1
- (30,52): `k`1 → `d`5. Daarmee eindigt de manchet net als de andere gouden banden: `dd` + `k`.

**R2. Zwart aan de lichtkant van het verre voorwindsel** (7 px). x18 is `k` op y50–56, terwijl de poot erboven en eronder `d` heeft. Gebruik de donkerste tint van elke band, net als aan de rechterkant van de nabije banden:
- (18,50) `k`1 → `d`5 (goud)
- (18,51) `k`1 → `m`11 (rood)
- (18,52) `k`1 → `D`9 (blauw)
- (18,53) `k`1 → `D`9 (groen; de nabije groene band eindigt ook in `D`)
- (18,54) `k`1 → `d`5 (goud)
- (18,55) `k`1 → `m`11 (rood)
- (18,56) `k`1 → `d`5 (goud)

**R3. Verre voorpoot heeft geen volume** (7 px). Nu is x19–21 één vlak `S`. Dit is hetzelfde recept als bij de goedgekeurde verre achterpoot (lichte kolom links). Rechts blijft `S`, met de `d` op x22 ernaast.
- (19,45), (19,46), (19,47), (19,48), (19,49): `S`4 → `C`3
- (19,57): `S`4 → `C`3
- (20,58): `S`4 → `C`3

**R4. Voorhoeven en scheiding onderaan** (4 px). Nu hebben de achterhoeven een bruine hoef en de voorhoeven niet.
- (26,62): `S`4 → `d`5. De nabije hoef wordt dan twee nagels, `dd` en `d`, met de `k`-splitsing op x27.
- (20,59), (21,59): `S`4 → `d`5. Dat geeft de verre voorpoot een hoef boven de `kk`.
- (21,58): `S`4 → `d`5. Dat scheidt de verre poot van de lichte nabije manchet (22,58).

**R5. Bies en zoom van het pak boven de voorpoten** (2 px).
- (25,41): `D`9 → `r`10. Zo sluit de rode bies aan: (26,41) zat los met een gat op x25.
- (21,46): `S`4 → `k`1. De zwarte zoomlijn over de verre poot loopt dan als nette diagonaal (19,44) → (20,45) → (21,46). Nu stopt hij en ligt de rode bies (21,45) direct op de crème.

**R6. Klont zwart tussen de nabije voorpoot en de gouden ruche** (4 px). Nu is het zwart daar 2–3 px breed. Laat 1 px `k` staan voor de poot, en geef de ruche aan haar lichte linkerkant haar eigen omlijning:
- (34,42), (34,43), (34,44), (33,45): `k`1 → `d`5

**R7. Inkepingen in de omtrek** (2 px alpha).
- (36,26): `.`0 → `k`1. Dat is een putje in de rugcontour tussen cape (35,26) en pak (37,26).
- (50,42): `.`0 → `k`1. Dat is een inkeping rechts in de rok tussen (50,41) en (50,43).

Totaal: **28 px**, waarvan 3 alpha (+3 px: (31,52), (36,26), (50,42)). Lever het resultaat op met een pixeldiff die laat zien dat er buiten deze 28 px niets veranderd is. Raak de verre achterpoot (x32–41, y46–58), het oog en de bombín niet aan.

## 4. Voor Jordi (geen fout, ontwerp of silhouet)
- **Banden die om de poot buigen:** de windsels zijn op beide poten even netjes, maar de banden zijn kaarsrecht. Bij Entei buigen de ringen. Dat kan als aparte kleine ronde (±25–30 px), als Jordi het wil zien.
- **Knie/hak van de voorpoten en de nabije achterpoot:** de flanken zijn recht, en dat komt uit het bevroren silhouet W3. Jordi noemde de poten eerder "puur controle en afwerking".
- **Formaat:** 1403 px = 1,18× fase 2 (1184), kleiner dan Tauros (1589) en Entei (2011). Het komt uit silhouet A (kop 1,25×, lijf ±7 % kleiner), dat Jordi koos.
- **Aguayo-halsband (y30–33):** het patroon is druk. Op 1× leest het als een bonte band met pompons, op 8× als losse kleurpixels. Het is ontwerp en geen fout.
- **Verre achterpoot:** in orde. De enige noot is (35,58), een `d`-pixel in de zwarte onderrand van de hoef. Op 1× is die onzichtbaar, en hij blijft staan.

## Samenvatting
- Oordeel: **AF NA KLEINE REPARATIES**: 7 punten, 28 px (3 alpha).
- Techniek: 64×64, P, index 0 transparant, 16 kleuren, één component, 0 open randen.
- Poten: de nabije achterpoot en de verre achterpoot zijn PASS. De nabije voorpoot faalt op randen en hoef (R1, R4, R6). De verre voorpoot faalt op volume, zwart aan de lichtkant, hoef en zoom (R2, R3, R4, R5). De windsels zijn even netjes en hebben gouden manchetten, maar de banden buigen niet (voor Jordi).
