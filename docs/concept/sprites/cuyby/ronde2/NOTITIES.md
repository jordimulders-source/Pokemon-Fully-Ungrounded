# Cuyby fase 1, ronde 2 (pixelronde volgens de nieuwe werkwijze)

## Modeltekening: concept C2 (verfijning van C)
Jordi koos **C, Langhaarbol**, met de opmerking "zorg wel dat het echt Pokémon-stijl wordt". C zat het dichtst bij een echte cavia: een haarbal met een realistisch snuitje, kleine stipogen en lokken als franje. Daarom eerst een verfijnde tekening gemaakt: `docs/concept/ontwerp/cuyby/concept_C2.png` (script `docs/concept/ontwerp/scripts/cuyby_c2.py`). Het idee is hetzelfde gebleven, alleen gestileerd:
- een **zuivere bol** (Jigglypuff) met een middenscheiding. Onderaan zit een **zoom van brede lokken met punten**, in plaats van losse franjes rondom (vgl. Swablu's wolk en Wooloo's wol). Het silhouet is een bol met een gekartelde rok;
- **grote glimmende ogen laag in de bol** (Skitty/Jigglypuff) met een grote glans en een kleine tweede glans; een roze neusje en een klein 人-mondje. Geen blosjes;
- de **driekleur als drie strakke vlakken**: een zwart vlak over het linkeroor tot om het linkeroog, een oranje rug en rechterkant, de rest wit. De scheiding loopt als een kruinlijn over het midden;
- **hangoortjes** met een roze binnenkant, in de kleur van hun vlak.

Let op: C2 is een verfijning die ik zelf heb gemaakt, geen nieuwe keuze van Jordi. Wil hij terug naar C, dan staat C ongewijzigd.

## Werkwijze sprite
- **Skelet:** Jigglypuff (ronde bol, ±30 px, stairstep-contour, gekleurde omlijning) en Skitty (grote ogen met glans). Het oppervlak is 789 px, dat past bij een vroege Normal (doel ±600–850; Jigglypuff 747, Whismur 884).
- **Palet:** de rampopbouw van Jigglypuff (vier stappen, met een gekleurde omlijning in de donkerste stap) is gedraaid naar oranje. Daarnaast een warme crème-ramp (de keuring vroeg geen grijs) en twee tinten voor het zwarte vlak. Elk onderdeel heeft eigen indexen: crème (3 tinten + lijnbruin), oranje (4), zwartvlak (2), roze (2), oog + bruine weerglans, wit en omlijning. Samen 16 kleuren, index 0 transparant.
- **Pixels met de hand:** de hele sprite staat rij voor rij als tekst in `bron/cuyby_grid.py` (bol, zoom, oren). Daarbij komen twee met de hand gekozen puntenlijsten voor de gekleurde omlijning: bruin langs het wit aan de lichtkant, donkeroranje langs het oranje. Er is geen automatische schaduw.
- **Frame 2:** een popcornsprongetje. De hele cavia gaat 1 px omhoog en het mondje staat open (fluiten/wheeken).

## Metingen (frame 1)
| | oppervlak | b×h | donkere buitenrand | detail | losse pixels / opp. | verzadiging |
|---|---|---|---|---|---|---|
| Cuyby r2 | 789 | 31×32 | 0,56 | 1,55 | 0,10 | 0,40 |
| Jigglypuff | 747 | 32×33 | 0,35 | 1,71 | 0,13 | 0,43 |
| Whismur | 884 | 38×37 | 0,53 | 1,42 | 0,11 | 0,48 |
| Skitty | 934 | 41×40 | 0,38 | 1,83 | 0,21 | 0,51 |

## Blinde test
`blindtest.png`: de sprite tussen twaalf echte Gen 3-sprites (Jigglypuff, Igglybuff, Skitty, Whismur, Swablu, Mareep, Zigzagoon, Sentret, Teddiursa, Azurill, Snubbull, Clefairy). De kandidaat staat op **plek 10**.

**Nog niet onafhankelijk uitgevoerd.** In deze subagent-sessie was geen Agent-tool om een frisse agent zonder context te starten. De hoofdsessie moet de test nog draaien.

Eigen inschatting (niet blind): Cuyby valt minder op dan de nachtaap. Het formaat, de bolvorm, de gekleurde omlijning en de ogen passen in de rij. Wat hem kan verraden:
1. De zoom van lokken leest als een spookrokje of kwal en is minder 'haar' dan bedoeld.
2. De crème onderhelft is vlakker dan bij Gen 3, met maar een paar korte streng-lijntjes.
3. Het zwarte vlak is erg donker en egaal. Het linkeroog valt erin weg, alleen de glans en een grijze rand blijven over.

## Volgende stap
Laat Jordi eerst kiezen of C2 de modeltekening wordt. Daarna, als de blinde test hem aanwijst, een schaduw- en textuurronde: strengen in de zoom, een lichtere rand om het linkeroog en meer clusters in de crème. Het silhouet blijft dan staan.

Bestanden: `anim_front.png` (64×128, 2 frames), `normal.pal`, `compare.png`, `blindtest.png`, `bron/` (`cuyby_grid.py` tekent, `cuyby.py` bevat het palet, `lib.py`). De vellen maakt `docs/concept/sprites/nachtaap/ronde6/bron/vellen.py`.
