# Sauna-yeti – sprite ronde 4 (verse maker)

`sauna_yeti_r4.png` = **r2** (gezicht en vacht) + uit r3 **alleen** palet en stenen + gezicht per spritepixel **gemeten** uit het model. De gezichts- en vachtwijzigingen van r3 (egaal gezicht, weggehaalde vachtlijnen = pixelblur) zijn teruggedraaid. `bouw.py` (argument `log` print elke pixel met reden) maakt ook `vel.png`: r4 | r2 | model op 8× / gezicht 16× (sprite | natief model, zelfde uitsnede) / stenen 12× (2 schouders, buik/knie) / 1× op licht en donker naast fase 2 + model 1×.

r2 → r4: 202 px (P 70, S 60, G 72, AFW 1). r3 → r4: 90 px.

## Uit r3 overgenomen
- **P (70 px):** handen één tint (112,151,164) (gemeten gem. vlakke handcellen); plek 12 = rood (216,72,32) terug.
- **S (60 px):** stenen 1-op-1 uit r3 binnen hetzelfde steenmasker (model ≥ 45 % steen): rand 1 px rood waar het model ≥ 40 % gloed heeft, oranje naden, geel in de heetste naadpixels, geen oranje band.

## Gezicht gemeten (G, 72 px t.o.v. r2)
Zone rij 20–32, X 23–40 (wenkbrauw, ogen, neus, mond, wangvacht, kin); stenen, emmer, buitenlijn/randpixels en zwarte omlijning buiten de kern blijven. Per spritepixel de natieve modelcellen (pitch 5,867) waarvan het middelpunt erin valt (4–9 cellen):
- **zwart (2 px nieuw, 4 behouden):** per groep modelcellen L < 60 één pixel op het zwaartepunt van de groep (zo verdubbelt een groep op een pixelgrens niet). Groepen: zwaar linkerlid (28,24), linkerpupil (28,25), rechterpupil (34,24), neus (30,25), mondhaak (33,27).
- **lijn (41 px):** ≥ 2 cellen L < 150 (een 1-cel-lijn van het model raakt 2–3 cellen per spritepixel); tint = gemiddelde van die lijncellen → l of s (geen zwart). Zo kwamen terug/erbij: wenkbrauw-/rimpellijnen rij 21–22 (ook de rimpel tussen de wenkbrauwen (30,23)), oogleden rij 23 (links (27,23)(28,23) nu lijntint i.p.v. zwart: niet zwart in het model), onderrand ogen, wangvachtranden links (23–24, 24–27) en rechts (35–40, 21–30), kinvacht rij 31–32.
- **vlak (29 px):** mediaan van de niet-lijncellen → s/m/h/w.

### Afwijking van de meting (1 px)
- **(33,26) → l (AFW):** bovenkant van de mondhaak. In deze pixel valt 1 lijncel (natief x123,y43, het opgaande eind van de glimlach), onder de drempel van 2. Zonder deze pixel is de haak een plat eindje.

## Vacht kop/schouders
Zoals r2. Gezocht naar losse 1-px lijnpixels zonder lijnbuur buiten de gezichtszone (rij 14–39): **geen gevonden**, dus niets weggehaald.

## Controle
16 kleuren incl. transparant, bbox x1–62, y12–60 (= r2).

## Zelf nog zwak
- De meting legt de dunne modellijnen (±0,4 spritepx) op hele pixels: rij 23 rechts wordt één doorlopende lijn X32–38 (lid + wangvacht), het rechteroog heeft geen oogwit meer ((33,24) is 3/4 lijn in het model). Op 8× leest het gezicht drukker dan r2; ogen lezen als zware leden met pupil, minder als "halfopen oog met wit".
- Linkeroog: zwaar lid + pupil = 2 zwarte pixels onder elkaar ((28,24)(28,25)), rechteroog 1 zwarte pupil: asymmetrisch zoals het model, maar op 1× kan links als één streep lezen.
- Mondhaak hangt op 1 afwijkingspixel.
- Steenclose-ups in het vel: modeluitsnede schuift iets t.o.v. de sprite (zelfde afbeelding als vel.py van r1–r3).
