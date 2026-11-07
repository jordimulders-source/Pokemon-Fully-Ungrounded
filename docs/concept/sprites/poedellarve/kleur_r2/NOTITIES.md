# Poedellarve: kleur r2

Vanaf r1f, met de benoemde reparaties van de coördinator. De eindstand is `stappen/r2.txt` (met de hand per rij). Het vel toont r2 | r1 | model op 8×.

Bouwen:
1. `python3 stappen/bouw.py stappen/r2.txt raster.txt`
2. `python3 palet.py`
3. `python3 controle.py`
4. `python3 vel.py ../kleur_r1/poedellarve.png`

## Reparaties
1. **Gezicht**
   - **Oog:** gemeten op het model, x 41,1–44,2 en y 45,5–48,9, donker vlak plus rand. Het nieuwe oog is 4×4 en komt pixel voor pixel van het rechteroog van Pichu (`graphics/pokemon/pichu/anim_front_gba.png`, x 32–35, y 27–30), horizontaal gespiegeld. Daardoor staat de glans rechtsboven, zoals in het model (x 42,75–43,25): glans wit op (43,46), reflectie op (42,47), de grijze ooglidrand van Pichu in 3 op (44,46)/(44,47).
   - **Oogvlek:** opnieuw gezet als ronde vorm op de gemeten beigeplek (beige-fractie per pixel). Bovenkant x 41–44 op rij 44, links x 39 op rij 46–50 en x 38 op rij 50–51, rechts tot x 49. De onderrand op rij 51 en de kin op rij 52 staan in 8, als schaduwsikkel.
   - **Neus:** 2 px zwart op (47,48)/(48,48).
   - **Mond:** een korte curve in 2: (45,49), (46,50), (47,50) en (48,49). (48,49) sluit aan op de neus, zoals het steeltje in het model.
   - **Verre oog:** ongewijzigd: donker, half achter de snuit, met de glans in 7.
2. **Kop als bal**
   - **Binnenlijn links van de kop:** x32 rij 45–46 in 5, rij 47–53 in 4, (33,54) in 4. Hij loopt door in de borstrand (35–38,56) in 3. Gemeten: px.py op x32 gaf 150–200.
   - **Kinlijn:** (40,51)–(48,51) in 3 en loopt taps naar (39,51) in 4.
   - **Schaduw aan de binnenkant:** 7 langs x33 (rij 44–46 en 49–53) en (34,53)/(34,54).
3. **Sprieten**
   - **Linkerkrul:** C-ring: wit (35,34), donkere holte (36,34) in 1, het licht haakpuntje (37,34) in 7. Daarvoor is **alpha +1: (38,34)** nodig, als buitenlijn rechts van het puntje; in het model ligt de haakrand op x 37,6–38.
   - **Rechterspiraal:** een lichte ring om het donkere middelpunt (48,35) met een armpje (48,36) in 3. In het model krult de rechterspriet naar binnen (links); dat heb ik gevolgd.
   - **Ribbels:** per spriet hooguit 2 dwarsstreepjes in 4. Links (37,36)/(36,37) en (39,37)/(38,38); rechts (50,37)/(49,38). Geen dambord.
4. **Segmenten**
   - **Naden:** "(", bol naar links, die onderaan naar rechts uitzwaaien, zoals het model:
     - S1/S2: x19 rij 50–55, daarna (20,56) en (20,57);
     - S2/S3: (25,47)/(24,48), x24 rij 49–53, daarna (25,54), (25,55), (26,56) en (27,57);
     - S3/S4: x28 rij 46–51, daarna (29,52), (29,53), (30,54) en (31,55).
   - **Toon:** licht bovenaan (6/5), donker onderaan (4/3).
   - **Schaduwsikkel per segment:** rechtsonder, waar het segment onder het volgende valt. In 7: S1 x18 rij 53–55, S2 x23 rij 53–55, S3 x27–28 rij 52–55, S4 x31 rij 51–54. De bovenkant is wit, het licht valt van linksboven. Onderaan liggen 6 (rij 56–57) en de donkere rand 4, met 3 onder de naden, zodat elke onderkant per segment iets bol leest.
5. **Bolletjes en pootjes**
   - **Bolletje 2:** **alpha −1: (20,46)**, de hoek afgerond. Licht boven (A), 7 eronder, scheiding in 3 op rij 49.
   - **Bolletje 3:** **alpha +1: (28,44)**. Het model is daar 2,2 px breed (x 26,3–28,5); nu is er binnen plaats voor een lichte bovenkant.
   - **Bolletje 4:** **alpha −1: (33,39)**. Het modelbolletje begint op y 39,9; de punt is weg, de top is rond met selout in 3.
   - **Achterpootjes:** drie aparte ronde lobben (licht boven, donkerder onder), met 3/4 ertussen. De verste is donkerder.
   - **Nabije voorpoot:** twee ronde lobben met een licht midden en schaduw rechtsonder, gescheiden door een 3-lijn op rij 57.
   - **Verre voorpoot:** licht bovenaan (35–39, 57–59), met een sikkel naar linksonder.
6. **Kijkrichting:** naar rechts, zoals het model.

Zo gelaten, zoals gevraagd: de glans van het verre oog, de selout in 3 en het weglaten van de dambordtextuur.

## Alpha-wijzigingen (totaal 4, alleen dunne delen en bolletjes)
- +(38,34): linkerkrul, buitenlijn naast het haakpuntje.
- +(28,44): bolletje 3.
- −(33,39): bolletje 4.
- −(20,46): bolletje 2.

## Controle (`controle_uitvoer.txt`)
- alpha-diff 4: precies de vier hierboven, de rest is gelijk aan het silhouet;
- open randen 0, losse pixels 0, tintclusters < 3 px 0;
- selout 3 in 5 reeksen van 3–8 px;
- 10 kleuren + transparant.
- Uitzonderingen als lijnwerk: `spriet_zone.txt`, `naden.txt`, en de oogglansen (43,46) en (49,46).

## Zelfgenoemde zwakke punten
Gerepareerd in deze ronde:
- de 7-schaduw liep eerst over de hele hoogte naast elke naad en las als een dubbele lijn; nu is het alleen een sikkel onderaan;
- een eerste krul met +(36,32) stak als een spijker omhoog; vervangen door +(38,34).

Nog open:
1. **Naden:** de bovenste helft blijft nog grotendeels verticaal (x19 en x24 elk 5–6 rijen recht), omdat het model daar ook bijna recht is (x 19,7–20,3). Meer bolling zou van het model afwijken.
2. **Onderkant:** de onderkant van de segmenten is maar licht bol. De silhouetonderrand is op rij 58 recht, dus de bolling komt alleen uit de toon (3 onder de naden).
3. **Bolletje 1 (x17–18):** blijft een heel klein nubje van 2×1 binnen. Dat is in het model ook zo, maar het leest op 1× nauwelijks als balletje.
4. **Krullen:** op 1× zijn het kleine knopjes; op 8× lezen ze als krul en spiraal.
