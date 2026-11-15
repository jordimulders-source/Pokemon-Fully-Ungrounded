# Keuring welp p6 (onafhankelijke keurder, 15 nov)

**Oordeel: FAIL**

Bekeken: p6 op 8× en 12× naast p4 en het model, kop, tong/poot en staart op 16×, 1× en 3× naast Growlithe, Vulpix en de steenjaguar. Palet gelijk aan p4 (index 0 = transparant).

## Hoofdvraag: zou Jordi dit nu mooi vinden?
Nee. p6 verschilt maar **38 pixels** van p4 (voorhoofd 15, rugkrul 9, tong 4, staart 10); de romp is ongewijzigd (goed). Op 1× en 3× is p6 nauwelijks van p4 te onderscheiden. Van de vier verzoeken is alleen de staart duidelijk opgelost; de tong half; het lila deel bovenin en het voorhoofdspatroon niet. Jordi zag p4 en zal bij p6 dezelfde punten terugzien.

## De vier punten
1. **Tong en poot: half.** De nieuwe donkere lijn (index 2) op y=41, x=10–13 scheidt ze op 8×. Maar direct onder die lijn liggen nog twee lichte, roze-achtige pootpixels (index e = 204,166,148) op **(12,42) en (13,42)**, recht onder de tongpunt (12,40)c en (13,40)f. Op 1×/3× lezen die als het vervolg van de tong door de lijn heen: de tong lijkt nog steeds op de poot te liggen/plakken.
2. **Lila deel bovenin: niet opgelost.** De rugband is niet veranderd: een 2 px strook licht lila (index 8) die van (33,32) tot (40,38) **direct tegen de buitenlijn (index 1)** aan ligt, met daarbinnen een rij index 7: 1|8|8|7|4 parallel aan de rand. Dat is banding en een lichte kleur op de buitenrand; het leest als randlicht/glitch langs een kaarsrechte 45°-rug. De eindkrul (38–41, 38–42) is alleen hergekleurd naar donkerlila (index 6) met 8 erin: een vierkant grijs-paars blokje ("G"/meanderhaakje), geen ronde krul. In het model ligt de band naar binnen (bruin tussen band en rand) en eindigt hij in een ronde, open spiraal. Ook het voorhoofd heeft hetzelfde probleem: lila (8) op y=20, x=16–21 direct onder de kopomlijning.
3. **Voorhoofdspatroon: leest niet als de golvende band.** Vorm in p6: een rechte horizontale rij (y=20, x=16–21) die met een rechte 45°-diagonaal naar linksonder loopt tot (12,25), met daarin een donkerbruine diagonale groef (index 3: (18,21),(19,21),(20,21),(15–17,22),(14,23)) en index 7-stukjes. Dat leest als twee schuine strepen / een haak naar het oog, niet als een golf. Het model toont één band over de bovenkop met een duidelijke golf (dal en bult, "~"), links omkrullend.
4. **Staart: opgelost.** De rechte crème streep langs de onderrand (p4: x=52, y=53–56) is weg; de ring ligt nu dwars over de staart als een getrapte, licht gebogen band (b op (53,52),(54,52),(54,53), lila 8 op (53,53), 9 op (55,53)). Leest als ring, crème + lila zoals het model.

**Lichaam niet veranderd:** klopt, diff valt alleen in de vier zones.

## MOET-reparaties
1. **Tong/poot:** (12,42) en (13,42) van index e naar 5 (of 4), zodat er onder de lijn geen roze-achtige kleur meer direct onder de tong zit. Daarna op 1× controleren dat tong (roze) en poot (bruin) losstaan.
2. **Rugband van de rand af:** de band 1 px naar binnen, met bruin (3 of 4) tussen buitenlijn en band. Concreet: de pixels index 8 die aan index 1 grenzen — (33,32),(34,33),(35,34),(36,35),(37,36),(38,37),(39,38),(40,38) — naar 4 (bovenste helft) / 3 (onderste helft); de band (8 met 7 als schaduwkant) één rij lager/naar links leggen, volgens de bandvorm van het model, geen strook die de rand volgt.
3. **Eindkrul rond en licht:** vervang het blokje (38–41, 38–42; nu 6/8/7/3) door een ronde, open krul zoals in het model (ringvorm van 8 met 7 aan de schaduwkant, bruin hart 3/4 zichtbaar, ±5×5 px), zonder index 6 (het donkerlila maakt hem grauw en vierkant).
4. **Voorhoofd als golf:** maak van de band één golvende strook: links omkrullend bij (12–14, 21–23), daarna een dal rond x=16–17 (y=22) en een bult rond x=19–20 (y=21), naar rechts uitlopend richting oor; haal de rechte rij langs de kopomlijning (y=20, x=16–21) los van de rand (bruin ertussen, zoals punt 2), en laat de band niet als diagonaal tot (12,25) tegen de wenkbrauw doorlopen. Geen donkerbruine groef (3) als derde streep: binnen de band alleen 8 + 7.

## MAG
- Staartring kan 1 px breder (lila 8 ook op (54,54)) zodat hij op 1× nog iets beter leest.
- De rug is een kaarsrechte 45°-trap van (29,26) tot (47,44); het model heeft een licht gebogen schouder. Valt buiten de opdracht ("lichaam niet veranderen"), dus alleen noemen als Jordi het vraagt.
- Algemeen weinig contrast naast Growlithe/Vulpix (bruin op bruin); geen punt voor deze ronde.
