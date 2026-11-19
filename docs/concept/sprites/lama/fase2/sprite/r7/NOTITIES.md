# Llamauler r7: eindkeuring Dragonfly Cave + kleine reparaties (19 nov)
Basis `../r6/lama.png`. Gekeurd op 8× naast Mareep, Flaaffy, Ponyta, Girafarig en Stantler (`vel.png`: model | r7 | r6, daaronder 1× en 2× op licht en donker).
`bouw.py` maakt r7 uit r6 (assert alfa-diff 0), `vel.py` maakt het vel.

**Alfa-diff met r6: 0.** Pixels veranderd: **11**, plus één paletkleur (index 6). 16 kleuren incl. transparant.

## Punten
| # | Punt (DFC/KERN) | MOET/MAG | Pixels (x,y) | Gedaan |
|---|---|---|---|---|
| 1 | Open rand: bovenste pixel van het linkerkwastje is licht rood (A) op de buitenrand, zonder omlijning boven/links | MOET | (11,5) | A → 1 (zwart, zoals de kap van het rechterkwastje (23,4)) |
| 2 | Open rand onder de buik tussen de achterpoten: midden/licht bruin (3/4) op de buitenrand; schaduwkant hoort zwart; (41,49)/(45,50) donkerbruin 2 tussen zwart zou zwart/donker om en om geven | MOET | (40,48) 4→1; (41,49) 2→1; (42,50) 3→1; (43,50) 4→1; (44,50) 3→1; (45,50) 2→1 | onderrand haunch dicht in zwart |
| 3 | Verre voorpoot: bovenkant direct onder de buik in de lichtste tinten (6,5,5,4), lichter dan de nabije poot; KERN "verre poot in schaduwtint", DFC "slagschaduw volledig in schaduwkleur" | MOET | (22,48) 6→3; (23,48) 5→3; (24,48) 5→3; (25,48) 4→3 | slagschaduw 3, zoals de nabije poot (20,48) |
| 4 | Kleurramp vacht: hooglicht 6 (231,181,128) lag maar ±22 helderheid boven basis 5 (Gen 3: ±30–40; Ponyta 162→204→239) | MOET (meetbaar) | palet index 6 | → (238,192,140), stap ±34; tint gelijk (±32°) |
| 5 | Licht vlekje aan de schaduwkant van de kaak (6 onder een 3) | MAG, niet gedaan | (22–23,18–19) | leest als wolkrul (model heeft lichte krullen daar); laten staan |
| 6 | Lichte rand aan de rechter (schaduw)kant van de onderste staartkwast | MAG, niet gedaan | (45–47,35–36) | idem, eigen wolkwab met lichte bovenkant |
| 7 | Crotch-spleetje van 1 px tussen de achterpoten | MAG, niet gedaan | (40,49)–(41,50) | dichtmaken = alfa-wijziging; met (40,48) zwart leest het als gewone kruisrand |

Verder ok: buitenlijn 1 px en overal 1 of 2 (script: geen open randen meer), licht linksboven, geen pillow shading (nek en lijf licht links, 4/3 rechts en onder), geen dambord (de 3-boogjes op het voorhoofd (12–19,11–12) zijn wolkrullen), rode ramp (58/87/119) en grijs ok, 3/4-pose, alle poten/oren/kwastjes verbonden.

## Ter info voor Jordi (ontwerp/pootstand, niet aangeraakt)
- Voorpoten kruisen in de sprite als een X (rij 48–52); in het model staan ze naast elkaar (nabij licht, ver donker). Pootstand is bevroren.
- Halsband is een rechte horizontale band (rij 29–31); in het model licht gebogen.
- Paletkleur 6 is iets lichter (punt 4): vergelijk r7 en r6 op het vel; terugzetten = één regel in `bouw.py`.
