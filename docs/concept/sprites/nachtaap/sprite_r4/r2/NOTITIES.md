# Nocticue r2 (vanaf r1): benoemde reparaties

Script `bewerk2.py` (start van `r1/anim_front.png`; elke pixel met zone en reden). **Alpha-diff met r1 = 0** (scriptuitvoer). Alleen tinten uit het bestaande palet binnen bestaande vlakken; niets getekend. Studie vooraf: oude sprite en Teddiursa op 8× (middentoon, licht linksboven, 1–2 px donkerder sikkel rechts/onder binnen de lijn).

| Zone | px | Wat |
|---|---|---|
| kop sikkel | 27 | 4 → 3 langs de rechter-/onderkant: 1 px bovenaan (y22–24), 2 px lager (y31–39), langs de oorovergang x35 (y25–28) |
| oor R sikkel | 6 | rechterrand oor 4 → 3 ((41,26–30), (40,30)) |
| kop wang | 5 | lichte 5-plek rechts naast de snuit lag in de schaduwkant → 4 |
| gezichtsschijf | 14 | smalle crème schaduw 7 → 6 langs de rechterrand van de schijf (x32–34, y25–35) en rechtsonder (30,36), (29–30,37); onderrand had al 6 uit het model |
| arm R (nabij) | 8 | rechterkolom x33 (y42–49) 5 → 4; linkerkolom blijft 5 (lichtkant) |
| romp R | 5 | (36–37,47–48), (36,49) 4 → 3, sluit aan op de 3 erboven/eronder |
| arm L (ver) | 5 | (22,44–46), (21,47–48) 5 → 4: iets donkerder dan de lichtkant van de nabije arm |
| buik | 0 | sikkel rechts (x30, 6) en onder (y50–51, 6) zat al in het model |
| voet L | 2 | dambord opgeheven: (20,53) 7 → D, (19,53) D → 7: verticale teenlijn x20 (y52–53) zoals de rechtervoet |
| streep | 1 | (24,28) 3 → 4: trapje y28→y29 zachter; streep blijft 3 px, twee tinten |
| staart, ogen, mond, silhouet | 0 | ongewijzigd |
| **totaal** | **73** | |

Controle: 14 kleuren + transparant, geen lichte kleur op de buitenrand, geen tintvlakjes < 3 px, geen losse omlijning (`r1/controle.py r2/anim_front.png`).

Zwakke punten: de crème schaduw langs de schijfrand is 1 px (bewust smal); de wang rechtsonder is nu 4 tussen 3 en de crème schaduw, wat een klein tussenvlak geeft. Verder zie ik niets.
