# Keuring lama fase 2, kleur ronde 1b (onafhankelijke keurder, 2 nov)

Eerst zelf geoordeeld (1×, 3×, 8×, licht en donker, naast de alpaca en 14 Gen 3-sprites: Girafarig, Stantler, Ponyta, Rapidash, Mareep, Flaaffy, Mightyena, Absol, Houndoom, Linoone, Combusken, Marshtomp, Camerupt, Numel; `anim_front_gba.png` + `normal_gba.pal`), daarna pas NOTITIES.md gelezen. Vel: `keuring_vel.png` (boven 1× en 3× naast de alpaca, onder de FAIL-zones op 8×).

## Technische controle (script)
- `lama.png`: mode P, 64×64, transparency 0, 16 kleuren gebruikt.
- **Alpha-diff met `silhouet/ronde1b.txt`: 0** (1188 px). Box x11–54, y3–62.
- Open randen (vul-/lichtkleur naast transparant): **0**. Losse/zwevende pixels: 0.
- Geïsoleerde vachtpixels: vooral bewuste schuine banen op de opgeheven voorpoot (x21–27, y41–46: cilinder, ok) en de pomponkleuren; echte spikkels: zie punt 6.

## Tabel

| # | Punt | Oordeel | Waar | Reparatie |
|---|---|---|---|---|
| N1 | Leest op 1× als een echte Pokémon | PASS | geheel | Leest als slungelige lama/hertachtige naast Stantler/Girafarig. |
| N2 | 3/4 links-voor, kop meer naar kijker, één oog bij lange snuit | PASS | kop x12–25 | Eén oog, snuit linksonder; houding = goedgekeurd silhouet. |
| N3 | Alle ledematen tellen, verre in schaduwtint | PASS | poten | Vier poten tellen op 1×; verre poten in 3/2. (Knie/hak alleen door silhouet bepaald, bevroren.) |
| N4 | Geen Escher | PASS | x24–34, y40–44 | Nabije voorpoot ligt over de verre, gescheiden met 2 (x29). |
| N5 | Geen rechte lijnen waar het dier rond is | **FAIL** | buiklijn y39 x24–50; aguayo x37 y25–31 | Zie punt 2 en 4. |
| N6 | Kopgrootte | PASS | | Silhouet bevroren (35%). |
| N7 | Ogen geïntegreerd | PASS | oog x17–19, y13–16 | Donker bovenlid, glans F (18,14), lichter blauw onderaan (19,16). Klein maar leest; past bij "fase 2 brutaal". |
| N8 | Kenmerken op 1× leesbaar | **FAIL** | halsband, handschoennagels | Zie punt 1 en 3. |
| N9 | Omlijning per kleurgroep, zwart alleen aan schaduwkant, licht linksboven | **FAIL** | verre voorpoot x30 y44–56; verre achterpoot x41 y41–57 | Zie punt 5. Rest ok: lichtkant in 2 (bruin), schaduwkant 1, doek rechts 1. |
| N10 | Geen Chernobyl | PASS | | Geen misvormingen, geen vlakken uit het niets, niets zwevend. |
| V1 | Kop als helm | PASS | kop | Eén kleurfamilie, licht via 5-baan links. |
| V2 | Ruis | **FAIL** (klein) | (36,36), (40,36) | Zie punt 6. |
| V3 | Plat (2D) | **FAIL** | aguayo x37–48, y25–32 | Romp, hals en dij hebben nu volume; de doek is nog een plat vlak met rechte strepen. Zie punt 2. |
| V4 | Mini-oog | PASS | | Zie N7. |
| V5 | Verre ledematen | **FAIL** | zie N9 | Gescheiden met zwart in plaats van met de omlijningsbasis. |
| V6 | Open randen / losse pixels | PASS | | Script: 0 / 0. |
| K1 | Aguayo-halsband leest als ring (leitmotif) | **FAIL** | x19–31, y26–30 | Zie punt 1. |
| K2 | Aguayo-doek op de rug | PASS (met reparatie 2) | x36–48, y25–32 | Leest als gestreepte doek, niet meer als koffer. |
| K3 | Rode MMA-handschoenen met teennagels | **FAIL** | (21,56),(23,56); (28,62),(30,62) | Rood + polsband leest; nagels niet (grijs A op zwart). Zie punt 3. |
| K4 | Oorkwasten | PASS | x12–22, y3–6 | Rode kwasten op beide oortoppen lezen op 1×. |
| K5 | Lamasnuit | PASS | x11–17, y18–23 | Lange snuit met donkere kin/mond, leest als lama. |
| L1 | Zelfde lijn als de alpaca | PASS | | Handschoenen, halsband, oorkwasten en oogstijl gedeeld. |
| L2 | Evolutie, niet volgroeid | PASS | | Slungelige tiener, duidelijk groter en ouder dan fase 1; ruimte voor fase 3. |
| L3 | Vacht iets donkerder (karamel) | PASS | palet 2–5 | Karamel (200,142,85) vs. crème alpaca; lamakant. |

## FAIL-punten en reparaties (alleen kleur, alpha blijft 0)

1. **Halsband leest niet als ring** (x19–31, y26–30). Op 8× een rode U met losse teal/geel/roze pixels erboven en eronder; op 1× een gekleurde vlek. De pompons (D/B/C op y30 x22,24,26 en (28,29),(30,28)) zijn 1 px en lezen als confetti; de bovenste aguayo-rij is onderbroken door vacht (y27 x22–26).
   → Maak de band **twee doorlopende rijen** langs de U (onderrij rood 8 van x20 tot x30, rand 9 eronder), bovenrij doorlopend in 2-px-blokjes. Pompons 2 px (kleur + 9-schaduw eronder) in plaats van 1 px, en aan de rechterkant (x29–31, y25–27) de band zichtbaar achter de hals laten wegdraaien in 9/1 zodat de ring sluit. **Budget ±25 px.**
2. **Aguayo plat en hoekig** (x37–48, y25–32). Linkerrand x37 is een rechte verticale lijn van 6 px; de strepen D/B/E zijn 8 px kaarsrecht en effen (geen licht/schaduw over de lengte).
   → Linkerrand schuin/afgerond laten afhangen (bovenhoek (37,25) naar vacht, onderhoek (37,30–31) naar 9); per streep links 1–2 px lichter (7 voor rood, 6/B voor geel) en rechts 1–2 px donkerder (9, A voor blauw), zodat de doek over de bolle rug buigt. **Budget ±16 px.**
3. **Teennagels lezen niet** (nabije handschoen (21,56),(23,56); verre (28,62),(30,62)). Grijs A tussen zwart 1 valt weg.
   → Per handschoen twee nagels van 2 px in een lichte hoorn-/crèmetint (6, met 3 eronder) onderaan-voor de handschoen, binnen het silhouet. **Budget ±8 px.**
4. **Buiklijn recht** (y39, x24–50): een donkere 2-band van 26 px kaarsrecht (gekarteld met 3, maar leest op 1× en 3× als liniaal).
   → Laat de band in het midden 1 px zakken of de uiteinden 1 px stijgen (x24–28 en x45–50 naar y38), en laat de nabije dij (x45–50) en de schouder van de nabije voorpoot (x24–29) er overheen lopen. **Budget ±20 px.**
5. **Verre poten met zwart aan de lichtkant** (verre voorpoot x30, y44–56; verre achterpoot x41, y41–57). Beide zijn `13321`: zwart links én rechts, wat ze als twee identieke zwart omrande paaltjes laat lezen.
   → Lichtkant (links) in 2, zwart alleen rechts; eventueel 1 px 4 bij de knie/hak als gewrichtsaanduiding. **Budget ±30 px.**
6. **Spikkels op de romp** (36,36) en (40,36): losse 3 in het 4-vlak.
   → Naar 4 (of laten aansluiten op de kernschaduw van y37). **Budget 2 px.**

## Eindoordeel: **BIJNA**
Silhouet exact gelijk, geen open randen, romp/hals/dij nu rond, vacht en lijn kloppen. Wat overblijft zijn kleurreparaties binnen het bevroren silhouet in zes benoemde zones:
1 halsband (±25), 2 aguayo (±16), 3 nagels (±8), 4 buiklijn (±20), 5 verre poten (±30), 6 spikkels (2). **Totaal ±100 px.** Buiten deze zones pixeldiff 0 (kop, oog, oren, snuit, staart, nabije poten, palet).
Let op: halsband en aguayo zijn hun tweede reparatie; slaagt de halsband in de volgende ronde niet, dan stoppen en eerst met Jordi de bandvorm kiezen (werkwijze: na 2 rondes niet doorpatchen).

## Na het lezen van NOTITIES.md
- De maker noemt de halsband "een gekleurde ring met belletjes". Op 3× klopt dat ongeveer, op 1× niet; mijn FAIL blijft.
- De maker zet de band bewust hoger dan de onderlaag (halsbasis valt samen met borst). Dat is een redelijke keuze en raakt het silhouet niet.
- De verre poten en nagels vallen volgens de maker onder "bevroren" (uit ronde 1); ze zijn niet eerder door een keurder bekeken, dus ze staan hier wel open.

## Voor Jordi (smaak, geen opdracht)
- Het oog is kleiner en "brutaler" dan bij de alpaca. Past bij het ontwerp (fase 2 brutaal), maar de lijn verliest wat van de schattigheid van fase 1.
- De handschoenen lezen op 1× als ronde bokshandschoenen; "MMA" (open, kort) is op 64 px eigenlijk alleen via de nagels te tonen.
- Formaat 1188 px is 1,17× fase 1 (norm zegt 1,5–1,7×); het silhouet is goedgekeurd als slank, dus alleen ter kennisname.
- Geen neusgat zichtbaar op de snuit; optioneel 1 px.
