# Picapau-evolutie: sprite r13 (alleen de slierten, op r12)

## Jordi letterlijk
- Over r12: **"kijk die eerste is beter, alleen het mag iets meer buigen en elkaar overlappen, zodat het niet precies op pixels grenst met de vleugel"**
- Eerder: **"ik ben nog steeds niet tevreden met de slierten op het hoofd overigens, die moeten beiden ongeveer uit dezelfde plek komen en netjes langs elkaar hangen zoals de raichu oren op de gen 1 sprite"** · **"en ja ze mogen overlappen"**

## Wat r13 doet (`slierten.txt`, met de hand; 2 px dik, kleuren 4/k zoals r12)
- **Eén pluk**:
  - de nabije ligt over de hele boog direct onder en vóór de verre;
  - per kolom van boven naar onder: verre 4, nabije 4, nabije k;
  - ze lezen daardoor als één dikke sliert vanaf de achterkruin.
- **Meer buigen**: de bovenrand loopt in trapjes 3-2-2-1-1 (rij 0 → 4) en wordt steiler naar het eind; in r12 was dat gelijkmatig 3-3-3-3-2.
- **Uiteen pas onderaan**:
  - **Verre**: rolt achter de nabije in een spiraal met gat rechtsboven (x36-41, rij 3-8). Zijn linkerkant gaat achter de nabije schuil; zijn rechterkant en onderkant steken uit.
  - **Nabije**: hangt vóór hem omlaag (x36-37, rij 7-10) en rolt naar de kop toe in een spiraal met gat linksonder (x32-37, rij 8-12).
- **Los van de vleugel**: de slierten liggen hoger en dichter bij de kop. De minimale afstand tot de vleugel is **3** (Chebyshev; 1 = raakt, 2 = 1 px lucht), dus overal minstens 2 px lucht. Het kleinste gat zit tussen (35,12) en de vleugel op (38,15). Zie `diff_uitvoer.txt`.

## Bevroren: bewijs
- `diff_uitvoer.txt`: **0 px verschil met r12 buiten de zone slierten** (x24-46, y0-14).

## Controle (`controle_uitvoer.txt`)
- Geen lichte kleur op de buitenrand.
- Geen losse pixels.
- Geen alleen-diagonale verbindingen.
- 15 kleuren + transparant.
- Eén tintcluster kleiner dan 3 px: G (19-20,11) in de bevroren P5-snavel.

## Bestanden
- `picapau_evo.png`, `normal.pal` en `raster.txt`.
- `slierten.txt`.
- `bouw_r13.py`: r12 zonder slierten + `slierten.txt`, controle, diff en de afstand tot de vleugel.
- `platen.py` → `vel.png`: kop op 8× van r13, r12 en Raichu Gen 1, met daaronder de hele sprite op 1×.
- Draaien: `python3.11 bouw_r13.py && python3.11 platen.py`

## Eerlijke zwakke punten
1. **Kleine spiralen.** Ze zijn klein (±5×5 zichtbaar). Op 1× lezen ze als twee haakjes onderaan de pluk, niet als volle krullen met een duidelijk gat. Bij de verre spiraal is het gat 1-2 px.
2. **Rechte stukken.** Het verticale stuk van de nabije (x36-37, rij 7-10) is 4 px recht, en de onderkant van de nabije spiraal (rij 11) 5 px recht. Beide zijn langer dan 3 px.
3. **Eén kleur in de pluk.** Doordat verre en nabije allebei donkerbruin (4) zijn, is in de pluk de grens tussen de twee niet zichtbaar. Je ziet één band van 3 px (bruin, bruin, zwart). Dat is bewust ("één pluk"), maar van dichtbij zie je niet dat het er twee zijn tot ze uiteengaan.
4. **Verre spiraal deels verstopt.** De nabije loopt over de linkerkant van de verre spiraal. Daardoor lijkt de verre spiraal op 8× meer een "C" achter de nabije.
5. **Niet gekeurd.** Er is nog geen onafhankelijke keuring gedaan.

Er is niets gecommit en niets verwijderd.
