# Onweerswolk-Swablu frontsprite, ronde 6

Jordi over r5: "de originele swablu heeft nog heel subtiel een iets lichtere tint om de zwarte pixels in het oog heen, probeer hetzelfde te doen. wat betreft de mond, de lijn is te hard en 1 pixel te veel naar links, het zijn ook net teveel 2 lijnen, dat kan misschien iets netter, kijk ook naar hoe de originele swablu met tinten en schaduw speelt".
Bestanden: `swablu_r6.png`, `swablu_r6_8x.png` (op wit), `vel.png` (`vel6.py`: r6 | r5 | model | echte Swablu 8× / oog+snavel 20×: r6 | model | echte Swablu / 1×), `bouw.py` (op r5).

## Studie echte Swablu (oog en snavel)
- **Oog:** zwart (32,34) (31,35) met glans (31,34). Recht ernaast staat donker blauwgroen (56,104,128): links van de glans, erboven, en rechts van het onderste zwart. Dat is een tint tussen zwart en lijf; schuin ernaast zit middenblauw.
- **Snavel:** geen harde mondlijn. Wit boven, dan lichtlila en lila schaduw, grijs onderaan; de bek leest uit die tintstap.

## Wijzigingen: 12 px, alleen oog en snavel (assert: diff elders 0)
- **Oog (3 px):** (27,28) links van de glans, (29,27) rechtsboven het zwart en (30,29) rechts van het onderste zwart: vogel midden → vogel donker (68,90,110). Dat zijn dezelfde plekken als bij Swablu, als subtiele halo; geen volle ring.
- **Mondlijn (5 px):** begint 1 px naar rechts: (21,31) → wolk midden, zoals de snavelrand erboven. De lijn zelf (22,31) (23,31) (24,30) (25,30) gaat van selout donker naar wolk donker (96,108,126): zachter, en sluit rechts aan op de rechterrand in dezelfde tint. Het wit erboven blijft (licht boven de lijn).
- **Geen tweede lijn (4 px):** de onderrand (22–25,32) gaat van wolk donker naar wolk midden. Die leest nu als schaduw onder de onderkaak; de onderkaak (24,31) (25,31) blijft wolk licht. Van boven naar onder: wit → donkere lijn → licht → midden.

## Twijfel
De halo is maar 3 px; op 1× is hij nauwelijks zichtbaar, wat "heel subtiel" ook vraagt.
