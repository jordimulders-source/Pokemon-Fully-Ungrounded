# Stap 4, hoofd ronde 5b (6 nov): reparaties op ronde 5 optie 2

Optie 1 vervalt. Hieronder alleen de benoemde reparaties uit `ronde5/vel_hoofd.png.keuring.md`. Bestanden: `hoofd.png` (64×64, op de schermplek), `vel_hoofd.png` (8×, 2× en 1× naast Hitmontops spritekop en de anime) en `stap4_r5b.py` (met het raster). Coördinaten zijn schermpixels.

1. **Mond.** Een recht streepje van 4 px, haaks op de gezichtsas. Door de draaiing loopt het licht schuin, met rechts hoger: (17,44), (18,44), (19,43), (20,43). Er is geen U meer. Het midden (18,5;43,5) ligt onder het punt tussen de ogen. Tot de omtrek is 2 px J aan de rechterkant en 2 px aan de onderkant.
2. **Fadestreep.** Korter, als een flauwe V hoog op het voorhoofd: K (11,32), L (12,32) (13,32) (14,31), en K (15,30). Hij eindigt ruim vóór de omtrek: links zijn 6 px vrij, rechts 6 px.
3. **Knot en punt.** De knot zit nu hoger en verder naar achteren, bovenop de schedelomtrek (x1–6, y23–28). Hij is geen bol op oorhoogte meer. De kleine punt heeft tip (8,22) en een voet van 2–3 px ((7–8,25), daarna open in de schedel). Knot en punt gaan bij y26 zonder lijn over in de schedel. De inham ertussen is een gesloten V-keepje: (5,23) → (6,24) → (7,23). Het enige lichtvlak zit linksboven op de knot ((3–4,24) en (2,25)).
4. **Rechteromtrek.** Het rechteroog is 1 px naar binnen geschoven (x18–21). De omtrek loopt nu op x24 van y33 tot y40, zonder de bult. De linkeromtrek is op y35–39 1 px rond naar buiten gezet: eerst was hij 10 px recht.

Controle (met een script): geen open randen. Het hoofd raakt geen pixel van het lijf van `stap3b/optie_C`. Het hoofd is 441 px.

## Zwakke punten
- **Knot en punt.** Op 1× smelten ze samen tot één spitse bult linksboven. Op 8× zie je twee bulten, die als oortjes kunnen lezen.
- **Fadestreep.** Op 1× is hij bijna onzichtbaar.
- **Gezicht.** Het blijft simpel en lief, met een grote lege huidvlakte.
