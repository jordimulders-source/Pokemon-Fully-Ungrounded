# Nachtaap fase 3, kleur ronde 3b: lijf (verbeterronde op ronde3_lijf)

Basis: `../ronde3_lijf/nachtaap_fase3.png` (blijft staan). Palet = 1s. Studie en rugstudie: zie `../ronde3_lijf/NOTITIES.md` en `../ronde3_lijf/studie_rug.png`; ze gelden hier ook.
Bestanden: `nachtaap_fase3.png` (= variant 0), `normal.pal`, `lijf.py` (toontabel per rij), `lijf.txt`, `check.py`, `varianten/dij_min1..4.png` + `varianten.py`, `vel.png`, `vel_varianten.png`.

## Opdracht (coördinator) en wat ik deed (88 px t.o.v. ronde3_lijf)
1. **Lichte massa niet plat.** Er is nu een kern van 5 linksboven op schouder en borst. De rand naar 4 is een gebogen grens die de ronding van de borst volgt: r31 tot x34, r32 tot x33, r33 tot x32, r34 x27–31, r35 x27–30, r36 x27–29, r37 x27–28. Daaronder en naar rechts ligt een breed vlak van 4 tot aan de schaduwband (zoals Aipom-back en Primeape: licht bovenaan, middentoon eromheen). Het vlak 5 is van ±60 naar ±40 px gegaan, en er staan geen vlekken.
2. **Healer-bovenarm leesbaar.** De arm is een eigen cilinder: lichte kant x22–24 (5), middentoon x25–26 (4) en daarnaast de lichte borstkern (5). Zo leest de arm boven rij 38 door toonverschil, zonder lijn. Op rij 38–41 staat een korte, zachte scheiding in schaduwtint (x26, 4 px). Daarna komt de oksel (x27–28, r41–45, 3), die in de buikschaduw overgaat. Geen zwart en geen streep over de hele lengte. De schouder (r31–33) blijft één licht vlak waaruit de arm ontspringt (Machamp-back, Vigoroth).
3. **Buik/dij lichter.** De basis van de buik zakt 1–2 rijen lager (r43 tot x35, r44 tot x34, r45 x32–35, r46 x33–35). Daardoor is de grens tussen licht en schaduw een evenaar op één oppervlak, geen band. De 2-pixels langs de linkerdiagonaal van de dij zijn 3 geworden, en de rij 2 boven de buikrand (r45 x28–31) ook. Kleur 2 staat alleen nog direct boven de onderrand van de dij (r52 x39–40/45–46, r53 x41–44).
4. **Vuistarm terug naar 1s.** Vuist, pols en arm tot de schouder zijn gelijk aan 1s. Alleen r31 x23–25 (de schouderovergang) is 5, zodat de arm aansluit op de lichtband.

## Bewijs (`python3 check.py`)
- Alpha-diff met ronde3_lijf: **0**. Met 1s: **0**. Palet = 1s.
- Vuistarm (x0–25 r14–30 + x19–22 r31) tegen 1s: **0 px**.
- Hand + gloed (x4–23, r44–62): **0**. Staart (x44–63, r22–40): **0**. Voeten: **0**. Niet-vachtindexen gewijzigd: **0**.
- In het kopvak alleen (20,33) en (20,34): dat is de healerarm (3→4) naast de kopomlijning op x19. Kop en maan: 0.
- Open randen: geen. In totaal 177 px t.o.v. 1s.

## Dij-varianten (`vel_varianten.png`, 3× en 1× licht/donker; Jordi kiest)
Gemaakt op 3b. De onderrand van de dij gaat omhoog; alleen de omtrek op x34–46 verandert. Onderrand per kolom x33…48:
- 0: 47 48 49 50 51 52 53 53 54 54 54 54 53 53 52 52 (de dij hangt als een zak tot r54)
- −1: 47 48 49 50 50 51 52 52 53 53 53 53 52 53 52 52 (de kniekuil blijft)
- −2: 47 48 49 49 50 50 51 51 52 52 52 52 52 52 52 52 (de dij loopt vloeiend over in het onderbeen)
- −3: 47 48 49 49 49 49 50 50 51 51 51 51 51 52 52 52 (slanke dij, de onderkant buigt licht)
- −4: 47 48 49 49 49 49 50 50 50 50 50 51 51 52 52 52 (dunste dij; **met de hand gladgemaakt**: de deuk bij x37–38 en de trap van 2 px bij x45→46 uit de automatische versie zijn weg, de rand loopt per 1 px)
Elke variant heeft een zwarte onderrand en een rij 2 erboven, en geen open randen.

## Eigen check (1× en 3× naast ronde3_lijf, 1s, het model, Vigoroth, Aipom, Primeape)
- Het blijft één lijf, en de healer-bovenarm leest nu als arm. Op 3× oogt de borst rond in plaats van vlak, en de onderkant oogt minder zwaar. Op 1× is de arm in licht en donker zichtbaar.
- Ik vind dit goed genoeg om op te leveren. Wat ik eerlijk meld (geen zwak punt van deze ronde, maar wel een keuze voor Jordi): de vuistarm staat weer letterlijk als in 1s, dus met zwart boven naast de lichtband en kleur 2 aan de onderkant. Dat is omgekeerd aan de omlijningsregel, maar het is zo goedgekeurd. Wil Jordi het omdraaien, dan staat de omgedraaide versie in `../ronde3_lijf/`.

## Lessen
- Een ledemaat vóór het lijf leest zonder lijn als zijn middentoon naast een lichter lijfvlak ligt (toonverschil). De lijn in schaduwtint is alleen nodig waar beide in de middentoon liggen, en dan kort.
- Een variant met "k px omhoog per kolom" geeft deuken en trapjes waar de oude onderrand al ongelijk was. Zet de eindvariant per kolom met de hand (tabel met de onderrand) en controleer dat de rand per 1 px loopt.
