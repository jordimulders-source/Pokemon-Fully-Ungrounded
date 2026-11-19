# Hoatzin fase 2, r12 (19 nov), maker: reparaties op r11 na keurder-FAIL

`sh alles.sh` bouwt alles vanaf `../r11/hoatzin.png`: kuif12 → kop12 → nek12 → poten12 → staart12 → fix12 → check → vel.
`vel.png` = r12 | r11 | model | Archeops | Braviary (8x) + 1x/2x licht/donker, kop 12x r12 | model | r11.
`zoom.py in.png uit.png x0 y0 x1 y1 K` = uitsnede met raster naast dezelfde uitsnede van het model (meetgereedschap).
Vorm per onderdeel afgelezen op het model (`modelgrid.py`); kleur/schaduw/lijn met de hand op het raster.

| reparatie | wat |
|---|---|
| 1 kuif | het bruine blok is weg; 6 losse veren F1-F6 uit het model (F1 omhoog-links, tip 6,9; F2 omhoog, tip 10,9; F3 tip 16,9; F4 tip 23,7 in de lucht; F5 tip 26,12; F6 krult naar 28,19), elk 2 px (kern 7, schaduwkant 6) en 1 px naar de top, donkere top 2; over de verre vleugel alleen een donkere lijn 2 aan de schaduwkant, tegen de lucht rondom (1 schaduwkant, 2 lichtkant). Een 7e, doffe streng (6) laag in de nekschaduw (19-23, 20-21). Tussen de veren: de donkere verre vleugel. |
| 2 kruin | ronde donkere kruin y16-19 (x8-18), 6 met 7 op de boog linksboven en 2 rechtsonder; links langs het gezicht tot y21. Geen rechte lijnen op y18/y20; veren groeien uit de kruin. |
| 3 oog | 5x5 rond (x11-15, y20-24, hoeken blauw): zwarte ring, 3x3 rood met zwart puntje in het midden (13,22), glanspixel (12,21). Blauwe vlek 7x7 (x10-16, y19-25), 8 rechtsonder. |
| 4 nek | eigen vorm: voorkant 5, vlak 4, sikkel 3 (2 px) rechts, binnenlijn 2 waar de vleugel over de nek valt; nekschaduw onder de kuif loopt schuin (2→3); 4 korte strepen (3) schuin rechtsomlaag langs de nekcurve (vleugellijnen lopen linksomlaag en zijn 2). |
| 5 nabije voet | rechter (lagere) voet: 3 gespreide tenen (links, omlaag, rechts) met transparante gaten, F/E/2, zwarte klauwen (26,58-59), (30,62-63), (38,58)-(39,59). |
| 6 verre voet | linker voet: lange teen naar links + korte teen omlaag, E/2 (geen F, een stap donkerder), klauwen (15,57-58) en (23,60-61). |
| 7 verre vleugel | lobben opnieuw naar het model (toppen 8-9/3, 12-13/3, 16-17/5, 19-20/8, schuine rechterrand tot 27/21); toppen links selout 2, rechts zwart; rechterrand zwart, linkerrand selout 2. Fill 3, lichte linkerkolom 4 per lob, scheiding 2 vanuit de inkeping. |
| 8 snavel | bovensnavel F/E met haak linksonder, bekspleet 1 px zwart (y25), lichte onderkaak F/E (y26); geen donker blok. |
| klein | staart: 3 lange vlakken (3) met 2 scheidingen (2), schaduw 2 bovenin en langs de rechterrand; buikrand: 2 waar de vleugel over de buik valt (x25-27, y36-42). |

## Afwijking van de keurderopdracht (bewust)
- Nabij/ver: de keurder noemde de linker voet (x16-27) nabij en de rechter (x29-38) ver. In het model staat de rechter voet lager (tot y63) en vóór de linker, en heeft hij 3 tenen; de linker heeft er 2. Ik volg het model: rechts = nabij (3 tenen, F/E/2), links = ver (2 tenen, E/2, donkerder). Zelfde tellingen als de opdracht, alleen andersom geplaatst.
- Oog 5x5 in plaats van 4x4: in 4x4 raakt de pupil altijd de ring en zie je geen zwart puntje in het rood; 5x5 met ronde hoeken geeft 3x3 rood met een vrij puntje (modeloog 11-14 × 20.5-23.5, dus 1 px groter).

## Script-check (`check.py`)
dambord 0, om-en-om 0, zwarte binnenklonten 0. 16 kleuren (index 0 transparant), palet ongewijzigd t.o.v. r11.

## Afwijking t.o.v. r11
489 px anders, silhouet 57 px. Kuif + verre vleugel + kruin 243, kop/oog/snavel 65, nek 89, poten 74, staart 78.

## Zwakke punten (eerlijk)
- Kruin + veerbases (x6-18, y14-19) blijven een vrij grote bruine massa; de veren lezen wel als losse veren, maar minder fijn dan de haarstrengen van het model.
- Oog is groot en vierkant-achtig op 8x (5x5); op 1x leest het als rood oog met zwart puntje.
- Snavel blijft klein t.o.v. het model (gezicht valt over de basis), zoals in r10/r11.
