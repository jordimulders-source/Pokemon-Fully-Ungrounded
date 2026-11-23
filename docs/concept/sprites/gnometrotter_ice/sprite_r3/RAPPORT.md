# Gnometrotter Ice – sprite r3 (A, zelfde pose), 23 nov

Basis: `../sprite_r2/gnometrotter_ice_gatdicht.png`. Uitgevoerd: de reparaties A1–A5 uit `../keuring/KEURING.md`, per pixel. Er is niets nieuw getekend buiten de pegel van A3.
Bouwen: `python3 r3.py` → `gnometrotter_ice.png` + `_8x.png`. Het script logt elke pixel.

**Diff t.o.v. r2 gatdicht: 89 px. Silhouet: 0 px.** Alleen tint en lijn.

| punt | px | wat |
|---|---|---|
| A1 baardtinten | 50 | x26–28/x30 rij 26–35 D→C (23), x25 rij 26–28 E→C (3), x29 rij 25–30 E→C (6), (29,31) E→3 (1; op rij 32–34 staat al 2), x24 rij 29–35 C→3 (7), x24 rij 25–28 C→D (4; model 205–231), x20 rij 27–32 C→D (6) |
| A2 roze notch | 2 | (20,34), (20,35): 7→3 |
| A3 pegel op de linkerdij | 23 | ijs 11 px: x19–20 D, x21 C op rij 43–45, (21,42) C als aansluiting op de riem, punt (20,46) D. Rand in 2 waar het ijs aan blauw grenst: 11 px. Daarnaast (19,47): het losse B-pixel dat onder de punt overbleef → 9 |
| A4 stok | 5 | (5,37), (5,41), (6,42), (6,49), (7,50): 1→2. De linkerrand is nu overal 2, zoals Rock r4 |
| A5 hand R | 9 | (61,37), (60,38), (60,39), (56–59,40), (57,41), (58,41) → 1, zoals Rock r4 |

## Pixels die niet rechtstreeks uit het model komen
- **A3:** de vorm volgt de lichte streep in het model (x19–21, y42–46), maar de verdeling van de tinten (links/midden D, rechts C) en de 2-rand zijn een regel uit de keuring. De modelpixels zijn per pixel ruisig (`kaart.py` geeft C/D/3 door elkaar).
- **(21,42)** en **(19,47)** zijn eigen keuzes: aansluiting op de riem en het opruimen van een los pixel.
- **A1:** de lijst van de keuring volgt de kolomgemiddelden van het model. Per pixel wijken (26,26) en (26,27) af: het model is daar licht (242/228), in de sprite staat C.

## Eigen kanttekening
- De pegel op de dij heeft rondom een rand in 2 en leest daardoor iets zwaarder dan de dunne streep in het model.
- De losse dij-pixels (23,43) B, (41,41) A en (42,40) B vielen niet onder A en zijn niet aangepast.
