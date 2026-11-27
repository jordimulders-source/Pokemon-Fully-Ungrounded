# Regionale Hitmonchan (ijssculptuur, uppercut) – sprite-notities maker

**Kandidaat:** `kandidaat.png` (64×64, geïndexeerd, palet van 16 plaatsen waarvan 8 gebruikt: index 0 achtergrond + 7 kleuren), `kandidaat_8x.png`, `vel.png` (r7 | kale reductie r5 | model, 1×/2× op licht en donker).
Figuur 40 × 64 px (onderaan, horizontaal gecentreerd). Laatste ronde `r7/`.

## Onderlaag (model overnemen)
- **Raster:** pitch 10,24, fase 9,25, op 8× gecontroleerd (geen halve cellen van 5,12). `natief.py` → `natief.png` (50×81, mediaan binnenste 4×4 per cel; gelijk aan `../test/natief.png`).
- **Achtergrond:** neutraal wit (min ≥ 248, grijs). IJswit is blauwig (bv. 239,248,250) en hoort bij de figuur; het ingesloten gat onder de wachtvuist is achtergrond.
- **Palet** (`palet.py`, k-means in Lab op de modelpixels): 1 lijn navy (18,27,46) · 2 diepblauw L34 · 3 L47 · 4 middenblauw L61 (ook de selout aan de lichtkant, zoals in het model) · 5 lichtblauw L77 · 6 lichtcyaan L90 · 7 wit/glans L96. Met 15 en 9 kleuren was het beeld gelijk maar met meer spikkels in de facetten (r1–r4).
- **Ogen op natieve grootte (Jordi):** de gezichtszone natief rij 24–31 × kol 28–37 (oog, wenkbrauw, wang/snede eromheen) staat 1-op-1 op sprite rij 18–25 × kol 21–30 (gecontroleerd: identiek aan het gekwantiseerde model). Oog zelf (wenkbrauw + pupilruit + oogwit + onderrand) = 7 × 5 px in model én sprite.
- **Verkleinen** (`r5/bouw.py`): de rest stuksgewijs lineair (rijen 0–24 → 18, 32–81 → 38; kolommen 0–28 → 21, 38–50 → 9; factor ±0,75–0,78), per spritepixel de paletkleur met het grootste overlappende modeloppervlak (lijnkleur ×1,5). Dit gaf schonere facetten dan schrappen (r1: rijen/kolommen schrappen, verworpen; r1b = deze methode op 9 kleuren).
- Meetgereedschap: `meet.py` (M_donker/M_licht/M_gem per spritepixel), `vergelijk.py` (sprite-uitsnede naast het model vervormd met dezelfde afbeelding), `check.py` (kleuren, oog, kleine clusters, rechte randruns), `vel.py`, `zoom.py`.

## Rondes
| ronde | wat |
|---|---|
| r1 | schrappen (Gengas) op 9 kleuren – verworpen: vlekkeriger in romp/rok |
| r1b | oppervlaktegewogen verkleining, 9 kleuren |
| r2–r4 | ontkorrelen + buitenlijn op 9 kleuren (r2 sloopte eerst het oog: daarna oogzone beschermd) |
| r5 | = r1b met 7 kleuren: **kale reductie** (basis voor alle tellingen) |
| r6 | A ontkorrelen (38 px), B buitenlijn-tint (16 px) |
| r7 | 5 losse pixels |

## Pixels die niet 1-op-1 uit de kale reductie (r5) komen: 59 van 1330 (4,4 %), silhouetdiff 0
Per zone: opgeheven kubus 6, kuif/hoofd 17, wachtvuist 5, romp/rok 21, benen 16, arm 4 (zones overlappen deels). Per pixel in `r6/log.txt` en `r7/log.txt`.
- **A ontkorrelen (38):** een vultintpixel (2–6) die in zijn kleur alleen staat (4-buren), niet in een diagonale keten ligt en niet aan de rand/oogzone → meest voorkomende buurkleur. Geen nieuwe tinten.
- **B buitenlijn (16):** lichte randpixels (wit/lichtcyaan op de buitenrand) → lichtkant: de donkerste modelkleur in dat gebied (meestal 4, de selout van het model), schaduwkant: 1. Alleen tint, niet de plek.
- **r7 (5):** vier zwarte lijnpixels zonder lijnbuur (kuif (31,17), gezichtsfacet (19,20), rok/been (28,48), rechterbeen (33,55)) → 2; lichte stip (8,9) midden in het donkere voorvlak van de opgeheven kubus → 2.
- Niets getekend; geen vorm of onderdeel toegevoegd.

## Getoetst
- Kubussen: opgeheven vuist boven licht (6/7), rechts middenblauw (3), voorvlak donker (2–3, van boven naar onder donkerder); wachtvuist boven licht, links lichtblauw (4/5), rechts/voor middenblauw (3). De donkere lijn onder de opgeheven kubus staat ook zo in het model (natief rij 17: 9 lijnpixels op rij).
- Rechte randruns ≥ 6: alleen kubusbovenkant, kubus-rechterzijde, kuif-linkerrand, achterkant linkervoet; het model heeft ze op dezelfde plek. Linkerrand onderarm per rij binnen 0,75 px van het model.
- Geen uitsteeksels van 1 px behalve de kuifpunt (20,9) (punt van de linkerkuifpiek, zoals in het model).

## Twijfelpunten
1. Omdat de gezichtszone op 100 % staat en de rest op ±76 %, is het hoofd naar verhouding ±1,3× groter dan in het model; de arm, romp en benen zijn iets gedrongener. Dat volgt rechtstreeks uit "ogen niet kleiner".
2. Het oog is in het model zelf klein (7×5, pupil = ruitje van 4 donkerblauwe pixels met een lichte kern). Op 1× leest het als een smal, boos oog; het is niet groter gemaakt dan het model.
3. Er blijven ±200 kleine clusters (1–2 px): vooral diagonale lijnstukjes (52) en facetrandjes van middenblauw (46). Dat is de facettextuur van het model; verder ontkorrelen zou facetten wegpoetsen (pixelblur-valkuil) en is daarom niet gedaan.
4. Binnenlijnen (riem, kin, kuifsneden, onder de opgeheven kubus) zijn navy (index 1) zoals in het model, niet een donkere eigen tint; een DC-eindkeuring kan hier anders over oordelen.
5. Palet heeft 7 kleuren: 8 plaatsen vrij voor de eindkeuring (bv. een aparte selout- of glanstint).
