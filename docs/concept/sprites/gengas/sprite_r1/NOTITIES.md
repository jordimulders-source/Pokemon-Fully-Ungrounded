# Gengas frontsprite – ronde 1 (maker)

Opgeleverd: `gengas_r1.png` (64×64, geïndexeerd, index 0 transparant), `raster.txt` (één teken per pixel = paletindex), `maak.py` (raster → png + `vergelijk_8x.png`), `vel.png` (8× naast kleurgids, 1×/2× op licht en donker, close-ups 12× van gezicht en de vier manen naast het model).
Meetscripts: `pal.py` (palet), `meet.py` (modelklasse per spritepixel uit het natieve model, blok 74/64), `gids.py` (meetkaart: bolcirkel + modelklassen + Gengar-gezicht op plek A), `gezicht_px.py` (Gengar-gezichtspixels, dx −6 / dy +5), `controle.py` (kleuren, gezicht-diff, vlakjes, losse omlijning, lichte rand, rondheid), `closeup.py`, `vel.py`.

## Wat ik deed
- **Palet (16 incl. transparant):** lijftinten gemeten in `model/gekozen_v3_natief.png` (meest voorkomende kleuren): omlijning (28,12,20), diep (81,36,60), donkere band (96,54,75), magenta midden (136,44,82), lichte band (188,84,105), lichtvlek (198,128,140). Rood (Gengar-idx 5, 6) en tanden (Gengar-idx 1, 2, 7, 3) exact uit `gengar/normal.pal`. Maangrijs: 164 / 122 / 82 (model 183 / 132 / 100), iets warmer; tanden blijven het lichtste punt.
- **Bol:** cirkel x 8–52, y 13–57 (middelpunt 30,35; straal 22,5), met de hand in runs (bovenkant 11 px vlak, dan 3-2-2-1-1-1-1-1, zijkant 11 px). Selout donkermagenta (idx 2) aan de lichtkant (linksboven, tot y 36), zwart vanaf y 37 en rechts/onder; één overgangspunt links en één bij het linkeroor, geen om-en-om. Onder de oren loopt de cirkelboog door als binnenlijn (links idx 3, rechts idx 4, zoals het model daar donkerder is), zodat de bol een bol blijft.
- **Banden** per rij overgenomen van de meetkaart (`meet.py`/`gids.py`) en opgeschoond: lichte bovenband met lichtvlek (model-ellips x 15–26, y 16–25), donkere streep rechtsboven, schuine donkere band (rechts y 23–31, links y 31–41, door de ogen), middenband met de wervel, lichte band onder de mond met de wolkenstreep (y 47–48), donkere schuine band onderaan, magenta onderrand, diepe schaduw rechtsonder. Waar het oude Gemini-gezicht zat loopt de donkere band nu door.
- **Wervel:** opnieuw getekend op de modelplek (x 38–45, y 32–38; model ±38–46 × 32–39) als één doorlopende spiraallijn (idx 3) op een lichte ondergrond (idx 5), zoals in het model.
- **Gezicht (plek A):** 98 Gengar-pixels rood/wit/grijs exact (diff 0). Gengar-idx 15 → omlijning; idx 14 → omlijning in de donkere band (ogen, wenkbrauwen, bovenlip, mondhoek rechts) en → diep magenta (idx 2) voor de onderlip in de lichte band; idx 13 → idx 2. Weggelaten uit de selectie van `gezicht.py`: 8 pixels van Gengars eigen hoofdomtrek (x 10–11, y 29–31 en 41–45), want dat is lijfrand, geen oog of grijns.
- **Ledematen (indeling 3):** boven = hand (vóór, vingers naar links zoals het model, 13×11), rechtsonder = hand (vóór, drie vingers omlaag zoals het model, 15×13), rechtsboven en linksonder = voeten (achter). Vóór: licht (164) met midden-sikkel rechtsonder, selout donkergrijs linksboven en zwart rechtsonder, zwarte lijn waar ze over de bol vallen; elk 2–3 kraters (put idx f, rand lichter). Achter: kleiner (±10×11 en 12×10), alleen midden/donker grijs, zwart omlijnd; rechtsboven half achter de donkere gaslob van het verre oor en de bolrand, linksonder met het rechterdeel achter de bolrand. Voeten: ovaal met teennotjes aan de punt (Gengars voetvorm: afwisselend licht/donker aan de teen, hobbelige rand).
- **Rookslierten** aan beide oorpunten als dunne lijntjes (idx 5/6, zonder omlijning, zoals in het model).

## Controle-uitslagen (`python3 controle.py`)
- Kleuren: 16 incl. transparant.
- Gezicht: 98 rood/wit/grijze pixels, **0 afwijkend**; geen rood/tandkleur buiten het gezicht.
- Bol: cirkelfit middelpunt (30,00; 35,00), r 22,18 op 64 randpunten; **max afwijking 0,39 px**, gem. 0,19 px.
- Vlakjes < 3 px (8-samenhang, randpixels niet meegeteld): alleen nog kraterbodems/-randen van 2 px (hand boven (31–32,4) en (35–36,7), hand onder (45–46,54)) en de taps uitlopende vingerlijnen (28,3) en (28,6). Bewust.
- "Losse" omlijning: (47,21)–(49,24) is de bolrand vóór de gaslob (binnenlijn tussen twee donkere vlakken) en (44,59) is een vingernotje; beide bedoeld.
- Lichte tint aan de buitenrand: alleen de twee rookslierten (model heeft daar geen omlijning).
- Tintstappen lijf (helderheid): 18 / 52 / 69–76 / 117 / 150; maan 76 / 115 / 157; tanden 250 / 217 / 179 / 103.

## Zwakke punten die ik zelf nog zie
1. **Hand boven:** leest nu als vuist met drie vingers naar links, maar nog wat als een steen met strepen; het model heeft meer gespreide knokkels met zwarte spleten. Kandidaat voor een gerichte ronde.
2. **Voeten (achter):** de teennotjes zijn op 1× nauwelijks te zien; ze lezen vooral als ronde stenen. Het model is daar ook vaag, maar Gengars voet heeft duidelijker tenen.
3. **Lichtvlek:** het model heeft een lichtere kern (221,172,177, ±5 px). Weggelaten: geen paletplek over en de lichte band zou dan 4 tinten krijgen (regel ≤ 3). Daardoor oogt de vlek iets vlakker dan in het model.
4. **Kleine randlicht-stukjes rechtsonder** (model y 45–47, x 45–48: tint 3/4 in de diepe schaduw) zijn weggelaten als ruis; ook de zwarte schuine lijn in het model rechtsboven (x 45–48, y 20–29) is vervangen door de bolrand + diepe schaduw.
5. **Achter-ledematen zwart omlijnd rondom** (ook aan de lichtkant), om ze donker en "achter" te houden; streng genomen zou de lichtkant een selout krijgen. Keuze om voor te leggen.
6. **Wervel en wolkenbanden** hebben 1-px tussenruimtes (spiraal) en golvende randen uit het model; op 1× ok, op 8× wat druk bij de linkerkant boven de ogen (y 26–31).
7. Selout bij oren/bovenkant is idx 2; in het model is de bovenrand van de bol lichter (geen donkere lijn). Gen 3-keuze; kan te zwaar ogen.
