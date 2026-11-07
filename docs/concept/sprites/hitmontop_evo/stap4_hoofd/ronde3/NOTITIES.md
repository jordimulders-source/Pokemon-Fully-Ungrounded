# Stap 4, hoofd ronde 3 (reparatieronde, 6 nov)

Basis: ronde 2 optie **1M** (stand ±15°, blijere mond). Stand 2 is vervallen, op advies van de keurder (`ronde2/vel_hoofd.png.keuring.md`). Ik heb alleen de benoemde punten gerepareerd; ogen, fronslijnen, hoorn en mondvorm zijn uit 1M overgenomen.

## Opties
- `optie_1M-r3.png`: 1M met reparaties 1–5. De knot ligt op de haarmassa linksboven, met een bandje (zwart) eronder.
- `optie_1M-r3-knot.png`: hetzelfde, maar de knot staat 2–3 px verder naar achter en boven (x0–9, y20–27). Hij is beter zichtbaar en zit met een hals van 4 px aan de schedel.
- Losse hoofden: `hoofd_*.png`. Vel: `vel_hoofd.png` (8×, 1× en 2× naast Hitmontop). Rasters: `stap4_r3.py`. Opbouw: `opbouw_r3.py` (leest 1M uit ronde 2 en past de reparaties toe).

## Reparaties
1. **Omtrek rond:** links x5 alleen op y34–38, x6 op y30–33 en y39–42, x7 op y28–29 en y43. De onderkant buigt: y47 x14–19, y46 x12–13 en x20–21, y45 x10–11 en x22–23, y44 x8–9 en x24–25. De rechterkant op x27 is gebleven.
2. **Groot oog los van de rand:** het oog met zijn plooi en vleugel staat 1 px naar links (nu x21–26). Op x26 zit 1 px schaduwhuid tussen oog en omtrek, dus het raakt de arm niet meer. De oogvorm is ongewijzigd.
3. **Mond los van de kinschaduw:** de U van 1M (x19–23, y42–43) heeft eronder (y44) en rechts ervan (x24–25) huidtint 3 in plaats van schaduw. De zwarte hoeken van 1M zijn gebleven.
4. **Knot:** met de hand getekend. Vlakken licht linksboven (3), midden (4) en rechtsonder (5), zonder dambord. Er zit een zwart bandje waar hij in het haar overgaat, en de aanzet is breder dan 4 px (x5–10, y25–27). De kamstrepen lopen erin uit.
5. **Haar:**
   - De haargrens is nu een boog: hoog op het voorhoofd (y29), lager aan de zijkanten, en links achter het oor tot y35 naar de knot toe.
   - Langs het voorhoofd is de grens basistint 4 in plaats van een donkere band. Links (x≤9), waar het haar naar de knot loopt, is hij donkerbruin.
   - Drie doorlopende kamstrepen in donkerbruin lopen van de haargrens naar de knot: (21,29)→(10,26), (14,29)→(10,27) en (9,32)→(8,28).
   - De diagonale glimlijn is weg. Er is alleen een klein glimvlak van 3 px boven het kleine oog (x11–12, y32–33).

## Bevroren
`controle.txt`: bij beide opties is de pixeldiff t.o.v. `stap3b/optie_C.png` 0 buiten de zone. De zone bestaat uit het nieuwe hoofd plus het oude hoofd: x3–29, y21–47 en x0–29, y20–47.

## Eerlijke zwakke punten
- De haarkap is nog steeds een bruine massa van ±4 px boven het voorhoofd. Door de boog en de strepen leest hij minder als pet dan in ronde 2, maar de kap blijft breed.
- De knot kan op 1× nog als een bolletje linksboven lezen. Bij de r3-knot-variant zit hij aan een korte hals, wat ook als steeltje kan lezen.
- De knot van r3-knot komt tot x0, de linkerrand van het 64×64-vak.
- De kamstrepen zijn 1 px dun en lopen trapsgewijs schuin.
