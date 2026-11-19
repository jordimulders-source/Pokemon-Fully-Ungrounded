# Palpaca r1 (19 nov): model overgenomen, niet hertekend

## Bestanden
- `palpaca.png`: 64×64, geïndexeerd, index 0 transparant, 14 kleuren gebruikt (+ transparant; index 11 magenta niet gebruikt).
- `normal.pal`: ongewijzigd het oude palet (`../../ronde17/variant_kop/normal.pal`).
- `onderlaag.png`: kale reductie (33×48) in modelkleuren (per vak de dichtstbijzijnde natieve modelkleur).
- `vel.png`: r1 8× | model op dezelfde schaal 8× | oude sprite 8× | 1× op licht/donker + 2× | close-ups kop en poten 12× naast het model.
- `scripts/alles.sh` draait alles opnieuw: `natief.py` → `zones.py` → `bouw.py` → `maak.py` → `reparatie.py` → `meet.py` → `vel.py`.

## Werkwijze
1. **Natief raster** (`natief.py`, uit `steenmozaiek/sprite/natief2.py`): adaptieve celgrenzen op randsterkte, pitch ±8 → 130×132 natief; figuur 76×112 natieve px.
2. **Zones op het natieve raster** (`zones.py`, alleen classificatie, niets getekend): achtergrond (wit, verbonden met de rand + grote ingesloten witte gaten tussen de poten), lijn K (donker of ≥30 onder de lokale mediaan), wol W, verre achterpoot D (taupe), handschoen G, kwastje T, oorbinnenkant P, kraag/manchet C, oog E.
3. **Reductie** (`bouw.py`): oppervlakgewogen, schaal 2,333 (112 natief → 48 px hoog), 33 px breed. Silhouet = vakken met ≥ 45 % figuur (staartpluim ≥ 40 %, houdt de ronde top van het model). Modellijnen (componenten ≥ 8 natief) als dunne lijn via niet-maximum-onderdrukking op de lijnfractie (lijnkaart-les).
4. **Palet** (`maak.py`): wol op toon (2 ≥ 237, 3 ≥ 198, anders 4; toonkaart licht gladgestreken binnen de wol), verre poot 4/5/6, handschoen 7/8/9/10, kwastje 8/9/10, kraag/manchet dichtstbijzijnde van 11–14.
5. **Technisch opschonen** (`maak.py`): tintvlakjes < 3 px in de wol samengevoegd; buitenlijn = randpixels van het silhouet (lichtkant links/boven selout 6, handschoen 10; schaduwkant 1); binnenlijnen: donkere modellijn 5, lichte krullijn 4, tussen onderdelen (raakt poot/handschoen/kraag) 1; losse 1-px lijnpuntjes → 4.
6. **Reparaties** (`reparatie.py`, bovenlaag, elke pixel met reden en modelplek): oog (glans linksboven, lichtere onderkant 15, verre oog op de wangrand), neusgat en mondlijn, roze binnenoor links, kraagvolgorde teal-roze-teal-geel-teal-roze, manchetten (roze band + onderste rij teal/geel), afgeschuinde glansband op de rug.

## Afwijking van de onderlaag (`meet.py`)
Silhouet: **0 px** anders dan de onderlaag. Kleurafwijking t.o.v. de onderlaag op het oude palet (stap A):

| zone | px | opschonen | reparatie | totaal |
|---|---|---|---|---|
| kop + gezicht | 242 | 61 | 8 | 65 |
| hals + lijf | 278 | 38 | 5 | 43 |
| handschoenen + manchetten | 84 | 32 | 8 | 40 |
| poten (licht) | 102 | 20 | 0 | 20 |
| staart | 59 | 12 | 1 | 13 |
| oren + kwastjes | 27 | 10 | 0 | 10 |
| verre achterpoot | 42 | 9 | 0 | 9 |
| kraag | 9 | 3 | 4 | 7 |
| **totaal** | **843** | **185** | **26** | **207** |

"Opschonen" is vrijwel geheel buitenlijn (randpixel → lijnkleur) en binnenlijnkleur; de reparaties zijn de 26 pixels hierboven, alle naar het model.

## Afmetingen
Wezen 33 × 48 px (oortop t/m hoeven), op 64×64 op x 16–48, y 14–61 (onderaan, gecentreerd).

## Pootstand (de kern) uit het model
Nabije voorpoot geheven met handschoen (links, rij 32–42), verre voorpoot staand met handschoen (midden, rij 36–47), nabije achterpoot licht en naar voren onder de buik (kol 17–22), verre achterpoot donker (5/6) en naar achteren (kol 26–32). Allemaal rechtstreeks uit de reductie, geen pixel aan de poten verschoven.

## Zwakke punten die nog over zijn
- **Wol** leest vlak: de krullen van het model worden op 2,3× kleiner grotendeels één tint 3 met een paar 4-krullijnen; het model heeft meer zachte krulvormen op borst en lijf.
- **Pony/fringe-lijn** boven het oog is een mengsel van 4 en 5 (model heeft daar donkere en lichte lijnstukjes); leest iets vlekkerig op 8×, op 1× niet.
- **Hals** heeft een grote vlak in schaduwtint 4 (model: hals in de schaduw onder de kin); door het rozige 4 van het oude palet oogt dat warmer/donkerder dan het grijsbeige van het model.
- **Staartpluim**: linksboven een getrapte schuine rand; de bultjes van de pluim vallen weg bij deze schaal.
- **Gezicht** is trouw maar klein: oog 2×3 (zoals het model op deze schaal), mond 2 px. Of dit "cute" genoeg leest is de vraag voor de keurder/Jordi; groter maken = afwijken van het model.
- Selout aan de lichtkant is index 6, die donkerder is dan 5 (overgenomen van de oude sprite).
