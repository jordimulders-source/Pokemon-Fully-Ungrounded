# Ruimtestation sprite r7 (25 nov): grotere oogbollen, PB voor PA, paneelrecept van fase 2

Opdracht (Jordi over r6): "de panelen lezen niet als panelen ... de bollen zijn niet groot genoeg" · "de bovenste [staat] achter de linksachterste ipv ervoor" · bollen = "de 3 oogbollen met zichtbare ogen erin". Het paneelrecept is een voorstel van Claude.

Uitvoer: `sprite_bol120.png` en `sprite_bol130.png` (+ `_8x`, 16 kleuren incl. transparant, transparency=0), `model_bol120.png` en `model_bol130.png` (+ `_8x`), en `vel.png` (r6 | r7-120 | r7-130 op 8×, paneel-close-ups r6 tegenover r7, 1× en 2× naast fase 2 op een lichte en een donkere achtergrond).

## Controle van de pijplijn
De pijplijn bestaat uit `pijp/` (een kopie van de r4-scripts) en `maak7.py`. Draai je die op het onveranderde model (`VAR=100`), dan komt er exact r4 uit (0 px verschil). Stap 2–4 geven dan exact `kleur_r6/sprite.png` (0 px verschil). Buiten de bolzones is r7 tot en met stap 4 pixel voor pixel gelijk aan r6. De enige verschillen daar zijn PB (stap 5) en de paneelkleuren (stap 6).

## Stap 1: model (`model_bol.py`)
- **Middelpunt en straal** komen uit een cirkelfit op de buitenrand tegen de achtergrond (spreiding 0,3–0,6 px): voor (62,16; 127,95) r 20,62, links (75,01; 64,28) r 10,75, rechts (188,46; 91,70) r 11,98. Bol en oog worden samen nearest-neighbour geschaald, ×1,2 en ×1,3. Er is niets getekend en de rand is niet bijgewerkt: de NN-rand bleef zonder gaten.
- **Volgorde:** de voorste en de rechter bol liggen in het model al vóór hun kraag, en de vergrote bol ligt er nu ook voor. **Afwijking van de opdracht:** bij de linker bol ligt de kraag in het model vóór de bol (de bol eindigt per rij tegen de kraag, x 79–83). Die bol is vergroot maar blijft achter zijn kraag. Zou hij ervoor liggen, dan moest het verborgen deel van de bol getekend worden. Het verschil is ≤1,5 modelpx, dus ±0,4 spritepx.
- **Kraag voorste bol:** omdat de bol rond zijn eigen middelpunt groeit, bedekt hij zijn kraag. Bij ×1,2 blijft een smal paars randje zichtbaar, bij ×1,3 vrijwel niets. De bol sluit dan met een donkere lijn direct op de buis aan. Een voorstel dat ik niet heb uitgevoerd: de bol langs de armas naar buiten schuiven, zodat de kraag zichtbaar blijft.
- **Canvas:** blijft 231×159 (bbox y tot 152 bij ×1,2 en tot 154 bij ×1,3). De schaal blijft 3,515625, de uitsnede is 43 rijen (×1,2) of 44 rijen (×1,3). `model_bol*_bg.npy` legt de achtergrond vast. Zonder dat masker sloot de grotere rechterbol het gat tussen de rechterarm en PC af, en dat gat werd dan wit in plaats van transparant.

## Stap 2: sprite, afwijkingen van de kale reductie per onderdeel
Tabel 1 telt de afwijkingen van `kaal.png` uit `bol*/log.txt` (de r4-regels, ongewijzigd).

| onderdeel | ×1,2 | ×1,3 | reden |
|---|---|---|---|
| romp omlijning | 88 | 90 | navy aan de lichtkant, zwart aan de schaduwkant (r4) |
| panelen PA/PB/PC/PD/PE/PF | 22/22/26/20/30/6 | 22/22/24/20/30/6 | vakken, randen en dwarslijnen (r4) |
| oog voor | 11 | 14 | ring/iris/pupil uit de modeldekking; pupil 2×2; ring gesloten |
| oog links | 7 | 10 | ring tussen de buitenlijn en de iris; bij ×1,3 2 px omlijning naar buiten (model ≥40 % bol, zoals r4); 1 handreparatie (19,30) iris, anders 2 px kleiner dan r6 |
| oog rechts | 8 | 11 | idem; bij ×1,3 3 handreparaties (ring links/boven: de iris lag 4 px breed tegen de bolrand en las als een teal blok) |
| **totaal** | **240** | **249** | |

De ogen volgen dezelfde regel als r4 (ring + iris + pupil, geen wit in de ring, modelkleuren). Ze zijn nu uit de dekking van het vergrote model berekend (`pijp/ogen7.py`) en niet meer per pixel met de hand geplaatst, op de 4 genoemde handreparaties na.

Tabel 2 telt de stappen erna (`bol*/log_maak7.txt`).

| stap | ×1,2 | ×1,3 |
|---|---|---|
| r5 fix5 (MOET) | 17 van 23 (6 overgeslagen: bolzone) | 17 |
| ek5 (DFC) | 12 van 28 (16 overgeslagen: bolzone voor) | 12 |
| bolomlijning in de zones, r4-regel ook op kaal-donkere pixels (ek5-fouttype) | 3 | 1 |
| r6-kleurregels (indexwissels) | 442 | 453 |
| PB voor PA | 8 | 8 |
| paneelrecept | 144 | 144 |

## Stap 3: PB voor PA
De uv-meting op de modelgeometrie geeft voor PB de kolommen x34 (lichte rand, navy), x35 (vak) en x36 (schaduwrand, zwart). De overlap met PA ligt op rij 22–25. Die pixels zijn nu van PB. Rij 21 krijgt de tweede dwarslijn van PB (modelpositie u=2/3), die in r6 ontbrak. PA blijft rechts van de mast zichtbaar (x37–38).

## Stap 4: paneelrecept (alleen kleur, het silhouet is gelijk)
De kleuren zijn exact die van fase 2:

| rol | kleur | index |
|---|---|---|
| vak licht | 112,104,182 | 14 |
| vak midden | 84,76,150 | 13 |
| vak donker | 44,34,84 | 11 |
| rasterlijn en lichte rand | 170,158,222 | 12 |

- **Buitenrand:** navy 41,38,69 aan de lichtkant, zwart aan de schaduwkant. Die bleef zoals in r6.
- **Tint per vak:** de vakken liggen tussen de dwarslijnen en lopen van linksboven naar rechtsonder.

| panelen | vakken |
|---|---|
| PD en PE (voorpanelen) | 14, 13, 13, 11 |
| PA en PC (achterpanelen) | 13, 13, 11, 11 (achterpaneel donkerder, zoals in fase 2) |
| PF (mast) | 14, 13, 11 |
| PB (mast) | 14, 13, 13 (het onderste vak is midden en niet donker, zodat de mast tegen het donkere uiteinde van PA leest) |

- **Rasterlijnen:** 12 op een licht of middenvak, 14 op een donker vak (fase 2 zet B-lijnen op vak 9).
- **Lichte rand:** 12 op de vakpixel direct onder of rechts van de navy lichtrand, alleen als daarachter nog een vakpixel ligt.

## Maten
**Sprite:**

| | r6 | r7 ×1,2 | r7 ×1,3 |
|---|---|---|---|
| bbox (x 0–62) | 63×42 | 63×43 | 63×43 |
| pixels | 1023 | 1062 | 1096 |

**Rondheid:** de afwijking van de vrije bolrand tegen de cirkel blijft binnen ±0,8 px.

| bol | ×1,2 | ×1,3 |
|---|---|---|
| voor | −0,38/+0,45 | −0,34/+0,45 |
| links | −0,57/+0,31 | −0,56/+0,46 |
| rechts | −0,48/+0,51 | −0,41/+0,64 |

**Ogen** (iris + pupil, met ring):

| oog | r6 | ×1,2 | ×1,3 |
|---|---|---|---|
| voor | 13+4 px, 4×5, ring 6×7 | 19+4, 5×6, ring 7×9 | 24+4, 6×6, ring 8×9 |
| links | 3+1, 2×2, ring 4×4 | 2+1, 2×2, ring 4×4 | 2+1, 2×2, ring 4×4 |
| rechts | 5+1, 3×2, ring 6×4 | 5+1, 3×2, ring 6×4 | 7+1, 3×3, ring 5×6 |

## Ter info
- **Zij-ogen:** de oogring is in het model ±4 spritepx breed, dus ×1,3 levert nauwelijks 1 px op. De zijbollen worden wel groter, maar hun ogen blijven ongeveer zo groot als in r6. Alleen het voorste oog wordt duidelijk groter.
- **Panelen:** die lezen nu als vakken met tint en lichte lijnen. PE (onder) is het drukst, met een dambordachtig patroon van lichte lijnen en vakken.
- **Keuring:** er is nog geen keurder geweest.
