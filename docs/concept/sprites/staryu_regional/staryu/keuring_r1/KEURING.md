# Keuring r1 regionale Staryu (chocolate chip-koekje), verse keurder, 27 nov

**Oordeel: BIJNA.** De sprite volgt het model trouw. Er zijn vier kleine, gemeten reparaties nodig, waarvan één een harde lijnregel is. Daarna PASS.

Vel: `vel.png` (sprite 8× | model op dezelfde schaal 8× | Gen 3 Staryu 8×, met de punten gemarkeerd; onderaan 1× op licht, crème en donker naast model 1× en Gen 3 1×). Scripts: `toon.py` (deegtoon van de sprite tegenover de modelhelderheid per spritepixel), `clusters.py` (vlekjes < 3 px), `vel.py`.

## Blind oordeel (vóór NOTITIES.md)
**Eis 1, trouw aan het model.** Silhouet, armhoeken en maat (41×43) kloppen. Alle 11 chips staan op hun modelplek, met ongeveer de goede maat en een glanspuntje linksboven. Het juweel is rond, met een ring, een glans linksboven en diagonale strepen in dezelfde richting als het model. De barst- en naadlijnen naar de inkepingen staan erin. Niets is toegevoegd of weggelaten dat je op 64 px zou zien.

**Eis 2, Gen 3.**
- **Volume (eerst getoetst):** voldoende, en zoals het model. Elke arm heeft licht aan de linker- en bovenkant en een schaduwsikkel van 2–3 px rechts en onder (rechterarm r. 29–35, linkerarm-onderkant r. 30–35, beide benen onder en rechts). Het midden is middentoon en de naden geven reliëf. Gemeten: 492 van de 618 deegpixels (80 %) vallen in dezelfde toonklasse als de modelhelderheid, en de afwijkingen liggen verspreid, op één zone na (punt 4). Het model heeft getoaste randen vooral rechts en onder; links en boven is de rand ook in het model licht. Een donkere rand rondom zou dus een afwijking van het model zijn.
- **Contrast:** deegtinten L 203 / 170 / 136, selout 95, zwart. Dat zijn stappen van ±33–35, binnen de norm.
- **Belijning:** 1 px. Selout (2) zit aan de lichtkant (linker- en bovenranden), zwart aan de schaduwkant (rechts en onder). Er is één plek waar zwart en selout om en om liggen (punt 1).
- **Banding en pillow shading:** geen pillow shading. De 1-px schaduwband langs de rechterkant van het rechterbeen (r. 38–47) en de lichte band links op het linkerbeen komen uit het model (gemeten) en mogen blijven. De m-lijn op x18 r. 48–51 is een barst uit het model (p15 ≈ 120) en is dus geen dubbele lijn.
- **Leesbaarheid op 1×:** het koekje, de chips en het juweel lezen goed. De barstjes zijn subtiel, zoals in het model.

## Reparaties (alleen deze; geen andere pixels)
1. **Lijn om en om bij de linkerarmtip (hard).** De linkerrand loopt nu (11,27) b, (11,28) b, **(11,29) K**, (12,30) b, (12,31) K: zwart en selout wisselen elkaar af. Zet **(11,29) → 2 (selout)**, zodat de tip lichtkant is en zwart pas begint bij (12,31), aan de onderkant. Het model is daar ook licht (gem. (159,113,85), anti-aliased). Dit is 1 px.
2. **Chip plakt aan het juweel.** De chip links van het juweel heeft zijn rand (6) op **(24,32) en (24,33)**, direct tegen de juweelring op x25. Op 1× wordt dat één donkere klodder aan het juweel. In het model zit er deeg tussen: de gemiddelde modelhelderheid van die cellen is 142 en 119, een mengsel van chiprand en deeg, en de deegschaduw (3) heeft L 136. Zet beide pixels **→ 3**. De chip blijft dan x19–23, net als in het model.
3. **Chipbruin als barst (losse kruimel).** Op **(20,36)** en **(29,46)** staat chipmidden (7, L 66) als enkele pixel in een naadlijn. Op 1× leest dat als een kruimel of losse chip die het model niet heeft. Gemeten modelhelderheid: (20,36) gem. 94 → **2** (selout, L 95; de naad uit de inkeping is een binnenlijn in de donkerste eigen tint). (29,46) gem. 118 → **3** (L 136). Dit is waarschijnlijk een klassenfout in `klassen.py`: een donkere naad die als "chocolade" werd ingedeeld.
4. **Bovenarm volume naar het model.** Het model splitst de bovenarm in een lichte linkerhelft en een schaduwrand van 2 px rechts. In de sprite is de arm vrijwel één middentoon met 1 px schaduw. Gemeten (gem. modelhelderheid):
   - (30,13) 150, (31,13) 135, (31,14) 141 → **3**;
   - (29,15) 186, (29,16) 197 → **5**.

   Dit zijn 5 pixels uit de modelhelderheid; niets wordt gladgestreken.
5. *(Optioneel, op 1× onzichtbaar.)* De juweelring onderaan loopt (25,35) r, **(26,35) R**, (27,35) r. Volgens de eigen regel van de maker ("onder/rechts donkerst") wordt (26,35) → 9 voor een gesloten ring.

**Niet doen:** niets gladstrijken of rustiger maken. De barstjes, de lichte plukjes in het deeg en de 1-px diagonale juweelstrepen komen uit het model en blijven.

Ter info (geen reparatie): de zwarte onderkant van de modelchips is iets dikker dan de chiprand (6) in de sprite. Het verschil is minder dan een halve pixel (cellen onder de chips: gem. 83–127), dus het telt niet.

## Na het lezen van NOTITIES.md
De notities en mijn meting komen overeen: de reductie is eerlijk, er is niets getekend, het silhouet is ongewijzigd en de 11 chips en 10 glanspixels kloppen. De twijfels van de maker over het juweel en de barstjes deel ik niet: op 1× leest het als glanzend juweel en de barstjes staan op modelplekken. Wat de maker niet zag zijn punt 1 (de controle "geen losse zwarte pixels" vangt geen afwisseling), punt 3 (chipklasse op een naad) en punt 4.
