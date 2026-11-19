# Hoatzin fase 2, r11 (19 nov), maker: reparaties op r10 naar het model + Jordi's punten

`sh alles.sh` bouwt alles (modelcel → bouw → kop → kuif → poten → ontdam → check → vel). `vel.png` = r11 | r10 | model | Archeops | Braviary (8x) + 1x/2x, kop 12x r11 | model | r10.
Werkwijze en studie: zie `../r10/NOTITIES.md`.

| reparatie | wat (gemeten op het model, `modelgrid.py` 40x) |
|---|---|
| 1 kop | blauwe vlek 7x7 (x10-16, y19-25, model 9.9-16.1 × 19.5-25.3), 9 vlak + 8 rand rechtsonder; oog 4x4 rond (x11-14, y20-23, model 11-14 × 20.5-23.5): zwarte ring, 3 px rode iris, zwarte pupil |
| 2 snavel | x5-11, y21-27 (model 6.4-11.5 × 20.7-27.5), rug licht F, midden E, bekspleet en onderrand donker, haakpunt linksonder |
| 3 verre vleugel | 5 puntige pennen (taps 1.9 → 0.55) op de modelpunten, een stap donkerder |
| 4 poten | schenen 4 px vulling, tenen 3 rijen, klauwen 2 px zwart; nabij F/E/2, ver E/2 (donkerder); omlijning 1 schaduwkant, 2 lichtkant |
| 5 nekband | lichte streepjes uit het model als 2 doorlopende 1-px-lijnen (M4) in de donkere band, 2 donkere lijnen in de lichte hals |
| Jordi: plukken 1 px smaller | losse plukken nu 1 px (punt 7, basis 6), K5/K6 2 rijen; plekken, richting, lengte gelijk |
| Jordi: plukken sluiten aan op de kop | geen donkere rand meer tussen kruin en kop (rand alleen over de verre vleugel), kruin onderaan 6 op de kop; gaten van de oude r9-kuif gedicht |
| Jordi: bovenkant buik geleidelijker | buik met ronde bovenkant (ellips), geen rechte bovengrens meer |
| Jordi: nek onderscheiden van vleugel | nek lichter (L5/M4), voorrand en arm van de vleugel een niveau donkerder (M4/D3/D2), D2-binnenlijn waar de vleugel over de nek valt |

## Script-check (`check.py`, na `ontdam.py`)
dambord 0 (was 21 in r10; 33 px opgelost door één mauve-pixel per blok gelijk te maken of een 1-px-pluk een trapje te geven), om-en-om op de buitenrand 0, zwarte binnenklonten 0.

## Afwijking t.o.v. r10
486 px anders, silhouet 76 px (snavel, puntige pennen, poten). Kop/snavel 49, kuif + verre vleugel 133, poten 111, nek + buik 171.

## Zwakke punten (eerlijk)
- Oog: in 4x4 is de iris maar 3 px rood (L-vorm rond de pupil); geen glans meer. Leest als rood oog met zwarte pupil, maar klein.
- Verre vleugel + dunne plukken boven op de kop blijven druk (veel donkere randen rond 1-px-plukken).
- Verre poot heeft 2 grijstinten (E/2); een derde (paars D3) vloekte.
