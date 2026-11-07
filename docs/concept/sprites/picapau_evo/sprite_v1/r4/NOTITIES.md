# Picapau-evolutie: sprite r4 (reparaties 1–5 op r3)

r3 (`../r3/`) blijft staan. Jordi's woorden: zie `../r3/NOTITIES.md` (onveranderd). De opdracht was: alleen mijn eigen zwakke punten 1–5 van r3 repareren. De omtrek is bevroren, behalve bij de poten en de punten van de verre vleugel.

## Werkwijze
- Zelfde handwerk als r3: `tekening.txt` (kopie van r3) is met de hand bijgewerkt, segment voor segment.
  - `zet.py` zet die segmenten op hun plek in `raster.txt`.
  - `bouw.py` maakt `picapau_evo.png` en `normal.pal`. Het palet is gelijk aan r3.
- `controle.py` → `controle_uitvoer.txt`.
- `diff.py` → `diff_uitvoer.txt`: de omtrek tegen r3.
- `vel.py` → `vel.png`: 1× en 8× naast r3, r2, Picapau, Taillow, Staraptor, Raichu Gen 1 en de r5-render.
- Draaien: `python3.11 zet.py && python3.11 bouw.py && python3.11 diff.py && python3.11 controle.py && python3.11 vel.py`

## Bevroren omtrek (`diff_uitvoer.txt`)
- **Alpha-diff buiten de zones: 0 px.**
- Binnen de zones:
  - POTEN (rij 46–55, x 14–38): 46 px.
  - VERRE_PUNTEN (rij 2–14, x 35–45): 8 px.
- Kleurwijzigingen met dezelfde omtrek: 90 px buiten de zones (punten 2–5), 35 px in POTEN, 25 px in VERRE_PUNTEN.

## Per punt
1. **Poten.**
   - Nabije poot:
     - Het loopbeen is nu 3 px dik (g g G), met zwarte omlijning aan beide kanten, en loopt van onder de dij door tot de voet.
     - De voet heeft een lichte bovenkant (g), een donkere onderkant (G), een zwarte teenscheiding tussen de voorste tenen en de achterteen, en zwarte klauwen aan beide uiteinden.
   - Verre poot:
     - Hoger en verder naar achteren, alleen in schaduwtint G.
     - Het loopbeen is 2 px; de voet is een rij G met een zwarte onderrand en twee klauwen.
2. **Vleugel.**
   - De voorrand is nu licht (2, de lichtste kastanje) als rand van 1 px. Linksboven bij de pols zijn de kleine dekveren 2 px breed licht. Daardoor lezen voorrand, kleine dekveren, grote dekveren en pennen als lagen.
   - Vier handpennen kregen een lichte bovenrand (3) vlak onder de veerlijn, zodat ze als ronde veren afsluiten.
   - De punten van de verre vleugel bovenop zijn breder (4 px) en rond afgesloten, met een lichte streep (3) per veer. Het zijn geen spitse "vingers" meer.
3. **Flank rechtsonder.**
   - De dij is nu een eigen vorm: licht 2 linksboven, 3 rechtsonder.
   - Een binnenlijn in de donkere tint (4) loopt als boog over de achterkant van de dij, op de plek waar die over de onderbuik valt.
   - De onderbuik achter de dij is 3, met een sikkel 4 langs de onder- en achterrand in plaats van één vlak.
   - Een donkere lijn (3) scheidt de dij van de crème buik.
4. **Kop.** Het licht (1) is nu een rand van 1–3 px langs de linkerbovenkant (schedel en voorhoofd). Het binnenvlak is 2 en de sikkel 3 rechts en onder blijft, zodat de kop rond leest.
5. **Donkere strook tussen kop en nabije vleugel** (verre vleugel). Twee veerranden in 3: de bovenrand bij de pols en een tweede rij lager. De lichte stip (b) blijft. Het is nu een vleugel en geen vlak meer.

## Controle (`controle_uitvoer.txt`)
- Geen lichte kleur op de buitenrand.
- Geen losse pixels.
- Geen tintclusters kleiner dan 3 px.
- 15 kleuren + transparant, 1972 px.
- Alleen-diagonaal verbonden zijn 5 px: de 1px-lijnen van de oorspiraal en het haakje (bewust, zoals Gen 1).

## Eerlijke zwakke punten
1. **Voeten nog niet op het niveau van Staraptor.**
   - De nabije voet is dikker en duidelijker, maar de tenen lezen op 1× als één grijze balk met klauwen, niet als losse tenen.
   - De verre voet is een smalle grijze streep.
   - Staraptor heeft 3–4 px brede, apart omlijnde tenen in een opvallende kleur. Dat lukt alleen als de voet meer ruimte krijgt: de zone moet groter, of de bliksem moet iets opzij.
2. **Vleugel op 1×.** De lichte voorrand en de stippen lezen, maar de waaier blijft een groot donker vlak. De veerlijnen zie je vooral op 8×.
3. **Licht op de kop.** De lichte rand is subtiel (1 px). De kop leest ronder dan in r3, maar het verschil is op 1× klein.
4. **Verre vleugel tussen kop en nabije vleugel.** De twee veerranden helpen, maar de strook blijft smal en donker.

Er is niets gecommit, en er is niets uit git-mappen weggehaald.
