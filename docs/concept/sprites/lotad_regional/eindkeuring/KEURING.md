# Eindkeuring Dragonfly Cave: gaucho-Lotad (25 nov)

Basis: `../sprite/r3/lotad_gaucho_oogG.png` (Jordi: "G"). Resultaat: `lotad_gaucho_e.png` (64×64, geïndexeerd, index 0 transparant), `lotad_gaucho_e_8x.png`, `vergelijk.png` (voor | na | model op 8×; 1× op licht en donker naast Lotad (Gen 3, `_gba`), Dundragoon, Skinguin, Zapacha en Princadee).
Scripts: `e1.py` (alle wijzigingen, per stap geteld), `meet.py` (modelhelderheid per spritepixel en materiaalkaart uit de kale reductie van r2), `clusters.py`, `controle.py`, `vel.py`, `uit.py`. Uitvoer: `e1_uitvoer.txt` en `controle_uitvoer.txt`.

Alleen uitvoering, geen herontwerp, niets hertekend. Elke tintkeuze voor schaduw komt uit de modelhelderheid (`meet.py`).

## Beschermd (bewezen in `controle.py`)
- **Alpha-diff 0** (silhouet, kraagpuntvorm en poten ongewijzigd).
- **Oog-diff 0** (x18–33, y39–41, indexen gelijk; oogwit 12 en oogrand 13 ongewijzigd in het palet).
- **Gewijzigde pixels: 83** van 1148 (hoed 13, kop 5, snavel 0, kraag 53, poten 11).
- **Kleuren: 14 incl. transparant** (zelfde indexen als r3; slots 14 en 15 blijven vrij).

## 1. Schaduw (licht linksboven, schaduw rechtsonder)
- Hoed, kop, snavel en poten volgen het model al: kroon links licht (5) en rechts 3, rand-voorkant 4 en rechts 3, donkere band onder de kroon, kop onder de hoed 3, kop links licht, snavel onder/rechts middentint, achterpoten donker. Hier niets veranderd.
- **Kraag (53 px, 6 → 7):** in r3 had donkerbruin 6 een modelhelderheid van gem. 137, p85 172. Dat is midden/licht in het model. Daardoor las de rechterkant als "één bruine massa" (zwak punt 1 van de r2-maker). Een kraagpixel blijft nu 6 waar het model donker is (ML < 135) of een lijn/streng heeft (≥ 12 donkerder dan de mediaan van zijn 5×5-kraagomgeving). Elders wordt het de middentint 7. Daarna zijn 9 losse 7-eilandjes van 1 px teruggezet naar 6, dus geen nieuwe ruis. Resultaat: links-voor licht (8/9), rechts middentint (7) met de donkere strengen en diepten van het model (6). Dat is de verdeling van het model.
- Niet gladgestreken of gemiddeld; alleen per pixel de tint die bij de gemeten modelhelderheid hoort.

## 2. Belijning (omlijningsronde volgens de gids)
Gids (r. 80–170, 340–470): "The 'outline shadows' are always black"; "we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide"; "Put some of the shadow/outline highlight color on the outlines in the very most highlighted parts ... place pixels of the outline highlight color on the inside of the outline rather than the outside."
- Getoetst en goed: lichtkant per onderdeel in de eigen donkerste tint (hoed 2, kraag 6, snavel 6, poten 2/6), zwart rechts en onder. Binnenlijnen van de hoed zijn 2 (niet zwart). Zwart binnen het silhouet alleen waar vorm over vorm valt (onder de hoedrand, onder de snavel, kin, kraagpunten over de poten, tussen de poten); zo doen de maatstaf-sprites het ook (gemeten: 44–102 binnenpixels zwart).
- **B1 klonters (26 px):** zwarte binnenpixels in de binnenhoek van een getrapte buitenlijn (zwarte randburen boven/onder én links/rechts, dus een 2×2-klonter) zijn de eigen donkere tint geworden (hoed 2, kraag/poten 6). De lijn blijft dicht (8-verbonden) en is nu overal 1 px. Plekken: rechterrand hoed en kroon, hoedrand linksonder, kraag rechtsonder, tussen de poten.
- **B2 om-en-om op één rand (4 px):** hoedrand links (11,34) 2 → zwart (rij was 1,2,1); kop links boven de snavel (17,41) zwart → 2 (rij was 2,2,1,2, lichtkant); kraag links onder (18,53),(18,54) 6 → zwart (rij was 1,1,6,6,1; zwart als boog vanaf linksmidden naar onder).
- **B3 (1 px):** losse zwarte pixel (41,27) in de lijn kroon/rand rechts (rest van die lijn is 2) → 2.
- **B4 snavel-bovenlijn (3 px):** de lijn wisselde 6/2 (snavellijn/koplijn). (24,42),(25,42) → 6, zodat de snavel één doorlopende eigen lijn heeft. De hoekpixel (26,42) wordt kop licht 5 (ML 131, buren 5), anders lag de lijn daar 2 px dik.
- **B5 outline highlights (5 px), alleen waar het model aan de rand het lichtst is (ML ≥ 160) en het vlak erbinnen licht is:** kroon linksboven (27,23),(26,24),(30,22) 2 → 3; kraagpunt linksvoor (18,49),(17,50) 6 → 7. Ze liggen op de lijn zelf, niet erbuiten (zoals Lotads linkerbladrand 8 i.p.v. 9).

## 3. Kleurtinten (palet; r1-families gehouden)
| index | was | nu | L | hue |
|---|---|---|---|---|
| 2 terra lijn/donker | 111,59,33 | 108,52,34 | 67 | 15 |
| 3 terra schaduw | 156,90,59 | 156,86,58 | 104 | 17 |
| 4 terra midden | 188,113,78 | 192,118,80 | 136 | 20 |
| 5 terra licht | 213,137,101 | 222,152,106 | 168 | 24 |
| 6 kraag donker | 88,68,46 | 86,62,44 | 67 | 26 |
| 7 kraag midden | 120,108,77 | 124,104,74 | 107 | 36 |
| 8 kraag licht | 161,132,92 | 164,137,92 | 140 | 37 |
| 9 kraag hooglicht | 223,195,127 | ongewijzigd | 196 | 42 |
| 10 snavel midden | 179,155,90 | 180,150,86 | 152 | 41 |
| 11 snavel licht | 228,199,123 | 232,204,124 | 203 | 44 |
- Hue shift nu per ramp oplopend (schaduw roder en verzadigder, licht lichter en geler). In r3 liep de terra-ramp vlak (hue 19–20 overal) en was de kraagmiddentint groener dan het licht (44 tegen 35).
- Helderheidsstappen terra 36/32/32 (was 36/25/24, de bovenste twee te dicht op elkaar), kraag 40/33/56. Taillow-maat ±30–40.
- Per ramp 4 tinten (terra, kraag) + zwart, snavel 2 tinten + eigen lijn (6), zoals Gen 3-Lotad (snavel 2 + lijn).

## Ter info voor Jordi (geen wijziging gedaan)
- De oogrand (13) is in r2 berekend uit de oude terra licht. Met de nieuwe 5 ligt hij iets roziger dan het lijf. Het oog is beschermd en daarom niet aangepast; kan desgewenst in één paletwaarde worden bijgesteld.
- De poten gebruiken de kraag-donkerbruin (6) als donkerste tint, naast terra (uit r1: pootonderkant bruin). Zo gelaten.
- De kinstrook onder de snavel (rij 47) is terra midden 4. Het model zit daar tussen 3 en 5 in. Zo gelaten.
