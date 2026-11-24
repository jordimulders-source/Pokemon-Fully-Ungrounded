# Satelliet fase 1 – sprite r1 (maker)

Model: `../model/model_gekozen_natief.png` (99×99, bevroren). Vel: `vel.png`. Sprite: `sprite.png` (64×64, P-modus, 16 paletplekken, index 0 transparant, 10 kleuren in gebruik).

## Werkwijze (model overnemen, niets getekend)
1. `reduce.py`: achtergrond = floodfill vanaf de rand op bijna-wit (≥244), zodat het witte lijf binnen de omlijning blijft. Uniforme factor 59/75 = 0,787 (object 75×66 → **59×52**, x 2–60, y 6–57; onderkant rij 57). Elke modelpixel gaat naar de spritepixel waar zijn middelpunt in valt (1–4 modelpixels per spritepixel); regels: achtergrond bij >helft, zwart als er een zwarte modelpixel in zit (1-px-lijnen blijven 1 px en doorlopend), anders meerderheid per kleurgroep (teal > paars > lijf bij gelijkspel), binnen de groep vlakgemiddelde → dichtstbijzijnde tint. Uitvoer `kaal.npy`/`kaal.png` = kale reductie.
2. `fix.py`: alleen pixelreparaties op de kale reductie, elk met zone en reden; volledige lijst per pixel in `afwijkingen.txt`. Alpha-diff met de kale reductie: 1 px (zie A3).
3. Meten: `cel.py y0 y1 x0 x1 [npy]` (per spritepixel welke modelpixels erin vallen), `check.py` (tintclusters < 3 px, open randen), `view.py`/`vel.py`.

## Palet (kleur mag afwijken van het model; Gen 3-stappen)
| idx | kleur | helderheid | rol |
|---|---|---|---|
| 1 | (24,20,32) | 21 | omlijning schaduwkant, pupil |
| 2 D | (84,46,108) | 62 | selout lichtkant (model 100,57,120), bovenrand antennes/voetjes, buitenrand oogring links |
| 3 P | (118,70,150) | 89 | naad, antennes/voetjes midden, binnenring oog |
| 4 p | (168,118,202) | 137 | antennes/voetjes licht, oogring |
| 5 W | (255,255,255) | 255 | hooglicht bol |
| 6 w | (226,220,244) | 224 | basis bol |
| 7 l | (174,162,218) | 170 | schaduw bol (dieper dan model 163,154,196 → lavendel) |
| 8 m | (130,114,184) | 126 | diepe schaduw-sikkel (dieper dan model 137,130,178) |
| 9 | (56,128,140) | 108 | iris |
| 10 | (140,204,200) | 187 | iris licht linksboven (modeltint, geen glans) |

## Afwijkingen van de kale reductie per zone (132 px totaal)
| zone | px | wat |
|---|---|---|
| bol omlijning | 16 | lichtkant-selout uniform D (model heeft overal dezelfde 100,57,120, reductie gaf D/P door elkaar); (38,3) D→zwart zodat zwart/paars niet om en om gaat (vanaf rij 37 zwart); (40,4) AA-randje l→w |
| bol rand onder/rechts | 22 | model-reflectierand (163,137,194, viel in de paarsgroep) → lijftint l; dubbele binnenlijn onder (model P) → m; rechtsboven open rand dicht (17,29)→D, (17,28) p-ruis→w |
| naad | 30 | 11× naadpixel D/p → P (één tint, 1 px, geen zwart); 14× lichtpaarse band naast de naad (model q, 1 modelpx) → w, anders leest de naad dubbel; 5× band onder de naad (model qqqq) → l |
| oog | 20 | ringrand gesloten (27,7),(27,8),(27,13),(28,7)→P; (34,4),(35,4)→D; (36,15),(39,8)→zwart; wit gat in de ring (30,6)→p; binnenring (35,6)→D, (36,13),(37,11)→P; pupil rond 4×5: (33,7)→iris, (35,8) paars→iris, (32,8)→zwart; 5 AA-randjes l→w rond de ring |
| voet linksboven | 7 | bovenkant (lichtkant) zwart→D (12,19–21); open randen (13,18),(14,17)→D; onderrand (15,18) p→P; (12,23) lijftint→P |
| voet rechtsboven | 3 | open bovenrand (18,29–31)→D |
| antenne A1 (boven) | 9 | 8× open bovenrand P→D; (12,30) dubbele zwarte trap→P (anders 1 px kleur) |
| antenne A2 (rechtsboven) | 9 | 9× open bovenrand P→D |
| antenne A3 (midden) | 10 | 7× open bovenrand →D; (33,54) terug naar modelkleur p; **(32,54) D nieuw** |
| antenne A4 (onder) | 6 | open bovenrand →D (de automatische regel "P/p tegen transparant eronder/rechts → zwart" raakte niets) |

**Pixels die niet uit het model komen:** precies 1: (rij 32, kol 54) D, bovenrand van de middelste antenne 1 px verlengd zodat de antenne daar 2 px kleur houdt. Alle andere reparaties veranderen alleen de tint van een bestaande spritepixel (silhouet = kale reductie).

## Controles
- Antennes (kleur zonder D-bovenrand / met / totaal per kolom): A1 2–3 px kleur over de lengte, A2 2–3, A3 2–3, A4 2–3; alleen de punten (laatste 1–2 kolommen) lopen af naar 1 px kleur, zoals in het model. Totale dikte 3–5 px incl. omlijning.
- 4 antennes, 4 voetjes zoals in het model (middelste antenne zonder zichtbaar voetje).
- Geen open randen meer (`check.py`); geen glans in het oog.
- Oog op 12× naast het model: buitenrand D links / zwart rechtsonder, lichtpaarse ring, donkerder binnenring, iris teal met lichte tint linksboven, ronde zwarte pupil 4×5.

## Eigen zwakke punten / vragen
- **Lijf heeft 4 tinten** (W, w, l, m), de regel zegt ≤3 per kleurgroep. Het model heeft hooglicht, basis, schaduw en diepe schaduw; één samenvoegen kost het volume (W+w = vlak lichtvlak, l+m = geen sikkel). Ik heb het zo gelaten; Claude/keurder beslist.
- Stap w→l is 54 (groter dan 30–40), om de schaduwkant dieper te krijgen zoals gevraagd; met 4 tinten en een wit hooglicht gaat 30–40 overal niet.
- De lichte band naast de naad (rechts) en de schaduwband l/m zijn uit het model, maar lopen evenwijdig aan de rand (lichte banding rechts). Niet aangepast, omdat het de modelvorm is.
- Voet linksboven blijft een vrij platte paarse vorm, zoals in het model.
