# Blobfish fase 1, sprite r3 (maker)

Start: `r2.png` (= `../sprite_r2/blobfish_r2.png`). Silhouet bevroren (alpha-diff 0, assert in `maak_r3.py`).

## 1 Lipmasker (`lipmasker.py`, `lipmasker.npy`, `lipmasker_overlay.png`)
Natieve pixel = liptint als helderheid 100–200, R ≥ 180, R−G ≥ 60 (lichtroze/zalm-cluster), in de gezichtszone; sluiting 3×3 zodat de dunne mondlijn binnen de band valt; spritepixel (zelfde 4×4-fase) in het masker bij ≥ 6/16. Masker = 50 px: van de voorkant van de kop (x7, y44–47) schuin omlaag tot x20 (y48–50), recht onder het nabije oog. Overlay: cyaan omtrek over r2 op 16×.
Gemeten: r2 vulde het masker al bijna helemaal; 8 maskerpixels stonden nog op lijf/lijn en zijn nu liptoon (dichtstbijzijnde van 9/10/11 bij het gemiddelde van de liptint-pixels in het blok): (8,44) (9,45) (10,46) (12,47) linksboven, (20,48) (20,49) (20,50) rechts onder het oog, (12,50) onderlip. Mondlijn 1 px zwart: (8,46) (9,47) (10,48) (11,48) (12..19,49). De rand (x7) blijft buitenlijn.

## 2 Ogen (vel: gezicht 16×, gele kaders = spritecellen waarin het oog van het model valt)
Model: nabij oog = cellen (19–20, 45–46), ver oog = (9–10, 41–42) (+ glanspuntje op de rand (8,40)). Beide nu 2×2 in die cellen, zoals het model opgebouwd: glanspuntje linksboven wit, pupil rechtsboven zwart, wit sikkeltje onder → 3 wit + 1 zwart tegen het donkere lijf. Nabij: (19,45) wit (3 donker + 1 glanspx), (20,45) zwart (7 donker), (19,46) wit (5 licht), (20,46) wit (12 wit). Ver: (9,41) wit, (10,41) zwart (3 donker), (9,42) (10,42) wit (= kale reductie van r1).

## 3 Borstvin
Model: lichte bovenrand + stralen die van de aanhechting (links) naar de rand waaieren: B schuin omhoog (32,44)→(36,43), C vlak (33,46)→(37,45), D omlaag (33,50)→(36,51). De krul kwam van straal A ((34,42) (36,41)), die vlak onder en evenwijdig aan de bovenrand ligt: weggelaten (lijftint 4, minder stralen mag), plus losse glanspixel (37,42). Straal B doorgetrokken naar de aanhechting: (32,44) 4 en (33,43) 3 straalpx → tint 11.

## Afwijkingen t.o.v. r2: 16 px (`afwijkingen_r3.txt`)
| Zone | px |
|---|---|
| gezicht, lippen (L) | 8 |
| gezicht, ogen (O) | 3 |
| borstvin (S) | 5 |

## Zelf gekeken op 1× en 2× (punt 4)
- Ogen: beide nu als wit oog met zwarte pupil te zien, ook op 1×.
- Mond: op 2× een brede lichte lipband met één donkere mondlijn van de voorkant van de kop tot onder het oog; de mondlijn daalt links schuin in (de "smile"-boog aan de voorkant). Het omhoog krullen aan het **rechter**eind is in het model maar ±2 natieve px (0,5 spritepixel binnen rij 49) en is op deze maat niet als pixel te zetten zonder te tekenen; het lipeind (lijnrood, x21 y47–50) buigt wel rond. Leest op 1× als brede mond, "blij" vooral door de lichte lippen; een echte opkrul rechts zou een afwijking van het model zijn (1 px op (19,48), daar heeft het model 0 donkere px) — keuze voor Claude/Jordi, niet gedaan.
- Borstvin: geen "@" meer; bovenrand + 3 stralen die naar rechts waaieren.
