# Regionale Abra, kleur_r3 (maker-agent, 13 nov)

Uitgangspunt: `../kleur_r2/abra_r2.png`. Benoemde reparaties van de coördinator: (1) onderhelft is een mozaïek, (2) te veel binnenlijnen, (3) rechterhand per pixel van het model lezen, (4) kop niet aanraken, (5) bovenrand staart lichte selout.

## Reproduceren
`python3 maak_r3.py` → `abra_r3.png`; `python3 bewaak.py abra_r3.png` (silhouet t.o.v. r1/r2, lijnpercentages, open rand, losse lijnpixels); `python3 maak_vel.py` → `abra_r3_8x.png`, `vel.png`, `closeup.png`.
Meetgereedschap: `cel.py PNG x0 x1 y0 y1` (per spritepixel de r3-kleur naast het 2×2-modelblok als tekst), `naast.py` (zelfde, als rijen), `mzoom.py` (origineel model 32× op het spriteraster), `zoom.py` (sprite | model 16×), `txt.py` (raster als tekst).
Spritepixel (x,y) = natief modelblok vanaf (2x−1, 2y−14) (offset uit kleur_r1).

## Wat maak_r3.py doet
1. **Silhouet = r2** (bevroren; `bewaak.py`: diff 0 buiten de handenzone; de 3 vingergaten van r2 blijven).
2. **Kop bevroren uit r2** (masker `KOP`, per rij tot en met de rechterlijn van de kop; diff 0 bewezen) en **romp/schouders y < 40 bevroren uit r2** (geen opdracht; de gladfilter verloor daar modeltonen).
3. Regelstap voor de rest: modelklassen per natieve pixel (AA-tint m en geïsoleerde modelpixels nemen de buurtklasse aan); binnenlijn alleen bij ≥ 2 zwarte modelpixels in het blok (1 alleen als brug), verdund tot 1 px; vulling = meerderheid in het blok; meerderheidsfilter per gebied tussen de lijnen; clusters < 4 px nemen de buurtint aan, behalve de vlekjes uit de lijst van kleur_r2/LOG.md (`VLEK`) die het model nog steeds bevestigt (≥ 3/4 modelpixels).
4. **RASTER** (onderhelft, x 8–46, y 40–58): per spritepixel van het modelblok gelezen met `cel.py`/`mzoom.py`, per lichaamsdeel als banden (meerderheid per band, niet per pixel). Niets bijgetekend: elk teken volgt het blok eronder.
5. Zwartpas onderhelft: binnenlijn zonder plaat ernaast en randpixels die alleen boven/links open zijn → L; zwart blijft aan de schaduwkant (onder/rechts) en tegen de platen.
6. EDITS (3 regels, zie onder).

## Palet (11 kleuren + transparant)
| idx | teken | RGB | luma | rol | px |
|---|---|---|---|---|---|
| 0 | . | – | – | transparant | |
| 1 | K | (14,13,22) | 14 | omlijning schaduwkant, plaatlijnen, ogen | 223 |
| 2 | L | (60,54,80) | 59 | omlijning lichtkant, hoofdlijnen (arm over dij, onderarm over knie) | 122 |
| 3 | 1 | (49,48,61) | 49 | plaat donker | |
| 4 | 2 | (71,68,87) | 70 | plaat midden | |
| 5 | 3 | (89,88,103) | 90 | plaat licht | |
| 6 | T | (104,98,126) | 103 | **nieuw** (was ongebruikte 'd'): lichte selout waar het model aan de lichtkant geen zwarte rand heeft (bovenrand staart, bovenkant linkervoet, linkerkant arm) | 44 |
| 7 | s | (130,126,150) | 129 | huid schaduw | |
| 8 | m | (161,158,174) | 160 | huid overgang (alleen kop en dij, waar het model een eigen m-vlak heeft) | |
| 9 | b | (180,179,191) | 181 | huid basis | |
| 10 | h | (209,206,219) | 208 | huid hooglicht | |
| 11 | I | (92,86,114) | 90 | **nieuw**: plooi (vingerlijnen, teenplooi), lichter dan een omlijning | 16 |

## Percentages (1068 px)
| | r2 | r3 |
|---|---|---|
| zwart K | 21,3 % | **20,9 %** |
| L | 19,5 % | 11,4 % |
| donkere lijnen K+L | 40,7 % | **32,3 %** |
| T + I (lichte selout/plooi) | 0 | 5,6 % |
| alle lijnkleuren samen | 40,7 % | 37,9 % |

Zwart zit net boven de bovengrens van ±15–20 %: het resterende zwart is buitenrand aan de schaduwkant (onderhelft ±100 px), de plaatlijnen van schouders/romp (bevroren) en de kop (bevroren). Verder omlaag kan alleen door bevroren zones of de schaduwrand aan te pakken; niet gedaan.

## Per zone
- **Kop**: diff 0 met r2 (ogen op hun gemeten plek).
- **Romp/schouders (y < 40)**: diff 0 met r2.
- **Linkerarm**: buis met lichte band h (x 22–23, y 42–46) en schaduwband s, zoals het model; linkerrand T (model: grijze rand), rechterrand één doorlopende lijn op x 26 (y 40–48), in L waar hij over de dij valt.
- **Knieplaat links**: alleen de modeltonen 3/1 (19–20, 45–46) met lijn op x 21; geen losse lijnstukjes meer.
- **Linkerhand**: vingers b met plooien I op (22,51)(22,52)(24,51); lijn tussen hand en scheen doorlopend (21,47–49)→(20,50–51).
- **Linkerbeen/voet**: lichte bovenband h (x 12–14, y 48) onder een T-rand zoals het model; teenplooi I (12–13, 49); scheen b/s in twee banden.
- **Dij en vlak tussen de benen**: dij links m/s (model heeft daar een eigen m-vlak), bovenlijn L; buik/dij rechts b met h-plekken zoals het model; geen losse 1-px tinten meer.
- **Rechteronderarm**: diagonale lichtband h (38,43)→(34,47) met s-band ernaast; de linkerkant van de onderarm is in het model alleen een donkergrijze toonovergang → in de sprite een toongrens, geen lijn. De rechterlijn (onderarm over knie) doorlopend in L.
- **Rechterhand (opdracht 3)**: per pixel van het model gelezen (cel.py 29–38 × 47–55): drie vingers — A x 30 (b), B x 32–33 (h), C x 34–35 (s) — met plooien I op x 31 en x 33/34, en de lichte knokkel h op x 36 (y 50–51) tussen de lijnen x 35/36 en x 37, zoals het model. **Diff t.o.v. r2 in x 29–38, y 47–55: 38 px.**
- **Knie/staartplaat**: plaatgrens zwart (41,48)(41,49)(42,49)(42–44,47), knie b/s.
- **Staart (opdracht 5)**: bovenrand van het onderste staartstuk (x 23–50, y 56–60) in T: in het model is die rand licht/grijs (geen zwart). Rechterkant van de staart houdt de zwarte modelrand. Staartsegmenten (b/s-banden en '2'-streepjes) blijven.

## EDITS
| zone | x,y | van → naar | reden |
|---|---|---|---|
| staart | 48,60 49,60 | I → s | model 'ss/KK': de lijn ligt op de grens met rij 61 (die al rand is), geen dubbele lijn |
| staart | 37–41,62 | s/3 → s | afwisseling s/3 was reductieruis |
| rechterhand | 33,48 | I → s | losse plooipixel (model donker streepje, geen doorlopende lijn) |

## Diff t.o.v. r2: 177 pixels
kop 0 · romp/schouders 0 · linkerarm+hand 20 · linkerbeen/voet 21 · rechterhand 38 · dij/onderarm/vlak tussen benen 18 · knie/staartplaat 17 · rechtervoet 5 · staart 58 (vooral T op de bovenrand).

## Zelfgeziene zwakke punten (open)
1. **Handen blijven klein en druk**: het model heeft 1-px-vingers met 1-px-lijnen; op 2× zijn het vingers van 1 spritepixel. De vingers lezen op 8× als vingers, op 1× als een lichte vlek met streepjes.
2. **Zwart 20,9 %**: net boven de grens; zie boven waarom.
3. **Lichte selout T naast L** op de linkerarm (T y 41–42, L y 43) en de linkervoet (L bij de teen, T erachter): volgt de modelrand (grijs vs zwart), maar het zijn twee lijnkleuren op één rand.
4. Kleurenaantal 11 (+ transparant): T en I zijn nieuw.
