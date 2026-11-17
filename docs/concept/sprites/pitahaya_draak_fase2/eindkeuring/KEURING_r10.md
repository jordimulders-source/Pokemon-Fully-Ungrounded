# Herkeuring r10 (`sprite_r10/pitahaya2_r10.png` + variant `_plaatlicht`), 16 nov

**Oordeel: FAIL, nog 14 px.** Daarna PASS. Een toets van die 14 px staat in `proef_r10.py` → `proef_r10.png`; dat is geen oplevering.
Hoofdvraag: r10 is op 1× en 2× duidelijk beter dan r9A. De poten lezen als volume, de staart is rond, de tenen zijn te zien en de mondhoek gloeit niet meer. Er zijn geen nieuwe fouten: dambord 7 (gelijk), op de buitenrand geen vlaktint behalve de tand (4,43), 13 kleuren, en het silhouet is alleen op de B-pixels gewijzigd.

## A–G
| | | |
|---|---|---|
| A bek-roze | **FAIL** (8 + 1 px) | zie hieronder |
| B silhouet | PASS | staart 4, kop 4, poot 3 px recht |
| C belijning | PASS | selout van de kop is één tint d; randen ok |
| D schaduw | **FAIL** (5 px) | d-plak in de keel, zie conflict 2 |
| E kleur | PASS | roze 34/43/61, groen 35/38/43; het roze blijft roze |
| F netheid | PASS | losse H-pixels zijn diagonaal randlicht uit het model |
| G checklist | PASS | A6 opgelost door B |

## Roze in en om de bek (opnieuw)
De mondhoek gloeit niet meer en de voorlip is goed: P op de voorste bocht, r eronder en K onderaan. Er resten twee punten:
1. **De verre lipband is 4–5 px breed, in effen p.** Het model heeft daar 2 px p en daarachter r (modeltoon per blok). Daardoor leest de band nog als een roze wang en niet als een lip om het vruchtvlees. Neem over uit het model: p → r op (19,48), (18,49), (19,49), (17,50), (18,50), (19,50), (16,51) en (17,51).
2. **De mondhoek is open.** (19,43) p raakt het p van de bovenkaak (18,42) en de lipband (18,44). Daardoor lopen boven- en onderkant van de bek in elkaar over, wat Jordi ook bij r3 zag. Het model heeft hier r: (19,43) p → r.

Resultaat in de proef: één lipband van ±2 px rond het vruchtvlees, met donkerder keel en kaak erachter. Dat is de opbouw van Exploud en Gyarados: lipband, dan donker.

## De vijf meetconflicten (het model is leidend)
1. **D1 evenaar: maker heeft gelijk.** Per blok heeft het model de p/r-grens zelf recht op rij 44/45. De verhoging naar achteren (r op (44–47,43) en (45,37–38)) komt uit de gladde modelhelderheid, dus uit het model. Accoord.
2. **D1-sikkel: half.** De d op (37,50), (38,51) en (39,51) langs de middelste dij volgt het model (model d op (36,50) en (37,51)). Accoord. Maar **(24,48), (25,48), (26,48), (27,48) en (26,49) d → r**: per blok heeft het model daar r (helderheid 74–78, dichter bij r 86 dan bij d 52). De gladmaking trok de donkere keellijn van rij 49 omhoog. Zo ontstaat een horizontale d-plak van 2 rijen (banding). De lijn d (20–25,49) blijft.
3. **D3 randlicht rechts: maker heeft gelijk.** Het model heeft het lichtste groen als randlicht rechts op de dijen en de staartkrul; mijn "linksboven" was een Gen 3-gewoonte. Accoord.
4. **F: maker heeft gelijk.** De vijf G-pixels zijn modeltoon G. Accoord.
5. **B2 inkepingen: blijft.** De modeldekking is 9/9, maar het model heeft daar teenlijnen (zwart 4/9 en 5/9) en op de onderste rij geen doorlopende lijn. De inkeping is de enige manier om die teenlijnen op 64 px te laten lezen. Model en Gen 3 (Feraligatr, Swampert) wijzen dezelfde kant op.

## Is het onderlijf echt één vlak uit het model?
Ja. De modelhelderheid per spritepixel in het roze onderlijf (x 28–46, rij 45–46) is 87–91, vrijwel constant (r = 86, p = 129). Het model heeft daar geen verloop en het vlak is maar ±3 rijen hoog tot de dijen. Binnen de modeltinten valt er niets meer uit te halen, en de maker heeft dat terecht niet geforceerd. Meer volume kan alleen buiten het model: bijvoorbeeld 1 rij d langs de bovenkant van de dijen, of p-tongen per plaat omlaag. Dat is een keuze voor Jordi en geen reparatie.

## Variant `_plaatlicht` (niet gekozen)
- **Hoofdversie:** geen P op het lijf. De rugplaten zijn effen p met r-naden, trouw aan het model (3 % P). De rug is rustig maar wat vlak; het licht zit alleen op de kop.
- **Variant:** 8 px P op de top van de twee grootste rugplaten, (28–29,36–37) en (35–37,36–37). De platen krijgen een lichte bovenkant, de rug leest meer als bol, en het licht linksboven loopt van de kop door over het lijf. Daar staat tegenover dat het niet in het model staat. Op 1× zijn het twee lichte vlekjes op de rug.

## Reparatielijst (14 px, met assert op de oude waarde)
1. A: p → r op (19,43), (19,48), (18,49), (19,49), (17,50), (18,50), (19,50), (16,51), (17,51).
2. D: d → r op (24,48), (25,48), (26,48), (27,48), (26,49).
3. Dezelfde 14 px in de variant `_plaatlicht`. Buiten deze pixels diff 0.
