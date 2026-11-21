# Onweerswolk-Swablu frontsprite, ronde 5

Jordi over r4: "de mond van swablu is nog niet herkenbaar genoeg, de mondlijn, verder vind ik hem wel goed".
Bestanden: `swablu_r5.png`, `swablu_r5_8x.png` (op wit), `vel.png` (`vel5.py`: r5 | r4 | model | echte Swablu op 8× / snavel-close-up 20× (meer dan de gevraagde 12×): r5 | model | echte Swablu / 1×), `bouw.py` (op `sprite_r4/swablu_r4.png`).

## Wijziging: alleen de mondlijn, 5 px (diff buiten de snavel = 0, met assert bewezen)
De model-mondlijn loopt natief van (93,59) via (94–97,61), (99–100,60) en (102,59) naar (103–104,58). Omgerekend naar de sprite is dat de stijgende lijn **(21,31) (22,31) (23,31) (24,30) (25,30)**. Die pixels zijn nu selout donker (46,60,78), de donkerste tint zonder zwart.
- In r4 waren ze wolk midden ×3, snavelwit en wolk licht: de lijn ging op in de grijze onderkaak.
- Daaronder blijft de onderkaak wolk licht ((24,31) (25,31)), met de onderlijn wolk donker eronder. Erboven blijft het witte snavelvlak.
- Zoals bij de echte Swablu en in het model deelt de lijn de snavel nu in een witte bovenkant en een grijze onderkaak.

## Twijfel
Door de lijn houdt de grijze onderkaak maar 2 px over. Op 1× leest de mond nu als een donker streepje schuin door de snavel.
