# Hoatzin fase 2, r9 (19 nov), maker: eerste Gen 3-kleurronde op r8

Op r8 (`r8.png` = r8 P2 + oog A); kop/kuif (x ≤ 28, y ≤ 27) ongewijzigd, silhouet 0 px anders. `python3 r9.py` (regels per onderdeel),
`vel.py` → `vel.png` = r9 | r8 | model | Pidgeot | Skarmory (8×) + 1×/2×. Studie: `../r8/NOTITIES.md`.

| regel | px |
|---|---|
| R1 buitenlijn: selout (2) aan de lichtkant waar zwart stond / mauve tegen de achtergrond; zwart aan de schaduwkant | 11 |
| R2 waaier: donkere pengrens direct links van elke schacht → per pen licht (schacht) · midden · donkere grens | 22 |
| R3 staart: lichtkant van elke staartveer 1 tint lichter (3) | 28 |
| R4 poten: nabije poot licht 15 met midden 14 aan de schaduwkant; verre poot 14 met donker 2 aan de schaduwkant | 23 |
| R5 lijf: sikkel (1 tint donkerder) langs de onderrand van het lijf | 17 |
| R6 buik: selout lichtkant in de donkerste buiktint (11) | 9 |
| **totaal t.o.v. r8** | 108 (regels overlappen deels) |

## Eerlijk oordeel
Kleine stap: buitenlijn, staart, poten en buik zijn Gen 3-achtiger, maar de **waaier heeft nog geen pennen als eigen vormen**. De pennen
liggen in het model als ±2 px brede banden zonder bruikbare segmentatie (de r4-pensegmentatie valt in 154 stukjes). Voor echte pennen
(licht/midden/donker per pen, eigen punt) is per pen een vorm nodig: voorstel om de 7–8 pennen van de waaier als middellijnen op het model
af te lezen (zoals de kuifplukken in r8) en ze als banden van 3 px te rasteren, of een Gemini-model van alleen de vleugel op spritegrootte.
