# Gnomini – sprite r1 (maker-agent, 22 nov)

Model: `../r2/gemini_r2.png` (bevroren). Lever: `gnomini_A.png` (lijfvorm als model), `gnomini_B.png` (ronder lijf), `vel.png` (A | B | model op schaal, 8×; 1× op licht/groen/donker; 2×).

## Werkwijze (overnemen, niet hertekenen)
1. `pitch.py` → Gemini-raster 10,24 px, fase 9,25; `natief.py` → `natief.png` (100×100, figuur 44×53).
2. `klassen.py` → modelpalet (k-means, 15 tinten); `zones.py` → onderdelen tussen de modellijnen (muts, neus, lijf, arm L/R, voet L/R); lijnpixels horen bij de voorste buurzone (`gemeen.py`).
3. `reductie.py A|B` → schaal 41/53 (figuur 34×41, x15–48, y18–58, voeten op rij 58). `kaal_X.png` = kale reductie (vlakgemiddelde + dichtstbijzijnde modelkleur). `red_X.png` = technische onderlaag: per zone vlakgemiddelde (zonder lijnen) → dichtstbijzijnde zonetint, buitenlijn 1 px, binnenlijn aan de rand van het voorste onderdeel, vouwlijnen van de muts waar de modellijn ≥ 35 % dekt, lijnkleur = donkerste modelpixel (zwart of selout zoals in het model).
4. `schaduw.py` + `lijf.py` (alleen het lijf, Jordi's toegestane afwijking "schaduw en volume"): middentint als basis, schaduwsikkel rechts die naar onder breder wordt (2→9 px), slagschaduw onder de mutsrand (1 rij, rechts 2), kleine hooglichtlens op roze (rechts naast de neus) en blauw (linksboven), selout aan de lichtkant van de lijfrand. Kleurfamilie roze/blauw en de broekgrens blijven die van het model. Muts, neus, armpjes en voetjes houden de modeltonen (die zijn al bol met licht linksboven).
5. `maak.py` → benoemde pixelreparaties + B-samenstelling; `controle.py`, `vel.py`, `kijk.py`, `zoom.py`, `toon.py` = meetgereedschap.

**B (ronder lijf):** in het natieve model 4 kolommen ingevoegd in het lijf rechts van de neus (natief x 53, rijen ≥ 47, laag zonder muts); alles rechts daarvan schuift onvervormd mee. Lijf 3 px breder (23 → 26 px), hoogte gelijk. Arm R en voet R zijn in B 1-op-1 de pixels van A, 3 px verschoven (onvervormd). Muts, neus, arm L en voet L: pixeldiff A↔B = 0. (Proef met 5 kolommen/4 px gedaan; nauwelijks verschil, 4 gehouden.)

## Palet (14 incl. transparant)
zwart · muts 4 tinten (modeltinten) · roze 4 (modeltinten) · blauw 3 modeltinten + 1 hooglicht (170,216,244, nieuw voor het volume).

## Afwijking t.o.v. de kale reductie (px anders / px zone)
| zone | A | B | waarvan lijnen (A) | waarvan schaduw/hand (A) |
|---|---|---|---|---|
| muts | 84 / 434 | 84 / 434 | 51 | 0 (rest = vlakgemiddelde zonder lijnen) |
| neus | 6 / 60 | 6 / 60 | 2 | 0 |
| lijf | 99 / 283 | 114 / 329 | 7 | 63 (schaduw/volume) |
| arm L | 14 / 34 | 14 / 34 | 13 | 2 (selout-reparaties) |
| arm R | 13 / 38 | 14 / 38 | 13 | 0 |
| voet L | 20 / 51 | 20 / 51 | 16 | 0 |
| voet R | 16 / 40 | 18 / 40 | 14 | 0 |
| silhouet | 0 | 3 px | | |

Handreparaties (`maak.py`): (30,37) blauwe ruispixel in de lijn neus/mutsrand → zwart; (15,45) lichte kleur op de buitenrand arm L → selout; (16,42) selout arm L gelijkgetrokken; B: (44,39) mutsrand rechts kreeg mutstint op de buitenrand → zwart.

## Controle (`controle.py`)
A en B: 64×64 geïndexeerd, transparant index 0, 14 kleuren; zwart 14,8 % / 14,4 % (Gen 3 ±12–19 %); geen lichte kleur op de buitenrand; geen losse zwarte pixels. Resterende vlekjes < 3 px zijn modeldetails (vouwstreepjes in de muts, selout-hoekjes van armen).

## Eigen zwakke punten
- Muts: tinten 1-op-1 uit het model (vorm en tint bevroren gehouden); de muts zelf heeft dus geen extra volume gekregen. Mag dat ook (muts heeft al licht links/schaduw rechts), dan is dat een aparte kleurronde.
- Roze hooglichtlens rechts naast de neus is een eigen plaatsing (licht linksboven op de bol, de plek linksboven zit achter de neus); op 8× een lichte vlek, op 1× leest hij als glans. Keurder laten kijken.
- Voet R is in het model onderaan lichter dan boven (teen naar de kijker); zo gelaten.
- B verbreedt alleen naar rechts (links zit de neus vast onder de muts); daardoor iets asymmetrisch, in 3/4 aanzicht leest het als een bollere buik.
