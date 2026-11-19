# Palpaca r6 (19 nov): romp-omtrek rond en wollig

Jordi (letterlijk), over het zwakke punt van r5 "De omtrek van de romp blijft hoekig, met een rechte rug en achterkant": "Ja dit kan beter".

## Bestanden
- `palpaca.png`, `normal.pal` (= r5-palet, 16 kleuren incl. transparant).
- `vel.png`: model | r6 | r5 (8x, zelfde hoogte) · torso 12x: model op spriteraster | r6 | r5 · kop 12x · 1x en 2x op licht en donker.
- `scripts/bouw_r6.py` (r5 → r6; controleert dat elke wijziging in de romp-randzone ligt), `scripts/dekking.py` (modeldekking per spritepixel naast r5-alfa), `check.py`, `zoom.py`, `vel.py`.

## Model gemeten
Op het spriteraster (`dekking.py`, `modelkop.py`): de modelrug ligt vanaf de halsband op y 37–38 met wolbulten (x 31–33 en x 35–37, dipje ertussen); de bil bolt onder de staart uit (x 43–45, y 41–44) en buigt dan naar binnen naar de verre achterpoot; de borst heeft een lichte wolbult links (x 20, y 41–44, dekking 16–24%).

## Randpixels
- **Toegevoegd (9):** rug (32,37) (33,37) zachte lijn 6 = tweede wolbultje naast het bestaande op x 35–36, dip op (34,38); bil (45,42) (45,43) zwart, (44,42) (44,43) wol 5, (44,44) zwart; borst (20,42) (20,43) zachte lijn 6.
- **Weggehaald: geen.**
- Kop, nek, staart, poten, handschoenen en pootstand: diff 0 (assert in `bouw_r6.py`). In totaal 26 px anders dan r5.

## Schaduw/selout langs de nieuwe rand (stijl r5)
- Rug: onder het nieuwe bultje hooglicht 2 op (32,38) (33,38) (was lijn 6).
- Bil: oude rand x 43 wordt wol; sikkel 4 → 5 naar de nieuwe zwarte rand: y 42–43 x 42–43 = 4, x 44 = 5; y 44 x 41–42 = 4, x 43 = 5; (41,42) (41,43) (40,44) = 3 zodat de band niet breder wordt dan 2 px.
- Bil over de verre poot: binnenlijn (43,45) (42,45) zachte lijn 6, sluit aan op (41,46) (40,47) 6 en (39,48) 1.
- Borst: oude lijn (21,42) (21,43) wordt wol; borsthooglicht als ovaal tot in het bultje: (21,42) (22,42) (22,43) = 2, (21,43) = 3.
- `check.py`: geen nieuwe losse pixels t.o.v. r5.

## Zwakke punten
- De bulten zijn 1 px; de rug blijft over de hele lengte ongeveer op dezelfde hoogte (zoals in het model, dat ook een vrij vlakke rug met wolbulten heeft). Een hogere, bollere rug zou de staart- of nekaanzet raken (bevroren).
- Buikrand niet veranderd: tussen de poten is te weinig ruimte voor een wolbult zonder de pootaanzetten te raken.
- Niet gekeurd door een onafhankelijke keurder.
