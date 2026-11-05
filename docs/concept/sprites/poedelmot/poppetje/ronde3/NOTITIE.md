# Poedelmot poppetje, ronde 3 (5 nov)

Opdracht: alleen (1) poten uit de echte bron, (2) verre achtervleugel zichtbaar, (3) dubbele kam op de sprieten. De rest is
ronde 2 (`../ronde2/pop3d_poedelmot_r2.py`): hoek 45°, kop, ogen, neusbrug, nabije vleugels, sprietlengte.

## Bestanden
- `pop3d_poedelmot_r3.py`: het poppetje; schrijft ook de overlay en het vel.
- `overlay_poten.png`: de poten nagetrokken op `foto_tak_katoen.webp` (heup, knie, voet, pompon per poot; lucht tussen de poten; onderkant lijf), naast het poppetje met dezelfde kleur per poot.
- `poppetje_45.png`, `poppetje_45_1x.png`, `vel.png` (tak-foto, poppetje, 1× naast butterfree, venomoth, volbeat, teddiursa).
- `keurvel_45.png` + `keurvel_45.png.keuring.md`: eigen keuring, **FAIL**.

## Wat er veranderd is
1. **Poten** (naar de overlay): de poten staan in een waaier uit de borst, met de dij naar buiten, de knie naar buiten/voren en het onderbeen omlaag. De voeten staan ver uit elkaar met lucht ertussen.
   - De punten zijn op 45° in beeld uitgezet (`op45(sx, y, diepte, r)`). Van links naar rechts: verre voorpoot, verre middenpoot, nabije voorpoot, verre achterpoot, nabije middenpoot, nabije achterpoot.
   - De nabije poten staan lager (voet y −12) en hebben grotere pompons (8,6/7,8/7,2). De verre poten staan hoger (−5 tot −7), hebben kleinere pompons (6,6/6,0/5,4) en staan in de schaduwtint.
   - De poten zijn langer dan in ronde 2 en blijven wollig: er zitten bobbels op de gewrichten en halverwege elk segment.
   - De lage buikwol en het achterlijf op de grond zijn weg; die vulden de lucht tussen de poten. Het achterlijf zit iets hoger en de borstwol is smaller.
2. **Verre achtervleugel** is naar voren en opzij gedraaid. Hij steekt nu links naast de kop uit onder de verre voorvleugel, één gladde ronde vorm. De nabije is ongewijzigd.
3. **Sprieten** hebben tanden aan beide kanten van de schacht, in het vlak loodrecht op de kijkrichting en iets naar de punt gericht (veervorm).

## Eigen zwakke punten
- **Poten:** ze lezen op 1× als losse poten, maar op werkformaat eerder als lammetjespoten (steil omlaag) dan als insectenpoten. Op de foto zijn de voorpoten langer en schuiner naar buiten en voren. Mogelijk moet de dij meer horizontaal opzij en het onderbeen meer uitwaaieren.
- **De verre middenpoot en verre achterpoot** zijn op 1× maar 11–13 px groot: zes tel je niet zonder te weten dat ze er zijn.
- **Het lijf** hangt nog iets hoger dan op de foto.
- **De verre achtervleugel** is bijna even groot als de nabije, dus er zit weinig perspectief in. Op 1× kan hij als een grijze flap naast het oog lezen.
