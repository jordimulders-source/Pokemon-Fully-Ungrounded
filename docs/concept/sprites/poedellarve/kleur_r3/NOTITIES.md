# Poedellarve: kleur r3 (alleen kleur, licht linksboven)

Basis is `../af/poedellarve.png` (r2 gespiegeld). `stappen/af_raster.txt` is dat bestand als raster; `raster.txt` is r3. Coördinaten in de gespiegelde stand. Vorm, alpha en lijnplaatsing zijn ongewijzigd: alpha-diff 0 tegen af/.

## Reparaties (eindkeuring Dragonfly Cave)
1. 2 → 3: (35,44), (40,46), (44,49), de selout aan de linkerkant van de rugbulten.
2. 3 → 2: (32,42), (32,43), (37,45), (43,47), (49,53), (50,54). **Afwijking:** (47,50) blijft 3. Met 2 lag daar een losse 2 tussen twee 3-reeksen op de staartrand: 3, 2, 3, 3, 2, dus om en om. Bovendien bleef de staarttop (48,51)/(49,52) dan een selout-reeks van 2 px. Met (47,50) in 3 loopt de rand in één overgang van 3 (boven) naar 2 (rechtsonder). Dat is de kleinste oplossing: 1 px.
3. 2 → 3: (14,41), (14,42), (13,43), de selout linksboven op de kop.
4. 7 → A: (14,43), (14,44), (15,44).
5. 7 → A: (13,54), (13,55), (14,55); de pillow shading is weg.
6. 6 → 7: (13,36), (13,38); 5 → 6: (14,39).
7. Palet 7: 230,224,212 → 226,216,200.

21 px wijken af van af/ (lijst in de controle hieronder), plus de paletkleur.

## Controle (`controle_uitvoer.txt`)
- alpha-diff 0, open randen 0, losse pixels 0, tintclusters < 3 px 0;
- selout 3: 23 px in 6 reeksen van 3–7 px, geen reeks < 3;
- 10 kleuren + transparant.
- **Lichtrichting op de buitenrand:** 3 staat 20× aan de bovenkant, 7× links en 9× rechts. De 9 rechts zijn de topjes van de bulten, die volgens de opdracht 3 blijven. Daarnaast staat 2 47× onderaan.
