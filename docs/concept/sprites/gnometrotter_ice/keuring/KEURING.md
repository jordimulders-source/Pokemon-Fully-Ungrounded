# Keuring Gnometrotter Ice, zelfde pose (A) en hybride (B), 23 nov (verse eindkeurder)

Gekeurd:
- **A** `sprite_r2/gnometrotter_ice_gatdicht.png` tegen model `r3/gemini_r3_lijf.png`
- **B** `sprite_hybride/gnometrotter_ice_hybride_gatdicht.png` tegen model `hybride/model_hybride.png`

Maatstaf: Rock `gnometrotter_rock/sprite_r4/` (PASS) en Gnomad `gnomad/af/gnomad.png`. Niet afgekeurd zijn de afgesproken afwijkingen: het gat bij de mutspunt is dicht en de oogstrook is dicht.
Eigen beelden in deze map: `vgl8_A/B.png` (sprite | model op schaal | Rock r4, 8×), `vgl1x3_A/B.png` (sprite | model | Rock | Gnomad, op 1× en 3× vergroot, licht/donker), `z_kop_*`, `z_onder_*`, `zbaard_A.png`, `zrechts_A.png`, `zlijf_B.png`, `zbenen_B.png`, `zmodel_baardonder_A/B.png` (raster met rode lijnen elke 5 px). Gemeten met `lum.py` (modelhelderheid per spritepixel, gemiddelde en p15) en `kaart.py` (dichtstbijzijnde paletkleur in het model per spritepixel). Paletluminantie: 2 = 85, 3 = 153, C = 188, D = 225, E = 248; 9 = 97, A = 134, B = 173.

## Dragonfly Cave-omlijning (getoetst tegen de gids)
Gids r. 80–170: *"The 'outline shadows' are always black (or ever-so-slightly off-black) on Pokémon sprites"*, *"The outline base and outline highlight colors are also colors ... you must also recolor the outlines"*, *"The outlines must be reasonably dark."* Gids r. 340–470: *"we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide"*, *"lighter pixels on the inside of the outline are a far better idea"*, *"place pixels of the outline highlight color on the inside of the outline rather than the outside."*

Uitkomst (A en B gelijk, behalve B punt 1). Muts, rugkam, haar L/R, neus, lijf, arm L, vuist, riem, benen en zolen doen het zoals Rock r4 en Gnomad: base 2/6/9 aan de lichtkant, zwart rechts en onder, binnenlijnen in eigen donkere tint, 1 px, geen lichte kleur op de buitenrand. Afwijkingen:
- **Stok, linkerrand:** zwart en 2 wisselen elkaar af ((5,37), (5,41), (6,42), (6,49), (7,50) zijn 1, de rest 2). Rock r4 heeft hier na de keuring overal 2. SPRITE_KERN zegt: "nooit zwart en ... om en om op één rand".
- **Hand R, schaduwkant:** de rechter- en onderrand zijn 6/7. Rock r4 sluit die na keuring r3 (punt 2) in zwart.
- **B: de rechterrand van de baard is op rij 29–36 weg** (zie B punt 1). Daar staat een open rand: licht ijs grenst direct aan lichtroze.

---

## A. Ice, zelfde pose: **BIJNA**

**Op het oog (eerst):** op 1× leest A als het model. Je ziet de ijsmuts met omgevallen punt, de rugkristallen, haar L en R, de neus, de witte baard, het roze lijf met de schouderovaal, de vuist met de ijspegelstok, hand R, de witte riem met gesp, de blauwe dijen met lichte voetballen en de witte zolen. Silhouet en maat zijn gelijk aan Rock r4. Volume is goed: muts 5 → 4 → 3, lijf F/8/7 met een sikkel rechts, dijen B/A/9 en voetballen. Er is niets toegevoegd.

**IJspegelstok:** goed. De breedte volgt het model: 6 px op rij 37–43, 4 px op rij 44–49 en 3 px op rij 50–56, met de punt op (7–8,56). Het model meet hier 6/4/3 met de punt op (7–8,56). Licht links (5), midden 4, schaduw 3. Alleen de linkerrand is fout (zie punt 4).

**IJspegelbaard: leest nog niet als losse hangende pegels zoals in het model.** Hij leest als een wit blok met drie gelijke verticale strepen, een "radiator". Op rij 25–35 staat elke rij precies `C E D D` met een periode van 4 px. Het model heeft dat niet:
- Links (x 18–23) is het model één brede, lichte pegelmassa (gem. 190–240) **zonder spleet op x 20** tot rij 33.
- De duidelijkste donkere spleet zit op **x 24** vanaf rij 29 (gem. 172–181, p15 103–137).
- De **rechterhelft (x 26–30) is de schaduwkant** (gem. 130–190). In de sprite staat daar juist de lichtste tint E (x 29).
- Er hangt een pegel **over de riem tot op de linkerdij** (x 19–21, y 43–46, gem. 197–221). In de sprite houdt de baard bij de riem op.

### Reparaties A (neem over uit het model; belangrijkste eerst)
1. **Baard: tinten uit het model (schaduwkant en spleten).** Het silhouet blijft gelijk.
   - x 26–28 en x 30, rij 26–35: D → C (model 140–190). x 25, rij 26–28: E → C (model 144–154).
   - x 29, rij 25–30: E → C. x 29, rij 31–34: E → 3 (model 130–143).
   - x 24, rij 29–35: C → 3 (model gem. 172–181, p15 103–137). x 24, rij 25–28 blijft D (model 205–231).
   - x 20, rij 27–32: C → D (model 191–224; daar zit geen spleet).

   Daarmee is de linkerhelft licht, de rechterhelft schaduw, en de spleten zitten onregelmatig zoals in het model.
2. **Baard: de roze "notch" (20,34) en (20,35) (index 7) → 3.** Het model toont daar een donkere ijsspleet (gem. 170/129, p15 67–75) en geen lijf.
3. **Baard: de pegel over de riem naar de linkerdij.** Neem uit het model wit ijs over op x 19–21, y 43–46 (gem. 197–221). Licht links en midden in D, rechts C, punt op (20,46). Een rand in 2 (outline base) waar hij tegen het blauw ligt. Het zijn ±10 px binnen het bestaande silhouet.
4. **Stok, linkerrand één tint:** (5,37), (5,41), (6,42), (6,49) en (7,50) van 1 → 2, zoals Rock r4. Zwart blijft alleen rechts (x 9–10) en op de punt (rij 56).
5. **Hand R, outline shadow:** (61,37), (60,38), (60,39), (56–59,40), (57,41) en (58,41) → 1, zoals Rock r4 (hand R rechts en onder zwart). Boven en links blijft 6.

Niet aanpassen: silhouet, muts en het dichte gat, oogstrook, neus, haar L/R, schouderovaal, lijf, riem en gesp, dijen, voetballen, zolen.
Ter info (geen eis, gevolg van het dichte gat): het grote rugkristal (model x 45–50, y 8–22, eigen donkere omtrek) loopt nu over in de mutsvulling. Alleen (44–45,9) in 2 en de 3-naad op x 42–43 (rij 12–14) scheiden ze. Wil Jordi het gat dicht houden, dan kan later 2/3 op de linkerrand van het kristal (x 44, rij 10–15), uit het model.

Na 1–5 (±70 px, allemaal tint/lijn, silhouet 0) is A voor mij een **PASS**. Een diffcontrole volstaat.

---

## B. Ice hybride: **BIJNA**

**Op het oog (eerst):** op 1× leest B als het hybride model: hetzelfde figuur, met een gefacetteerd roze lijf en blauwe benen met ijsblokken. Buiten het lijf is B gelijk aan A (dus ook de punten A1–A5). De blokken lezen in het lijf, al zijn ze kleiner en drukker dan de grote facetten van het model. In de dijen en arm L is het naadwerk deels ruis/dambord geworden, waar het model egale blokken heeft. Volume in het lijf is aanwezig (F linksonder, 8 midden, 7 rechts). Dat het grote lichte facet rechtsboven (model x 41–47, y 22–27, F) in de sprite 8 is, valt onder "kleur naar Gen 3" en is geen eis.

### Reparaties B (neem over uit het model; belangrijkste eerst)
1. **Baardrand en pegelpixels herstellen (regressie).** Het hybride script overschreef 9 baardpixels met lijfkleur: (31,29), (31,30), (31,31), (31,32), (29,32) en (30,33) van 2 → F/8, (27,35) en (27,36) van 2 → 8, en (26,36) van D → 8. Het model heeft daar de baard van r3 (100 % gelijk, zie `hybride/RAPPORT.md`). Zet deze 9 px terug zoals in A. Nu staat er een open rand (ijs direct tegen lichtroze) en zweeft (30,32) D tussen roze.
2. **Baard, stok en hand R: dezelfde punten als A1–A5.** Daarbij geldt voor A3: in het hybride model is de pegel over de dij smaller, wit op x 20–21, y 44–45. Neem die modelpixels over.
3. **Arm L zonder dambord:** (13–17, 31–33) wisselt 6/8 om en om ((15,32) 8, (16,32) 6, (17,32) 8, (13,33) 8, (14,33) 6, (15,33) 8). Neem per rij één tint over, zoals A en het model het doen: bovenrij 6 (lijn), midden 8, onderrij 7.
4. **Rechterdij onderaan te donker:** (41–44,48) 9 → B (model 213/191/169/167). (47–49,48) 9 → A (model 137/138/89 → A, A, 9: laat (49,48) 9). (45–48,49) 9 → A (model 168/158/130/138). De naad dij/voet op rij 50 blijft.
5. **Linkerdij: losse pixels en dambord.**
   - (21–24,47) 9 → A (model 142–163).
   - Losse A-pixels (25,44), (26,45), (25,46) en B-pixels (22,42), (22,43), (20,47) opnemen in het omringende vlak, zoals het model meet. (25–26, 44–46) model 97–155, hier geldt de meerderheid van de buren. (22,42–43) valt samen met de pegel van punt 2/A3.
6. **Lijf: losse vlekjes < 3 px.** Neem 7 op (48,25), (49,26), (48,27), (40,26), (41,27), F op (40,25), (33,21), (29,32) (vervalt met punt 1) en 8 op (54,30) op in het facet eromheen. Het model heeft daar één facet. Naden (6) blijven alleen waar het model een naad van ≥ 3 px heeft.

Niet aanpassen: silhouet, alles buiten lijf/benen/armen dat gelijk is aan A, de facetnaden die ≥ 3 px doorlopen, voetballen, zolen.

Na 1–6 (±90 px, silhouet 0) is B voor mij een **PASS**. Een diffcontrole tegen deze lijst volstaat.
