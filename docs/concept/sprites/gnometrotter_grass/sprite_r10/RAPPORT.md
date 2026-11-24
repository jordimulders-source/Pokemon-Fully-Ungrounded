# Gnometrotter Grass r10 (maker, 23 nov)

Basis `../sprite_r9/gnometrotter_grass.png`. Jordi: "de houten stok moet beter gekleurd, betere schaduw, evenals de muts en de bladersnor/haren. ... voor de rest ben ik tevreden".
Alleen kleur/schaduw binnen het bestaande silhouet; lijnpixels (5, 1, buitenrand) blijven staan. Script `maak_r10.py` (→ `gnometrotter_grass.png`, `_8x.png`, `log_r10.txt`, `vel.png` = model | r9 | r10 op 8×); `meet10.py` → `hel10.npy` (modelhelderheid per spritepixel).
Studie (8×): Shiftry/Tropius-blad = per blad een lichte en een donkere helft langs de nerf; Trevenant/Nuzleaf-hout en Rock af-stok = selout links, lichte strook, midden, donker rechts tegen zwart.

| Zone | px t.o.v. r9 |
|---|---|
| stok | 27 |
| muts | 89 |
| bladbaard/-snor | 61 |
| haar L | 10 |
| haar R | 18 |
| rest | 0 (assert) |

- **Stok:** per rij Rock af-opbouw: selout 2 | licht 4 (±45 %) | midden 3 | donker 2 tegen de zwarte rand rechts (vanaf 4 px breed); zijtakken licht van boven (bovenrij 4, onderrij 2).
- **Muts:** het linkerblad (model lum ±100–133, lichtst langs de linkerbovenrand) in bogen rond een hooglicht linksboven: 14 → 13 → 12 (sikkel onderaan boven het haar); het rechterblad (model lum ±70–89) blijft schaduw: 12, met 13 als randje langs de nerf linksboven en 5 als sikkel tegen de zwarte rand rechts. Nerven (5) onveranderd = de bladlijnen uit het model.
- **Bladeren (baard, haar L/R):** elk blad (vlak tussen de nerven) lichte helft linksboven 14, dan 13, schaduwkant rechtsonder 12 (bladeren < 8 px: 14/13).
- **Palet (alleen 12–14, groene ramp gelijkmatig, voorstel keuring_r5 E):** 14 (176,210,120) → (150,196,104); 13 (104,150,80) → (110,156,82); 12 (58,98,56) → (72,116,62). 0, 1, 2–11, 15 ongewijzigd. Let op: het blaadje aan de rugtak gebruikt ook 5/13, dus dat verschuift mee in kleur (index gelijk).
- Vlakjes < 3 px die overblijven: diagonale ketens (lichte nerfrand rechterblad, donkere strook stok rechts), en 4 losse pixels op een vlak van 1 px tussen nerven ((18,32), (32,15), (32,16), (35,14)).
- Niet gedaan: de "hout boog onder de arm" (wacht op Jordi).
