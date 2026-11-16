# Blobfish fase 1: oogvarianten (op r5)

Jordi: "probeer een aantal verschillende ogen uit en laat me zien". Basis `sprite_r5/blobfish_r5A.png` en `_r5B.png`; per variant A en B (zelfde pixels, B = lichtronde). Alleen oog + directe buren (nabij x18-21/y44-47, ver x8-11/y40-43); alpha, buitenlijn en de rest pixeldiff 0 (asserts in `maak_ogen.py`). Kleuren: bestaande indexen 1 zwart, 2 lijnrood, 4 lijf, 12 lichtgrijs, 13 wit. Vel: `ogen_vel.png`.

## v1: huidig (r5): 2x2, glans linksboven, pupil rechtsboven, wit sikkeltje onder
- geen wijziging (referentie)

## v2: zoals het model: wit oog 2x2, zwarte pupil rechtsboven, lijnrode rand rondom
- 16 px: (9,41) lichtgrijs→wit, (11,41) lijf midden→lijnrood, (9,42) lichtgrijs→wit, (10,42) lichtgrijs→wit, (11,42) lijf midden→lijnrood, (9,43) lijf donker→lijnrood, (10,43) lijf donker→lijnrood, (19,44) lijf donker→lijnrood, (20,44) lijf donker→lijnrood, (18,45) lijf donker→lijnrood, (19,45) lichtgrijs→wit, (21,45) lijf donker→lijnrood, (18,46) lijf donker→lijnrood, (19,46) lichtgrijs→wit, (20,46) lichtgrijs→wit, (21,46) lijf donker→lijnrood

## v3: groot rond oog 3x3 (Magikarp-stijl): wit, 1 zwarte pupil midden, rand rechts/onder
- 22 px: (10,40) lijf licht→wit, (11,40) lijf licht→lijnrood, (9,41) lichtgrijs→wit, (11,41) lijf midden→lijnrood, (9,42) lichtgrijs→wit, (10,42) lichtgrijs→wit, (11,42) lijf midden→lijnrood, (9,43) lijf donker→lijnrood, (10,43) lijf donker→lijnrood, (18,44) lijf donker→wit, (19,44) lijf donker→wit, (20,44) lijf donker→wit, (21,44) lijf donker→lijnrood, (18,45) lijf donker→wit, (19,45) lichtgrijs→zwart, (20,45) zwart→wit, (21,45) lijf donker→lijnrood, (18,46) lijf donker→wit, (19,46) lichtgrijs→wit, (20,46) lichtgrijs→wit, (21,46) lijf donker→lijnrood, (18,47) lijf donker→lijnrood

## v4: zwart kraaloog 2x2 met 1 witte glanspixel linksboven
- 8 px: (9,41) lichtgrijs→wit, (11,41) lijf midden→lijf donker, (9,42) lichtgrijs→zwart, (10,42) lichtgrijs→zwart, (11,42) lijf midden→lijf donker, (19,45) lichtgrijs→wit, (19,46) lichtgrijs→zwart, (20,46) lichtgrijs→zwart

## v5: derpy scheel: wit oog 2x3 (ver 2x2), pupillen omhoog naar elkaar toe
- 16 px: (9,41) lichtgrijs→wit, (11,41) lijf midden→lijnrood, (9,42) lichtgrijs→wit, (10,42) lichtgrijs→wit, (11,42) lijf midden→lijnrood, (9,43) lijf donker→lijnrood, (10,43) lijf donker→lijnrood, (19,44) lijf donker→zwart, (20,44) lijf donker→wit, (21,44) lijf donker→lijnrood, (19,45) lichtgrijs→wit, (20,45) zwart→wit, (21,45) lijf donker→lijnrood, (19,46) lichtgrijs→wit, (20,46) lichtgrijs→wit, (21,46) lijf donker→lijnrood

## v6: breder wit oog 3x2, pupil rechtsboven, lijnrood ooglid onder
- 17 px: (9,41) lichtgrijs→wit, (10,41) zwart→wit, (11,41) lijf midden→zwart, (9,42) lichtgrijs→wit, (10,42) lichtgrijs→wit, (11,42) lijf midden→wit, (9,43) lijf donker→lijnrood, (10,43) lijf donker→lijnrood, (11,43) lijf donker→lijnrood, (18,45) lijf donker→wit, (19,45) lichtgrijs→wit, (21,45) lijf donker→lijnrood, (18,46) lijf donker→wit, (19,46) lichtgrijs→wit, (20,46) lichtgrijs→wit, (21,46) lijf donker→lijnrood, (18,47) lijf donker→lijnrood

## v7: extra: blije dichte ogen (boogjes ^ ^), zwart
- 12 px: (9,41) lichtgrijs→zwart, (11,41) lijf midden→lijf donker, (9,42) lichtgrijs→lijf donker, (10,42) lichtgrijs→lijf donker, (11,42) lijf midden→zwart, (19,45) lichtgrijs→zwart, (18,46) lijf donker→zwart, (19,46) lichtgrijs→lijf donker, (20,46) lichtgrijs→lijf donker, (21,46) lijf donker→zwart, (19,47) lijnrood→lijf donker, (20,47) lijnrood→lijf donker

## Eigen blik op 1× (maker)
- Leest als oog op 1×: v3 het duidelijkst (groot wit met stip, staart derpy), dan v5, v6, v2. v1 en v4 zijn op 1× nauwelijks te zien (klein/zwart op donker lijf). v7 (boogjes) verdwijnt op 1× bijna in het donkere lijf.
- Derpy blij met de opkrullende mond: v3 (wijd starend) en v5 (scheel) het sterkst; v2 ligt het dichtst bij het model.
- Het verre oog zit tegen de buitenlijn linksboven; bij v3/v5/v6 is het daardoor deels "achter de kop".
