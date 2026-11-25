# Ruimtestation sprite r8 (25 nov): grotere zijbollen en bredere panelen

Jordi over r7: "rechts het beste, maar de twee kleinere bollen hebben nog steeds amper ogen en de panelen zijn allemaal net wat te smal denk ik". De basis is r7 ×1,3.

**Varianten:** de naam geeft de vergroting van de zijbollen en de verbreding van de panelen, allebei ten opzichte van het originele model r13b. De voorste bol blijft overal ×1,3.

| variant | zijbollen | panelen |
|---|---|---|
| s16p13 | ×1,6 | ×1,3 |
| s16p15 | ×1,6 | ×1,5 |
| s18p13 | ×1,8 | ×1,3 |
| s18p15 | ×1,8 | ×1,5 |

**Uitvoer:**
- `sprite_<variant>.png` (+ `_8x`), 16 kleuren, transparency=0
- `model_<variant>.png` (+ `_8x`)
- `vel.png`: r7-130 en de 4 varianten op 8×; daaronder 1× en 2× naast fase 2, op licht en op donker
- scripts: `model8.py`, `maak8.py`, `vel.py`, `pijp/`
- tussenstappen en logboeken: `w_<variant>/`

**Controle:** de pijplijn draait met dezelfde scripts als r7.
- Op het onveranderde model geeft hij na stap 4 exact r6 terug (0 px verschil).
- Met de r7-instelling (VAR=130) komt er r7-130 uit, op 2 px na. Die 2 px zitten op de onderste rij van PB vóór PA. Ze verschillen omdat PB-voor-PA nu met een algemene regel gaat in plaats van met vaste rijen; anders kon het niet met bredere panelen.

## Model (`model8.py`)
**Panelen:** elk paneel is in zijn korte richting (v) breder gemaakt door de eigen paneelpixels nearest-neighbour te schalen. Lengte (u), vakkenaantal en dwarslijnen bleven gelijk.
- **Paneelmasker:** paneelkleur binnen het paneelvlak, zonder bollen, zonder wit en zonder paarse kraag.
- **Volgorde:** de panelen worden van achter naar voor gelegd: PC, PA, PB, PD, PF, PE. Romp, buizen, staafjes en bollen gaan er daarna weer bovenop.
- **Anker:** PA, PE en PF zijn verbreed rond hun middellijn.
- **Afwijking van de opdracht:** PD, PC en PB zijn alleen naar binnen verbreed. Hun buitenrand bleef staan. Rond de middellijn zou het model breder worden dan 225 px en hoger dan 149 px, en dan wordt de hele sprite door de grens van 64 px kleiner.
- **Staafjes:** die blijven aan het korte uiteinde van de panelen vastzitten.

**Zijbollen:** de rechterbol is net als in r7 rond zijn middelpunt geschaald, vóór zijn kraag.
- **Linkerbol:** die blijft achter zijn kraag. Schalen rond het middelpunt gaf bij ×1,6 en ×1,8 een wit blok dat boven en onder de kraag naar rechts uitstak. Daarom is hij geschaald vanuit de kraagkant (x=79), zodat de snede achter de kraag blijft. Hij groeit daardoor naar links, boven en onder.
- **Rechterbol ×1,8:** die dekt een groot deel van paneel PC en van zijn kraag af.

**Vooraf berekend voor 64 px** (diameter in spritepx; de ring rekent als 1,6× de iris):

| oog | r7 ×1,3: iris / ring | ×1,6: iris / ring | ×1,8: iris / ring |
|---|---|---|---|
| links | 2,6 / 4,1 | 3,2 / 5,1 | 3,4 / 5,4 |
| rechts | 3,0 / 4,8 | 3,7 / 5,9 | 4,2 / 6,8 |

Dat is genoeg voor ring 1 + iris ≥ 2 + ring 1.

## Ogen (gemeten in de sprite)
Iris en pupil in pixels, met de afmeting van iris + pupil en van het hele oog met ring.

| | links | rechts |
|---|---|---|
| r7 ×1,3 | iris 3 + pupil 1, 2×2, ring 4×4 | iris 7 + pupil 1, 3×3, ring 5×6 |
| ×1,6 (p13 en p15) | iris 7 + pupil 2 (1×2), 3×3, ring 5×5 | iris 10 + pupil 4 (2×2), 4×4, ring 6×6 |
| ×1,8 (p13 en p15) | iris 9 + pupil 4 (2×2), 4×5, ring 6×7 | iris 15 + pupil 4 (2×2), 5×5, ring 7×7 |

- **Regels:** dezelfde als r7 (ring, iris en pupil uit de modeldekking, geen wit, ring gesloten).
- **Nieuw (r8):** een zij-oog met een iris van ≥ 3,3 px krijgt een pupil van 2×2 op de plek met de meeste modelpupil, net als het voorste oog. Losse pupilpixels daarbuiten worden iris.
- **Geen handreparaties:** de r7-handreparaties golden alleen voor ×1,2/×1,3 en zijn hier niet gebruikt. Er zijn geen nieuwe nodig.
- **Linkeroog:** de ring ligt op de silhouetrand, als gekleurde selout (zoals in r7-120).

## Panelen in spritepx
Breedte loodrecht op de lengte, berekend uit de modelgeometrie.

| paneel | r7 | ×1,3 | ×1,5 | lengte |
|---|---|---|---|---|
| PA (achter, linksboven) | 4,5 | 5,9 | 6,8 | 15,2 |
| PC (achter, rechts) | 4,3 | 5,6 | 6,4 | 15,0 |
| PD (links) | 4,3 | 5,6 | 6,5 | 12,4 |
| PE (onder) | 5,4 | 7,0 | 8,1 | 14,2 |
| PB (mast boven) | 2,6 | 3,3 | 3,8 | 13,4 |
| PF (mast onder) | 2,8 | 3,7 | 4,3 | 10,2 |

## Afwijkingen en maten

| | s16p13 | s16p15 | s18p13 | s18p15 |
|---|---|---|---|---|
| r4-regels t.o.v. kaal (romp, panelen, ogen) | 252 | 278 | 258 | 285 |
| waarvan ogen | 32 | 32 | 42 | 42 |
| fix5 / ek5 (rest overgeslagen) | 15 / 10 | 16 / 9 | 15 / 10 | 16 / 9 |
| PB voor PA | 8 | 9 | 8 | 9 |
| paneelrecept | 177 | 198 | 174 | 197 |
| sprite (alle 63×43) | 1217 px | 1249 px | 1248 px | 1282 px |

- **fix5 / ek5:** een fix is overgeslagen als hij in een bolzone viel of als de pixel al veranderd was.
- **Rondheid:** de vrije bolrand blijft binnen ±0,8 px. Bij p15 staat in het logboek voor links +2,4 (s16p15) en +1,75 (s18p15). Dat is één pixel van het bredere PA dat tegen de bol aankomt, geen bolrand.

## Ter info
- Bij ×1,8 is het rechteroog groot (iris 5×5). De rechterbol dekt dan de kraag en een groot deel van PC af.
- Bij ×1,6 blijft PC beter zichtbaar en is het linkeroog 3×3.
- Er is nog geen keurder geweest.
