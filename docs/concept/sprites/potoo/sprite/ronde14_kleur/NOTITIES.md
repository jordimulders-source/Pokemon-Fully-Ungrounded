# Ronde 14 kleur (maker) — notities
Basis: `../ronde13_standen/raster_85.txt` (vorm goedgekeurd). Omtrek bewezen gelijk: `zet.py` meldt alpha-diff 0 met `basis_85.txt` (ook `../controle.py raster.txt ../ronde13_standen/raster_85.txt`: alpha-diff 0). Geen randpixel rechtgetrokken.
Werkwijze: elke ronde is een bestand met rijen als met de hand gezette segmenten `(x, "pixels")` (`r1.py` volledig, `r2.py`–`r4.py` overschrijven delen); `zet.py` zet ze in het raster en controleert de omtrek. Geen gegenereerde patronen. Palet `palet.py` → `normal.pal` (15 kleuren + transparant).

## Ronde 1 (`r1.py`)
Hele sprite rij voor rij: kop met licht linksboven en selout, hoornplaat + haakje van 2 px, muil in banden onder de snijrand (slagschaduw 9, verhemelte C, dan B/A, keel 9), lippen D rondom, halsrand als tint 3 i.p.v. zwarte lijn, vleugel van schouder tot over de staart, takschaduw, borst met U-schubjes, staart met banden.
Eigen oordeel: muil las als "schaal met rand" (lip rondom) en de lichte C-band onder de snijrand als glasglans; U-schubjes = bakstenen; grijze nek als sjaal.

## Ronde 2 (`r2.py`) — vooral snavel en muil
- Haak groter (x10–12, y12–16), punt donker en terug gekruld, met zwarte rand naar de muil; snijrand E vóóraan, taps naar de zwarte mondlijn.
- Muil opnieuw: geen slagschaduwband meer; verhemelte vooraan licht (C/B, naast de donkere haak zodat die loskomt), naar achteren donker; keel 9 achter bij de mondhoek; kaakbodem lichter (B → C) naar de punt; lip D alleen langs de verre kaak en het voorste deel van de nabije kaak, de mondhoek blijft donker.
- Keel/borst onder de kaak licht met slagschaduw onder de kaak; T-schubjes; staart donkerder met minder banden.

## Ronde 3 (`r3.py`)
- Onderkaak als eigen vorm: lichte kaakrand (6) langs de muil, 5, schaduw 4 naar de halsrand en onderaan.
- Vleugelveren alleen bovenaan belicht (onder rij 38 geen witte strepen meer), alleen de voorrand blijft licht.
- Borst: korte neerwaartse streepjes (3 px, 4) i.p.v. T-schubjes.

## Ronde 4 (`r4.py`)
- Keelspleet 3 px (1) in het diepste punt, zoals de spleetjes op de leidraad. Keurvel gemaakt.

## Zelf nog zwak (eerlijk)
- **Haak/bovensnavel** is op 1× klein; leest als snaveltje, maar het "imposante" zit nu vooral in de muil. Als de keurder de snavel mist: hoornplaat 1 tint lichter/warmer of de haak 1 px langer (binnen de omtrek, ten koste van de muil linksboven).
- **Muil**: de diepe keel is een groot egaal donker vlak; het verhemelte "vangt licht" (Jordi) maar is op de foto juist donker — bewuste keuze, maar controleren of het nog leest als binnenkant van een snavel en niet als een gat.
- **Halsrand** leest als lijn, niet als verenkraag.
- **Vleugel** leest als planken (lange evenwijdige lijnen); vleugelpunten over de staart zijn niet als punten te zien.
- **Takschaduw** kan als riem lezen; de staart is wat rupsachtig (banden).
- **Schorsstreepjes** (7) lezen als losse staafjes; het vlekje op de staart als vuil.
- Controlescript: geen open randen/gaatjes; 81 tintclusters < 3 px, vrijwel allemaal diagonale lijnen (lippen, kaakrand, halsrand, vleugelrand) en de borst-/schorsstreepjes; dat moet de keurder beoordelen.
- Niet blind getest.
