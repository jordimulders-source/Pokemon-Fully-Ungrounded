# Gaucho-Lombre r4: blik (maker, 25 nov)

Jordi over r3: "a is het beste maar de blik is niet naar driekwart". Basis = `../r3/lombre_gaucho_r3_A.png`. Het lid van A (bijna vlak, 1 trede) blijft in het nabije oog. Alleen de pupilplaats verandert. Het verre oog wordt 3 px breed (x21–23), met een lid van 3 px, zodat de pupil een plek binnen het wit kan krijgen.

## Studie (Gen 3 anim_front_gba, kop 12× op het vel)
- **Ludicolo:** pupil midden in beide ogen (wit-zwart-wit). Hij kijkt naar de kijker.
- **Nuzleaf** (halfgesloten lid, driekwart links): pupil vooraan (naar de snuit), direct onder het lid.
- **Gaucho-Lotad G** (Jordi's keuze bij dezelfde vraag): nabij oog pupil midden, ver oog stip rechts (naar de kijker).

## Varianten (pixelgelijk buiten de oogvakken nabij x29–34 y25–28 en ver x21–23 y24–26; gecontroleerd)
De pupil zit steeds in de rij direct onder het lid (nabij rij 26, ver rij 25).
- **A:** nabij pupil x32 (net vóór het midden, zoals r3 A); ver pupil x22 (midden van 3). Beide kijken licht vóór de sprite uit. 3 px verschil met r3 A.
- **B:** nabij pupil x33 (net achter het midden); ver pupil x23 (rechts). Beide kijken naar de kijker, zoals Lotad G en Ludicolo. 6 px verschil.
- **C:** nabij pupil x31 (vooraan tegen het lid); ver pupil x21 (links). Beide kijken naar voren, zoals Nuzleaf. 7 px verschil.

Ver oog, nieuwe pixels in alle varianten:
- (23,24) wordt lid (zwart).
- (23,25) wordt wit of pupil.
- (22,26) wordt wit.
- (23,26) wordt rood lijn: de ronde onderkant rechtsonder.

## Bestanden
- `lombre_gaucho_r4_A/B/C.png`: 64×64, P, index 0 transparant, 14 kleuren incl. transparant.
- `pixels.txt`: elke pixel oud → nieuw.
- `vel.png`: kop 12× (r3 A | r4 A/B/C | model | artwork); de referentiekoppen Nuzleaf/Ludicolo/Lotad op 12×; A/B/C geheel 8×; 1× (en 2×) op wit en donker.

## Zwakke punten
1. Een pupilverschuiving van 1 px is op 1× klein. Het verschil tussen de varianten zie je vooral op 8× en hoger.
2. Het verre oog (3×3) is nu bijna even breed als het wit van het nabije oog (4 px). Dat is bewust, voor de leesbaarheid, maar het verkleint het perspectief.
3. Er is nog geen keurder en geen DC-eindkeuring gedaan.
