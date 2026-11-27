# Uku Pacha r5: notitie van de maker

**Bestand:** `uku_pacha_r5.png` (64×64, geïndexeerd, index 0 = transparant, **16 kleuren incl. transparant**, palet identiek aan r4). Vel: `vel.png` (r5 | r4 | model op 8×; 12× r5 | r4 | model: borst linkernek, borst rechternek, linkerkop, rechterkop, kronkel links, kronkel rechts; r5 op 1×/2× licht en donker).
**Start:** `../r4/raster_af.txt`. **Silhouet:** alpha-diff met r1 en r4 = **0**. Pixeldiff r4 → r5: **85 px** (41 in de borstzone, 44 erbuiten, allemaal hieronder verantwoord). **Pupillen** staan er nog: (10,16), (10,17) en (40,5) = K.

## Scripts (volgorde, reproduceerbaar)
`maak.sh`: `borst5.py` (gebruikt `platen.py`, `zone.py`) → `scherp.py raster.txt raster_s.txt zone` → `afwerk5.py` (3 pixels, zie 3) → `raster2png.py` → `check.py`, `vel.py`. Hulp: `modmed.py` (modelhelderheid per spritepixel). Reproduceert r5 exact vanaf `../r4/raster_af.txt`.

## 1. Borst: platen per nek
Elke plaatgrens is op het natieve model per cel gemeten (lijncellen langs de lijn, van bandrand tot bandrand) en staat als polylijn in `platen.py`; geprojecteerd met dezelfde transformatie als r1–r4 (factor 64/92) en als één doorlopende 1 px lijn getekend. Lijntint naar de gemeten modelkleur van die lijn: de vage grijsblauwe lijnen (model ±(73,102,120)) → `s`; de donkere (±(42–52,59–74,75–92), even donker als de bandranden) → `n`. Geen zwart in de borst.

| nek | plaatgrenzen in het model | in de sprite |
|---|---|---|
| rechternek, medium voorkant | R-a (onder de kin), R-b | R-a (38–39,12)(40–43,13), R-b (38–39,18)(40–41,19)(42–44,18) |
| rechternek, lichte diagonale band | **3**: L0, L1, L2 (+ de kruislijn X onderaan) → 4 platen (topje, L0–L1, L1–L2, L2–X) | **3**: L0 (36,21)(37,22)(38–40,23)(41–42,22); L1 (34,25)(35,26)(36,27)(37,28); L2 (28–30,29)(31,30)(32–33,31). Afstand langs de band 5 / 5 px (model 7,4 / 7,8 cellen = 5,1 / 5,4 px) |
| linkernek, medium voorkant | LA, LB | ongewijzigd (lagen al op de modelplek) |
| linkernek, lichte band | **4**: A, B, C, D (+ kruislijn X waar de rechterband eroverheen loopt) → platen boven A, A–B, B–C, C–D | **4**: A (18,37)(19,38) tot X; B (16,42)(17,43)(18–20,44)(21,43), loopt door in het medium vlak (22–26,42); C (15,47)(16–23,48)(24,47)(25–26,46); D (15,52)(16–17,53)(18–21,54)(22,53)(23–24,52)(25,51). Tussenafstand 6 / 5 / 5 px (model 5,6 / 4,9 / 5,2 px) |
| buik onder D (medium) | E | E (17–18,58)(19–23,59)(24–25,58) |

- **Kruislijn X** (model (44,47) → (34,62), waar de rechterband over de linkerband ligt): doorlopend (27,30)(26,31)(25,32)(24,33)(23,34–35)(22,36)(21,37)(20,38–40); r4 had alleen losse stukken tot rij 33.
- **Vlakken in de band:** per pixel de oppervlak-gewogen mediaan van de lichte modelcellen (lijnen tellen niet mee): ≥ 205 `w`, ≥ 172 `p`, anders `l`. Zo komt de schaduwkant van elke plaat uit het model (bijv. `p` boven B (18–20,43), `l` onder C (19–21,49), de lagere plaat C–D in `p` zoals het model daar 190 heeft). Losse tintvlakjes van 1–2 px in de zone gaan naar de vlakburen.
- **Weggehaald uit r4 (niet uit r3):** de losse navy blokjes van r4 in de bovenkant van de linkerband ((20,32), (21,33), (19,34), (21–22,34), (20–21,35), (18,36), (20,36), (19,37)): daar heeft het model geen lijn (allemaal lum 218–221 of schaduw 178–184; r4's "flauwe plaatgrens"-detectie pakte de schaduw). Verder r4-lijnpixels die 1 px naast de gemeten lijn lagen (dezelfde lijn, verschoven of dubbel): (34,24) (L1), (38–39,22) en (41,23) (L0), (25,31) (X), (16,43), (18–20,43) (B dubbel), (23,47), (25,47) (C), (16,52), (17,54) (D), (19,58), (24,59) (E). Elk kreeg zijn r3-tint terug of de modeltint van de plaat.
- **r3-lijnen:** allemaal behouden, op één na: (42,19) was de hoekpixel van een dubbele R-b ((41,19)–(42,18) sluiten diagonaal aan); de lijn is niet korter geworden. (39,5) en (11,16) zijn sinds r4 oog/pupil.
- **Tintwissel (geen lijn weg):** (30,28) `D` → `n` (bandrand, model (48,44) zwart; `D` is vleugelkleur), (30,29) `D` → `s` (ligt op L2).

## 2. 2×2-lijnklonten
- (18–19,43): weg, B ligt nu één keer op de r3-plek (18–20,44).
- (26,42): `n` → `d` (r3-tint; B loopt in het medium vlak in `d` zoals r3 (23–25,42)).
- (7,58): (8,58) `n` → `d` (r3-tint); die dubbelde de buitenlijn. Het modelstompje (16,88)–(17,89) blijft als (7,58).
- (32,24) zou nieuw zijn (L1-start naast de bandrand): L1 begint daarom op (34,25), diagonaal tegen de rand.
- Over (niet in de opdracht, al bekend uit r3): (5,22) donker mondbinnenwerk, (41,39–40) vleugelklauw (2 px brede omlijning zonder binnenruimte).

## 3. Blur
- `scherp.py`: een middentoon die als 1 px brede strook tussen een lichtere en een donkerdere tint van dezelfde ladder ligt (`d..w` of `D-B-h`), krijgt de buurtint die het dichtst bij de modelhelderheid ligt; niet naast de buitenrand, niet in ogen/tong/tanden/geest/borstzone, en niet als dat een los vlakje maakt. Over de hele sprite gemeten vond hij maar 2 echte gevallen: (29,34) `b` → `s` (rand rechterband, model 110), (46,47) `s` → `m`. Ook stroken van 2 px gezocht: alleen (46–47,44–45) waar het model 71–73 heeft → (46,44), (47,44), (47,45) `d`.
- Rechterkronkel: (34–36,50) `b` → `d`. Het model heeft daar donker (lum 50–65) onder het lichte gaatje op rij 49; r4 maakte er een lichte vlek van 2 rijen van.
- Buik onder D: E als één lijn (zie 1); de r4-stompjes eromheen terug naar het medium vlak.

## Zelfgenoemde zwakke punten
1. **Kronkels:** de rechterkronkel leest nog vlekkeriger dan in het model (veel segmentlijnen, lichte blokken `m` in het midden), maar de opdracht was "alleen scherper, opbouw van r3/r4 houden" en alle lijnen blijven. Met de strookmeting vond ik daar maar 4 echte waas-pixels. Moet de kronkel er meer uitzien als het model (minder, langere lijnen), dan moeten er lijnen weg; dat is een keuze voor Jordi.
2. **Toon van de nekvoorkanten:** het model zit daar op `m`-hoogte (lum ±133), de sprite (sinds r2/r3) op `b` (145, blauwer en lichter). Niet veranderd; kleur mag afwijken en Jordi heeft er niets over gezegd.
3. **Topje van de rechterband (P0, boven L0):** in het model een plaatje van 2 cellen in `p`; in de sprite 1–2 px en daarom `b` (anders een tintvlakje < 3 px).
4. Lijntint: de vage lijnen L0, L1, L2 en A zijn `s` (zoals het model), B, C, D, E en X `n`. In het medium vlak loopt B in `d` door (r3).
