# Kudu r6: strengere ogen (S1–S6)
Jordi over oog B: "hij heeft een veel te lief oog"; daarna "alle 4" (A–D zijn allemaal te lief). Eisen: zwart oog ("kudu irl heeft een zwart oog"), uitstraling "koninklijk, kalm". Het model heeft een zwaar, half gesloten lid.

Script: `sprite/oog_streng.py` (start = `r6/grid.json` met oog B; eerst alle A–D-oogpixels terug naar het lege oogvlak (wit uit het model of vachttint uit de modelhelderheid, zelfde regel als `r6.py`), dan de variant). Vel: `oog_streng_varianten.png` (hoofd 8×, sprite 2× en 1× op licht en donker). Elke pixel staat per variant met bron in `oog_streng_pixels.txt`. Buiten het oogvlak verandert niets (diff 0, met script gecontroleerd).

## Meting van het model (zwart = helderheid < 60, per spritecel)
- Rij 22, x 10–13: 22 / 43 / 37 / 18 %. Rij 21, x 12: 26 % (de plooi aan de achterkant: het lid is achteraan dikker dan vooraan). Rij 23, x 11: 21 %.
- Onder het lid heeft het model alleen een smalle strook oogwit (rij 23, 7–18 %). Het modeloog is dus een spleet van ruim 1 px hoog. B (Ponyta, 3×3 met de glans bovenaan) maakt het oog rond en groot, en daar zit het "lieve" in.

## Varianten
| | Wat | Bron per pixel |
|---|---|---|
| **S1** | Alleen de modelspleet, geen pupil, geen glans | Model: elke cel met ≥ 20 % zwart → 0: (12,21), (10–12,22), (11,23) |
| **S2** | Modellid met daaronder de halve Ponyta-pupil, geen glans | Ponyta (17–19, 25–28) 1 rij hoger dan B (dy −4): haar eigen lid komt op rij 21 (x 11–12), haar bovenrij met de glans valt onder het modellid; zichtbaar blijft K K 0 / 0 0. Daarover de modelcellen van S1 |
| **S3** | S2 + glans in de onderhoek | Als S2; de Ponyta-glans (bronpixel (18,26)) staat op (10,23), linksonder in de pupil |
| **S4** | Zwaar lid: modellid 2 rijen dik over de B-pupil | Ponyta op de B-plek (dy −3); modellid op rij 22 én 1 rij lager (rij 23, x 10–13) erover; modelplooi (12,21). Glans bedekt |
| **S5** | Tauros-oog (rund, schuin lid) | Tauros rechteroog (24–27, 30–34) 1-op-1, dx −13, dy −8 (lidpunt op de achterkant van het modellid). Omgekleurd: lid 74,49,0 → 0, rand 106,82,16 → K, lavendel oogwit → 0 (zwart oog), pupil → 0, eigen glans → W |
| **S6** | S5 zonder glans | Als S5; de Tauros-glans → K (tint van zijn eigen oogrand) |

Niet gebruikt na controle (oogwit in de bron): Stantler, Tropius, Lapras, Hypno, Alakazam, Nidoking, Donphan. Ursaring (glans bovenaan, rond) en Pidgeot (5×5, roofvogeloog) bekeken, te rond of te groot voor het oogvlak.

## Oordeel Claude (op 1×)
- **Minst lief + meest kalm-koninklijk: S2.** Klein donker oog half onder het zware modellid, zonder glans: rustig en neerkijkend, niet lief, niet boos.
- S4 is het strengst, maar het lid en de pupil worden op 1× één donkere vlek (zwaar, bijna somber).
- S1 is het trouwst aan het model, maar kan op 1× lezen als een gesloten oog.
- S3 (glans onderin) wordt weer iets levendiger en lieflijker dan S2.
- S5/S6 (Tauros): een groter, schuin oog; streng, maar rommeliger en minder kalm.
