# Gengas v15: lijf zonder manen rechts rond en dicht (16 nov)

Jordi: "nu moet je zonder manen na nog fixen" (na = `sprite_v14/lijf_zonder_manen_v14.png`); eerder: "hij is niet rond".
Alleen het lijf zonder manen (frame 2-onderlaag); de hoofdsprite `sprite_v14/gengas_v14.png` is niet aangeraakt.

**Methode:** dezelfde ellips als v14 links, die de onaangetaste omtrek volgt: x = 29,5 ± 22,5·√(1 − ((y−34)/24)²) (raakt x 52 op rij 30–39 en de bodem op rij 58). Rechtsonder alleen rij 50–54 aangevuld tot die ellips; rij 49 en 55–57 klopten al. Nieuwe binnenpixels trekken de donkere band (index 2) van rij 50–52 door; de lichte onderband (5) eindigt waar hij al eindigde; nieuwe rand = 1 px omlijning (index 1), diagonaal aansluitend op (47,49) en (40,55).

**Gasarm rechts (rij 21–23):** de arm (index 2) blijft. Er stond een losse lijnpixel (53,22) met een gat ervoor (51–52,22) en een open rand op (50,23); de omlijning loopt nu (53,21) → (52,22) → (51,23) → (51,24). Rechts waar de handmaan lag (rij 24–31) was de omtrek al dicht (x 51–52 met lijn). Linksboven: de bovenste maan (rij 0–9) overlapte het lijf niet; niets te doen.

**Gewijzigde pixels (14), (x,y): voor → na**
- rechtsonder: (47,50) 1→0 · (45,50) 1→2 · (43,51) 1→2 · (44,51) 0→2 · (45,51) 0→1 · (43,52) 0→2 · (44,52) 0→1 · (43,53) 0→1 · (41,54) 5→1 · (42,54) 0→1
- onder de gasarm: (51,22) 0→2 · (52,22) 0→1 · (53,22) 1→0 · (51,23) 0→1

**Rechterrand per rij (laatste niet-achtergrondpixel), voor → na (ellips):**
| rij | voor | na | ellips | laatste index voor → na |
|---|---|---|---|---|
| 22 | 53 | 52 | – | 1 → 1 (losse lijn weg) |
| 23 | 50 | 51 | – | 2 → 1 (open → dicht) |
| 49 | 47 | 47 | 47,1 | 1 |
| 50 | 47 | 46 | 46,3 | 1 (platte snede 45–47 weg) |
| 51 | 43 | 45 | 45,4 | 1 |
| 52 | 42 | 44 | 44,4 | 2 → 1 (was open) |
| 53 | 42 | 43 | 43,2 | 5 → 1 (was open) |
| 54 | 41 | 42 | 41,9 | 5 → 1 (was open) |
| 55 | 40 | 40 | 40,4 | 1 |
| 56 | 38 | 38 | 38,5 | 1 |
| 57 | 36 | 36 | 35,9 | 1 |

Stappen rij 49–57 nu 0,1,1,1,1,1,2,2,2 (vloeiend). Asserts in het script: diff alleen in de twee zones (x 40–48 / rij 49–56 en x 50–54 / rij 20–24), x < 40 en rij 0–19, 25–48, 57–63 pixel voor pixel gelijk (ogen, grijns, oren, banden), geen nieuwe indexen, laatste pixel rij 44–57 is omlijning, geen losse pixels in de zones.

Bestanden: `rond_rechts.py`, `lijf_zonder_manen_v15.png` (index 0 = achtergrond), `lijf_zonder_manen_v15_8x.png` (wit, 512×512), `voor_na.png` (boven 8×: v14 | v15; onder 16×: rechtsonder x 34–51/rij 44–58 voor | na, gasarm x 44–57/rij 16–27 voor | na).
