# Potoo kleur r3

Vanaf r2 (`rijen_r3.py`, met losse handwijzigingen `W` onderaan). Wijzigingen:
- Kruin x29-33 y2 selout 4 (lichtkant boven) i.p.v. 2.
- Tenen wit: (28,49),(28,50) teen A, (30-32,49),(31,50) teen B. Om teen A wit te kunnen zetten staan (27,49) en (27,50) er als zwarte omtrek bij: het model toont daar de teenomtrek (alpha 0,24 en 0,29, net onder de drempel 0,45). Dunne delen, met de hand.
- Borstband B rechts (x32-35) crème, band C overwegend crème met wit op x27-33 (model).
- Schaduw onder de chevronlijnen 7 i.p.v. 6; donkere lijn boven de muilrand onderaan 9 (model 72-92).
- Hals: vlekje naar (34,21) (gemeten 107), (35-36,21) en (32,22) grijs 4.

Controle (`controle_uitvoer.txt`): alpha-diff 3 ((43,8), (27,49), (27,50), gemotiveerd), open randen 0, losse pixels 0, clusters 0, 12 kleuren.

Zwakke punten (meting `afwijking_90.txt`, `gereedschap/afwijking.py`):
- Chevrons: de zigzaglijnen met periode 3 bestaan op 64 px niet in het model; gemeten zijn het zachte grijze V-vlekken (186-208) tussen wit. Lijnen liggen op (27,29), (32,29), (33,30), (32,36) waar het model wit is (246-249).
- Vleugelrand begint te hoog (35,25-27 model 146-179, geen lijn) en loopt op y36-42 een pixel te ver links.
- Kuifplukken rechts (42,8), (42,9), (43,10) zwart; model grijs 148-158 zonder zwart.
- Muilrand bovenaan (36,14), (35,15) en onderaan (24-25,23) te wit; model 95-144.
