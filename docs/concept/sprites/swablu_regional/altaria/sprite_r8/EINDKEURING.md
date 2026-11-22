# Eindkeuring Altaria r8 (Dragonfly Cave-stijl, 21 nov)

Getoetst: uitvoering en trouw aan het model (`model_kop/natief_kop15_dy10.png`, 1/3-blokken). Geen herontwerp; aantal en plek van de bollen niet getoetst (Jordi: "de hoeveelheid is het issue niet").
Proef met alle MOETEN: `proef_eindkeuring.png` (16 px gewijzigd t.o.v. `altaria_r8.png`, verder diff 0; alpha gelijk, 14 kleuren).

## Wat al goed is
- **Tinten = modeltinten** (wolk 34/46/75/124/185, kop 39/107/143/172): geen modderige tussentint meer; bollen lezen door cyaan kap boven en navy onder, zoals het model.
- **Kop niet meer blurry:** drie heldere violetvlakken (hooglicht linksboven, licht, midden rechts), komt 1-op-1 overeen met de bandstemmen van het model. Snavel/wang cyaan zoals het model.
- **Kuif:** donkere onderkant, lichte bovenkant, glanzen op de modelplekken; leest als schokkerige voelsprieten op 1×.
- **Zwart** alleen in de 5 pupilpixels; ≤16 kleuren (14); silhouet = r5-proef.
- **Static** op de modelplekken, dun, cyaanwit; leest als static op wit, crème, grijsblauw en zwart.

## MOETEN (getest op de proef)
Static: op 14 plekken was de 1-px-lijn een trapje met dubbele hoekpixels (L-vorm, leest als 2 px dikke jaggy). Hoekpixel weg, lijn blijft 8-samenhangend; nieuwe kleur = de wolkband van de niet-static modelpixels van dat blok (als die tint ernaast ligt, anders de buur-tint om geen korrel te maken).
| pixel | van → naar | modelstemmen (zonder static) |
|---|---|---|
| (54,19) | 7 → 4 | WD 6 |
| (55,20) | 7 → 4 | WD 5 |
| (14,24) | 7 → 4 | WD 7, WT 1 |
| (15,25) | 7 → 4 | WD 3 |
| (53,26) | 7 → 3 | WN 7 |
| (52,28) | 7 → 3 | WN 7 |
| (10,29) | 7 → 4 | (blok vrijwel static; buur 4) |
| (51,29) | 7 → 4 | WN 7, maar buren 4 (anders losse navy-pixel) |
| (50,30) | 7 → 4 | idem |
| (11,38) | 7 → 4 | WD 5 |
| (10,40) | 7 → 4 | WD 8 |
| (49,42) | 7 → 4 | WD 6 |
| (45,46) | 7 → 3 | WN 7 |
| (14,47) | 7 → 3 | WN 5 |

Kuif:
- (30,10) 12 → 13: de glansstreep op de bovenste streng liep w-d-w (13,12,13) = korrel; het blok heeft 2 lavendelwitte modelpixels en ligt op de modelglans; nu één doorlopende glans (29–31,10) → (32–33,9) → (34–35,8).

Wolk:
- (47,22) 4 → 6: modelblok is 8/9 cyaan kap; sluit aan op de kap (47–50,21), bol rechtsboven leest ronder.

## ZOU KUNNEN
- Rechtervleugel, bol linksboven (X40–44, Y24–27): het model heeft hier een cyaan kap ((41,25) WC 8/9, (40,26) WC 7/9), r8 heeft 5. Alleen die twee terugzetten geeft een diagonaal 2-px-plukje; overwegen samen met (42,25)/(41,26) als Claude/maker dat netjes vindt.
- Nabij oog: glans (27,22) staat niet in het model (modelglans zit bovenin het verre oog, (21,22)); komt uit r3–r5. Gezicht = belangrijkste: alleen veranderen als Jordi het noemt.
- Static-boog links buiten de vleugel (x4–5, Y23–28) is op 1× op wit nauwelijks zichtbaar (L215 op wit); zo in het model, dus laten.
- Static grenst op 3 plekken aan cyaan kap ((14,21), (12,32), (17,35)): daar weinig contrast; model-plekken, dus laten.

## Oordeel
r8 zoals hij is: BIJNA (trapjes in de static). **Na toepassing van de MOETEN (= `proef_eindkeuring.png`): PASS.**
