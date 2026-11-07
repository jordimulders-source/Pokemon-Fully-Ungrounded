# Poedelmot: kleur r21

Vanaf r20 (`stappen/basis.txt`). Stap: `python3 apply.py basis.txt ../raster.txt r21` (in `stappen/`), daarna `palet.py`, `controle.py` en `vel.py`. Er zijn 11 px gewijzigd. Gemeten met `stappen/px.py` (gem/p15).

1. **Linkerrand voorvleugel:** (43,29) 139/54, (42,30) 118/12, (41,31) 102/6, (40,32) 87/5 en (40,33) 113/44 staan nu in 4. De lijn sluit aan op (40,34).
   - De witte strook (42,29), (41,30), (40,31), (39,32) blijft wit (model 207–210). (39,33) is ook wit geworden, zodat de strook aansluit op (38,33).
   - De twee nieuwe diagonale strookpixels staan in `krul_lijnen.txt`.
2. **Gat in de naad** (54,36) dicht met 4 (model 153/96).
3. **Middenpoot:** (35,50) staat in 4 (model 90/3). (36,50) ook in 4 (model 110/5), anders bleef er een los 7-pixel over.
4. **Glans linkeroog:** gemeten (18,34) 206/120 (licht) en (18,35) 110/16 (half donker). Ik volg de meting: de glans staat alleen nog op (18,34), en (18,35) staat in 1. GLANS in `controle.py` is bijgewerkt.

Controle: alpha-diff 0, open randen 0, losse pixels 0, clusters < 3 px 0, 14 kleuren. Zwakke punten: geen gezien (1× naast het model: `stappen/box1x_r21.png`).
