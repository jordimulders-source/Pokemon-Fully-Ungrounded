# Keuring Pinsir-evolutie v2 r6 (rug B), 23 nov, onafhankelijke keurder

Maatstaf zoals eerder: (1) trouw aan `referenties/model_v2_r4.webp`, (2) een Gen 3-sprite volgens SPRITE_KERN, met belijning, kleur en schaduw naast Tyranitar, Aggron en Pinsir. Speciaal getoetst: Jordi's drie punten (hoofdvorm, arm, benen), banding in de nieuwe rugplaten en het palet tegen het model.
Hulpbeelden in `keuring/`:
- `kop.png`, `arm.png`, `verrearm.png`, `benen.png`, `rug.png`: sprite | model op het spriteraster;
- `1x2x.png`;
- `raster.txt`: index per pixel, E = 14;
- `silhouet_vs_model.txt`: # = beide, S = alleen sprite, M = alleen model.

Palet (L): 1=23, 2=50, 3=68, 4=101, 5=133, 14=166 · room 6/7/8 = 176/213/235 · rood 9–12 · oog 13.

## Eindoordeel: BIJNA
Er is duidelijk vooruitgang op het palet, het kopschild, de rug en het verre been. Er zijn nog vier benoemde reparaties nodig. De zwaarste is punt 1: zonder die opschoning blijft het lijf op 2× korrelig naast Tyranitar en Aggron, en dan is het oordeel FAIL.

## Jordi's drie punten
| Punt | Oordeel | Toelichting |
|---|---|---|
| **Hoofd: "te recht, niet de juiste vorm"** | ✔ | Het silhouet valt in de kop vrijwel samen met het modelmasker (`silhouet_vs_model.txt`, y 9–21). De vorm leest nu als gewelfd: donkere bovenrand, licht vlak met hooglicht op (14–18,15–17), en een rechterdeel in schaduw achter de schuine grens (27,16)→(22,19). De rechteronderrand loopt schuin omhoog naar de punt (24–28,22)→(29–32,21)→(33–34,20), zoals in het model, en de rechte band uit r4 is weg. Gezicht ongewijzigd, nog steeds één boze blik. |
| **Arm "niet goed te zien"** | ½ | Koepel, lijnen en hand staan op de modelplek, en de rechterrand is zwart zoals in het model. Maar de bovenarm (33–36,37–41) staat in 4/3, dezelfde tinten als het lijf erachter (42–46,35–42). Op 1× en 2× is de arm daardoor nog niet los te zien. Zie reparatie 2. |
| **Benen "niet goed"** | ½ | Verre been: ✔ (knieschijf, dwarslijn y 54, buik/dij-lijn, twee klauwen, een stap donkerder). Nabije been: dij, scheen en voet zijn ✔, maar de **knie is geen ronde knieschijf**. De ring is alleen rechts en onder dicht. Het model heeft een rondom donkere ring (boven y ≈ 50, links x ≈ 35), en Jordi noemde eerder al "geen knie te zien". Zie reparatie 3. |

## Rug B en palet
- **Rug B: geen banding meer** ✔. Drie platen, elk met licht linksboven (5 plus 2–3 px 14) en schaduw rechtsonder (3), geen strepen langs de naden. Helderheid 96 tegen model 101. De vereenvoudiging valt binnen wat Jordi toestond.
- **Palet** ✔. Bruin 68/101/133/166 sluit aan op de modelbanden (52/95/125/148, in tint gelijk). De stappen zijn 33 (Gen 3-norm ±30–40). Lijn 2 = het donkerste modelbruin, buitenlijn 1 de donkerste kleur. Rood en room liggen op de modeltinten. Helderheid per vlak binnen ±5, behalve gezicht −7 en verre zijde −8 tot −11 (bewust). Geen bezwaar.

## Reparaties
1. **Korrel: 61 bruine vlakjes < 3 px** (Gen 3-netheid). Het meeste komt door de per-pixel-meting. Een vlakje neemt de meest voorkomende buurtint (geen lijnpixels aanraken). Waar het om gaat:
   - lijf tussen arm en staart: (38,33–34)3, (39,35)3, (41,35)3, (44,35)3, (40,36)3, (41,37)3, (45,37)3, (41,38)5, (45,39)5, (46,40–41)5, (52,37–38)5, (52,39–40)4, (52,41)3, (45,44)3, (48,45)3;
   - schouder en hals: (33,28)3, (36,28)3, (34–35,28)4, (36–37,27)4, (34–35,23)4, (28–29,23)5;
   - heup en dij: (35,46)3, (37–38,47)4, (40,49–50)4, (33,50–51)4, (45–46,52)4, (40–41,55)3;
   - verre been: (18–19,49)3, (18–19,50)4, (23,51)4, (22,53)4, (16,56)5;
   - kopschild rechts: (30–31,20)3 en (35,18)4/(34,19)4. De lichte randstreep (34,18), (32–33,19), (26–28,20) mag blijven als één doorlopende streep. Vul daarvoor (29,20)4→5 en (31,19)4→5, zodat hij niet in losse stukjes valt.
   - **Laten staan:** gezicht, klauwen, stekelflanken en hooglichten 14 (bewust klein).
   - Na het opschonen opnieuw tellen. Doel: geen bruine vlakjes < 3 px buiten die uitzonderingen.
2. **Nabije arm los van het lijf** (kleur mag afwijken, Gen 3: een ledemaat vóór het lijf is lichter dan het lijf erachter):
   - bovenarm (33–35,37–39) 4→5, en (33,40), (34,40), (33,41), (34,41) 4→5;
   - (35,39) en (36,38–39) 3→4, zodat de sikkel naar de lijn (37,39)/(36,40) blijft;
   - (32,37–38) blijft 5 als lichtrand;
   - de slagschaduw op het lijf blijft 3, zo komt het contrast arm|lijf van ±1 naar ±2 tinten;
   - **onder de hand**: het zwarte blok (36–41,44) plus (35–37,45), (39–40,45) is 2 rijen dik. Het model is daar zwart, maar op 1× wordt het een vlek. Houd rij 44 als buitenlijn (1) en zet (39,45) en (40,45) 1→3, de slagschaduw op de dij. (36,45) en (37,45) blijven 1 als klauwrand.
3. **Knie nabij been als ronde knieschijf** (model: rondom ring):
   - boven (37,50), (38,50), (39,50) 5→3;
   - linksboven (36,51) 5→3;
   - links (35,52), (35,53) 5→3 en (35,54) 4→3;
   - hooglicht 14 (36,52) en (37,52) schuift 1 px naar rechts: (37,52) en (38,52) worden 14, (36,52) wordt 5. Zo ligt het hooglicht binnen de ring;
   - geen zwart: de ring in 3 aan de lichtkant, 2 rechts en onder zoals nu.
4. **Buitenrand**: (37,62) is room 6 op de silhouetrand (onderkant klauw links, nabije voet) en wordt 1.

## Kort
BIJNA. Hoofd ✔, palet ✔, rug B zonder banding ✔, verre been ✔. Nog doen: de korrel opschonen (61 vlakjes), de arm een tint lichter dan het lijf met een smallere zwarte vlek onder de hand, de knie als gesloten ring in 3, en (37,62)→1. Daarna een korte herkeuring (alleen telling en 1×/2×), dan naar Jordi.
