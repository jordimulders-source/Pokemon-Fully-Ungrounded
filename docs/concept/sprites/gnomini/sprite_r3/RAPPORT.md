# Gnomini – sprite r3 (22 nov)

Basis: `r2.png` (= `../sprite_r2/gnomini.png`). Script: `r3.py` (bewijst de diffs), vel: `vel.py`.

Jordi: "ja en misschien dat we een soort streep ertussen moeten doen, doe dat als A/B test" · "en zijn linkerhand is niet rond".

- **A** (`gnomini_A.png`): grens roze/blauw als ring om de bol. Eerste blauwe rij b(x) = 44 + 3,4·(1−u²), u = (x−31,5)/11. Zijkanten op rij 44, midden zakt door naar 47. Gemiddelde hoogte 46,2 (r2: 46,0). Elke lijfpixel houdt zijn toonklasse uit r2 en krijgt de familie van de nieuwe grens. De roze sikkel is rechts 3 px breed (rijen 41–46, ook waar eerst blauw lag). Het roze hooglicht blijft zoals in r2. Het blauwe hooglicht ligt linksboven op het blauwe vlak (rijen 48–50, x22–27).
- **B** (`gnomini_B.png`): A + 1 px streep in donkerblauw (56,109,142), op de bovenste blauwe rij langs de grens. De gemiddelde hoogte blijft daardoor gelijk. De streep in p-roze (172,72,102) staat als `gnomini_B_proze.png` bijgeleverd. Die leest als roze schaduw en niet als streep, dus donkerblauw gekozen.
- **Armpje links** (A en B): rond balletje op dezelfde plek, x15–20 en y40–46, zonder bultje. De opbouw volgt het rechterarmpje: selout linksboven, hooglicht D linksboven, schaduw B onder, zwart onderaan. De lijn tegen het lijf is p.

## Pixeldiff t.o.v. r2 (`r3.py`)
| | lijfvlak | arm L | arm R | rest (muts, neus, voetjes, lijnen) | silhouet buiten arm L |
|---|---|---|---|---|---|
| A | 37 | 12 | 0 | 0 | 0 |
| B | 53 | 12 | 0 | 0 | 0 |

Het silhouet van arm L verandert binnen de zone: het bultje is weg en de bovenkant is rond. Controle: 14 kleuren, geen lichte kleur op de buitenrand, geen losse zwarte pixels.

Bestanden: `AB_8x.png` (A | B, 8×), `vel.png` (A | B | r2 op 8× en 1× op licht en donker).
