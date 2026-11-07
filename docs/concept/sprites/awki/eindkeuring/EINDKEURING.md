# Awki – eindkeuring (Dragonfly Cave), kleur ronde 4

**Gekeurd:** `kleur_r4/awki.png` (64×64, 15 kleuren + transparant, `normal.pal`; png = `raster.txt`, pixeldiff 0). 1388 px.
**Tegen:** het bevroren model `referenties/model_gekozen.png` (gemeten met `kleur_r3/stappen/kw.py`, schaal 6.232, top 2, left 4) en echte Gen 3-sprites (`graphics/pokemon/*/anim_front_gba.png`): Taillow, Swellow, Pidgeotto, Fearow, Ho-Oh.
**Vel:** `vergelijk.png`: 1× en 4×, op licht en donker, awki naast de vijf Gen 3-sprites.
**Getoetst:** alleen de uitvoering (Gen 3-techniek volgens `SPRITING.md`, `FAKEMON_CHECKLIST.md` deel E en `SPRITE_KERN.md`). Het ontwerp en de vorm volgen het model en zijn niet gekeurd; de trouw aan het model is in `keuring_r3/KEURING.md` al per onderdeel PASS bevonden. De r3-reparatie (4 staartpixels van 7 naar 6) zit erin: de pixeldiff r3 → r4 is precies die 4 px.
**Coördinaten:** (x,y) in de 64×64. Indexen: 1 zwart, 2/3/4 bruin (donker → licht), 5/6/7 vuur (donkerrood, rood, oranje), D karmijn, 8/9/A geel (oker → licht), B/C wit/grijs, E/F lavendel (licht/donker).

## Checklist
| # | Punt | Oordeel | Bevinding |
|---|---|---|---|
| 1 | 3/4 naar links-voor, kop meer naar de kijker (SPRITING §0.1, B1) | PASS | Zoals het model: de kop staat in 3/4 met één oog bij de snavel, het lijf is schuin, de verre vleugel is opgeheven en de nabije gevouwen. |
| 2 | Alles geteld en verbonden (§0.2, C1) | PASS | Twee vleugels (ver en nabij), twee poten in perspectief, de staart sluit aan op het lijf, één oog. Niets los. |
| 3 | Formaat fase 2 (D1) | PASS | 1388 px, box ±56×58. Swellow heeft 1425, Pidgeotto 1087 en Fearow 1735 px: awki past bij een late fase 2. |
| 4 | Buitenlijn 1 px, geen klonten (§8) | PASS | Er is één 2×2 zwart blok, op (32–33, 18–21): dat is het masker, een vlak en geen lijn. Verder geen dubbele lijnen. Er staat geen zwarte pixel los midden in een vlak (scan op index 1 zonder rand of lijn: 0). |
| 5 | Zwart aan de schaduwkant, selout aan de lichtkant (§8, SPRITE_KERN) | PASS | De selout aan de lichtkant: oker 8 om de gele veren, karmijn D op de bovenrand van de kuif (34–38, 6–9), 5/6 op de bovenrand van de staart, F om de lavendel punt. Aan de schaduwkant staat zwart. Nergens wisselen zwart en een donkere tint om en om op één rand. |
| 6 | Geen open randen, geen lichte kleur op de buitenrand | **FAIL (2 px)** | Er staat geen lichte kleur (A, B, C, E, 7, 9) op de buitenrand. Wel staat op de onderkant van de staart, in de schaduw, de basistint rood **6** direct tegen transparant: (49,52) en (55,52), de inkepingen vóór en tussen de twee veerpunten. Daar is de rand open. Het model heeft op die plekken donker: (49,52) DD12 en (55,52) 5D15; ernaast is (54,52) al 5 (model 4111). Brede tinten 3 tegen transparant op de poten en tenen ((30,53), (40,52–55), (30–32,56), (42,58), (39,59)) zijn pseudo-omlijning van delen van 1–2 px (SPRITING §8) en zijn in orde. |
| 7 | Licht linksboven, schaduw als sikkel (§5) | PASS | Opgeheven vleugel: geel aan de punten linksboven, karmijn naar de schouder. Buik: 9 linksboven en 8 rechtsonder, met een licht gebogen grens rond rij 40. Gevouwen vleugel: 4 boven, 3 midden en 2 langs de rechter schaduwrand. Kuif: oranje kern met een donkere onderzijde. Overal volgt de schaduw de vorm. |
| 8 | Geen pillow shading / banding | PASS | Aan de lichtkant van een vlak staan nergens donkere randen. De donkere strook links in de gevouwen vleugel (x32–34) is de binnenlijn waar de vleugel over de buik valt, in een donkere tint van het vlak (E2). Die loopt niet rondom. |
| 9 | ≤ 3 tinten per kleurgroep + omlijning, ramps (§4) | PASS | Geel 8/9/A (lum 140/175/219, stappen 35/44), vuur D/6/7 (79/106/147) met 5 voor lijnen, bruin 2/3/4 (52/77/107, stappen 25/30, iets kleiner dan Taillow maar nog duidelijk te zien), keel C/B, lavendel F/E. Geen kleurgroep heeft een vierde vlaktint. |
| 10 | Anti-aliasing alleen binnen (§8) | PASS | De overgangspixels 5 en 2 (bijv. (34,14) en (7,21)) liggen aan de binnenkant van de lijn, op gemeten modelplekken. |
| 11 | Losse pixels / tintvlakjes < 3 px | PASS | De losse pixels (8-buren-scan) zijn allemaal bewust: de oogglans (30,19), het oog en het rode vlakje, de uiteinden van de veerlijnen in de opgeheven vleugel, de teenscheidingen en klauwpuntjes, en de glans op de voet (26,56). Het 9/7-reepje (32–35,13) aan de voet van de kuif volgt het model (7799/9999/9977) en is op 1× niet te zien. |
| 12 | Geen zebra/raster/dambord (§7, poedelmot-les) | PASS | Eén veerlijn per veerrij. De tenen hebben een 3/4-afwisseling als teenscheiding, zoals in het model. |
| 13 | Rechte stukken / curven (§3) | PASS | De omtrek is het bevroren silhouet. Het korte rechte stuk aan de rechterflank (x49, rij 41–44) staat ook in het model. Ik zie geen spijkertjes. |
| 14 | Oog (§6, SPRITE_KERN) | PASS | Een 2×2-oog in het zwarte masker: glans B linksboven (30,19), iris oker (31,19–20) en pupil (30,20). Het oog leest op 1× op licht en donker, vergelijkbaar met het oog van Taillow en Swellow. |
| 15 | Leest op 1× op licht en donker (§0.5) | PASS | Zie `vergelijk.png`. Kuif met lavendel punt, opgeheven vuurvleugel, wit-zwarte kop, buik, staart en poten lezen allemaal op beide achtergronden. De dichtheid en omlijning liggen tussen Pidgeotto en Swellow. Op donker verdwijnt niets: de zwarte rand houdt de schaduwkant bij elkaar en de lichtkant heeft gekleurde selout. |
| 16 | Omlijningsdonkerte (E3) | PASS | Zwart is 13,8 % van de pixels (Gen 3 ±13 %). Met donkerbruin 2 erbij is het 24 %, wat past bij een donkerbruine vogel. |
| 17 | Verre kant donkerder, overlap met lijn (E1, E2) | PASS | De verre vleugel ligt vóór de borst, met een bruine voorrand en een zwarte lijn naar de kop. De verre poot (links) is dunner. Waar de nabije vleugel over de buik valt, scheidt een donkere lijn ze. |

## Reparatie (FAIL 6)
**Staartonderrand, 2 px:**
- (49,52): **6 → 5**
- (55,52): **6 → 5**

De rand van beide inkepingen is dan donkerrood, net als (54,52) ernaast en de punt (59,51–52). De ondervlakken van de veerpunten blijven 1/2. Het model wordt niet geschonden: het heeft op die plekken donker (DD12, 5D15). Daarbuiten is de pixeldiff 0.

## Ter info voor Jordi (geen eis, model gaat voor)
- Naast de Gen 3-vogels oogt awki wat donkerder en vlakker. De buik heeft geen hooglicht (lichtste tint 9) en het lijf is grotendeels bruin met zwarte omlijning. Pidgeotto en Fearow hebben meer lichte tint en meer gekleurde selout. Dat is zo in het model, dus geen fout. Wil Jordi meer "R/S-licht", dan zou een paar pixels A linksboven op de buik dat geven; dat wijkt af van het model en mag alleen op zijn woord.
- De punten uit `keuring_r3` die ter info waren (de zwarte voet onder de kuifpunt (42–43,10) en de snavelpunt die 1 px dunner is) staan nog open als vraag. Technisch zijn ze in orde.

## Eindoordeel
**Goed, op één reparatie van 2 px na.** Op 16 van de 17 punten is de uitvoering Gen 3-waardig. Naast Taillow, Swellow, Pidgeotto, Fearow en Ho-Oh leest awki op 1× en 4× als een echte Emerald-sprite van een late fase 2. Na de staartreparatie ((49,52) en (55,52) van 6 naar 5, pixeldiff 0 erbuiten) kan de sprite zonder nieuwe keuring naar Jordi, op 64×64 en 8×.
