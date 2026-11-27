# Regionale Staryu (koekje) r4: nieuw model `gemini/r4_staryu.png`

Jordi koos dit model: "staryu r4 is uitstekend ja". Het staat in driekwart, als gekantelde ster. Het r3-model stond "te recht".

Bestanden:
- `staryu_r4.png`: 64×64, mode P, index 0 transparant, 14 kleuren.
- `kaal.png`: de kale reductie.
- `vel.png`:
  - bovenaan r4 8× | kaal 8× | model op dezelfde schaal 8×;
  - in het midden close-ups 12× van bovenarm, juweel, linkerarm, rechterarm en benen (sprite | model);
  - onderaan 1× op wit, crème, donker en zwart, met model 1×, Gen 3 Staryu en Starmie 1×, en de maatstaf-sprites Skinguin, Dundragoon, Zapacha en Princadee 1×.
- `bouw.py`.

Gereedschap: `../gereedschap_r4/`. Dat is een kopie van `gereedschap/` met de r4-rastermaten. Erbij gekomen: `armen.py` (armhoeken en -lengtes) en `naast.py`.
Bouwen: `cd staryu_regional/staryu && python3 sprite_r4/bouw.py`.

## Metingen
- **Raster:** pitch 10,24, fase x 9,35 / y 9,25. Natief raster 99×99, figuur x11–91, y7–90 (81×84, 3921 px).
- **Schaal 0,50:** een exacte 2×2-reductie. De figuur is 41×42 op x11–51, y12–53, 994 px. Gen 3 Staryu is 43×44 en 910 px.
  - Ik heb een exacte halvering gekozen in plaats van 0,49. Bij 0,49 schuift het raster en breken de chips.
  - 994 px ligt net boven de 980. Gemeten op dezelfde maat is het koekje boller dan de puntige Staryu.
- **Niet gespiegeld en niets rechtgezet.** Armhoeken en -lengtes vanaf het juweelmidden (`armen.py`, model omgerekend naar spritecoördinaten):

| arm | hoek model | hoek sprite | lengte model | lengte sprite |
|---|---|---|---|---|
| rechterarm | 10,9° | 10,6° | 24,3 | 24,4 |
| bovenarm | 70,6° | 70,3° | 20,8 | 20,7 |
| linkerarm | 159,2° | 157,9° | 17,2 | 17,3 |
| linkerbeen | 233,3° | 232,9° | 23,6 | 23,2 |
| rechterbeen | 304,9° | 303,1° | 26,1 | 25,7 |

  De armen zijn ongelijk (17–26 px) en de hoeken liggen niet 72° uit elkaar, net als in het model. Alle afwijkingen zijn ≤ 1,8° en ≤ 0,4 px. Het juweelmidden ligt in het model op (27,4; 31,9) en in de sprite op (27,5; 32,0).

## Kale reductie (`kaal.png`)
Zelfde klassen als r2, inclusief `naden_uit`: chocoladecomponenten kleiner dan 15 natieve px buiten het juweelvak tellen als deeg. Er zijn 12 echte chips, alle ≥ 15 px; de rest is ≤ 5 px. Zo komen er geen losse chipbruine pixels in de naden.

Oppervlakteweging per spritepixel:
- zwart wint vanaf 30 %;
- juweel wint vanaf 35 % en krijgt de meest voorkomende modeltint. De drempels zijn gemeten op dit model: rand 0–3, donkerrood 33–45, rood 80–88, roze 146–155, glans 200;
- chocolade wint vanaf 35 %, met de chiprand uit het zwart van het model.

**Deeg (nieuw t.o.v. r1):** dit model heeft één vlakke hoofdtint (L 193) met schaduwvlakken (148) en barsten (90–120). Een vaste drempel gaf een plat, licht koekje. De tint komt nu uit een gladgestreken toonkaart van de modelhelderheid (5×5 natieve px, alleen deeg). De drempels komen uit de eigen verdeling: licht ≥ 173 (bovenste 30 %), schaduw < 133 (onderste 22 %). Het volume komt dus per pixel uit het model; er is niets met de hand gezet.

## Afwijkingen van de kale reductie: 180 px (silhouet-diff 0)
**Per zone (`zones.py`):**

| zone | px |
|---|---|
| bovenarm | 39 |
| linkerarm | 30 |
| rechterarm | 31 |
| juweel | 20 |
| linkerbeen | 38 |
| rechterbeen | 22 |

**Per stap:**
- **Buitenlijn (60):** zwart aan de schaduwkant (achtergrond rechts/onder), selout 2 aan de lichtkant. Zwart uit het model blijft zwart.
- **Barstjes (72):** dunne donkere deeglijnen van het model (L < 135, lijnstuk ≥ 6 natieve px, ≥ 3 px van de rand) zijn per modelpixel naar de sprite geprojecteerd en worden 3. Daarbij zijn ook de naden van het juweel naar de inkepingen. Plek en vorm komen uit het model.
- **Ontkorrelen deeg (9 + 11):** tintvlekjes < 3 px in het deeg nemen de buurtint aan. Barsten zijn bevroren.
- **Chipglans (12):** per lichtpuntje in het model één glanspixel op de gemeten plek. Er zijn 12 glanspixels voor 12 chips; meestal schuift het bestaande glanspixel 1 px naar de modelplek.
- **Juweelrand (14):** de ring is gesloten, met 10 boven/links (het model is daar donkerrood) en 9 onder/rechts (het model is daar zwart).
- **Juweel binnenring (3):** de 1-px concentrische donkere ring van het model is geprojecteerd en wordt 10. Op deze maat blijven er maar 3 pixels van over.
- **Om-en-om lijn (4):** een lijnpixel tussen twee lijnburen van de andere lijnkleur krijgt die kleur (les keuring r1). Daarna zijn er nergens meer afwisselingen zwart/selout.
- **Outline highlights (5):** de lichtste selout-pixels volgens het model (gemiddelde deeg-L ≥ 145, binnenbuur licht, ≥ 2 px van zwart) worden 3. Dat zijn (26,19), (25,20), (19,23), (41,24) en (15,39). Het zijn er minder dan in r3 (10), omdat dit model rondom een getoaste donkere rand heeft.
- **Losse zwarte pixels:** 0.
- Er staat geen pixel in die niet uit het model of uit deze technische stappen komt. Niets is getekend, rechtgezet of symmetrisch gemaakt.

## Palet
| index | rol | kleur |
|---|---|---|
| 0 | transparant | — |
| 1 | zwart | (24,16,16) |
| 2 | selout | (146,74,34) |
| 3 | schaduw/barst | (198,112,50) |
| 4 | deeg midden | (228,160,72) |
| 5 | deeg licht | (244,198,118) |
| 6 | chiprand | (56,26,18) |
| 7 | chipmidden | (102,54,36) |
| 8 | chipglans | (206,160,140) |
| 9 | juweel donkerst | (92,18,24) |
| 10 | juweel donkerrood | (178,34,40) |
| 11 | juweel rood | (228,60,56) |
| 12 | juweel licht | (244,128,122) |
| 13 | juweel glans | (252,212,204) |

Selout en schaduw komen uit het r3-palet.

## Controle
64×64, mode P, transparency 0, 14 kleuren. Zwart is 8,1 % van de figuur. Geen lichte kleur op de buitenrand en geen losse zwarte pixels.

Vlekjes < 3 px die over zijn:
- chipmidden/-rand: chips zijn 3–4 px;
- glans: bewust 1 px;
- juweeltinten: 1-px ring en glans;
- barststukjes;
- de 5 outline highlights;
- 4 middendeeg-pixels;
- 1 selout op (39,24): een randpixel aan de bovenkant van de rechterarm.

## Eerlijke twijfels
- **Maat:** 994 px, net boven de 980. Kleiner kan alleen zonder exacte 2×-reductie, en dan breken de chips.
- **Juweel:** de concentrische binnenring van het model leest op 8 px nauwelijks (3 px). Wat wel leest: zwarte rand rechtsonder, donkerrood linksboven, rood midden, roze en glans linksboven. Op 1× leest het als een rond rood juweel.
- **Deeg:** het lichte en het middendeeg liggen in grotere plukken die de modelvlakken volgen (de lichte vlakken per arm, de schaduwvlakken rechtsonder en in de naden). Op 8× is het wat vlekkerig, maar zo staat het in het model. Ik heb niets gladgestreken.
- **Outline highlights:** er zijn er maar 5 tegen 10 in r3. Het model heeft geen echte lichte rand, dus meer zou een eigen toevoeging zijn.
