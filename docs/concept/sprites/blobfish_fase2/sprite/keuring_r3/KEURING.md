# Keuring r3 blobfish fase 2 (verse keurder, 16 nov)
**Oordeel: PASS**, na één kleine MOET (3 px, mechanisch). Plaatjes: `r3_2x.png`, `r3_8x.png`, `naast_8x.png` (model verkleind | r3), `naast_1x_4x.png` (model | kale reductie | r3), `gen3_vergelijk_4x.png` (r3 | Muk | Grimer | Slowpoke | Chansey | Wigglytuff), `model_links_crop.png` / `r3_links_crop.png`.

**Blind (1×/2×/8×):** mooie, leesbare sprite; leest meteen als ingezakte blobfish. Koepel rond en vol, twee kleine visogen, hangende neus met donkere onderrand, brede chagrijnige boogmond met omlaaghangende hoeken, vin rechts, borstvinnetje rechtsonder, rode en bordeaux golflaag eronder. Staat naast Muk/Grimer/Chansey als Gen 3; iets meer textuur (flankplooien) dan Chansey, net als Muk.

**Eis 1, accuraat op het model:** alpha-diff met de kale reductie 0; bbox 61×45 = model 947×702 (zelfde verhouding). Ogen, neus, mond, vinnen, lagen en flankplooien liggen op de donkere modelcellen (gemeten p15 per cel). De losse zwarte pixels (25,35) neus, (51,39) vin, (9,43) mondhoek staan in het model ook donker (p15 ≤ 6). Niets toegevoegd of weggelaten.

**Eis 2, Gen 3:** 15 kleuren + transparant; buitenlijn 1 px, zwart rechts/onder, mauve (9) en rood/bordeaux-selout linksboven; geen pillow shading; licht linksboven; binnenlijnen alleen waar het model ze heeft. Kleine clusters zijn lijnstukken (diagonaal) of komen uit het model.

## MOET
1. Rechterrand onder de koepel, (49,36), (50,37), (50,38): mauve 9 tussen zwart (49,35) en (51,39) = zwart en mauve om en om op de schaduwkant. Het model is daar zwart (p15 8, 0, 3): neem over uit het model → index 1.

## MAG (alleen als het niets anders raakt)
- Linker nubje (6–8, 41–45) is een massief mauve blok; het model heeft daar een klein roze bultje met lichte bovenkant (model (7,42) ≈ 228,190,198). Neem de vulling over uit de reductie, rand blijft selout.
- Onderrand bordeaux linksonder (2,58), (3,59), (10,59), (11–12,60), (13,61): selout F aan de onderkant (schaduwkant); zwart zoals de rest van de onderrand.
- Roze streep op de koepel (x39–44, y23–34) gebruikt lippink 5 (223,144,164); het model is daar zachter (mediaan 201,139,155). Eventueel een eigen tint uit het model.
- Losse 1–2 px tintjes in de vin (54,38) c3, (52–53,39) c4, (52–53,41) c6 en (55,46) c4: samenvoegen met de buurtint uit het model.
- Linkeroog 1 px hoger dan het model: (14,29) zwart, model p15 72 (licht donker); mag terug naar de reductie.

## Dragonfly Cave-eindkeuring (uitvoering)
Silhouet leesbaar op 1×, focuspunt gezicht, geen open randen, geen lichte buitenrand, contrast lijf ↔ lagen goed. Ter info voor Jordi (ontwerp, niet keuren): de lagen nemen ±¼ van de hoogte in; het lijf zelf is daardoor ±40 px hoog.
