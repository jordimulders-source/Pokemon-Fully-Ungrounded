# Llamauler r1 (19 nov): notities van de maker

## Bestanden
- `onderlaag.png`: kale reductie (geen hand): model `gemini/poten/r4_poten_r12.png` + de handschoenen van `gemini/r3/r3_prompt_v3.png` (zelfde schaal, verschoven op de voorvoeten: nabij (dy -2, dx -15), ver (dy 5, dx 0) modelpx). Los: `onderlaag_zonder_handschoen.png`, `handschoenlaag.png`.
- `stap1.png`: onderlaag + alleen technische regels (`scripts/opschonen.py`).
- `lama.png`: 64×64, geïndexeerd, 14 kleuren + index 0 transparant; `normal.pal` (JASC, 16 regels, index 15 ongebruikt).
- `model_1x.png`: het model op 1× op hetzelfde raster (vlakgemiddelde), om tonen te meten.
- `vel.png`: r1 8× | model op dezelfde schaal | oude Llamauler | 1× licht/donker | close-ups kop en poten 12× naast het model.
- Scripts (vanuit `lama/fase2`): `python3 sprite/r1/scripts/reduceer.py` → `cd sprite/r1 && python3 scripts/opschonen.py && python3 scripts/bewerk.py && python3 scripts/maak_vel.py`. Hulpjes: `closeup.py` (uitsnede 12× naast het model, `Z=` voor de vergroting), `dump.py` (tekstraster), `check.py` (kleine vlakjes, kleuren), `box1x.py`.

## Reductie
- Raster: model y 28–1016 → 62 rijen (15,94 modelpx per spritepixel), 44 kolommen, rijen 1–62, kolom 10–53. Box 44×62, 1379 px (oude: 41×62, 1184 px).
- Per blok: gevuld als ≥ 45% niet-wit; lijn (index 1) als ≥ 20% van het blok modellijnpixels zijn; anders de overheersende klasse (vacht/rood/geel/groen/blauw/grijs) met de gemiddelde helderheid van die klasse → dichtstbijzijnde paletkleur.

## Afwijkingen van de onderlaag (477 px totaal)
| zone | px | wat |
|---|---|---|
| opschoonregels (stap1) | 96 | losse lijnpixels weg, losse tintpixels naar de buur, binnenlijnen vacht-vacht → donkere vachttoon 2, buitenrand → 1 (rood: 7) |
| handschoen | 76 | r3-handschoenen opgeschoond: polsband grijs/zwart, rood licht linksboven → donker rechtsonder, twee nageltjes; verre handschoen donkerder; onderlaag-vorm en plek gehouden |
| achterpoten | 54 | dunne poten: 1 px buitenlijn om een vulling op de gemeten modelposities per rij (nabij licht 5/4, ver 3/2), hoefjes onderaan |
| kleed | 110 | randen gemeten op het model (schuin, linksboven (27,4; 26,5) → (31,7; 39,7), rechts (39,6) → (42,4)); tonen gemeten (boven lum 100–115 → licht, onder 65–80 → midden), onder- en rechterrand donker, twee donkere strepen, kwastjes op de onderhoeken |
| halsband | 89 | toegestane afwijking 5: band langs de gemeten middellijn (13,5; 30,3) → (25; 26), rood/geel/groen elk 1 px; vijf pompons (rood, geel, groen, blauw, rood) als 2×2 stip met donkere rand op de gemeten middens |
| oren | 31 | rechteroor: lichte rand + donkere binnenkant (model); kwastjes licht linksboven |
| gezicht | 14 | zwaar vlak ooglid 4 px, oogwit-iris-pupil-oogwit, plooi boven het lid, neusgat, platte mond 3 px, licht op de snuit |
| wol | 7 | binnenlijnen waar het model een wolcontour heeft (romp/voorpoot) |

## Resterende zwakke punten
1. Wol: het model heeft op deze schaal weinig bolvormen in de toon (lum 160–180); de sprite leest daardoor vrij glad, minder "Mareep-bollen" dan gevraagd. Ik heb geen bollen toegevoegd die niet in het model staan; de kap tussen de oren heeft maar een lichte schulprand.
2. Kleedstrepen: het model heeft fijne aguayo-strepen die op 1× wegvallen; de twee donkere strepen (posities op 3 en 7 px van de linkerrand) zijn mijn keuze, geen meting.
3. Halsband is met 3 strepen van 1 px dikker en feller dan in het model (zoals afgesproken); de rechterpompon ligt tegen de kleedhoek en valt daar minder op.
4. Nabije achterpoot onderaan maar 1 px licht tussen de lijnen (model ±3 px incl. lijn).
5. Kleuren: 14 van de 15; de polsband gebruikt 2 eigen tinten (grijs + bijna-zwart); die kunnen naar 1 als er een kleur nodig is.
