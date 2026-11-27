# Sneeuwmonster r4
Basis: `sprite_r3_ogen/sneeuwmonster_r3.png` (linkeroog a1, glans linksboven). Twee keurderreparaties uit `sprite_r2/KEURING.md`; de ogen zijn niet aangeraakt. Diff t.o.v. r3: **24 px**, precies de lijst hieronder (assert in `bouw.py`); silhouet ongewijzigd.
1. **Kin, modeltinten terug (4 → 5), 21 px:**
   - rij 27: (22,27) (23,27) (33,27) (34,27)
   - rij 28: x23–26 en x29–33
   - rij 29: x25–32
   - Model-L per pixel 238–243, allemaal ≥ 236 (gecontroleerd).
   - Schaduw op rij 30–31 blijft. De onderrand van het licht buigt nu: midden tot rij 29, aan de zijkanten tot rij 28 en 27. De nekband is 2 rijen (rij 30 met middentint in het midden), geen rechte streep.
   - (31,27) en (32,27) blijven midden: het model heeft daar L 232–234, de schaduw onder het rechteroog.
2. **Pluklijntjes taps (2 → 3), 3 px:** (31,14), (33,14) en (28,17); model-L 201, 183 en 240 (eindpixels van de lijntjes).

Oogvarianten als complete sprites met dezelfde twee reparaties: `r4_oog_{a,a1,b,c}_{lb,onder}.png` (r4_oog_a1_lb = sneeuwmonster_r4).
Fix in r3_ogen (26 nov): de oogreset maakte buitenlijnpixel (21,27) per ongeluk sneeuw in alle r3-varianten. Dat is hersteld en r3 is opnieuw gebouwd vóór r4.
Vel: r4 8× naast het model, kin-close-up 12× voor (r3) | na (r4) | model, 1× op vier achtergronden.
