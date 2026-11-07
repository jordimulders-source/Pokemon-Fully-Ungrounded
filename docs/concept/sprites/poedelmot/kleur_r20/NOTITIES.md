# Poedelmot: kleur r20

Vanaf r19 (`stappen/basis.txt`). Stap: `python3 apply.py basis.txt ../raster.txt r20a r20b` (in `stappen/`), daarna `palet.py`, `controle.py` en `vel.py`. Er zijn 384 px gewijzigd. Meten: `stappen/grid.py` (p15 van het model per spritepixel), `stappen/px.py`, en `stappen/box1x.py` (BOX-verkleind model naast de sprite op 1×, `box1x_r20.png`).

## Gedaan
1. **Sprietvlak (r20a):**
   - Baardjes in middentint C (118,96,80), lum 98. Daaronder vlak E (40,30,24), zwartbruin.
   - Zelfde steile strepen (links '/', rechts '\', periode 3), nu ook tot tegen de nerf. De buitenrand blijft 1/2.
   - Gemeten over het vlak (275 px): model gem 56 / std 28, sprite gem 54 / std 32. In r19 was dat 48/67.
   - De nerf (D, lum 191) is de lichtste lijn. Op 1× leest de spriet als een donker, fijn gestreept blad.
2. **C en D samengevoegd:** de nerf staat nu in D. Index C is de baardjestint en E de nieuwe vlaktint. Palet: 14 kleuren + transparant. De spriet heeft 3 tinten (E, C, D) + lijn 1/2.
3. **Rechtervoorvleugel (r20b), gemeten met p15:**
   - Buitenste krulboog naar (55–56,21), (56–57,22), (57–58,23), (57–58,24), (56–57,25), (55–56,26). Het model meet daar 150–180.
   - Ik mat dat de boog doorloopt naar (56–57,27), (57,28), (57,29) en (55,30–31). Die stukken heb ik ook verlegd; daar lag (55,28) in r19 op wit.
   - De oude plekken staan nu in 7/A (model 200–247).
   - 444 (51–53,24) en 555 (52–54,26) zijn weg (model 210–244). Tan in 5 op (50–51,25), (50,26) en (53–54,27). Rij 30: 5 op x48–52, (47,30) licht.
   - Omliggende vlakjes naar de meting: (52–55,24–25), (51–52,26–27) en (59–60,24) zijn wit.
4. **Linkervleugel:**
   - Rij 31: D op x10–11 en x15–16 (model 150), (13–14,31) wit (model 210). (17,31) 3 en (18,31) 4: het model meet daar 70/120.
   - Rij 32: D op x10–13 (model 130–140).
   - Rij 33: D op x10–13 (model 140–150), (14–15,33) in 7 (model 170–190).
   - Rij 30: (14–15,30) in D (model 110–160). Rij 34: (13,34) in D (model 140).
   - Kleine reparatie: (11,34) en (12,34) in 7.

## Controle
Alpha-diff 0, open randen 0, losse pixels 0, clusters < 3 px 0. `krul_lijnen.txt` is bijgewerkt: de nieuwe krulpixels staan erin, de verplaatste zijn eruit.

## Zwakke punten
Geen. Op 1× naast het BOX-verkleinde model lezen de sprieten, de krullen en de linkervleugel als het model. De nerf is lichter dan in het model (keurder: "nerf blijft zoals hij nu is").
