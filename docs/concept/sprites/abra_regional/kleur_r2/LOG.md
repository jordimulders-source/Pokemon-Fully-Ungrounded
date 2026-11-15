# Regionale Abra, kleur_r2 (maker-agent, 13 nov)

Jordi over r1: "de basis is ok, maar ... erg slordig lijnenwerk etc, maar ga vooral verder met verbeteren, en kijk hoe krassault tot een eindresultaat kwam".
Recept Krassault: silhouet bevroren (bewaakscript), lijnen 1 px en doorlopend, buitenrand dicht met gekleurde lijn aan de lichtkant, vlakken per zone opnieuw gemeten op het model, handwerk als data.

## Reproduceren
`python3 maak_r2.py` (regels + EDITS als data) → `abra_r2.png`; `python3 bewaak.py abra_r2.png` (silhouet, % zwart, open rand, losse lijnpixels); `python3 maak_vel.py` → `abra_r2_8x.png`, `vel.png`, `closeup.png`.
Hulpjes: `auto.py` (palet, modelmeting), `lijnen.py` (lijnen uit het model + verdunning), `txt.py` (raster als tekst, `-m` = model 2×), `zoom.py` (sprite | model 16×), `mzoom.py` (origineel model 32× op spriteraster), `handen.py` (fasevarianten handen, verworpen: zie onder).
Spritepixel (x,y) = natief modelblok vanaf (2x−1, 2y−14).

## Regels in maak_r2.py
1. **Silhouet = r1** (buiten de handenzone x 18–37, y 46–58 bevroren). Buitenrand = omlijning, 1 px, dicht.
2. **Binnenlijnen uit het model:** elk blok met ≥ 1 zwarte modelpixel is lijnkandidaat (er valt niets meer weg); daarna Zhang-Suen-verdunning tot 1 px (lijnen breken niet; bij keuze verdwijnt eerst de pixel met de minste zwarte modelpixels). Losse lijnpixels zonder aansluiting worden vulling.
3. **Vulling** = mediaan van de niet-zwarte modelpixels in het blok, op de tintenreeks. Binnen het silhouet tellen bijna-witte modelpixels (lum ≥ 215) als hooglicht, niet als achtergrond (in r1 maakte dat de voet en de snuit te donker).
4. **Ontkorrelen:** clusters < 4 px nemen de meest voorkomende buurtint (zelfde materiaal) aan, **tenzij het model de vlek echt heeft** (in elk blok ≥ 3 van de 4 modelpixels in die tint). Zo blijven Jordi's vlekjes en streepjes; reductieruis gaat weg.
5. **Lijnkleur:** buitenrand open naar boven/links → lijnkleur L; open naar onder/rechts → zwart; binnenlijn op de huid → L; lijnen tegen de donkerste plaattinten (P1/P2) en de ogen → zwart.
6. Huid: modeltint d (115) valt samen met s (130): 4 huidtinten.

## Palet (9 kleuren + transparant; modeltonen, plus één lijnkleur)
| idx | teken | RGB | luma | rol | px |
|---|---|---|---|---|---|
| 0 | . | – | – | transparant | |
| 1 | K | (14,13,22) | 14 | omlijning schaduwkant, plaatlijnen, ogen | 227 |
| 2 | L | (60,54,80) | 59 | **nieuw**: lijnkleur lichtkant + binnenlijnen huid (donker grijs-violet) | 208 |
| 3 | 1 | (49,48,61) | 49 | plaat donker / kaakschaduw | 76 |
| 4 | 2 | (71,68,87) | 70 | plaat midden | 9 |
| 5 | 3 | (89,88,103) | 90 | plaat licht | 65 |
| 6 | d | (115,111,132) | 113 | niet meer gebruikt (samengevoegd met s) | 0 |
| 7 | s | (130,126,150) | 129 | huid schaduw | 223 |
| 8 | m | (161,158,174) | 160 | huid overgang | 20 |
| 9 | b | (180,179,191) | 181 | huid basis | 190 |
| 10 | h | (209,206,219) | 208 | huid hooglicht (linksboven) | 50 |

Huidkleur = de modeltonen (Jordi heeft nog niet gekozen).
**Bijna-zwart: 21,3 %** (r1: 34,6 %); lijnkleur 19,5 %. 1068 px (r1 1071; 3 px gat in de linkerhand, zie onder).

## Per zone
- **Kop:** omlijning dicht, lichtkant (boven/links) L, rechts/onder zwart; kerf in het oor (gat (32,18)) en binnenlijn van het rechteroor uit het model. Vlakken opnieuw gemeten: hooglicht linksboven, schaduwband rechts.
- **Ogen (gesloten, op de modelplek gemeten):** rechteroog (29,28)(28,29)(28,30) zwart, (30,28) huid (model: streep van (30,28) schuin naar (28,30)); linkeroog (22,30)(23,30)(23,31) zwart (model: kort schuin streepje (22,5–23,5; 30–31)). Geen mond.
- **Snuit/kaak links:** donkergrijs kaakvlak (P1) onder het linkeroog en het lichte snuitvlak (h) ernaast zoals het model; zwarte kaaklijn (23,32).
- **Platen (schouders/lijf):** eigen donkere reeks P1/P2/P3, lijnen zwart.
- **Armen:** lijnen nu doorlopend 1 px (in r1 braken ze in de reductie); binnenlijnen L.
- **Linkerhand:** gelezen op `mzoom.py 17 44 30 58`: vingerlijnen (21,52) en (23,52) in L, vingers s, gat tussen de vingers (20,52), (26,51), (26,53) transparant zoals het model; rechterrand (25,53) zwart.
- **Linkerknie:** donkere plaatvlek (19,46)(20,46) en lijn (21,46) zoals het model.
- **Linkervoet:** lichte teenbovenkant (12–14,48), zwarte lijn onder de eerste teen (11–12,49), zwart onder de tweede (10–11,50).
- **Rechterhand:** alleen de regels (lijnen + vulling uit het model); geen handwerk.
- **Staart:** bovenrand nu L (r1 had daar de modeltoon als open rand), onderrand zwart.

## Handenzone: silhouet-diff (toegestaan) = 3 pixels weg
(26,51), (20,52), (26,53): gaten tussen de vingers die het model heeft (blok half wit). Buiten de zone: diff 0 (`bewaak.py`: OK).
Geprobeerd en verworpen: per spritepixel één vaste fase uit het 2×2-blok (`handen.py`, vier varianten): gaf overal open omlijning en geen leesbaardere vingers.

## Diff t.o.v. r1
374 van de 1068 pixels hebben een andere kleur: kop 103, lijf/armen 58, handen/benen/voet 174, staart 39. Lijnpixels r1 370 → r2 435 (28 weg, 93 erbij: gesloten buitenrand + modellijnen die in r1 wegvielen).

### Handwerk (EDITS in maak_r2.py, 40 pixels)
| zone | x,y | van → naar |
|---|---|---|
| oog | 29,28 | L → K |
| oog | 30,28 | L → b |
| oog | 28,29 | L → K |
| oog | 22,30 | L → K |
| oog | 23,30 | L → K |
| oog | 28,30 | L → K |
| oog | 23,31 | L → K |
| sn | 21,31 | K → 1 |
| sn | 22,31 | b → 1 |
| sn | 22,32 | K → 1 |
| sn | 23,32 | L → K |
| sn | 24,32 | b → h |
| sn | 21,33 | 3 → 1 |
| sn | 24,33 | b → h |
| sn | 22,34 | K → 1 |
| sn | 23,34 | L → 1 |
| sn | 24,34 | b → h |
| vt | 12,48 | s → h |
| vt | 13,48 | s → h |
| vt | 14,48 | s → b |
| vt | 10,49 | K → h |
| vt | 12,49 | L → K |
| vt | 13,49 | L → s |
| vt | 10,50 | L → K |
| vt | 11,50 | L → K |
| hl | 19,46 | L → 2 |
| hl | 20,46 | L → 1 |
| hl | 21,46 | L → K |
| hl | 24,50 | L → b |
| hl | 26,50 | b → K |
| hl | 27,50 | L → s |
| hl | 29,50 | L → K |
| hl | 26,51 | K → . |
| hl | 20,52 | K → . |
| hl | 21,52 | s → L |
| hl | 22,52 | L → s |
| hl | 23,52 | b → L |
| hl | 24,52 | L → s |
| hl | 25,53 | L → K |
| hl | 26,53 | K → . |

## Gehouden vlekjes en streepjes (cluster < 4 px dat het model echt heeft)
h (32,17); s (34,17); s (22,21); s (30,22); s (20,24); 1 (39,26); b (22,31); 1 (44,31) (45,31); 1 (21,32); 3 (21,33); 1 (22,33); 1 (30,35); s (41,35); 1 (29,36); s (39,36); d (40,36) (40,37); 2 (25,37) (26,37); s (25,38) (25,39); s (40,38) (40,39) (40,40); s (42,43) (42,44) (41,44); 3 (20,45); b (42,46) (43,46); s (44,46); s (19,47) (20,47); h (12,48); m (20,49); b (31,49); h (33,49); s (34,49); b (21,50) (21,51); h (32,50); 2 (51,50); b (16,51) (17,51) (17,52); s (19,51); s (34,51); s (18,52); s (21,52); s (22,53); s (24,53); 3 (43,53); b (53,53) (53,54); s (36,55); s (53,57); b (50,58); s (52,58); b (26,59); b (48,59) (49,59); b (44,60) (45,60); s (47,60); b (33,61); s (39,61); b (41,61) (42,61); s (45,61)

## Zelfgeziene zwakke punten (open)
1. **Handen blijven het zwakst.** De linkerhand leest nu als hand met vingerlijnen; de rechterhand is alleen met de regels gedaan en is op 8× nog onrustig (model: drie vingers naar beneden met lichte knokkel). Volgende stap: de rechterhand zoals de linker per pixel van `mzoom.py 28 44 42 58` lezen.
2. **Lijnen samen ±41 %** (zwart 21 + L 20): het model heeft veel binnenlijnen. Zwart zit op het doel; het totaal is zwaar.
3. **Staartbovenrand in L** volgt de opdracht (buitenrand dicht); in het model is die rand licht. Leest iets zwaarder dan het model.
4. Rechteroog is 3 px zwart; leest op 1× als gesloten oog, maar minder als boogje dan in het model.
