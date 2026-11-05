# Kolibrie pre-evo – kleur r1 op silhouet A open (maker)

Bestanden: `rijen.txt` (handwerk: per rij `y x0 tekens`) → `bouw.py` → `raster.txt`; `palet.py` → `kolibrie_pre.png` + `normal.pal`; `controle.py`; `vel.py` → `vel.png`; studie in `STUDIE.md`.

## Controles (script)
- alpha-diff met `../silhouet_open.txt`: **0** (590 = 590 px).
- open randen (licht vlak naast transparant): **0**.
- schaduwkant-rand niet zwart (rechts/onder, x ≥ 26): alleen (27,14) en (33,23) (bovenrand kop/nek, gekleurde selout) en twee teenpixels (dun deel).
- losse pixels: alleen bedoelde enkelingen (oog-omgeving uit r10, diagonale vleugelrand `E`, iris `5`, een `4`-glans op de vleugelpunt); geen ruis in de vlakken.

## Palet (start r10, bijgesteld)
r10 + donkerder/iets voller lila voor contrast met de buik: `3` (116,98,160)→(106,88,152), `4` (162,148,206)→(152,136,200), `B` (108,98,176)→(102,90,172). Rest gelijk. Geen blauwgroen, geen keelvlek.

## Wat ik deed
- Zones volgens `model_open.png` (8×-raster eroverheen): kop/lijf lila, kap `B`/`E` als kleurgrens zonder lijn boven/achter (grens loopt rechtsboven langs het oog, iets naar voren t.o.v. het model zodat de kleur boven het oog verandert), slab van onder de snavel tot de keel + witte buik als ronde boog, vleugel als donkerder plaat met zachte voorrand in `E` (geen zwart), staartje in lila schaduw, pootjes.
- Oog: Starly-oog uit `maker/kleur_r10/raster.txt` (x21–25, y14–18) pixel voor pixel naar x21–25, y17–21 (middelpunt model ±(23,4; 19)); alleen het nabije oog. Omgevingspixels (`4`/`5`) aangepast aan de kop.
- Snavel: boven (12,15)–(16,17), onder (13,20)–(16,21); `1` punten, `A` donkergrijs, `F` boventint aan de basis; V-binnenkant `9`, roze `8`, gele mondhoek `C`/`D`, donkere lijn `1` op de verbinding (17,17)/(18,18)/(18,20)/(17,21).
- Licht linksboven: hooglicht kop `5` linksboven, kernschaduw `3` rechtsonder; buik `7`-plek linksboven, `5` onder; onderkant lijf `3`→`2`→`1`.

## §0 / SPRITE_NORM
1. 3/4 links-voor: silhouet (bevroren) – ok. 2. ledematen: 2 pootjes, staartje, vleugel – ok (pootjes klein, zie onder). 3. rechte lijnen: alleen waar het silhouet ze heeft (zie onder). 4. oog: Starly-oog – ok. 5. leest op 1× als lila vogeltje met open bekje – ok. 6. formaat 590 px (silhouet). 7. pose: silhouet.
Omlijning per kleurgroep, zwart alleen schaduwkant – ok. Geen open randen – ok (script). Geen willekeurige zwarte strepen: de enige binnenlijnen zijn vleugelvoorrand (`E`) en de korte kop-over-borst-lijn (`5`/`2`).

## Eerlijke zwakke punten
1. **Snavel**: de snavelhelften zijn in het silhouet 1 px dik; op 1× lezen ze als twee dunne streepjes (bijna "snorharen"). ≥ 2 px kan alleen bij de basis binnen het silhouet. Oplossing vraagt een silhouetwijziging (Jordi).
2. **Linker buikrand** is in het silhouet 10 rijen recht (x21, y28–37); met kleur alleen iets verzacht (selout `2`, hooglicht linksboven). Raakt Jordi's "vorm van de buik links".
3. **Vleugelvoorrand** is een doorlopende `E`-lijn van y28 tot y40; zachter dan zwart, maar Jordi kan hem nog steeds als "hard" lezen. Alternatief: middenstuk onderbreken.
4. **Pootjes** lezen op 1× zwak (kleine grijze teentjes onder de zwarte onderrand).
5. **Onderste flank** (onder de vleugel, y37–41) is een groot vlak `3`; rustig maar wat vlak.
6. Staartje leest klein; het is vooral een uitstulpje rechtsonder.

## Lessen
- Een rijenbestand (`y x0 tekens`) + bouwscript met assert op overlap is een snelle, controleerbare manier om met de hand te tekenen.
- Lichte selout (`3`) op een wit vlak oogt als een open rand; `2` (donkerviolet) aan de lichtkant leest beter naast Taillow.
