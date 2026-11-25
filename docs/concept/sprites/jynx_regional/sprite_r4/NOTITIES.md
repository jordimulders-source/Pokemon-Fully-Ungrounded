# Regionale Jynx (sirene), ronde 4: alleen de rokvouw rechts

Jordi over r3: "eigenlijk wel heel netjes, op die horizontale streep in de jurk na". Bedoeld is de vouw op r3 rij 47, x33–46.
Basis is r3. Alleen die lijn verandert; het palet blijft gelijk.
Bouwen: `cd docs/concept/sprites/jynx_regional && python3 sprite_r4/bouw.py` (variant B: `... bouw.py B`), vel: `python3 sprite_r4/vel_r4.py`.

## Gemeten in het natieve model (`gereedschap/natief.png`, veerlijn L < 95, punten omgerekend naar sprite-coördinaten)
| stuk in het model | natief | sprite |
|---|---|---|
| schuine vouw | (57,66)→(61,68) | (37,47) → (38,48) (39,48) → (40,48) |
| aansluiting | (61–63,66) | (40–41,46) |
| bijna vlak stuk | (64–67,67) | (42–44,47) |
| naar rechts omlaag | (68,66)→(70,68)→(72,69) | (45–46,47) (47,48) (48,49) |

- Op x34–36 van rij 47 staat in het model geen lijn: natief u54–56, v65–67 is vlak (145). In r3 liep de lijn daar door tot de verticale vouw x33. Dat stuk is weg.

## r4 (9 px anders dan r3, allemaal in de rokzone x33–48, y45–49)
- Lijn → rok-midden (6 px), zoals de tint erboven en eronder: (34,47) (35,47) (36,47) (38,47) (39,47) (41,47).
- Rok-midden → lijn (3 px), op het modelpad: (38,48) (39,48) (41,46).
- **Het nieuwe pad:**
  - De lijn begint los bij x37, zakt naar rij 48 en sluit aan op de verticale vouw x40.
  - Daarna stapt hij één rij omhoog naar (41,46) en loopt via (42–44,47) naar de vouw x44 en verder naar rechtsonder.
  - Overal 1 px en doorlopend (8-buren).
- **Bewijs** (asserts in `bouw.py`): silhouet-diff 0, 0 px anders buiten x33–48 × y45–49, 16 kleuren incl. transparant.

## Variant B: `jynx_regional_r4_B_zonder_lijn.png` (11 px anders dan r3)
- **Waarom:** op deze schaal blijft het middenstuk van het model (natief v66–67 over u61–67) bijna vlak: x42–46 op rij 47.
- **Wat:** de dwarslijn valt helemaal weg tussen de verticale vouwen x33, x40 en x44; die vouwen blijven staan. De vrijgekomen pixels krijgen rok-midden.
- **Gevolg:** rechts van x44 grenst rok-midden nu zonder lijn aan rok-schaduw (rij 48). Het stukje vouw (47,48)–(48,49) blijft.
- Jordi kiest tussen r4 en B.

## Vel
`vel.png`:
- bovenaan r4 | r3 | model, 8×;
- close-ups 12× van de rok (r4 | r3 | model en r4 | B | model) en van de vouw (r4 | r3 | B | model);
- 1× op licht en donker naast Skinguin en Dundragoon.
