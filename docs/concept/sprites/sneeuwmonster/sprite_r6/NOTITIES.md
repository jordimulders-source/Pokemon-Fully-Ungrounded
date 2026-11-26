# Sneeuwmonster r6
Basis r5. Ogen bevroren (assert in `bouw.py`). Jordi: "linkerstukje van de kuif ook niet [rond] en linkerkant van het hoofd is ook hoekig"; daarna "de knopen zijn te recht" · "hij staat in driekwart".
Ruimer mandaat (Claude): dekking ≥ .30 mag erbij en ≤ .60 mag eraf, alleen richting de modelvorm. Er is niets > .60 weggehaald.

## Hoofd links (varianten A en B)
Modelrand (0,5-dekking), r16–28: 25,7 · 24,6 · 23,5 · 22,6 · 22,3 · 21,7 · 21,2 · 20,6 (4×) · 21,1 · 21,2. Gen 3-patroon: ronde lijven met horizontale stappen bovenaan en steeds langere verticale stukken naar de zijkant (Igglybuff `_gba`: 31,30,30,30,28,26,25,24,24,23,23,21,20,20; Marill vergelijkbaar).
- **A (licht), 6 px:** randpixel per rij 26,25,24,23,22,22,21,21,20,20,20,21,21. Trap 1-1-1-1, dan verticaal 2-2-3, kin 2. Bij: (20,24–26) dekking .45.
- **B (sterker), 15 px:** 26,24,23,22,22,21,21,20,20,20,20,21,21. Horizontaal 2-1-1, dan verticaal 2-2-4, kin 2, als een cirkelboog. Bij: (24,17) .40, (23,18) .50, (22,19) .40, (21,21) .30, (20,23–26) .41–.45. Horizontale stappen > 1 zijn helemaal buitenrand (geen open rand). Selout aan de lichtkant blijft sneeuwlijn, onderaan zwart zoals r5.

## Kuif links (varianten 1 en 2)
- **1, 2 px:** (29,12) terug naar achtergrond (dekking .38) en (29,13) zwart: de inkeping van het model (natief (45,19), L 6–8). Het bolletje heeft dan een puntige top.
- **2, 1 px (op r5):** bovenop 2 px breed ((28,12) en (29,12)), binnenkant (29,13) licht, inkeping naar het middenbolletje = (30,12) zwart.
- De inkeping tussen het bolletje en het hoofd is het zwarte (27,15) uit het model; meer kan niet binnen de regels ((26,16) heeft dekking .74).

`sneeuwmonster_r6.png` = hoofd B + kuif 2. Alle combinaties staan als `r6_hoofd{A,B}_kuif{1,2}.png`.

## Knopen in driekwart (`knopen.py`, op sneeuwmonster_r6)
- **a, modelvorm, 18 px:** steendekking ≥ .55 op het 1024-model, geen eigen vorm. Boven `.XXX/XXXX/XXXX/.XX.` (y35–38, gekanteld: boven naar rechts); onder `.XX./XXXX/XXXX/.XX.` (y41–44). De onderrij van de onderste knoop heeft dekking .52 aan de zijkanten; met de oude drempel .5 werd dat het rechte staafje.
- **b, smaller en schuiner, 23 px:** 3 breed gekanteld ovaal, het ver-oog van Delcatty (`_gba`, (23,24)) gespiegeld: `.XX/XXX/XXX/XX.`, op x25–27, y35–38 en y41–44.
- Tinten per pixel uit het model (< 40 zwart, < 70 steen donker, < 105 midden, anders licht): licht linksboven, donker/zwart rechtsonder.
- Bestanden: `r6_knoop_a.png`, `r6_knoop_b.png`, `vel_knopen.png`.

Twijfel: in het model is de onderste knoop breder dan hoog (meer naar opzij gedraaid). Gemeten (a) wordt dat op deze maat een rond 4×4; b maakt hem smaller in plaats van breder.
