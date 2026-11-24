# Gnometrotter Grass r8 (maker, 23 nov)

Basis `../sprite_r7/gnometrotter_grass.png`; alleen de blauwe benen (keuring_r6 R3–R5). Script `maak_r8.py` (→ `gnometrotter_grass.png`, `_8x.png`, `log_r8.txt`, `vel.png` = model | r7 | r8 | Rock af op 12×, alleen de benen x 14–52, y 35–58; assert: niets buiten de zone).

| Zone | px t.o.v. r7 |
|---|---|
| heup rechts (R3) | 23 |
| dijen + laarzen (R4, R5) | 173 |
| rest | 0 |

- **R3:** de pixellijst uit de keuring 1-op-1 (incl. (48,36) riem 3 → 1 en (49,36) → 1, zoals de lijst zegt) plus alle blauwe Rock af-pixels in x 43–50, y 36–42 waar Grass blauw heeft. Zes Rock-pixels zijn hier zwart (de onderrand van de Rock-riem, die in Grass anders ligt); die zijn niet overgenomen, Grass houdt daar blauw (diff 6).
- **R4:** per bol (dij L, dij R, kruisstuk, voet L, voet R) één verdeling 11 linksboven / 10 / 9-sikkel rechts en onder. Grootste 11-vlak 23 px (was ±100); 9 in x 17–50, y 42–48: 69 px (Rock af 76). Plankvormen uit het model: linkerdij één diagonale naad in 9 van (20,44) naar (28,47) in treden van 2 px, met de schaduwkant eronder in 10; rechterdij: het kruisstuk (x ≤ 35–38, de diagonale grens uit het model) als donkerder plank in 10, de dij zelf met de lichte diagonale baan en sikkel rechts. Geen extra lijnen.
- **R5:** laarzen met 9-sikkel rechts en onder (2–4 px, de bolling volgend); grenslijnen dij|voet uit r6 blijven.
- Vlakjes < 3 px: alleen (23–24,45), een trede van de diagonale naad (diagonaal aansluitend).
