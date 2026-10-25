# Olinguito v2: silhouet met de hand, ronde 2

Ronde 1 (`../silhouet.txt`) blijft staan als afgekeurde versie. Claude keurde die af: hij stond als een tafel, met vier verticale poten op een rij die als een kam lazen. De pose van de onderlaag ging verloren, er zaten spleten van 1 px tussen de poten, de kruin had een kroontje en de klauwen waren te klein.

**Bestanden:** `silhouet.txt` (64 × 64, `.`/`#`), `silhouet_1x.png` en `vel.png`. Op het vel staan:
- de B2-onderlaag;
- ronde 2 op 4×;
- ronde 2 half doorzichtig over de onderlaag, 2 px naar rechts en 2 omlaag;
- ronde 2 met de verre poten lichter;
- ronde 1 ernaast;
- alles ook op 1× (grijs en wit), naast Linoone, Zigzagoon, Poochyena, Growlithe en Sentret (1× en 4×).

## Maten
| | ronde 2 | ronde 1 |
|---|---|---|
| pixels | **1110** | 982 |
| box | 52 × 48 (x 2–53, y 10–57) | 47 × 42 |
| kop (oppervlak) | ±36 % | ±34 % |
| kop (hoogte, oor t/m kaak) | 25/48 = 52 % | 55 % |
| samenhang | 1 geheel; geen losse pixels (alleen klauwpunten, tenen en hak hebben 1 buur) | |
| spleten van 1 px tussen poten | **0** (gemeten per rij, y 38–57) | meerdere |

Het formaat is groter dan in ronde 1. Dat komt doordat de pose nu uitgestrekt is (een lange voorpoot naar voren en een verre achterpoot naar achteren), zoals op de onderlaag. 1110 px is fase-1-Zigzagoon-formaat (1127); de 950 haal ik niet zonder de poten weer dun te maken.

## Per punt van de keuring
- **Pose van de onderlaag:** over de onderlaag gelegd vallen de kop, de schuine voorpoot met de klauwen, de lage borst, de oplopende rug en de dij goed samen. Alleen de staart staat dichter op het lijf (Pokémon-verhouding).
- **Nabije voorpoot:**
  - begint onder de kop (schouder x 19–26, y 38) en loopt in één diagonaal naar linksonder, ver vóór de borst;
  - 7–8 px dik, met een pols: de poot buigt bij y 49–51 naar voren;
  - de klauwen staan vooraan op de grond (y 57).
- **Verre voorpoot:** opgetild en kleiner, achter de nabije (x 24–33, y 41–49). Hij hangt met de pols geknikt naar linksonder en de klauwen hangen omlaag; geen grondcontact.
- **Nabije achterpoot (gehurkt):**
  - een grote ronde dij die doorloopt in het achterlijf; de knie naar voren (x 34, y 43–45);
  - de scheen loopt schuin terug naar de hak (x 44);
  - de voet ligt plat naar voren onder de buik (x 31–44, y 50–52);
  - eronder een driehoek lucht (±x 34–41, y 46–50).
- **Verre achterpoot:** hoger en verder naar achteren, onder het achterlijf uit. De scheen loopt schuin naar achteren naar een zichtbare hak (x 53, y 41–43), daarna gaat de voet naar voren-omlaag (voet y 46–47, de hiel van de grond).
- **Vier fases:**
  - nabije voorpoot: vooruit en op de grond;
  - verre voorpoot: opgetild;
  - nabije achterpoot: gehurkt en dragend;
  - verre achterpoot: achteruit en afzettend.
  - Vier verschillende hoeken en hoogtes: grondcontact bij y 57, 52, 49 (opgetild) en 47. Geen kam meer.
- **Lucht:** overal minstens 2 px tussen naburige poten:
  - nabije en verre voorpoot: 4–5 px;
  - verre voorpoot en dij: 2–3 px;
  - dij en verre achterpoot: 2 px.
  - Alleen op de rij waar een poot uit het lijf komt, is de inkeping 1 px.
- **Romp:** de borst laag vooraan (y 37–40). De rug loopt vanaf een nekwig achter de kop schuin omhoog naar een hoger, rond achterlijf (y 26). De staart begint boven op de bil, gaat in een boog omhoog dicht op het lijf en eindigt in een haak naar links met lucht in de krul (3 px dik).
- **Kop:**
  - de kruin is één gladde boog (stappen 2-1-1-1-0); het rommelige randje en het verre oor zijn weg;
  - één rond oor van 8 × 5 bovenop, achteraan, als duidelijke bult met een inkeping eronder;
  - een hoog, rond voorhoofd, dan een kleine knik (stop) en een stompe snuit naar linksonder (punt x 2, y 30–32);
  - de kaak loopt terug onder de kop; een inham tussen kaak en voorpoot houdt de kop als eigen onderdeel.
- **Klauwen:**
  - nabije voorpoot: 2 Linoone-haakjes van 6 rijen, aan de basis 3 px breed. Ze lopen schuin naar voren-omlaag en de punt buigt terug. Tussen de twee zit 2–3 px lucht;
  - verre voorpoot: 2 haakjes van 4 rijen met 2 px lucht ertussen.

## Eerlijk: wat nog niet perfect is
- **Formaat:** 1110 px en een box van 52 breed, boven de richtlijn (950 en ≤ 48). Dat is bewust om de uitgestrekte pose te houden; zie hierboven.
- **De verre achterpoot is in één kleur het lastigste onderdeel.** Op 1× leest hij als poot met een hak; in de versie met de verre poten lichter is het eenduidig. In kleur moet hij in de schaduwtint, anders kan hij naast de staart als extra aanhangsel lezen.
- **De klauwen van de verre voorpoot** zijn op 1× klein (4 rijen), wel als twee haakjes te zien.

## Lessen
- **De pose eerst als lijnenskelet van de onderlaag overnemen** (schouder → pols → klauwpunt, heup → knie → hak → tenen), en pas daarna dikte geven. In ronde 1 begon ik met dikte, en dan schuift alles naar vier verticale palen onder een romp.
- **Na elke wijziging een spleetcheck per rij** (`#.#` onder de romp) uitvoeren: zo zie je meteen de kam-spleten van 1 px.
- **Een pixel die alleen op één rij uitsteekt** aan een poot (achterrand) leest als bultje; zoek met "≤1 buur" naar zulke pixels.
