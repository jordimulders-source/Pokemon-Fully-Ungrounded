# Sauna-yeti (sneeuwmonster fase 3) – sprite ronde 1 (maker)

`sauna_yeti_r1.png` (64×64, geïndexeerd, index 0 transparant, 16 kleuren incl. transparant). `bouw.py` (vanuit `sneeuwmonster_fase3/`), `kaal.png` = kale reductie, `vel.png` = r1 | model op 8×, close-ups gezicht/schouders/buik+knieën/emmer op 12×, 1× op licht/donker naast fase 2 + model 1×.

## Werkwijze
1. **Natief raster** (`gereedschap/pitch.py`, `natief.py`): pieken bij 5,87 én 11,73 → pitch p = 5,867 (1408/240), fase x 4,5 / y 5,0. `natief.png` = 240×130 cellen (mediaan per cel). Figuur natief x44–196, y6–127.
2. **Klassen per natieve cel** (`klassen.py`, alleen indelen): achtergrond, zwart, sneeuw, hout, band, steen, gloed, geel, hand/voet. Hand = blauwgrijs met b−g ≤ 19 (sneeuwschaduw heeft b−g ≈ 24) + opening; emmer = de warme component bovenaan.
3. **Schaal**: 153 cellen → 62 px (2,468 cellen per spritepixel), figuur x1–62, onderkant rij 60. Silhouet = cellen niet-achtergrond ≥ 50 % (bevroren).
4. **Kale reductie** (`kaal.png`): vlaktint = meerderheid van de modeltonen per pixel (sneeuw w/h/m/s, hand 2 tonen, hout 3 tonen), geen gemiddelde. Lijnen via **lijnoverdracht** (`lijnen.py`): elke natieve lijncel (0,4 px) gaat op zijn middelpunt naar één spritepixel → 1 px dun, doorlopend, op de modelplek. Dekking ≥ 45 % = lijntint, minder = s (modellijnen zijn licht, L~124); zwarte binnenlijnen ≥ 30 % = zwart, anders lijntint; zwarte cellen die aan de achtergrond grenzen (buitenlijn) tellen niet mee (anders dubbele buitenlijn). Stenen: vorm = ≥ 45 % steen; rand gloeit waar ≥ 50 % gloed, anders zwart; binnen gloed waar ≥ 40 % (dat zijn in het model de naden tussen de brokken), geel waar ≥ 20 % geel en ≥ 55 % gloed; grijs facet waar de niet-gloeiende steen L ≥ 50 heeft. Buitenrand 1 px zwart.

## Afwijkingen van kaal (168 px; `bouw.py` telt ze)
- **Emmer 39 px.** Band 1 px per kolom op de rij met het grootste bandaandeel (gemeten: X27–29 rij 17, X30–33 rij 16 boven het lichte houten lipje, X34–37 rij 17, X38–41 rij 18; X29 48/47 % → 17 zoals X28). De rest van de 1,5–2 px dikke modelband wordt hout: erboven de houttint van de pixel erboven, eronder hout als hout+zwart ≥ 45 % (donkere lijn + onderrand). Duignaden donker hout op X30, 33, 36, 39 (pieken van `naden.py`, ≥ 3 px uit elkaar zoals fase 2), rij 13 tot de band.
- **Gezicht 41 px** (zone X24–39, Y20–29): geen lijnoverdracht (die gaf elke vachtstreng een pixel); lijntint waar de modellijndekking ≥ 45 %, s bij 25–45 %, anders de vlaktint. Ogen/neus/mond per pixel op de gemeten modelplek (modelcoördinaat omgerekend): oogleden rij 23 (links X26–28, rechts X32–35, model y214/212), ooghoeken (26,24) en (35,24) lijntint, oogwit (27,24) en (33,24), pupillen (28,24) en (34,24) zwart (model: pupil rechts in het oog), neus (30,25) zwart (model 688,236), glimlach rij 27 X27–32 lijntint + donkere haak (33,26) (model 720–732, 255–267). Het donkere vlekje bij de linkerooghoek (model 657,230 → (28,25), 14 %) is weggelaten: het smelt anders samen met de pupil tot een verticale streep.
- **Omlijning 43 px**: selout zoals fase 2: buitenlijn die naar links of recht omhoog wijst in lijntint (sneeuw/hand) of donker hout (emmer); rechts en onder zwart.
- **Ruis 45 px**: vlaktint-vlekjes < 3 px → meest voorkomende vlaktint van de buren; losse lijnstukjes < 3 px (8-samenhangend) die nergens aan raken → vlaktint. Buiten gezicht/emmer/stenen.

## Controle
bbox x1–62, y12–60 (62×49), 2000 px; 16 kleuren incl. transparant; geen lichte kleur op de buitenrand; gloed 56 van 256 steenpixels (22 %, model 28 %).
Palet: fase 2 overgenomen (omlijning, lijntint (62,96,140), sneeuw, hout, grijs, steen, oranje, geel); **rood (216,72,32) eruit** om plaats te maken voor de twee blauwgrijze handtinten (96,140,156) en (136,170,180) (model, b−g ≈ 10–16). Handlijnen = lijntint.

## Zelf nog zwak
- Vacht rond kop en schouders heeft veel losse lijn- en s-pixels (de vele dunne modelstrengen); leest drukker dan het model.
- Linkerschoudersteen: weinig scheuren zichtbaar (2–3 px), model heeft een duidelijk brokkenpatroon.
- Gezicht op 1× klein (ogen 3 px); ogen lezen als halfopen, maar check of de leden zwaar genoeg zijn.
