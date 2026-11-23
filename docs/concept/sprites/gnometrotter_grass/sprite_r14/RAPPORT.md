# Gnometrotter Grass r14 (maker, 23 nov)

Basis `../sprite_r13/gnometrotter_grass.png`. Jordi: "het is nu een warboel geworden, het grote blad klopt, maar voor de rest herken je er amper nog iets in, kijk naar het model en maak er dan bladeren van zoals bij andere pokemon".
Script `maak_r14.py` (→ `gnometrotter_grass.png`, `_8x.png`, `log_r14.txt`, `muts_raster.txt`, `masker_r14.png`, `vel.png` = model | r12 / r13 | r14, muts 12×).

## Bladindeling van het model (masker_r14.png, donker = nerf/omlijning)
1. **Groot linkerblad** (bevroren, = r13): punt boven bij x ±33, voet linksonder (x ±16, rij 13). Ligt vóór 2 en 4.
2. **Middenblad**: smal, punt boven bij x 34 (rij 2–3), wordt breder naar beneden tot de voet boven de neus (x 31–37, rij 12–14). Ligt tussen modellijn L1 (rechtsrand van 1) en L2 ((34,3)→(37,9)); ligt vóór 3, achter 1.
3. **Krulblad rechts**: begint aan de top (x 34–36, rij 1–2), loopt naar rechts en omlaag tot de punt rechtsonder (x ±43, rij 13–14), met het gat eronder; ligt achter 2, in de schaduw.
4. **Onderste blad**: liggend, onder 1 en 2, boven de neus (x 24–30, rij 13–16).

## Uitvoering
| Zone | px t.o.v. r13 |
|---|---|
| blad 2–4 (muts) | 40 |
| blad 1 (groot, bevroren) | 0 |
| rest | 0 (assert) |

- De dikke nerfklodders uit r9 midden in de muts (rij 3–9, x 34–38) zijn weer blad 2/3 geworden; scheiding nu als dunne lijn 5: L1 (rechtsrand van 1, onveranderd) en L2 volgens het model.
- **Blad 2**: punt taps (rij 3–6: 1 px, licht 13); middennerf 5 op x 34 (rij 8–12, niet in punt of voet); helft links licht 13, helft rechts schaduw 12.
- **Blad 3 (krul, schaduw)**: punt/toprand 13; buitenhelft boven licht 13, verder 12; binnenhelft 12, onderaan bij de krul 5 (het donkerst, zoals het model bij het gat); nerf = grens van de helften (36,2)→(42,12).
- **Blad 4**: lichte bovenhelft 13, schaduwhelft 12.
- Losse pixels: alleen (41,11) (1 px 5 bij de punt van de krul, tegen de omlijning).
