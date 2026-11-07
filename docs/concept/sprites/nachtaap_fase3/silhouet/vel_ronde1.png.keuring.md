# Keuring vel_ronde1.png (silhouet nachtaap fase 3, ronde 1, 5 nov)
Bron: het goedgekeurde model `../model2d/model.png` (50%-dekking `model50.txt`); Gen 3: Alakazam, Medicham, Deoxys, Primeape, Slaking (anim_front_gba); fase 1 en 2.
Bekeken: 4× (vel), 8× (eigen controle per zone, dekking per pixel), 1× en 2×; scripts: korrel.py (0), diff met de 50%-grens (+22/−5, alles ≤ 1 px), opening 2×2 (0 dunne delen), componenten (1).
- Kop/vuist/arm: lijkt op het model / wijkt af in: niets (samenvallen komt uit het model).
- Opgeheven been + voet: lijkt op het model / wijkt af in: niets.
- Healerhand + gloed: lijkt op het model / wijkt af in: niets (vingers in de kleur).
- Onderste been: lijkt op het model / wijkt af in: niets.
- Spiraalstaart: lijkt op het model (buitenrand exact, gat 3×4) / wijkt af in: spleten tussen de windingen gevuld (< 1 px; lijnen in de kleur).
Onafhankelijke keurder: één FAIL (buitenrand staart 1 px te dik) → gerepareerd en nagemeten.
Oordeel: PASS
