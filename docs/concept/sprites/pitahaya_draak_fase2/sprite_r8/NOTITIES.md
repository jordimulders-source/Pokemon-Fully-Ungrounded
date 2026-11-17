# Pitahaya-draak fase 2, sprite r8 (maker): diagonale binnenrand links

Jordi (letterlijk): "wacht, de vorm van de bek klopt ook niet. Ik heb vier pixels ingestipt, wat als die weggehaald worden om de binnenkant wat diagonaler te maken? Zoals in het model" · "en dan de rest netjes bijkleuren"

Op `pitahaya2_r7A.png` en `pitahaya2_r7B.png`. Script `maak_r8.py` → `pitahaya2_r8A.png` en `pitahaya2_r8B.png`. Vel: `vel8.py` → `vel.png`.
- Het vel toont de bek op 12× (model | r7A | r8A | r8B), de hele sprite op 8× (A | B), en 1× en 2× op licht en donker.
- Afwijkingen per pixel: `pitahaya2_r8A_afwijkingen.txt` en `pitahaya2_r8B_afwijkingen.txt`. A en B hebben dezelfde 10 px.

## Meting van de stippen
Op `feedback/jordi_r7_vier_pixels.png` is 1 spritepixel 11,6 schermpixels. Geijkt op de pit (11,44) en de zwarte kaaklijn (14–16,44). De stippen staan op:
- (9,45) r;
- (9,46) d;
- (9,47) d;
- (10,46) v.

Dat is gelijk aan de meting van Claude.

## Wijzigingen (10 px)
- **Jordi: 4 px transparant.** Het silhouet verandert alleen hier (assert).
- **Rand dicht, bovenkant van de V (3 px), zwart:** (9,44) r→K, (10,45) v→K en de punt (11,46) v→K.
  - Dit is de onderkant van de bovenkaak, de schaduwkant.
  - Model: de zwarte lijn loopt van de tweede tand schuin naar rechtsonder (natief nx 29–30, ny 91–95). Croconaw en Gyarados hebben ook een zwarte bekrand onder de bovenkaak.
- **Onderkant van de V (1 px), selout:** (9,48) p→r. De bovenkant van de lipband is de lichtkant. Daar hoort de selout van de lipband (r, zoals keuring_r2 voorschreef), en geen lichte tint op de rand. (10,47) r stond al goed.
- **Pit 1 px naar rechts:** (10,48) s→W en (11,48) W→s.
  - Op (10,48) lag de pit tegen de nieuwe rand en las hij als een verdikking van de lijn.
  - Het is dezelfde modelpit (component 913). Hij ligt precies op de grens X10|X11: blok X10 heeft 3 pitpixels in de rechterkolom, blok X11 3 in de linkerkolom.

**Bewijs (asserts):**
- alle wijzigingen liggen in de bekzone, dus buiten de zone is de diff met r7 **0**;
- het silhouet verandert alleen op de 4 gestipte pixels;
- elke figuurpixel naast transparant in de bek is lijn of selout (een tand mag ook);
- er is geen dambord in x 6–13. De bekende lijn-tegen-vulling bij de mondhoek (16,43)/(17,44) zit er nog, zoals in keuring_r5.

## Zelf getoetst
- **12× en 2×:** de linkerrand loopt nu als V-insnijding schuin van de tweede tand naar de punt (11,46), en weer terug naar de lipband. Dat is de vorm van de insnijding in het model (natief nx 27–28, ny 96–104 achtergrond). Op 2× leest de bek daardoor ruimer en schuiner.
- **Lipband en tong:** die sluiten aan zonder gat.
- **Zwak:** (10,44) is in A nog één v-pixel en in B één pixel van de donkerste tint. Hij ligt tussen de zwarte lijn, de pit (11,44) en de nieuwe rand (10,45). Via (11,45) hangt hij alleen diagonaal aan de wig vast. Weghalen zou de wig nog kleiner maken; dat heb ik niet gedaan.
- Wig en plooi worden door de nieuwe rand 1 px smaller aan de linkerkant: (10,45) en (11,46) zijn nu lijn.
