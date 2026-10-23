# Keuring alpaca ronde 15 (laatste check, 23 okt)

Onafhankelijke keuring van `anim_front.png` (64×128, 2 frames, 16 kleuren) inclusief de reparatie van de nabije voorpoot. Getoetst aan `SPRITING.md` (§0 en de alpaca-secties 14, 17, 21, 23), `FAKEMON_DESIGN.md`, de *Spriting Guide* (Outlining, Shading, Textures) en de referentiefoto `docs/concept/ontwerp/alpaca/referentie_alpaca.webp`.

Vellen (in `keuring/`):
- `vel1_vergelijking.png`: 1× op licht, donker en gras (frame 1 en 2) en 3× naast 14 echte Gen 3-sprites: Torchic, Mudkip, Treecko, Mareep, Flaaffy, Ponyta, Girafarig, Makuhita, Swablu, Altaria, Absol, Zangoose, Skitty en Smeargle (`graphics/pokemon/*/anim_front_gba.png`).
- `vel2_details_10x.png`: kop, hals/rug/staart en poten/vuisten op 10× met coördinatenraster, plus de poten van Ponyta, Girafarig en de vuisten van Makuhita ter vergelijking.
- `vel3_aandachtspunten.png`: frame 1 op 10× met de punten hieronder omkaderd (rood = nodig, blauw = polijsten).

Coördinaten: (x, y) binnen het frame, y = 0 bovenaan. Frame 2 is frame 1 met de kop (y ≤ 22) 1 px lager; verder pixel voor pixel gelijk (gemeten: 0 afwijkingen).

## Eindoordeel: **goed, met één kleine reparatie**
Op 1× leest hij meteen als alpaca (lange hals, spitse oren, kuif, wollig crème lijf) en als Pokémon, niet als schaap of lama-foto. De rode handschoenen zijn de blikvanger en maken hem herkenbaar Fighting. Palet, omlijning en licht zitten binnen de Gen 3-marges (metingen hieronder). Het oog met de schuine bovenrand kijkt vastberaden, en dat past bij een vechter. De vlechtknoopjes en de aguayo-band zijn op 1× rode en bonte puntjes. Ze lezen als accent en niet als ruis. Wat nog moet, is klein werk: **vier open randen** (één ervan is door de pootreparatie ontstaan) en **de achterpoten die aan elkaar vastzitten**. Dat laatste is hetzelfde probleem als Jordi bij de voorpoten aanwees. De rest is polijstwerk en mag ook blijven zoals het is.

## Metingen

| | Alpaca r15 | Gen 3 ter vergelijking |
|---|---|---|
| Oppervlak (frame 1) | 938 px | Torchic 782, Mudkip 852, Treecko 967; Mareep 893, Flaaffy 885, Skitty 934 |
| Kader | 34 × 51 | Torchic 33 × 47, Treecko 47 × 48, Flaaffy 35 × 44 |
| Kleuren | 15 + transparant | Mareep 15, Treecko 15, Girafarig 14 |
| Zwart-aandeel rand, totaal | 0,59 | Mareep 0,57, Makuhita 0,57, Girafarig 0,53, Smeargle 0,63 |
| idem lichtkant / schaduwkant | 0,30 / 0,92 | Flaaffy 0,31 / 0,87, Girafarig 0,29 / 0,88, Smeargle 0,43 / 0,92 |
| Vachtstappen (luma W → w → v → u → V → K) | 250 → 226 → 179 → 124 → 80 → 29 | les §21: ±40–50 per stap |

Hij is net de hoogste van de drie starters (+3 à 4 px door hals en oren) en qua oppervlak middenmoot. Dat is in orde.

## Regel voor regel

| Regel | Echte sprites | Alpaca r15 | Oordeel |
|---|---|---|---|
| §0.1 Lijf én blik 3/4 | Ponyta, Girafarig: lijf zijwaarts, diepte via voethoogte | Voeten op y 54 / 50 / 51 / 47 (nabij voor, ver voor, nabij achter, ver achter); kop 3/4 met snuit naar voren | ✔ |
| §0.2 Ledematen geteld en verbonden | Ponyta: verre poten donker en los van de nabije | 4 poten, 2 oren, 2 vlechtjes ✔; **verre achtervoet zit met een doorlopende zwarte lijn aan de nabije achterpoot vast** | ✗ (punt 2) |
| §0.3 Geen rechte lijnen in ronde omtrek | Mareep, Skitty | Snuit, kop en buik zijn rond ✔; rug 7 px recht (y 28) met een rechte hoek naar de nek; handschoen als afgerond blok | polijsten (3, 5) |
| §0.4 Ogen geïntegreerd | Ponyta, Absol: klein zwart oog met glans | 3×4 zwart, glans (27,15) binnen het zwart, reflectie B (28,17) rechtsonder; schuine bovenrand = vastberaden | ✔ |
| §0.5 Silhouet op 1× | foto: hals, oren, kuif | Leest als alpaca; de kuif en de hals dragen het | ✔ |
| §0.6 Formaat | zie metingen | 938 px | ✔ |
| §0.7 Pose niet stijf | Girafarig, Ponyta | Schuine voorpoten, geknikte achterpoot, gewichtsverschil ✔ | ✔ |
| Palet 3 tinten + omlijning, hue-shift | Altaria/Swablu (koel), Mareep (warm) | Crème → oudroze → mauve → pruim: één warm-naar-koel-lijn ✔; vuist 4 tinten ✔ | ✔ |
| Licht linksboven, schaduw op de evenaar | alle | Kop, hals, lijf en poten consequent ✔; **verre vuist even licht als de nabije** | polijsten (4) |
| Omlijning per kleurgroep, 1 px | Treecko, Flaaffy | Pruim V aan de lichtkant, K aan de schaduwkant, wijnrood S rond de vuisten ✔; geen klonten | ✔ |
| Anti-aliasing alleen binnen | alle | Geen buitenpuntjes; schoon op donker | ✔ |
| Gesloten omtrek | alle Gen 3 | **vulkleur (u/v) tegen transparant aan de onder- of schaduwkant** op 4 plekken | ✗ (punt 1) |
| Glans/wol mat | §21 | Geen witte glans op wol of vuisten ✔ | ✔ |
| Textuur | Guide: dithering mag, niet overdrijven | Schaakbordje r/s op de vuist (x 18–21, y 49–52) leest als breisel/plooi | ✔ (optie 5) |
| Twee vuisten naast elkaar | §23: 1 kolom lucht | Kolom x 23 vrij ✔; **verre vuist raakt de nabije achterpoot op (31,48)–(32,48)** | polijsten (4) |
| Evolutiehints | — | Vlechtknoopjes (16,12) en (35,13) en band (x 23–28, y 26–27) op 1× zichtbaar als kleurpuntjes, niet druk | ✔ |
| Frame 2 | Gen 3: zelfde schaduwlogica | Alleen een knikje met de kop; band en hals blijven staan ✔ | ✔ |

## Nodig

**1. Open randen (4 plekken, beide frames): NODIG, snel**
- *Wat:* hier grenzen schaduwkleuren direct aan transparant, aan de onder- of schaduwkant, waar zwart hoort. `bouw15.py` meldt ze niet, omdat v en u daar als randkleur gelden. Aan de lichtkant mag dat (v als omlijnings-hooglicht), aan de onderkant niet.
  - **(25,39) en (26,39)**, buik tussen de voorpoten. Deze zijn ontstaan door de pootreparatie: er kwam lucht onder de buik, maar geen onderrand.
  - **(19,22)**, onderkant van de kaak (frame 2: (19,23)). Daar zit u tussen K (x 15–18) en V (x 20–22).
  - **(42,36)**, onderkant van de kont. Rij 36 eindigt met K op x 43, rij 37 met K op x 41, dus de hoekpixel (42,37) ontbreekt.
  - **Staart, (43,29), (44,30) en (45,30)**: de onderkant is open, en op (43,30) zit een gaatje tussen staart en kont. Daardoor zweeft de staart.
- *Regel:* gesloten omtrek, aan de schaduwkant zwart (Outline Shading; SPRITING §8, §24).
- *Goed bij:* alle referenties. Geen enkele Gen 3-sprite heeft vulkleur tegen transparant aan de onderkant.
- *Oplossing:* (25,39) en (26,39) → K. (19,22) → K (frame 2: (19,23)). (42,37) → K (nieuwe pixel). (43,30) → K, en (44,30) en (45,30) → K. De staart krijgt zo een zwarte onderrand en zit vast aan de kont. Het silhouet verandert niet.

**2. Achterpoten zitten aan elkaar vast: NODIG (klein)**
- *Wat:* de verre achtervoet loopt met één zwarte lijn (y 47, x 36–41) door in de nabije achterpoot. Op (37,46) vult hij zelfs tegen de nabije poot aan, en op (37,43)–(38,43) raken de poten elkaar bij de hak. Tussen de poten blijven twee ingesloten gaatjes over (x 37–38, y 40–42 en (37,44)–(37,45)). Op 1× is dat één driehoek en geen twee poten. Het is precies het probleem dat Jordi bij de voorpoten aanwees ("zit vast aan een ander") en dat in deze ronde voor de voorpoten is opgelost.
- *Regel:* §0.2 (verbonden, maar elk deel apart leesbaar), §23 (1 kolom lucht tussen twee gelijke delen).
- *Goed bij:* **Ponyta** en **Girafarig** (`vel2`). De verre achterpoot is donker en staat los, met een eigen hoefje en lucht naast de nabije poot. Overlap bij de hak mag, een gedeelde voetlijn niet.
- *Oplossing:* geef de verre achtervoet een eigen afgerond hoefje op x 38–41: (37,46) → transparant, (37,47) → transparant, (38,46) → K, (38,47) → transparant (afgeronde hoek), K op (39,47)–(40,47), (41,46) blijft K. Dan staat er een kolom lucht op x 37 vanaf y 44. De aanraking bij de hak (37,43)/(38,43) mag blijven, want daar overlappen de poten echt.

## Polijsten (mag, hoeft niet)

**3. Nekrug in een rechte hoek op een vlakke rug**
- *Wat:* de achterkant van de hals staat 7 px verticaal (K op x 30, y 21–27) en gaat via één diagonale pixel (31,28) over in een rug van 7 px recht (V op x 32–38, y 28). Direct daaronder ligt een even rechte hooglichtstreep (W op x 32–37, y 29). Op 3× staat de hals als een paal op een kist.
- *Regel:* §14 ("nekrug als één holle curve van achterhoofd naar rug"), Guide-curven (geleidelijke overgang).
- *Goed bij:* de referentiefoto (holle overgang hals → schoft), Girafarig (hals loopt met een boog in de rug over).
- *Oplossing:* 3 à 4 px wol in de hoek: K naar (31,26) en (32,27), vul (30,26) en (30–31,27) met v/u, laat de rug-V op (33,28) beginnen en zet (32,28) op w. Breek de W-streep op y 29 in 2 + 3 px (bijv. (34,29) → w). Proporties en pose blijven gelijk.

**4. Verre vuist: even licht als de nabije en raakt de achterpoot**
- *Wat:* de verre vuist (x 24–31, y 45–50) heeft net zoveel R-hooglicht (25–26,45) en (25,46) als de nabije, terwijl zijn poot wel in schaduwtinten staat. Op (31,48)–(32,48) raakt hij de nabije achterpoot.
- *Regel:* SPRITING §12 en nachtaap-keuring punt 3: verre ledematen kleiner en donkerder. §23: lucht tussen delen.
- *Goed bij:* Makuhita (verre vuist in de schaduw van het lijf), Ponyta (verre poten donkerder).
- *Oplossing:* R → r op (25,45), (26,45) en (25,46). Zet de rechterhelft één stap donkerder (r → s op x 28–29, y 45–48). Maak (31,48) transparant en (30,48) K, of houd de vuist rechtsonder 1 px in.

**5. Nabije vuist als blok**
- *Wat:* de linkerkant (x 14, y 48–52) en de rechterkant (x 22, y 48–53) lopen 5 à 6 px recht, en de onderkant (y 54, x 16–21) 6 px recht. Elke hoek heeft maar één diagonale pixel. Een duim of plooi is alleen te zien als het schaakbord r/s.
- *Regel:* §0.3 en Guide-curven (ronde vorm zonder lange rechte stukken).
- *Goed bij:* Makuhita (vuisten als ronde bollen, hoeken 1-2-3).
- *Oplossing:* hoeken 1 stap extra afronden: (14,48) en (14,52) → transparant met S op (15,48) en (15,52), en (22,53) → transparant met K op (21,53). Optioneel: vervang het schaakbord door één schuine s-lijn als duimplooi (x 19–21, y 49–51).

**6. Aguayo-band begint naast de rand**
- *Wat:* op y 26 begint de band pas op x 23. Op x 22 staat nog een W-hooglicht tussen de band en de omlijning (x 21). Daardoor leest hij op 3× als een plakkaatje of hangertje op de keel, niet als band die om de hals loopt.
- *Regel:* markeringen volgen de vorm (Shading, Textures).
- *Oplossing:* (22,26) → M, of P als lichte magenta, zodat de band tot de omtrek doorloopt. Wil je het sterker, dan zakt de band aan de lichtkant 1 px (ellips om een cilinder). Jordi vond de huidige maat goed ("net leesbaar"), dus dit is een optie en geen eis.

## Ontwerpnotities voor Jordi
- **Handschoenen op de grond:** op 1× lezen ze deels als rode laarsjes. Pas op 2–3× maken de bolle vorm en de manchet er bokshandschoenen van. Dat is acceptabel, want in gevecht is de sprite 1× maar het oog vult aan. Wil je hem op 1× sterker Fighting maken, dan kun je bij fase 2/3 een handschoen in de dekking optillen (Hitmonchan-houding). Voor fase 1 zou ik de goedgekeurde pose niet meer aanraken.
- **Staart:** het staartje staat omhoog als een vlaggetje (x 41–46, y 25–30). Dat is levendig, maar eerder geit of hert dan alpaca. Een alpaca draagt een korte pluim laag tegen de kont (zie de foto). Geen fout, wel iets om bij de evoluties consequent te houden.
- **Eén zichtbaar oog:** sinds het verre oog wol is, staat de kop bijna in profiel. Dat is de gewone Gen 3-conventie voor viervoeters (Ponyta, Girafarig, Absol), dus prima.
- **Kleuren:** crème, rood, magenta, geel, turquoise en roze zijn zes kleurgroepen op een kleine sprite. Dat werkt nu, omdat de bonte kleuren in drie kleine clusters zitten (vuisten, band, knoopjes). Bij de evoluties de aguayo laten groeien en er niet nog meer kleurgroepen bij nemen.
- **Toon:** de schuine bovenrand van het oog (lichtere pixel (26,14) naast het zwart) geeft een vastberaden blik zonder boos te kijken. Dat is goed voor een vechtersstarter. Bij het polijsten niet "rechtzetten".
