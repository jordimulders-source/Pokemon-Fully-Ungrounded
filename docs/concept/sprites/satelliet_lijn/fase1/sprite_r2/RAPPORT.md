# Satelliet fase 1 – sprite r2 (maker)

Basis: `../sprite_r1/sprite.npy`. Reparaties: precies de lijst uit `../keuring_r1/KEURING.md` (code overgenomen uit `keuring_r1/voorstel.py`) in `r2.py`, elke pixel met een assert op de oude waarde. Niets hertekend, geen andere pixels.
Jordi (tussendoor): "let erop dat de bol mooi rond blijft".

## Pixeldiff r1 → r2 (23 px + 2 paletkleuren)
| code | pixels (rij,kol): oud → nieuw |
|---|---|
| R1 rand linksboven | (22,5) D→transp.; (24,4) D→transp., (24,5) w→D; (25,3) D→transp., (25,4) w→D; (26,3) D→transp., (26,4) w→D |
| R2 rand linksonder | (48,9) transp.→zwart; (47,9) zwart→m |
| R3 rand rechts | (29,38) transp.→zwart; (29,37) zwart→m |
| T1 hooglicht | (22,22),(18,20),(19,21),(24,21) W→w |
| T2 losse tintpixels | (26,12),(27,14) w→W; (26,7) W→w; (36,37),(25,36),(26,36) l→m; (41,6) p→P |
| T3 open rand | (12,23) P→D |
| P1 palet | tint 7 (174,162,218)→(184,174,226); tint 8 (130,114,184)→(140,126,194) |

Diff buiten deze 23 pixels: **0** (script `r2.py`). Kleuren: 10 + transparant.

## Controles
- **Bol rond** (`rond.py`, cirkelfit op de buitenlijn): centrum (20,6; 33,7), r = 18,26. Max afwijking per kwadrant: linksboven −0,64, linksonder +0,68, rechtsboven +0,64, rechtsonder +0,78 px (allemaal ≤ 0,8; r1: tot 0,86). Enige punt > 0,7: onderrand (52,23) 0,78, uit het model.
- **Trappen** links (rijen per x, boven → onder): 1-1-1-1-2-1-2-2-3-**8**-3-2-1-1-2-1-1-1-1-1-1. Boven en onder van de evenaar nu regelmatig en bijna gespiegeld (r1 had boven …1-2-2-1-5-8 met een knik). Onderkant (kolommen per y): 1-1-1-1-1-1-1-2-2-2-3-6-2-2-1, zonder de zigzag van r1 (2-1-2).
- **Open randen:** geen (`check.py`).
- **Losse tintpixels** (< 3 px, 8-buren, vultinten): r1 had er 5, r2 heeft er 0, en er zijn geen nieuwe bijgekomen. Wat `check.py` met 4-buren nog noemt zijn diagonale lijntjes (antennes, oogring, naadlip) die al in r1 stonden en door de keurder zijn goedgekeurd.
- **Lijfstappen** (helderheid): 255 / 225 / 182 / 139 → stappen 30 / 43 / 43 (was 30 / 53 / 45).

## Eigen zwakke punten
Geen nieuwe. Wat de keurder in r1 heeft laten staan, staat er nog: de vlakke bovenkant achter het voetje, de onderrand van 6 px (rij 52, allebei uit het model) en de w-lip naast de naad.
