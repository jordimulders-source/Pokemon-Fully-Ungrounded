# Kudu sprite ronde 4 (verse maker)
Start: r3 (`r3/grid.json`). Model: `r3/model_A3.png` (door Jordi akkoord). Script: `sprite/r4.py` (oogvariant als argument: `python3 r4.py A|B|C|D`, `HOOFD='B'` bovenin bepaalt welke `kudu_r4.png` wordt). Oogvarianten: `oog4.py`, vel `oogvel4.py`; vel en lijnkaart: `vel4.py`.
Bestanden: `kudu_r4.png`, `kudu_r4_8x.png`, `vel.png` (r4 | r3 | model, 8x; 1x op licht en donker naast de impala), `lijnkaart_hals.png`, `oog_zwart_varianten.png`, `kudu_r4_oog{A,C,D}.png` (+ 8x), `grid.json`, `lijnen.json`, `telling.txt`, `wijzigingen.txt` (per pixel: stap, oud -> nieuw, reden). Palet: 15 kleuren incl. transparant.

## 1 Nek/hals (Jordi: "dat je de nek niet helemaal goed ziet in de sprite, dat moet duidelijker")
- **Oorzaak in r3:** `zones.py` maakte met een vaste rechthoek (model x200-345, y440-740) alles onder rij 27,5 tot manen. Daardoor werd de onderkant van de wang (rij 28, x7-14) haartint en liepen kop en hals in elkaar over.
- **Nu:** zone per modelpixel op kleur. Haar = blauw < 0,31 x rood (modelhaar 204,168,48 / 156,120,24 / 144,108,12). Vacht = goud met meer blauw (216,168,72). Gemeten: kop, keelfranje, hals en schoudermanen zijn zo netjes gescheiden.
- **Kaaklijn** (groen in de lijnkaart): de zwarte modellijn onder de wang, van (8,28) via (13,27) naar (14,24). In de sprite als binnenlijn in D (donkerste vachttint), 9 px. Erachter en eronder staat haar uit het model.
- **Hals zelf:** het model laat tussen keelfranje en halsmanen een smalle strook vacht in de schaduw zien (x13-14, rij 28-40). Die strook staat nu als D. In r3 was hij haar.
- **Manenrand over de vacht** (blauw): een haarcel met een vachtbuur, waar het model een zwarte lijn heeft (≥ 12% lijnpixels binnen 1,5 cel), wordt d. Dit geeft de rand van de schoudermanen (x26, rij 31-40) en de lokpunten op de borst.
- **Borst:** de vacht onder de lokpunten (x21-28, rij 41-46) is vachttint uit het model.
- **Mond:** (7,28) is het witte lip van het model; (4,28) is terug naar r3.

## 2 Manen
- **Kleur.** Modelgoud, iets donkerder dan de vacht, hue ±43° (vacht ±38°):

  | Tint | r3 | r4 |
  |---|---|---|
  | l | #D0A038 | #D8AC30 |
  | m | #A87C24 | #B08824 |
  | d | #6C4C14 | #7C5A10 |

  Daarnaast komt d alleen nog op lijnen; r3 had grote d-schaduwvlakken.
- **Toon per cel** is de meerderheid van de modelhaartonen (licht ≥ 140, midden 108-140, donker < 108).
- **Strengen** (rood in de lijnkaart, 64 cellen). Skelet van de zwarte modellijnen in het haar (4x verkleind, Zhang-Suen), alleen componenten van ≥ 4 cellen hoog. Per rij gaat de prioriteit naar de langste modellijn. Een strengcel binnen 2 kolommen van een al gekozen streng valt af, zodat elke lok ≥ 2 px breed is (dus geen "dldld"-zebra).
- **Lokken.** Tussen twee strengen is per rij licht links (l) en donker rechts (m). **Dit is een regel, niet per pixel uit het model** (87 px, stap `lok`). Per rij uit het model meten gaf vlekken. Licht komt van linksboven.
- **Punten onderaan** komen uit het silhouet van de kale reductie (niet veranderd).
- **Kam over de rug** (x ≥ 21, rij 25-31): in het model liggen de lokken daar liggend/schuin naar rechts. De lokregel gaat daar daarom per **kolom**: strengen = skelet van de modellijnen (per kolom 1 cel binnen 2 rijen); tussen twee strengen boven l (licht van boven), onder m (41 px, stap `kam`).

## 3 Hoorns
- **Staal neutraal** (niet blauw):

  | Tint | r3 | r4 |
  |---|---|---|
  | A | #3C4864 | #4A4A52 |
  | 3 | #62749A | #8A8A92 |
  | 4 | #B4C4D8 | #C8C8CC |

  W blijft wit.
- **Binnenkant per pixel** = de meerderheid van de modelstaaltonen in de cel: wit (≥ 215) W, lichtgrijs (165-215) 4, grijs 3. Zo leest de spiraal zoals in het model: per draai een wit stuk (voorkant) en een grijs stuk (achterkant). Losse pixels gaan naar de buurtint.
- **Vorm:** de band uit r3. Alleen de bult op rij 8 van de linkerhoorn is weg: (11,8) wordt transparant, (10,8) wordt lijn, zodat de rechterrand gelijk loopt met rij 7 en 9 (model: hoorn x 7,7-9,6).

## 4 Flank
- Vachttint per cel uit de modelhelderheid, waarbij de lichte rand rond de witte strepen (4 px) niet meetelt. Daardoor de L-vlekken tussen de strepen weg. L ≥ 181, M ≥ 160, D eronder.
- Resultaat: lichte band bovenop de flank, M midden, D-sikkel onder de buik (model: buik ±146-150).
- Strepen: de doorlopende 1-px-lijnen uit r3.

## 5 Oog (Jordi: "kudu irl heeft een zwart oog"; uitdrukking kalm, half gesloten lid)
- **Model:** dikke zwarte lidlijn op rij 22 (x 10,3-13,3). Daaronder een plat oog van 1 rij. Zoekscript over alle Gen 1-3 `anim_front_gba.png` (glanspixel omringd door donker, geen oogwit); daarna met het oog nagekeken.
- **Bruikbaar zonder oogwit:** Ponyta, Kangaskhan (donker oog onder zwaar lid), Flareon, Lickitung (glans linksboven, valt af), Eevee (te hoog). Camerupt, Numel en Rhyhorn hebben oogwit; Tauros is lila/boos.
- **Varianten** (`oog_zwart_varianten.png`, elk met de bron op 8x):
  - **A: Kangaskhan 1-op-1**, box (39,38)-(42,40). Het lid zit in de bron.
  - **B: Ponyta 1-op-1**, box (17,26)-(19,28), plus het lid uit het model (rij 22, x10-13). **Staat in kudu_r4**: leest het kalmst; vlak lid over een klein zwart oog met glans, zoals het model.
  - **C: Flareon 1-op-1** (rechteroog, box (23,29)-(27,32)), plus het lid uit het model. Groot en rond.
  - **D: Ponyta 1-op-1** met haar eigen lid, zonder modellid.
- **Omkleuring:**
  - zwart → 0
  - donkergrijs/donkerbruin → K
  - glans → W
  - grijze tweede glans (Flareon) → 3
  - mauve (Kangaskhan) → D
- **Oogvlak:** eerst leeggemaakt (impala-oog uit r3 weg), daarna vacht/wit uit het model.

## 6 Belijning
- **Buitenlijn opnieuw**, licht linksboven: een rand die naar boven of naar links wijst krijgt een selout in de donkerste eigen tint (vacht D, manen d, staal A, oor r), zoals bij de impala (links index 2, rechts zwart). De rest is zwart.
- **Is de binnenkant al de donkerste tint** (verre poten), dan wordt de rand zwart; anders blijft de rand open.
- **Twee losse zwarte pixels** tussen selout zijn selout geworden: (9,37) en (24,53).
- Hoeven en hoeflijn zoals in r3.
- **Ontkorrelen:** vachtvlakjes < 3 px gaan naar de buurtint (31 px). De lokken zijn uitgezonderd.

## Pixels t.o.v. de kale reductie (model A3, gemapt; telling.txt)
**643 van 1361 px wijken af:**

| Zone | Pixels |
|---|---|
| manen | 199 |
| vacht | 196 |
| staal | 136 |
| lijn | 83 |
| donker | 11 |
| roze | 9 |
| oog | 9 |

**T.o.v. r3: 336 px:**

| Zone | Pixels |
|---|---|
| manen | 152 |
| vacht | 111 |
| staal | 57 |
| oog | 9 |
| roze | 4 |
| lijn | 3 |

## Pixels die niet uit het model komen (benoemd)
- **lok (87) en kam (41):** l/m per lok volgens de regel licht links, donker rechts (in de kam: licht boven, donker onder).
- **oog (Ponyta-bronpixels, 8):** het lid (4) is wel uit het model.
- **hoornbult (2):** vormreparatie.
- **selout/buitenlijn:** de regel "lichtkant = eigen donkerste tint" bepaalt de kleur. De plek komt uit het silhouet van het model.
- **ontkorrel (31):** tintvlakjes < 3 px naar de buurtint.
- **uit r3 overgenomen** (niet opnieuw uit het model):
  - poten volgens Kirlia (tint in de lengte)
  - hoeven volgens de impala
  - flankstrepen als 1-px-lijnen op het streepmidden van het model
  - de hoornband (breedte 4)

## Eigen zwakke punten (na eigen reparatie)
- **De halsstrook in D** (x13-14) staat in het model, maar leest op 8x als een bruine baan tussen keelfranje en halsmanen. Graag oordeel van de keurder of dit de hals laat lezen of als extra streng leest.
- **Buiksikkel (D):** de bovenrand is op rij 44 tussen x29 en x38 vrijwel recht. Dat komt uit de modelhelderheid; ik heb hem niet gebogen, omdat dat hertekenen zou zijn.
- **Hoornvorm:** dezelfde band als in r3 (S-bochten van het model). Kleur en spiraal lezen beter. Waar het model een vloeiende curve heeft, zijn de randtrappen van 1 px diagonaal; verder niet aangepast.
- **Hue van het haar:** het haar ligt dicht bij het modelgoud, maar naast de oranjere vacht kan het op 1x iets groenig/mosterd lezen.
- **Kam van de manen over de rug:** gerepareerd met liggende lokken (zie punt 2). De losse lokpunten die in het model naar rechtsboven uitsteken, vallen buiten het silhouet van de kale reductie; die zijn niet toegevoegd.
