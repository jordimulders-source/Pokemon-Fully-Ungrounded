# Silicobra (Uyuni) – ronde 5 (vanaf ronde 4)

Jordi (letterlijk): "ok prima, de pekelzak mag aan de bovenkant nog iets meer. Daarnaast mag het hoofd van Silicobra nog een klein beetje meer een lijn hebben zodat we de zoutkuif los kunnen zien, althans, ik wil eens testen hoe dat eruit ziet"

Bestanden:
- **A** `silicobra_uyuni.png` + `silicobra_uyuni_raster.txt`: ronde 4 met een hogere band.
- **B** `silicobra_uyuni_kuiflijn.png` + `silicobra_uyuni_kuiflijn_raster.txt`: de test, A plus de kuiflijn.
- `vel.png`: ronde 4, A en B naast elkaar op 4× en 1×, licht en donker.
- `scripts/`: `handwerk.py` (de segmenten met de hand), `bouw.py`, `controle.py`, `vel.py`.

Het palet is hetzelfde als in ronde 2 en 4: 15 kleuren, transparency=0.

## A: band hoger
- **Bovenrand:** de bovenrand van de halsband ligt 1 px hoger. Aan de zijkanten zat hij op rij 33 en in het midden op rij 36; nu loopt hij van rij 32–33 aan de zijkanten tot rij 35 in het midden. Hij blijft een ∪-boog met trapjes van 3–6 px.
- **Linkerkant:** links blijft de band op rij 33, direct onder de kinlijn, en gaat zo onder de kin door.
- **Glans en belletjes:** het glanslicht schoof mee en volgt de nieuwe bovenrand 1 rij lager, op (21–23,34) en (24–25,35). De belletjes en de onderrand zijn gelijk aan ronde 4.
- **Silhouet:** ongewijzigd (0 alpha-pixels).

## B: kuiflijn (test)
- **Lijn:** de oorspronkelijke kopomtrek van Silicobra, die onder de kuif ligt, is opnieuw als lijn getekend: 30 pixels van het voorhoofd (20,17) over de bovenkant (rij 16) en langs de achterkant (x=39–41) tot de nek (40,31). Alle lijnpixels liggen binnen de oude kopomtrek.
- **Kleur:** lichter grijs-oker `h` aan de lichtkant (voorhoofd en bovenkant links), donker warm grijs `K` op de rest, geen zwart.
- **Effect:** de kuif leest daardoor als een losse rand van platen op een ronde kop, een soort helmrand.
- **Ongewijzigd:** gezicht, oog, snuit en silhouet; alleen pixels op de lijn zijn veranderd.

## Diff (`scripts/controle.py`)
| Vergelijking | Zone | Alpha | Kleur |
|---|---|---|---|
| A t.o.v. ronde 4 | nek (rij 31–44) | 0 | 26 |
| A t.o.v. ronde 4 | kop en rest | 0 | 0 |
| B t.o.v. A | kuiflijn (kop) | 0 | 29 (1 lijnpixel was al `K`) |
| B t.o.v. A | nek en rest | 0 | 0 |

Open randen 0 en losse pixels 0, zowel in A als in B.

## Eerlijk oordeel
- **A:** de band zit voller onder de kin en de kop en blijft netjes gebogen.
- **B:** de kuif leest duidelijk als een apart onderdeel en niets brokkelt af. De lijn volgt exact de oude kop van Silicobra, dus bovenop loopt hij net zo vlak (rij 16, x=23–32) als de bovenkant van de originele sprite. Of Jordi die extra lijn mooi vindt, is een smaakkeuze; daarvoor is dit de test. Technisch zie ik in A en B geen open zwak punt.

## Lessen
- Een "losse" kuif of helm maak je het goedkoopst door de oude omtrek van de basis eronder terug te tekenen: binnen het silhouet, ±30 px, niets eraf.
