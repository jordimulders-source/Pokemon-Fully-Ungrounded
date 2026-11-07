# Keuring stap 4 hoofd, ronde 3b (6 nov)

Bron: `ronde3b/optie.png` (64×64), `ronde3b/hoofd.png`, `ronde3b/vel_hoofd.png`, controle.txt en NOTITIES.md. Vergeleken met `ronde3/optie_1M-r3-knot.png` (eigen diff per pixel), `stap3b/optie_C.png` (bevroren deel), `graphics/pokemon/hitmontop/anim_front.png` (bovenste 64×64) en de vorige keuring `ronde3/vel_hoofd.png.keuring.md`. Coördinaten zijn schermpixels van de 64×64-sprite. Afkortingen: J = basishuid, K = middentint, L = donkerbruin, P = glim, E = omlijning.
Bekeken: 8× en 20× (eigen vergroting, nearest, met raster en een eigen pixeldump), 3× en 1× (op groen, naast Hitmontop en ronde 3).

## Vorige NODIG-punten (ronde 3)
| # | punt | opgelost | toelichting (eigen dump) |
|---|---|---|---|
| 1 | Knot in haartinten | **ja** | De vulling is nu K met een L-sikkel rechtsonder ((6–7,23), (4–5,24), (4–5,25)). J staat alleen als glim van 3 px linksboven: (2,21) en (2–3,22). De knot leest als haar en niet meer als huidbol. |
| 2 | Voorhoofdslijn weg, schuine haargrens | **ja** | De lijn L op (14–21,30) is weg. De grens loopt nu als een gelijkmatige schuine trap: huid vanaf y30 op x18–22, vanaf y31 op x14–23, vanaf y32 op x10. Rechts staat hij hoog, links ligt hij lager richting de knot. Op 3× leest de kap als haar dat naar achteren gekamd is, niet meer als pet. |
| 3 | Mond los van de schaduw | **ja** | (21–23,44) is J en (24,42) is J. De U (19,42), (20–22,43), (23,42) staat vrij. De kinschaduw begint pas op y45. |
| P | Knot van de vakrand af | **ja** | De knot loopt nu van x1 tot x9. x0 is leeg. |
| P | Kamstreep loopt door in de hals | **ja** | (9–13,26) is één doorlopende L-lijn tot in de hals ((6,26) L, (7–8,26) K). |
| P | Reep x7–8, y30–33 haar | **ja** | Hij is nu K (met (8,33) L als haarlijn): geen oor en geen bakkebaard. |
| P | Plooi niet tegen de mond | **ja** | (18,42) is K en (17,42) blijft J. |

## Per onderdeel
| onderdeel | lijkt op | wijkt af in |
|---|---|---|
| ogen | Hitmontops halfdichte ogen met glimpixel en plooi. Ze liggen vrij in het gezicht. Ongewijzigd ten opzichte van ronde 3. | Niets. |
| wenkbrauwen | Dalende fronslijn (14,33)→(17–19,35) en (20,34), zoals bij Hitmontop. | Niets. |
| mond | Kleine U met hoeken omhoog: blijer dan Hitmontop. Op 1× zichtbaar. | Niets. |
| hoorn | Hitmontops hoorn, kleiner (x12–15, y22–26). Hij staat los van de knot. | Niets wezenlijks. |
| haar | Een gladde gekamde massa zonder puntige rand. De strepen lopen van het voorhoofd naar de knot. | Niets wezenlijks. |
| knot | Achter op de kop, met een haarkleurige hals: duidelijk een staartje of knotje. | Niets wezenlijks. |
| maat | Iets groter dan Hitmontop naar verhouding, geen mens. | Niets. |
| omtrek | Rond links en onder, 1 px, geen open randen. | Niets. |

## Gecontroleerd op nieuwe fouten
- De diff met ronde 3 zit alleen op de benoemde pixels: knot y20–26, y30–31 en de mond/kin op y42 en y44. Ogen, hoorn en omtrek zijn onveranderd.
- Buiten de zone x0–29, y20–47 zijn 0 px anders dan `stap3b/optie_C.png`. controle.txt (zone x1–29) klopt.
- Er zijn geen nieuwe kleuren buiten wat ronde 3 en optie_C al gebruikten.
- Ik zie geen ruis of banding. Het glimvlak (11–12,32) en (11,33) is gebleven.

## POLIJSTEN (niet blokkerend)
- Tussen de knothals en de hoorn zit op y24 maar 1 px lucht ((10,24)). Op 1× sluit dat dicht. Het mag zo blijven. Het kan ook 1 px ruimer, door (9,24) leeg te laten en (9,25) als omlijning te geven.
- (12–13,27) J is de lichte voet van de hoorn in het haar. Die mag blijven als glans. Als hij op 1× als vlekje leest, kan hij naar K.

## Advies
Deze versie, die is gebouwd op r3-knot, kan naar Jordi. Laat hem op 1× en 3× naast Hitmontop zien.

Oordeel: PASS
