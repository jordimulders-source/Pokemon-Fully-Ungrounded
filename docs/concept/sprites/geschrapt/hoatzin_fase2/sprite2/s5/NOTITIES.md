# Hoatzin fase 2, ontwerp 2, s5 (20 nov): licht/schaduw per vorm (pitahaya fase 3)

`sh alles.sh` (bouw5.py, keuze.json → `per_vorm`, afwerking.json). Basis s4. Niets getekend; het silhouet is gelijk aan s4.

## Pitahaya fase 3: wat er tussen blurry (r3) en af veranderde
- **Palet:** basistint donkerder (groen L 150 → 137), donkere tinten dieper, stappen gespreid.
- **Vlakken:** het grootste deel in één vlaktint, geen gevlekte modeltextuur.
- **Lijnen:** alleen lange ribben, in de donkerste vlaktint.
- **Schaduw per vorm:** elke vorm (arm, been, staart) heeft een eigen lichte kant (2 px band langs de voorcontour) en een schaduwsikkel. Verre ledematen één stap donkerder, met hun eigen lichte kant.

## Toegepast op de hoatzin
- **Per vorm:** vlakken in de vleugelzone tussen de lijnen = vormen (verre vleugel, nabije vleugel, lijf, staart).
  - Nabij: rand boven/links lichte tint 2, vlak 3, rand onder/rechts 2 px schaduw 4.
  - Verre vleugel een stap donkerder: lichte kant 3, vlak 4.
  - Penranden blijven 2.
  - Werkte: de vleugels krijgen volume, en verre en nabije vleugel komen los van elkaar.
- **Palet en contrast** uit s4 (stappen ±38).
- **Penlijnen in de donkerste vlaktint (152):** in s4 al getest en verworpen; zwart blijft.
- **Tint-barcode** (3/4 om en om) wordt vlak doorgetrokken.

## Controle
dambord 0 · om-en-om 0 · klonten 0 · barcode 0; losse tintpixels 10 (klauwen, poot, snavel, staartpunt, 1 schaduwpixel in de vleugel (52,19)).
`naast.png`: s4 | s5 | Honchkrow, Staraptor, Mandibuzz op 1×/2×. `naast_pitahaya.png`: s5 naast pitahaya fase 3 af op 8×.

## Eerlijk
- Strakker dan s4, maar nog niet zo strak als Honchkrow. De penlijnen zijn trapjes van de modelkromme en de buitencontour is rafelig waar het model veren heeft (vleugeltoppen, staart).
- Kuif en snavel zijn ongewijzigd t.o.v. s4.
