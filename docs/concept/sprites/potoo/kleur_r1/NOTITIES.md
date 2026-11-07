# Potoo kleur r1

Bron: `model/model_lijf_30.png` (kader `gereedschap/kader.json`, 16,57 modelpx per spritepixel). Silhouet bevroren.

Werkwijze: palet gemeten met k-means op het model (12 kleuren). Meetkaarten per spritepixel: `meetkaart.txt` (helderheid, donker-aandeel, kleurklasse) en `gids_index.txt` (dichtstbijzijnde paletkleur bij gemiddelde en p15). Rijen met de hand gezet in `rijen_r1.py` (per onderdeel in stukken), `bouw.py` maakt `raster.txt`. Uitsnedes met spritepixelrooster: `gereedschap/rooster.py` (nieuw), helderheid per pixel: `gereedschap/lgrid.py` (nieuw).

Gemeten (L gem/p15): oog schijf x30-36 y5-11; glans (34,7) 220, (34,6) 110 -> glans 2 px verticaal. Oogreflectie onderin (31-35,10) L 13-35 -> 2. Snavel x17-22 y5-9 donker (34-90) -> 1/2/3. Keelholte (28-35,14) L 1-75, (27-31,15) 0-36. Muilrand wit (35,15) 144, (34,16) 167, (33,17) 184, (32,18) 186; donkere lijn ernaast (34,15) 72, (33,16) 83, (32,17) 77, (30-31,18) 92/115.

Pixel buiten het silhouet: (43,8) kuifpluk. Het model toont daar een grijze streng van (41,8) naar (46,8); (44,8) zat al in het silhouet maar los, (43,8) verbindt hem met de kop.

Belijning: rechts/onder 1 (zwart-navy); kruin 2; kuif linksboven en borst links (lichtkant) 3; muilrand links 9 (donkerblauw); kin links 1/2 (schaduw onder de muil).

Zwakke punten (naar r2):
- witte muilrand valt weg tegen de crème borst; het model heeft eronder een grijze band.
- nek (x38-41, y9-15) is in het model lichtgrijs (150-180), hier wit/crème.
- chevrons lezen als stippellijntjes; model: grijze zigzag met grijze schaduw eronder.
- vleugelrand heeft trapgaten (y33-38).
- gezicht boven de bekspleet mist de crème band.
