# Hauntflare v8b: tanden vast aan de lip (maker, 15 nov)

Opdracht (Jordi via Claude): I afgekeurd ("die tanden kloppen toch niet, kijk nu eens naar het referentiemateriaal"); daarna "niet de hele mond opnieuw tekenen, alleen de tanden eraan vast maken". Mond van v7 (omtrek, maat, plek, opening, tong) blijft; geen rij erbij.
Reproduceren: `python3 tanden.py` · `python3 controle.py` · `python3 vel.py` (vel.png: bovenaan mondcrops artwork | 3D | pixel-ref | Haunter G3; daaronder v7, R, S: gezicht 12x, sprite 6x, 1x).

## Bouw (zoals Haunter G3 rij 39-41: voet in de lip, punt met zwarte flanken)
- Boventanden: de zwarte bovenlip (y33) breekt open waar een tand zit; de tandvoet is hoofdroze 7 in de liprij (vast aan het hoofd), de punt 1 rij lager met zwarte flanken = de lijn loopt in een V om de tand. Tand 1 x25-27 punt (26,34); tand 2 x29-31 punt (30,34). Inkepingen zwart op (24,33), (28,33), (32,33).
- Ondertanden: zelfde, gespiegeld vanuit de onderlip (y37), punten verspringend tussen de bovenpunten: (24,36) en (28,36).
- Tong blijft in y35 (hele rij) en tussen de onderpunten op y36; donkerrood blijft tussen de bovenpunten op y34.

## Kandidaten (diff t.o.v. v7; buiten de mond x19-33 y32-38 = 0, silhouet 0, palet v7, P, transparantie 0)
- **R** (26 px): ondertanden met voet 3 breed in de onderlip (y37 x24-25 en x27-29, kin (27-28,38) 2->7 zodat de tand aan het hoofd vastzit), lijn om de ondertanden in lipdonker 2 (zoals de onderlip van v7 rechts), bovenlijn zwart. Boven en onder even grote tanden = de zigzag van het 3D-model.
- **S** (23 px): als R, maar kleine ondertanden (onderlip blijft zwart, 1 px voet onder elke punt): grote V's boven, kleine golf onder, zoals de artwork en Haunter G3.

## Afgevallen
- P: als R met zwarte lijn ook om de ondertanden: te veel zwart, kluwen.
- Q: zwarte lijn alleen aan de schaduwkant: tanden lopen over in het donkerrood, mond verdwijnt op 1x.
- Punten met zwarte dop eronder (Haunter G3 rij 41): de tongrij wordt een zwart-roze schaakbord.
- Eerdere v8 (I/J/K): losse blokjes onder een rechte lip, niet vast aan het hoofd (afgekeurd).

## Oordeel
Op 12x naast de refs: dezelfde bouw (hoofdroze V's vast aan beide lippen, zigzagrij boven en onder, verspringend, tong ertussen), het meest als het 3D-model. Op 1x leest het als een tandige grijns. Beperking: de opening is 3 rijen hoog, dus de tanden vullen een groter deel ervan dan bij Haunter (5 rijen); de mond oogt daardoor wat meer dicht dan in de artwork.
**Favoriet R**: de ondertanden lezen op 12x en 6x echt als tanden (W); bij S zijn ze 1-px pinnetjes die op 1x wegvallen.

## T (na "R en S gaan niet naar Jordi": mond bijna dicht)
Reproduceren: `python3 maak_t.py` (gebruikt `rek.py`) · `python3 controle.py` · `python3 vel.py` (vel: refs-mondcrops | v7 | R | T).
- **Oprekken zonder tekenen (`rek.py`)**: per kolom bestaande v7-rijen gedupliceerd; bovenlip blijft op y33. x20-28: rij 34 (donker) en rij 35 (tong) elk 1x (+2, opening y34-38, onderlip y39); x29-33 (rechter mondhoek, ring dichtbij): alleen rij 34 (+1). De zijkanten schuiven mee; de onderste bolrijen vlak boven de ring vallen weg. Bol boven de ring: overal ≥1 px (x24-28: y40; x29-32: y39).
- **Tanden** (bouw van Haunter G3 rij 39-44 en de pixel-ref: hoofdroze voet breekt de lip open, punt steekt uit, zwarte lijn langs de tand; ongelijk, Jordi: "niet allemaal precies hetzelfde"):
  - boven, ver (links) klein: voet (25-26,33), punt (25,34); dichtbij groot: voet (29-31,33), (30-31,34), punt (30,35), zwarte lijn links (29,34-35); rechte lip ertussen (27-28,33).
  - onder, kleine bultjes in de onderlip: dichtbij punt (28,37) met zwart aan beide kanten, voet (27-29,38-39); ver punt (24,38), voet (24-25,39), inkeping (26,39). Kinschaduw (27-28,40) 2->7 zodat de voet aan het hoofd vastzit.
  - Verspringend: punten boven x25/x30, onder x24/x28. Donker blijft y34-35, tong y36-38 zichtbaar.
- Controle: diff alleen in x20-33, y33-40 (mondzone), silhouet 0, palet v7, P, transparantie 0. Ogen 0.
- Afgevallen tussenstappen: T met gelijke tanden (zoals R), T2 (kleinere ondertanden: lazen niet).
- **Oordeel**: naast G3 en de pixel-ref op 12x/1x nu een open grijns met 2 ongelijke V's boven, kleine bultjes onder, donker + tong ertussen: zelfde bouw. Zwak punt: de opgerekte linker mondhoek wordt een 2 px brede zwarte balk van 5 rijen (x20-22, y34-38; ontstaat vanzelf door het dupliceren); de mond is daardoor hoger dan bij Haunter.

## T2 (alleen herkleuren van T, `maak_t2.py`)
- Linker mondhoek: de 2x5 zwarte balk is nu een 1-px lijn die schuin naar de hoek loopt: (20,33),(20-21,34),(21,35),(21,36),(22,37),(23,38), zoals v7/C3 en Haunter G3. Herkleurd: (20,35) 1->7, (22,35) 8->10, (23,35) 1->10, (22,36) 1->5, (21,37) 1->7, (21,38) 1->7. Het hoektandje (22,34) blijft zoals in v7.
- Rechter mondhoek is al een 1-px lijn ((33,33-35),(32,36),(31,37),(29-30,38)): ongewijzigd.
- Gecontroleerd op 12x naast G3/pixel-ref: tandlijnen 1 px; niets anders dikker dan in die sprites. Diff alleen in de mondzone, silhouet 0.
