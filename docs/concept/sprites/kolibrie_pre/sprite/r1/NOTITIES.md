# Hummlet r1 (19 nov), maker

Model: `../../referenties/gemini_gekozen_r5.png`. Breedte 40 px (Jordi: "40px breed mag je proberen"), palet `../../af/normal.pal` (Jordi: "het kleurpalet van het origineel mag gebruiken").

## Resultaat
- `hummlet.png`: 64×64, P-modus, 16 paletplekken (14 gebruikt), index 0 transparant (`transparency=0`). Figuur 40×35 px (x 12–51, y 24–58), 688 px; pootjes op rij 56–58.
- `onderlaag.png`: kale reductie in modelkleuren, op dezelfde plek. **Silhouetverschil sprite ↔ onderlaag: 0 px.**
- `vel.png`: r1 8× | onderlaag 8× | oude sprite 8× | Taillow 8× | Starly 8× | 1× en 2× op licht/donker/wit | close-up kop 12×: sprite | model | onderlaag.

## Werkwijze (scripts in `scripts/`, alles opnieuw: `sh alles.sh`)
1. `natief.py`: natief raster van het Gemini-plaatje, pitch 10,24, fase 9,25 (randsterkte gemeten) → `natief.png` 100×100, figuur 77×67.
2. `zones.py`: zonekaart op het natieve model, alleen met kleurregels (lijn, lila, buik, blauw, poot, geel) plus vakken voor snavel, oog en spikkels.
3. `bouw.py`: verkleinen 77 → 40 px (factor 1,925, oppervlakgewogen; fase −0,5/−0,5 gekozen uit 6 fases omdat het oog daar zijn glans houdt). Per doelpixel: lijn als ≥ 28 % modellijn, oog ≥ 30 %, geel ≥ 12 %, anders de grootste zone; toon = gemiddelde van die zone in de cel. Onderlaag = dichtstbijzijnde modelkleur; stap A = dezelfde zones en tonen op het oude palet (alleen kleurvertaling).
4. `stappen.py`: B (technisch), C (Gen 3-licht als bovenlaag), D (opschonen). Elke wijziging gelogd per regel en zone (`log_*.json`).

## Afwijkingen t.o.v. de onderlaag (stap A = onderlaag in paletkleuren), per zone
| Zone | px | afwijkend | waardoor |
|---|---|---|---|
| kop/lijf/dekveren (lila) | 199 | 62 | buitenlijn 17, sikkel achter kop/lijf 7, hooglicht dekveren 28 (modelplek met toon ≥ 168), wang 5 (mengtint snavel+lila → lila zoals het model), ontkorrelen 7 |
| buik | 184 | 24 | buitenlijn 6, kinschaduw 8, sikkel onder de buik 10 |
| spikkels | 32 | 26 | uitgedund tot 11 losse pixels op de zwaartepunten van de modelspikkels (≥ 3 natieve px); 4 grootste in tint 3, rest 4 |
| vleugel/staart (blauw) | 95 | 29 | buitenlijn 5, sikkel onder vleugel 21, ontkorrelen 5 (deels overlappend) |
| snavel | 12 | 4 | bovenrand selout 2 (lichtkant) |
| oog | 15 | 0 | uit de reductie |
| mondhoek | 1 | 0 | uit de reductie |
| pootjes | 22 | 5 | buitenlijn |
| modellijn | 128 | 12 | snavelbovenrand selout 5, selout lichtkant buik/kop 7 |
| **totaal** | 688 | 162 | silhouet 0 |

Niets is met de hand getekend; alle afwijkingen zijn regels op gemeten modelzones.

## Zelf gezien en gerepareerd in deze ronde
- Ooglans viel weg als "achtergrond" → achtergrond alleen nog via flood vanaf de rand.
- Spikkels werden een raster/dambord → alleen modelzwaartepunten, ver genoeg uit elkaar.
- Losse witte hooglichtvlekken op de borst (proef) → geschrapt; het model heeft daar geen glans.
- Zwart en selout om en om op de linkerbuikrand → lichtkant (links/boven, boven rij 22) consequent selout 2, onderkant zwart.
- Donkere mengvlek tussen snavelbasis en oog → terug naar lila 4.

## Resterende zwakke punten (voor Claude/keurder)
- Oog is een vrij hoekig zwart blok (4×4 met glans linksboven, hoekjes in 14); het model-oog is ronder met lichte rand. Starly-oog uit de oude sprite is de terugvaloptie als de keurder het niet leest.
- Snavel is 1–2 px en trapt in stapjes van 2; leest als lange dunne dichte snavel, maar de vulling van het model (leisteen) is grotendeels lijn geworden.
- Staart is een klein donker blokje met twee lichte pixels; de twee veren van het model zijn op deze maat nauwelijks te scheiden.
- De lichtere veerranden in de blauwe vleugel (model) zijn bij de reductie weggemiddeld; vleugel is nu 8 + sikkel 10.
- Spikkels zijn lichter/kleiner dan in het model (bewust: "enkele duidelijke pixels").
