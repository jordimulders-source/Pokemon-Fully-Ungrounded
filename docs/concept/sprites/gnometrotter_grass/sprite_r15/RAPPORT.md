# Gnometrotter Grass r15 (maker, 23 nov)

Basis `../sprite_r14/gnometrotter_grass.png`, model `../hybride/model_hybride.png`. Jordi over r13: "het is nu een warboel geworden, het grote blad klopt, maar voor de rest herken je er amper nog iets in, kijk naar het model en maak er dan bladeren van zoals bij andere pokemon".
Script `maak_r15.py` → `gnometrotter_grass.png`, `_8x.png`, `log_r15.txt` (elke gewijzigde pixel), `muts_raster.txt`, `masker_r15.png` (genummerde indeling | model op dezelfde uitsnede), `vel.png` (model hoog | model op 64 | r14 | r15, muts 12×).

## Bladindeling uit het model (gemeten: donkere modelpixels lum < 60 per spritepixel)
1. **Groot linkerblad** = bevroren, inclusief zijn randlijn L1.
2. **Rechterblad**: van de top naar rechtsonder, eindigt in de haak boven het gat. Voorrand = modellijn D (34,5)(35,6)(35,7)(36,8)(37,9) (ligt vóór 3). Nerf = de modelcurve (38,4)(39,5)(40,6)(40,7)(41,8)(41,9), als grens van de helften. Het model heeft dit blad het donkerst: lichte helft (linksboven) 12, schaduwhelft (rechtsonder, tegen de omlijning) 5; de voet bovenop (rij 1–3) 13; de haak 12, haakpunt 5 (= r14).
3. **Middenblad**: wig tussen 1 en 2, punt boven (34,6), ligt achter beide; lichte helft links 13, schaduwhelft rechts 12.
4. **Onderblad** boven de neus: onder 1, links van modellijn LL (30,12)(31,13)(32,14) (3 ligt vóór 4); voet bij de kruising (30,12), nerf naar linksonder; helft linksboven 13, rest 12.

Bladgrenzen D en LL: 1 px 5. Geen nerf als losse lijn in de kleine bladen 3 en 4 (alleen helften). Geen facetten of tussentinten meer: elk blad heeft 2 tinten.

## Pixels t.o.v. r14
| Zone | px |
|---|---|
| blad 2 (rechts) | 31 |
| blad 3 (midden) | 7 |
| blad 4 (onder) | 11 |
| lijnen D/LL | 4 |
| **groot blad 1 (+ L1)** | **0** |
| **omlijning/silhouet muts** | **0** |
| **rest (buiten de muts)** | **0** (assert) |

Palet ongewijzigd; muts: 12 ×131, 5 ×92, 13 ×68, 14 ×8 (de 14 alleen in het bevroren blad 1). Losse vlakjes < 3 px in mijn zones: geen (alleen de haakpunt, 1 px tussen omlijning, = r14).
Zelf bekeken op 16× naast model en r14: alle vier de bladen van het model zijn als eigen blad met licht/schaduw te herkennen; het rechterblad leest als één breed donker blad dat over de rand buigt tot de haak.
