# Kelp-/anemoon-Vileplume frontsprite, ronde 7 (keuring r6 verwerkt)

Bestanden: `vileplume_r7.png` (gelaat B, standaard), `vileplume_r7_gelaatA.png`, `vileplume_r7_gelaatC.png`, `kaal.png`, `bouw.py` (`python3 r7/bouw.py` vanuit `vileplume_sprite/`), `uitvoer.txt` (tellingen + tekstraster), `vel.png` (r7 8× | r6 8× | model 8× / 12×: krater, achterste anemoon L, voorste anemoon VL naast het model / 1× licht/donker + model 1×).
64×64, 4 bpp, 16 paletplekken (palet = r4), index 0 transparant (transparency=0). Figuur x2–60, y1–62.

## Keuring r6, per punt
1. **Toppen (L, R, T):** geen losse 1-px-spikes meer. Elke gemeten modelpunt is een afgeronde vinger van ±2 px (capsule r 0,95 rond de as mondje → modelpunt, dus waaiervormig: L leunt links, R rechts), licht R3 met de schaduwkant R2. De schijf van de achterste anemonen ligt boven lager (b_boven L 3,6 / R 3,4 / T 2,0), zodat de vingers als in het model ±4–5 px uitsteken. Waar twee vingers elkaar raken, wordt de pixel die het verst van zijn eigen as ligt een donkere scheiding (R0, zwart aan de schaduwkant). Omlijning alleen om de vingers.
2. **Voorste kronen:** de hele kroon is licht (tentakels); per twee tentakels loopt één doorlopende scheidingslijn in R1 van de lichte ring rond het mondje tot de rand (één rechte lijn per sector, 1 px breed). Daardoor is elke tentakel één doorlopende straal. Geen wiggen meer, dus geen losse streepjes.
3. **Krater:** per rij overgenomen van het model (30× met raster): ovale zwarte rand met gebogen boven- en onderlip (x24–39, y10–17), lichtgrijze binnenrand boven/opzij, bruine schaduw onder de bovenlip (y11), **lensvormig bad**: y12 roodoranje x28–35, y13 oranje x26–37 met geel x29–34, y14 oranje x28–35 met geel x30–33; bruine band y15, donkergrijze onderwand y14–16. De keel eronder blijft de kale reductie. 26 px anders dan r4.
4. **Gelaat:** B blijft standaard. De ogen (1×2 zwart) staan één rij lager (y33–34), zodat de lichte modelrij y32 tussen de zwarte kroonrand en de ogen blijft. Het balkje van het model schuift mee naar y35. C = B zonder balkje. A = model (U).
5. **Licht/volume:** licht linksboven; de schaduwsikkel rechtsonder in elke kroon (0,55·nx + 0,83·ny > 0,75) is R2. De tentakels liggen nu als stralen over de hele schijf.
6. **Beeneinden:** linkerpoot loopt licht uit tot de laatste rij (y59 lijn | licht | zwart) met eronder een zwart kapje van 2 px (y60, x21–22), zoals het model (y59 + kap y60). Rechtervoet was al gelijk aan het model (licht tot y61, kap van 2 px op y62) en is niet aangepast.

## Telling
- T.o.v. de kale reductie: anemonen 765, krater 61, lijf+armen 43 (gelaat), poten 102.
- T.o.v. r4: anemonen 714, krater 26 (punt 3), lijf+armen 10 (alleen gelaat B, punt 4), poten 72 (linkerpoot + kapje); rechterpoot 0 (geassert, net als lijf en armen buiten het gelaat).
- Gelaat: A t.o.v. B 10 px, C t.o.v. B 3 px.

## Toets
- 16 kleuren; lichte kleur op de buitenrand 0; lijnpixel midden in een vlak 0; zwart 17,6 %.
- Losse pixels 15: 8 in de vingertoppen van T en R (y1–4: kapjes en scheidingen tussen de korte T-vingers), 2 lichte vingertoppen (11,8) (7,10) van L, 2 buitenlijnhoekjes (9,24) (10,25), 3 in de bevroren arm-oksel.

## Twijfels (eerlijk)
- **T-toppen** (x25–41, y1–4) lezen nog als een kammetje: de modelpunten van T liggen ±3 px uit elkaar en de vingers zijn maar ±2 rijen lang, dus licht/donker wisselt daar nog dicht (2 licht : 1 donker, geen 1:1 meer). Klonteren tot ±5 T-vingers zou rustiger zijn, maar is minder dan het model; vraag of dat mag.
- L en R: tussen vingers aan de basis staan donkere scheidingspixels; op 8× lezen ze als vingers met kerven, op 1× als stekelige rand.
- Scheidingslijnen in R1: rustig en doorlopend, maar zachter dan de zwarte lijnen in het model. Met `--tussen=2` (R0) is er meer contrast, maar dan vallen de mondringen weg tegen de lijnen.
- Ik heb na punt 5 geen aparte keurder gedraaid.
