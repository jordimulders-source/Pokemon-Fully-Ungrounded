# Vuurduivel fase 2: oogvarianten op r1

Jordi (letterlijk): "het oog mag afwijken van het model, beetje neutraal chaotic idee, rood met zwart erin of zwart met rood erin, geen wit".

**Werkwijze (`maak.py`):** elk oog is pixel voor pixel overgenomen uit een echte Gen 3-sprite (`graphics/pokemon/<soort>/anim_front.png`, frame 1). Alleen de oogpixels van de bron zijn gebruikt: lijn, oogwit/glans, iris. Huid- en vachtpixels van de bron zijn niet meegenomen. De kleuren zijn omgezet naar alleen zwart (3,1,1), donkerrood (105,20,22) en een nieuw oogrood (200,36,40) op de vrije paletindex 14. Er zit geen wit en geen crème in de ogen.
- **Versie X:** oogwit/glans wordt rood, iris en pupil worden zwart.
- **Versie Y:** oogwit/glans wordt zwart, iris wordt rood, donkere iris wordt donkerrood.
- **A** = de versie met het meeste rood ("rood met zwart erin"), **B** = de andere ("zwart met rood erin").
- **Basis:** r1, met de 6 oude oogpixels (27–29, 19–20) op de donkere maskertint (22,22,22). Daarna komt het bronoog erop.
- **Diff-bewijs:** buiten de zone x25–31, y17–21 is de diff met r1 0 (assert in het script). Aantallen per optie staan in `diff.txt`.

| Bron | Bronpixels (x,y in de bron) | Verschuiving naar vuurduivel |
|---|---|---|
| Absol (nabij oog) | x22–27, y24–26 (16 px) | +3, −6 |
| Sharpedo | x24–28, y39–43 (18 px) | +2, −22 |
| Sneasel | x30–35, y21–24 (19 px) | −4, −4 |
| Umbreon (nabij oog) | x19–23, y26–28 (12 px) | +7, −8 |
| Banette (linkeroog, spleet) | x17–20, y25–28 (14 px) | +10, −7 |

**Bestanden:** `oog_<bron>_<A|B>.png` (64×64, geïndexeerd, index 0 transparant). `opties.png` toont het model, r1 en daarna per optie de kop op 8× (x16–37, y10–29) met label, plus de optie op 1× op wit en op donkerblauw.

## Zelf gezien
- Het oog zit in het zwarte masker van het model. Daardoor valt de zwarte lijn van de bron weg tegen het masker, en de B-versies tonen soms maar 1–3 rode pixels (Sneasel B, Umbreon B). Op 1× leest B als een gloeiend puntje.
- Bij Absol zijn de donkere ooglijnen van de bron (vachtkleur 41,57,57 en 65,74,106) als lijn meegenomen.
- Sneasel A is een volle rode vlek van 3×2 met zwarte iris links (het oogwit van Sneasel is groot).
