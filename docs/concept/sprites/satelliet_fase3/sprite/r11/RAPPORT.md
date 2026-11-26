# Ruimtestation sprite r11 (25 nov): ogen in driekwart, rechterbol rond, mast boven en onder

Jordi over r10: "de ogen zijn nu zwarte vierkanten, allemaal dezelfde grootte en zelfde blik, dit moet nog wat meer driekwart, vooral de zijwaartse ogen. Rechterbol is niet goed bol, het maakt niet uit dat die dan het paneel overlapt. Kijk naar hoe het model dat doet. Bovenste paneel is een beetje afgekapt, onderste moet ook nog net wat verder doorlopen".

**Basis:** `r10/sprite.png`, met gerichte reparaties in `herstel11.py` (en `oogmasker.py`). Ten opzichte van r10 zijn **134 pixels** anders, allemaal binnen de vier opdrachtzones:

| zone | pixels |
|---|---|
| oog voor | 40 |
| oog links | 28 |
| oog rechts | 42 |
| rechterbol | 13 |
| PF | 10 |
| PB | 1 |

Buiten deze zones is de diff 0 (`diff_r10.png`). Elke pixel staat met zijn reden in `log_herstel11.txt`.

**Uitvoer:**
- `sprite.png`: 16 kleuren incl. transparant, transparency=0, palet ongewijzigd.
- `sprite_8x.png`
- `vel.png`: r10, r11 en het model op 8×. Daaronder close-ups van de drie ogen (r10, r11 en het modeloog), PB-top, PF onder PE en de rechterbol. Onderaan 1×/2× naast fase 2.

## 1. Ogen
**Uitgangspunt: het model.** Per oog is de vorm genomen uit `model/model_gekozen.png` (r13b, de echte ogen):
- De oogzone is het convex omhulsel van ring en iris.
- De iris is het omhulsel van de teal pixels, met de pupil daarin.
- De rest van de zone is ring. Er zit dus geen wit binnen de ring.

**Verkleining:**
- Elk oog is verkleind met de schaal van zijn eigen bol: voor 1,3/s, zij-ogen 1,8/s.
- De zij-ogen zijn horizontaal extra verkort met ×0,75.
- Per spritepixel bepaalt de modeldekking of het ring, iris of pupil wordt.

**Opschonen:** daarna is per pixel opgeschoond, alleen ringdikte en pupil (tabel `SCHOON` in het script).

**Resultaat:**

| oog | maat | ring | pupil |
|---|---|---|---|
| voor | 8×9 | links 1 px, rechts 2 px; lichte band rechtsboven, schaduw rechtsonder | 3 px + een donkere tealhoek (afgerond), iets links van het midden |
| links | 5×6 | iris tegen de bolrand links, zoals in het model; ring rechts 2 px | 1×2 |
| rechts | 6×7 | ring rechts 2 px | 1×2, met de iris rechtsonder donker teal |

Alle drie kijken naar voren-links, zoals het model. Ze zijn verschillend van maat, en de zij-ogen zijn smaller dan hoog. De bolomlijning blijft overal staan: waar de ring in het model de bolrand raakt, ligt hij er hier tegenaan.

## 2. Rechterbol
- Een volle cirkel met middelpunt en straal van r10: c = (52,75; 38,23), R = 6,48.
- Hij ligt vóór paneel PC en de buis.
- De nieuwe pixels krijgen hun tint uit de kale reductie (licht bovenaan).
- Omlijning: zwart aan de schaduwkant (onder/rechts), navy elders.
- Rondheid over de hele omtrek: **−0,45 … +0,49 px** (35 randpixels).

## 3. Mast PB (boven)
- De punt linksboven van de eindkap is terug: pixel (34,13), navy, zoals in de kale reductie.
- Daardoor is de schuine bovenkant nu volledig zichtbaar. Er is niets geschoven.

## 4. Mast PF (onder)
- Volle lengte 47 modelpx, gelijk aan PB, met dezelfde vakgrenzen 1/3 en 2/3.
- Het paneelrecept is dat van herstel10.
- De bestaande PF-pixels zijn ongewijzigd. Nieuw is het stuk dat rechtsonder naast/onder PE uitsteekt: 10 px, x 38–40, y 52–55, in de donkerste vaktint met zwarte rand.

## Aandachtspunten
- De pupil van het voorste oog is 2×2, maar met één hoek in donker teal: rond gelezen, geen blok. Als dat nog te vierkant leest: alleen 3 px.
- De ring rechts bij de zij-ogen is 2 px paars. Op 8× leest dat als een flinke band, ongeveer zoals in het model.
- Of de PB-top met één pixel "volledig" genoeg is, ter beoordeling. De kale reductie geeft niet meer.
- Nog geen keurder geweest.
