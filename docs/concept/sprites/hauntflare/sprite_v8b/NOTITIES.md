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
