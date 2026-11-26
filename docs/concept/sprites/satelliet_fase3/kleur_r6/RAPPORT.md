# Kleurronde r6 ruimtestation (25 nov)

Invoer: `../eindkeuring_r5/sprite.png`. Script: `kleur6.py` (alleen indexwissels en paletwaarden). Uitvoer: `sprite.png` (transparency=0), `sprite_8x.png`, `vel.png` (r5 | r6 | model verkleind, 8×; daaronder 1× en 2× naast fase 2, Magneton en Metagross (`anim_front_gba`), op licht en op donker).

- **Silhouet:** alpha-diff 0, er is geen vorm getekend.
- **Gewijzigde pixels:** 705 van de 1023 pixels hebben een andere kleur. 413 daarvan zijn indexwissels (zie hieronder), de rest is een paletverschuiving binnen dezelfde rol (paars, iris, binnenlijn).
- **Kleuren:** 14 inclusief transparant. Index 13 en 14 zijn vrij.

## Palet voor → na (L = helderheid)
| idx | r5 | r6 | rol |
|---|---|---|---|
| F | 250,248,252 (L249) | 248,248,252 (L248) | wit licht |
| E | 231,220,238 (L225) | → index 5 | |
| D | 209,198,221 (L204) | → index 5 | |
| 5 | 116,99,143 lila | **206,198,228 (L204)** | wit midden (oud E+D) |
| C | 186,175,205 (L182) | → index 4 | |
| B | 140,120,163 (L131) | → index 4 | |
| 4 | 84,74,112 | **150,138,186 (L147)** | wit schaduw (oud C+B; de oude 4 is opgesplitst, zie onder) |
| 3 | 63,52,90 | 60,48,96 (L57) | binnenlijn |
| 8 | 182,132,196 (L154) | 156,100,182 (L126) | paars licht |
| 7 | 150,104,168 | 116,70,142 (L92) | paars midden |
| 6 | 120,78,143 (L98) | 80,44,104 (L62) | paars donker |
| 9 / A | 52,100,102 / 80,160,158 | 38,104,110 / 86,182,174 | iris donker / licht |
| B (11) | | **58,52,104 (L60)** | paneelvak (nieuw) |
| C (12) | | **120,106,172 (L118)** | paneelrasterlijn (oud lila 5) |
| 1 / 2 | ongewijzigd | 24,19,36 / 41,38,69 | outline shadow / outline base |

## Wat er per onderdeel veranderde
- **Romp, buizen en bollen:** er waren 6 wittinten met stappen van 24/21/22/51 (F, E, D, C, B en 4). Nu zijn het er 3: licht 248, midden 204 en schaduw 147, met stappen van 44/57 in plaats van 24/21/22. De verdeling volgt de bestaande r5-indexen, dus de lichtval van het model: E en D werden midden, C en B werden schaduw. De oude donkere 4 (30 px) is per pixel bekeken. Waar het verkleinde model donker is (L<100, 15 px: naden en kragranden) werd het binnenlijn 3, de andere 15 px werden schaduw. De hue verschuift van wit naar lavendel naar blauwpaars. De bollen blijven rond, want de grenzen zijn niet verplaatst.
- **Kragen en banden (paars):** de 3 tinten zijn ongeveer 30 L donkerder en verzadigder gemaakt (126/92/62 in plaats van 154/122/98). Daardoor liggen ze duidelijk onder de witte schaduw (147) en lezen ze als paarse ringen in plaats van als pastel. De verdeling per pixel is ongewijzigd.
- **Panelen en masten:** in r5 was het vak dezelfde navy als de buitenlijn (index 2). Nu krijgt elke paneelpixel met 4 paneelburen het vak 58,52,104 (153 px), en de rand blijft navy aan de lichtkant en zwart aan de schaduwkant. De rasterlijn werd 120,106,172 (41 px, alleen waar ≥3 buren paneel zijn). De ene lila pixel in de romp (28,39) werd binnenlijn 3. **Ter info:** de vakken zijn even donker als in het model (L60, modelgemiddelde ≈70,63,100 met L66), maar wel blauwer, en de rasterlijn is helderder. Dat gaat iets richting fase 2. Ik heb geen tweede vaktint toegevoegd.
- **Ogen:** ring, iris en pupil staan op dezelfde plekken, zonder wit binnen de ring. De iris is iets helderder en de ring is mee donkerder geworden met de paarse ramp.
- **Belijning:** de buitenlijn is ongewijzigd (zwart aan de schaduwkant, navy aan de lichtkant). Er zijn geen zwarte pixels bijgekomen.

## Indexwissels per pixel (alles behalve paletverschuiving)
E→5 (108) · D→5 (3) · C→4 (89) · B→4 (3) · 2→11 (153, paneelvak) · 5→12 (41) · 5→3 (1) · 4→3 (15). Samen 413.

## Open
- Op 1× is r6 duidelijk scherper dan r5 (zie `vel.png`), maar hij blijft kleiner en luchtiger dan fase 2. Dat komt door de vorm en niet door de kleur.
- Er zijn 1–2 px kleurclusters gebleven in de kragen en de paneelrasterlijnen. Dat zijn dunne onderdelen op 64 px en het is geen ruis.
