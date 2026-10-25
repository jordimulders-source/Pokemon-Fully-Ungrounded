# Olinguito v2: kleursprite ronde 3

Basis: kleur ronde 2 (`../ronde2/bron/raster_grid.txt`). Hetzelfde palet (16 kleuren, index 0 transparant).

**Bestanden:**
- `olinguito.png`
- `vel.png`, met:
  - ronde 3 op 4× op licht en op donker;
  - ronde 2 op 4×;
  - het ontwerp;
  - beide rondes op 1× op licht en op donker;
  - de vijf referenties op 4× en 1×, op licht en op donker.
- `bron/nieuw.txt`: de met de hand geschreven rijen van deze ronde.
- `bron/raster_grid.txt`
- `bron/bouw.py`
- `bron/vel.py`

## Bewijs
- **Alpha-diff tegen het silhouet van ronde 5: 0.**
- **Bevroren zone (rijen 17–42: kop, oor, masker, snoet, romp): pixeldiff 0.** De staartpixels in die rijen (x ≥ 49, y 17–28) en de toegestane maskerrand zijn uitgezonderd.
- In totaal zijn 86 pixels gewijzigd; 6 daarvan zijn de maskerrand.

## Per punt
1. **Staart en poten opnieuw geschaduwd**, met dezelfde aanpak als de romp.
   - **Staart als cilinder:**
     - De lichtkant ligt links en boven in de boog: 2 px hooglicht naast de donkerbruine selout.
     - Daarna één rij middentint, en de schaduwkant rechts eindigt in de zwarte omlijning.
     - Op de brede basis (6–7 px) staat ook een schaduwrij.
     - In de krul is de bovenkant licht en de onderkant van de boog donker met zwart. De punt is licht met een donkere onderkant.
     - De dunne lichtstrook van 1 px is weg.
   - **Nabije voorpoot:** licht aan de voorkant (2 px), middentint, schaduw aan de achterkant en dan de zwarte scheiding met de verre voorpoot (strook in de schaduwtint, ongewijzigd). De pols gaat via licht over in de roze poot.
   - **Achterpoten:**
     - De nabije achterpoot volgt de dij: onder de lichte dijkap loopt het licht door aan de voorkant van scheen en voet (2 px), met de middentint ernaast en schaduw aan de achterkant (hak).
     - De roze voet heeft een donkerroze schaduwrand.
     - De verre achterpoot blijft in de schaduwtint.
   - Er zit geen ruis of losse plukjes in.
2. **Onderrand van het masker:** de rechte lijn van ±15 px gaat nu mee met de bolling van de kop. Het middenstuk (x 13–18) zakt 1 px (y 35), voor en achter blijft de rand op y 34. Dat is één trapje omlaag en één omhoog, met **6 pixels gewijzigd**.

## Toets op 1×
Staart en poten hebben nu hetzelfde volume als de romp: een ronde staartboog met een lichte kant, en poten met licht voor en schaduw achter. Naast het ontwerp en naast Linoone en Zigzagoon leest hij als één Gen 3-sprite.

## Eerlijk
- De staart heeft over de hele lengte hetzelfde patroon (selout, 2 licht, 1 midden, zwart). Bij 5 px breedte is er geen ruimte voor een aparte schaduwtint naast de zwarte rand; de zwarte rand is daar de schaduwkant.
- De verre poten zijn ongewijzigd (strook en voet in de schaduwtint). Zoals afgesproken.

## Lessen
- **Bij een staart van 5 px is "selout + 2 licht + 1 midden + zwart" het maximum** aan volume. "Selout + 1 licht + midden + schaduw + zwart" geeft de dunne lichtstrook die als lijntje leest.
- **Een rechte maskerrand buig je met één verzakt middenstuk** (1 px, ±6 pixels). Dat volgt de kopbolling zonder de band te verbreden.
