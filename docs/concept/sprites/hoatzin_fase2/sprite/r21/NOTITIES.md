# Hoatzin fase 2, r21 (20 nov): vanaf r20

`sh alles.sh` (bouw19 → kleur21 → check → vel). Vorm = r20 (alpha-diff 0). check.py: dambord 0, om-en-om 0, klonten 0. 16 kleuren, palet = r20.
Afwijkend t.o.v. r20: kuif 40, verre veren 34, vleugel 211 px; kop, nek, buik, staart, poten, oog/gezicht/snavel 0.

## Wat er veranderde (alles afgelezen op het model, niets getekend)
1. **Armpennen** (donker vlak): scheidingslijnen tussen de veren uit het model (`lijnen.VEER`; per spritekolom de donkerste modelpixels,
   profielmeting) als 4-verbonden lijnen in middentint 3 over 2. Vijf rijen veren, ±2,5 px uit elkaar, waaierend naar de achterrand.
2. **Slagpennen**: waaier rond C (33,23). `polar.py` meet per hoek het modellicht langs de straal: lichte schachten (maxima) en
   donkere scheidingen (minima) → `lijnen.SCHACHT` (5) en `lijnen.SCHEID` (2), vlak 3 (4 waar het model licht is). Schachten beginnen
   pas waar de buurschacht ≥ 2,5 px weg ligt (anders klonteren ze op 1×).
3. **Kuif**: hele kuifvlak 6; zeven plukken als polylijnen langs de modelstrengen (`lijnen.PLUK`, gecontroleerd met `overlay.py`):
   A buitenste links (dun, 6), B staand, C, D lange diagonaal, E en F naar rechts, G liggend boven het oog. Kern 7, donkere kant 2
   (alleen waar daarna nog vlak ligt). Plukken eindigen op verschillende hoogte zodat ze bij de basis niet tot één band samenklonteren.
   Selout van de kuif aan de lichtkant nu 2 (was 6 = zelfde als het vlak, dus geen omlijning).
4. **Vleugel tegen de staart**: de staart is bevroren (geen binnenlijn mogelijk), dus toonsprong aan de vleugelkant: vleugelpixels
   die aan de staart grenzen in 3 (model T 75–90 boven de zwarte staart).

## Gecontroleerd
- Onderdelen: nek/vleugel (neklijn), kop/kuif en kuif/verre veren (toonsprong), buik (eigen donkere rand), poten (lijn), vleugel/staart (nu toonsprong).
- Belijning: zwart aan de schaduwkant, selout in de donkere tint aan de lichtkant (boven/links), geen om-en-om.
- Naast Archeops/Braviary op 3× en 1×: de vleugel leest nu als waaier van pennen; kuif als bruine haardos met losse strengen.

## Zwak (eerlijk)
- Kuif: op 1× leest de onderste helft nog als bruin blok met lichte lijnen erboven; de modelstrengen steken buiten de massa uit, het bevroren silhouet niet.
- Binnenvleugel (x 28–38, y 34–46): model heeft daar korte lichte streepjes (tertials); meting gaf geen betrouwbaar signaal, dus vlak 3 gebleven.
- Model-staartgrens ligt verticaal bij x 39–40 (rijen 46–49 zijn in het model vleugel), maar het bevroren staartmasker (r16-knip op y ≥ 46) begint horizontaal; niet aangeraakt.
- vel.png: r21 | r20 | r17 | model op 8×, daarna kuif/vleugel/nek/poten op 16× (r21 | r20 | pixelblad | model).
