# Meetstudie overworld per onderdeel (19 nov)

Vraag: hoe verhouden overworldsprites (HGSS, 32×32) zich per onderdeel tot de front en het icoon, per aanzicht?

## Opzet
- **15 soorten** (viervoeters/knaagdieren, bouw van de viscacha): rattata, raticate, sentret, zigzagoon, eevee, pikachu, pachirisu, dedenne, skwovet, minccino, buneary, rockruff, electrike, yungoos, nickit. Stilstaande frames: 0 = voor, 2 = achter, 4 = opzij (links).
- **Met de hand afgelezen** op indexrasters (`laad_ow.py soort` = hexraster met coördinaten; `detail.py uit.png soort` = 26× vel met index per pixel; `rooster_ow.py` = 3 frames met rooster). Afspraken bovenaan `punten_ow.json`. Figuurkader, omlijningskleur en binnenlijnen rekent `analyse_ow.py` uit de pixels.
- **Front- en icoonpunten** uit `../../verhoudingen/data/punten.json` (niet opnieuw gemeten). **Minccino** staat daar niet in: alleen OW-maten; zijn ogen zijn in de OW niet te lezen (het rood is de oorbinnenkant), dus ook geen oogmaat.
- Controle: `vel_ow_1.png`, `vel_ow_2.png` (front 3× met kop/oog | OW voor, achter, opzij 8×; paars kop, rood kruis oog, rode lijn oortop, blauw lijf, groen onderkant poot, oranje staart). Opnieuw rekenen: `python3 analyse_ow.py --vel` → `metingen_ow.csv`, `samenvatting_ow.json`.
- Nauwkeurigheid ±1 px; een OW-kop is 8–13 px, dus ±10%. S = OW-figuurhoogte / front-figuurhoogte (met oren); "×" = t.o.v. gewone verkleining met S.

## Tabel (mediaan (p25–p75), n)
| maat | voor | achter | opzij |
|---|---|---|---|
| S (hoogte OW / front) | 0,43 (0,40–0,53) 15 | 0,39 (0,35–0,48) 15 | 0,39 (0,35–0,41) 15 |
| OW-hoogte / icoonhoogte | 1,00 (0,89–1,05) | 0,86 (0,80–1,02) | 0,87 (0,70–0,90) |
| kop als deel van figuurhoogte | **0,55** (0,46–0,60) | 0,44 (0,37–0,49) | **0,58** (0,50–0,63) |
| (ter vergelijking) front / icoon | 0,39 / 0,50 | | |
| kop b × h (px) | 13 × 11 | 13 × 8 | **9 × 9** |
| kophoogte × | 1,38 (1,05–1,53) | 0,97 (0,90–1,13) | 1,46 (1,11–1,58) |
| kopbreedte × | 1,27 (1,15–1,45) | 1,50 (1,25–1,71) | 1,06 (0,98–1,42) |
| kop OW / kop icoon (h; b) | 1,10; 0,96 | 0,78; 1,00 | **0,86; 0,74** |
| kop/lijf OW ÷ kop/lijf front | | | 1,03 (0,87–1,17) 12 |
| lijflengte × | | | 1,17 (0,84–1,42) 12 |
| oog b × h (px) | 1 × 2 (b 1–2) 14 | – | 1 × 2 (b 1–2) 14 |
| oog verticaal in kop (0 boven, 1 kin) | 0,69 (0,59–0,78); front 0,55 | – | 0,67 (0,62–0,75) |
| verschuiving t.o.v. front (zelfde soort) | **+0,19** (0,02–0,39) | – | +0,19 (0,06–0,31) |
| oog horizontaal (0 snuit, 1 achterkant) | – | – | 0,43 (0,36–0,50); front 0,60; verschuiving −0,11 (−0,18…+0,02) n=10 |
| oogafstand | 5 px (4–6); 0,37 × kopbreedte (0,34–0,40) | | |
| oorlengte boven kopboven (px) | 1 (0–3) | 1 (1–3) | **3** (2–3,5) |
| oor × (alleen oren > 0) | 0,70 (0,55–0,81) 7 | 0,63 (0,50–0,93) 10 | 1,39 (0,89–2,37) 12 |
| oorbreedte (px) | 4 (3–5) | 4 (3–5) | 4 (4–5,5) |
| poot zichtbaar (px) / aantal | 2 (2–3) / 2 | 2 / 1 (0–2) | 2 (2–3) / 2 (1–2) |
| staart × | 0,68 (0,55–0,77) 9 | 0,90 (0,81–1,31) 12 | 1,12 (0,92–1,42) 12 |

**Pixelregels** (OW = a + b × front, rest = rms in px): ooghoogte 1,2 + 0,33 × front (rest 0,4; n 28); oogbreedte ≈ 1,5 constant (rest 0,5); oogbreedte = icoon-oogbreedte (0,1 + 0,86 × icoon, rest 0,25). Kop opzij 8,4 + 0,05 × front breed, 6,3 + 0,14 × front hoog (rest 1,2/1,1): **vrijwel constant**. Kop voor ≈ 14 breed (rest 1,9). Oor opzij 1,9 + 0,19 × front (rest 0,85). Poot opzij ≈ 3 − 0,07 × front (rest 0,6): constant 2–3 px. Staart opzij 5,4 + 0,14 × front (rest 2,1).

**Tellingen:** voor 15/15 beide ogen zichtbaar; opzij 15/15 echt profiel (één oog, kop recht opzij, niet driekwart); lijf opzij 9 horizontaal, 4 rechtop/zittend, 1 rond, 1 alleen kop. Staart zichtbaar voor 9/15 (meestal recht boven/achter de kop, 2× aan de zijkant), achter 12/15 (meestal midden over de rug). Oren voor/achter vaak zijwaarts (lengte ≤ 1). Omlijning: **onderkant zwart bij 43/45 frames**; bovenkant zwart maar 12/45: daar een donkere tint van de lichaamskleur (bijv. 383058 paars, 584018 bruin, 313131 grijs); zijkanten half/half. Binnenlijnen: ja in alle 45 frames (mediaan 19 px in een lijnkleur binnen het silhouet).

## Rekenregels
| # | regel | spreiding | hoe vast |
|---|---|---|---|
| 1 | Figuur: voor ≈ 0,43 × fronthoogte; achter/opzij ≈ 0,39 × front. Ongeveer de icoonhoogte (voor 1,0; opzij 0,87 × icoon). | 0,35–0,53 | vast |
| 2 | **Kop is een vaste maat, geen factor**: opzij ±9 × 9 px, voor ±13 b × 11 h, achter ±13 × 8. | rest ±1–2 px | vast (b ≈ 0 in de lijn) |
| 3 | Kop beslaat **55–58% van de figuurhoogte** voor en opzij (front 39%, icoon 50%); achter 44%. | p25–p75 ±0,07 | vast |
| 4 | **OW-opzij is kleiner dan het icoon**: figuur ×0,87, kop ×0,86 hoog en ×0,74 breed (profiel is smaller dan de driekwartkop van het icoon); maar de kop beslaat relatief meer (0,58 tegen 0,50). | 0,70–0,97 | redelijk vast |
| 5 | OW-voor: kopbreedte ×1,27 t.o.v. gewone verkleining van de frontkop (±13–14 px); ogen 5 px uit elkaar = 0,37 × kopbreedte. | 1,15–1,45; 0,34–0,40 | vast |
| 6 | **Oog = 1 × 2 px** (glans of wit boven, donker onder), soms 2 × 2/2 × 3 bij grote front-ogen; zelfde breedte als het icoonoog. | rest 0,4 px | vast |
| 7 | Oog ligt **lager in de kop** dan in de front (+0,19 → ±2/3 van kopboven naar kin) en opzij iets meer naar de snuit (0,43 tegen 0,60; let op: front is vaak driekwart). | verticaal 0,02–0,39; horizontaal −0,18…+0,02 | verticaal redelijk, horizontaal los (n 10) |
| 8 | Kop/lijf-verhouding opzij = die van de front (×1,03); lijf iets langer dan gewone verkleining (×1,17). | 0,87–1,17; 0,84–1,42 | kop/lijf vast, lijf los |
| 9 | Poten: altijd **2–3 px** zichtbaar, opzij 2 poten, voor 2, achter 0–2. | rest 0,6 px | vast |
| 10 | Oren: opzij 3 px boven de kop (1,9 + 0,19 × front), 4 px breed; voor/achter gaan ze zijwaarts (0–1 px boven de kop). Staart: opzij ×1,1, achter ×0,9, voor ×0,7 (verkort), meestal boven de kop/midden op de rug. | oor ×0,9–2,4; staart rest 2 px | oren als pixelregel redelijk, als factor los; staart los |

Patroon: net als bij het icoon krijgen kleine onderdelen een vaste minimummaat (oog 1×2, poot 2–3 px, oor 3–4 px) en is de kop een vaste blok van ±9 px opzij; de rest van de figuur volgt S ≈ 0,4.
