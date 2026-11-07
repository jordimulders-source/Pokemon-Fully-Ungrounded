# Sapa Inca – ronde 5 (kleine bewerking op ronde 4)

Basis: `ronde4/sapa_inca.txt`; de wijziging staat onderaan in het blok "ronde 5". Verder: `bouw.py`, `controle5.py` (diff per zone t.o.v. ronde 4), `vel.py` → `vel.png` (linkerkant op 6× en gezicht op 10× naast ronde 4), `kijk.py`. Draaien vanuit de repo-root.

Jordi: "het is nu niet helemaal duidelijk meer dat hij een staf vast heeft, misschien onderin de staf nog iets meer ervan tonen? zodat de vleugel het grotendeels overlapt maar niet volledig".

## Wat er veranderde
- De staf komt onder de vleugelpunt weer tevoorschijn, **op dezelfde lijn en met dezelfde dikte** als erboven: x14–16, 3 px, gouden schacht (y) op x15 met de roestbruine vaan (t) aan beide kanten (rij 47–49). Daarna buigt hij in twee rijen naar rechts (rij 50–51) en eindigt hij tegen de zwarte rand van het donkere lijf (21,51) / (19,50), net als eerst. Achter de vleugel (rij 38–46) blijft hij verborgen.
- De vleugel is alleen onderaan aangepast: de linkerpunt van de onderste pen is 1–2 px ingekort (3 px: (15,47), (16,47), (16,48)).
- De oude korte veer (16–18,49) en (17–19,50) is opgenomen in de nieuwe bocht; daar is nu donker lijf.

## Diff t.o.v. ronde 4 (`controle5.py`)
| Zone | Gewijzigd |
|---|---|
| kroon | **0 px** |
| gezicht en ogen | **0 px** |
| opgeheven rechtervleugel | **0 px** |
| buik | **0 px** |
| rechterpoot + staartaanzet | **0 px** |
| linkerpoot | **0 px** |
| staf + zon boven de vleugel | **0 px** |
| linkervleugel (y36–46) | **0 px** |
| staf onder de vleugel + onderste pen + aansluiting lijf (x12–24, y47–53) | 24 px: 15 staf (nieuw/doorgetrokken), 3 vleugelpen ingekort, 6 donker lijf/omlijning waar de oude veer zat en waar de bocht aansluit ((17–19,49), (20,50), (21,51) K, (22,51)) |
- Alpha: +13 px (de doorgetrokken staf onder de vleugel), −0; totaal 1640 px.
- 0 open randen; 15 kleuren + transparant; aandeel zwart 0,13.

## Zelf gekeken (1×, 4× en 6× naast ronde 4)
- Op 4× en 6× zie je nu één doorlopende staf: boven de hand, onder de vleugelpunt weer tevoorschijn, en dan de bocht naar het lijf. Op 1× zie je onder de hand een gouden stukje dat aansluit op de bocht.

## Eerlijk: wat nog niet klopt
- Tussen rij 38 en 46 is de staf helemaal weg achter de vleugel (9 rijen). Op 1× lees je het bovenste en het onderste stuk niet altijd als dezelfde staf; het onderste stuk is maar 3 rijen recht vóór de bocht.
- De bocht (rij 50–51) is een korte diagonaal van 2 rijen; op 6× leest hij als een knik, niet als een zachte boog.
- De onderste pen is iets korter, waardoor de vleugelpunt links minder gekarteld is dan in ronde 4.

## Lessen
- Een staf die achter een vleugel doorloopt leest als één ding als hij aan beide kanten precies dezelfde kolom en dikte heeft (hier x14–16, schacht x15); laat de vleugel daarvoor wijken (pen inkorten) in plaats van de staf te verschuiven.
