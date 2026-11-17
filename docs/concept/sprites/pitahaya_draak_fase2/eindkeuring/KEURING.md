# Eindkeuring pitahaya-draak fase 2, `sprite_r9/pitahaya2_r9A.png` (verse keurder, 16 nov)

Gekeurd naast het model (`model/model.png`, natief raster 5,076, sprite = 3×-reductie, geo uit `sprite_r1/kaal_info.npz`: natief x = 2+3·sx, y = 3·(sy−13)) en Gen 3: Salamence, Lairon, Feraligatr, Croconaw, Totodile, Gyarados, Exploud, Swampert, Sceptile, Corsola, Lickitung en Skitty (pinkpaletten).
Eerst blind gekeken (1×/2×/8×), daarna gemeten. Bevroren en niet aangeraakt: de vier weggehaalde V-pixels (r7), de grijze gehemeltetint (r5/r6) en de roze V-rand (r9, Jordi's keuze).

**Hoofdvraag (1×, 2×):** leest als laag, gemeen reptiel met een wijd open bek vol vruchtvlees, roze schubbenrug met groene punten en een staartkrul: ja. Wat op 1× het meest stoort: de gloeiende lichtroze vlek in de mondhoek, de donkere, vlakke roze onderhelft, de donkere groene poten en de drie liniaalranden die Jordi noemt.

**Oordeel: FAIL.** Het model en het silhouet staan. Wat moet gebeuren is uitvoering (palet, tinten en een paar randpixels), samen ±60 px plus een paletronde. In `proef.py` → `proef_alles.png` heb ik de reparaties A, B en C en het palet als toets uitgevoerd (62 px). Dat is geen oplevering: de maker voert ze zelf uit en meldt de afwijkingen. D (volume) zit niet in de proef.

| Meting (`meet.py`) | r9A | Gen 3 (Feraligatr, Swampert, Salamence, Sceptile, Croconaw) |
|---|---|---|
| px / kleuren | 1218 / 13 | 1226–2446 / 13–15 |
| buitenrand zwart | 59 % | 56–64 % |
| zwart binnen de figuur | 8,0 % | 4,8–12,3 % |
| zwart/niet-zwart-wissels op de rand | 15 % | 9–18 % |
| 2×2-dambord | 7 | 6–54 |
| vlaktint (geen lijn/selout) op de buitenrand | **17 px** (15 G, 2 p) | 0–3 |
| helderheidsstappen roze d→r→p→P | **21** / 43 / 50 | Corsola 40/53/50, Skitty 47/28/25, Lickitung 54/32/25 |
| helderheidsstappen groen g→G→h→H | 29 / 29 / 29 | Sceptile 61/52/37 |
| gebruik lichtste tint | P 36 px (alleen kop), H 7 px | R/S gebruikt veel hooglicht (Dragonfly Cave §5) |

---

## A. Het roze in en om de bek (Jordi's vraag): FAIL
**Waarom werkt het niet?** In elke Gen 3-open bek (Totodile, Croconaw, Exploud, Gyarados) is de binnenkant **donker achterin en bovenin**, onder de bovenkaak, en **licht vooraan en onderin**. De opening heeft rondom één donkere rand. Bij r9A is dat op vijf punten omgekeerd of rommelig:
1. **De lichtste tint zit op de donkerste plek.** P (lichtroze) staat in een blok van 15 px in de mondhoek en op de verre lip: (18,44) (19,44) (18,45) (19,45) (20,45) (18,46) (19,46) (20,46) (18,47) en (16,48) (16,49) (17,49) (15,50) (16,50) (15,51). Daar, onder de bovenkaak, zet Exploud zijn donkerste mondtint (#582058) en Croconaw zijn donkerrood. Daardoor gloeit de mondhoek en leest de verre lip als een losse roze tong of wang naast het vruchtvlees.
2. **De lip is aan de lichtkant donker.** De voorlip links is r/d: (7,50–53) en (8,48) (8,49). De achterlip is P. Het licht valt van linksboven, dus het moet andersom.
3. **De onderkant van de kaak is het lichtst.** (9,54) p, (10,54) P en (11,54) P liggen op de onderrand vlak boven de zwarte lijn, en die rand kijkt naar beneden. Bij Exploud en Gyarados is de onderkant van de onderkaak donker.
4. **P is zalmkleurig.** Hue 348 tegen 340–342 voor r en p: het hooglicht schuift naar warm. Gen 3-roze schuift het hooglicht juist koeler (Corsola #f8a0c0 hue 338, Lickitung #ffbdde hue 330). Het lichtroze leest daardoor als een ander materiaal (vlees). Daarnaast scheelt P (helderheid 179) maar 11 met het grijze vruchtvlees w (190): op (15–16,48–51) lopen lip en vruchtvlees in elkaar over, dezelfde klacht als Jordi bij r3 had.
5. **De lipband is ongelijk dik:** 0 px links (vlees direct tegen de buitenlijn op (8,51) en (8,52)), 1 px onder en 3 px rechts. Het witte vlak lijkt daardoor naar links geschoven.

De **V-rand (9,44) (10,45) (11,46)** zelf is niet het probleem: hij is nu één tint met (10,47) en (9,48), zoals Jordi vroeg. Met het donkerdere palet (E) blijft hij los van het gehemelte. Laten staan.

**Reparatie A (23 px, getoetst in `proef_A.png`):**
- A1. Mondhoek en verre lip worden de basistint, met donker eronder:
  - P → p op (18,44) (19,44) (18,45) (19,45) (20,45) (18,46) (19,46) (20,46) (18,47).
  - P → p op (16,48) (16,49) (17,49) (15,50) (16,50) (15,51).
  - (17,45) p → r. Dat neemt het model over (model = r) en maakt de lijn onder de bovenlip (17,44–47) één doorlopende r.
  - Volgt Exploud en Croconaw: donker achterin.
- A2. Onderkant van de kaak in schaduw: (9,54) p → r, (10,54) P → r, (11,54) P → r.
- A3. Licht op de voorste lipbocht, die naar het licht kijkt: (9,53) en (10,53) p → P. Zo staat het in het model (modeltoon P). (8,50) P blijft. Daarna staat P alleen nog voorin-onder, nergens naast w.
- A4. Lipcontour in één tint: (8,48) en (8,49) d → r. Dan loopt de rand van de V tot (7,53) helemaal in r, en is de onderkant zwart (7,54) en (8,54).
- A5. Palet (0 px, zie E): P → #f8a0c0. Daarmee is P koeler en is het zalm weg.
- Ter info (niet gerepareerd, oud punt van Jordi): de bovenrand van de bek gaat K (9–13,43) → K (14–16,44) → K (17,43). Daarboven ligt r (14–16,43). De variant `r9A_achter` raakt dat.

## B. Rechte silhouetlijnen (Jordi): FAIL
Gemeten met de modeldekking per spritepixel (`dekking.py`: modelpixels van de 9 in het natieve blok) en de modelomtrek over de sprite (`overlay.py`).
- **B1. Rechterkant staart:** x=60 is 7 px kaarsrecht (rij 47–53). In het model bolt de staart op x=61 uit, met een dekking van 2, 3, 3 en 2/9 op rij 48–51. Reparatie (8 px):
  - (61,48) (61,49) (61,50) (61,51) worden K.
  - De oude lijnpixels (60,48–51) K → g, de donkerste groen-tint van de schaduwrand.
  - Randprofiel per rij: x 59, 59, 60, 61, 61, 61, 61, 60, 60, 59, oftewel segmenten 2-1-4-2-1: een ronde boog, zoals de staartkrul van Swampert en Salamence.
- **B2. Meest linkse poot:** de onderrand is één zwarte lijn van 9 px (x 9–17, rij 59) en de bovenrand een trap 1-1-1. Het model heeft daar drie tenen met teenlijnen op (12,58) (4/9 zwart) en (15,58) (5/9). In het model is de onderste rij geen lijn: G op x 10 en 13, donker op x 11–12 en 15–17. Reparatie (4 px):
  - (12,58) g → K: de teenlijn uit het model.
  - (12,59) en (15,59) K → transparant: een inkeping onder elke teenlijn.
  - (12,56) wordt g: een bolling op teen 1, modeldekking 2/9. Daarmee is de diagonaal geen 1-1-1 meer.
  - De onderrand wordt zo drie teenpunten (3, 2 en 2 px), zoals de voeten van Feraligatr en Swampert.
- **B3. Bovenkant van het hoofd:** rij 34 is gevuld van x 10 tot 24 (15 px, alleen het blad op (13–14,33) erboven). Het model daalt achter de wenkbrauw: de dekking is 9/9 tot x 17 en 6/9 op x 18–23, en daarna begint de nekschub (x 24+, 9/9). Reparatie (6 px):
  - (18,34) (19,34) (20,34) worden transparant.
  - (18,35) (19,35) (20,35) p → d (selout).
  - Er ontstaat een zadel van 1 px tussen wenkbrauw en nekschub. De voorkant (x 10–17) wordt door het blad gebroken.

## C. Belijning: FAIL (alleen kleine punten)
Goed: buitenlijn 1 px, zwart op de onderkant en rechts, binnenlijnen 8 % (Gen 3-band), randwissels 15 %.
- C1. **Vlaktint op de buitenrand** (open rand, 17 px), wordt selout:
  - G → g op (25,32) (26,32) (25,33) (27,33) (32,33): rugpunten.
  - G → g op (49,38) (48,39): rugpunt.
  - G → g op (51,43) (52,43) (57,43) (58,44): bovenkant staartkrul.
  - G → g op (10,58) en (12,57): teen.
  - G → g op (29,59) (28,60): middelste voet.
  - p → d op (31,34) (38,34): toppen van de rugplaten.
  - Zo doen Feraligatr en Salamence het: de punten hebben een donkere omlijning.
- C2. **Selout op de kopbovenrand wisselt van tint:** r, r, g, g, K, d, d, r, r, r, d. Maak (10,34) (11,34) (17,34) (9,35) r → d. Na B3 vallen (18,34) en (19,34) weg. Dan is de selout van de kop één tint d. De lip blijft r (A4).
- C3. Binnenlijnen zijn al taps en in vlaktint, behalve de teen- en pootoverlap: niets te doen.

## D. Schaduw en volume: FAIL
- D1. **Evenaar is een liniaal.** De grens p → r op het lijf loopt ±20 px recht horizontaal over rij 44/45 (x 28–48). Daarbinnen is de onderhelft een vlak r-blok van ±9×28 px zonder verloop. Bij Salamence en Shelgon volgt de schaduwsikkel de ronding: hoger naar achteren (rechts), lager waar het lijf naar de kijker bolt, met de donkerste tint alleen langs de onderrand. Reparatie, niet uit de hand: de gladgestreken luminantie van het model (σ ±1,5), alleen binnen het roze, als toonkaart met 4 tonen, zoals bij de spooktrein en fase 1. Daarmee de grens per plaat laten stappen (1 px per ±5 px), en d (na E donkerder) als sikkel van 1–2 px waar het lijf achter de dijen verdwijnt (rij 52–53, x 23–27 en x 38–41). De keel achter de kop (x 19–27, rij 42–53) blijft r: dat is slagschaduw van de kop.
- D2. **Geen hooglicht op het lijf.** P staat alleen op de kop; de rug heeft 0 px. Dragonfly Cave §5: R/S gebruikt veel hooglicht, en te weinig maakt de sprite donker. Voorstel: 2–4 px P aan de linkerbovenkant van elke rugplaat (x 26–31, 33–38 en 40–46, rij 35–38), binnen de r-naden. Let op: het model heeft daar maar 3 % P (45 van 1563 natieve px). Dit gaat dus verder dan het model en valt onder Jordi's "hard aan schaduwen en kleur werken". Laat het als variant naast de versie zonder zien.
- D3. **Groen heeft geen hooglicht** (H 7 px). De dijen van de middelste en rechterpoot hebben al een h-bol. Neem H over van de modelplekken (modeltoon H op (47,48–50) en (36,51)) en breid die uit tot een sikkel van 2–3 px linksboven op elke dij, zoals Salamence en Sceptile.
- D4. De nabije voorpoot is donker (G/g). Dat klopt met het model en met de slagschaduw van de kop. Niet lichter maken; na B2 lezen de tenen.
- Geen pillow shading, geen banding gevonden behalve D1.

## E. Kleur: FAIL (alleen paletwaarden, 0 px)
Goed: 13 kleuren (≤ 16), ≤ 3 tinten + lijn per groep, roze en groen complementair. Het groen schuift naar geel in het licht, zoals bij Gen 3.
- E1. **d → #681838.** De oude #712b37 heeft helderheid 65 en hue 349, een bruinig kastanje. De nieuwe heeft helderheid ±52 en hue ±330. Daarmee wordt d→r 34 in plaats van 21: twee lijntinten die bijna gelijk waren worden twee echte stappen, en de schaduw schuift koel naar paars (Dragonfly Cave §4, Exploud).
- E2. **P → #f8a0c0** (Corsola), helderheid ±190, hue 338: koeler en lichter. Plaats P nooit naast w (A3 zorgt daarvoor).
- E3. **Groen lichter en verder uit elkaar:** g #305830, G #4f8040, h #78a850, H #b0d068. Dat geeft helderheid ±72, 106, 144 en 187, stappen ±34, 38 en 43 in plaats van 29, 29 en 29. De poten lezen dan als volume in plaats van als donkere massa (vergelijk Sceptile, Feraligatr).
- r #b12854, p #e74e7b, zwart en grijs blijven. Na de paletronde nagaan of het roze roze blijft en niet lila wordt (spooktreinles). In de proef bleef het roze.

## F. Netheid: PASS met 6 kleine punten
Dambord 7 (Gen 3-band), losse lichte pixels alleen tanden en vlees. Losse G-pixels in de poten worden de meest voorkomende buurtint: (27,50) (28,51) (21,52) (40,52) (48,52) (47,53). De losse G's op de rugpunten zijn punttoppen en blijven.

## G. Dragonfly Cave-checklist (uitvoering): PASS behalve A6
- A1 (silhouet), A2 (open bek en rugschubben breken de omtrek), A3 (kop links, staartkrul rechts), A4 (lucht tussen de poten), A5 (niet symmetrisch): ok.
- A6 (geen rechte stukken): fout, dat is B1–B3.
- B2 (lange snuit, één oog), B6 (kop over het lijf), C1 (vier poten, de verre voorpoot donker achter de nabije), D1 (1218 px, fase 2) en E3 (zwart 8 %): ok.
- Ter info voor Jordi (ontwerp, niet gerepareerd): het vruchtvlees leest op 1× als een witte bek met stipjes en op 2× als pitahaya. De rug is druk door de groene punten met zwarte naden; dat is het model.

---

## Reparatielijst op prioriteit (voor de maker; alles "neem over uit het model" of "volg Gen 3-sprite X")
1. **A1–A4 bek-roze** (23 px): lijst hierboven. Proef: `proef_A.png`.
2. **Palet E1–E3** (0 px).
3. **B1 staart** (8 px), **B2 poot** (4 px), **B3 kop** (6 px).
4. **C1 en C2 randen** (21 px).
5. **D1 evenaar en d-sikkel** via de gladde modeltoonkaart. **D3 groen hooglicht.** **D2 rughooglicht** als variant voor Jordi.
6. **F** 6 losse pixels.

Asserts voor de maker: buiten de genoemde pixels en zones diff 0 met r9A; de bevroren bekpixels (r7-V, gehemelte, V-rand) ongewijzigd; silhouet alleen gewijzigd op de B-pixels. Daarna r9A en de nieuwe ronde op 1× en 2× naast elkaar leggen en eerst de vraag stellen: is dit beter?

## Bestanden
- `vel.png`: r9A op 8× met de zones omcirkeld, het model op dezelfde maat, de keurderproef op 8×, Salamence en Lairon, en alles op 1×/2×.
- `meet.py` (Gen 3-metingen), `dekking.py` (modeldekking per spritepixel), `overlay.py` (modelomtrek over de sprite), `modeltoon.py` (gemiddelde modelkleur per spritepixel), `zoom.py`, `proef.py` → `proef_A.png`, `proef_alles_oudpalet.png`, `proef_alles.png`, `vel.py`.
