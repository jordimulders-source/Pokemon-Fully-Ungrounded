# Hauntflare v3 (maker, 15 nov)

Vanaf `../sprite_v2/hauntflare_v2.png`, alleen herkleuren op de plek (`v3.py`; log per pixel in `v3_log.json`; controles `meet.py` -> `meet_uitvoer.txt`; vel `vel.py`).
Diff t.o.v. v2: 210 px, **0 buiten bol/ring/kluwenvak**, 0 op gezicht of buitenrand.

1. Glans: modelpixels met min >= d0 binnen de bol (niet de oude modelogen), voorwaarts afgebeeld (>= 50 % dekking) -> glans f9ccd8, behalve onder gezichtspixels. Het gat x19-21,y20-24 is bol/glans (al in v2 opaak).
2. Oogcontrast: bolpixels 8/9 naast een oogwit -> middentint fa76a2 (14 px).
3. Ring: per verticale strook van de band: bovenste px licht, onderste donker, rest midden (strook van 2: midden+donker). Achterkant (boven de middellijn y = 39 - 8x/59) binnen 3 px van bol/kuif een toon donkerder. 149 px; 1 vlekje opgeruimd.
4. Kluwen: (45,25),(45,26) roze -> kuifrood (de kuifpunt van het model), (48,27) donkerrood -> zwart (één ringomlijning).
5. Bol: f9ccd8 buiten de glans -> f8aec2 (34 px), binnen-selout c8435b -> f04482 (12 px), 1-2 px vlekjes -> buurtint. Bol = 3 tinten + glans + selout.

## Eerlijke zwakke punten
- De modelglans ligt vrijwel helemaal onder Haunters smalle oog (x19-23, y20-24); met regel 2 (geen glans naast oogwit) blijft er alleen een klein glansvlak rechtsboven het oog over. De bol oogt daardoor nog steeds vlakker dan het model. Oplossing kan alleen met een keuze van Jordi (gezicht verschuiven of de glans elders laten).
- Rond de ogen staan 7 losse 1-px middentintpixels (regel 2) en één 1-px f8aec2 bij (20,28); bewust, tussen ooglijnen.
- Ring: de strookregel geeft op de schuine stukken kleine trapjes in de lichte bovenrand.
