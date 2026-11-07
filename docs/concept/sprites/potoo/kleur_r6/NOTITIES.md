# Potoo kleur r6

Basis r5; alleen de vleugelzone x35-46 y25-46 (`wijzig_r6.py`). Bewijs: `diff_uitvoer.txt`: 25 px gewijzigd, 0 buiten de zone.
- Dekveren rustiger: crème 7 met wit 8 bovenlinks per veer, grijs 6 alleen als schaduwrand x43 (en (42,23-25), (43,35-37) om clusters heel te houden). De donkere V-puntjes uit r5 blijven.
- Witte handpenstrook x41 doorgetrokken: 8 op y36-40, 7 op y41-46. De binnenrand (3) schuift daardoor naar (42,40-41) en (43,42-44).

Controle (`controle_uitvoer.txt`): alpha-diff 13 (gemotiveerd in r5/NOTITIES), open randen 0, losse pixels 0, clusters 0, 12 kleuren.

Wat nog afwijkt van het model:
- Vleugel: de witte veervormen van het model (lange witte punten met donkere rand) zijn hier crème vlakken met losse donkere puntjes. De vleugel leest als vorm door de voorrand en de handpenstrook, maar de verenlagen zijn zwakker dan in het model.
- Borst-V's lezen op 8× als korte streepjes, niet als doorlopende zigzag. Het model heeft per rij meer tanden dan op 64 px passen.
- Klauwen: tenen crème met omtrek, maar door de donkere onderkant (model 39-96) en de zwarte teenpunten leest het gebied op 8× nog vrij donker.
- Glans 2x2 is groter dan gemeten (het model heeft ±1,5 px).
- Kuifplukjes zijn 1 px en klein vergeleken met de witte spitse plukken van het model.
