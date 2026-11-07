# Potoo kleur r5: benoemde reparaties van de coördinator

Basis r4; alleen de zones in `wijzig_r5.py` (`ZONES`, `KUIF`) zijn veranderd. Bouwen: `python3 bouw.py && python3 diff.py && python3 palet.py && python3 controle.py && python3 vel.py ../kleur_r4/potoo.png`.
Bewijs bevriezing: `diff_uitvoer.txt`: 302 px gewijzigd, 0 buiten de zones. De oogzone is x29-38 (de ring raakt (38,9), dat door de ring een losse pixel werd).

1. **Vleugel:** voorrand in 2 van de schouder (35,28) tot de punt (40,47) (gemeten 28-120); dekveren crème/wit met spitse donkere puntjes in 3 (V met punt (40,33); (42,30-31), (43,34), (38,35)); binnenrand van de handpennen in 3 (39-40,38-39) -> (41-42,40-41) -> (43,42-44) (gemeten 84-161 met p15 4-46); witte handpenstrook x41 y37-39 en x43 y37-41, rand x44 in 5 (gemeten 150-175).
2. **Borst:** schoon wit; 3 rijen V-lijnen in middengrijs 4 op de gemeten lijnpixels (modelpixels L 110-195, kaart in NOTITIES-meting): A (21-23,28) -> punt (24-27,31) -> (31,28); B (23-24,35) -> (26-27,37) -> (29-30,35); C (23,40) -> (24-27,41) -> (28,40) en (33-34,40). Losse streepjes in 2 alleen waar het model donker is (L<80): (25,29)+(24,30), (31-32,33), (34,36-37), (31,38), (25,39), (33,40), (28,41-42), (30,41), (30,44), (34,44-45).
3. **Schaduw:** één sikkel in 6 onderaan de buik y42-46 (model 174-198); geen vlekken erboven.
4. **Klauwen:** teen A (28,49-50) en teen B (31-32,48), (30-32,49), (31,50-51) crème 7/8 met zwarte omtrek; verre teen C (34,48-49), (35,49-50) hoger/achter in 5.
5. **Oog:** ring 1 px in 5: boven (31-35,4) en (30,5), (36,5-6), links (29,7-10), rechts (37,7-10), onder (30,11), (36,11), (30-31,12), (32-35,12). Glans 2x2 wit op (33-34,6-7) (gemeten glanscentrum (34,3; 7,1)).
6. **Staart:** naar de meting: rand x44 zwart (model 64-100), pennen x42-43 y48-54 en x40-42 y55-62 licht, scheidingen x41 y48-50, x42 y51-53, x39 y55-58, (40,60). Vlakvergelijk staartblokken nu +11/+3/-7 (was +19..+25).
7. **Kuif (pixels buiten het silhouet, met de hand):** (24,1) alpha 0,30 L130; (27,1) 0,41 L160; (23,2) 0,34 L140; (39,3) 0,43 L130; slierten rechts (42,7) 0,44 L140, (45,8) 0,30 L130, (44,10) 0,31 L130, (45,10) 0,20 L130, (43,11) 0,34 L140, (44,11) 0,38 L130. Allemaal 4 (grijs, lijnkleur), elk vast aan de omtrek.

Controle (`controle_uitvoer.txt`): alpha-diff 13 (de 10 kuifpixels hierboven + (43,8), (27,49), (27,50) uit eerdere rondes), open randen 0, losse pixels 0, clusters 0, 12 kleuren.

Zwakke punten (naar r6): vleugeldekveren nog druk (veel 6/5 tussen de crème); witte handpenstrook is te kort (model loopt x41 van y36 tot y47 door).
