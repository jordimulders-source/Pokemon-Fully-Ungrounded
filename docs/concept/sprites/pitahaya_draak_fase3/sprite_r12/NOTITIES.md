# Pitahaya-draak fase 3, sprite r12 (maker): Jordi op r11 D

Jordi (letterlijk): "d is het beste, maar deze rechte lijn die ik geel getekend heb aan sprites ziet er een beetje gek uit, in de mond kan dat onderdeel van het wit worden en buiten de mond kan die misschien iets minder rechtlijning worden" (gele lijn: rij y30, x7-16).

- **Basis:** `../sprite_r11/pitahaya3_r11_D.png`. Palet gelijk. `python3 maak_r12.py` schrijft `pitahaya3_r12.png`, `pitahaya3_r12_alt.png` en `pitahaya3_r12_afwijkingen.txt`; `python3 vel.py <tijdelijke map>` maakt `vel.png` (kop 12× x0-22 y18-36: r12 | r12_alt | D | model; hele sprite 8×; 1× en 2× op licht en donker naast Salamence/Tyranitar/Sceptile).
- Wijzigingen alleen in x 6-16, y 26-31 (assert). Buik, knots en de rest pixelgelijk aan D.

## 1. In de mond (beide versies, 4 px)
- (8,30) (9,30) d -> w, (10,30) # -> w: het vlees loopt door tot de ondertanden, in de schaduwtint w (grijs boven, wit midden, grijs onder = holte).
- (7,30) blijft d: tandvlees naast de hoektand (6,30); anders loopt de tand in het vlees over.
- (9,31) w -> W: de ondertanden (8-9,31) zijn nu lichter dan het vlees erboven en lezen los.
- Pitjes ongewijzigd (driehoek (9,27) (11,28) (8,29)); geen pitje raakt een ander.

## 2. Onderkaak buiten de mond
- Model gemeten: de onderrand loopt schuin omhoog van ±(11; 31,5) via (13; 30,8) naar (14; 30,3), pas daarna vlak naar de nek. De sprite had x 12-16 één rechte zwarte lijn op y30.
- Zonder silhouetwijziging kan de rand niet verspringen (onder x 12-15 is transparant). Daarom **+1 px silhouet**:
  - **r12:** (12,31) . -> #, (12,30) # -> d. Onderrand: (7-9,33) (10,32) (11-12,31) (13-16,30): trap 3-1-2-4.
  - **r12_alt:** ook (13,31) . -> # en (13,30) # -> d (+2 px). Trap 3-1-3-3; de rechte lijn wordt 3 px.
- Model kiest eerder r12 (x 13 ligt in het model grotendeels op y30).

## Eerlijk oordeel
- Mond: de donkere streep is weg; leest als vlees in een holte met tanden eronder. Het vlees is aan de onderkant grijs, dus geen wit vlak tot de lip; puur wit gaf tand + vlees als één vlek.
- Kaak: r12 breekt de lijn met één trapje volgens het model; de rechte stukjes (13-16,30) zijn er nog, maar korter. alt is zachter maar loopt minder op het model.
