# Keuring guaraná fase 1, ronde 3 (dezelfde keurder als r2, 25 nov)

Getoetst: alleen (1) trouw aan `model.png` (verkleind naar 44×37, BOX) en (2) Gen 3-techniek. Eerst op 7–16× bekeken naast het model en r2, daarna gemeten. Coördinaten = spritepixels (x,y) in het 64×64-vel. Silhouet: alpha-diff 0 t.o.v. r2 (gecontroleerd). Hoofdversie 87 px anders dan r2, variant 98 px.

## Wat de r2-punten opleverden

| r2-punt | r3 | oordeel |
|---|---|---|
| Oogwit versplinterd (hoofdversie) | Psyduck-oog 1-op-1, wit 3× 15 px aaneengesloten, rand rechts/onder zwart en links/boven lijnrood | **opgelost** (zie wel de kijkrichting hieronder) |
| Pupil rechteroog tegen de buitenlijn | pupil (27,22), wit ertussen | **opgelost** |
| Linkervrucht zonder hooglicht | hooglicht (14,24), (13,25) | **opgelost** |
| Rechte lijn rij 28 | nog steeds recht, nu x 12–19 (8 px) met een rechte hoek op kolom 17 (y 24–28). De bocht via (16,27)/(17,26) uit NOTITIES zit **niet** in de png: (16,27) en (17,27) zijn lijnrood 2 in een blok. **Wel** gemeten: het model heeft hier zelf een rechte lijn (lijndekking rij 28 x 13–19 41–96 %, kolom 17 y 23–27 34–66 %). | **trouw aan het model, telt niet als fout** |
| Kolom 22 recht | blijft; het model is daar ook steil en recht (lijndekking 47–78 %, x 22 y 29–33) | **akkoord** |
| Middenondervrucht in banden | kolom 23 is opgelost, maar **kolom 21 y 30–33 (idx 3, 4 px)** staat nog als schaduwband pal naast lijnkolom 22 | **deels** |
| Ruis | (27,27) en (28,29) zijn nog losse schaduwpixels; nieuw/gebleven: zie hieronder | **deels** |
| Hooglicht oogvrucht tegen het wit | (19,33–34), gescheiden door de zwarte oogrand | **opgelost** |
| Blad zonder helften | licht linksboven (7), donker rechtsonder (6) | **opgelost** |
| Krullen als lusjes | rij 50 x 27–29 weer streng; verder lusjes binnen het bevroren silhouet | **akkoord** (rondere spiraal kan alleen met een ander silhouet) |

## Per onderdeel (wat nog moet)

**Ogen (hoofdversie): technisch PASS, trouw = vraag voor Jordi**
- Leest op 1× als drie schone, starende ogen: één wit vlak, Gen 3-rand. Het formaat (wit 5×4) ligt dicht bij het model (±4–5 px).
- **Afwijking van het model:** de pupil is 1 px en staat boven-midden in elk oog op (18,20), (27,22) en (17,30). In het model is de pupil ±2×2 en kijkt het bovenoog naar links, het rechteroog naar rechts en het onderoog naar links. De ogen kijken nu alle drie omhoog en recht vooruit; de kijkrichting uit het model ("ogen die je volgen") is weg. Volgens SPRITE_KERN mag het gezicht afwijken als het een echt Gen 3-oog 1-op-1 is, dus dit is geen keurfout. Het is wél een afwijking in het belangrijkste onderdeel die Jordi moet zien. Leg hem drie versies voor: Psyduck-oog (r3), Weepinbell-oog (variant) en r2-modeloog.

**Ogen (variant):** ongewijzigd t.o.v. r2: de kijkrichting volgt het model, maar de ogen zijn ±1,5× zo groot (keuze voor Jordi).

**Tros (beide versies)**
- Lijkt op: 7 vruchten met elk een hooglicht, het lijnraster op de modelplekken en de puntjes.
- Nog doen:
  1. **Kolom 21 y 30–33, idx 3:** een verticale schaduwband pal naast lijnkolom 22. Reparatie: neem de vulling over uit het model (de zone links van de modellijn is daar midden/licht; lijndekking x 21 y 30–33 is 1–18 %), zodat alleen de lijn overblijft.
  2. **Sikkel linkervrucht (13–15,27), idx 3:** een rechte rij pal boven de lijn op rij 28, dus dubbele horizontale band. Reparatie: de schaduw uit het model laten oplopen naar links ((12,26) is lijnrood; laat (13,27) midden en houd (14–15,27) + (16,26)), zodat de sikkel een boog wordt in plaats van een streep.
  3. **Losse rode pixels:** idx 3 (27,27), (28,29), (16,26), (15–16,23) en (13–14,29); idx 4 (15,22) en (18,34). Elk laten opgaan in de buurtint, gelezen op het model. Voor (16,26) geldt dat alleen als hij niet bij de sikkel uit punt 2 hoort.

**Rank:** PASS. Volume en grenzen zijn goed, de onderrand is rustiger dan in r2 ((31,46–47) is weg).

**Krullen/blad:** PASS binnen het bevroren silhouet. Nog 4 losse groene pixels: idx 7 (47,45), (23,46), (48,46) en idx 8 (52,46). NOTITIES zegt dat die zijn omgezet, maar in de png staan ze er nog. Reparatie: zet ze in de buurtint (6 of 7) zoals in het model. De idx-6-stukjes van 1–2 px in de rank, zoals (33–34,29–32), zijn binnenlijnen en tellen niet als ruis.

**Belijning:** PASS. Zwart alleen rechts/onder (0 zwarte pixels aan alleen de lichtkant), selout links/boven, binnenlijnen in eigen tint. Zwart 16,7 % (variant 18,0 %).

**Palet:** PASS. Ongewijzigd: per groep 3 tinten + lijn, stappen ±27–43.

## Oordeel
- **`guarana_r3.png`: BIJNA, dicht bij PASS.** De grote r2-problemen (oogwit, rechteroog, linkervrucht) zijn opgelost. Er resten drie kleine reparaties: kolom 21, de sikkel op rij 27 en een handvol losse pixels. De kijkrichting van de Psyduck-ogen is geen keurfout, maar moet als keuze naar Jordi.
- **`r3_ogen_groter.png`: BIJNA.** Zelfde resterende punten aan tros en krullen; oogmaat blijft een keuze voor Jordi.

Na reparaties 1–3 + de groene ruis: PASS voor beide, zonder nieuwe keurronde op de rest (diff buiten die pixels = 0 laten bewijzen).
