# Sneeuwmonster fase 2 – sprite ronde 3 (maker)

`sneeuwmonster2_r3.png` = r2 + de drie benoemde reparaties van Claude; de rest is r2 (57 px verschil: emmer 36, mond 9, stenen 12).
`bouw.py` (start van r2), `vel.png` = r3 | r2 | model, nieuw meetscript `../gereedschap/naden.py`.

## 1. Mond (golvende glimlach)
Lijnprofiel van het model per halve natieve kolom (onderkant van de mondlijn, in spritecoördinaten):
x20,6–21,1 → 24,7–25,5 (linkerhoek omhoog) · x21,6–23,5 → 25,7–26,1 (laag) · x24,4–27,2 → 25,3–25,5 (bultje omhoog) · x27,7–28,8 → 25,7–26,1 · x29,1–33 → 26,2–26,9 (dip) · x34,5 → 26,1 · x34,7–34,9 → 24,7–25,6 (haakje omhoog, zwart in het model).
Rijgrens op 25,75 gelegd zodat de golf van het model in 1 px blijft: pad (20,24) (21,25) (22–23,26) (24–27,25) (28–33,26) (34,25) (35,24). Eén pixel dik, alles lijntint 2 (donker blauwgrijs); het zwarte eindje van r2 is nu ook tint 2. Oude mondpixels eerst naar wit. Afwijking: het haakje rechts eindigt op (35,24) i.p.v. (34,24), zodat het niet tegen het rechteroog plakt.

## 2. Emmer (duigen + bovenrand)
- **Donker hout opnieuw gemeten**: de mediane modelhelderheid van het hout in de rechterhelft is 85–97 (het model gebruikt daar een midden-donkere schaduwtint met zwarte naden). Palet 7 is nu die schaduwtint (132,78,42) i.p.v. (104,60,32); daardoor is de rechterhelft niet meer een bijna zwart blok.
- **Naden** (`naden.py`): naadpixel = houtpixel ≥22 donkerder dan het lokale houtgemiddelde (17×17) of zwart. Gemiddeld naadaandeel per kolom, apart boven en onder de band; pieken: boven x31 (0,29), x34 (0,23), x40 (0,32), x44 (0,24); onder x28 (0,22), x32 (0,33), x35 (0,20), x39 (0,46), x41 (0,29), x44 (0,50). Tussen x35 en x39 boven heeft het model geen naad (lichte duig), dus daar ook niet.
- Per rij volgt de naad het naadmaximum binnen ±1 kolom (licht schuin zoals in het model). Kleur: donker hout op licht/midden hout, zwart op donker hout (het model heeft daar zwarte naden). Losse 1-px naadstukjes teruggezet; geen zwart tegen de sneeuw (onderlijn emmer blijft hout).
- **Bovenrand**: eerste houtrij onder de buitenlijn = lichte rand (licht hout t/m x40, midden hout rechts), zoals de lichte strook langs de bovenkant in het model. Band ongewijzigd.

## 3. Stenen (gloeirand rondom)
Per randpixel het gloedaandeel van het model gemeten: randpixel (zwart) met ≥8 % gloed → rood (13); sneeuwpixel tegen de steen met ≥20 % gloed → rood (gloed die in het model buiten de zwarte rand steekt). Erbij: bovenste steen (26,35)(27,35)(28,37)(21,36), onder (23–25,41); onderste steen (25,43)(21,44)(21,47)(21,48). Oranje/geel en scheuren binnenin = r2. Bovenkant en linksmidden blijven zwart: daar meet het model 0 % gloed op spritemaat.

## Maat en controle
bbox x8–55, y3–58 (48×56), 1780 px; 16 kleuren incl. transparant; geen lichte kleur op de buitenrand. Losse zwarte pixel (41,16) = 2-px zwarte naad in het donkere hout (bewust).

## Zelf nog zwak
- Emmer: de naden in het lichte deel linksboven zijn kort (2–4 px); de modelduigen zijn daar fijner dan 64 px kan tonen.
- Stenen: bovenkant zonder gloed (zoals gemeten); als de gloeirand rondom ook bovenop moet, is dat een keuze, geen meting.
