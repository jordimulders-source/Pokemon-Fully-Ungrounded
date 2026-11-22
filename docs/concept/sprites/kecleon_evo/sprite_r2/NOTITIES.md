# Kecleon-evolutie, sprite r2 (maker-agent, 22 nov)

Jordi over r1: "maar de tinten kloppen niet" ("alles"). r2 = alleen nieuwe tinten; silhouet, lijnen en licht/schaduw-opbouw zijn die van r1 (`../sprite_r1/rijen.txt`, silhouet-assert in `bouw_r2.py`).

## Tinten: gemeten, niet bedacht (`meet.py` → `palet_gemeten.json`)
Mediaan per tintgroep in het Gemini-model, omlijning (l < 0.15) niet meegeteld; bij elke kleur staat de modelpixel die het dichtst bij de mediaan ligt (ook op `vel.png`).
- Lijf (r1_nat100): F (232,156,85) licht oranje · m (223,117,75) oranje tussentint · G (215,94,73) zalmrood · H (166,63,64) schaduw · r (143,55,53) donkerste schaduw/selout.
- Buik/geel (r1_nat100, mosterd): A (241,216,128) · B (235,189,95) · C (204,167,74) · D (145,117,54) · E (122,92,41) lijn/selout geel.
- Roze (r1_nat100): p (228,152,146) · q (204,102,109); de roze schaduw van het model (163,58,61) is gelijk aan H, dus samengevoegd.
- k (23,19,19) omlijning, w wit (pupilglans). Totaal 15 kleuren incl. transparant.
- r2-kuifgeel (243,217,89) gemeten maar niet gebruikt: valt qua helderheid samen met A; het r1-mosterd heeft de volledige ramp.

## Groen → oranje (Jordi koos variant A; B vervalt)
- `zones.py`: zone "was groen in het model" (kop en staart) uit het verkleinde model, 3×3-meerderheid, lijnen niet meegeteld (`zones_8x.png`). Daarin r1-geel → oranje op dezelfde toonplek: A/B→F, C→m, D→G, E-lijnen→r. De gele lijnen/strepen ertegenaan (kuifrand, ring om de oogkegel, strepen op de staartbasis) blijven geel, zoals in het model en bij de originele Kecleon (geel als band/rand tegen het vlak, spiraal als donkere lijn van de vlakkleur).
- Oranje tussentint m: zalm-pixels (G) die aan licht oranje (F) grenzen → m (ramp miste die stap).

## Per pixel bijgewerkt (`patch_r2.txt`)
- Buik: het model-mosterd D is donker (helderheid 118); 36 D-pixels midden in de buik → C, D alleen langs lijnen.
- 6 losse pixels na het omkleuren van de zones: (6,5) (17,19) (24,27) (51,43) (58,44) (47,51).

## Twijfels
- De gele kuifrand is mosterd (C/D) waar r1 schaduw had; daardoor lezen de kuiflijnen minder fel dan bij Kecleon. Lichter zetten kan per pixel, maar dat wijkt af van de r1-opbouw.
- Gezicht/wang en kuif zijn nu allebei oranje; alleen de gele lijnen scheiden ze (zoals gevraagd).
