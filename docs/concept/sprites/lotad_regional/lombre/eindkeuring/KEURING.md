# Keuring + eindkeuring: gaucho-Lombre (25 nov)

Basis: `../sprite/r3/lombre_gaucho_r3_A.png` (Jordi: r3 A, "links"). Model: `../r1/gemini_r1.png`. Familie: `../../af/lotad_gaucho.png`.
Resultaat: `lombre_gaucho_e.png` (64×64, P, index 0 transparant), `lombre_gaucho_e_8x.png`, `vergelijk.png` (voor | na | model per spritepixel op 8×; 1× en 2× op licht en donker naast gaucho-Lotad, Gen 3-Lombre/Ludicolo (`_gba`), Dundragoon, Skinguin, Zapacha en Princadee).
Scripts: `meet.py` (modelkleur/-helderheid per spritepixel via de geschrapte rijen/kolommen van `../sprite/r1/kaal_meta.npy`), `e1.py` (alle wijzigingen, per stap geteld → `e1_uitvoer.txt`), `controle.py` (→ `controle_uitvoer.txt`), `clusters.py`, `uit.py`, `vel.py`.

## Stap 1: keuring (twee eisen)
**(1) Accuraat op het model: ja.** Elke pixel buiten mond en ogen is een natieve modelpixel (kale reductie door schrappen, 0,77×); silhouet, pose, hoed met rode binnenrand, band, vest, vuisten, poten en kleurverdeling volgen het model. Gemeten: per paletindex ligt de modelhelderheid exact op de tint (rood 3/4/5: ML 96/132/147; olijf 7/9/10: 81/128/156). Afwijkingen van het model zijn alleen Jordi's keuzes (mond A5, ogen r3 A, kaak). Twee kwantiseerfouten gevonden: de schaduwkant van de hoedband (model grijsbruin) stond in olijf, en één nagel van de rechtervuist (model geel) stond in olijf licht.
**(2) Gen 3: voldoende, met kanttekeningen.** Op 1× leest hij als een gaucho-Lombre: hoed, boze kop, vuisten, brede stand. Maar naast de maatstaf-sprites was hij te donker en modderig: de olijflijn (46,36,22) was bijna zwart, zodat binnen het vest alles als zwarte lijn las; rood licht (147) lag te dicht op rood midden (134); de lichtkant van de olijf-buitenlijn stond in de schaduwtint (7) in plaats van een outline base; er waren dubbele (2 px) lijnen op 8 plekken; de hoedband liep in de rand erachter over. Effen vlakken: het olijf van vest en laarzen is grotendeels één donkere tint (7) met lijnen; dat is het model (ML 71–90 over het hele vlak), dus geen kwantiseerfout. Gen 3 zou hier meer volume tonen; ik heb dat niet verzonnen (zie ter info).
Bekende zwakke punten van de maker, beoordeeld: hoedband drukker → opgelost (eigen bandschaduw, lijn één kleur); vingerlijnen → nu rode lijn (2) in plaats van zwart/olijf door elkaar, licht vlakker dan zwart maar volgens de gids; rood licht/midden → opgelost (stap 35); 44 losse pixels → de meeste zijn diagonale lijnstukjes (geen ruis); de echte menging (olijflijn in rood, rode lijn in olijf, zwart binnen één onderdeel) is rechtgezet; puntjes van de lippunt → bevroren (A5), niet aangeraakt.

## Stap 2: eindkeuring (75 pixels gewijzigd, alleen indexwissels; niets hertekend)
Gids (`dragonflycave_spriting_guide.txt` r. 80–170, 340–470): "The 'outline shadows' are always black"; "The outline base and outline highlight colors are also colors ... you must also recolor the outlines"; "The outlines must be reasonably dark"; "we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide"; "Put some of the shadow/outline highlight color on the outlines in the very most highlighted parts ... place pixels of the outline highlight color on the inside of the outline rather than the outside"; "the relative luminosity of the shades on the original sprite should always be maintained".

### Schaduw (15 px)
Tinten volgen al per pixel de modelhelderheid; niets gladgestreken of gemiddeld.
- **S1 hoedband (14 px, 7 → 14):** het model heeft een grijsbruine band (licht 115,92,67 = al index 8; schaduw ±75,59,43). De schaduwhelft viel in olijf donker en smolt met de hoedrand. Pixels in de band (y14–17, x33–40) met bruine modelkleur (B > 0,5 R) krijgen een eigen bandschaduw (14, vrij slot).
- **S2 nagel rechtervuist (1 px, (33,43) 10 → 12):** model geel (184,150,82), nu nageltint zoals de andere nagels.

### Belijning (60 px)
Getoetst: de buitenrand was al consistent (schaduwkant 141/141 zwart; lichtkant rood in rode lijn 2). Wijzigingen:
- **B1 (32 px):** lichtkant van de olijf-buitenlijn 7 → 6 (outline base). 11 px blijven 7 als outline highlight: alleen op de hoedrand linksboven, waar het vlak erbinnen de lichtste tint (10) is, op de lijn zelf (niet erbuiten).
- **B2 (17 px):** binnenlijnen binnen één onderdeel in de eigen lijntint: in rood 9 px (zwart of olijflijn → 2: vuistlijnen, arm, dij), in olijf 8 px (zwart of rode lijn → 6). Zwart blijft waar vorm over vorm valt (hoed over band, rand over kop, vest over dij, arm over vest); zo doen de maatstaven het ook. De onderkant van de hoedrand boven de kop (21–22,21) blijft bewust zwart.
- **B3 dubbele lijnen → 1 px (18 px):** arm|band (x28–29, y39–42: grens zwart, tweede lijn → bandtint 9), kraag (40–41,31 → 7), onder linkervuist (15–16,44 → 3), vest|dij (39–40,47 → 7; grens 39–41,48 zwart), rechterbeen buitenrand (47,52–53 → 7), rechtervoet (40,60 → 3).
- **B4 (2 px):** hoedbandlijn (33,14) en (36,18) olijflijn → zwart: één lijn in één kleur (model daar 52,43,27 en 1,3,0).

### Kleurtinten (palet; ≤ 16: nu 15 incl. transparant, slot 11 vrij)
| index | rol | was | nu | L was → nu | hue |
|---|---|---|---|---|---|
| 2 | rode lijn | 118,48,31 | 108,44,30 | 67 → 62 | 11 |
| 3 | rood schaduw | 159,69,46 | 160,74,50 | 93 → 97 | 13 |
| 4 | rood midden | 201,111,77 | 204,114,80 | 134 → 137 | 16 |
| 5 | rood licht | 211,125,90 | 230,154,112 | 147 → 172 | 21 |
| 6 | olijflijn | 46,36,22 | 66,56,30 | 37 → 56 | 43 |
| 7 | olijf donker | 92,80,48 | 110,98,58 | 80 → 97 | 46 |
| 9 | olijf midden | 145,130,78 | 156,142,86 | 129 → 140 | 48 |
| 10 | olijf licht | 174,157,100 | 194,180,114 | 156 → 177 | 50 |
| 8 | hoedband licht | 118,99,65 | 128,100,72 | 101 → 105 | 30 |
| 14 | hoedband schaduw | (ongebruikt) | 88,68,50 | – → 72 | 28 |
| 12 | mond/nagel midden | 179,155,90 | 180,150,86 | 155 → 152 | 41 |
| 13 | mond/nagel licht | 228,199,123 | 232,204,124 | 199 → 203 | 44 |
Zwart (1) en wit (15) ongewijzigd. Stappen rood 35/40/35 (was 26/41/13), olijf 41/43/37 (was 43/49/27): Gen 3-niveau (±30–40). Hue shift per ramp oplopend (schaduw roder, licht geler), zoals de gaucho-Lotad (terra hue 15→24). Mond 12/13 = de snaveltinten van de goedgekeurde gaucho-Lotad (`af/`), zodat Jordi's "de kleur die de snavel van lotad heeft" klopt met de eindversie. Rode familie blijft iets roder/verzadigder dan Lotads terra, zoals in het model.

## Bevroren zones (controle.py, uitvoer in `controle_uitvoer.txt`)
- Alpha-diff 0 (silhouet).
- Indexdiff 0 in: mond A5 (x17–29, y26–35), ver oog (x20–23, y23–27), nabij oog (x28–36, y23–29) en het hele kopvak x17–38, y22–35 (kopcontour/kaak). `e1.py` weigert elke wijziging in het kopvak (assert).
- Let op: de paletwijzigingen voor rood en mond gelden ook in het kopvak (zelfde indexen, iets andere tint). Zwart en wit (ogen) zijn ongewijzigd.
- Gewijzigd: hoed 34, romp/armen 28, benen/voeten 13; totaal 75.

## Ter info voor Jordi (geen wijziging gedaan)
1. **Vest en laarzen zijn één donkere olijftint met lijnen** (model ook). Gen 3 zou daar een lichte kant en een schaduwsikkel geven; dat is tekenwerk buiten het model. Zie je liever meer volume, zeg het; dan als aparte ronde met varianten.
2. **Mond en ver oog** zijn op 1× druk (zwarte puntjes van de lippunt naast het verre oog); bevroren, niet aangeraakt.
3. **Rood tegen terra:** de Lombre is roder dan de gaucho-Lotad (model). De hoed van de Lotad is bruin, die van de Lombre rood met een olijf rand; dat is het model. Kan desgewenst in het palet naar Lotads terra.
4. De rechterhand vóór het vest (x29–37, y39–47) blijft op 1× een drukke knoop (hand, nagels, banddelen); het is het model.
5. Kleine resten: één 1-px bandschaduwpixel (14), één 1-px rode pixel (44,42) en (48,60) uit het model, gelaten.
