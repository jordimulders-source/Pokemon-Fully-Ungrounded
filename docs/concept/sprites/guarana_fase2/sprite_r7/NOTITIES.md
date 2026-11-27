# Guaraná fase 2, ronde 7: pupillen van de grote ogen

Jordi over r6 (letterlijk): "er is geen enkel oog dat echte driekwart kijkt", "laat in elk geval de grote ogen dat doen",
daarna: "ja dus iets naar linksonder vanaf het midden".

Bestanden: `guarana2_r7.png` + `normal.pal` (= r6), `voor_jordi_r7_8x.png` (r7 | r6, 8×, wit). Bouwen vanuit `guarana_fase2/`: `python3 sprite_r7/bouw7.py`.

## Wat er veranderde
- Alleen de vijf grote ogen (2×2-pupil): L4, L5, M4, R5, R6. Oogvorm zoals r6.
  Het wit (stempel r5) is per rij 3-5-5-3 breed (rij 1 met grijs aan de zijkanten). De pupil (2×2) staat nu in kolom 2–3 en rij 2–3 van het oog:
  1 kolom wit links, 2 kolommen wit rechts, 1 rij wit boven en 1 rij wit onder.
- 17 px anders dan r6 (oude pupilpixels → oogwit, nieuwe → zwart), allemaal binnen deze vijf ogen; daarbuiten diff 0, silhouet diff 0.
  R6 ligt grotendeels onder de buitenlijn/andere ogen: daar veranderde maar 1 px.
- Kleine en half dichte ogen niet aangeraakt.

## Beperking
Het wit is maar 4 rijen hoog. Daardoor kan de pupil niet tegelijk een stap omlaag én wit eronder hebben:
- pupil in rij 2–3 (gekozen): wit links en onder, maar verticaal in het midden; hij staat alleen een halve tot één pixel links van het midden;
- pupil in rij 3–4: wel lager, maar dan raakt hij de onderrand (zo stonden M4 en R6 al in r6).
Wil Jordi het oog duidelijker linksonder laten kijken, dan moet het oog een rij hoger worden of de pupil kleiner (bv. 3 px L-vorm). Dat moet hij dan zelf kiezen.
