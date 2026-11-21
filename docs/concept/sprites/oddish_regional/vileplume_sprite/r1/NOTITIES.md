# Kelp-/anemoon-Vileplume frontsprite, ronde 1

Bestanden: `vileplume_r1.png` (64×64, geïndexeerd, index 0 transparant, 14 kleuren incl. transparant), `kaal.png` (kale reductie), `bouw.py` (+ `kaal.py`), `vel.png` (r1 8× | model 8× / close-ups 12× krater, anemoon VL, lijf+poten naast het model / 1× licht en donker + model 1×).
Opnieuw bouwen: `cd vileplume_sprite; python3 gereedschap/natief.py; python3 r1/bouw.py r1`.

## Wat uit het model komt
- **Natief raster:** de randsterktezoeker geeft pitch 10,24 / fase 9,25 (zelfde als de Oddish), maar op een uitvergrote krater en tentakels zijn de echte cellen 5,12 px (half raster) → 200×200 natieve px, figuur 128×144 (x36–163, y28–171). `gereedschap/natief.py`.
- **Formaat:** 144 rijen → 62 (S = 0,43); 128 kolommen → 55. Figuur x3–58, y1–62 (56×62 incl. 1 klontlijn links). Met 56 breed zou hij 63–64 hoog worden, dus 55 breed (1 px marge boven, voet op y62). Vileplume in de game: x4–59, y5–56.
- **Kale reductie** (`kaal.py`): oppervlakteweging per spritepixel, meest voorkomende modelklasse; lijnklassen (zwart, R0, W0) winnen vanaf 30 % dekking. Palet = mediaan van de modelpixels per klasse (geen eigen kleuren). Achtergrond = vanaf de rand verbonden bijna-wit (het lijf is zelf bijna wit, e8f3eb).
- **Krater:** kale reductie (zwart/grijze rand, bruine binnenrand, roodoranje en geel gemeten in de kom); 4 px afwijking (buitenlijn/losse pixel).
- **Lijf, armen, poten:** kale reductie; poten 3 px (zie hieronder).

## De toegestane afwijking (Jordi, optie A): klonteren
Per anemoon (5 stuks, mondjes en schijfmaten gemeten op het natieve raster, `gereedschap/anemonen.py`):
- 9 sectoren van 40°, gedraaid tot de lichte modeltentakels zoveel mogelijk in de kernen vallen; richting van elke klont = massamidden van de modeltentakels in die sector; punt = 92e percentiel van waar de modeltentakels (tentakeltint + R0-lijnen) eindigen; lengte 0,45 (genormaliseerd) terug naar het mondje ("kort").
- Klont = dik lijnstuk, 2,4 spritepx breed, in de tentakeltint van het model (R3; bij de achterste T-anemoon R2, want daar heeft het model 9 px R3 en 200 R2).
- Lijf tussen de klonten in de schaduwtint R1 (kleur wijkt af van het model, waar het lijf R2 is; met R2 was er te weinig contrast met de tentakels).
- Lijnen: R0 aan de schaduwkant (rechts/onder) van elke klont en tussen twee klonten die elkaar raken; zwart waar een achterste anemoon aan een voorste grenst ("donkere rand om elke anemoon"); bij een punt tegen de achtergrond komt de lijn buiten de klont.
- Mondjes: ovaal (ring R0, binnen R2) precies op de bbox van de modelring; de verkleining maakte er een streepje van (benoemde reparatie, zoals een oog).

## Pixels die niet uit de kale reductie komen (900 px totaal)
Per zone: anemonen 806 (waarvan mondjes 35) · lijf+armen 36 · poten 54 · krater 4.
Per stap: klonteren + mondjes 752 · klont- en anemoonranden 281 (overlapt) · lijn midden in poot/lijf → vultint 17 · poten 3 px 45 · buitenlijn 110 · losse pixels 32.
De anemonen zijn bijna volledig opnieuw opgebouwd uit modelmetingen (dat is de afwijking van optie A); lijf, armen, poten en krater zijn de kale reductie met technische opschoning.

## Toets
- Kleuren 14 incl. transparant; transparency=0.
- Losse pixels: 14 over, allemaal bewust: 3 in de krater (geel/oranje/grijs, uit het model), 6 zwarte/R0 puntjes op de buitenrand (punten van tentakels), 3 rond de rechterarm, 2 op de rand van anemoon L.
- Lijnpixels midden in een vlak zonder lijnbuur: 0. Lichte kleur op de buitenrand: 0. Zwart 16 % (Gen 3 ±12–19 %).

## Zwakke punten (voor r2)
- De onderste klonten van de voorste anemonen lopen bijna tot de onderrand; in het model zit onder de tentakels een duidelijke rode band (de zijkant van de schijf).
- De lijn bovenop het lijf (kraagschaduw, een ondiepe U in het model) is twee losse streepjes geworden die als oogjes lezen.
- Rechterarm: trapje en gat bij de oksel (x41–44, y35–38).
