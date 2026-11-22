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
