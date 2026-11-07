# Stap 4, hoofd ronde 2 (6 nov)

## Opdracht (bovenop ronde 1)
- Jordi: "ja de mond is weg, de stekel is alleen dunner, maar die moet gewoon kleiner in zijn geheel, plus het mag iets duidelijker zijn dat het haar naar achter is gekamd, een knot moet wel duidelijk zijn".
- Jordi: "de puntige haarrand kammen we naar achteren, dus die is weg". Het haar ligt dus glad naar achteren.
- Jordi: "het hoofd mag wel iets groter, hitmontop heeft een erg groot hoofd voor zijn lichaam, bij deze evolutie wordt het naar verhouding minder, maar het wordt geen mens".
- Jordi: "de mond mag wat meer vreugde uitstralen dan bij hitmontop".
- Coördinator: ogen en wenkbrauwen in Hitmontops ontwerp (half dicht, zware bovenrand, scherpe hoek, fronslijnen), niet als ronde stippen. Stand 1 en 2, allemaal met een duidelijk knotje.

## Opties
| optie | stand | mond |
|---|---|---|
| 1L | ±15°, meer naar de kijker | licht: mondhoeken in donkerbruin, iets omhoog |
| 1M | ±15° | iets meer: zwarte mondhoeken, breder |
| 2L | ±40°, zoals de foto | licht |
| 2M | ±40° | iets meer |

Alle opties hebben een knotje. Bestanden: `optie_XX.png`, `hoofd_XX.png` (het hoofd los op 8× naast Hitmontops front en overworld), `vel_hoofd.png` (8×, 1× en 2× naast Hitmontop) en `controle.txt`.

## Opbouw en bronnen
- **Gezicht:** Hitmontops eigen gezicht uit `anim_front.png`, gespiegeld (groot oog rechts) zodat het met de pose meehelt. Exact overgenomen zijn de beide ogen met glimpixel, de donkerbruine/zwarte plooi onder elk oog die de scherpe ooghoek geeft, en de V-fronslijnen (5) erboven. In stand 1 staan ze pixel voor pixel; het grote oog raakt de rand, zoals bij Hitmontop. In stand 2 staan dezelfde oogvormen op de meegedraaide plek, en zijn de plooien en fronslijnen met de hand meegedraaid.
- **Halfdicht (aanpassing):** per oog 3 px extra zwart: de bovenste rij een pixel breder aan beide kanten, plus een puntje aan de buitenhoek. Dat geeft de zware bovenrand; de oogpixels zelf zijn niet veranderd.
- **Mond:** in Hitmontops stijl (zwarte streep met donkerbruine uiteinden), als lichte glimlach onder en tussen de ogen. Licht en iets meer, zie de tabel.
- **Hoorn:** Hitmontops hoorn als geheel verkleind (punt FF, dan F34F, F345F, basis in het haar), ongeveer 5×4 in plaats van 7×8. Dezelfde vorm en tinten, licht links.
- **Haar:** glad naar achteren, zonder punten. Er is een duidelijke haargrens in donkerbruin. Kamstrepen (5) lopen vanaf de haargrens over de schedel naar het knotje en komen daar samen. Licht linksboven (3), basis 4.
- **Knotje:** 6×6 px achter-linksboven, met strepen en een bandje waar het aan de schedel vastzit.
- **Maat:** de schedel is 23 px breed (stand 1: x5–27, y25–47; stand 2: x5–27, y25–47 gekanteld), plus hoorn en knot. In ronde 1 was dat 17–19 px; Hitmontop zelf is 37 px.
- **Kleuren:** alleen Hitmontops `normal.pal`.
- `opbouw_stand1.py` en `opbouw_stand2.py` zijn de hulpscripts waarmee ik de rasters heb opgebouwd (stand 1 in Hitmontop-broncoördinaten, scherm = bron + (4, −5)). Het eindresultaat staat als tekstraster in `stap4_r2.py`.

## Bevroren
`controle.txt`: bij alle 4 opties is de pixeldiff t.o.v. `stap3b/optie_C.png` 0 buiten de zone. De zone bestaat uit het nieuwe hoofd (450–501 px) plus het oude hoofd (169 px), samen binnen x0–29, y22–47. Het grotere hoofd dekt meer van de vrije bovenarm en de schouder af: x25–28, y29–41.

## Eerlijke zwakke punten
- Stand 1 leest op 2× als Hitmontops gezicht met het haar naar achteren in een knot. Stand 2 leest ronder en minder als Hitmontop: het haar ligt als een helm schuin over de kop.
- Het knotje kan op 1× als een oortje of balletje lezen, vooral in stand 2.
- De highlight onder de haargrens is een dunne diagonale lijn van losse pixels. De kamstrepen en de kleine hoorn bestaan ook uit 1-px-lijnen.
- Het verschil tussen mond licht en mond meer is klein (2–4 px).
- Interpretatie die Jordi moet zien: bij Hitmontop (die op zijn hoofd tolt) zit de hoorn onder het gezicht. Hier staat de hoorn op de kruin en het gezicht zoals de kijker het kent.
