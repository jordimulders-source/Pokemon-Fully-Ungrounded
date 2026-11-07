# Viscacha frontsprite, kleur ronde 7 (verse maker): gemeten, niet op het oog
Opdracht: het Gemini-model (`referenties/gemini_gekozen_ronde6.png`) heel accuraat namaken op de r6-schaal (`meta.npy`: x = (ox−165)/10,78, y = (oy−86)/10,78 + 14). Enige afwijking: het luie oog (Drowzee, uit r4–r6). Keuring r6: 13 punten.

## Werkwijze
- `stappen/tl.py`: model op spriteschaal; `mg.py` (model + raster), `zij.py` (sprite | model | spritelijnen over het model), `tab.py` (per pixel: onderlaagkleur + donkerfractie + dekking), `meet.py` (maakt `stappen/meting.npz` en `onderlaag.txt`), `vel.py` (keurvel).
- `r7.py`: met de hand per rij/punt (`seg`, `pts`), per onderdeel; start = r6 (`raster_r6.txt`), kop/oren/gezicht/sikkel/bef/voorpoten, lijf, achterpoten, staart en pluim nieuw gezet op gemeten modelpixels; daarna ronde 7b (overal tegen `tab.py` gecontroleerd) en opschonen van kleine tintvlakjes. 699 pixels anders dan r6.
- Palet gemeten met k-means op het model: lijf 5 = (238,184,100) (model 237,184,100), schaduw 4, terracotta 3, crème 6/7, geel 9/A, staart C/B en de snorharen F (model 119,103,88). E (pupil) was bijna gelijk aan 1 en is nu de verre achterpoot (168,100,66; model 165,97,57). De pupil is 1.

## Per onderdeel (meting → sprite)
- **Oor ver:** dekking r15–24, buitenlijn x9 r19–22, rechterrand x12 (r16), x13 (r17–20), x14 (r21–23); terracotta onderin vanaf r21 rechts, r22 vol. Sprite volgt dat.
- **Oor nabij:** brede ronde schelp, top r16 (x23–25), rechterrand x25 (r17) → x26 (r18–21) → x25 (r22–24); donkere ring linksboven (x23–24 r18, x22 r19, x21 r20–21, x20 r22–25), bruin B links/C rechts, lichte rand 4 rechts (x25 r18–21, x24 r22–24), lichte rand 5 links. Onderkant van de ring r25–26.
- **Oog:** Drowzee-lui uit r6 (lid r29, spleet + glans r30, onderlid r31), op het modeloog (x14–19, r29–31). Bewuste afwijking.
- **Neus (Y):** armen (8,34) en (10,34), samen (9,35), steel (9,36–37) in 2. Snuitvoorkant x7 (r34–36), hoek (8,37). Gemeten: armen y 34,5–35, knoop 35,6, steel 35,8–37,4.
- **Mond/kin:** terracotta lip (10–13,37), crème kinnetje (10–11,38), zwart eronder (9,38), (12–14,38), (10–11,39).
- **Snorharen nabij (F):** boven (4–6,35) → (1–3,36) → (0,37); midden (6,36) → (4–5,37) → (2–3,38) → (1,39) → (0,40–41); onder (7,37) → (6,38) → (5,39) → (4,40–41) → (3,42). Pad per modelpixel gemeten (50×-zoom).
- **Snorharen ver (F):** beide vanaf (13,35–36): boven (13–14,35) → (15–17,36) → (18,37) → (19–21,38) → (22,39); onder (13,36) → (14–15,37) → (16–17,38) → (18,39) → (19,40) → (20,41) → (21,42) → (22,43), over de bef.
- **Pluk:** kroontje x5–8, r28–33: punt omhoog (6,28), punt links (5,31), onderkant (7,33); A/9 binnen, 8 rand, 1 onder.
- **Wangsikkel:** volgens `tab.py`: punt (25–27,28–29) met rand erboven, vulling r30 x23–24, r31 x22–23, r32 x20–22, r33 x19–21, r34 x19–20 met kerf (21,34), r35 x19–21, onderpunt (21–22,36–37) en (22,38). Zwart aan de binnenkant, 8 aan de buitenkant; A boven, 9 onder (gemeten: donkerder goud in de onderste helft). Terracotta nek erachter (x22–28, r27–35).
- **Bef:** crème 6 links / 7 rechts; linkerrand (14,38–39) → (15,40–41) → (16,42–43) → (17,44); rechterrand x22, x23 oranje (gemeten: geen lijn); onder het sikkeltje oranje (r37–38 x19–23 zijn 4/5 in het model, niet crème).
- **Voorpoot ver:** terracotta onderarm (14–18,44–46), wantje x12–15 r45–50, rechterrand x16 (r46–47) → x15 (r48–49), teenlijn (14,49).
- **Voorpoot nabij:** voorrand x22 (r44–46) → x21 (r47) → x20 (r48–51); poot x20–24, rechterrand x25 (r48) → x24 (r49–51), onder r52; teenlijn x22.
- **Rug/lijf:** bovenlijn r31 x27–28 → r30 x29–32 → r29 x33–39, vachtpuntje (40,29–30) met kerf (38–39,30); rechterrand x41 (r31) … x46 (r37–38), x47 (r39–40), x48 (r41–43), bilpuntje (49,44), tweede vachtpuntje (44–45,34). Schouderlijn x30 (r40–45) → (28–29,46) → (27–28,47) → (25–26,48). Buikvlek 7 (x31–34, r42–46), crème 6 (x26–35, r46–50) met onderlijn (26–28,49), (29–31,50), (32–36,51). Dijlijn: 4-streepjes (39,38), (38,39), (37,40), dan 2: (37,41), (36,42), x35 r43–48, (36,49).
- **Achterpoot ver (E):** bovenrand = buikonderlijn, linkerrand (26,50) → (27,51) → (28–29,52) → (30–31,53) → (31,54); rechterrand (35,52) → (36,53–54) → (35,55) → (34,56) → (33,57) → (32,58); voet x25–33 r56–59 met teenlijnen x27 en x29.
- **Achterpoot nabij:** dij-onderlijn (37,52) → (38–39,53) → (40–45,54); onderbeen x46–49, rechterrand x50 (r53–61); voet x43–50 r58–62, teenlijnen x46 en x48.
- **Staart:** binnenrand B/1 (52,30) → (53,32) → (54,33) → (55,34–35) → (56,36–37) → (57,38–39) → (56,40–42) → (55,43–44) → (54,45) → (52–53,46) → (47–51,47); buitenrand x59–60 (r30, puntje), x61 (r31–33), x62 (r34–42), x61 (r43–44) … onderrand (47–55,49). Kleuren volgens meting: tan 4 boven, bruine band C, lichte rand 5/4 rechts (r32–38), oranje 3 rechts (r39–47), onderboog B/C boven en 3 onder.
- **Pluim:** 4 slanke vlammen op de gemeten plekken: F1 punt (58–59,14), rand rechts x59 → x57; F2 punt (53–54,16) met zwarte kerf x54 (r17–18); F3 punt (58,20) met kerf x56 (r21–22) en x57 (r20); F4 (50,22) met kerf (51,23). Bruine wig vanaf (53–54,23) breder naar r28. A overheerst, 9 rechts/onder, 8 als rand links/boven, 1 rechts.

## Controle (`controle_uitvoer.txt`)
- Masker (dekking ≥ 0,5): alles gevuld. Buiten het model (dekking < 0,12): 4 randpixels, elk ≤ 0,5 px: (13,17) oorrand, (40,30) vachtpuntje, (45,35) en (48,41) rugrand.
- Open randen: 0. Losse pixels: alleen 5 snorhaarpixels (1-px-lijnen, diagonaal).
- 16 kleuren incl. transparant; png = raster; index 0 transparant.
- Clusters < 3 px: 30, alle in dunne delen (oorrand-lichtlijn, sikkelpunt, vlammen, oogglans, tenen, snuitpuntje, bef tussen de snorharen, dijlijnstreepjes).

## Afvinklijst
- [x] kop, snuitvorm, neus (Y), mond (lip), kin
- [x] oren (ver smal met terracotta, nabij brede ronde schelp met donkere ring)
- [~] oog: bewust lui (Drowzee)
- [x] snorharen beide kanten, langs het gemeten pad
- [x] pluk, wangsikkel (vorm, kerf, punten), bef
- [~] voorpoten: plek en vorm volgens meting; 1 teenlijn per voorpoot (model 2)
- [x] lijf, rugpuntjes, buik, bil, achterpoten met 2 teenlijnen
- [x] staart, pluim (4 vlammen), kleuren gemeten

## Eigen zwakke punten (na 3 eigen rondes: tekenen, 7b-meting, opschonen)
1. **Voorpoten één teenlijn:** het model heeft er twee, maar de wantjes zijn op deze schaal 2–3 px breed binnen de rand; een tweede lijn maakt er een donker blok van. Ter beoordeling.
2. **Pluim:** vorm en plekken kloppen, maar met 8-rand links en 1 rechts is de pluim op 8× wat goudener en blokkeriger dan Gemini's bleke, slanke vlammen (Gemini: A ≈ 2× zoveel als rand; sprite A 28, rand 8: 18).
3. **Fijne vachtlijntjes** van het model (korte streepjes op de rug, (29–30,33), (35,33) en (31,35)) en de lichtere voorhoofdvlek (x10–13, r26–27, gemeten als crème) zijn niet gezet: geen vrije paletkleur en ze worden op 64 px ruis.
4. Oogglans en lid zijn de r6-oplossing; niet opnieuw beoordeeld.
