# Keuring stap 4 hoofd, ronde 3 (6 nov)

Bron: `ronde3/optie_1M-r3.png` en `ronde3/optie_1M-r3-knot.png` (64×64), `ronde3/vel_hoofd.png`, `ronde3/hoofd_*.png`, NOTITIES.md, controle.txt; vergeleken met `ronde2/optie_1M.png`, `graphics/pokemon/hitmontop/anim_front.png` (bovenste 64×64) en de vorige keuring `ronde2/vel_hoofd.png.keuring.md`. Coördinaten zijn schermpixels van de 64×64-sprite. Palet in deze keuring: J = basishuid (222,189,131), K = middentint (180,139,90), L = donkerbruin (131,90,41), P = glim, E = omlijning.
Bekeken: 8×, 12× en 20× (eigen vergroting, nearest, met raster en pixeldump), 3× en 1× (op wit en op groen, naast Hitmontop).

## Vorige NODIG-punten
| # | punt | opgelost | toelichting |
|---|---|---|---|
| 1 | Linkeromtrek rond, onderkant buigen | **ja** | x7 (y28–29), x6 (y30–33), x5 (y34–38), x6 (y39–42), x7 (y43), x8–9 (y44); bodem y47 x14–19, y46 x12–13/x20–21, y45 x10–11/x22–23. Geen rechte wand en geen platte bodem meer; op 1× is het broodje weg. |
| 2 | Groot oog los van de rand | **ja** | Het oog staat nu op x21–25 (vleugel tot x25 op y37–38). Op x26 zit K-huid (y35–42) en de omlijning ligt op x27. Oogvorm ongewijzigd. |
| 3 | Mond los van de kinschaduw | **half** | Links is het gelukt ((20,44) is J). Recht onder de mondbodem (21–22,43) ligt nog steeds K (21–23,44). NOTITIES zegt "y44 huidtint 3", maar de dump laat K zien. Nieuw is een donker pixel (24,42) L tegen de rechtermondhoek (23,42). |
| 4 | Knot als haar, niet als bal | **half** | Het dambord is weg (J linksboven, K midden, L rechtsonder), er is een bandje en de aanzet is ≥ 4 px. Maar de knot is overwegend **huidkleurig**: in r3 bestaat hij uit 9× J, ±7× K en ±5× L, terwijl de haarmassa K/L is. Hij leest daardoor als een huidkleurige bol (oor of tweede bult), niet als haar dat in een knot samenkomt. |
| 5 | Haar als gekamde massa, haargrens als boog | **half** | Er zijn kamstrepen die doorlopen, vooral (21,29)→(18–20,28)→(14–17,27)→(11–13,26): goed, ≥ 3 px per stuk, zonder huidstippen. De haargrens buigt alleen aan de linkerkant (x9 y31–32, x8 y33, x7 y34, x6–7 y35). Over het voorhoofd is hij nog een **rechte donkere lijn L op y30, x14–21 (8 px)**, met de huid recht eronder vanaf y31, x10–23. NOTITIES zegt dat de grens daar "basistint 4 in plaats van een donkere band" is, maar de dump laat L zien (identiek aan ronde 2). Op 3× en 1× leest de kap daardoor nog als muts of pet met een rand. |

## Per onderdeel (beide opties zijn binnen x10–29 identiek)
| onderdeel | lijkt op | wijkt af in |
|---|---|---|
| ogen | Hitmontops halfdichte ogen met glimpixel ((15,38), (23,36)), de zware bovenrand en de plooi onder het kleine oog. Ze liggen nu vrij in het gezicht. | Niets wezenlijks. |
| wenkbrauwen | Een dalende fronslijn (14,33)→(15–16,34)→(17–19,35) naar het grote oog, plus (20,34): het idee van Hitmontop. | Ze zijn klein en op 1× nauwelijks zichtbaar, net als bij het origineel. Dat is goed zo. |
| mond | Een kleine U (19,42), (20–22,43), (23,42) met de hoeken omhoog. Blijer dan Hitmontop, wat Jordi vroeg. | De kinschaduw K (21–23,44) raakt de mondbodem nog. (24,42) L verlengt de rechterhoek. De plooi onder het kleine oog (15–16,42) E en (18,42) L ligt op 1 px van de linkerhoek, dus op 1× kan plooi+mond als één lange streep van x13 tot x24 lezen. |
| hoorn | Hitmontops hoorn, kleiner (x12–15, y22–26), zelfde tinten. Voldoet aan "kleiner in zijn geheel". | In r3 staat de knot er op dezelfde hoogte naast (x3–10, y21–26), met maar 1–2 px omlijning ertussen ((10–11,24) E, (8–11,25) E). Op 3× en 1× lezen ze als twee bulten bovenop (risico op oren, het probleem van stand 2). In r3-knot staan ze los. |
| haar | De puntige rand is weg. Er zijn kamstrepen en een glimvlakje van 3 px ((11–12,32), (11,33)) in plaats van de trap. | Zie NODIG 5: rechte donkere voorhoofdslijn. Links ligt een smalle reep J/K tussen omtrek en haarlijn (x7–8, y30–33): leest als oor of bakkebaard, niet als haar. Haar (K) en wangschaduw rechts (K, x24–26, y31–34) hebben dezelfde tint en lopen in elkaar over. Dat mag, Hitmontop is ook één bruin. |
| knot | De plek klopt: achter op de kop (het gezicht kijkt naar rechts). r3-knot zit met een haarkleurige hals (5–9, 25–26 L/K) aan de kop: leest als "staartje met knot", dus duidelijk naar achteren. | Huidkleurig (zie punt 4). r3: te dicht bij de hoorn. r3-knot: raakt de rand van het vak op x0 (y22–24), en de kamstreep (11,26) loopt dood op de omlijningshoek (10,26) E in plaats van de hals in. |
| maat | Schedel ±23 px breed: "iets groter" dan Hitmontops kop naar verhouding, geen mens. | Niets. |
| omtrek | Rond aan links en onder, 1 px, geen open randen. | De bovenkant rechts van de hoorn is recht op y25 (x15–18). Dat is kort genoeg. |

## Bevroren
Zelf nagerekend tegen `stap3b/optie_C.png`: bij beide opties 0 px anders buiten de zone (r3: x3–29, y21–47; r3-knot: x0–29, y20–47). controle.txt klopt.

## Nieuwe NODIG (basis r3-knot)
1. **Knot in haartinten:** de knotvulling naar K als basis, L als schaduwsikkel rechtsonder en J alleen als glim van 2–3 px linksboven. Nu zijn de J-pixels (1–4, 21–24) het grootste vlak. Daarna leest hij als haar en niet als huidbol.
2. **Voorhoofdslijn weg:** (14–21,30) van L naar K, en laat de haargrens schuin lopen in plaats van recht. Bijvoorbeeld huid J op (19–23,30), haar K tot y31 op x10–13 (links lager dan rechts, richting knot). Zo krijg je de boog die NOTITIES beschrijft, en de kap leest niet meer als pet.
3. **Mond echt los:** (21–23,44) van K naar J. (24,42) van L naar J (of naar K als je een lachrimpel wilt, maar dan niet direct tegen de hoek).

## POLIJSTEN
- Knot 1 px naar rechts (x1–10) zodat hij de vakrand x0 niet raakt. De hals blijft ≥ 4 px.
- Kamstreep (11,26) laten doorlopen in de hals ((10,26) K of L in plaats van E, de omlijning 1 px hoger leggen), zodat haar zichtbaar in de knot uitkomt.
- Reep x7–8, y30–33 naar K (haar tot de omtrek), zodat er geen oor of bakkebaard ontstaat.
- (17,42) J tussen plooi en mond houden en (18,42) L lichter (K), zodat de plooi niet tegen de mond plakt.

## Advies
**r3-knot.** De knot staat los van de hoorn (dus geen twee oren) en de haarkleurige hals laat zien dat het haar naar achteren in een staartje met knot is gekamd, wat Jordi vroeg ("een knot moet wel duidelijk zijn"). r3 zet de knot naast de hoorn bovenop de kop en valt daarmee terug naar het oorprobleem. Na NODIG 1–3 hoef je niet opnieuw een volle ronde te doen; een korte controle van alleen die pixels is genoeg. Ogen, omtrek en hoorn zijn af.

Oordeel: FAIL
