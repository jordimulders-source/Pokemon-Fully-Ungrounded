# Gnometrotter (Grass) – frontsprite r1 (maker-agent, 23 nov)

Model (bevroren): `../r4/gemini_r4_lijf.png`. Lever: `gnometrotter_grass.png` (64×64, P, index 0 transparant, 16 kleuren), `gnometrotter_grass_8x.png`, `vel.png` (sprite | model op schaal 8×; 1× op 6 achtergronden; 1× en 2× naast Gnomad, Rock r2 en Grass).

## Gedeeld met Rock (GEDEELD.md)
- **Reductie exact gedeeld** (`reductie_gedeeld.py`, ongewijzigd gekopieerd): P = 8,1, model x 512 → sprite 32, model y 523 → voetlijn 60, ≥ 50 % dekking. Figuur x 3–60, y 0–59, **2056 px** (Rock 1973: zelfde bbox, +83 px door de bladplukjes en het twijgje; voetlijn, hoogte en lijfmaat gelijk).
- **Palet**: 0, 1, 6–11 en 15 exact gelijk aan Rock (zwart, roze, blauw, roze hooglicht). Eigen materiaal: 2–4 schors (2 = outline base (72,50,36), 3 (112,82,58), 4 (152,118,84)) en 5, 12–14 blad (5 = outline base (38,70,42), 12 (58,98,56), 13 (104,150,80), 14 (176,210,120)). Bladmuts 12/13, baard/haar/twijgblaadjes 13/14, schors 3/4 (≤ 3 tinten bruin incl. lijn).

## Werkwijze (verkleinen, niet tekenen)
`fam.py` (blad/schors/roze/blauw/zwart) → `zones.py` (19 onderdelen, vlakken tussen de modellijnen op zwaartepunt) → `reductie.py` (`kaal.png` = kale reductie) → `skel.py` → `maak.py` → `dc.py` → `tel.py`, `controle.py`, `vel.py`. `tx.py` = tekstraster.
- **Lijnen op gemeten plekken** (`skel.py`, nieuw t.o.v. Rock): de zwarte en duidelijk donkere modellijnen worden op volle resolutie tot skelet verdund; een spritepixel met ≥ 3 skeletpunten wordt binnenlijn (outline base van het eigen onderdeel, nooit zwart). Skeletstukjes < 20 modelpx (houtnerfstreepjes) tellen niet mee: alleen de naden tussen de houtplaten en de bladranden, geen zebra. Onderdeelgrens zonder modellijn ernaast: lijn op het voorste onderdeel (19 px).
- **Bladeren**: elk blad (vlak tussen de lijnen) in zijn geheel licht of schaduw naar de gemiddelde modeltoon van dat blad; een groot blad krijgt de schaduw langs zijn onder-/rechterrand. Bladmuts: tonen uit het model (lichte linkerbladen, donkere rechterkant).
- **Volume (kleur mag afwijken)**: lijf één bol (8 licht linksboven, 7 sikkel rechts/onder, slagschaduw 7 onder muts/haar/baard/neus), elk been een eigen bol (split kolom 34, zoals Rock r2), schijven en handen elk een bol. Hooglicht 15 alleen op neus, hand R en vuist L (2 px).
- **Ronde delen** (neus, hand R, vuist L, elleboogschijf): rand rondom 6, zwarte boog linksonder (Gnomini/Rock); schouderschijf alleen rand 6 (met zwarte boog las hij als donkere vlek).
- **Dunne delen**: stok, twijg en twijgblaadjes op drempel 0,35 (Rocks stokregel), anders breken ze. Stok, beide zijtakjes, twijg en blaadjes zijn heel.
- **Ruis**: onderdeel-eilandjes ≤ 3 px naar het omringende onderdeel; tintvlekjes < 3 px naar de buurtint; 3×3-meerderheid binnen elk stuk.
- **Dragonfly Cave** (`dc.py`, zelfde regels als Rock): buitenlijn outline base aan de lichtkant, zwart aan de schaduwkant en onderkant; geen zwart/base om-en-om (2 px gelijkgetrokken); outline highlights muts 3 px (tint 13) en vuist 1 px (tint 7). Zwart 9,4 % (Rock 9,5–9,6 %).
- **Oogstrook**: niet nodig; onder de bladmuts zit in dit model geen donkere strook die als ogen leest (de Rock-regel zou 4 losse px raken). Geen gesp (het model heeft geen gesp).

## Afwijking t.o.v. de kale reductie (`tel.py`)
| zone | px anders / zone | lijn | DC | vlaktint/volume |
|---|---|---|---|---|
| bladmuts | 91 / 337 | 63 | 0 | 28 |
| haar L | 20 / 28 | 16 | 0 | 4 |
| haar R | 37 / 52 | 17 | 0 | 20 |
| baard | 113 / 178 | 66 | 0 | 47 |
| neus | 35 / 55 | 21 | 0 | 14 |
| lijf | 188 / 257 | 91 | 0 | 97 |
| arm L | 36 / 36 | 19 | 0 | 17 |
| elleboogschijf R | 26 / 31 | 16 | 0 | 10 |
| hand R | 42 / 65 | 25 | 0 | 17 |
| riem | 51 / 193 | 35 | 1 | 15 |
| stok | 50 / 111 | 40 | 1 | 9 |
| broek/benen | 242 / 353 | 62 | 0 | 180 |
| zool L | 33 / 56 | 28 | 0 | 5 |
| zool R | 30 / 54 | 27 | 0 | 3 |
| rugplank+twijg | 49 / 125 | 46 | 0 | 3 |
| twijgblaadjes | 20 / 23 | 20 | 0 | 0 |
| knoesten (knieën) | 10 / 10 | 10 | 0 | 0 |
| schouderschijf R | 39 / 56 | 21 | 0 | 18 |
| vuist L | 24 / 36 | 17 | 1 | 6 |
| **totaal** | **1136 / 2056** | 640 | 3 | 493 |

"lijn" = lijn van 1 px (de kale reductie geeft modellijnen als middentinten). "vlaktint/volume" = Gen 3-volume (lijf en benen bewust herkleurd: "kleur mag afwijken") en ruisfilter. **Silhouet**: 9 px erbij, 0 eraf, allemaal dunne delen op drempel 0,35: twijg (53,19), stok (11,37) (5,39) (3,41) (3,42) (12,42) (6,48) (10,48) (7,56).

## Pixels die niet rechtstreeks uit het model komen
- Volumetinten (regel, geen vorm) van lijf, benen, schijven, handen; 2 px hooglicht 15 op neus (19–20,17), vuist L (5,31) en hand R (54–55,35).
- Onderdeelkaart opgeschoond (5 px): (41,18) muts→rugplank; (32,19) (34,20) (37,20) (35,21) muts→haar R.
- Outline highlights 4 px: (17,12) (20,7) (21,6) muts, (5,30) vuist; om-en-om 2 px: (5,38) (18,39).
- Niets getekend: geen blad, naad, schijf of tak die niet op een modelplek ligt.

## Controle (`controle.py`)
64×64 P, transparantie 0, 16 kleuren, bbox x 3–60 y 0–59, zwart 9,4 %, geen losse zwarte pixels; lichte kleur op de buitenrand alleen de 4 outline highlights. Vlekjes < 3 px die overblijven: lijnstompjes die aan een lijn vastzitten, de knoesten, de twijgblaadjes en de hooglichtjes.

## Eigen zwakke punten (voor Claude/keurder)
- **Schouderschijf R** leest als ronde bult met rand op het lijf, minder als los ovaal schijfje dan in het model (het schijfje ligt tegen de silhouetrand, waar het modelskelet niet meetelt).
- **Baard**: lichtgroene bladeren met donkergroene randlijnen (diagonale 1 px-trapjes); op 1× een bladerbaard, op 8× iets minder strak dan de modelbladeren.
- **Knoesten op de knieën** zijn 2×2 donkerbruin (de lichte ring van het model valt weg op deze schaal).
- Roze en blauw zijn de gedeelde Gnomad-kleuren (feller dan het model; zelfde indexen als Rock).
