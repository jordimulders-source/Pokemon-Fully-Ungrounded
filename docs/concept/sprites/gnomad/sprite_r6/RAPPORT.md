# Gnomad – sprite r6 (maker-agent, 22 nov)

Basis: `../sprite_r5/gnomad.png`. Script: `r6.py A|B`. Een assert bewaakt dat er alleen pixels in lijf, broek, riem en gesp veranderen.
Jordi: "nee want hij is nu iets te vierkant, voor het ontwerp is het goed als dat net afwijkt, evenals de riem zelf die niet moooi op zichzelf aansluit".

## Riem: één doorlopende boog
- In r5 lag het laagste punt van de boog bij x25, rechts van de gesp. Daardoor lag het stuk links van de gesp 1 rij hoger dan het stuk rechts: het sprongetje.
- Nu ligt de voorkant van de bol (driekwart) bij de gesp. Van de linkerflank tot x29 loopt de riem vlak: bovenlijn op rij 44, band 45–47, onderlijn 48, links en rechts van de gesp op één lijn.
- Daarna buigt hij vloeiend omhoog naar de rechterflank (bovenlijn 44 → 42 bij x40).
- Gecontroleerd door per kolom de boven- en onderrand uit te lezen: links x15–17 en rechts x24–29 allebei 44/48. Een proef met een steile boog links gaf weer 1 rij verschil en is verworpen.
- Opbouw blijft als in r5: zwart, 3 rijen bruin, zwart; glansrij links in lichtbruin.
- Buitenlijn links (x14–15, y43–46): blauwe selout van de oude broekgrens vervangen door roze selout boven de riem en zwart langs de riem.

## Gesp (x18–23, y43–49, niet groter dan r5)
- Het staande gat is terug naar 2×3. De voorkant is crème met een glanspixel linksboven, de rechterkolom lichtbruin als zijkant.
- **A (trapezium):** de rechterkant is 2 px korter (hoeken rechtsboven en rechtsonder weg), zodat hij terugwijkt mee met de bol.
- **B (afgeronde hoeken):** alle vier de hoeken weg. De zijden kunnen op 6 px breedte niet nog boller.

## Diff t.o.v. r5
| | riem + roze/blauw eromheen | gesp | elders |
|---|---|---|---|
| A | 41 | 19 | 0 |
| B | 43 | 18 | 0 |

Controle: geen lichte kleur op de buitenrand, geen losse zwarte pixels. Zwart is 21,5 % (A) en 21,4 % (B); r5 had 21,6 %.

## Eigen zwakke punten
- Doordat de riem links lager ligt (rij 44 in plaats van 42–43), is de zichtbare broek onder de riem kleiner geworden.
- Het verschil tussen A en B is op 1× klein.
