# Keuring spooktrein fase 2, sprite_r5 (16 nov)

**Oordeel: FAIL (dichtbij).** Eis 1 (trouw) is in orde. Op 1× en 8× naast `sprite_r5/model_geschaald.png` kloppen pose, wagen met banden, scheuren, wielen, wolk en spookwiel. Hij zakt nog op een paar punten van eis 2: de omlijning van de vuist, ruis en te veel bruintinten in de wagen, geen donkere schaduwrand aan de wolk, en een te lichte schaduwkant van de geest. Niet beoordeeld: het gezicht (x25–42, y9–26), de weggegumde onderdelen en de ingedrukte staart.
Gemeten: helderheid van de paletindexen, clusters (4- en 8-verbonden), samenstelling van de buitenrand, en modelhelderheid per spritepixel. Naast haunter, banette, shuppet en magneton zijn de geest en de wagen veel vlakker en drukker.

Helderheid per index: 2=217, 6=203, 3=174, 4=148, 5=103 · 7=137, 10=107, 8=91, 13=68, 9=55, 1=33.

## Reparaties (belangrijkste eerst)
1. **Vuist, linker- en bovenrand x50 y6–12 en (56–57,6), (49,15)**: hier staat tint 9 (donker wagenbruin, 55) op de lichtkant van een groen onderdeel. Eis: selout aan de lichtkant, in de groene omlijning. Het model heeft hier een middengroene rand (x50: 143–172). Zet tint 5 (of 4) en houd het zwart op de rechterrand. Nu bestaat de rand uit 1:12, 9:11 en 5:10 door elkaar, en (49,15) is een 9 tussen twee 5'en.
2. **Bruin hout, contrast en tintaantal**: de wagen gebruikt 7/10/8/13/9 + 1. Tint 10 tegen 8 scheelt 16 en 13 tegen 9 scheelt 13, terwijl de eis ±30–40 is. Gevolg: gespikkelde vlakken. Dit stond al in r4 punt 10. Breng elk vlak terug naar ≤3 houttinten + omlijning met stappen van ≥30, per vlak gekozen op de modelhelderheid. De rechterflank (x36–50, y30–44) is in de sprite 114 en in het model 94: de flank mag donkerder.
3. **Spikkels in de wagen (< 3 px, 8-verbonden)**: tint 9 komt 19× voor, onder andere (26,23),(29,24),(31,25),(27,26),(33,26),(37,28),(45,32) en de onderkant (33,45),(42,45),(48,45),(35,46),(39,46),(41,47),(43,49). Tint 8 komt 9× voor (o.a. (22,32),(18,33),(48,34),(49,36)) en tint 10 7× ((25,27),(19,28),(6,30),(9,30),(4,35),(27,37),(38,41)). Neem de nerven en banden uit het model over als vormen van ≥3 px, of laat de spikkels opgaan in het vlak eromheen. Er staat nog een losse zwarte pixel op (39,47), midden tussen 13 en 9.
4. **Wolk zonder schaduwrand**: de buitenrand van de wolk (y ≥ 48) bestaat uit 92 px tint 5 en 4 px zwart. Eis: zwart of de donkerste lijntint aan de schaduwkant (onder en rechts), selout alleen aan de lichtkant. Op (52,42) staat een 5 tussen twee 1'en: dat is om en om.
5. **Schaduwkant van de geest te licht**: de rechterkant van de kop (x42–46, y8–20) is in de sprite 190 en in het model 168. De arm (x44–50, y15–21) is 189 tegen 164, de vuist 184 tegen 164. De kop is bijna helemaal tint 2, met maar een smalle sikkel van 3. Verbreed de sikkel van 3/4 aan de rechter- en onderkant zoals het model hem toont. Tint 3 tegen 4 scheelt maar 26: spreid die iets (≥30).
6. **Rij 7 van de vuist, x51–54 "4444"**: een streep van 1 px middentint direct onder de lichte bovenrij. Dat is banding evenwijdig aan de rand. Het model (y7: 154–204) toont hier geen doorlopende donkere rij. Neem het vlak uit het model over.
7. **Kleine groene snippers**: tint 3 staat los op (12,24),(8,29),(11,29) en de rand (62,56). Tint 4 staat los in de wolk op (31,47),(36,50),(45,60). Laat ze opgaan in het vlak, tenzij ze bij een scheurlijn horen.

## Punten uit r4
Opgelost: 1 (linkerrand wagen), 2 (rechterrand kop), 4 (krul), 6 (bovenrand wagen), 9 (tint 6 uit de geest), 11 (banding in de linkerlob van de wolk). Punt 5 (inkeping kop-arm, x22–24 y19–21) is in orde: het model is daar ook achtergrond (208–255).
Deels opgelost: 3 (knokkellijn wel, de lichtkant van de vuist nog donker; nu 9 in plaats van zwart, zie 1), 7 (de meeste losse zwarte pixels zijn weg, (39,47) staat er nog), 8 (van 58 naar 19 spikkels tint 9).
Niet opgelost: 10 (contrast 13/9, zie 2).
