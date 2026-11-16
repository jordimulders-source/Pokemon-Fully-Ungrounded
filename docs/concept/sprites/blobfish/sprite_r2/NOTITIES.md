# Blobfish fase 1, sprite r2 (maker)

Start: `r1.png` (= `../sprite_r1/blobfish_r1.png`). Silhouet bevroren: **alpha-diff 0** (assert in `maak_r2.py`). Geen contrastronde.
Alleen de 5 benoemde reparaties van Claude; elke pixel gemeten op het natieve model (4×4-blok per spritepixel). Lijst per pixel: `afwijkingen_r2.txt`.

Meetgereedschap: `kaart.py` (donker/licht per blok), `patroon.py` (natieve pixels per blok als tekens), `stralen.py` (lichte straallijnen: natieve pixel ≥ 22 helderder dan zijn 7×7-mediaan → `stralen.npy`), `blok.py`, `raster.py`. Uit r1 overgenomen: `natief.png`, `kaal_info.npz`.

## Afwijkingen t.o.v. r1: 98 px
| Stap | Zone | px | Wat en meting |
|---|---|---|---|
| L lippen/mond | gezicht | 28 | Per blok: ≥ 4 donker + ≥ 5 licht = dunne zwarte lijn door de lichte lip → mondlijn zwart; ≥ 4 donker + < 5 licht (blokgemiddelde ±65) → onderliplijn lijnrood; ≥ 8 licht → liptoon (9/10/11) van de niet-donkere modelpixels. Daarna: mondlijn doorlopend (9,47) en (19,49) zwart (3 en 6 donkere px); onderlip x15–19 y50 = liptint 9 (model (182–188,62–64,67) ligt even ver van 8 als van 9); onderliplijn waar hij tegen de buitenlijn ligt ((8,48) (9,49) (10,50) (11,50)) krijgt de lipkleur van zijn blok, zodat hij niet samensmelt; lipeind gesloten met (20,47) (3 donkere px). |
| O ogen | gezicht | 4 | Beide 2×2 op de modelplek: pupil boven ((19,45) (20,45) 4 en 7 donkere px; (10,41) 3 donkere px; (9,41) ring + glanspuntje → pupil, anders leest het verre oog als witte vlek), wit onder ((20,46) 12 witte px; (9,42) (10,42) 3–4 witte px, stonden al). Pupil zwart i.p.v. de gemeten lijnrood-tint (77–92,38–44,37–44) voor leesbaarheid op 1×. |
| V kopvinnetje | kop | 1 | Ondercontour vinnetje/kop: (14,33) 4 en (15,33) 3 donkere px → lijnrood (één stond al op lijnrood). Samen met de bestaande rand (17,32) een doorlopende lijn; de inkeping tussen kopvin en rugvin zit al in het silhouet. |
| S vinstralen | borstvin 15, rugvin 6, staart 5 | 26 | Spritepixel met ≥ 5 straalpixels in het blok, niet op de rand, en met minstens één straalbuur (losse stippen weg = geen raster) → tint 11 (222,144,150); gemeten straalkleur (211–223,130–149,133–152), helderheid p50 155–172. Borstvin: bovenrandglans + 3 stralen; rugvin 3 korte stralen; staart 2. |
| G glans | kop 23, borstvin 9, staart 7 | 39 | p90-helderheid per blok overgenomen, alleen lichter: p90 ≥ 200 → nieuw glanswit (253,253,253) = mediaan van de glanspixels op de kop; 160–199 → 11; 140–159 → 10. Losse G-pixels zonder lichte buur teruggezet. Rand, ogen en lipzone uitgesloten. |

## Kleuren
11 + transparant: zwart, lijnrood, lijf 3 tinten, mauve, lip/straal 3 tinten (202,75,73) (185,112,112) (222,144,150), oogwit (219,203,203), glanswit (253,253,253). Palet-index 3 en 5 ongebruikt (uit r1).

## Zelf gezien (r2 naast r1 en het model op 8× en 12×)
- Mond leest nu als lichte lippen met één zwarte mondlijn en een rode onderliplijn; het opgekrulde eind is op 4× maar 1 px (19,49) en leest vooral door het gesloten lipeind (20,47)–(21,50).
- Ogen lezen op 1× als twee donkere stipjes met wit; het verre oog ligt tegen de omtrek (zoals in het model).
- **Borstvin:** bovenrandglans + stralen vormen samen een krul ("@"-achtig) op 8×; in het model is dat de lichte bovenrand van de vin plus de stralen. Gemeten en niet bijgewerkt; mogelijk een punt voor de keurder (tint 10 i.p.v. 11 zou zachter zijn maar wijkt af van de gemeten straalhelderheid).
- Kopglans is nu wit met een roze rand langs de linkerkant van de kop, zoals in het model.
