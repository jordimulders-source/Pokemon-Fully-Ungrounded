# Onweerswolk-Altaria frontsprite, ronde 10 (alleen de kop, vanaf r9)

Jordi (21 nov, over r9): "het gezicht klopt helemaal nog niet.. Linksonderin valt die helemaal weg, het linkeroog is niet goed te zien, rechts is een volledige rechte lijn. Sowieso klopt het gezicht in het model niet, daar mag je vanaf wijken, baseer je op de echte altaria, de wolken zijn nu goed gelukt".

Bouwen vanuit `altaria/`: `python3 sprite_r10/bouw.py && python3 sprite_r10/vel.py`.
Bestanden: `altaria_r10.png` (14 kleuren incl. transparant, palet = r9), `altaria_r10_8x.png` (wit), `vel.png` (r10 | r9 | echte Altaria op 8×; kop 20× naast de echte Altaria-kop; 1× op wit/crème/grijsblauw/zwart), `bouw.py`, `vel.py`, `kz.py` (kop-close-up r10 | echte Altaria met coördinaten).

## Bevroren
Diff r10 ↔ r9 = 85 px, allemaal in de kopzone X19–34, Y18–27 (assert in `bouw.py`). Wolk, static, vleugels, hals (Y≥28) en kuif zijn diff 0.

## Methode (Gengas: overnemen, niet tekenen)
1. Kop van de echte Gen 3-Altaria (`graphics/pokemon/altaria/anim_front.png`, bovenste 64×64, X20–36, Y13–24) pixel voor pixel overgenomen. Naar onze kopmaat door hele rijen en kolommen te schrappen: rijen Y16 en Y17 (herhaling in de schedel), kolommen X28 (voorhoofd tussen de ogen) en X34 (zijkant). Daarna geplaatst op X19, Y18.
2. Omgekleurd per kleurlaag: Altaria-hooglicht (152,216,248) → violet hooglicht 12, basis (88,192,248) → violet licht 11, schaduw (16,152,200) → violet midden 10, selout/zwart → violet-selout 8. Het wit van de snuit- en wangpluis → licht cyaan 6, de lichte grijzen (216/168) → teal 5, de pluisschaduw (112,112,152) → donker teal 4, de pluisrand → wolk-selout 2. Pupillen blijven zwart (1), oogwit en glans → lavendelwit 13.
3. Reparaties per pixel (`KOPGRID`), steeds naar de opbouw van Altaria:
   - **Ver oog:** Altaria heeft zijn verre oog direct tegen de rand en de snuitlijn. Hier staat het op (22,22–23), met kopkleur links (21,22–23), oogwit erboven (22,21) en kopkleur rechts. De snuitbovenlijn staat 1 rij lager (Y23 violet midden, X24–27) in plaats van tegen het oog.
   - **Nabij oog:** 2×2 op (28–29,22–23), glans rechtsboven (29,22), zoals Altaria.
   - **Schedel:** hooglicht linksboven (Y19–20, X23–27). De bovenrand is violet midden, zoals Altaria's blauwe schaduwrand; aan de rechterkant violet-selout.
   - **Rechterkant:** niet meer 7 rijen recht. Nu X33 over Y20–24 (5 rijen, net als Altaria's rechterrand), daarna diagonaal (32,25), (31,26), (30,27). Ernaast zit violet midden als schaduwsikkel (32,23–24).
   - **Snuitpluis links / kin:** de pluis X20–26, Y24–27 is cyaan met teal schaduw. De rand tegen de wolk loopt als diagonaal in wolk-selout (19,24), (20,25), (21,26), (22,27), aansluitend op de bestaande selout (19,25–26) en (22–23,28). Zo valt de kop linksonder niet meer weg.
   - **Wangpluis rechts:** (29–31,25) en (28–30,26), van de snuit gescheiden door donker teal (28,25) en (27,26), zoals Altaria's grijze scheiding.
   - **Kin/hals:** (26–27,27) violet-selout als kinlijn boven de hals, zoals Altaria's (27–28,24).

## Alpha (alleen kopzone)
- Erbij: (33,20).
- Weg: (23,18), (24,18), (31,18), (22,19), (21,20) (ronde schedel) en (33,25), (32,26), (33,26), (31,27), (32,27), (33,27) (ronde rechteronderkant).
- Kuif niet aangeraakt: de stengel (24,17) sluit nu diagonaal aan op (25,18).

## Controle
14 kleuren incl. transparant; zwart alleen de 5 pupilpixels (22,22) (22,23) (28,22) (28,23) (29,23); kop in 3 violettinten + violet-selout.

## Eerlijke twijfels
- De pluis heeft dezelfde cyaan als de wolkkappen. Op 1× scheidt alleen de selout-diagonaal hem van de wolk links.
- Het verre oog staat 1 px van de rand. Op 8× leest het, op 1× is het klein (net als bij Altaria zelf).
- De bovenkant van de kop is vrij vlak, omdat de kuifstengels er direct op staan.
