# Pinsir-evolutie (Bug/Ground) frontsprite, ronde 3: alleen poten en onderlijf

Bestanden: `pinsir_evo_r3.png` (64×64, geïndexeerd, index 0 transparant, 14 kleuren incl. transparant, palet ongewijzigd), `bouw.py`, `raster.txt` (het onderlijf per onderdeel als tekstraster), `klauwen.txt`, `vel.png` (r3 8× | r2 8× | model 8× / close-ups 12× met raster, o.a. poten en staart / 1× op wit, licht, donker). Bouwen: `cd pinsir_evo && python3 sprite_r3/bouw.py [toon]`.

## Opdracht
Alleen poten en onderlijf (y ≥ 36, x ≥ 14: arm met klauwen linksonder, twee benen, buik, staartaanzet); de rest pixel voor pixel gelijk aan r2. Probleem r2: donker veld met losse lichte plekken; het model heeft duidelijke delen.

## Controle (script, `bouw.py`)
- diff met r2 boven y36: **0**; diff in kaak en dekschild (+1 px rand), x < 14 en overal buiten de zone: **0**; silhouet-diff met r2: **0**.
- 401 van de 699 zonepixels anders dan r2. Zwart 28,1 % (r2 29,4 %). Lijftinten 2/3/4/5: 271/309/149/111.

## Werkwijze (model overnemen)
Per spritecel in de zone gemeten in het 1024-model: zwartaandeel (modellijn) en gemiddelde helderheid van de niet-zwarte modelpixels. Daarmee per onderdeel een tekstraster (`raster.txt`): zwart op de modellijnen, binnen elke plaat de modelschaduw (helderheid < 34 → 2, < 51 → 3, < 80 → 4, ≥ 80 → 5 = modelglans). r2 deed dit per plaat met de mediaan (< 50 → 2): bijna het hele onderlijf werd tint 2, alleen de glans 5, vandaar de losse lichte plekken.
Onderdelen zoals in het model:
- **Arm links** (x15–24, y42–51): diagonale band, selout boven, lichte strook 4 erlangs (modelglans), 3 binnenin, zwarte rechterrand; zwarte polslijn y50.
- **Hand links** (x14–19, y50–56): handpalm 3/2, drie klauwen (A x18–19 y52–53, B x14–15 y54–55, C x17 y55–56).
- **Linkerbeen**: dijplaat (x24–28, y46–47) 4; ronde knieplaat (x22–25, y47–53) met glans 5 op (23–24, 48–50), 4-rand, 3 onderaan, zwart eromheen; scheen (x24–30, y53–56) donker 2 zoals het model; voet met twee klauwen (y56–58).
- **Buik**: borstplaat (y36–39) 2, segmentlijnen y40 en y45, segment B (y41–44) 3 met 4 onderaan (model lichter onderaan), segment C (y46–47) 3, lijn y48; schouderplaatje (x33–37, y36–38) 4.
- **Onderarmstrook** (x35–40, y39–51): lichte diagonale strook 5/4 met zwarte randen (model: lichtste deel van het onderlijf); **middelste hand** (x30–38, y51–59) met drie klauwen.
- **Rechterbeen**: grote ronde dijplaat (x40–48, y45–49) met glans 5 op (42–43, 47–48), 4 eromheen, 3/2 naar rechtsonder; zwarte boog y50 (dij/knie, model); ronde knieplaat (x40–46, y51–54) met glans 5 op (43–44, 51) en (43, 52); onderlijn y55; scheen 3 (y55–57); twee klauwen (x41–43 en x47–49, y58–61).
- **Staart** (x48–63, y45–54): lichtere bovenband 4, midden 3, onderkant 2 (model 28), segmentlijnen op de modellijnen (x51–52, x54–55, x57–58); stekels als selout.

## Pixels die niet 1-op-1 uit het model komen
- `bouw.py` telt per onderdeel de pixels die afwijken van de **directe** celvertaling (cel ≥ 60 % zwart → K, anders helderheid → tint): arm+hand 38, linkerbeen 34, buik 24, strook+middelste hand 65, rechterbeen 99, staart 33, rest 1 = **294**. Oorzaken, alle benoemd:
  1. **Lijnen samengevoegd tot 1 px op de modellijn**: modellijnen vallen vaak op een celgrens (twee cellen 30–50 % zwart, geen van beide ≥ 60 %): één van de twee wordt K (bv. segmentlijn y45 x28–35, boog y50 x42–46, knieranden x26 en x39/40).
  2. **Plaatschaduw gladgestreken**: de modeltint per cel springt (bv. dij 58/59/68/93); binnen een plaat is gekozen voor één ring (4), één glanskern (5) en schaduw rechtsonder (3/2) zoals in het model, i.p.v. per cel. Rechterdij en -knie één tint donkerder aan de buitenkant dan de celvertaling (anders één lichte vlek samen met de strook).
  3. **Buitenlijn Gen 3** (40 px): randpixels zwart aan de schaduwkant, selout 3 aan de lichtkant.
  4. **Klauwen** (24 px, `klauwen.txt`): na stap 3 waren alle klauwen zwart (zoals in r2). Lichte klauwpixel 4/5 op de rand aan de lichtkant, zwart op de punt. Dit zijn de enige lichte pixels op de buitenrand (`controle.py`: 24 stuks, allemaal klauw).
  5. **9 losse correcties tegen tintvlekjes**: (25,40) 3→2, (35,38) 3→4, (44,44) 3→K (bovenrand dij), (40,44) 3→4, (40,47) 3→4, (27,49) 2→3, (47,50) 3→2, (48,51) 3→2, (56,49) 4→3.
- Niet in het raster (r2 gehouden): rugstekels (53–54, 37–38) en (55, 43–44) aan de rand van het dekschild.

## Twijfels
- **Helderheid**: het onderlijf is nu één tintstap lichter dan de modelmapping van de rest van de sprite (daar < 50 → 2). Met die mapping wordt het weer een donker veld; nu lezen de platen, maar het onderlijf is lichter dan in het model (kleur mag afwijken, vorm niet).
- **Klauwen op de rand** zijn licht (uitzondering op "geen lichte kleur op de buitenrand"); anders verdwijnen ze. Op 1× lezen ze als kleine lichte puntjes.
- **Tintvlekjes < 3 px**: in de zone vooral de 1-px lichtstrook langs de arm (diagonaal) en de klauwen; totaal sprite 153 (r2 99).
- **Middelste hand** (x30–38, y51–59) blijft druk: drie klauwen en een handplaat op ±8×8 px.
- Borstplaat en scheen links blijven tint 2 (model 29, het donkerste deel); ze lezen als vorm door hun zwarte rand en de lichtere platen ernaast.
