# Eindkeuring Dragonfly Cave: Bibarel-evolutie `sprite_r13` → `sprite_r14` (24 nov)

Alleen de uitvoering gekeurd, geen herontwerp. Vorm, silhouet en onderdelen zijn bevroren (tanden, ogen, neus, potlood, staartvorm, tuinbroekvorm, klep). Gewijzigd zijn alleen lijnpixels en tinten. Het silhouet is alleen onder de staart aangepast (punt 4). Palet ongewijzigd (15 kleuren + transparant).
Jordi: "top, stuur maar naar de eindkeuring, let op lijnen, schaduwconsistentie, kleurtinten. Ook dat de bollen om het hoofd heen goed gelijnd zijn. Verder onder de staart een paar onnodige pixels".

## Gids, letterlijk (`docs/lessen/bronnen/dragonflycave_spriting_guide.txt`)
- r. 96–97: "The "outline shadows" are always black (or ever-so-slightly off-black) on Pokémon sprites".
- r. 112–113 (regel 3): "The outline base and outline highlight colors are also colors. When you're recoloring, you must also recolor the outlines."
- r. 117 (regel 4): "The outlines must be reasonably dark."
- r. 106–107 (regel 1): "the relative luminosity of the shades on the original sprite should always be maintained on the new one."
- r. 421–423: "we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide."
- r. 427: "lighter pixels on the inside of the outline are a far better idea".
- r. 443–444: "the wing "shadow color" is really used where the front wing overlaps the back wing".
- r. 452–456: "Put some of the shadow/outline highlight color on the outlines in the very most highlighted parts [...] place pixels of the outline highlight color on the inside of the outline rather than the outside."
- r. 406: "It has a consistent light source and the shading is reasonably placed."

## Meting r13 (`meet.py`)
- Buitenrand schaduwkant: 91/91 zwart. Lichtkant: eigen tinten (b 39, e 24, g 12, D 10). De basis klopt.
- Om en om op de buitenrand: helmtop (33,6)K–(34,7)b–(35,7)K, staartboven (58,20)K–(59,21)g–(60,21)K. Kleppunt (19–20,12–13): dambord b/c, met lichte c op de buitenrand.
- Lijnklont 2×2 zwart: (42–43,23–24) tussen kraagbol en schouder.
- Zwarte binnenlijnen in de kraag: onderlijnen van de kraagbollen (20–22,29), (24,31), (25–28,32), (29,31). Officiële Bibarel: de onderlijnen van de vachtpluk over het lijf zijn donkerbruin, niet zwart. Voorbeeld uit een eerder gesprek: Gnomad, snor-onderlijn → eigen tint.
- Kraagbollen: links is de rand tegen de hand b-c-b-c (om en om); onder heeft de bol rechts van het midden geen onderlijn (het model heeft er wel een); rechts zijn de bollen één vlak zonder naden, met log-tint e en bijna-zwart (35,14), (20,15) als lijn.
- Tuinbroek linkerbuitenrand: b b b b D D D b (twee lijntinten op één rand). D (L145) is ook te licht voor een buitenlijn (regel 4).
- Onder de staart: zwevende zwarte pixel (54,49), nopje in de heuplijn (53,50) (staat niet in het model), staartstompje (52–53,46–47).
- Tinten: bruin f/d/c + b met stappen van 37/37/38 (goed). Crème C/M/S + D met stappen van 26/26/36 (iets onder ±30, niet aangepast, zie hieronder). Donker L/e + K (35/31). Oranje o/g. Geen banding of pillow shading.
- Schaduw: licht linksboven klopt op helm, klep, armen, tuinbroek (C links → M → S rechts), dijen, staart en log. Uitzondering: de bollen rechts van de snuit (één vlak d).

## Reparaties (56 px, `sprite_r14/bouw.py`; diff buiten de zones = 0, met assert bewezen)
| Zone | px | Wat |
|---|---|---|
| A staartonderkant (punt 4) | 7 | Zwevende pixel en heupnopje weg. Stompje weg: de staart sluit met een zwarte onderlijn op y46. Enige silhouetwijziging: (52,47), (53,47), (53,50), (54,49). |
| B helm en klep | 6 | Helmtop zwart vanaf x33. Kleppunt helemaal b (geen dambord, geen lichte buitenrand). Klep-onderlijn doorlopend b ((35,14) e→b, (38,15) c→b, (20,15) e→b). |
| C kraagbollen links | 7 | Rand bol/hand overal b. (21,21) D→e (snuitlijn), (21,22) D→d (bolvulling). |
| D kraagbollen onder | 17 | Zwarte onderlijnen → b. De bol onder rechts krijgt een onderlijn als boog (31,31)→(32–35,32)→(35,31)→(36,30), zoals in het model. (35,30) b→c voorkomt een lijnklont. |
| E kraagbollen rechts | 15 | Naad bol rechtsboven (39,16), (40,17), (40,18) sluit op de bestaande lijn. Naad tussen de middelste en de rechter bol (40,20), (40,21), (39,22). Schaduwsikkel aan de rechterkant van de middelste bol (3× d→c). Onderlijn e→b. 2×2-zwartklont → één lijn van 1 px (44,22)–(43,23)–(42,24). |
| F tuinbroek linkerrand | 3 | D→b. De buitenrand is nu één tint, donker genoeg. |
| G staart boven | 1 | (59,21) g→K. Geen om-en-om meer. |

Na r14: schaduwkant 92/92 zwart, lichtkant alleen eigen tinten (b 43, e 24, g 11, D 7 op het potlood). Geen om-en-om meer behalve (17,15) in de donkere hand (e/K, niet te zien). Geen 2×2-zwartklonten. Zwarte binnenpixels alleen nog in ogen, mond/tanden, vingers, logdetail en de lijf/staart-grens (schaduwkant van het lijf, net als bij Ursaring). Silhouet en tanden, ogen, neus, potlood en tuinbroekvorm zijn ongewijzigd.

## Oordeel: PASS na de reparaties (r14)
Op 8× (`vergelijk_gen3_8x.png`) en op 1× (licht en donker, onderaan `sprite_r14/vel.png`) leest hij naast Bibarel, Ursaring, Swampert, Linoone en Furret als Gen 3. Elke kraagbol heeft nu een eigen bruine omtrek, ook rechts. Onder de staart staat niets los meer.

## Ter info voor Jordi (niet gewijzigd)
- Crème-stappen C→M→S zijn 26/26 (Taillow ±30–40). Bijstellen kan alleen via het palet, en dat raakt ook de oogband en het potlood. Daarom niet gedaan.
- De potlood-bovenrand is D (L145), lichter dan een Gen 3-crèmelijn (Linoone ±L80–110). Het potlood is bevroren ("uitstekend"), dus niet aangeraakt.
- De zakrand heeft twee tinten: boven D, zijkanten S. Dit is goedgekeurd in r12/r13.

## Bestanden
- `meet.py`: meting r13/r14 en `kop_model_r13_r14.png` (model geprojecteerd op het spriteraster | r13 | r14, 16×).
- `vergelijk_gen3_8x.png`: r14 naast Bibarel, Linoone, Ursaring, Swampert en Furret.
- `../sprite_r14/`: `sprite.png`, `sprite_8x.png`, `vel.png` (r14 | r13 | model 8×; kop 12× met de gewijzigde pixels gemarkeerd; staartonderkant 12×; Gen 3; 1× licht/donker) en `bouw.py`.

## Aanvulling r15: vachtvlekjes (Jordi: "maar kloppen de vlekjes op het lichaam ook met de dragonflycave regels?")
Gids r. 1459–1465: "Fur is shaded by making the outline between the shades, especially the base and shadow colors, jagged and fuzzy like the outline of the fur itself. The jagged outlines often continue into the shading. There is often dithering (blending two colors in a crosshatch pattern) and short lines of the other color near the border between the shades. Don't overdo this, though, or it will look messy, and keep all lines running in the direction of the hairs."
Toets per vlek: blijft alleen als hij aan een tintgrens ligt (kort, spaarzaam, in de haarrichting) of geen vachtvlek is (lijn, poot, mond, tuinbroekrand). Vergeleken met de kale modelreductie (`sprite_r13/reductie.py`).

| Vlek (r14) | Oordeel | Reden |
|---|---|---|
| c (28,26) | blijft | Mondhoek: taps eind van de mondlijn naast de tand (model: lijn). Gezicht, geen vacht. |
| c (27,27) | blijft | Taps eind van de zwarte tandonderlijn, tegen de b-lijn. Mond, geen vacht. |
| d (29,27) | **weg → c** | Lichte pixel ingesloten door lijnen midden in de slagschaduw onder de snuit; licht tegen de lichtrichting in (model: lijn/donker). Opgenomen in die schaduw. |
| c (17,27) | blijft | Op de grens hand/arm; schaduw onder de hand; staat zo in het model. |
| c (49,27), (50,28) | blijft | Geen vlek: diagonale rand (8-verbonden met (48,26), (51,29), (51,30)) van de schouder tegen de staart. |
| c (21,31) | blijft | Smalle reep flank tussen de armlijn en het tuinbroekbandje, aan een tintgrens; opnemen kan alleen in lijn of crème (dan verandert de tuinbroekvorm). |
| c (18,34), (19,35) | blijft | Taps eind van de onderlijn van de arm waar die op de flank/crème stuit (model: lijn). |
| c (26,34), (27,34), (28,35) | blijft | Korte diagonale schaduwrand (3 px) op de grens bruin/crème tussen de bandjes: precies de "short lines ... near the border" uit de gids, in de haarrichting (omlaag). Bruin of crème maken verandert de tuinbroekrand (bevroren). |
| e (45,38) | **weg → d** | Pootkleur midden in de bruine onderarm, naast een armlijn die al doorloopt ((45,37)→(44,38)): verkeerde kleurgroep, maakt een lijnklont. Wordt onderarmvulling d, zoals (46,38). |
| e (51,42) | blijft | Lijf/staart-grenslijn (model: e). |
| e (49,43), (50,44), (50,45) | blijft | Klauwtjes van de poot op de heup tegen de staart, 1-op-1 uit het model (e c e). Poot = eigen kleurgroep, geen vacht. |
| e (43,44)… (43,45), (44,45) | blijft | Onderkant van de poot (poot e/L), geen vacht. |

Schaduwvlakken als geheel volgen de vorm (licht linksboven): schouder f linksboven, onderarm f boven, dijen f linksboven met een c-sikkel rechts/onder, armholte c links van de onderarm (x40–44, y34–39, staat zo in het model). Geen vlakjes midden in een vlak meer.
**r15 = r14 + 2 px** (`../sprite_r15/bouw.py`): diff alleen (29,27) en (45,38), silhouet en lijnen 0 (assert). Vel: `../sprite_r15/vel.png` (r15 | r14 8×, vacht 12×).
