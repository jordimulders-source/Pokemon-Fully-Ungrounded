# Blobfish fase 1, sprite r4 (maker): alleen het mondeind

Start `r3.png`. Silhouet bevroren, diff alleen in de mondzone (x16–21, y47–50; beide met assert gecontroleerd in `maak_r4.py`).
Model: de mondlijn stijgt bij x18–19 van onderin naar bovenin rij 49, richting het nabije oog (±2 natieve px, kleiner dan 1 spritepixel; door de reductie verloren). Herstel naar plek en richting van het model:

- **r4a (gekozen = `blobfish_r4.png`), 2 px:** (19,48) lip 9 → zwart (eind 1 rij hoger, richting oog), (19,49) zwart → liptoon 9 (lip sluit onder en rond het eind, zoals het model). Mondlijn blijft overal 1 px: rij 49 x12–18, dan schuin omhoog naar (19,48).
- **r4b (variant), 1 px:** alleen (19,48) zwart erbij; (19,49) blijft zwart → haakje van 2 px dik in de hoek.

Op 1×/2× lezen beide als glimlach met opkrul; r4a is de dunne lijn van het model en houdt de lipkleur rond het eind, r4b leest iets zwaarder ("J"). Gekozen: r4a.

Afwijking t.o.v. r3: r4a 2 px, r4b 1 px, beide in de mondzone. Vel: r4 | r3 | model op 8×, gezicht 16× r4a | r4b | model, 1×/2×.
