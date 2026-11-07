# Poedelmot: kleur r19

Vanaf r18 (`stappen/basis.txt`). Stap: `python3 apply.py basis.txt ../raster.txt r19` (in `stappen/`), daarna `palet.py`, `controle.py` en `vel.py`. Er zijn 143 px gewijzigd. Elk punt is eerst gemeten met `stappen/px.py` (gem/p15/max van de modelhelderheid per spritepixel).

## Top-5 van de keuring r18
1. **Sprietnerf:**
   - Per kolom gemeten (lichtste band in het model). Links: x10–12 y20,5, x14 22,2, x16 23,8, x18 25,3. Rechts: x34 23,6, x36 22,5, x38–40 20,9, x42 20,5, x44 20, x47–50 19,1.
   - De oude nerf lag 1–2 px te laag. De keurder had gelijk.
   - Nerf nu als boog: links (4–5,18), (6–8,19), (9–11,20), (12–13,21), (14,22), (15–16,23), (17,24), (18,25), (19,26). Rechts (30,27), (31,26), (32,25), (33,24), (34–35,23), (36–37,22), (38–41,21), (42–45,20), (46–51,19).
   - Baardjes opnieuw volgens dezelfde regel (steil, periode 3, geen streep naast de nerf of op de rand).
   - Nerfkleur C nu (214,192,160): het model meet (211,188,158). Het was wit (240,232,208).
2. **Ooglichten:**
   - Links: het model meet (17,34–35) donker (91/49) en (18,34) licht (206). Glans nu op (18,34–35).
   - Rechts: het model meet (27–28,34) donker (52/40) en (27,35) 240, (28,35) 152, (27,36) 185. Glans nu op die drie.
   - `controle.py` GLANS is bijgewerkt.
3. **Ring rechteroog:** het model meet x32 y34–37 161–163 en x33 y35–36 117/129. x32 staat nu in 6, x33 y35–36 in 4. Het oog is 1 px smaller.
4. **Kraag y43:**
   - Het model meet hier wit (212–248), met één tan streek (23,43) 179.
   - y43 x20–35 is nu A, en de losse 7-tanden op y44–45 zijn weg.
   - Haarstreken in 7 op de modelplekken: (22–23,43)+(22,44); (32,44–46); (35,44–45)+(36,45–46); (18,45).
   - Kin en snuit: (18–19,41) en (20,40) licht (model 209/206/248), (26,42) 7 (202), (25–26,41) 3 (129/112). Snuit y39 x20–24 en (24,40) in 7 (model 207–216).
5. **Losse lijnpixels:**
   - (59–60,24) naar D, (58–59,29) naar A, (54,37) naar A, (12,29) naar 7 (model 222–245).
   - Pootlijnen: (30,48) 195 naar 9, (35,48) 187 naar 7, (29,53) 157 naar 7 (de lijn ligt op (30,53), 69), (46,56) 159 naar D (de buitenlijn (47,56) blijft).
   - **Naadstomp, opnieuw gemeten:** (39,35) 204 en (40,35) 215 zijn licht. Daar had de keurder gelijk; in r18 maakte ik die ten onrechte zwart. Ze staan nu in 7. (38–41,34) meet 135/77/74/115 met p15 2–5: dat is donker en blijft zwart. De naad loopt nu over y34 tot x41 en dan over y35 vanaf x41, zoals de keurder beschrijft.

## Controle
Alpha-diff 0, open randen 0, losse pixels 0, clusters < 3 px 0, 13 kleuren.

## Zwakke punten
Op 8× en op 1× naast het model zie ik er geen. Op de lijnkaart (`stappen/lijnkaart_r19.png`) staan nog verschillen bij de baardjes (de modelperiode van ±1,5 px is te fijn voor 64 px) en bij de selout 4 en de klauwteentjes in 4 (bewust).
