# Kudu sprite ronde 3 (maker)
Benoemde reparaties uit de r2-keuring (Claude), punt 1-6.

## 1 Model A3 (`manen_a3.py`, crop 2x: `model_A3_crop2x.png`)
De rechte snede en het blok uit A2a zijn weg. Alleen verschuiven en spiegelen van modelmateriaal:
- Kopie van het halsdeel van de r3b-manen (+70,+30), alleen links van x455. Daar ligt hij over de oude manen; het is de A-verbreding.
- Over de schouder ligt de keelfranje van r3b (x190-300, y520-770), **horizontaal gespiegeld**. Die lokken eindigen in het model in punten naar linksonder, met hun eigen zwarte lijn; gespiegeld vallen ze naar rechtsonder over de schouder. Geplaatst op x455-565, y480-730.
- De kamlokken van r3b weer bovenop, zodat de bovenrand van de gespiegelde lokken eronder verdwijnt.
- Gespiegeld = andere lichtrichting op die lokken; in de sprite worden de lokken per lok opnieuw belicht (punt 2).

## 2 Manen
- **Hoofdstrengen:** de lange zwarte modellijnen tussen de lokken, als skelet op hun gemeten plek, max. 6. Een lijn die voor >40% vlak naast een al gekozen lijn loopt (dubbel door origineel + kopie) valt af. Gekozen skeletlengtes (×4 modelpx): 129, 87, 70, 47, 34, 26. Ze worden `d`.
- **Overige modellijnen in de manen:** worden haartint.
- **Haartint per cel:** de meest voorkomende haartoon van het model (licht ≥140, midden 118-140, donker <118), dus harde toongrenzen en geen gemiddelde.
- **Lokken:** tussen twee strenglijnen is de fijne haartextuur van het model smaller dan 2 spritepx. 1-op-1 gaf een zebra ("dldld"). Per lok staat daarom de lichte kant (gemeten: welke helft is in het model lichter) als `l`, de andere kant als `m`, de strenglijn als `d`.
- Niets gemiddeld of gladgestreken.

## 3 Flankstrepen
- Per witte modelstreep (lum ≥200, blauw >120; 5 strepen gevonden) een doorlopende 1-px-lijn: per spritenrij de kolom van het streepmidden in het model.
- Lengtes: 13, 12, 10, 12 en 8 rijen.
- Wit naast een streep wordt vacht.

## 4 Hoorns
- **Breedte (gemeten):** modelhoorn inclusief lijn 2,6-3,4 spritepx (halve breedte 1,3-1,7). De band is 4 px (2 binnen) tot 85% van de lengte, daarna taps naar 3; voor licht én donker binnen zijn 2 binnenpixels nodig.
- **Binnenkant per pixel uit het model**, over de breedte vergeleken:
  - lichtste kant W als het model daar ≥20% wit heeft (voorkant van de draai / slijprand), anders 4;
  - andere kant 3 (grijze achterkant van de draai).
- **Staal donkerder gezet** zodat de afwisseling leest: A #3C4864 (selout en binnenlijn), 3 #62749A, 4 #B4C4D8, W wit.

## 5 Oog (`oog.py`, `oog_varianten.png`, hoofd op 8x)
Alle drie geplaatst met het oogmidden op het modeloog (spritecel 12,23).
- **a (in r3):** impala af (B3), box x18-24, y22-26, 1-op-1, alleen omgekleurd. Impalatinten 1→0, 2→K, 3-4→D, 5-6→M, 7→L, 8→W.
- **b:** Stantler `anim_front_gba.png`, box x23-29, y23-27, 1-op-1. Stantlerkleuren: bruinzwart (index 5) en zwart → lijnkleur 0, wit → W, goud → L/M/D, grijs → 4.
- **c:** modeloog met lid: lidlijn rij 22 (x10-13), daaronder wit|pupil|wit|ooghoek.

## 6 Hoeven
- **Impala gemeten:** hoef 4-5 px breed tegen een poot van 3, 2-3 rijen, donkerste tint met zwart rechts/onder.
- **Kudu:** per poot (component onder rij 50) de onderste 2 rijen, 1 px breder naar rechts; binnen K, rechts/onder zwart.

## Pixels t.o.v. de kale reductie (model A3, omgekleurd naar het palet; 619 van 1362)

| Zone | Pixels |
|---|---|
| manen | 228 |
| vacht | 218 |
| staal | 142 |
| donker (hoeven) | 19 |
| roze | 11 |
| wit | 1 |

Per stap en per pixel: `telling.txt` en `wijzigingen.txt`. 15 kleuren incl. transparant.

## Eigen zwakke punten
- **Manen:** donkerder en bruiner dan het lichte goud van het model; de lokken lezen nu als strengen, maar de schaduwkant (donker in het model) is groot.
- **Hoorns:** de spiraal leest beter (wit/donker per draai), maar de band blijft smal en heeft trapjes. 4 px is al iets breder dan het model (±3).
- **Flank:** tussen de strepen staat de lichte modeltint L in vlekken.
- **Oog a:** neemt de lichte vacht (impalatint 7 → L) rond het oog mee, dus er staat een licht vlakje rond het oog.
- **Gespiegelde keelfranje:** lijnen staan rechts in plaats van links; in het model gelden ze daar als lijn, in de sprite worden ze binnenlijn.
