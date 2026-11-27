# Sneeuwmonster fase 2 – sprite ronde 4 (maker)

`sneeuwmonster2_r4.png` = r3 met alleen de emmernaden opnieuw (24 px verschil, allemaal in de emmer; mond, stenen en de rest = r3, diff 0 buiten de emmer). `bouw.py`, `vel.png` = r4 | r3 | model.

## Emmernaden: doorlopende 1 px-lijnen
- Naadkolommen = de gemeten pieken uit r3 (`../gereedschap/naden.py`), ±3 px uit elkaar: boven de band x31, x34, x40, x44; onder de band x28, x32, x35, x39, x44. x41 onder vervalt (2 px naast x39: "minder").
- Elke naad loopt door: boven van de rij onder de lichte bovenrand tot tegen de band; onder van tegen de band tot de rij boven de onderlijn van de emmer (onderlijn blijft hout).
- Schuinte: per naad een rechte lijn x = a + b·y door het naadmaximum (±1 kolom) per rij, gewogen met het naadaandeel van het model, begrensd tot ±1 kolom. Zo lopen ze licht schuin mee (bijv. x31 → x32 en x34 boven), zonder losse stappen.
- Kleur: donker hout (7). Alleen de naad helemaal rechts (x44, schaduwkant, op donker hout) in de donkerste tint (omlijning), boven rij 9–12 en onder 15–18. Naden die over donker hout lopen (x39/x40 in het rechterdeel) vallen daardoor weg in de vulling; geen zwart in het midden.
- De losse zwarte pixels van r3 (o.a. (41,16)) zijn weg: zwart in de emmer zit nu alleen in de doorlopende naad op x44.

## Controle
bbox x8–55, y3–58 (48×56), 16 kleuren incl. transparant, geen lichte kleur op de buitenrand, geen losse zwarte pixels.

## Zelf nog zwak
- In het donkere rechterdeel zijn x39/x40 onzichtbaar (donker hout op donker hout); daar leest alleen de naad op x44. Zichtbaar maken kan alleen met een extra donkere tint (palet vol) of zwart, wat de opdracht uitsloot.
