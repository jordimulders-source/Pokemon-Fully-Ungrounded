# Picapau-evolutie: sprite r14 (alleen de slierten, op r13)

## Jordi letterlijk
- Over r13: **"doe maar, maar de aansluiting op het hoofd moet iets dikker"** ("doe maar" = de krullen mogen groter, met een duidelijker gat)
- Eerder: **"kijk die eerste is beter, alleen het mag iets meer buigen en elkaar overlappen, zodat het niet precies op pixels grenst met de vleugel"** · **"en ja ze mogen overlappen"** · **"... netjes langs elkaar hangen zoals de raichu oren op de gen 1 sprite"**

## Wat r14 doet (`slierten.txt`, met de hand; kleuren 4/k, 2 px zoals r13)
1. **Dikke aansluiting**:
   - de pluk is bij de voet 4 rijen dik (x24-29, rij 0-3);
   - hij zet de kopomlijning (4, rij 2) voort en groeit zo zonder knik uit de achterkruin;
   - daarna loopt hij taps af naar de twee sprieten van 2 px.
2. **Boog en overlap zoals r13**:
   - de verre ligt bovenop en de nabije direct eronder, vóór hem (4 + k);
   - de bovenrand loopt in trapjes 3-2-2-2 en wordt steiler naar het eind.
3. **Grotere krullen** (elk 7×7 met een gat van 3×3):
   - **Verre**: rechtsboven (x39-45, rij 2-8). Hij gaat links omlaag, onder naar rechts, rechts omhoog en boven terug. Hij zit niet meer half verstopt: de nabije raakt alleen zijn linkerkant.
   - **Nabije**: linksonder (x33-39, rij 7-13). Hij hangt vóór de verre krul omlaag (x37-38) en rolt dan naar links en omhoog naar binnen.
4. **Lucht tot de vleugel**: de minimale afstand is 2 (Chebyshev), dus overal precies 1 px lucht. Het krapste punt ligt tussen (36,13) en de vleugel op (38,15). Zie `diff_uitvoer.txt`.

## Bevroren: bewijs
- `diff_uitvoer.txt`: **0 px verschil met r13 buiten de zone slierten** (x24-46, y0-14).

## Controle (`controle_uitvoer.txt`)
- Geen lichte kleur op de buitenrand.
- Geen losse pixels.
- Geen alleen-diagonale verbindingen.
- 15 kleuren + transparant.
- Eén tintcluster kleiner dan 3 px: G (19-20,11) in de bevroren P5-snavel.

## Bestanden
- `picapau_evo.png`, `normal.pal` en `raster.txt`.
- `slierten.txt`.
- `bouw_r14.py`: r13 zonder slierten + `slierten.txt`, controle, diff en de afstand tot de vleugel.
- `platen.py` → `vel.png`: kop op 8× van r14, r13 en Raichu Gen 1, met daaronder de hele sprite op 1×.
- Draaien: `python3.11 bouw_r14.py && python3.11 platen.py`

## Eerlijke zwakke punten
1. **De verre krul is een lus, geen spiraal.** Zijn eind sluit bovenaan bijna terug op het begin. Hij leest daardoor als een "O" of "P" aan het eind van de spriet. Een binnenwaartse spiraal is het niet.
2. **Rechte stukken.**
   - Waar de pluk in de verre krul overgaat, liggen 5 px bruin op rij 4 (x35-39): de nabije bovenkant en de verre bovenkant lopen in elkaar over.
   - Het verticale stuk van de nabije is 4 px (x37, rij 5-8).
3. **Krap bij de vleugel.** Onder de nabije krul zit precies 1 px lucht tot de vleugel, het minimum.
4. **Voet.** De dikke voet heeft bovenop één rij 4 en een rij k eronder. Op 8× is hij een donkere massa achter de kop. Een lichtere tint zou meer volume geven, maar r13 en de opdracht houden het bij 4/k.
5. **Niet gekeurd.** Er is nog geen onafhankelijke keuring gedaan.

Er is niets gecommit en niets verwijderd.
