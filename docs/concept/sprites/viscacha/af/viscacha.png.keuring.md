# Keuring viscacha kleur r8 (verse onafhankelijke keurder, 7 nov)
- Bron: `referenties/gemini_gekozen_ronde6.png` (origineel, op spriteschaal gelegd met `kleur_r6/meta.npy`: sx = (ox−165)/10,78, sy = (oy−86)/10,78 + 14), `kleur_r6/gemini64.png`, meting `kleur_r8/stappen/meting.npz` (dekking en donkerfractie per spritepixel) en `onderlaag.txt`, `raster.txt` (= `viscacha.png`), `controle_uitvoer.txt`, `NOTITIES.md`, vorige keuringen `kleur_r5/vel.png.keuring.md` en `kleur_r6/vel.png.keuring.md`. Getoetst: alleen (1) trouw aan het model (oog mag luier) en (2) Gen 3 volgens SPRITE_KERN.
- Bekeken: sprite 8× naast het model op dezelfde uitsnede; close-ups 12–16× met raster (kop, lijf, poten, staart); 1× naast `gemini64.png` en naast het model verkleind tot 64 px.

## Wat ik zag
- **8×:** zelfde pose, massa en verdeling als het model: brede ronde oorschelpen, lui oog, geel kroontje op het voorhoofd, sikkelvormig wangaanhangsel met terracotta erachter, crème bef met de verre snorharen erover, twee wantpootjes met teenlijntjes, driehoekige buikvlek, dijlijn, terracotta bil en achterpoten (verre in donkere tint), tweekleurige krulstaart met vier gele vlammen. Niets toegevoegd of weggelaten.
- **1×:** leest identiek aan het verkleinde model: oranje knaagdier, gele wangsikkel en pluim, drie snorharen aan de voorkant. De sprite is iets strakker belijnd dan de zachte verkleining; dat is de Gen 3-vertaling, geen afwijking.

## Afvinktabel
| onderdeel | lijkt op | wijkt af in | ok |
|---|---|---|---|
| kop | massa, plek, ronde voorhoofdlijn | – | ja |
| oor nabij | brede ronde schelp: r16 x23–25, r17 x21–26, rechterrand x26 r17–21 (model idem); donkere schelp B/C met lichte rand links | – | ja |
| oor ver | top r15 x11–12, buitenlijn x9 r19–22, terracotta onderin | – | ja |
| oog | lui: zwaar bovenlid, amandelspleet met glans (toegestane afwijking) | – | ja |
| neus-Y | armen (8,34) en (10,34), samen (9,35), steel (9,36); model donker op (10,34) en de mondlijn (7,35–36)→(8–9,37) | binnen wat 64 px toont | ja |
| mond | lijn langs de snuitvoorkant naar de lip, terracotta lip (10–14,37) | – | ja |
| kin | crème kinnetje (10–11,38), kinlijn (12–14,38) en (10–11,39): gemeten donker in het model op (12–14,38) | – | ja |
| snuit | ronde voorrand x7, r33–37 | – | ja |
| snorharen nabij | 3 lijnen, gemeten tegen het model: boven eindigt (0,37) (model (0,9; 36,6)), midden (0,40) (model (0,9; 39,8)), onder steil tot (3,42) (model (3,7; 41,5)); vast aan de snuit, overal ≥ 1 rij lucht, geen raster | – | ja |
| snorharen ver | 2 lijnen vanaf (13,35) achter de mond: boven tot (22,39) onder de sikkelpunt, onder over de bef tot (22,43), zoals het model | begin dicht op elkaar (x13–19), maar het model doet dat ook; geen klont | ja |
| gele pluk | kroontje: punt omhoog (6,28), punt links (5,31), vlak A, selout 8 | – | ja |
| wangaanhangsel | sikkel x18–27, r28–38, punt (26–27,28–29) met donker erboven, terracotta erachter | – | ja |
| bef | crème met schaduw links, tot x22 r40–43 | model loopt 1 px verder door op (20–21,46): onder 64 px-grens | ja |
| voorpoten | ver (12–16,45–50) en nabij (20–25,46–52) op de modelplekken, wantjes met 2 teenlijntjes | – | ja |
| lijf/rug | massa, schouder, dijlijn (39,38)→(34,48), binnenlijn (30,40–41) | rugtop r29 recht (x33–40): het model loopt daar in r29 op van dekking 0,5 naar 1,0 (x33→39), dus ook vlak op 64 px | ja |
| buik | driehoekige crème vlek x31–37, r42–46, crèmeschaduw eronder | – | ja |
| bil | terracotta, punt (49,44) | – | ja |
| achterpoten | ver in E (27–36,50–58) met voet r56–59, nabij (46–50,54–57) met voet r58–61, teenlijntjes, perspectief klopt | – | ja |
| staart | omtrek volgt het model (buitenrand x61–62 r31–44, binnenrand x51–57), lichte rand (59–60,33–36), onderrand r48–49 als model | – | ja |
| pluim | 4 vlampunten F1 (58,14), F2 (54,16), F3 (58–59,20), F4 (50,22), bleek A : rand 8 ≈ 2 : 1 zoals gemeten, kerven | – | ja |
| kleuren | palet per vlak gemeten op het model (k-means); lijf, crème, terracotta, oor, staart, geel | – | ja |

## Vorige punten (r5, r6)
- r5: framing, snuit, neus, mond, kin, snorharen (beide kanten), bef-raster, pluk, pluim, voorpoten, lijflijnen, achterpoten, staartonderrand: alle opgelost.
- r6 1 oor nabij: opgelost (top 1 px smaller dan r6 vroeg, maar gelijk aan de modelmeting). 2 oor ver: opgelost. 3 neus+mond: opgelost. 4 kin: opgelost volgens de meting (donker op (12–14,38), niet (9–14,39)). 5–6 snorharen: opgelost. 7 pluk: opgelost. 8 sikkel: opgelost. 9 bef: opgelost. 10 rug: blijft vlak, maar de meting laat zien dat het model op 64 px ook vlak is (zie tabel); vervalt. 11 pluim: opgelost. 12 staart: opgelost. 13 teenlijntjes: opgelost.

## Techniek (Gen 3)
- 16 kleuren, png = raster, open randen 0.
- Per kleurgroep ≤ 3 tinten + omlijning; licht linksboven, schaduw rechts/onder als sikkel langs de vorm; geen banding of pillow shading.
- Kleine clusters (< 3 px) zijn teenlijntjes, de dijlijn (4 op (37–39,38–40)), oogglans, sikkelpunt en vacht tussen snorharen: functioneel, geen ruis.
- Losse pixels alleen snorhaarlijnen van 1 px.
- Belijning: zwartbruin aan de schaduwkant, selout 2/8 aan de lichtkant; geen om-en-om-rand.
- 7 randpixels buiten het modelmasker (dekking < 0,12), allemaal 1 px antialias-rand van de omlijning: onder 64 px-grens.

## Reparaties
Geen (afwijkingen die overblijven zijn kleiner dan wat 64 px kan tonen).

Oordeel: PASS
