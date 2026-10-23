# Alpaca fase 1, ronde 6: eerste sprite op het goedgekeurde ontwerp

Opdracht: de Gen 3-frontsprite van fase 1 volgens de werkwijze uit `KEURING_RONDE5.md`. De modeltekening is concept A (Wolvuist, `docs/concept/ontwerp/alpaca/concept_A.png`) en wordt trouw gevolgd: geen nieuwe ontwerpkeuzes.

## Bestanden
- `anim_front.png`: 64×128, 2 frames, 16 kleuren, index 0 transparant.
- `normal.pal`: het palet (JASC).
- `compare.png`: de modeltekening naast frame 1 en frame 2 en Mareep en Growlithe op 3×, met daaronder een rij op 1× met de Gen 3-starters, Mareep, Growlithe, Eevee en Skitty.
- `blindtest.png`: blinde test ronde 3 (de kandidaat is nr. 2). `blindtest_ronde1.png` (nr. 11) en `blindtest_ronde2.png` (nr. 13) zijn de eerdere rondes. De letterlijke antwoorden staan in `blindtest_antwoorden.txt`.
- `bron/sprite.py`: de sprite als ASCII-raster. Elk teken is één pixel, met de legenda in `PAL`. Het script maakt `anim_front.png` en `normal.pal`. `bron/compare.py` maakt het vergelijkingsvel. `bron/lineup.py` en `bron/run_blind.py` (met `blindprompt.txt`) maken en draaien de blinde test.

## Werkwijze
- **Skelet:** Mareep, voor de wolbal, de geschulpte wolrand met binnenplooien, de verdeling licht/basis/schaduw over het lijf, het formaat (893 px) en de korte pootjes. Growlithe is gebruikt voor de driekwartskop en de behandeling van de omlijning. De pose zelf komt uit de modeltekening: kop links vooraan, wollijf rechts erachter en twee vuisten vooraan op de grond.
- **Palet:** de tintopbouw is overgenomen en alleen de kleur is gedraaid.
  - **Wol** (1–5) volgt de warme gele ramp van Mareep (255,238,131 → 230,197,98 → 197,148,41 → bruine omlijning), iets lichter en crèmer zoals in de modeltekening. Er zit geen grijs of lavendel in.
  - **Vuisten** (6–9) volgen de vier stappen van Mareeps blauw, gedraaid naar warm rood. Na de blinde test van ronde 2 zijn ze iets naar oranje en bruin geschoven, zodat ze aansluiten bij de vacht.
  - **Vacht** (10–13) volgt de oranje ramp van Growlithe.
  - Daarnaast zijn er 14 (oogglans) en 15 (omlijning).
  - Elk onderdeel heeft zijn eigen indexen (wol, vuist, vacht), dus kleurvarianten kunnen ze apart kleuren. De snuit gebruikt de wolindexen.
- **Met de hand:** elke pixel is in het raster gezet. Het script tekent geen schaduw en geen omlijning. Er waren tien versies:
  - v1–v2: het silhouet.
  - v3–v6: vlakke kleuren, daarna schaduwclusters, geschulpte randen en wolkrullen.
  - v7: een compacter lijf. Dat las als een kuiken, dus teruggedraaid.
  - v8: selectieve omlijning. Aan de lichtkant is de omlijning een tint van de vulling (lichtbruin op de kuif, donkerrood op de vuist, donkerbruin op de wang), aan de schaduwkant zwart.
  - v9: grotere ogen (4×5 en 2×5, met iris en glans), wolkrullen in de vuisten en diepere plooien.
  - v10: de rechterflank 1 px naar binnen, om het oppervlak kleiner te maken.
- **Frame 2:** hij duikt 1 px in, in de hurk vóór een stoot. Alles boven de voeten zakt mee.

## Metingen (frame 1, met `keuring_ronde5/scripts/metrics.py`)
| | oppervlak | accentpixels per px | detail | verzadiging | zwart aan de rand |
|---|---|---|---|---|---|
| **alpaca r6** | **979** | **0,13** | **1,77** | **0,54** | **0,51** |
| alpaca r5 | 1300 | 0,07 | 1,36 | 0,25 | 0,63 |
| Mareep | 893 | 0,16 | 1,65 | 0,53 | 0,57 |
| Treecko | 967 | 0,14 | 1,76 | 0,51 | 0,65 |
| Growlithe | 1088 | 0,15 | 1,85 | 0,48 | 0,41 |

Op deze metingen zit hij nu binnen de spreiding van Gen 3. Het oppervlak is met 979 nog iets boven het doel van 950 (tussen Treecko en Growlithe in). Verder inkorten maakte de randen recht (kuif) of haalde de halsbolling weg.

## Blinde test (3 rondes)
Een verse Claude-sessie kreeg de rij te zien: 12 echte Gen 3-sprites en de kandidaat op een willekeurige plek, op 2× en 1×. De sessie had geen projectcontext en draaide via `claude -p` vanuit een lege werkmap. De vraag was welke van de dertien nep is, en waarom.

| ronde | versie | aangewezen? | zekerheid | belangrijkste redenen |
|---|---|---|---|---|
| 1 | v6 | ja (meteen) | 95% | onbekend wezen; rode 'laarzen' botsen met het palet; omlijning overal even donker; klonterige schaduw; stijf zijaanzicht, grote hoekige kop |
| 2 | v8 | ja (binnen een seconde) | 92% | onbekend wezen; rode laarzen los van het palet; schaduw met weinig toonstappen; klein, simpel gezicht met een piepklein oog |
| 3 | v9 | ja (bijna meteen) | 90% | onbekend wezen; rode laarzen; schaduw in vlekken; weinig selectieve omlijning; grote kop en hals op een klein lijf |

Wat ik tussen de rondes veranderde:
- **Na ronde 1:** selectieve omlijning, een rondere snuit, en vuisten en wol in tinten die bij elkaar horen.
- **Na ronde 2:** grotere ogen, wolstructuur in de vuisten en meer toonstappen in de wol.

De zekerheid zakte iets (95 → 92 → 90%), maar hij werd alle drie de keren direct aangewezen. **De test is dus niet gehaald.**

Kanttekening: elke ronde begint de beoordelaar met het opnoemen van de twaalf echte soorten, en wijst daarna 'de enige die ik niet ken' aan. Een model dat alle Gen 3-sprites kent, vindt een nieuw ontwerp in deze opzet dus altijd via uitsluiting, hoe goed de pixels ook zijn. De opzet meet daarom vooral 'onbekend'. De redenen erachter zijn wel bruikbaar, en die zijn over de rondes verschoven: van techniek (omlijning, schaduw) naar ontwerp (rode laarzen, klein gezicht). Een eerlijkere variant voor een volgende ronde: laat de beoordelaar alleen het vakmanschap rangschikken (welke sprite is technisch het minst Gen 3), met een rij van fakemon en echte sprites waarvan de beoordelaar niet weet hoeveel er nep zijn.

## Eigen oordeel
- **Beter dan ronde 5, en meetbaar:**
  - De wol is warm geel in plaats van grijslavendel.
  - Er zijn twee keer zoveel losse accentpixels.
  - Er is geen spul meer: geen hoedje en geen manchet.
  - Hij is kleiner (979 i.p.v. 1300).
  - Op 1× lees je meteen 'alpaca met wollen vuisten'.
- **Nog niet op Game Freak-niveau:**
  - **Het gezicht is klein naast de kuif.** De bruine kop zit ingeklemd tussen de wolkap en de hals. De modeltekening heeft dezelfde verhouding, maar op 64 px kost dat expressie.
  - **De vuisten lezen op 1× als rode laarzen** (alle drie de beoordelingen). Dat komt uit het ontwerp: in de modeltekening staan de vuisten op de grond. Een oplossing is één vuist opgeheven in dekking, zoals al in de keuring van ronde 5 stond (prioriteit 5). Dan lezen ze als vuisten en niet als schoeisel. Dat is een ontwerpkeuze, dus **voor Jordi**.
  - **De wolschaduw is op sommige plekken nog vlekkerig.** Mareep heeft grotere, rustigere schaduwvlakken.
- **Advies:** laat Jordi eerst kiezen of de opgeheven vuist mag (modeltekening bijwerken). Daarna één pixelronde alleen op het gezicht (iets groter, snuit en mond duidelijker) en op rustigere wolschaduw.
