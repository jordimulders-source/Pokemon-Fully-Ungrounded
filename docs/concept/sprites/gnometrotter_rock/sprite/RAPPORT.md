# Gnometrotter (Rock) – frontsprite r1 (maker-agent, 23 nov)

Model (bevroren): `../r8/gemini_r8.png`. Lever: `gnometrotter_rock.png` (64×64, P, index 0 transparant, 16 paletkleuren, 15 gebruikt), `gnometrotter_rock_8x.png`, `vel.png` (sprite | model op schaal 8×; 1× op 6 achtergronden; 1× en 2× naast Gnomini en Gnomad). Gedeelde reductie + palet voor de zusters: `GEDEELD.md` + `reductie_gedeeld.py`.

## Werkwijze (verkleinen, niet tekenen)
1. `pitch.py`: geen bruikbaar natief raster (kamscore 1,3, pitch x≠y) → rechtstreeks verkleind, P = 8,1, voeten op rij 59 (zie GEDEELD.md).
2. `fam.py` + `zones.py`: per modelpixel familie (zwart, grijs, roze, blauw) en onderdeel (samenhangende vlakken tussen de modellijnen).
3. `reductie.py` → `kaal.png`: vlakgemiddelde → dichtstbijzijnde paletkleur. Dit is de basis van de sprite.
4. `maak.py` (alleen technisch, alles uit kaal.png): kleur binnen de eigen familie van het onderdeel (vreemde/te donkere tint uit de vlakgemiddelde → lijn of dichtstbijzijnde vlaktint op helderheid); buitenlijn 1 px; zwart binnenin → outline base; onderdeelgrens zonder lijn → lijn op het voorste onderdeel; modelnaden die de vlakgemiddelde wegpoetste (0,5 px brede modellijn, bedekking ≥ 0,17 en lokaal maximum) terug als lijn (32 px); losse lijnstipjes < 3 px weg (9 px); tintvlekjes < 3 px en één ronde 3×3-meerderheidsfilter binnen hetzelfde onderdeel (ruis).
5. `dc.py`: Dragonfly Cave-omlijningsronde, daarna de gesp.

## Dragonfly Cave-omlijning (gids r. 80–170, 340–470; maatstaf Gnomad r10–r11)
- Buitenlijn: outline base van het eigen vlak waar de rand naar het licht (linksboven) wijst, zwart (outline shadow) aan de schaduwkant en onderkant. Outline bases: gesteente (muts, rugkam, riem, stok, zolen, baard, haar) 2; roze 6; blauw 9.
- Binnenlijnen en naden nooit zwart: outline base van het eigen vlak.
- Ronde delen (neus, hand R, bovenarm R): rand rondom in 6, zwart als boog van linksmidden via linksonder tot ondermidden (SPRITE_KERN, Popplio/Gnomini r10).
- Geen zwart en outline base om en om op één rand: 2 px gelijkgetrokken.
- Outline highlights binnen de lijn: muts bovenrand 3 px (tint 3), handen/vuist 4 px (tint 7).
- Gesp (enige uitzondering op "binnenlijn niet zwart"): zwarte rechthoek zoals de bevroren gesp van Gnomad.
- Zwart 9,5 % van de figuur (Gnomad 12–13 %).

## Afwijking t.o.v. de kale reductie (`tel.py`)
| zone | px anders / zone | lijn | oogstrook | DC + gesp | vlaktint |
|---|---|---|---|---|---|
| muts+rugkam | 104 / 431 | 68 | 12 | 3 | 22 |
| haar L | 25 / 31 | 15 | 0 | 0 | 10 |
| haar R | 26 / 38 | 18 | 0 | 0 | 8 |
| baard | 92 / 176 | 33 | 0 | 0 | 59 |
| neus | 22 / 58 | 21 | 0 | 0 | 1 |
| lijf | 89 / 307 | 54 | 0 | 0 | 35 |
| arm L+hand | 38 / 73 | 29 | 0 | 3 | 6 |
| arm R | 17 / 31 | 16 | 0 | 0 | 1 |
| hand R | 24 / 64 | 22 | 0 | 1 | 1 |
| riem | 49 / 199 | 23 | 0 | 16 | 10 |
| stok | 35 / 101 | 31 | 0 | 0 | 4 |
| broek/benen | 85 / 361 | 79 | 0 | 0 | 6 |
| zool L | 39 / 56 | 30 | 0 | 0 | 9 |
| zool R | 36 / 55 | 26 | 0 | 0 | 10 |
| **totaal** | **681 / 1981** | 465 | 12 | 23 | 182 |

- "lijn" = de lijn van 1 px (de kale reductie geeft lijnen als grijze middentinten, want de modellijnen zijn ±0,5 spritepx breed). "vlaktint" = tint teruggezet naar de eigen familie of ≤ 3 tinten (baard: donkere grijze vlakgemiddelden → lichtgrijs 12) en de ruisfilter.
- **Silhouet:** 8 px erbij t.o.v. kaal, allemaal aan de stok (drempel 0,35 i.p.v. 0,5, anders breekt hij): (11,37) (4,38) (10,40) (5,42) (10,42) (6,48) (10,48) (7,56).

## Pixels die niet rechtstreeks uit het model komen (met de hand / buiten de regels)
- **Gesp** (17 px): rechthoek x 24–29, y 39–41, zwarte rand, binnen tint 4. Gemeten op het model (raster over de gesp gelegd); de vlakgemiddelde had de 0,5 px-lijnen weggepoetst. Plek en maat zijn van het model, de zwarte lijn volgt Gnomad.
- **Oogstrook** (14 px in de strook, waarvan 12 anders dan kaal; Jordi "1 akkoord"): (24,16) (25,16) (26–30,17) (28,18) dicht met muts, en (26,18) (27,18) (29,18) (30,18) (27,19) (28,19) (lijf onder de mutsrand, in het model zwart) ook muts tint 3. De neusrand (25,17–18) is neus gebleven.
- **Outline highlights** (7 px): (21,8) (23,5) (24,4) muts; (4,31) (5,30) (15,31) vuist; (53,35) hand R.
- Verder geen getekende pixels: alle andere wijzigingen zijn regels (lijn, familie, ruis) op de kale reductie.

## Controle (`controle.py`)
64×64, P, transparantie 0, 15 kleuren in gebruik (index 14, lichtste steen, valt weg na de ruisfilter; blijft in het palet voor de zusters). Geen lichte kleur op de buitenrand behalve de 4 outline highlights; geen losse zwarte pixels. Vlekjes < 3 px die overblijven zijn lijnstukjes (naden in tint 2/6 die aan een zwarte lijn vastzitten) en de glans.

## Eigen zwakke punten (voor Claude/keurder)
- **Baard** leest op 8× wat rommelig (lichtgrijs met losse donkere naadpixels); het model heeft daar vlakke facetten met dunne lijnen. Op 1× leest hij als één stenen baardblok.
- **Haarplukken** (vooral rechts) zijn kleine grijze vlekken onder de muts; de spitse plukjes van het model (±1 px dik) worden in de verkleining grijze middentinten. Herkenbaar, niet scherp.
- **Lijfplaten**: de naden tussen de roze rotsstukken zijn minder duidelijk dan in het model (deels lijn 6, deels weggevallen).
- **Neus**: bovenkant valt onder de muts (zoals in het model), daardoor oogt hij op 8× iets kleiner dan in het model.
- Kleuren roze/blauw zijn die van Gnomad (feller dan het model; mag, lijn klopt).
- Toets door de zusters: Ice r3 met dezelfde parameters geeft x 3–61, 1889 px (Rock 1973 px): de omtrek is niet pixel-gelijk; verwacht een paar pixels verschil.
