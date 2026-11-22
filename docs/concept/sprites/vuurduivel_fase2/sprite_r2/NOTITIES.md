# Vuurduivel fase 2, sprite r2

Reparaties naar de MOET-punten van `../keuring_r1/KEURING.md`. Het oog is gelijk aan r1 (wordt apart gekozen, zie `../sprite_r1/ogen/`).
**Sprite:** `vuurduivel2_r2.png` (64×64, 4-bit, 13 kleuren + transparant op index 0), figuur x4–59, y5–62 zoals r1. `vuurduivel2_r2_8x.png`.
**Vel:** `vel.png` = r2 8× | r1 8× | model; daaronder handvlam en staartvlam op 12× (model | r1 | r2); 1× op 4 achtergronden (r2 links, r1 rechts).
**Diff (`diff.txt`):** 58 indexen anders dan r1: handvlam 30, staartvlam 25, manen 3, **buiten de zones 0**.

## 1. Zwart lijf leesbaar (alleen het palet)
De twee lijftinten gaan omhoog en blijven neutraal zoals het model (geen paarse of blauwe zweem): 22,22,22 → **46,44,44** en 40,40,40 → **76,72,72**. De omlijning blijft 3,1,1. De stappen zijn ±43 en ±29 helderheid. De plaats van de tinten is exact r1 (= model), zonder pixelwijziging.
Let op: deze twee indexen zijn ook de tinten van het gezichtsmasker, de staart en de donkere vingerlijnen. Die worden dus mee lichter, net als in het model, waar dat allemaal hetzelfde zwart is.

## 2. en 3. Hand- en staartvlam in modelbanden (`vlam.py`)
- **Silhouet:** dat van r1.
- **Band per vlampixel:** de gemiddelde vuurhitte van een venster van 4×4 natieve modelpixels rond de cel (geel 4, oranje 3, oranjerood 2, rood 1, donkerrood 0), afgerond naar een band. Zo komen de gele kern, de oranje ring en de rode rand van het model terug zonder de vlekkerigheid van losse pixels.
- **Vlekjes < 3 px:** gaan op in de meest voorkomende buurband.
- **Buitenrand:** rood, en donkerrood waar de achtergrond rechts ligt (schaduwkant). Dat is de rand die het model toont: donkerrood rechts, rood links.
- **Vonkjes:** (9,17), (9,18) en (10,18) blijven.
- Wat overblijft aan "vlekjes" in de controle zijn randpixels die diagonaal aan elkaar hangen (traplijn van de rand), geen losse vlekken.
- **Verworpen proef** (`--sil2`, `proef_sil2.png`): vlamsilhouet met de regel ≥2 van 4, zoals de rest van de sprite. De zijvonken komen dan los, maar de tongen vallen uiteen in losse pixels. Daarom blijft het silhouet van r1.

## MAG
- **Manen rechts:** (46,29), (46,31) en (47,31) van oranje naar oranjerood. Dat zijn de buitenste vuurpixels die aan de achtergrond grenzen; een tint donkerder als selout, met de rode haarpunten van het model ernaast. (44,29), (45,29) en (45,31) grenzen niet aan de achtergrond en blijven.
- **Kleine hoornhaak:** niet gedaan. In het model valt de linkerhelft van de haak (kolom x15) half in de achtergrond. 2 px dik kan alleen door het silhouet naar x14 uit te breiden, en dat geeft het model niet.

## Zelf gezien
- De handvlam blijft blokkig van vorm, door het silhouet van r1 (vuur telt al bij 1 van 4). Het model heeft een slankere tong met losse zijvonken. Dit is de afweging met de verworpen proef.
- Door het lichtere zwart lezen de vachtplooien in de romp nu. Het gezichtsmasker is ook iets grijzer; op 1× leest het nog als zwart masker.
