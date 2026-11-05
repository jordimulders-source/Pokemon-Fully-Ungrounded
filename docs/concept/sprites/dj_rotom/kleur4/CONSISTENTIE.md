# DJ Rotom kleur4: consistentie met de 6 game-Rotoms

Vraag van Jordi: "best goed al, laat een agent het met de andere rotom sprites vergelijken en kijken of er dingen zijn die consistent zijn die in deze sprite missen".

Vergeleken: `graphics/pokemon/rotom/anim_front.png` + `{heat,wash,frost,fan,mow}/anim_front.png` (beide frames), `normal.pal`, `shiny.pal`, `back.png`, en de species-data (`gen_4_families.h`). Getoetst: `kleur4/dj_rotom.png`. Vel: `consistentie_vel.png` (3× en 1× op licht en donker, frame 2 van de game-vormen, uitsneden op 8× (A–E) en de paletten).

Alles is met een script gemeten (paletindexen, pixeltellingen, de kleur van de pixel die tegen de gloed ligt per zijde, de dikte van de gloed, zwaartepunten). Coördinaten: x,y in het 64×64-vak, frame 1. Indexen van DJ: 1/2/3 = gloed donker/licht/kern, 4 = oranje hooglicht, 5 = midden, 6 = donker, 7 = donkerst, 8 = zwart, 9/a = navy speaker, b = grijs, c/d = iris, e = equalizergroen, f = wit.

## Tabel per kenmerk

| # | kenmerk | de 6 game-Rotoms | DJ Rotom kleur4 | oordeel |
|---|---|---|---|---|
| 1a | **Oranje: tinten** | Alle 6 precies dezelfde 4 tinten: **248,168,128 / 232,112,40 / 192,72,24 / 120,56,32**. Fan heeft 2 extra fan-tinten. | 4 tinten: 246,164,131 / 230,115,41 / 189,74,24 / 123,57,32. | **wijkt af.** Het verschil is klein, maar gbagfx deelt door 8: 246→30 tegen 248→31, 230→28 tegen 232→29, 189→23 tegen 192→24. In de ROM zijn hooglicht, midden en donker van DJ dus elk één GBA-stap donkerder dan bij de andere Rotoms. Wit 246 tegen 248 geeft hetzelfde probleem. |
| 1b | **Volgorde van de indexen** | Is niet gelijk: de oranje tinten staan per vorm in een andere volgorde. Het patroon is wel vast: 0 = 152,208,160, daarna 1–2(–3) = gloed, dan de 4 oranje tinten, dan zwart/wit/grijs, en de vormkleuren achteraan. | 0 = 148,205,156; 1–3 gloed; 4–7 oranje; 8 zwart; daarna de vormkleuren. | **gelijk** (patroon). Index 0 voor de netheid op 152,208,160 zetten. |
| 1c | **Shiny.pal** | Bij alle 6 is het recept hetzelfde. Gloed → **232,160,112 / 240,200,160**, de lichte plasmakern (3e gloedtint) → **240,224,200**. Oranje → roze: 248,168,128→**248,128,168**, 232,112,40→**224,56,112**, 192,72,24→**184,24,80**, 120,56,32→**120,0,40**. Zwart, wit en grijs blijven gelijk. | Heeft nog geen shiny.pal. | **mist** (recept hieronder). |
| 1d | **Grijs** | 184,184,184 in alle 6 (oog onderaan, tanden). | 164,172,189 (blauwgrijs, index b). | **wijkt af** (klein). |
| 1e | **Iris** | Iris in de tint van de vorm: Heat rood, Wash/Rotom blauw, Frost paars, Fan geel, Mow groen. | Blauwgroen (bron), naast een mintgroene gloed. | **gelijk** (zelfde familie). |
| 2a | **Spits** | Een vrije oranje kegel van **9–11 px hoog**, met een basis van 4–5 px. Hooglicht-streep links van het midden, donker rechts. Steekt boven alles uit en heeft zijn eigen gloed. Rotom y16–27, Heat y18–28, Wash y7–17, Frost y4–13. | Zichtbaar maar **±6 px** (y26–31, x24–29), met de lichtstreep op x26 y27–32. De bliksem zit vast op de punt (staart y19–25 loopt over in de spits), dus de punt zelf zie je niet. | **mist** (de bron toont de spits ook duidelijk en vrij). |
| 2b | **Grijns met tanden** | 5 van de 6 hebben een grijns 1–2 rijen onder de ogen (Frost f1 een open mond). De tanden zijn **losse** witte pixels, gescheiden door zwart of grijs; de mondhoeken buigen omhoog. Zie Wash x24–30 y26–27 en Heat x24–28 y37–38. | U-grijns: hoeken (21,42) en (27,42), zwart (22,43) en (26,43), wit **één blok** x23–25 y43, zwart x23–25 y44. Staat 2 rijen onder de ogen. | **wijkt af.** Eén witte balk in plaats van losse tanden; de bron heeft er ook twee. |
| 2c | **Plek van het gezicht** | Recht onder de spits, op het bovenste deel van het "hoofd"-volume. De as van de spits loopt tussen de ogen. | Op het middenblok; de as van de spits (x26) loopt tussen de ogen (x18–21 en x26–29). | **gelijk** |
| 2d | **Maat van de ogen** | ±4–5 breed × 5–6 hoog; afstand tussen de ogen 3–6 px. | 4 × 6–7; afstand 4 px. Frost-sjabloon. | **gelijk** |
| 3a | **Gloed: opbouw** | 2 tinten: een donkere buitenring (index 1, 100% van de buitenste pixels) en binnen een lichte band. Nergens zwart aan de buitenkant. | Idem: index 1 is 100% van de buitenrand, met daarbinnen index 2. | **gelijk** |
| 3b | **Gloed: dikte** | Meestal 2–3 px. Gemeten (pixels van lichaam tot transparant): Wash 2:102/3:66, Fan 3:85, Mow 2:94/3:49. Dikker (4–8) bij uitsteeksels en plasma. | 2:148, 3:20. Bijna overal precies 2 px. | **gelijk** (iets stijver) |
| 3c | **Gloed: verzadiging** | Zuivere, verzadigde tint van de vorm (Mow 0,152,0 / 0,200,0; Frost 176,80,200 / 200,112,248). Base Rotom het bleekst: 40,168,184 / 88,192,184. | Bleek mint 65,164,123 / 131,213,164 (bron). Op een lichte achtergrond op 1× zwak. | **wijkt af** → vraag voor Jordi |
| 3d | **Contour binnen de gloed, schaduwzijde (R/O)** | **Zwart (16,16,16)** als binnenlijn tussen oranje en gloed rechts en onder. Tegen de gloed op R+O: Wash 71, Frost 68, Mow 74, Fan 53, Heat 38, Rotom 16 px. | **8 px** zwart. Hier staat het donkerste oranje (7): 89 px. | **mist** (grootste systematische verschil) |
| 3e | **Contour binnen de gloed, lichte zijde (L/B)** | **Donkerste oranje (120,56,32)**. Tegen de gloed op L+B: Wash 59, Heat 33, Frost 40 px. | **Donker (6)**: 60 px. Donkerst: 5 px. | **wijkt af**: de hele contourladder staat één stap te licht |
| 3f | **Naden tussen volumes** | Zwart: de deurnaden van Frost, de trommelring van Wash, hoofd tegen maaier bij Mow. | Donkerst oranje (7): x15 y38–56 (linkerspeaker/hoofd) en x34 y32–58 (hoofd/rechterspeaker). | **wijkt af** |
| 4a | **Plasma: opbouw** | Donkere rand (1) → lichte vulling (2) → witte of zeer lichte kern als streep. Alleen Frost heeft geen kern. | Rand 1 → vulling 2 → kern 3 (2 px) + witte noot. | **gelijk** |
| 4b | **Plasma-ledematen** | Alle 6 hebben plasma buiten het apparaat, meestal **2 ledematen opzij** (armen of bliksems). Mow heeft er 1 in frame 1 en 2 in frame 2. Het plasma komt **nooit uit de spits**. | Eén bliksem die op de spits staat (bron). | **wijkt af.** Eén element kan (Mow f1 is precedent); het aantal is een vraag voor Jordi. Dat de spits vrij staat, klopt wél met de bron (zie 2a). |
| 5a | **Richting van het licht** | Linksboven. Het zwaartepunt van het hooglicht ligt t.o.v. het lichaam op dx −3…−8, dy −5…−10; het donker rechts (dx +3…+7). | Hooglicht dx −6,8, dy −9,1; donker dx +1,7. | **gelijk** |
| 5b | **Hoeveel hooglicht** | Weinig. Hooglicht is 3–7% van het oranje, als **vlekjes**: de streep in de spits, één wangvlek linksboven bij het linkeroog, een glimp op een uitsteeksel. Nooit doorlopende randlijnen. | **10%** (81 px), als **lijnen** langs de randen: hoofd boven x18–32 y33 en links x17 y34–44; rechterspeaker boven x36–54 y28–32 en links x36 y33–44; linkerspeaker boven x6–13 y38–40 en links x5 y41–47. | **wijkt af** |
| 5c | **Verdeling van het oranje** | Midden (232,112,40) overheerst: 41–51% van het oranje. Donker 26–37%, donkerst 9–21%. | Midden 32%, donker 40%, donkerst 17%. | **wijkt af** (donkerder en harder; deels door de onder- en zijvlakken in 3/4) |
| 5d | **Bolheid** | Ronde volumes (Heat, Wash, Rotom) zijn zacht verlopen; kasten (Frost) zijn vlak, met donker op de zijkant. | Kasten, vlak, met donkere zijvlakken rechts. | **gelijk** (Frost-model) |
| 6a | **Kanteling / 3/4** | Alle vormen tonen een rechterzijvlak (donker) en staan licht gedraaid. | Zijvlakken rechts bij alle drie de kasten, top- en onderlijnen in perspectief. | **gelijk** |
| 6b | **Vulling** | Box 51–64 × 44–60. Pixels 1164–2173 (Rotom 605), dus 28–53% van het vak (Rotom 15%). | Box 60×53 (x2–61 y10–62), 1925 px, 47%. | **gelijk** |
| 6c | **Verticale plek** | Zwaartepunt (alle opake pixels) y 28–35, gemiddeld ±33. Onderkant y52–60. In de data zweven alle Rotoms: `enemyMonElevation` 6–10. | Zwaartepunt **y 43**, onderkant **y62**. Bovenin staat alleen de bliksem. | **wijkt af** (laag) |
| 7 | **Frame 2** | Bij alle 6 bewegen de plasma-ledematen (groter, omhoog of gespiegeld). Bij 3 van de 6 "doet" het apparaat iets: de grill van Heat kantelt open, de deur van Frost gaat open, de bladen van Fan worden een draaiwaas. Rotom, Wash en Mow verschuiven 1–9 px. De ogen blijven gelijk. 811–1920 px verschillen. | Heeft nog geen frame 2. | **mist** (later) |
| 8a | **Donkere apparaatdelen** | Neutraal donkergrijs: 40,40,40 en 72,72,80 (grill van Heat, bladen van Fan, wielen van Mow, trommelrand van Wash). | Navy 24,32,49 / 57,65,90 voor de speakerfronten (bron). | **wijkt af** → vraag voor Jordi |
| 8b | **Rugsprite, icoon** | Alle 6 hebben `back.png` (64×64) en `icon.png`. | Heeft ze nog niet. | **mist** (later) |

## Reparaties (op prioriteit)

Deze botsen niet met Jordi's keuzes: ze volgen de Rotom-stijl ("gebruik vooral de stijl van de rotom sprites") en/of de bron.

1. **Contourladder één stap donkerder (3d, 3e).**
   - Schaduwzijde: elke donkerst-oranje pixel (7) die rechts of onder tegen de gloed ligt → **zwart (8)**. Dat zijn 89 px:
     - rechterkant van de rechterspeaker: x55–59, y27–58 (x55 y27, x56 y28–29, x57 y30–35, x58 y36–50, x59 y51–58);
     - onderkant van de linkerspeaker: x4–10, y56;
     - onderkant van het hoofd: x11–35, y57;
     - x36–38, y58;
     - onderkant van de rechterspeaker: x39–50, y59.

     De 7 die daarbinnen ligt blijft staan als overgang.
   - Lichte zijde: elke donker-oranje pixel (6) die links of boven tegen de gloed ligt → **donkerst (7)**. Dat zijn 60 px:
     - linkerspeaker: links x4 y40–54 en boven x6–12 y38–39;
     - hoofd: links x16–17 y33–38 en boven x18–24 en x30–32 y32;
     - rechterspeaker boven: x36–54 y27–31 (de trap).

     Laat de spits zelf (x25 y30–31) staan.
2. **De spits vrijmaken en op Rotom-hoogte brengen (2a).**
   - Zet de hele bliksem (zone x17–31, y10–25) **3 px omhoog**, naar y7–22.
   - Laat de spits van y23 tot y32 lopen: 10 rijen, punt 1 px, basis 5 px (x24–29).
   - Lichtstreep 4 op x26 (links van het midden), donker 6 en 7 rechts, met de gloed 1→2 eromheen.
   - De bliksemstaart eindigt op de spitspunt. Zo staat het ook in de bron: de bliksem zweeft boven een vrije spits.
3. **Losse tanden (2b).** Maak van (24,43) zwart (8) of grijs, zodat er **twee** tanden overblijven: (23,43) en (25,43) wit. Zo doen Wash en Heat het, en de bron heeft er ook twee.
4. **Hooglicht als vlekjes in plaats van lijnen (5b).** Hooglicht (4) alleen in de hoek linksboven van elk volume; de rest van die lijnen → midden (5):
   - hoofd: houd x18–21 y33 en x17 y34–35, plus de wangvlek die er al staat op (20,36) en (21,37);
   - rechterspeaker: houd x36–42 y31–33 en x36 y34–35;
   - linkerspeaker: houd x6–9 y39–40 en x5 y41–42;
   - spits: houd de streep.

   Dat geeft ±35 px (±4–5%), zoals bij de game-vormen.
5. **Het palet op de exacte game-waarden (1a, 1d, 1b).** Volgorde en vormkleuren blijven, de pixels hoeven niet te veranderen.
   - index 4 → 248,168,128;
   - 5 → 232,112,40;
   - 6 → 192,72,24;
   - 7 → 120,56,32;
   - 15 → 248,248,248;
   - b → 184,184,184 (ook in de glimpjes van de conussen; dat kan);
   - 0 → 152,208,160.
6. **Naden zwart (3f).** De naadkolom van donkerst oranje (7) → zwart (8) op x15 y38–56 (achter de linkerspeaker) en x34 y32–58 (tussen hoofd en rechterspeaker). Doe dit pas na stap 1 en kijk dan op 1×: blijft het geheel leesbaar en wordt het niet te zwaar naast de navy fronten, dan houden; anders alleen de onderste helft.
7. **shiny.pal (1c).** Het recept van de game:
   - 1 → 232,160,112;
   - 2 → 240,200,160;
   - 3 → 240,224,200;
   - 4 → 248,128,168;
   - 5 → 224,56,112;
   - 6 → 184,24,80;
   - 7 → 120,0,40;
   - de rest gelijk.

   Let op: de equalizer gebruikt index 2 (en e). In de shiny worden die balkjes dus perzik; dat is consistent met de gloed. Wil je ze groen houden, gebruik dan alleen e.
8. **Verticale plek (6c), laag.** Bij voorkeur in de data oplossen: `enemyMonElevation` ±6, zoals de andere Rotoms, en `frontPicYOffset` passend. Schuif de sprite in het vak hooguit 2–3 px omhoog als er na stap 2 bovenin ruimte is (de bovenkant blijft ≥ y3, zoals bij Frost).

**Later (frame 2, rug, icoon).**
- Frame 2 volgens het game-patroon:
  - de bliksem groter of anders gekanteld (het plasma beweegt altijd);
  - het apparaat "doet iets": de conussen pompen (de ring 1 px groter, de glimp verschoven) en de equalizerbalkjes krijgen andere hoogtes;
  - het lichaam blijft staan of verschuift 1 px;
  - de ogen blijven gelijk.
- Daarna `back.png` en `icon.png`, zoals bij alle vormen.

## Vragen voor Jordi (gaan tegen een bewuste keuze in; geen opdracht)

- **Gloedkleur (3c, kleuren van de bron).** De gloed van de game-vormen is verzadigd; die van DJ is bleek mint en valt op een lichte achtergrond op 1× weg. Mag de gloed één stap voller, bijvoorbeeld 40,160,104 / 104,216,152? Hij blijft mint, maar staat steviger naast Mow en Rotom.
- **Speakerfronten (8a, kleuren van de bron).** De game gebruikt voor donkere apparaatdelen neutraal grijs (40,40,40 / 72,72,80); DJ gebruikt navy uit de bron. Navy houden of naar het grijs van de game?
- **Plasma-ledematen (4b, trouw aan de bron).** Elke game-Rotom heeft plasma buiten het apparaat, meestal twee ledematen opzij. DJ heeft alleen de bliksem met noot. Is dat genoeg (Mow frame 1 heeft er ook maar één), of willen we bijvoorbeeld kleine plasma-geluidsgolfjes opzij van de speakers? Die zouden ook mooi in frame 2 kunnen pulseren.
- **Laag zwaartepunt (6c, trouw aan bron en perspectief).** Door de brede, lage vorm zit DJ veel lager in het vak dan de rest (y43 tegen ±33). Dat volgt uit de bron; via `enemyMonElevation` zweeft hij in gevechten toch. Akkoord?
