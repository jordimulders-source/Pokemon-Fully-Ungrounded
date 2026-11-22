# Nocticue r4 (vanaf r3): reparaties 1–8 uit `r3/eindkeuring/EINDKEURING.md`

`bewerk4.py` past elke pixel als lijst toe en controleert eerst de 'van'-index; frame 1 en 2 gelijk.
Bewijs (scriptuitvoer): alpha-diff met r3 = 0; 48 px gewijzigd per frame (96 in beide), allemaal uit de lijst; diff buiten de lijst = 0; alle 'van'-indexen klopten.

| # | Zone | px |
|---|---|---|
| 1 | armen: rechts x32 y42–48 5→4; links (23,42),(23,43),(22,44–46),(21,47–48) 4→5, (23,44),(22,47) 3→4 | 16 |
| 2 | voetstrook (21–24,54) 5→3 | 4 |
| 3 | staartkrul (49,35–38) 5→4 | 4 |
| 4 | binnenlijnen romp x34 y43–48 en x31 y43–47 1→2 (x31 y42/y48 en x34 y42/y49 blijven zwart) | 11 |
| 5 | verre oog: (17,31) B→E, (17,32) 9→E, (17,33) 9→A, (18,33) B→A, (18,34) 9→B | 5 |
| 6 | linkerkoprand (14,30),(15,31),(16,32) 1→2 | 3 |
| 7 | rechterwang (33,32),(32,33),(29,36),(28,37) 7→6 | 4 |
| 8 | nabije oog (27,31) B→E | 1 |
| | **totaal** | **48** |

Punten 9–10 (laag) niet toegepast, zoals gevraagd.

## Controle (`r1/controle.py r4/anim_front.png`)
13 kleuren + transparant (8 wordt niet meer gebruikt), geen lichte kleur op de buitenrand, geen losse omlijning.
Nieuw door de reparaties, niet zelf aangepast (de keuring wilde ze zo):
- verre arm: (23,44) en (22,47) zijn nu losse 4-pixels tussen 5 en de lijn (overgang naar de schaduwkant);
- nabije arm x32–33 is nu volledig 4, zonder hooglicht (alleen de knie (31–32,49–50) blijft 5).
- In de lengterichting van de romp ontstaat geen banding meer: van x31 tot x37 loopt het nu 2-4-4-2-4-3-3.
Al bestaande 1-px vlakjes (punten 9–10 van de keuring): (24,28) 4 in de streep, (29,38),(28,39) 4 bij de kin, (35,47–48) 4 aan de rompzijde.
