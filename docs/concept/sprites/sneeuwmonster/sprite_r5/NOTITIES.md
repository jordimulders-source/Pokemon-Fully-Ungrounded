# Sneeuwmonster r5
Basis: `sprite_r4/r4_oog_c_onder.png` (Jordi: "c glans onder, want dan kijkt die naar driekwart"). Ogen bevroren.
Jordi: "Bovenste knoop is ook niet rond, linkerstukje van de kuif ook niet en linkerkant van het hoofd is ook hoekig".
Diff t.o.v. r4: **14 px**, alleen binnen de drie zones (assert in `bouw.py`): knoop 11, kuif links 2, hoofd links 1.

1. **Bovenste knoop (11 px):** patroon en tinten 1-op-1 van de onderste knoop (x24–27, y41–45, `.XX./XXXX/XXXX/XXXX/.XX.`; die leest rond), op de modelplek van de bovenste knoop (model natief u37–42, v53–59 → x24,7–27,9, y34,5–39,0 → vak x24–27, y34–38). Oude knooppixels buiten het patroon worden sneeuw (midden, zoals de buurt).
2. **Linkerbolletje kuif (2 px, silhouet +1):** modeldekking op rij 12 is x28 .61, x29 .38, x30 .74; het bolletje is in het model bovenop 2 px breed, niet puntig. (29,12) achtergrond → sneeuwlijn (bovenrand, lichtkant); (29,13) sneeuwlijn → licht (binnenkant bolletje). De scheidingslijn naar het middenbolletje begint nu op (30,13).
3. **Linkerkant hoofd (1 px, silhouet −1):** modelrand (0,5-dekking) per rij: 16: 25,7 · 17: 24,6 · 18: 23,5 · 19: 22,6 · 20: 22,3 · 21: 21,7 · 22: 21,2 · 23–26: 20,6 · 27: 21,1 · 28: 21,2. r4 had op rij 18 twee randpixels naast elkaar ((23,18) en (24,18)), een sprong van x25 naar x23 = de knik. (23,18) eruit (dekking .50). De trap wordt 1-1-1-1-2-7 (x26 r16, x25 r17, x24 r18, x23 r19, x22 r20–21, x21 r22–28). De selout blijft sneeuwlijn.

Vel: r5 8× | r4 8× | model; per zone 12× voor (r4) | na (r5) | model; 1× op vier achtergronden.

Twijfels:
- Kuif: met (29,12) gevuld lopen de bovenranden van het linker- en middenbolletje op rij 12 door (x28–30). De scheiding komt dan alleen van de lijn (30,13)–(31,14); in het model zit daar een klein zwart inkepinkje (natief (45,19), ±(29,8; 13,2)).
- Hoofd: de lange rechte rand x21 (rij 22–28, 7 px) is de bijna verticale zijkant zoals in het model (rand 20,6–21,2). Een extra bolling naar x20 op rij 23–26 (dekking .41–.45) zou een 1-px knik in de trap geven, dus die is niet gedaan.
