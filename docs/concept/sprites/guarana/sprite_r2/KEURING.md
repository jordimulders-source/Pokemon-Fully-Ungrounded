# Keuring guaraná fase 1, ronde 2 (verse keurder, 25 nov)

Getoetst: alleen (1) trouw aan `model.png` (verkleind naar 44×37, BOX) en (2) Gen 3-techniek, naast `bellsprout/weepinbell/oddish/hoppip/ekans` (`anim_front_gba` + `normal_gba.pal`) en de maatstaf-sprites. Eerst blind op 8×, daarna gemeten. Coördinaten = spritepixels (x,y) in het 64×64-vel.

## Blind oordeel (8× en 1×)
Rank, krullen en silhouet lezen goed en zijn trouw. De tros leest op 1× als één rode, versplinterde massa met hoekige facetten in plaats van zeven ronde vruchtjes met elk een glimlicht, zoals het model. In de hoofdversie zijn de ogen te gebroken om direct als ogen te lezen. Hoppip (rode bol, één vloeiende sikkel) laat zien hoe rood volume in Gen 3 hoort te werken.

## Per onderdeel

**Tros/vruchten**
- Lijkt op: omtrek, 7 vruchten op de modelplekken, puntjes op de tippen (20,15), (10,27), (16,36), (27,19). Selout (2) bovenlangs, zwart rechts/onder: correct.
- Wijkt af in:
  - **Linkervrucht (x 11–17, y 24–27) heeft geen hooglicht**: effen idx 4, geen volume. Het model heeft daar linksboven een duidelijke glimplek. Reparatie: neem de lichte plek over uit het model (2–3 px idx 5 rond (13–14,25)) en een sikkel idx 3 langs de onderkant.
  - **Rechte lijn rij 28, x 12–17 (idx 2, 6 px horizontaal)**: in het model is dit de gebogen onderkant van de linker- en de middenvrucht (twee bogen, geen streep). Reparatie: neem de grens over uit het model als twee bogen (de lijn per vrucht 1 px laten zakken naar de randen).
  - **Middenonder-vrucht (x 21–23, y 29–33)**: verticale banden: idx 2 in kolom 22 (y 29–32) naast idx 3 in kolom 23 (y 29–32) en kolom 21 (y 30–33), plus rij 32 idx 3 x 23–27. Dat zijn rechte banden zonder hooglicht. Reparatie: neem de vulling over uit het model (licht linksboven, schaduw als sikkel rechtsonder) en zet de lijn op de modelgrens.
  - Kolom 16 idx 3 y 20–23 (4 px recht verticaal) links van het bovenoog: leest als streep. Model: donkere ooglid-/vruchtgrens, gebogen. Overnemen als boog.
  - Losse ruis: idx 3 (28,25), idx 4 (27,27) en (28,29). Opgaan in de buurtint.
- Hooglichten nu: bovenvrucht, rechtervrucht, middenvrucht, rechtsondervrucht en oogvrucht linksonder. Bij die laatste ((18–19,32–33) idx 5) plakt het hooglicht tegen het oogwit, zodat wit en roze in elkaar overlopen. Reparatie: 1 px van het wit los zetten of naar de modelplek verschuiven.

**Ogen**
- Hoofdversie: positie en richting volgen het model (pupil boven links, rechts rechts, onder links), maar het **oogwit is versplinterd in 6 stukjes < 3 px**: (18–19,19), (17,20–21), (18,22), (29,22–23), (16,30), (15,31). Een oog moet één wit vlak rond een pupil zijn. **Rechteroog**: pupil (30,22–23) ligt tegen de zwarte buitenlijn, dus wit + pupil + lijn worden één streep. Volgens SPRITE_KERN ("ogen pixel voor pixel van een echte sprite") is dit niet goed genoeg. Reparatie: neem per oog het modeloog over als één aaneengesloten wit vlak met pupil en een zwarte omlijning zoals in het model; lukt dat op 4 px niet, neem dan een klein Gen 3-oog 1-op-1 over (Weepinbell-variant, of een kleiner oog zoals dat van Oddish/Ekans).
- Variant (Weepinbell-ogen): leest op 1× duidelijk als drie starende ogen en is technisch schoon (geen witfragmenten). **Wijkt wel af van het model:** de ogen zijn ±7 px tegen ±4–5 px in het model en bedekken bijna drie van de zeven vruchten, zodat de tros meer "ogen" dan "vruchten" wordt (hooglichten dalen van 6 naar 3 stukken). Of dat mag, is Jordi's keuze (SPEC: "ogen groter maken" is een voorstel van Claude, nog niet beslist). Nog een detail: bij het rechteroog is de rechterrand 1 px naar binnen geschoven (2 wit→zwart), wat zichtbaar is als een afgeplatte rechterkant.

**Rank**
- Lijkt op: S-/9-vorm, dikte en gat in de krul precies als het model. Volume is goed: hooglicht idx 9 volgt de buitenbocht linksboven, schaduw idx 7 binnen/rechts, gebogen grenzen. Hals (x 23–29, y 33–41) als cilinder met verticale tinten, wat bij een rechte steel klopt (Bellsprout doet het ook zo).
- Wijkt af in: de onderrand waar de krullen aanhechten (rij 45–46, x 28–41) is een rommelig 7/8/9-patroon met losse pixels: idx 9 (31,46–47), idx 7 (23,46), idx 7 (47,45), (48,46), idx 8 (52,46). Reparatie: neem de onderrand over uit het model (doorlopende schaduwsikkel idx 7 langs de onderkant, aanhechtingen alleen als lijn op de modelplek) en laat de losse pixels opgaan in de buurtint.

**Krullen**
- Lijkt op: vijf krullen op de modelplekken; de belijning naar Bellsprout (1 px eigen donkergroen, zwart alleen aan de schaduwkant) klopt.
- Wijkt af in: de twee onderste krullen (x 26–31, y 48–51 en x 39–46, y 48–51) lezen als hoekige lusjes/blokken met een wit gaatje, terwijl het model spiraaltjes toont. Losse pixels idx 8 (19,43), (18,44), (44,49–50) en idx 7 (22,48). Reparatie: neem de krullijn opnieuw over uit het model als doorlopende 1-px-spiraal (diagonale stappen in plaats van rechthoek) en zet de losse pixels in de lijntint.
- Afwijkingen kleiner dan 64 px kan tonen (spiraaltje in de linkerkrul) tellen niet.

**Blad** (x 48–52, y 25–29)
- Lijkt op: plek, richting (punt rechtsboven) en de donkerdere tint dan de rank.
- Wijkt af in: geen lichte/donkere helft zoals het model (nerf). Losse idx 7 (49,28) en idx 8 (48,27). Reparatie (klein): neem de twee helften over uit het model (links idx 7, rechts idx 6) en laat de losse pixels daarin opgaan.

**Belijning**
- Buitenlijn 1 px, zwart rechts/onder, selout (rood 2 / groen 6) links/boven. Nergens zwart en selout om en om op dezelfde rand gevonden. Binnenlijnen in de tros in eigen donkere tint (2): goed. Hierboven al genoemd: de rechte stukken rij 28 en kolom 16/22.
- Zwart 16,3 % (variant 18 %), binnen de bandbreedte van Gen 3 (Bellsprout 19 %, Ekans 14 %).

**Palet**
- 10 kleuren + transparant. Rood: 3 tinten (3/4/5) + lijn 2; groen: 3 tinten (7/8/9) + selout 6; wit, zwart. ≤ 3 tinten per groep: in orde. Helderheidsstappen rood 56/91/120/163 en groen 82/110/137/164 (±27–43): contrast in orde, vergelijkbaar met Hoppip/Bellsprout.

## Oordeel
- **`guarana_r2.png` (hoofdversie): BIJNA.** Silhouet, rank en palet zijn trouw en Gen 3. De tros mist volume in 2 van de 7 vruchten en heeft rechte lijnen (rij 28, kolom 16/22). Het oogwit is versplinterd en het rechteroog smelt in de rand. Na de reparaties hieronder: PASS.
- **`r2_ogen_groter.png`: BIJNA.** Technisch beter (ogen schoon en leesbaar), maar op eis 1 wijkt hij af: de ogen zijn ±1,5× zo groot als in het model en verdringen de vruchten. Die keuze ligt bij Jordi. Dezelfde reparaties aan tros, rank, krullen en blad gelden ook hier.

## Top-reparaties (allemaal "neem over uit het model")
1. Ogen hoofdversie: per oog één aaneengesloten wit vlak + pupil + zwarte rand zoals in het model; pupil van het rechteroog los van de buitenlijn (30,22–23).
2. Linkervrucht (11–17, 24–27): hooglicht linksboven + sikkel onder uit het model.
3. Rechte lijnen rij 28 x 12–17, kolom 22 y 29–32, kolom 16 y 20–23: vervangen door de gebogen vruchtgrenzen uit het model; middenondervrucht vullen met licht/sikkel zoals het model.
4. Ruis weg: rood (28,25), (27,27), (28,29); groen (31,46–47), (23,46), (47,45), (48,46), (52,46), (19,43), (18,44), (44,49–50), (22,48), (49,28), (48,27).
5. Onderste twee krullen als doorlopende spiraallijn uit het model in plaats van hoekige lusjes.
