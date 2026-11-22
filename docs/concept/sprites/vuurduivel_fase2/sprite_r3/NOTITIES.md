# Vuurduivel fase 2, sprite r3 (vanaf r2)

**Sprite:** `vuurduivel2_r3.png` (64×64, 4-bit, 14 kleuren + transparant op index 0; oogrood 200,36,40 op index 14), figuur x4–59, y5–62. `vuurduivel2_r3_8x.png`.
**Vel:** `vel.png` = r3 8× | r2 8× | model. Daaronder op 12× de handvlam (model | r2 | r3) en de staartvlam (model | r2 | r3). Daarna 1× op 4 achtergronden (r3 links, r2 rechts).
**Diff (`diff.txt`):** 54 indexen anders dan r2: oog 15, handvlam 23, staartvlam 16, **buiten de zones 0**.

## 1. Oog: Sharpedo A (Jordi's keuze)
De 15 pixels in de zone x25–31, y17–21 zijn exact gelijk aan `../sprite_r1/ogen/oog_sharpedo_A.png`. Dat is het Sharpedo-oog (bron x24–28, y39–43, verschoven +2,−22), omgekleurd: lijn zwart, oogwit oogrood, iris zwart. Eerst gecontroleerd dat r2 in die zone gelijk is aan r1. Na deze stap was de diff met r2 buiten de oogzone 0.

## 2. Handvlam opnieuw uit het model (`vlam3.py`, zone x5–13, y16–28)
- **Silhouet:** figuur als ≥2 van de 4 natieve modelpixels figuur zijn en er minstens één vuur is. Dat is dezelfde regel als in de rest van de sprite; r1/r2 telden vuur al vanaf 1 pixel, waardoor de vlam opzwol en de zijvonk eraan vastplakte.
- **Losse enkele pixels vallen weg.** Dat geldt alleen voor de rechter zijvonk (12,22): 1 px, en in het model ook maar een sliertje.
- **Resultaat:** een slanke tong met de punt op y20 en de linker zijvonk los op (6–7,21), in één oranje band. De bovenste vonkjes (9,17), (9,18) en (10,18) zijn ongewijzigd uit r2.
- **Banden:** zoals r2 (vuurhitte van een 4×4-venster in het model), vlekjes kleiner dan 3 px opgegaan. De rand is rood, en donkerrood waar de achtergrond rechts ligt.
- Alleen vuur- en achtergrondpixels in de zone zijn veranderd; hand en omlijning niet.

## 3. Staartvlam: dezelfde aanpak overgenomen (zone x50–60, y32–45)
Naast elkaar op 12× (model | r2 | proef) lijkt de proef duidelijk meer op het model: een dunne, gebogen tong bovenaan in plaats van de rechte kolom van 2 px uit r2. Daarom overgenomen.
Weggevallen: de losse pixel (56,33) van de uiterste punt. De punt begint nu op (55,34).

## Zelf gezien
- De punt van de handtong ligt op y20, iets naar links (x8–9), met de verbreding naar rechts op y21. Dat is wat het model op 2× geeft; de omkrulling van de modelpunt is kleiner dan 1 spritepixel.
- De rechter zijvonk van de handvlam is weg, omdat hij op 2× maar 1 px was.
