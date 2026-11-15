# Gengas sprite v4 (15 nov) – kern lichtvlek terug

v4 = v3 met twee wijzigingen (`v4.py`, daarna `maak.py`, `vel.py`):
1. **w (220,172,176) terug** op precies de 18 v2-plekken (= model), want v3 had de lichtvlek plat gemaakt.
2. **r (118,48,67) → m (140,49,85)** om plaats te maken.

## Waarom r → m (gemeten, niet gekozen op het oog)
Voor elk tintpaar heb ik gemeten hoeveel de afstand tot het model (ΔE, Lab) groeit als alle v3-pixels van tint A tint B worden. Als referentie diende het model op de juiste plek, met het gezicht verschoven zoals in v3:
| samenvoegen | px | extra ΔE (som) | gem./px |
|---|---|---|---|
| E→R / R→E (oogrood) | 14/16 | 164/168 | – valt af: oogrood blijft twee tinten |
| u→b (wig) | 47 | 279 | – valt af: wig blijft (opdracht) |
| **r→m** | 77 | **518** | 6,7 |
| g→G (maangrijs) | 74 | 540 | 7,3 (sloopt de kraters van v3) |
| r→u | 77 | 608 | 7,9 |
| r→b | 77 | 738 | 9,6 |
Wat w terugzetten oplevert: −277 ΔE op 18 px. r→m blijft een gekleurde selout aan de lichtkant: bovenrand van de kop, randen van de oren en lijnen, iets lichter dan voorheen.

## Diff v3 → v4
18 px v→w (alleen v2-w-plekken, lichtvlek) + 77 px r→m; **verder 0 pixels anders.** 15 kleuren + transparant.

## Zwak punt
- De selout op de bovenrand van de kop is nu m: iets minder contrast met de lichte band (l) dan r had. Op 1×/2× nauwelijks zichtbaar.
