# Onweerswolk-Altaria frontsprite, ronde 11: kop groter, varianten A en B (vanaf r10)

Jordi (21 nov): "ik denk dat de kop nog wat groter moet, want de vorm is echt raar" · "extra overlap over de wolk heen is ook niet erg".

Bouwen vanuit `altaria/`: `python3 sprite_r11/bouw.py && python3 sprite_r11/vel.py`.
Bestanden: `altaria_r11A.png`, `altaria_r11B.png` (elk 14 kleuren incl. transparant, palet = r9/r10), `altaria_r11A_8x.png`, `altaria_r11B_8x.png` (wit), `vel.png` (A | B | r10 | echte Altaria op 6,25×; koppen 16× naast de echte Altaria-kop; 1× op wit/crème/grijsblauw/zwart), `bouw.py`, `vel.py`.

## Methode (zoals r10, Gengas: overnemen, niet tekenen)
- **A (100 %):** de kop van de echte Gen 3-Altaria (`graphics/pokemon/altaria/anim_front.png`, X20–36, Y13–24 = 17×12) 1-op-1, niets geschrapt; geplaatst op X17–33, Y18–29.
- **B (±117 %):** dezelfde kop, met verdubbelde rijen Y16 (schedel) en Y22 (pluis) en verdubbelde kolommen X26 (schedel/snuit), X28 (tussen de ogen) en X33 (rechterwang) = 20×14; geplaatst op X16–35, Y18–31.
- **Plaats:** Altaria's kin (Y24) ligt direct boven onze bevroren hals, en Altaria's hals (X27–32) valt boven de onze (X24–29). De bovenkant van de kop komt dan op Y18, precies onder de bevroren kuifstengels (Y17, X24–30). **De kuif hoefde niet te schuiven** (diff 0).
- **Kleur per laag:** basis → violet licht 11, hooglicht → violet hooglicht 12, schaduw → violet midden 10. De rand wordt violet-selout 8 waar hij aan de kop grenst, anders wolk-selout 2. Pupillen blijven zwart; oogwit en glans → lavendelwit 13.
- **Pluis (snuit/wang):** het wit → cyaanwit 7 (de lichtste teal; in r10 cyaan 6, dat in de wolkkappen wegviel). Lichtgrijs → cyaan 6 / teal 5, de pluisschaduw → donker teal 4. Pluis die aan lucht of wolk grenst wordt wolk-selout 2, zodat kin en wang een rand hebben tegen de wolk.
- **Verre oog leesbaar:** 3 pixels in de Altaria-bron aangepast vóór de overname: (22,19) en (22,20) naar kopkleur (links van het oog) en (24,20) naar schaduw (de snuitlijn raakt het oog niet meer).

## Bevroren / diff
- Alles buiten de nieuwe kop en de opgeruimde oude kop is gelijk aan r10 (assert).
- **A:** diff met r10 = 129 px. 16 koppixels liggen over wolk/hals. Alpha: 20 px erbij (snuitpluis links over de vleugel, X17–19), 6 px weg (oude r10-kop rechtsboven die buiten Altaria's vorm valt: (31,19) (32,19) (32,20) (33,20) (33,21) (33,22)).
- **B:** diff met r10 = 198 px. 44 koppixels liggen over wolk/hals (snuit links over de vleugel tot X16, kin over de bovenkant van de hals tot Y31). Alpha: 45 px erbij, 0 weg.

## Controle
14 kleuren; zwart alleen de 5 pupilpixels (A: (20,24–25), (28,24), (28–29,25); B: (19,25–26), (29,25), (29–30,26)). Geen lichte buitenrand buiten de bestaande static-boogjes links.

## Eerlijke twijfels
- B laat de hals korter lijken: de kin ligt 2 rijen lager over de hals.
- Bij beide staat het verre oog dicht bij de linkerrand (zoals bij Altaria zelf). Op 1× is het een donker stipje naast de snuit.
- Het pluiswit gebruikt de static-kleur; de snuit leest nu als licht vlak, maar heeft dezelfde tint als de bliksems.
