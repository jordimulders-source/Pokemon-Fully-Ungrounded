# Hoatzin fase 2, r3 (19 nov), maker

Reparaties van Claude op r2. Alles opnieuw: `sh alles.sh`. `vel.png` = r3 | r2 | model | Pidgeot, 1×/2×, kop 12×. Buikvarianten opnieuw op r3: `buik/` (zelfde 4 paletten, pixels identiek, assert).

## Wat er anders is (regels op modelmetingen, niets met de hand)
1. **Vleugelstrepen**: per pen een rechte lijn gefit (PCA) op de lichte modelstreep van die pen, getrokken tussen de uiterste modelpunten, alleen binnen die pen en niet op een pengrens; korter dan 4 aaneengesloten px → weggelaten. Geen 1–2-px streepjes meer.
2. **Voorrand voorste vleugel** (`voorrand.py`, `voorrand.png`): de grootste verbonden lichte band (L ≥ 125) in het armgebied van het model, op het raster gelegd, gaten langs de band gedicht, per rij 1–2 px → doorlopende lichte lijn (36 px) tussen lijf en donkere armpennen.
3. **Nek**: per cel het aandeel donker modelpixel (L < 55) in de nek; ≥ 65 % → donkere streep (#321E30), anders de lichte modeltint gemeten zonder de strepen; losse donkere stippen weg. Gevolg: diagonale losse strepen in plaats van één blok.
4. **Buik**: Gen 3-schaduw op een ellips gefit op de buikcellen (licht linksboven-voor): hooglicht #A57A98 linksboven, sikkel #7A5270 onder/rechts, midden #8E6280; geen losse vlakjes.
5. **Kuif**: per cel het aandeel lichtbruin (L ≥ 62) in de modelkuif: ≥ 50 % → streng (#98522C), anders donkerbruin ertussen; het donkere blok rechtsonder is opgesplitst (28 px gewijzigd).

## Afwijkingen t.o.v. de onderlaag (stap A), per zone
| Zone | px | afwijkend |
|---|---|---|
| lijf/vleugel (M) | 891 | 548 |
| vleugelstrepen (W) | 178 | 140 |
| kuif (C) | 124 | 21 |
| gezicht (F) | 27 | 11 |
| oog (E) | 7 | 3 |
| snavel (S) | 15 | 1 |
| buik (P) | 161 | 76 |
| poten (T) | 73 | 30 |
| staart (D) | 120 | 36 |
| modellijn (K) | 219 | 111 |
| buiten silhouet | – | 3 |
| **totaal** | 1815 | 980 (silhouet 3) |
Per regel: zie `r3.log` (pentoon 455, pengrens 322, strepen 66, voorrand 36, nek 51, buik 79, kuif 28, clusters 31, buitenlijn 268, oog 6).

## Resterende twijfels
- Pengrenzen blijven op een paar plekken onderbroken (57 kleine stukjes index 2, deels diagonale lijnen die 8-verbonden doorlopen).
- De buikschaduw is een regel-ellips, niet uit het model; de lichtvlek van het model zit op dezelfde plek (linksboven).
- De voorrand loopt van de schouder tot halverwege de buik; het onderste stuk van de vleugelrand tegen de buik is in het model minder licht en dus niet meegenomen.
