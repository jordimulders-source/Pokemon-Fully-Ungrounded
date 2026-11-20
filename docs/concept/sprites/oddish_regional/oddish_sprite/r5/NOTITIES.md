# Kelp-Oddish r5 = r4b + Jordi's afwijking ("Akkoord, maar houd het subtiel")

Basis `../r4/oddish_r4b.png`. Gezicht en lijf pixelgelijk (diff 0 buiten index 0/6–9, met assert in `bouw.py`). 12 kleuren incl. transparant (ongewijzigd).

## Palet (alleen indices 6–9): tint −6°, verzadiging ×0,85, helderheid (Rec.601) gelijk
| index | r4b | r5 | L |
|---|---|---|---|
| 6 selout | (86,66,12) | (89,63,19) | 66 |
| 7 schaduw | (142,124,24) | (147,119,36) | 118 |
| 8 midden | (184,162,54) | (188,157,72) | 157 |
| 9 licht | (218,198,120) | (216,194,144) | 195 |
Let op: de hechtvoetjes gebruiken dezelfde indices en verschuiven dus mee (zelfde kelp).

## Rand: 10 px op 4 plekken (alleen waar de rand recht/regelmatig liep; geen silhouet- of richtingwijziging)
- Blad links (A), linkerrand 1 px uit: (24,24) 0→6, (24,25) 6→8.
- Blad linksboven (B), linkerrand 1 px uit: (19,27) 0→6, (19,28) 6→7.
- Blad rechtsboven (D), rechte bovenrand y20 x42–46 → bolling van 2 px: (19,43) en (19,44) 0→6, (20,43) en (20,44) 6→7.
- Blad rechtsonder (E), bovenrand 1 px in: (25,48) 6→0, (26,48) 8→6.
(x,y) = (kolom,rij) staat hier als (rij,kolom) zoals in `bouw.py`: (y,x).
Geen losse pixels of dambord toegevoegd; elke nieuwe randpixel is selout (6) met de vultint erachter.

`vel.png`: r4b | r5 | Oddish uit de game op 8×, eronder 1× op licht.
