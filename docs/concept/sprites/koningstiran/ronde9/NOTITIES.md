# Sapa Inca – ronde 9 (kroonpatroon + puntige stafkop)

Basis: `ronde8/sapa_inca.png` (`sapa_inca.txt` = raster van ronde 8). De varianten zijn gebouwd met `kroon9.py`, een constructie op de 9 radiale veren (middelpunt kopbasis (28,5; 21), veren van 20°). Elke variant is een `.txt` (ronde 8 + pixelregels onderaan) en een `.png`:
- `v1_een_boog_zwarte_rand` – één gouden boog + zwarte randvlekken
- `v2_twee_bogen_gouden_rand` – twee gouden bogen + gouden randvlekken
- `v3_een_boog_gouden_rand` – eigen keus: één gouden boog + gouden randvlekken (3 px per veerpunt); `sapa_inca.png` = deze variant

Verder: `bouw.py`, `controle9.py` (diff per zone per variant), `vel.py` → `vel.png` (kroon + kop op 8× van ronde 8 en de 3 varianten, 1× licht/donker, stafkop op 10× naast ronde 7 (A) en ronde 8), `kijk.py`.

Jordi: "kroonvariant vind ik geen enkele mooi, b komt in de buurt, maar is net te zwakjes, te willekeurig en die oranje stippen aan de buitenkant zijn ook maar half doorgevoerd". Over de stafkop: "ja dat is nu een bol, ik dacht dat je meer voor een puntig uiteinde ging, ga dat maar doen, een puntig einde".

## Opbouw van het patroon (alle varianten)
- **Opruimen:** alle oude zwarte stippen en vlekken in het oranje zijn weg (opgevuld met de veertint eromheen). Zwarte veerscheidingen in het oranje zijn veerranden geworden. De schaduwkant (veren rechts, < 80°) is rustig opnieuw ingedeeld: elke veer R buiten en r binnen (r < 11), scheidingen in r. Daarmee is het R/r-schaakbord ("diagonale streepjes") weg. Zwarte pixels in de kroon: 62 → 40 (v1) / 22 (v2, v3); wat overblijft is omlijning.
- **Boog 1:** in elke veer precies één gouden vlek van 2×2 op dezelfde afstand (r = 14,6) van de kop, dus 9 vlekken op een nette boog met gelijke tussenruimte. Aan de lichtkant (veren links en midden) y/g/g/a, aan de schaduwkant g/g/a/a.
- **Boog 2 (alleen v2):** per veer een kleine vlek (licht + schaduw eronder) op r = 10,2.
- **Rand:** per veerpunt dezelfde vlek in de lavendel vulling, op de pixels die het dichtst bij het veermidden liggen. Dat is 2 px in v1/v2 en 3 px in v3, rondom alle 9 veerpunten, ook rechts. De buitenste omlijning blijft. Oude zwarte streepjes in de rand tussen de veerpunten zijn lavendel geworden, behalve waar de rand de opgeheven vleugel raakt (scheiding blijft).

## Puntige stafkop (alle varianten gelijk)
- De ronde schijf van ronde 8 is weg. Nu is het een gouden ruit, 5 px breed (rij 23–25, op rij 24 inclusief de zwarte rand 7 px), met daarboven een spitse punt van 3 rijen (rij 20–22, 1 → 1 → 3 px). De roestbruine vaan eronder (rij 26–27) loopt over in de schacht. Symmetrisch rond de schacht x15.
- Zwarte omlijning alleen waar hij vóór de kroonrand en het kwastje ligt. Het kroonkwastje is vanaf rij 24 weer zichtbaar (de bol bedekte het tot rij 27); waar de bol lag, zijn de kroon- en kwastpixels teruggezet uit ronde 2.

## Diff t.o.v. ronde 8 (`controle9.py`)
| | kroon | stafkop | gezicht | rest (lijf, staf eronder, vleugels, poten) | silhouet |
|---|---|---|---|---|---|
| v1 | 156 px | 33 px | **0** | **0** | −2 |
| v2 | 167 px | 35 px | **0** | **0** | −2 |
| v3 | 165 px | 33 px | **0** | **0** | −2 |
- 0 open randen, 15 kleuren + transparant.

## Zelf gekeken (8× en 1×, naast ronde 8)
- Alle drie lezen als één doorlopend motief: een boog gouden vlekken met gelijke tussenruimte en een rand met vlekken op elke veerpunt. Nergens willekeurige stippen. De gouden vlekken zijn ook aan de schaduwkant zichtbaar.
- v3 (en v2) heeft de rand het duidelijkst rondom doorgevoerd. In v1 vallen de zwarte randvlekken rechts weg tegen de donkere lavendel en de zwarte omlijning.

## Eerlijk: wat nog niet klopt
- **v1:** rechts in de schaduwkant zijn de zwarte randvlekken nauwelijks te zien (zwart op donker lavendel naast zwarte omlijning), dus daar oogt de rand weer "half".
- **v2:** de tweede, kleine boog (2 px per veer) is op 1× een rij puntjes en maakt het geheel drukker.
- **Schaduwkant:** de vereenvoudiging (R buiten / r binnen) maakt rechts een donkere wig vlak bij de kop, die strakker oogt dan de lichte kant met zijn scheidingen.
- **Stafkop:** de spitse punt (rij 19–22) staat vóór de kroonrand; de zwarte omlijning eromheen maakt een donker inkepinkje in de onderkant van de kroon. De ruit is klein (5 px), dus op 1× is het een gouden speerpuntje en geen grote zon.

## Lessen
- Een patroon op een waaier construeer je per veer (vaste hoek en afstand) en niet door bestaande stippen om te kleuren; zo komen de bogen vanzelf netjes uit.
- Bij een script dat pixelregels schrijft: transparant expliciet als '_' wegschrijven, want '.' betekent in het rasterformaat "laat staan" (de oude bol bleef eerst staan).
