# Vuurduivel fase 1, r7: pijlopties voor de staartpunt

Jordi (letterlijk): "de staart is meer een vlam dan echt een pijl he". Eerder koos hij "pijlstaart met vuurkleur".

- **Vel:** `pijl_opties.png`: per variant de staart op 8×, en de hele sprite op 1× (licht en donker) en 2×.
- **Losse sprites:** `pijl_A.png` t/m `pijl_D.png`.
- **Script:** `pijl.py`.
- **Basis:** `sprite_r6/vuurduivel_r6.png`. Alleen het gebied van de punt (x40–52, y33–45) is opnieuw gezet. De stam sluit aan via (46,44–45).
- **Scriptcontrole:** buiten dat gebied is de diff 0 (silhouet en ogen ongewijzigd). Elke variant heeft 16 kleuren, het r6-palet zonder wijzigingen.

| | Vorm | Kleur |
|---|---|---|
| A | klassieke duivelspijl: driehoek met rechte randen (2:1-trap), scherpe punt (46,36), twee scherpe weerhaken onderaan, inkeping met de stam in het midden | vlakken: oranje links (licht), rood midden, donkerrood rechts; omlijning donkerrood aan de lichtkant, zwart aan de schaduwkant; geen geel |
| B | als A, smaller en langer (speerpunt, punt (46,34), max. 7 breed) | als A |
| C | schoppenpunt: strakke symmetrische randen, scherpe hoeken, twee lobben met de stam in de inkeping | als A |
| D | vorm van A | egaal rood met donkerrode schaduw rechts en één oranje lichtrand links (het minst vlamachtig) |

## vuurduivel_r7_basis.png: r6 + keuring_r6 MOET 1 en 2
- **Script:** `basis.py`. Pixels en redenen staan in `basis_wijzigingen.txt` (72 px).
- **Controle:** alpha-diff 0 t.o.v. r6, ogen-diff 0, lijn-diff 0, 16 kleuren.
- **MOET 1 (palet):**
  - Hoornmidden (190,45,46) is samengevoegd met haarrood r (162,41,41).
  - Index 14 is nu roze (212,94,90), voor de tong (22–25,38) en (22–24,39) en voor het hoornlicht (15,23), (15,24), (16,25), (25,23), (25,24), (26,22).
  - Vlam-middentint (226,88,62) staat alleen nog in het vuur.
- **MOET 2 (haar):**
  - Werkwijze in het haar (x10–41, y12–30):
    1. Middentint eerst terug naar O.
    2. Losse r-stipjes in oranje worden O.
    3. Middentint opnieuw alleen op een O-pixel met rood rechts of onder én oranje links of boven, dus als 1 px rand langs een tong, niet op tongtoppen.
    4. Een middentintpixel zonder middentint-buur (ook diagonaal) wordt weer O.
  - Rechts van de kop: één tong met O-kern (35,24–25), middentintrand (36,24–25), (35,26–27). Kolom 37 en (32–34,24–25) zijn r, dus geen om-en-om meer.
  - Er blijven 4 enkele middentintpixels over die alleen diagonaal aan een rand vastzitten.
- **Pijlopties:** opnieuw gemaakt op deze basis. Het "rood midden" is nu haarrood r, omdat het hoornrood is samengevoegd.
