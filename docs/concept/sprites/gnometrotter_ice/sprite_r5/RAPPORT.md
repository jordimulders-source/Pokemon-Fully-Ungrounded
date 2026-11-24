# Gnometrotter Ice – sprite r5 (23 nov)

Basis: `../sprite_r4/gnometrotter_ice.png` (zelfde palet en indexen). Bouwen: `python3 r5.py` (draait eerst `facet_meet.py`) → `gnometrotter_ice.png`, `_8x.png`, `r5_log.txt` (elke gewijzigde pixel, zone, oud → nieuw). `python3 vel.py` → `vel.png` (model | r4 | r5, 8×).

## Werkwijze
- `facet_meet.py` meet de facetten in `../r3/gemini_r3_lijf.png`: lijn = lichte barst (lum ≥ 215, weinig kleur) of donkere lijn (lum < 110); facet = samenhangend roze stuk ertussen (≥ 350 modelpx); per spritepixel het facet met de grootste bedekking. Kleine facetten (< 14 spritepx) gaan op in hun buur, daarna 3×3-meerderheid. Romp: 6 facetten (kraag links, kraag midden, linkerkolom, groot bovenvlak, groot vlak rechtsonder, vlak linksonder).
- Tinten: helderste grote vlak (model) = 15; facetten linksboven en niet donker in het model = 8; rechtsonder/kraag = 7. Facetgrens: lichte kant één tint lichter (heldere rand), schaduwkant één tint donkerder (8→7, 7→6). Geen nieuwe zwarte lijnen in de romp. Tintvlakjes < 3 px opgeschoond.
- Onderrand romp boven de riem: 7 als schaduwsikkel (het brede 7-blok van r4 is nu facet 8 met 7 alleen langs de rand).
- Ovaal: zelfde modelellips als r4, nu als eigen bal: rand 6 rondom, zwart (1) alleen rechts waar hij tegen ijs/achtergrond ligt, hooglicht 15 linksboven, 7 rechtsonder. (55,32) → 1: de zwarte rand van de bovenarm loopt door tot de hand.

## Telling
| zone | t.o.v. r4 | |
|---|---|---|
| romp (lijf roze) | 83 | |
| schouder (ovaal + aansluiting hand) | 20 | |
| benen | 0 | zie twijfels |
| rest | **0** | silhouet t.o.v. r4: 0 |

## Twijfels
- **Benen niet aangepast.** Dezelfde facetmeting op de benen (`facet_been.npy`, bewaard) gaf losse vlekjes, verloor de schaduw van de voeten en verschoof het lichte bovenvlak; na opschonen bleef het rommeliger dan r4. r4 heeft al vlakken op de modelribben (rechterdij: licht bovenvlak 11, twee rechtervlakken 10 met naad 9, ondervlak 10; linkerdij: boven 11, onder 10). Met maar 3 blauwtinten levert een extra lichte/donkere rand per facet daar vooral ruis op.
- Het 15-bovenvlak van de romp is groot (±35 px); het leest als het lichte facet uit het model, maar kan te bleek ogen.
