# Sapa Inca – ronde 5b (reparatie op ronde 5)

Basis: `ronde5/sapa_inca.txt`; de reparatie staat onderaan in het blok "ronde 5b". Verder: `bouw.py`, `controle5b.py`, `vel.py` → `vel.png` (linkerkant op 6× en gezicht op 10× naast ronde 5), `kijk.py`.

Jordi: "nu is er een zwart vlak tussen staf, lichaam en vleugel in wat er niet mooi uitziet".

## Wat er veranderde (alleen x12–24, rij 40–53)
- **Vleugelpunt in vleugeltinten:** m-basis, l op de belichte bovenrand bij de pols, twee schuine penscheidingen in d in plaats van K. K staat nog alleen op één plek: als doorlopende onderrand van de vleugelpunt van (12,43) via (14–16,46) naar (17–18,47), waar de punt over de staf en de flank ligt.
- **Flank erachter:** de schaduwtint d met een zachte lichte rand (m) langs de staf, zoals het lijf links; de oude K-streepjes zijn weg.
- **Staf:** loopt ongewijzigd door (boven de vleugel x14–16, eronder rij 47–51). De K-wig in de bocht is weg; de bocht ligt nu tegen m/d van de flank en eindigt bij één K op (21,51), de onderhoek van het lijf.

## Diff t.o.v. ronde 5 (`controle5b.py`)
- Alpha-diff: **0**.
- Binnen de zone x12–24, rij 40–53: **45 px**. Buiten de zone: **0 px** (kroon, gezicht, ogen, buik, poten, rechtervleugel, staartaanzet, staf boven de vleugel ongewijzigd).
- K-pixels in x17–23, rij 42–52: 12 → 4.
- 0 open randen; aandeel zwart 0,13 → 0,12.

## Zelf gekeken (1×, 4×, 6× naast ronde 5)
- De zwarte klont is weg: op 6× zie je een vleugelpunt met pennen, daarachter een donkere flank en de staf ertussen. Op 1× is het geen zwart gat meer.

## Eerlijk: wat nog niet klopt
- De vleugelpunt is nu lichter (m) dan het bovenste vleugeldeel (d). Op 1× leest de hand daardoor als een lichtere klomp onder de donkere bovenarm; de overgang op rij 39/40 is vrij abrupt.
- De bocht van de staf blijft een korte diagonaal van 2 rijen.

## Lessen
- Penscheidingen en omlijning in dezelfde zwarte tint naast een donkere flank vormen samen een zwart vlak; geef pennen de schaduwtint (d) en bewaar K voor één doorlopende onderrand.
