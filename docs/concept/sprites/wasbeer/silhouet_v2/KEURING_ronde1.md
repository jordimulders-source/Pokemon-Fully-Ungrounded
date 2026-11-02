# Keuring silhouet v2 ronde 1 (onafhankelijke keurder, 2 nov)

Gekeurd: `ronde1.txt` / `ronde1_1x.png` (1449 px, box 47x62, x 8–54, y 0–61), `vel_ronde1.png`, `zone_ronde1.png`, tegen `direct.txt`, `onderlaag_256.png`, `labels.txt`. Eigen vellen (1x licht/donker, 2x, 8x met raster) naast 13 echte sprites: weavile 1267, sneasel 976, zangoose 1388, gumshoos 1269, lucario 1053, raticate 1318, linoone 1089, sandslash 1597, ursaring 2258, vigoroth 1480, scrafty 1178, furret 1416, passimian 1819; formaat ook tegen de starterlijnen (combusken 1136 → blaziken 1579, monferno 1121 → infernape 1452, grovyle 1368 → sceptile 1783). Oordeel eerst zelf gevormd, notities van de maker daarna gelezen.

**Uitslag: FAIL (6 van 9 fail: punt 2, 3, 4, 5, 6, 7; PASS: 1, 8, 9).** Punt 2 (pose) en deels 7 (kopgrootte) komen uit het bevroren ontwerp E2 en zijn vragen aan Jordi, geen opdracht aan de maker; de rest is met kleine zonereparaties op te lossen.

| # | Punt | Oordeel | Reden |
|---|---|---|---|
| 1 | Massa en pose = onderlaag | **PASS** | Diff met `direct.txt` = 23 px, alle in de zones: verre klauw (x 8–13, y 33–37), spleet zak/staart (x 45–47, y 24–30), nabije voet (37,60). Overlay sluit op de render. |
| 2 | Leest als dier op 2 poten voorover | **FAIL** (twijfel; geërfd) | Niet horizontaal en niet helemaal rechtop, maar op 1x leest het als een rechtop staande beer/mens met een hoge rug: de hele linkercontour van kop tot heup is één verticale lijn (kopfront x 13, y 7–16; borst x 16, y 18–27, 10 px recht). Het "voorover" zit alleen in de rug/zak rechts. Naast Weavile/Sneasel/Zangoose (kop vóór de heup, borst schuin) staat dit rechter; het lijkt meer op Ursaring/Scrafty. |
| 3 | Verre klauw = korte koevoet | **FAIL** | Steel, bocht en eindstuk zijn er (steel y 33–34, bocht buitenhoek (8,34), eindstuk x 8–10, y 35–36), maar: tanden (8,37) en (10,37) zijn 1x1 px (eis ≥ 2 px) en lezen op 1x als stipjes/vorkje; de steel is op 1x niet los van de onderarm (één doorlopende diagonaal x 8–18, y 31–34 zonder pols), waardoor het geheel leest als "arm met hand/vingers omlaag" (maker noemt dit zelf). Bocht ±90°, geen 110°. |
| 4 | Rugzak als eigen vorm, deel van het lijf | **FAIL** (klein) | Goed: druppelvorm, zwaarst onderaan (rechterrand x 44–45 op y 24–33), sluit zonder inkeping op de schouder aan (geen jetpack), spleet tot de staart 2 px breed van y 21 tot 37 en V-dicht op (41,38). Fout: 1-px knobbel (39,17) met 1-px gat (39,18) bovenaan de zak = ruis in de contour. "Meer zichtbaar" komt verder uit de kleur (opening/plooi); het silhouet laat de onderrand van de zak tegen de heup niet zien. |
| 5 | Geringde haakstaart leest als haak | **FAIL** | Op 1x en 2x leest de staart als een dikke rechtopstaande zuil met een ronde kop (eekhoorn-/knotsstaart), niet als herdersstaf: breedte 7–9 px over 15 rijen, rechterrand x 54 recht op y 23–33 (11 px), linkerrand x 47–48 recht op y 24–33; de kop van de staart (y 19–23, 8–9 px) is breder dan de voet → knots. De holte onder de haakpunt is maar 1–2 px diep (linkerrand 46 → 48 → 47) en valt weg in de spleet. |
| 6 | Dunne delen | **FAIL** | 1-px tanden (8,37),(10,37); knobbel (39,17)/(39,18); deuk (30,8) in het achterhoofd; trapjes in de beenranden (26,50), (38,56), (28,58). Goed: onderbenen 4–5 px (Sneasel 3–4, Lucario 5–6; Jordi wilde ze dun), voeten 6–7, lucht tussen de benen ≥ 3 px, oren ≥ 3 px, teen (37–38,60) nu 2 px. De V-punten (19,32) (oksel) en (41,38) (eind spleet) zijn taps, geen dichtslibbende spleet: akkoord. |
| 7 | Kop: eigen onderdeel, oren gescheiden, ±33% | **FAIL** | Oren gescheiden (lucht 5/4/3 px op y 0–2): goed. Maar de kop is een doos: voorkant x 13 recht op y 7–16 (10 px), achterkant x 30 recht op y 3–12 (10 px, deuk op (30,8)), platte bovenkant y 3; geen snuitpunt (de neus van de render op ±(13,15) steekt niet uit), kin naar nek maar 2 px trap (y 16–18), achterkant loopt zonder nek over in de zak. Hoogte 18/62 = 29% (vraag ±33%), oppervlak 21%. |
| 8 | Formaat 1449 px, box 47x62 | **PASS** | Hoogte is vol (62), dus groter kan alleen in de breedte = de pose. Slanke tweevoeter-eindvormen: Infernape 1452, Blaziken 1579, Zangoose 1388, Weavile 1267. "Formaat volgt de vorm" wint van D1 (1700+). Groei t.o.v. Coathief wel klein, zie Voor Jordi. |
| 9 | Ruimte onder de buik / tussen de benen | **PASS** | Kruis open vanaf y 47 (3–4 px), twee benen in eigen kolommen met 3–7 px lucht, ruimte onder de verre arm (x 8–21, y 35–47) leeg, geen hangende slierten. |

## Reparaties (maker, alleen in deze zones)
**Zone 1 verre klauw (x 6–19, y 30–39)**
- Tanden weg als losse pixels: vul (9,37) zodat het eindstuk x 8–10, y 35–37 één blok van 3x3 is; de gespleten punt wordt kleurwerk (één donkere omlijningspixel op (9,37), zoals de koevoetproef al liet zien: de spleet leest pas op 8x). Alternatief alleen als Jordi de spleet in het silhouet wil: zie Voor Jordi.
- Pols: maak de steel zichtbaar dunner dan de onderarm: wis (17,33) en (16,33) (onderkant onderarm), zodat de steel x 8–15, y 33–34 2 px dik is tegen een onderarm van 4–5 px. Controleer daarna dat de oksel (19,32)/(18–19,33) een V blijft.
- Eindstuk eventueel 1 rij langer (8–10,38) als de bocht dan meer naar 110° leest; toets op 1x of het niet als poot gaat lezen.

**Zone 2 buidel/staart (x 33–56, y 15–40)**
- Knobbel: vul (39,18) (zakrand wordt 37, 39, 39, 39, 40 …).
- Staart als haak i.p.v. zuil: rechterrand bol en taps: wis (54,23) en (54,31)–(54,33), (53,34)–(53,35) blijven; staartkop smaller: wis (53,20)–(53,21) zodat de top rond en smaller is dan de voet.
- Holte onder de haakpunt 1 px dieper: wis (48,28)–(48,30), zodat de punt (x 46–47, y 22–27) als eigen lob over de spleet hangt; let op: lucht naar de zak blijft ≥ 2 px en de schacht ≥ 5 px.

**Nieuwe zone, ±1 px, eerst akkoord van Claude (buiten de huidige zones):**
- Kopomtrek: deuk (30,8) vullen; achterkant bol: (31,6)–(31,9) erbij; bovenhoeken rond: (14,2) en (30,2) weg; snuit: (12,14)–(12,15) erbij (neus), (13,16) weg (kin), (13,7) weg (stop tussen voorhoofd en snuit).
- Borst: (15,21)–(15,25) erbij, zodat de borst bol naar voren staat en de verticale lijn kop–heup breekt (helpt punt 2).
- Beenranden: (26,50), (38,56), (28,58) vullen.

## Voor Jordi (smaak / bevroren ontwerp, geen opdracht aan de maker)
1. **Richting verre koevoet:** maker heeft de punt **omlaag** gezet; in de render krult hij licht **op**. Omlaag leest rustiger (omhoog werd een drietand met de oksel), maar wijkt af van E2.
2. **Gespleten punt:** in het silhouet dicht (spleet = kleur) of zichtbaar? Zichtbaar kan alleen met een eindstuk van 4–5 px breed (tanden van 2 px), dan wordt de klauw groter dan "kort".
3. **Pose:** het silhouet leest rechter dan de render (de render toont het voorover vooral met kleur/schaduw). Meer voorover = romp of kop 2–3 px naar links verschuiven = ontwerpwijziging aan E2.
4. **Staarthaak:** in de render ligt de punt bijna tegen de schacht; een echt leesbare herdersstaf (punt verder omlaag met lucht eronder, zoals Raticate) wijkt af van E2.
5. **Kopgrootte:** 29% van de hoogte (doel ±33%); groter maken = ontwerpwijziging.
6. **Formaat:** 1449 px is 1,10x Coathief (1315); echte lijnen groeien 1,3–1,4x (Combusken → Blaziken, Monferno → Infernape). Hoogte zit vol; meer groei kan alleen via een bredere pose.
7. **Nabije arm** ligt volledig binnen het silhouet (zone 3, kleurwerk). Jordi zei bij ronde 10 "ik zie nog maar 1 arm": in silhouet is er inderdaad maar één arm; de kleurronde moet de nabije onderarm en koevoet vóór de borst duidelijk maken.
8. **Onderbenen** 4–5 px (Jordi wilde ze dun); Weavile heeft 6–7 px, Sneasel 3–4.

## Na het lezen van de maker-notities
- De maker noemt zelf vier zwakke punten (1-px tanden, bocht 90°, "hand met vingers omlaag", staarthaak smaller). Volgens SPRITE_NORM is een zelfgenoemd zwak punt een fail: bevestigd in punt 3 en 5.
- De lezing van de staart als "neerhangende haak" klopt met de render; in silhouet is die haak echter niet te zien (punt 5).
