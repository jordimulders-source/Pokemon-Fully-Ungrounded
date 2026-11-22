# Keuring r6 vuurduivel fase 1: kleurronde (`sprite_r6/vuurduivel_r6.png`)

Alleen kleur en schaduw; vorm, lijnen en ogen zijn bevroren (alpha-diff met r5 = 0, gemeten). Vel: `keuring_r6/vel.png` (r6 8× | model | kop 8×: r6, voorstel roze tong, model | r6 1×/2× en voorstel 2× | Houndour, Umbreon, Magcargo, Slugma 4×). Voorstelbestand: `keuring_r6/voorstel_roze_tong.png` (alleen de paletindeling hieronder toegepast, 26 px anders dan r6).

## Oordeel: **BIJNA** (twee MOET-punten, daarna PASS)

Het lijf is veel beter: het zwart heeft nu stappen ±25–30 (38/63/93) met glans 133 en lijn 15, zoals Houndour/Umbreon. Kop, borst, armen en oor hebben nu volume, en het lijf leest op 1× nog steeds zwart. Punten uit keuring_r5:

| r5-punt | r6 |
|---|---|
| 1 lijfpalet | goed |
| 2 kop (bolling, glans (20–21,25–26), wang (17,35)) | goed |
| 3 borst (licht + glans (23–24,44), sikkel rechts) | goed |
| 4 armen (nabij licht, ver donker) | goed |
| 5 linkeroor ((13,31) licht, (13,32) midden) | goed |
| 6 broek twee dijen | goed |
| 7 hoeven zonder streep | goed |
| 8 vlammen: middentint + geen dambord | **middentint wel, dambord niet opgelost** |
| 9 staartstam bovenlicht | goed |
| 10 geel pijlpunt 2 px | goed |
| (nieuw) tong | **oranjerood (226,88,62) waar het model roze heeft** |

## MOET

1. **Tong weer roze, binnen 16 kleuren.** Paletindeling:
   - Hoornmidden **(190,45,46)** (13 px, L 88) samenvoegen met het haarrood **(162,41,41)** (L 77; ΔL 11, de hoorn leest door de zwarte lijn en het hooglicht). Dat maakt een plek vrij.
   - Vrije plek: roze **(212,94,90)** (L ≈ 124). Model gemeten: tong (192–200, 88–96, 88), hoorn licht (228,84–96,84–96). Dat roze wordt de tong **én** het hoornlicht; beide zijn in het model roodroze.
   - Vlam-middentint (226,88,62) blijft alleen in het vuur (haar + pijl).
   - Pixels: tong (22–25,38), (22–24,39) → roze. Hoornlicht (15,23), (15,24), (16,25), (25,23), (25,24), (26,22) → roze. Alle (190,45,46)-pixels → (162,41,41). Uitgevoerd in `voorstel_roze_tong.png`. Hoornstappen R 45 → r 77 → roze 124 zijn goed, en de tong staat duidelijk los van het vuur.
2. **Haarvlammen: de middentint niet als losse stipjes.** Er zijn 21 losse clusters van 1–2 px van (226,88,62) in het haar:
   - (26,16), (25,17), (32,17), (36,17), (24,18), (22,19), (20,20), (27,20), (19,21), (28–29,21), (32,21), (30–31,22), (33,24), (32–33,25), (35,24–27), (37,26), (37,27)
   - ook nog r-stipjes zoals (25,16), (30,16), (24,17), (28,17), (31,17), (36,18), (21,19), (27,21).

   Regel: de middentint alleen als overgangsrand van 1 px **langs de onderkant/rechterkant van een oranje tong** (tussen O en r), doorlopend langs die tong. Een middentintpixel met alleen r om zich heen → r; met alleen O om zich heen → O. Rechts van de kop (x32–38, y21–28): één doorlopende tong (35,24–27) in middentint met O-kern, en (37,26–27) → r, zodat de kolommen 35/36/37 niet meer om en om wisselen.

## KAN
- Mondbinnenkant R (108,19,20) mag naar het model (120,56,48) als er een plek over is; nu niet nodig.
