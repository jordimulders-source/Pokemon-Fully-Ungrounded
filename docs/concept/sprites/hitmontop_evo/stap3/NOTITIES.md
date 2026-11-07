# Stap 3: ledematen, romp en kop op skelet D14 (knip- en plakwerk)

Draaien vanuit de repo-root: `python3 docs/concept/sprites/hitmontop_evo/stap3/stap3.py`. Het script importeert `stap2/stap2.py` (zonder `main()`) en gebruikt `OPTIES['D14…']` + `plaats()`; stap 2 is niet gewijzigd. Handen en voeten zijn exact die van stap 2 en worden als laatste geplakt.

Opties (`optie_A.png` … `optie_D.png`, vel `vel_stap3.png`; op het 8×-vel ligt het skelet er dun in groen over):
- **A:** kop a (zoals in Hitmontops sprite, hoorn omlaag), romp Hitmonchan
- **B:** kop b (180° gedraaid, hoorn omhoog), romp Hitmonchan
- **C:** kop c (alleen gezicht + hoorn, hoorn omlaag), romp Tyrogue
- **D:** kop c, 180° gedraaid, romp Tyrogue

## Uitsneden (coördinaten in de bovenste 64×64 van `anim_front.png`, box = x0,y0,x1,y1 exclusief)
| Onderdeel | Bron | Box | As (van → naar) | Bewerking |
|---|---|---|---|---|
| Kop a/b | Hitmontop | (16,35,53,58), 37×23 | ref = tussen de ogen (31,44) → midden kopcirkel | 1:1; b = 180° |
| Kop c | Hitmontop | (21,35,40,58), 19×23 (gezicht + hoorn, zonder zijranden van het haar) | idem | 1:1; D = 180° |
| Steunarm | Hitmonchan linkerarm | (22,20,30,35), rood/oranje (handschoen) weggemaskeerd | (26,20) → (25,34), 14 px | langs schouder → pols (16 px): twee kopieën, één aan elk eind |
| Vrije bovenarm | Hitmonchan | (22,20,30,28) | (26,20) → (26,27) | langs v_schouder → v_elleboog, 1:1 |
| Vrije onderarm | Hitmonchan | (22,25,30,35) | (26,25) → (25,34) | ronde elleboog op v_elleboog, boven bij de pols |
| Dij | Hitmonlee rechterbeen | (36,36,45,45) | (40,36) → (39,44), 8 px | langs heup → knie (11 px): twee kopieën → extra windselbanden; been 1 gespiegeld |
| Scheen | Hitmonlee | (32,44,43,54) | (39,44) → (37,53), 9 px | langs knie → enkel (10 px), idem |
| Romp Hitmonchan | Hitmonchan | (24,24,46,43), boven y 34 alleen x 29–40 (armen weg) | (35,24) → (35,42), 18 px | langs schouder → heup (20), gecentreerd: 1 px kier aan elk eind |
| Romp Tyrogue | Tyrogue | (26,30,41,46), boven y 38 alleen x 27–36 | (32,30) → (33,45), 15 px | idem, 2–3 px kier aan elk eind |
| Koord | – | rode lijn heup → koord | | |

Draaien: nearest-neighbour onder elke hoek (romp ±149°, benen ±60–120°). **Niets geschaald** in de opgeleverde opties. Getest en afgevallen: de hele kop op 50% (nearest) als optie D; dat werd een onleesbare brij (ogen weg), dus niet opgeleverd (staat als commentaar in het script).

Lagen (achter → voor): been 1 (verre been) → steunarm → romp → been 2 → koord → vrije arm → kop → handen en voeten (stap 2).

## Zelf getoetst op 1× (en 8× met het skelet erover)
- **Eenarmige handstand met V:** ja, de V van de blauwe voeten en de steunarm met de ronde hand onderaan lezen. Maar de kop is op 1× het grootste vlak en domineert: het leest eerder als "Hitmontop-kop met benen" dan als stevige figuur.
- **Gewrichten:** beide benen beginnen bij de heup en eindigen onder de voeten van stap 2 (enkels kloppen); de steunarm loopt van schouder tot hand; de vrije arm buigt bij de elleboog en eindigt bij de hand. De kop zit niet los: de nek valt binnen de kop (bij a/b ligt de kop zelfs over de schouder en de bovenkant van de steunarm).

## Wat ik zelf raar vind
1. **De Hitmontop-kop is 1:1 veel te groot voor D14** (37 breed tegen een kopcirkel van Ø14; zelfs alleen het gezicht is 19×23). Hij bedekt de romp, de nek en de schouder; daardoor zie je de romp-opties nauwelijks (alleen wat paars van Hitmonchan bij de heup en het witte shirt van Tyrogue tussen de vrije arm). De romp-vergelijking is dus pas zinvol als de kop kleiner is: kop met de hand kleiner tekenen (schalen werkt niet, zie hierboven) of het skelet een grotere kop geven.
2. **Richting van de kop:** in de pose hangt het hoofd ondersteboven (kruin naar de grond), dus a (hoorn omlaag) klopt fysiek. Het skelet legt de kruin (nek → kop) echter naar linksboven, wat eerder bij b past. b leest als "rechtop gezicht", a als Hitmontop zelf.
3. **Hitmonchans armen zijn dik (6–7 px) tegenover Hitmonlee's benen (4–6 px)**: de armen lijken zwaarder dan de benen. De steunarm is twee keer hetzelfde stuk, dus de schouderbol herhaalt halverwege.
4. **Benen:** Hitmonlee's dij (8) en scheen (9) zijn korter dan de segmenten (11/10); door de tweede kopie krijgt de dij extra windselbanden, wat er toevallig best natuurlijk uitziet. Bij de schuine hoeken zijn de windsels gekarteld.
5. **Romp Tyrogue** is te kort (15 op 20) en smal; Hitmonchans romp past qua lengte (18) beter maar is breed. Beide verdwijnen nu achter de kop en de vrije arm.
6. Marge: bovenrand 1 px, onderkant 63 (hand op de grond); links/rechts 1–2 px. Krap, zoals al bij stap 2 genoemd.
