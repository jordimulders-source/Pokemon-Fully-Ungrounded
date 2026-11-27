# Regionale Staryu (koekje) ronde 3: eindkeuring Dragonfly Cave (27 nov)

**Oordeel: PASS** (na de wijzigingen hieronder). Het gaat alleen om uitvoering, er is niets herontworpen. Silhouet alpha-diff 0 (assert in `bouw.py`). Er zijn 13 pixels gewijzigd ten opzichte van r2 en het palet is op 2 indexen aangepast. Er is niets gladgestreken: de barstjes, de lichte deegplukjes, de chips en de juweelstrepen zijn pixel voor pixel gelijk aan r2.

Bestanden: `staryu_r3.png` (64×64, P, transparency 0, 14 kleuren), `bouw.py` (r2 → r3, elke pixel met een assert op de oude waarde), `vel.py` → `vel.png` (r3 | r2 | model op schaal, 8×; daaronder 1× + 2× op wit en donker: r3, r2, model, Gen 3 Staryu, Taillow, Skinguin, Dundragoon, Zapacha, Princadee).
Bouwen: `cd staryu_regional/staryu && python3 sprite_r3/bouw.py && python3 sprite_r3/vel.py`.

## Toegepaste gidsregels (`dragonflycave_spriting_guide.txt`)
- r. 96–97: "The 'outline shadows' are always black (or ever-so-slightly off-black)". Zwart staat alleen aan de schaduwkant van de buitenlijn.
- r. 421–423: "we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide."
- r. 452–456: "Put some of the shadow/outline highlight color on the outlines in the very most highlighted parts, trying to keep the overall quantity of this color similar to how it is in the R/S sprite. Again, place pixels of the outline highlight color on the inside of the outline rather than the outside."
- r. 117 (regel 4): "The outlines must be reasonably dark". De selout heeft L 91, de outline base van Gen 3 Staryu L 90.

## (a) Schaduw/volume: gemeten, geen pixelwijziging
- Per arm komt het licht linksboven en ligt de sikkel rechtsonder, allemaal uit de modelhelderheid (r1/r2-reductie). Gemeten op r3 voor deegpixels binnen 3 px van de buitenlijn:
  - aan de selout-kant (licht): 47 % licht, 36 % midden, 15 % schaduw;
  - aan de zwarte kant: 66 % schaduw, 33 % midden, **0 % licht**.
  Het volume heeft dus één richting en er is geen pillow shading.
- De sikkel wisselt van breedte en volgt het model: rechterarm onder 2→3→2 px (model 124–136 tegen rand ±90), rechterbeen rechts 1 px (model 124) en onder breed (model 113–128), linkerarm onder 2 px (model 112–130). De sikkel loopt taps uit naar de armtippen. Er zijn geen handverzonnen rechte banden: alle grenzen komen uit de reductie.
- Barstjes (d) en lichte plukjes (l) zijn ongewijzigd (verboden om weg te poetsen).

## (b) Belijning: 12 px
- **Om en om (1 px):** de bovenrand van de rechterarm liep s s s s s **K** s s s K. (46,25) K → selout 2 (model gem. 176, licht). De buitenlijn heeft nu per overgang precies één wissel zwart/selout (trace: 4 wissels K↔s, op de toppen en inkepingen, geen afwisseling).
- **Outline highlights (10 px, s → d)** op de lichtste lijnpixels volgens het model (gem. ≥ 165). De binnenbuur is licht deeg en de pixels liggen ≥ 2 px van zwart, net als Gen 3 Staryu (tint 8 op zijn lichte lijn, ±10 px) en Gnomad r10:
  - bovenarm links (28,16), (27,17), (27,18): model 179/169/184;
  - linkerarm boven (14,26), (15,25), (16,25): model 178/177/170;
  - rechterarm boven (44,25), (45,25): model 168/177;
  - linkerbeen links (17,45), (17,46): model 180/183.
- **Chiprand 1 px (2 px):** de chip rechts van het juweel had een 2×2-blok rand (38–39, 35–36). (38,35), (39,35) gaan van 6 → 7 (chipmidden). De boog loopt nu rechts (40,33–35) en onder (38–40,36). De chipvorm blijft gelijk (het model loopt tot rij 36, gem. 66/66/95).
- **Gemeten hoe Gen 3 kleine ronde donkere onderdelen omlijnt:**
  - Girafarig-vlekken: vlak donker, geen lijn;
  - Sudowoodo-vlekken: licht boven, donker onder, geen ring;
  - Pikachu-wangen: links een ring in de donkerste eigen tint, rechts alleen een boog rechtsonder.
  
  Onze chips (rand 6 = donkerste eigen tint als boog rechtsonder, glans linksboven, geen zwart) vallen daarbinnen. Waar het model de chip ook boven/rechts donker heeft (gem. < 90), is dat gebleven.
- **Juweel:** de ring loopt rondom in de eigen tinten, met 10 linksboven (outline highlight) en 9 vanaf linksonder via onder naar rechts. Elke kant heeft één wissel. Er is geen zwart, er zijn geen 2×2-blokken en de ring is 1 px. Ongewijzigd.
- Controle: geen binnen-zwart, geen lichte kleur op de buitenrand, geen losse zwarte pixels, geen 2×2-blokken zwart/selout/chiprand/juweelrand meer. De enige selout binnen het silhouet is (20,36): de naad uit de inkeping (keuring r1).

## (c) Kleurtinten: palet, 2 indexen
- Schaduw 3: (200,120,48) → **(198,112,50)**, hue 28° → 25° (modelschaduw (185,99,39) = 25°).
- Selout 2: (150,80,32) → **(146,74,34)**, hue 24° → 21°.
- Het deeg loopt nu van licht (244,198,118) h 38° via midden (228,160,72) h 34° en schaduw h 25° naar selout h 21°. De schaduw is roder bruin en het licht geler (hue shift). Ter vergelijking Zapacha: 37/31/22/21°.
- Helderheid L 203 / 170 / 131 / 91, dus stappen van 33 / 39 / 40 (Taillow ±30–40, Gen 3 Staryu 42/50/42).
- Per groep ≤ 3 tinten + lijn: deeg l/m/d + selout, chip 7/8 + rand 6, juweel 10/11/12 + glans 13 + rand 9 (zoals Gen 3 Staryu: 3 rodetinten + glans).

## Gecontroleerd en zo gelaten
- Op de bovenarm wisselt Gen 3 Staryu zwart en outline base om en om. Dat nemen we niet over (onze regel: nooit om en om).
- Chip 4 heeft rechtsonder een L-hoekje van 3 randpixels, (19,28), (20,28), (19,29). Dat volgt het model (gem. 30/48/99) en is een normale trapstap. Het is niet aangepast.

## Ter info voor Jordi (geen ontwerpvragen open)
- Geen.
