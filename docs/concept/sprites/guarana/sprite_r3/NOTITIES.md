# Guaraná fase 1, ronde 3: reparaties uit `sprite_r2/KEURING.md`, silhouet bevroren

Bestanden: `guarana_r3.png` (hoofdversie), `r3_ogen_groter.png` (Weepinbell-ogen), `kaal.png` (= r1/r2-kaal), `vel.png` (r3 | r2 | model 8×, close-ups 12×, 1× op vier achtergronden), `vel_ogen_groter.png`, `varianten.png` (r3, r3-ogen, r2, r2-ogen; 8× en 1× op wit/crème/donker), `bouw.py` (= r2-pijplijn + r3-wijzigingen; zonder-puntjes werkt nog via `VARIANT=zonder_puntjes`).
Silhouet: alpha-diff 0 t.o.v. r1 voor beide versies (assert + controle), 809 px, 44×37.

## Wat er veranderd is
1. **Ogen hoofdversie.** Op modelmaat (wit ±4 px rond een 2×2-pupil) hangt het oogwit alleen diagonaal samen; dat kan op deze maat niet één vlak worden (r2: 6 stukjes; een Huntail-oog, eerst geprobeerd, gaf ook 2 stukjes per oog).
   - Daarom per oog het **oog van Psyduck** 1-op-1 (`graphics/pokemon/psyduck/anim_front_gba.png`, x21–25 y22–25): wit 5×4 met afgeronde hoeken, 1-px pupil boven-midden. Het wit is één samenhangend vlak (3× 15 px).
   - Psyducks oogrand (eigen donkergeel) wordt rechts/onder zwart (zoals de modeloogrand) en links/boven onze donkerrode lijntint (zelfde rolvertaling als het Weepinbell-ooglid).
   - Het oog is gevonden met een zoekscript over alle _gba-sprites: zwarte pupil met aan alle kanten wit, en een omgeving die geen wit lichaam is. Kandidaten: Jynx, Smeargle, Krabby, Psyduck, Kingler. Psyduck past qua maat (5×4) het best bij de modelogen.
   - Plaatsing: pupil op de modelpupil: (18,20), (27,22), (17,30). Pupil rechteroog staat 2 px van de buitenlijn (wit ertussen).
   - Variant: Weepinbell-ogen ongewijzigd (oogwit 17/15/17 px).
2. **Linkervrucht.** Hooglicht (13–14,24–25) komt nu uit het aandeel lichte modelpixels per spritepixel (≥ 30 % licht → licht) in plaats van het gemiddelde, dat kleine glimplekken wegmiddelde. Sikkel onderlangs (13–16,27) en (16,26) in schaduwtint, gelezen op het model (donkere onderkant van de vrucht).
3. **Rechte lijnen:**
   - **Rij 28:** loopt door tot x15 en buigt dan via (16,27) en (17,26) omhoog naar de verticale modelgrens (17,24–25). (16–17,28) wordt de modelschaduw van de oogvrucht.
   - **Kolom 23 (y29–32):** schaduw wordt middenrood (model is daar midden), zodat er geen band schaduw–lijn–schaduw meer is. (24,31) idem, rij 32 begint nu op x24 (sikkel rechtsonder).
   - **Kolom 16 (y20–23):** valt nu grotendeels onder de nieuwe ooglijn links.
   - **Kolom 22 (y29–32):** de lijn zelf staat er nog. Het model heeft hier een bijna rechte, steile grens; ik heb hem niet krommer gemaakt dan het model.
4. **Ruis:** rood (27,27) is schaduw. (28,25) en (28,29) zijn nu oogrand of schaduwrand. Groen: (19,43), (18,44), (44,49–50), (22,48) zijn lijntint; (31,46–47), (23,46), (47,45), (48,46), (52,46) zijn de meest voorkomende groene buurtint.
5. **Krullen en blad:**
   - **Krul onder links:** rij 50 (x27–29) is weer groene streng (schaduwgroen). In het model is rij 50 de streng en rij 51 de onderrand.
   - **Rechterkrul:** (44,49–50) in lijntint. Een echte doorlopende spiraal kan binnen het bevroren silhouet niet: het gaatje is 1 px en het silhouet heeft blokhoeken.
   - **Blad:** lichte helft linksboven (schaduwgroen 7: (49,26), (50,26), (48,27), (49,27)), donkere helft rechtsonder (lijngroen 6).
   - **Oogvrucht linksonder:** hooglicht (19,33–34), gescheiden van het oogwit door de zwarte oogrand.

## Metingen
| | hoofdversie r3 | ogen groter r3 |
|---|---|---|
| zwart totaal | 16,7 % | 18,0 % |
| zwart tros / rank / krullen | 20 / 13 / 20 % | 24 / 13 / 20 % |
| anders dan kaal | 303 px | 309 px |
| per zone t.o.v. kaal: tros+ogen / rank / krullen / blad | 156 / 51 / 79 / 17 | 162 / 51 / 79 / 17 |
| anders dan r2 | 87 px | 37 px |
| zwart alleen aan de lichtkant | 0 | 0 |

Controle: geen lichte kleur op de buitenrand. "Losse zwarte pixels" (18,20), (27,22), (17,30) zijn de 1-px pupillen.

## Zwakke punten (eerlijk)
- **Ogen hoofdversie:** Psyduck-ogen zijn een Gen 3-oog, niet het modeloog. De pupil is 1 px (model ±2×2) en staat boven-midden. Leest op 1× als drie starende ogen; Jordi moet zien of dat het model trouw genoeg is.
- **Kolom 22 (y29–32):** blijft een rechte lijn zoals het model.
- **Krullen:** de onderste twee blijven lusjes binnen het blokkige silhouet. Ronder kan alleen door het silhouet te veranderen (bevroren).
- **Correctielaag:** de r3-reparaties zijn een lijst pixelwaarden in `bouw.py` (stap 6), elk met de modelreden erbij. Het zijn geen nieuwe vormen, maar wel per pixel gezet.
