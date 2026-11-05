# Nachtaap fase 3: kleurronde 1d (5 nov)

Basis: ronde 1c (onaangeroerd in `../ronde1c/`). Bestanden: `nachtaap_fase3.png`, `normal.pal` (gelijk aan 1c), `raster.txt`, `vel.png` (1d 4× licht/donker, model, 3× 1d naast 3× 1c, 1× licht/donker naast 1c, fase 2 en echte Gen 3-sprites).
Bron: `bron/delen.txt` (1b) + `bron/ronde1c.txt` + **`bron/ronde1d.txt`** (alleen de vier zones) → `bouw.py` → `check.py` (diff met 1c per zone, afwijking silhouet) → `vel.py`.

Jordi (letterlijk): "let nog op dat stuk tussen onderbeen en staart, stuk rare kont daar" · "en om het nazca patroon na te doen mag de staart niet aan een ander stuk staart vastzitten" · "en de bovenste bovenarm is echt een bol nu, in het model niet" · "ik zie nu sowieso dat in het model het bovenste been iets te hoog op het lichaam zit, die mag iets naar beneden denk ik om realistisch als been goed aan te sluiten op het lichaam" · "we gaan het model en silhouet niet aanpassen" · "ja, je mag buiten het silhouet gaan" · "dit moet allemaal niet extreem ingrijpend zijn zoals de hand wel was eerder".

## Diff met 1c (check.py): 126 px, 0 buiten de zones
| Zone (x0,y0,x1,y1) | px | budget | |
|---|---|---|---|
| A achterwerk (42,38,48,48) | 17 | ≤ 20 | ok |
| B spiraal (44,21,63,40) | 80 | ≤ 25 | **over**, zie hieronder |
| C bovenarm (8,20,21,30) | 20 | ≤ 15 | **over** (+5), zie hieronder |
| D been-aansluiting (20,33,38,41) | 9 | ≤ 20 | ok |

## Afwijking van silhouet ronde 1 (nieuw t.o.v. 1c)
- **A achterwerk:** 7 px erbij: (46,41), (45,42–45), (45,46), (46,46). De inham tussen bil en onderbeen is dicht.
- **B spiraal:** 27 px eraf; dat is de spleet van lucht. Het spiraalgat van 1c zit ook in deze telling: 34 in totaal.
- De 18 px "buiten zone" en de 2 in zone C zijn de bestaande 1c-afwijkingen: hand/gloed en kruin (8,27), (7–8,28). Die zijn niet veranderd.
- Open randen: 0.
- Losse pixels: 32, dezelfde als in 1c.
- `korrel.py`: 0 uitsteeksels, 0 tanden. Er zijn 26 "inkepingen", en dat is precies de spiraalspleet van 1 px: korrel.py telt elke 1-px opening als inkeping, en hier is die bewust.

## Per zone
- **A achterwerk:**
  - De bult onder de staartwortel met de inham eronder (contour 48→47→46→44 en dan een gat bij rij 46) is nu één bolle heuplijn: rij 38 x48, 39 x47, 40–41 x46, 42–45 x45. Daarna loopt de lijn over in de bovenkant van het onderbeen (rij 46, x45–46 gevuld).
  - Binnenkant: S/D-schaduw met K-omlijning rechts. De oude K-contour (44,40–45) is D/S geworden, (43,39) is D.
- **B spiraal (Nazca):**
  - De K-groef tussen de windingen is overal lucht geworden: x49 van rij 28 tot 37 (komt onderaan vrij), de diagonaal (49–51,26–28), boven (51–56,26), de diagonaal rechts (56–58,26–28), rechts x58 van rij 29 tot 33, en via (57–58,33) in het gat.
  - De diagonale stukken zijn 2 px breed gemaakt, zodat de windingen ook schuin niet tegen elkaar komen.
  - Beide randen van de spleet zijn omlijnd: D aan de belichte kant (links/boven), K aan de schaduwkant.
  - De buitenwinding rechts is V gemaakt (x60, rij 29–32), anders werd het daar een donkere streep.
  - De staart blijft overal 3 px dik (omlijning + kern). Alleen de binnenpunt bij het gat loopt uit; de 1-px punt (57,32) is weg.
- **C bovenarm (vuistarm):**
  - De lichte vlek in het midden (x10–12, rij 23–26), die de bol maakte, is V geworden.
  - Er loopt nu een lichtband van 2 px langs de bovenrand van de schouder naar de pols: (14–15,23), (15–16,24), (16–17,25), (16–17,26), (18,27). De onderkant (x9–11) blijft S. Zo leest het als cilinder.
  - De omtrek is niet veranderd.
- **D been-aansluiting:**
  - Een zachte S-sikkel (1 px) onder de dijwortel van het opgeheven been: van de oksel (22,35) via (23,36), (24,37), (25–26,38), (27,39) naar de bestaande S-plooi (28–31,39), en dan omhoog via (32,39) en (33–34,38) naar de staartonderkant.
  - Daardoor eindigt de dijwortel zichtbaar op rij 38–39 in plaats van rond rij 35. Het been sluit 2–3 px lager aan, uit de heup.
  - De rest van het been is niet veranderd.

## Waarom over budget
- **Spiraal (80 i.p.v. 25):** "niet aan een ander stuk staart vastzitten" betekent dat de groef van 1 px (22 px) lucht moet worden. Lucht naast een vachtkleur is een open rand, dus beide buren moeten omlijning worden: dat kost ±2 px per spleetpixel. Daarbij komen 7 px om de diagonale hoeken echt los te maken, en 4 px kern rechts. Met minder px raken de windingen elkaar of komen er open randen.
- **Bovenarm (20 i.p.v. 15):** 8 px om de bol-vlek weg te halen en 9 px voor een lichtband van 2 px over de hele lengte. Met een band van 1 px leest het als streep; die keuze heb ik niet gemaakt.

## Eerlijk: wat nog zwak is (1× en 3× naast 1c en het model)
- **Bovenarm:** de shading is nu een cilinder, maar de **omtrek** heeft bovenaan (13–15,22) nog de bobbel uit het silhouet. Op 1× kan de arm daardoor nog wat rond ogen; de kleurverandering helpt maar is subtiel. Om de bobbel weg te halen moet de omtrek mee: ±4 px meer (silhouet).
- **Been-aansluiting:** de sikkel is 1 px S op V. Op 3× zichtbaar, op 1× nauwelijks. De aansluiting oogt lager, maar het effect is klein.
- **Spiraal:** leest op 1× nu duidelijk als losse spiraallijn (Nazca). Op donkere achtergrond vallen de spleten weg in het donker, wat normaal is. De binnenpunt bij het gat is dun (2 px omlijning).
- **Achterwerk:** de heuplijn is vloeiend. De bil is iets voller dan in 1c (7 px buiten het silhouet).
- Op 1× is de sprite direct herkenbaar als 1c.

## Lessen
- Een spleet van lucht tussen twee delen kost ±3 px per spleetpixel (lucht + omlijning aan twee kanten). Diagonale stukken moeten 2 px breed, anders raken de delen elkaar schuin. Reken dat mee bij een pixelbudget.
- `korrel.py` telt een bewuste spleet van 1 px als inkepingen; noem dat in de notities.
- Een "bol" komt vaak door een lichte vlek midden op een ledemaat. Een lichtband langs de rand maakt er een cilinder van zonder de omtrek aan te passen.
