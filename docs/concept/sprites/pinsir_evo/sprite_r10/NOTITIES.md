# Pinsir-evolutie frontsprite, ronde 10 (alleen de kop)

Jordi bij r9 (letterlijk): "het hoofd is gewoon nog steeds niet zoals het model en hij kijkt scheel". Eerder: "gewoon het model volgen", "je moest alleen de ogen een paar pixels aanpassen", "en dan verneuk je het hele hoofd lekker", "lekker opnieuw tekenen want dat kan je zo goed".

Bestanden:
- `pinsir_evo_r10.png`: oog A, hoofdvariant.
- `pinsir_evo_r10_oogB.png`: oog B.
- `kaal_kop.png`: de kale modelreductie van de kop, vóór opschoning en gezicht.
- `zone.npy`: het kopmasker.
- `bouw.py`.
- `vel.png`: kop 16× r10 | r9 | model met spriteraster; r10-B | r10 met rode modelmaskeromtrek | kaal; hele sprite 8× naast het model; 1× en 2× op wit en donker.

Formaat: 64×64, geïndexeerd, index 0 transparant, 16 kleuren (palet r9).

Bouwen: `cd pinsir_evo && python3 sprite_r10/bouw.py [raster]`.

## 1. Waar de r9-kop afwijkt van het model
Model op dezelfde registratie als `sprite_r1/kaal.png` (cel 15,22 modelpx, x31/y134, rij 13). Gemeten per kwart pixel.

**Silhouet.** Het r9-silhouet valt bijna samen met het modelmasker (dekking ≥ 0,35). Het verschilt op 6 pixels:
- r9 heeft 5 extra pixels: (25,16), (22,18), (40,18), (17,19) en (14,20). Dat zijn de stekelverbredingen van r7, die het model niet heeft.
- r9 mist de punt (23,16) van de voorste grote schildstekel.

Het probleem zit dus binnen de omtrek.

| rij | r9 | model |
|---|---|---|
| 13–17 | stekels als zwarte blokjes; de stekel achter het schild (x25–27) staat 1 kolom te ver links (25,16) | stekels met een lichte linkerflank. Punten: x15,5/y19,6 · x18,7/y18,3 · x23,7/y16,6 · x26,6/y15,6 · x32,7/y13,3 · x38,5/y13,6 · x44,2/y18,3 |
| 18–20 | bovenrand rafelig door de r7-verbredingen (22,18), (17,19), (14,20) | bovenrand: vanaf de punt x11/y22 stijgend naar x15/y20, vlak tot x22 op y19,5; daarboven de stekels |
| 20–22 | één grote crème vlek (d) op x14–19 rij 20–23 | lichte afschuining net binnen de bovenrand (x12–14, y21,8–23) en een lichte Y-rug (x16–19, rij 21–22, omlaag langs x18–19 tot rij 25) in de middentoon van het schild. Geen crème vlak |
| 22–24 | punt linksvoor als zwart blok van 3×2 | punt linksvoor: 1 px zwarte omtrek op x11 rij 22–23; daaronder begint meteen de donkere onderkant |
| 23–26 | onderrand van het schild onduidelijk: losse K's op (12,24), (13,25), (14,26), (16,26) en b/c ertussen | **lichte schildrand** loopt van de punt schuin omlaag: (12,23) → (14,24) → (16,25) → (17,26), daarna vlak over rij 26 tot x32. **Donkere onderkant** eronder: (12,24) → (13–14,25) → (14–16,26) |
| 26–28 | het schild valt als rechte zwarte rij (22–24,26) over het nabije oog; tussen de ogen staat zwart en crème door elkaar | de onderrand van het schild is een **zwarte V**: boven het verre oog op rij 26 (x14–16), zakt via (17,27) naar rij 28 (x18–20), en loopt als wenkbrauw boven het nabije oog op rij 27,5 (x21–27). Tussen de ogen ligt een lichte tong van de schildrand (x18–20, rij 27) |
| 27–28, ogen | ver oog: T (16,27), T (16,28), K-pupil (17,28), T (18,28), dus twee losse stukken. Nabij oog: wig met K-pupil midden-onder (22,28). Pupillen op verschillende plekken: **scheel** | ver oog: lichte spleet x16,1–16,8, y26,7–28,0, met staartje naar binnen-onder (x17,1–17,4, y27,9–28,2). Nabij oog: x20,8–23,9, y27,7–28,8, binnenkant (x21) iets lager, buitenkant (x22–23) iets hoger. Beide lopen naar het midden omlaag (\ /). **Geen pupil** |
| 18–24, achterkam x25–44 | middentonen met losse vlekken | donkere kam (≈30) met drie lichte kegels: x26–27 rij 20–21, x29–32 rij 19–22 (groot), x35–37 rij 19–21. Plus een donker streepje op het schild (x24–25, rij 23–25) |

## 2. Opbouw r10 = verkleining van het model
Per cel van de kopzone. De kopzone is de r9-kopzone zonder kaak- en dekschildpixels en zonder kolom 45, de naad met de r8-rugdoorn.
1. **Silhouet** = modeldekking ≥ 0,35. De rand is zwart, zoals in de rest van de sprite.
2. **Binnenlijn:** een binnencel met ≥ 35 % modelzwart wordt lijntint L. Er komt dus geen extra zwart bij.
3. **Toon:** de andere binnencellen krijgen de mediaan van de niet-zwarte modelpixels, omgezet naar de r9-lijftinten: < 38 L, < 54 a, < 78 b, < 128 c, anders d. Het schild gebruikt K/L/a/b/c/d. De crème d komt alleen nog voor op (17,26), de lichtste plek van de schildrand.

Wat de reductie zo levert, zonder ingreep:
- de lichte schildrand en de donkere onderkant (punt 1);
- de Y-rug: c op (18–19, 23–25);
- het streepje: a op (24,24);
- de kegels als lichte pixels: (27,17), (28,20), (29–31,20–22), (32–33,23), (35,20);
- de donkere kam.

## 3. Pixels die niet uit de kale reductie komen
A wijkt op 25 pixels af, B op 24.

**Stekeltips (4).** Een smalle punt die ≥ 1/3 rij in de cel steekt, maar onder de vlakdrempel blijft, krijgt die cel als punt.
- (15,19): modelpunt y19,6, dekking 0,30.
- (23,16): modelpunt y16,6.
- (26,15): modelpunt y15,6, dekking 0,30.
- (38,13): modelpunt y13,6, even hoog als de linker grote stekel.

**Vlekje (1).** (20,20) b → c: een losse b tussen c-pixels. Het model is daar 75 % licht ('=---') en de mediaan (74) lag op de grens.

**Gezicht (19), per pixel uit het model.**
- Zwarte V:
  - (15,26) en (16,26): K, waar de reductie L gaf;
  - (17,27): K;
  - (18–20,28): K;
  - wenkbrauw (21–24,27): K.
- Ogen T: ver oog (16,27), (16,28), (17,28); nabij oog (21,28), (22,28), (23,28).
- Lichte tong (18–20,27): c.
- (15,27): K, de zwarte rand links van het verre oog.
- Wangen (14,27) c, (15,28) b, (24,28) b.
- (17,26) d is gelijk aan de kale reductie.

**Alleen in A (2).** (23,27) T en (23,26) K.

## 3b. Ogen: A en B
Beide ogen zijn spleten zonder pupil, zoals in het model, en lopen naar het midden omlaag.
- **Ver oog** (beide varianten): buitenkolom van 2 hoog, (16,27) en (16,28), met een voetje naar binnen-onder op (17,28). Dat is de schuine streep \.
- **A (hoofdvariant).** Het nabije oog is het spiegelbeeld: buitenkolom (23,27) en (23,28) met een voet van 2 naar binnen op (22,28) en (21,28). Dat is de streep /, door het perspectief 1 px breder. Beide ogen zijn even hoog (rij 27–28) en geven samen een boze V.
  - Hiervoor schuift de wenkbrauw boven (23,27) één rij omhoog, naar (23,26).
  - Dat wijkt af van het model: daar ligt die wenkbrauw vlak op y27,5 en zit het nabije oog lager.
- **B (letterlijk het model).** Het nabije oog is een platte spleet (21–23,28) onder een rechte wenkbrauw. Het verre oog staat 1 rij hoger, zoals in het model.

Grootte: A heeft 3 + 4 oogpixels, B 3 + 3. r9 had 3 + 3 lichte pixels plus pupillen. Geen van beide is dus kleiner.

## 4. Controle (bouw.py)
- Diff buiten de kopzone met `sprite_r9/pinsir_evo_r9_A_A.png`: **0** (A en B).
- Het silhouet van de kop verschilt van het modelmasker alleen op de 4 stekeltips. De rode omtrek staat in `vel.png`.
- Zwart in de kop: 67 (r9: 70).
- 16 kleuren, index 0 transparant; heropend en vergeleken.

## Zelf gezien
- De achterkam blijft op 64 px een donker vlak met lichte stipjes. De kegels lezen niet als kegeltjes, maar het zijn de modelplekken.
- Stekels van 2 px breed (x32–33 rij 13–14, x38–39 rij 15) zijn helemaal zwart. Het model heeft daar een lichte flank, die op die breedte in de omtrek valt. Waar de stekel een binnenpixel heeft, staat de modeltoon: c op (27,17), (38,16) en (37,17), b op (33,15–16).
- Variant A wijkt 2 px af van het model voor de gevraagde gespiegelde schuinte. B is het model letterlijk.
