# Regionale Starmie r7: keuring + eindkeuring Dragonfly Cave op r6_licht (verse keurder, 27 nov)

**Eindoordeel: PASS.**
- 29 pixels gewijzigd en 10 paletkleuren aangepast.
- Silhouet: alpha-diff 0 met r6_licht (assert in `bouw.py`).
- Niets getekend. Glazuur, zigzag, hagelslag, juweelfacetten en chips staan op hun plek uit het model.
- Jordi's afgestompte punten zijn ongemoeid gelaten.

Bestanden:
- `starmie_r7.png`: 64×64, P, transparency 0, 16 kleuren incl. transparant.
- `bouw.py`: r6_licht → r7. Per pixel staan de oude index (assert) en de reden.
- `vel.py` → `vel.png`:
  - bovenaan r7 | r6_licht | model r4 op schaal, op 8×; de wijzigingen zijn blauw omkaderd;
  - onderaan 2× en 1× op wit en donker: r7, r6_licht, model, Gen 3 Starmie, regionale Staryu, Skinguin, Dundragoon, Zapacha, Princadee.

Bouwen: `cd staryu_regional/starmie && python3 sprite_r7/bouw.py && python3 sprite_r7/vel.py`.

Meetmaat: D = de gemiddelde modelhelderheid van alleen de koekcellen onder een spritepixel; Dp is hetzelfde voor de glazuurcellen. Beide komen uit het natieve r4-raster (`sprite_r5/gereedschap/natief_r4.png`) en meten met `gemeen.overlap`.

## Stap 1: keuring (blind, vóór het lezen van de r5/r6-notities)

**Eis 1, accuraat op het model en op Jordi's afstomping: ja.**
- **Vorm:** pose, verhoudingen en de vijf achterpunten op hun modelplek. De tien punten zijn afgestompt zoals Jordi koos.
- **Glazuur:** de zigzaglijnen (Z/N in de bovenarm, haken links en rechts, S/6-vormen onderaan), de hagelslag en het achtkantige juweel met lichte facetten linksboven staan op hun modelplek.
- **Chips:** de chips op de achterpunten staan op hun modelplek.
- **Tonen:** de toon volgt het model. Mediaan D per koektint: 4 → 129, 5 → 166, 6 → 188. Mediaan Dp per glazuurtint: 8 → 120, 9 → 157, licht → 192.
- **Gele hagelslag:** in de sprite is die koek-licht in plaats van felgeel, omdat het palet vol is. Op 1× valt dat niet op.

**Eis 2, Gen 3:**
- **Volume (eerst getoetst): bijna.**
  - Koekrand: licht aan de binnenkant, donkerder naar de buitenlijn.
  - Glazuur: binnenschaduw langs rechts en onder, en een lichte strook in de linkerarm.
  - Tekorten:
    1. De bovenste voorpunt was helemaal licht (5), zonder donker vlak rechts. Bij de Gen 3 Starmie loopt de tip licht links en donker rechts door tot het eind.
    2. Rechtsonder sprong de rand van 5 meteen naar 3, zonder 4 ertussen.
    3. De achterpunt rechtsonder had het licht alleen op het tipeinde, aan de schaduwkant.
    4. De lichte binnenstrook van het glazuur in de bovenarm en bovenaan de linkerarm stond wel in het model, maar niet in de sprite.
- **Belijning: twee fouten.**
  - **Bovenarm rechts:** daar stonden twee zwarte pixels binnen het silhouet, (33,11) en (33,12), tussen de glazuurlijn en de koekrand. Bij (33,13) zat een gat in de glazuurlijn en (35,16) had koeklijn in plaats van glazuurlijn.
  - **Bovenrand van de rechterpunt (rij 21):** die liep 2,2,1,1,2,2,1,2,1, dus om en om zwart en selout.
  - De rest is schoon. Ook de zwarte lijnen waar de voorste ster over de achterpunten valt zijn goed: rechts, onder en linksonder, net als de `e`-lijnen van de Gen 3 Starmie.
- **Tinten:**
  - **Koek:** het deeg paste niet bij de goedgekeurde Staryu. De koeklijn was L 66 tegen 85, en het hele deeg was ±15 L donkerder en oranjer. Game Freak geeft Staryu en Starmie hetzelfde goud (`normal_gba.pal`).
  - **Chocolade:** (124,80,56) was L 87, gelijk aan de nieuwe koeklijn.
  - **Paars:** geen hue shift; alle tinten hadden hue 282–283°.

## Na het lezen van de notities (r5/r6)
- **Twijfel 1 van r6** ("dunne, rafelige bovenrand rij 21"): dat is mijn belijningsfout 2, nu opgelost.
- **De zwarte pixels bij (33,11)–(33,12)** komen al uit de kale reductie (`sprite_r5/kaal.png`). Daar staat de donkere glazuurrand van het model. r6 heeft ze niet opgeruimd omdat die ronde buiten de punten niets veranderde.
- Ik deel de keuzes van r5/r6 verder: snede, buitenlijn per kant, koekrand.

## Stap 2: eindkeuring en uitvoering

### Gidscitaten (`docs/lessen/bronnen/dragonflycave_spriting_guide.txt`)
- **r. 96:** "The 'outline shadows' are always black (or ever-so-slightly off-black)". Zwart alleen als outline shadow.
- **r. 421–422:** "we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide."
- **r. 452–455:** "Put some of the shadow/outline highlight color on the outlines in the very most highlighted parts … place pixels of the outline highlight color on the inside of the outline rather than the outside."
- **r. 106–107:** "the relative luminosity of the shades on the original sprite should always be maintained". De volgorde van de tinten is behouden; alleen de waarden zijn veranderd.
- **r. 117:** "The outlines must be reasonably dark". De nieuwe koeklijn is L 85, gelijk aan de goedgekeurde Staryu (de Gen 3 Staryu heeft L 90).
- **r. 144–145:** "change the hue … (or possibly something slightly in the blue direction from there for shadows)". Dat is de hue shift van het paars.

### (a) Schaduw en volume: 22 px
| zone | px | wijziging | meting |
|---|---|---|---|
| **a1** voorste bovenpunt + rechterrand bovenarm | 8: (31,6) (32,7) (32,8) (33,9) (34,10) (34,11) (35,12) (35,13) | 5 → 4 | D 128–157; (32,8) D 177 is meegenomen zodat het vlak doorloopt zonder gat |
| **a2** rechtsonderarm, rechterrand | 3: (44,47–49) | 5 → 4 | D 150–153 |
| **a3** achterpunt rechtsonder, bovenrand | 3: (48,35) (49,35) (50,36) | 4 → 5 | D 146–152, tegen 125–140 eronder |
| **a4** glazuurlicht uit het model | 8: bovenarm (29,10) (28,11) (28,12) (27,13); linkerarm (23,21) (21,22) (22,22); linksonderarm (17,46) | 9 → licht | Dp 178–199 |

Gevolgen per zone:
- **a1:** de tip is nu licht links en donker rechts tot het platte eind, zoals de Gen 3-tip. De rand is binnen 5 en buiten 4, net als de rechterarm.
- **a2:** de sikkel loopt nu 5-4-3. De kolom 4 loopt door van rij 44 tot 51.
- **a3:** het lichte vlak loopt nu langs de lichtkant tot in de tip.
- **a4:**
  - in de bovenarm komt een lichte binnenstrook langs de lichtkant;
  - de lichte kolom in de linksonderarm loopt 1 px verder door;
  - bovenaan de linkerarm komt een lichtvlekje van 3 px.

Geen banden, geen pillow shading: de schaduw blijft rechts en onder, het licht links en boven, alles uit D/Dp. Zigzag, hagelslag en juweel: 0 px veranderd.

### (b) Belijning: 7 px
- **b1, glazuurlijn bovenarm rechts (4 px).** De lijn loopt nu als één diagonaal van 1 px van (32,10) tot (35,17):
  - (33,11) zwart → koekrand 5;
  - (33,12) zwart → glazuurlijn;
  - (33,13) gat → glazuurlijn;
  - (35,16) koeklijn → glazuurlijn.
  - Er staat geen zwart meer binnen het silhouet, behalve de lijnen waar voor over achter valt.
- **b2, bovenrand rechterpunt (3 px).** (49,21), (50,21) en (53,21) zwart → outline base. De rand loopt nu 2×8 en daarna 1 zwarte pixel aan het tipeinde: één wissel.
- **Gecontroleerd:**
  - geen lichte kleur op de buitenrand;
  - buitenlijn 1 px;
  - de 39 zwarte pixels binnen de buitenrand zijn allemaal lijnen waar voor over achter valt, aan de schaduwkant (zoals de Gen 3 Starmie);
  - chips en naden in koeklijn, niet in zwart.

### (c) Tinten: 10 paletkleuren, 0 px
| idx | rol | r6 | r7 | L | hue |
|---|---|---|---|---|---|
| 2 | koeklijn | 116,58,24 | **146,74,34** | 85 | 21 |
| 3 | koek donker | 178,102,40 | **198,112,50** | 120 | 25 |
| 4 | koek midden | 214,136,62 | **228,160,72** | 153 | 34 |
| 5 | koek licht | 236,182,100 | **244,198,118** | 187 | 38 |
| 6 | glans/gele hagel | 250,218,128 | **252,228,150** | 210 | 45 |
| 15 | chocolade | 124,80,56 | **102,54,36** | 64 | 16 |
| 7 | glazuurlijn | 76,34,92 | **66,34,92** | 64 | 273 |
| 8 | glazuur schaduw | 132,70,156 | **125,70,156** | 117 | 278 |
| 9 | glazuur midden | 172,112,198 | = | 161 | 282 |
| 10 | glazuur licht | 214,168,232 | **223,168,232** | 208 | 292 |

- **Koek en chocolade:** gelijk aan de goedgekeurde regionale Staryu. De stappen zijn 35/33/34 (Taillow ±30–40), met hue shift 21 → 45°. Het glanslicht ligt 23 hoger; het is een glans- en hageltint (32 px), geen vierde vlaktint.
- **Paars:** schaduw naar blauw, licht naar roze, bij gelijke helderheid. De stappen (53/44/47) blijven zoals bij de Gen 3 Starmie (41/49/42).

## Ter info voor Jordi (geen wijziging gedaan)
- **Achterpunt rechtsboven:** daar lopen twee donkere lijnen schuin over de koek, de koeklijn (rij 13–19). Ze komen uit de kale reductie: de schaduw die de voorste ster op de achterpunt werpt. Leest dat voor jou als een barst, zeg het dan.
- **Gele hagelslag:** die is lichtgeel (de glanstint) omdat het palet vol is. Felgeel kan alleen als er een andere tint uit moet.
