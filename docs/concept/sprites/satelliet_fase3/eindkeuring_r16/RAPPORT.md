# Eindkeuring r16 (Dragonfly Cave), ruimtestation fase 3

**Oordeel: PASS, met 0 gewijzigde pixels.** `sprite.png` is gelijk aan `sprite/r16/sprite.png` (pixeldiff 0). Het bestand is opnieuw opgeslagen met transparency=0.

## Wat er veranderd is ten opzichte van eindkeuring_r15 (PASS)
- Er zijn 38 pixels veranderd, allemaal in rij 54–61. Daar staat nu r12.
- Rij 0–53 zijn gelijk aan eindkeuring_r15 en rij 53–55 zijn gelijk aan r12. De naad sluit dus zonder overgang.
- De onderste rij is nu 55. Bbox: x 2–60, y 12–55.

## Vaste maten (zelf nageteld)
| Maat | Telling | |
|---|---|---|
| PB: breedte 6 px | x32–37: lijn 32 en 37, lichte rand 33, vak 34–36 | ok |
| PB: 3 vakken | bovenrand (34,14)/(35–36,15). Lijnen (34,17)/(35–36,18) en (34,21)/(35–36,22). Vakken 2/3/3 px | ok |
| PF: breedte 6 px | x32–37, gelijk aan PB | ok |
| PF: 3 vakken, zelfde trapje als PB | bovenrand (34,41)/(35–36,42). Lijn (34,44)/(35–36,45). Vak 1 is 2 px, zoals PB vak 1. Vak 2 is zichtbaar tot PE-rand (34,46)/(35–37,47). Bij steek 4 valt het einde van vak 3 (±rij 52) binnen PE: PE loopt bij x34–37 van rij 47 tot 54 | ok |
| PF eindigt achter PE | onder rij 53 geen PF-pixel. (36,54)=11 is de donkere PE-vaktint, de PE-punt | ok |
| Stok gecentreerd | boven (34–35,27), onder (35,40), midden PB/PF 34,5 | ok |
| Panelen voor/achter 4 vakken | PE: 4 (lijnen (30,47)→(27,50), (34,48)→(31,51) en (36,50)→(34,53), rechtervak 11). PD: 4. PC: 4 (2 d-vakken en 1 b-vak links van de bol, 1 b-vak rechts ervan). PA: 4 (d \| b \| b achter PB \| b rechts van PB) | ok |
| Sprite tot rij 55 | laatste pixel (36,55) | ok |
| Ogen: ring+iris+pupil, geen wit | ongewijzigd sinds r15 (rij 28–33 en 46–52 diff 0) | ok |
| Bollen rond | ongewijzigd sinds eindkeuring r15 (cirkelfit ≤0,55 px) | ok |

## Toets (DC r. 80–170 en 340–470)
- **Omlijning PF/PE (rij 40–55, kol 26–43):**
  - PF: links outline base navy (2). Rechts, aan de schaduwkant, zwart (1). Bovenhoek (37,42) navy.
  - PE: bovenrand navy (30–31,45) · (32–34,46) · (35–37,47) · (38–40,48), met een outline highlight (12) binnen de lijn. Rechts en onder zwart, als schaduwkant.
  - Nieuwe onderrand: trap (24–27,51) · (28–30,52) · (31–33,53) · (34–35,54) · (36,55), aan de rechterkant (37,54) · (38,52–53) · (39,51) · (40,50) · (41,49). Overal 1 px en zonder dubbele zwarte pixels. Wat de scan als "enkel" meldt, zijn alleen diagonale trapstappen en de twee punten (36,55) en (41,49).
- **Schaduw:** het licht valt linksboven. Het PE-vak links is licht (14), rechts het donkerste vak (11). PF vak 1 is licht (14), vak 2 midden (13).
- **Kleurtinten:** het paneel loopt van 12 via 14 en 13 naar 11. Het palet is ongewijzigd.
- **Ruis:** er zijn geen losse pixels in de zone. (34,53)=14 is het taps eind van lijn 3, en dat stond al zo in r12 en r15.
- **Kleuren:** 16, transparant meegeteld.

## Ter info (niet aangeraakt, geen nieuwe fout)
- (25–26,47) is paars (8), op de linkerbovenhoek van PE onder de buis. Het staat er al sinds r9, ook in elke keuring en elke versie die naar Jordi ging. Als het moet verdwijnen, is dat Jordi's keuze. Ik heb het niet gewisseld, omdat het onduidelijk is of het buisband of paneelrand is.
- De stok onder de hub (35,40) is 1 px. Boven is hij 2 px (34–35).
