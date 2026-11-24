# Satelliet fase 1 – sprite r3 (maker)

Basis: `../sprite_r2/sprite.png`. Reparaties P1, P2 en P3 uit `../eindkeuring_r2/KEURING.md` precies uitgevoerd met de code van `eindkeuring_r2/voorstel.py`, als `r3.py` (draaien vanuit `fase1/`). Bij elke pixel wordt eerst met een assert de oude waarde gecontroleerd. Het silhouet blijft gelijk (assert) en het palet is niet veranderd. Niets hertekend.
Jordi: "let op onnodige zwarte pixels ook".

## Pixeldiff r2 → r3 (23 px, zwart 230 → 209)
| code | (rij,kol): oud → nieuw |
|---|---|
| Z1 | (15,23) D→K; (15,22) K→P |
| Z2 | (17,34),(18,35) K→D |
| Z3 | (34,39) K→D |
| Z4 | (48,37) K→D |
| Z5 | (44,31),(44,32),(44,33),(45,30),(46,29) K→D |
| V1 | (37,37) K→m; (37,40) K→P |
| V2 | (12,55) K→P |
| V3 | (14,26) K→P |
| V4 | (42,5) K→P |
| V5–V7 | (44,7) K→w; (46,8) K→l; (48,11) K→m |
| V8 | (50,30) K→P |
| V9 | (56,55) K→P |
| O1 | (39,7) K→w; (37,15) K→w |

## Metingen
- Diff met r2 buiten deze 23 pixels: **0** (script). Silhouet gelijk aan r2.
- `rond.py` gelijk aan r2: centrum (20,6; 33,7), r = 18,26; max afwijking per kwadrant −0,64 / +0,68 / +0,64 / +0,78 px.
- Open randen: **0** (`check.py`).
- Losse vultintpixels (< 3 px, 8-buren): **0**, net als in r2.
- Antennes: per kolom vergeleken met r2 (kleurpixels P/p). Geen enkele kolom is dunner geworden, wel een paar dikker (V2, V3, V9, Z1).
- `sprite.png`: 64×64, indexed, 16 paletplekken, index 0 transparant, 10 kleuren in gebruik.

## Oplevering
`sprite.png`, `sprite.npy`, `vel.png` (r3 | r2 | model op 8×, oog op 12× naast het model, 1×/2× op licht/donker/groen), `sprite_8x.png` (alleen de sprite op 8×, transparant) en `sprite_8x_wit.png` (dezelfde op wit).

## Eigen zwakke punten
Geen nieuwe. Wat de keurder ter info voor Jordi noemt (zwart linksonder in kolom 2–8, rij 37–47, en de zwarte boog rond het oog uit het model) heb ik niet aangeraakt.
