# Eindkeuring viscacha kleur r8: Dragonfly Cave + Gen 3 (stap 7, 7 nov)

Hier is alleen de uitvoering gekeurd. Het model (`referenties/gemini_gekozen_ronde6.png`), het silhouet en het luie oog zijn bevroren en vallen buiten deze keuring.
De sprite is `kleur_r8/viscacha.png`, met als bron `raster.txt`.
Vellen (scratch):
- `dfc/vel8x.png`: 8× naast Taillow, Sandshrew, Pachirisu, Dedenne en Raticate (de bovenste 64×64 van anim_front);
- `dfc/vel1x.png` en `dfc/vel1x_3.png`: 1× op een lichte en een donkere achtergrond;
- `dfc/kop.png` en `dfc/staart.png`: close-ups op 16×.

## Controles
| Punt | Oordeel | Meting / pixels |
|---|---|---|
| Omlijning 1 px, geen klonten | voldoet | Overal 1 px. Open randen 0 en geen lichte kleur op de buitenrand (script: 0 lichte randpixels). |
| Selout aan de lichtkant | voldoet | Telling van de randpixels per richting. Selout 2: boven 38, links 41, rechts 2, onder 3. Selout 8 (geel): boven 16, links 20, rechts 3, onder 2. Zwart: rechts 102, onder 82. Zwart aan de lichtkant zit alleen op onderkanten (pluk (6,32)–(7,33), kin (9,38)–(10,39)), in de nekkerf achter de sikkel ((27–29,30–31), een diepe hoek) en op de binnenkant van de staart, die achter het lijf ligt. |
| Om en om zwart/selout | voldoet | Eén kandidaat: (58,20), een 8 tussen twee keer 1 op de punt van vlam F3. Dat is één selout-pixel op een vlampunt van 1 px en geen om-en-om-rand. |
| Schaduw | voldoet | Licht komt van linksboven. De schaduw ligt als sikkel rechts en onder: op de bil is de terracotta (3) 1 px breed bij r35 en 4 px breed bij r44, dus hij volgt de bolling. De verre achterpoot staat in de donkere tint E. Onder de kin en de borst valt slagschaduw op de bef en de buik (6). |
| Banding | voldoet, net | De bil rechts heeft een 4-lijn van 1–2 px breed op x43–44 (r34–49). Alleen in r35–36 staat 5‑4‑3‑1 als vier lagen van 1 px. Verder verbreedt de 3-band, zodat de grenzen niet parallel lopen. Raticate en Taillow hebben dezelfde tussentint. Dit is geen afkeur. |
| Pillow shading | voldoet | Geen enkel vlak is rondom donker. Kop, voorpoten en rug zijn tot de lijn licht. |
| Tintvlakjes < 3 px | voldoet | Volgens controle.py zijn er 31 clusters, en die hebben allemaal een functie: teenlijntjes, dijlijn (37–39,38–40), oogglans (16,30), sikkelpunt, oorrand (20,20–21) en crème tussen de snorharen ((8,35–36), (14,37), (10–11,38)). Ruis zit er niet bij. |
| Contrast | voldoet | Luminantie per stap: lijf 5→4→3→2→1 = 26 / 22 / 42 / 76; crème 7→6 = 35; geel A→9→8 = 36 / 54; staart C→B = 39. Het lijf zit iets onder Taillow (30–40) en gelijk aan de goedgekeurde poedellarve (25/22). Aandeel omlijning: 0,19, binnen de band (E3). |
| Kleurgroepen | voldoet | 16 kleuren. Per groep ≤ 3 tinten + omlijning, en de tinten zijn gemeten op het model. |
| Leesbaarheid 1× | voldoet | Op licht en donker naast de vijf Gen 3-sprites leest hij als knaagdier met gele pluim, sikkel en snorharen. Kop, oor, oog en pluim zijn als vorm te zien. De snorharen (F) blijven op donker zichtbaar, net als bij Raticate. |
| Gen 3-gevoel naast de referenties | voldoet | Dichtheid, lijndikte en kleurgebruik passen tussen Sandshrew en Raticate. |

## Ter info voor Jordi (ontwerp/model, geen reparatie)
- De bovenkant van de rug (x33–40, r29) is een recht stuk van 8 px. Op 64 px is het model daar ook vlak (zie `viscacha.png.keuring.md`). Een boller ruglijntje kan alleen via het bevroren silhouet.
- De staart heeft een lichte rand rechts (59–60,33–36) en een donkerbruine binnenkant. Het licht staat daar dus andersom dan op de rest van het lijf. Het model doet dat ook (tekening van de vacht, randlicht).
- Het lijf heeft geen hooglichttint, alleen basis 5 en schaduw 4/3, net als het model. De Dragonfly Cave-gids raadt voor de R/S-stijl meer hooglicht aan.
- De verre voorpoot is even licht als de nabije. Dat volgt het model, maar checklist E1 (richtlijn) vraagt om een donkere verre kant.

## Reparaties
Geen.

Oordeel: PASS
