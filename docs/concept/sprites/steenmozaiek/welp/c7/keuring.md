# Keuring welp c7 (onafhankelijke keurder, 15 nov)

Gekeurd: `welp_c7_a.png` en `welp_c7_a_grijs.png`, naast `../c5/welp_c5.png`, de foto (`referenties/chavin_jaguar_beeld_jordi.png`), de volwassen vorm (`af/steenjaguar.png`) en Golem/Graveler/Regirock op 8×, 3× en 1×; koppen op 12×. Eigen vellen, eerst blind.

## Beste kopvariant
Blind gekeurd vóór het bericht van de coördinator: c (voluut boven het oog) las voor mij het meest als Chavín-gravure (de foto heeft zo'n voluut op de kop), a tweede, b het zwakst (twee parallelle verticale strepen lezen als tabbystreep). **Jordi koos A** ("A heeft de lijnen die ik wil"): de koplijnen van A zijn bevroren. Technisch bij A geen MOET: geen rastertje, geen bril, geen frons (de balk y23 x18–21 ligt horizontaal en loopt naar buiten niet omlaag). De 5'jes op y25 (x15, x17) onder de lijnpixels zijn de lichte groefrand, geen dither.

## Oordeel: FAIL (klein): 3 MOET-reparaties op pixelniveau, daarna PASS
Geen nieuwe makerronde nodig: na de reparaties alleen pixeldiff controleren (alleen onderstaande pixels anders dan c7_a).

- **Hoofdvraag (zou Jordi dit mooi vinden?)** Waarschijnlijk ja voor de richting: het lijf is merkbaar meer gehouwen steen dan c5 (gegroefde lijnen met een lichte lip, randjes met hooglicht als afgebroken steen, donkerder vlakken op de schaduwkant, kaakvlak als facet). Voluten, banden en kleuren van c5 zijn behouden. Wat hem nu nog kan tegenstaan zijn precies de punten hieronder: de zware dubbele lijn + blok tussen voorpoot en dij (leest als een donkere "H"), en een paar lichte pixels aan de schaduwkant/buitenrand die als ruis lezen ("willekeurig").
- **Silhouet/gezicht:** alpha-diff met c5 = 0; oog, mond, tong (rij 26–29) pixelgelijk. Oké.
- **Licht:** overwegend consequent linksboven (bovenkanten van poten, dij, staartpunt en schouder licht; rechterkant en onderkant donker). Uitzonderingen in MOET 3.
- **Gen 3-netheid:** steengroep 2/3/4/5 + hooglicht 14, stappen 42/36/34/28: goed. Aantal tintvlakjes < 3 px steeg van 103 (c5) naar 138; voor steen met chips acceptabel, behalve de checker op de rugrand (MOET 3).
- **Grijs-variant:** zelfde indices (diff 0), alleen palet; oordeel geldt voor beide.

## MOET (x,y op 64×64, paletindex)
1. **Dubbele lijn tussen voorpoot en dij (de verticalen van de 'H'):** x34 (idx 2) en x36 (idx 2) + x37 (idx 1) geven twee donkere lijnen met één pixel ertussen: zwaar en rasterachtig. Zet **x36, y49–56: 2 → 3** (zoals c5). Zet **x37, y51–54: 1 → 2** (lijn in donkere tint van het vlak, zoals c5); y49–50 mag 1 blijven als diepste punt (taps).
2. **Blok boven de dij (de dwarsbalk van de 'H'):** y47–48, x35–39 is een rechthoek 5×2 van idx 2 (c5: 2×2). Maak er een taps wigje van: **(35,47), (36,47), (35,48), (36,48), (37,48): 2 → 3**. Over blijft y47 x37–39 en y48 x38–39 (idx 2), aansluitend op de lijn op x37.
3. **Licht aan de verkeerde kant / ruis:**
   - (44,42): 14 → 3 (haalt de checker e‑2‑e op de rugrand weg; (42,42) blijft 14).
   - (53,55): 14 → 3 (hooglicht aan de onderkant van de staartpunt, tegen de buitenlijn: schaduwkant).

## MAG
- (31,31): losse 5 tussen 2 en de buitenlijn op de nek; mag 4 worden (c5 had hier 2-lijn).
- (26,34), (27,34): zwart binnen het lijf in de kinplooi; c5 had 2. Mag blijven als diepste schaduw; 2 is rustiger.
- Kaak: harde verticale tonengrens x21|22, y30–32 (licht 4 | 3). Leest als facet en past bij "gehouwen"; een 4 op (22,31) zou hem iets zachter maken. Alleen als Jordi de kaak noemt.
- Losse hooglichtjes op de dijbanden (28,51), (28,53), (27,54) zijn bewuste groeflippen; laten.
