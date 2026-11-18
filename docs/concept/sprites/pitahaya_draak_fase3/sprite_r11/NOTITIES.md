# Pitahaya-draak fase 3, sprite r11 (maker): Jordi op r10

Jordi (letterlijk): "de binnenkant van de mond is niet verbeterd, 2 stipjes onder elkaar geeft niet het juiste effect. Doe de stipjes op de buik ook onregelmatiger".

- **Basis:** `../sprite_r10/pitahaya3_r10_A.png`; knots/been en verre been uit r10 ongewijzigd. Palet gelijk, index 13 (`q`, ongebruikt dubbel zwart) = teju-grijs (155,154,159).
- **Script:** `python3 maak_r11.py` schrijft C/D/E + `pitahaya3_r11_afwijkingen.txt` (asserts per pixel). `python3 vel.py <tijdelijke map>` maakt `vel.png`: kop 12× C | D | E | r10A | model, buik 12× r11 | r10A | model, hele sprite 5×, 1× en 2× op licht en donker naast Salamence/Tyranitar/Sceptile.

## Controle
- Silhouet alfa-diff 0 t.o.v. r10A; wijzigingen alleen in de bek (x 7-11, y 26-29) en de buik (x 17-30, y 30-43). C, D en E zijn buiten de bek pixelgelijk.
- C 21 px, D 25 px, E 24 px t.o.v. r10A.

## Studie (kort)
- Teju: bek ±6×8 px; bovenste twee rijen grijs (slagschaduw bovenkaak), achterkant grijs, voorkant wit; pitjes ±1 per 5-6 px vlees, verspreid, nooit naast elkaar.
- Salamence/Gyarados/Feraligatr: binnenkant achterin/boven donkerder, voorin licht; diepte komt uit die tweedeling, niet uit details.

## Bek (alle varianten)
- Model toont vlees op (11,29); daar stond zwart -> **bekopening 1 px groter** (`#` -> W). Oude pitjes (9,27) (9,29) (11,28) eerst weg.
- **C:** wit vlees, 2 pitjes schuin t.o.v. elkaar: (9,27) en (10,29).
- **D:** teju-opbouw: bovenrij grijs w (8-10,26), achterin donkerder q (11,26), achterkant (11,27) w, voor wit; 3 pitjes als driehoek (9,27) (11,28) (8,29) (keurdertip: driehoek + grijze bovenrij).
- **E:** wit vlees, één zwart pitje middenin (10,28), de twee die tegen de rand vallen in grijs q: (11,26) en (8,29).

## Buik
- Oude 10 pitjes (zigzag in paren) weg; 7 nieuwe: (21,31) (19,32) (22,33) (23,35) (25,38) (27,39) (28,41). Stappen ertussen wisselen: (-2,1) (3,1) (1,2) (2,3) (2,1) (1,2); geen twee in één rij of kolom naast elkaar, geen pitje raakt een ander (ook niet diagonaal).
- Minder dan 10: de buik heeft maar ±18 wit-pixels met vier witte buren; meer pitjes kan alleen tegen rand/schaduw of tegen elkaar. 6 staan vrij in wit, (21,31) raakt alleen de slagschaduw van de kaak, (28,41) staat in de schaduwsikkel (zoals het oude (27,42)).

## Knots
- Keurdertip (27,50) g -> zwart **niet toegepast**: in r10 staat de bladpunt al tegen donkergroen g met H ernaast (groot contrast), en Jordi gaf op r10 geen opmerking meer op de knots. Kan als losse stap als Jordi het nog dubbelzinnig vindt.

## Eerlijk oordeel
- D leest het meest als mondholte met vruchtvlees (zoals de teju). C is het rustigst maar blijft een wit vlak met twee stippen. E: grijze randpitjes lezen op 1× als schaduw, niet als pit.
- Buik: geen raster meer, maar omdat de buik een schuine strook is volgen de pitjes nog steeds globaal die schuine lijn.
