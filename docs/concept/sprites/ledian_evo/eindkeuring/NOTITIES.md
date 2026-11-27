# Ledian-evolutie: eindkeuring Dragonfly Cave (27 nov)

Basis: `../sprite_r2/rood_c.png` (Jordi: "ik vind c wel tof, verder helemaal goed"; perzik blijft). Opdracht Jordi: "schaduw, belijning, kleurtinten, dragonflycave". Alleen uitvoering; geen vorm, geen ontwerp.

Scripts (vanuit deze map): `analyse.py` (per buitenlijnpixel onderdeel + normaal + lichtscore, licht linksboven), `clusters.py` (tintvlekjes < 3 px), `ek.py` (vaste lijst wijzigingen + asserts → `ledian_evo_ek.png`, `_8x.png`), `vel.py` (→ `vel.png`, `vel_binnenlijn_test.png`).

**Bewijs:** silhouetdiff **0** (alpha, assert); **33 px** gewijzigd (alleen de lijst hieronder, assert); **13 kleuren + transparant** (index 0 transparant), 64×64. Rood c (831c10/c51810/ff3120) en perzik ffae83 ongewijzigd. Ogen, mond, stippen, ruitje, sprieten, gewrichten, vleugelband, vuisten: 0 px.
Zwart 364 → 362 px (18,8 % van de figuur; Scizor G3 18,1 %, Ledian G3 22,7 %).

## 1. Outline base aan de lichtkant
Gids r. 400–404: "we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide."
| Zone | Wijziging | Pixels |
|---|---|---|
| Hoofd, linkerpunt | zwart → selout 7 (rest van die rand was al selout) | (6,18) (7,20) (8,21) |
| Hoofd, rechterpunt boven | zwart tussen selout op de bovenrand → 7 | (32,14) |
| Hoofd, verre gezichtshelft (met het verre oog) | donkergrijze 393939 buitenlijn van een rood onderdeel → 7 | (6,22) (7,22) (8,22) (6,23) (6,24) (6,25) (7,26) |
| Hoofd, kaak linksonder | grijze 6a6a6a pixel op de rode lichtkantrand → 7 | (12,32) |
| Voorste been, bovenrand | zwart en selout om en om → doorlopend 7 (SPRITE_KERN: "nooit zwart en donkerlila om en om op één rand") | (51,51) (54,52) (55,53) |
| Voeten, linkerrand | zwart → donkerste geel a47b00 (nieuwe index 13 = Ledians eigen donkere geel, `normal_gba.pal` idx 9; Scizor doet hetzelfde met grijs op de klauwpunten) | (53,59) (53,60) (44,60) |

## 2. Outline shadow zwart aan de schaduwkant
Gids r. 89–91: "The 'outline shadows' are always black (or ever-so-slightly off-black) on Pokémon sprites".
| Zone | Wijziging | Pixels |
|---|---|---|
| Vleugelpunt, rechterrand | selout → zwart (bovenrand blijft selout, één overgang) | (62,21) (62,22) |
| Rechterarm naar de onderste vuist, rechterrand | selout → zwart (sluit aan op het zwart eronder) | (46,40) (44,42) (44,43) (44,44) |
| Kaak, onderrand | selout/grijs tussen zwart → zwart | (15,33) (13,33) |

## 3. Outline highlights
Gids r. 425–428: "Put some of the shadow/outline highlight color on the outlines in the very most highlighted parts ... place pixels of the outline highlight color on the inside of the outline". Ledian G3 doet dit met zijn schaduwtint op de kop linksboven.
| Zone | Wijziging | Pixels |
|---|---|---|
| Hoofd, bovenhelling (boven perzik) | selout → schaduwtint c51810 | (20,8) (19,9) (18,10) |
| Hoofd, linkerpunt boven | idem | (10,15) (11,15) |
| Vleugel, bovenrand | idem | (57,20) (58,20) |

## 4. Binnenlijnen: getest, teruggedraaid
Gids/KERN: binnenlijnen niet zwart. Getest op de twee zwarte binnenlijnen hoofd-over-arm (33,28)–(34,31) en arm-over-vleugel (44,29)–(41,32) → selout. Gevolg (`vel_binnenlijn_test.png`): aan beide kanten ligt schaduwrood c51810, en selout 831c10 is daar maar 18 helderheid donkerder; hoofd, arm en vleugel smelten tot één vlek. Gen 3-Ledian houdt op dezelfde plek (arm over romp, rijen 33–35) ook zwart. Teruggedraaid: zwart blijft. De overige zwarte binnenpixels zijn gewrichten, de oogranden, de kraag, de pootgewrichten en de zwarte kopnaad onder de spriet: kenmerken, niet aangeraakt.

## 5. Schaduw en kleurtinten (gemeten, niets veranderd)
- Helderheid (0,299R+0,587G+0,114B): perzik 193 · basis 109 · schaduw 75 · selout 57 · zwart 16 → stappen 84 / 34 / 18 / 41. Ledian G3: 207/133/94/70/16 → 74 / 39 / 24 / 54. Basis→schaduw zit in de ±30–40; schaduw→selout (18) is zwak, maar komt uit de gekozen rood c (−11°) en mag niet vervangen worden.
- Tintvlekjes < 3 px (`clusters.py`): alle rode 1–2 px-clusters zijn paneellijnen, glans langs de lijn of oog-/gewrichtsranden uit het model (bijv. de diagonale strepen in de linkerpunt (7..12,18..21)). Geen losse ruis gevonden die je weg kunt halen zonder detail weg te poetsen. 13 nieuwe kleine clusters = de bedoelde outline highlights + de gele lijnpixels.
- Banding/pillow: licht linksboven (perzik), schaduw rechtsonder (c51810) volgt de vorm; geen pillow. De perziklijnen langs de randen van het sterhoofd zijn de facetranden uit het model, geen banding van de maker.

## Bewust niet aangeraakt
- (33,25) grijze pixel buiten de zwarte rand rechts van het hoofd: volgens r1 een schoudergewricht uit het model ("losse grijze gewrichtspixel"); gewricht = kenmerk.
- (22,41) zwart tussen selout op de linkerrand bij de elleboog: rand van het donkergrijze gewricht, niet van het rood.
- Sprieten en geeltjes met donkergrijze lijn linksboven: donker onderdeel, lijn = eigen donkerste tint.
- Vuisten: lijn 6a6a6a/393939 linksboven, zwart rechtsonder; klopt al met Ledian G3.

## Ter info voor Jordi (ontwerp, niet veranderd)
- Schaduw→selout van rood c is maar 18 helderheid; daardoor zijn zwarte binnenlijnen nodig waar donkerrood op donkerrood valt.
- De sprite heeft veel donkergrijs (262 px: sprieten, stippen, gewrichten, kraag, vleugelband) en leest daardoor iets zwaarder dan Scizor/Ledian; dat komt uit het model.
