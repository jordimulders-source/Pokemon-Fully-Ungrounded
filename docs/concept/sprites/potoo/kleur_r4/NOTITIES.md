# Potoo kleur r4

Vanaf r3 (`rijen_r4.py`; rijen 25-42 opnieuw gezet, losse handwijzigingen `W` onderaan). Bouwen: `python3 bouw.py rijen_r4.py && python3 palet.py && python3 controle.py && python3 vel.py ../kleur_r3/potoo.png`.

Wijzigingen (alles gemeten met `gereedschap/lgrid.py` en `afwijking.py`):
- **Borst x21-35 y27-42 naar de meting:** de periode-3-zigzaglijnen van r1-r3 bestonden op 64 px niet in het model (fijnere zigzag dan het spriteraster). Nu: wit waar het model >= 232 is, crème 7 bij 205-231, grijs 6 bij 175-204, 5 bij 140-174; de grijze V-vlekken zitten waar het model ze heeft (band A x25-31 y29-31, band B x23-29 y35-37), spikkels op de gemeten donkere plekken (24-25,29-32), (31,33), (34,36), (31,38), (25,39), (30,41), (31,42), (28,41-42) en (35,39) (p15 3-50). Overal clusters >= 3 px; banding van r3 weg.
- **Vleugelrand:** begint op y28 (y25-27 model 146-179, geen lijn: nu 6), loopt y36 x36-38, y37 x37-38, y38-39 x38, y40-42 x39 (model 41-105); links ervan 5 (model 128-130).
- **Kuifplukken rechts** (42,8), (42,9), (43,10): 4 i.p.v. zwart (model 148-158, geen zwart).
- **Muilrand:** bovenaan (36,14) 5 en (35,15) 6 (model 124/144), (30,19) 6, einde (24,23) 5 en (25,23) 3 (model 141/95).
- **Tenen:** smalle witte strepen (28,49-50), (30-31,49) in 7 (model 110-137); (32,49) en (31,50) blijven 8 (190/189).
- (42,30) 4 (vleugelveerscheiding, model 144/9), (42,41) 4 (model 83).

Controle (`controle_uitvoer.txt`): alpha-diff 3 (alle gemotiveerd: (43,8) kuifpluk, model grijs, alpha 0,38; (27,49) en (27,50) teenomtrek, model alpha 0,24/0,29), open randen 0, losse pixels 0, clusters < 3 px 0, 12 kleuren + transparant.
Meting: `afwijking_90.txt` 22 px > 90 verschil (vooral buitenlijn en glans, zie hieronder). `box1x_r4.png`: model op 1× | sprite.

Bewuste keuzes (Gen 3-eisen):
- Glans 2 px verticaal (34,6)-(34,7); het model meet (34,7) 220 en (34,6) 110 (halve glans).
- Buitenlijn: zwart rechts/onder; lichtkant (borst links) 2, kuif linksboven en kruin 3/4, muilrand links 9. Het model heeft rondom zwart.

Wat nog afwijkt van het model (eerlijk):
- Staart x40-43 y40-59 is per 4x4-blok 19-25 lichter dan het model (`gereedschap/vlakvergelijk.py`): de donkere veerscheidingen in de staart zijn smaller dan in het model.
- Op 8× zijn de chevrons zachte grijze V-vlekken; het model toont scherpe zigzaglijnen, die op 64 px niet passen (op 1× klopt het, zie box1x).
- Kuif bovenop: het model heeft witte spitse plukjes boven de kruin; het bevroren silhouet heeft alleen (26,1) en (28,1), dus de kruin leest als een gladde rand.
- Haaksnavel is op 64 px een klein donker punt (x17-21); de grijze snavelrug van het model is maar 1-2 px (19,7), (21,6-7).
- Oog: schijf 7 px, iets kleiner ogend dan het model door de dunne grijze oogrand die het model eromheen heeft.
- Vlak (20-23, y20-23): sprite 13-28 lichter/donkerder per blok, binnen de ruis van de muilvormen.
