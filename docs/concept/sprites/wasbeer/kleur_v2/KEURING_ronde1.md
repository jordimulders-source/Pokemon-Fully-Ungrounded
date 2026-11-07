# Keuring kleur ronde 1 (onafhankelijke keurder, 2 nov)

Gekeurd: `ronde1.png` / `ronde1.txt` / `ronde1.pal` / `vel_ronde1.png`, op 1x, 2x, 3x en 8x, op licht en donker. Naast de render `silhouet_v2/onderlaag_s1a_256.png`, het bevroren silhouet `direct_s1a.txt` (+ `labels_s1a.txt`), foto 10/11/2/7, de lijn (olinguito, Coathief) en 12 echte sprites: zangoose, sneasel, linoone, ursaring, teddiursa, furret, sentret, mightyena, raticate, seviper, absol, weavile. Eigen oordeel eerst; makernotities pas daarna gelezen (ze bevestigen bijna alle fails hieronder zelf: "zwak", "leest als m-hand", "donkere vlek", "blokkerig").

Coördinaten: (x, y), 0-geteld, zoals in `ronde1.txt`. Paletindex als hexteken.

**Uitslag: FAIL (9 van 10 punten FAIL).** Sterk: de kop leest op 1x direct als wasbeer, de pose (sluipend op 2 poten, nabij been achter op de tenen) leest, de verre klauw is een herkenbaar klauwpaar met inkeping, de verre dij staat netjes in schaduwtint, en de silhouetdiff is 0. Wat faalt is vooral vakwerk binnen het silhouet: masker als helm, oog als rode stip, nabije hand als witte handschoen met donkere klodder, vlak lijf, rechte staartringen.

| # | Punt | Oordeel |
|---|---|---|
| 1 | Alpha-diff 0, geen open randen, geen ruis | **FAIL** (diff 0 ok; 19 open randpixels, enkele losse pixels) |
| 2 | Kop: masker, wenkbrauw, snuit, ogen | **FAIL** (helm-band, rode stip, verre oog op de omtrek) |
| 3 | Klauwen | **FAIL** (verre ok van vorm, open rand; nabije = 3 vingers/handschoen) |
| 4 | Buidel | **FAIL** (geen leesbare opening/plooi, dubbele naad = voorwerp) |
| 5 | Volume | **FAIL** (verticale banen, geen hooglicht/kernschaduw) |
| 6 | Omlijning/selout | **FAIL** (zwart op de lichtkant van kop en oren) |
| 7 | Staart | **FAIL** (rechte ringen, lichte vierkant in de kop, haak leest niet) |
| 8 | Leesbaarheid 1x | **FAIL** (nabije onderarm = donkere vlek, nabije klauw = witte klodder) |
| 9 | Familie | **FAIL** (contrast/hooglicht onder het niveau van Coathief; temperatuur → Voor Jordi) |
| 10 | Afgekeurde dingen | **FAIL** (indruk "klauwen uit de buik" + willekeurige lijnen; geen jetpack, geen bruin rechthoek: ok) |

## 1. Alpha, randen, ruis: FAIL
- Alpha-diff met `direct_s1a.txt`: **0** (1682 px, txt = png). PASS op dit deel.
- **Open randen** (crème schaduwtint 8 direct naast transparant, geen omlijning): verre klauw (10,34) (9,35) (8,36) (8,37) (8,38) (7,39) (7,40) (7,41) (6,42) (6,43) (6,44) (10,42) (10,43) (10,44); borstrand (20,34); staartring (50,31) (50,32) (49,33) (44,39). Op wit lost de linkerrand van de verre hand op (zie 8x).
  - Reparatie: verre hand y 34–41 linkerrand → een crème selout (nieuwe tint, zie palet hieronder, bv. 120,106,86); de klauwpunten y 42–44 (2 px breed) mogen pseudo-omlijning blijven, maar dan de buitenste pixel in de selout en de binnenste in 8. Staart (49–50, 31–33) en (44,39) → selout of 4. (20,34) → 4.
- **Losse pixels** die niets vormen: (16,12)–(16,13) streepje 3 in het masker; (22,17) 5 in de snuit; (30,26) 6 en (28,33) 5 in de nabije onderarm; (17,30) 6 en (11,34) 2 in de verre onderarm. → opnemen in het omringende vlak.
- **Palet:** 3 (72,63,58) en 4 (74,68,63) zijn op elk formaat niet te onderscheiden: één plek verspild. Voeg 3 samen met 4 (of 2) en gebruik de vrije plek voor wat ontbreekt (hooglicht-grijs of crème selout).

## 2. Kop: FAIL
- **Helm:** het masker (2) is één horizontale band van x 11 tot x 25 met rechte grenzen: bovenrand y 9–10 x 12–19 (8 px recht), onderrand y 14 x 19–24 (6 px recht). Op 8x en 1x leest het als een zonnebril/blinddoek, niet als het masker van de render (twee lobben om de ogen, verbonden over de neusrug, met de witte wenkbrauw als boogje erboven).
  - Reparatie (alleen binnen het masker, niets aan het silhouet): onderrand nabije lob rond maken: (19,14) → a (snuit), (24,14) → 6, (23,15) → 6, (25,12) en (25,13) → 6, zodat de lob onder het oog het laagst is (x 20–22, y 15) en achter het oog oploopt. Bovenrand: (18,9) → a zodat de wenkbrauw over het nabije oog als boog doorloopt; tussen de ogen de grijze neusrugstreep (16–17, 8–9) houden, maar de rij eronder (16–17, 10) → 3 als smalle brug, zodat het masker twee lobben met een brug wordt in plaats van één balk.
- **Oog = rode stip:** nabije oog (20–22, 10–12): bovenlid 1 ligt op masker 2 (22,16,16 op 44,37,35) en is onzichtbaar; wat overblijft is een rood vlekje met een witte pixel. Op 1x: twee rode puntjes in een zwarte band.
  - Reparatie: een lichtere oogkas zodat lid en iris een vorm krijgen: (20,13) (21,13) (22,13) (23,11) (23,12) → 3 (of de nieuwe donkergrijze tint); bovenlid 1 px breder: (19,10) → 1; iris rij 12: (22,12) e → f zodat de lichte onderkant 3 breed is; glans (20,11) a houden. Doel: Linoone/Mightyena-oog: donker lid, iris donker boven/licht onder, glans.
- **Verre oog op de omtrek:** (12,10) e en (12,11) f liggen tegen de zwarte rand x 10–11 en lezen als een rode veeg op de contour. → (12,10) (12,11) → 2 en het verre oog 1 px naar binnen: (13,11) e, (13,12) f (of weglaten achter de neusrug, SPRITING §0.4; zie Voor Jordi).
- Wel goed: witte wenkbrauwband (y 8), witte snuitrand (y 14–18), masker over de neusrug, masker stopt achter het oog (x 25/26), oren met lichte binnenkant.

## 3. Klauwen: FAIL
- **Verre klauw (x 6–17, y 34–45):** vorm PASS: 2 korte klauwen naast elkaar, kleine inkeping (x 9, y 41–45) uit het bevroren silhouet, vast aan de donkere onderarm. Kleur FAIL: open linkerrand (zie 1) en geen schaduwkant behalve de 1 rechts; het vlak x 8–15, y 35–39 is egaal 9 (een bleke peddel). → schaduwtint 8 langs de onderkant van elke klauw (x 7–8 en x 10–11 vanaf y 40), hooglicht 9 alleen langs de bovenrand.
- **Nabije klauw (x 19–27, y 26–33):** FAIL. Twee klauwen (x 22–23 en 25–26) zijn over hun hele lengte gescheiden door een donkere lijn (24, 30–33), en rij 33 heeft drie punten (x 20, 22–23, 25–26) door de 4-pixels op (21,33) en (27,33). Daarnaast loopt links een crème strook (x 17–20, y 27–33, 7/8/9 met 4-rand op x 21) die als derde vinger/bot leest. Resultaat: een witte "m"-handschoen (de maker zegt het zelf), niet Jordi's "letterlijk een inkeping tussen 2 klauwen".
  - Reparatie: (24,30) en (24,31) → 9 (klauwen tegen elkaar); inkeping alleen (24,32)–(24,33) houden. (20,33) en (21,33) → 8 (buik), zodat er 2 punten overblijven. Crème strook (16–20, 27–32) → grijs 7/6 (lichtkant van de borst), niet crème: de klauwen moeten het enige lichte ding op die plek zijn.
- Nabije klauw zit vast aan de hand/onderarm rechts (27, 29–32): ok, maar zie 8 (onderarm leest niet).

## 4. Buidel: FAIL
- Leest als bruine zak/rugzak, niet als jetpack (ok), maar: de opening die de maker noemt (34–38, 17: 1222 1 onder een flap bb op y 15–16) leest op 8x als bovenrand en op 1x helemaal niet. Geen plooi; het vlak is een glad verloop b/c/d.
- Langs de rug ligt een **dubbele naad**: grijze selout 4 + bruine b van (33,15) tot (38,33) in één doorgaande lijn. Dat maakt hem een voorwerp dat erop ligt, niet "echt onderdeel van zijn lichaam".
  - Reparatie: de 4 in die naad → 5 (rugschaduw), alleen b als grens; onderaan (y 30–34) de overgang 2–3 px laten overlopen (5/b afwisselend) zodat de buidel uit de rug groeit. Opening: een gebogen donkere spleet (1, met 2 eronder) van (35,18) naar (41,21), 1 px dik, met een lichte lip d erboven (x 35–40, y 17), zodat je een zakmond ziet; één plooi in b van (38,25) schuin naar (43,30).

## 5. Volume: FAIL
- Romp (x 15–35, y 19–34) = drie verticale banen 7 | 6 | 5 met rechte grenzen (7→6 op x 19/20, y 21–27; 6→5 op x 27/28, y 19–33, 7–14 px recht). Geen hooglicht op het lijf (lichtste lijftint is 7), geen kernschaduw die de bolling volgt. Op 1x: grijs-egaal, plat (maker: idem).
  - Reparatie: hooglicht (nieuwe tint ±176,168,156 op de vrije paletplek) als boog op schouder/borst x 16–20, y 21–24; de 6→5-grens gebogen laten lopen (op buikhoogte y 25–29 naar x 30, onder y 31 terug naar x 28); een 4-kernschaduw van 1 px langs de rugkant (x 33–34, y 22–32) vóór de buidel. Lichtere borst/buik (zoals foto 2 en 11 en de render) als zacht ovaal y 26–37 onder de nabije hand, in een tint tussen 7 en 9 (niet dezelfde als de klauwen).
  - Dijen: nabije dij (x 30–41, y 36–46) is egaal 6; hooglicht 7 linksboven (x 30–34, y 36–39) en een schaduwhalvemaan 5 onderaan. Staart: lichtkant links op elke lichte ring (9) en schaduwkant rechts (8), nu is het per ring nagenoeg egaal.

## 6. Omlijning/selout: FAIL
- Zwart (1) op de lichtkant: oortoppen (15–18, 0), (14,1), (19,1), (13,2), (25–27, 1), (24,2); kopomtrek linksboven (12,3) (12,4). Gen 3 (Zangoose, Linoone, Coathief) heeft daar een gekleurde selout. → die pixels naar 4 (grijs) of de crème selout bij de witte oren.
- Wel goed: lichtkant van romp en verre dij in 4 (x 14–15, y 21–29); verre dij in schaduwtint 5/4 en gescheiden met 4 (niet met zwart) op x 20–28, y 39–47, behalve (28,45) 1 → 4. Masker tegen zwart aan de linkerrand is acceptabel (Linoone doet dat ook).

## 7. Staart: FAIL
- Ringgrenzen boven zijn rechte horizontale lijnen van 7 px: y 30/31, 33/34, 38/39 op x 49–57. Bij een buis in 3/4 horen het bogen te zijn. → elke ring aan de randen 1 px lager dan in het midden: bv. lichte ring y 31–33: (50,31) en (56,31) → 2, (50,34) en (56,34) → 8.
- Lichte vierkant (54–56, 23–26, 8/9) in de donkere staartkop leest als een venster/gat, niet als vorm. → 2/3, en de haak tonen met een lichte rand langs de bovenkant van de haak (50–55, 19–20 → 3/8) en een 1-px schaduwlijn 1 onder de terugkrullende punt (49–51, 22–23).
- Onderste ringen (y 39–47) lopen schuin mee met de buis: goed.

## 8. Leesbaarheid op 1x (licht en donker): FAIL
- Leest: wasbeerkop, pose op 2 poten, verre klauw, zak op de rug, donkere onderbenen.
- Leest niet: **nabije onderarm (27–35, 26–33)** is op 1x een ronde donkere klodder naast een witte klodder (de klauw + crème strook). Er is geen bovenarm/elleboog: de hand lijkt op de buik geplakt.
  - Reparatie: onderarm als buis: bovenrand (28–32, 27–28) → 5 (lichtkant), midden 3, onderkant 2, rand 1; en de bovenarm op de romp tekenen met een 1-px 4-lijn van (33,27) omhoog naar (33,22), zodat de arm van schouder naar hand loopt.
- Staarthaak leest op 1x als knots (zie 7).

## 9. Familie: FAIL
- Oog (rood op donker masker) en masker passen bij olinguito/Coathief: goed. Dark, niet zwart-op-zwart: goed.
- Naast Coathief en de 12 Gen 3-sprites is dit de doffste sprite van het vel: weinig hooglicht, geen gekleurde selout aan de lichtkant van de kop, alles in middengrijs. R/S gebruikt veel hooglicht (SPRITING §5). Opgelost door 5 en 6.
- Kleurtemperatuur (koel grijs tegenover de warme bruine lijn): zie Voor Jordi.

## 10. Afgekeurde dingen: FAIL
- Niet terug: rechthoekig bruin vlak, jetpack, grijs blok, horizontale pose. Goed.
- Wel terug: **indruk "klauwen uit de buik"** (nabije hand zonder arm op de borst, crème strook als extra vinger) en **willekeurige lijnen**: crème strook (17–20, 27–33) met 4-rand op x 21, streepje 3 (16, 12–13) in het masker, 1-px 5 op (22,17).

## Voor Jordi (smaak, geen opdracht aan de maker)
1. **Kleurtemperatuur:** de render (en dus deze sprite) is koel grijs; olinguito en Coathief zijn warm bruin. Het echte dier is grijsbruin tot geelbruin (SPEC). Grijs zoals nu, of de grijstinten 10–15% warmer (richting de Coathief-schaduwen), zodat de lijn als familie leest?
2. **Handen:** in de render en de sprite crème; bij het echte dier (foto 10, 2, 7) zijn handen en onderarmen donker. Crème houden (klauwen springen eruit) of donkere handen met alleen lichte klauwpunten (klauwen korter ogend, dichter bij "ze hoeven echt niet lang te zijn")?
3. **Verre oog:** houden (1 px naar binnen) of weglaten achter de neusrug (één oog, zoals Linoone/Mightyena)?
4. **Buidelkleur:** eigen warm grijsbruin (nu) of uit de vachtkleur, zodat hij meer "deel van het lijf" is?
5. **Buik:** een lichtere crème borst/buik zoals op foto 2 en 11 (helpt het volume) of de romp egaal grijs zoals de render?
