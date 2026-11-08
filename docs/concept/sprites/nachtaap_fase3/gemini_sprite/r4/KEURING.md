# Keuring muriqui r4 (onafhankelijke keurder, 8 nov)

**Oordeel: FAIL (klein).** Er zijn twee reparaties van elk 2 tot 4 pixels nodig. Daarna is het een PASS: alleen de diff controleren, geen volledige ronde.

Toetsing: (1) trouw aan `gemini/gekozen_r4.png` (ogen en rugsikkels mogen afwijken), (2) Gen 3-techniek. Werkwijze als in r3: BOX-verkleind model op het spriteraster, 8× en 1× naast elkaar, close-ups, `sub.py`-metingen en `check.py`.

## Diff r3 → r4
113 pixels. Alle 8 punten uit `r3/KEURING.md` zijn uitgevoerd zoals voorgeschreven. De maker veranderde ook twee pixels die niet gevraagd waren:
- (55,32) `d` → `1`: akkoord. Het model is daar grijs-zwart, en een doorlopende lijn is technisch beter.
- (3,15) `b` → `4`: niet akkoord, zie punt 1.

## Afvinken
| Onderdeel | Oordeel |
|---|---|
| Silhouet, kop, maansikkel, masker | OK (ongewijzigd) |
| Snuit | OK. Het filtrum loopt nu van het linkerneusgat naar de mond, zoals in het model |
| Gloedhand | Lijnwerk en vingerposities kloppen nu met het model, het dambord is weg, en de hand leest op 1× als hand. Een trapje in de ondercontour moet nog weg (punt 2) |
| Gloedrand en romplijn (21,46–47) | OK |
| Hand boven | OK, met lila toppen zoals het model |
| Hand linksboven | Bovenrand OK. De vingertop is nu een pixel ingekort (punt 1) |
| Staart | Het witte spiraalpad loopt nu door van buiten tot het midden. Selout linksboven OK |
| Bovenarm, voetnaad | OK |
| Kleuren | OK: 15 + transparant |

## Reparaties
1. **Hand linksboven, top van vinger 1** (dit volgde uit mijn eigen r3-punt "(3,14) mag weg"). Na het weghalen van (3,14) werd (3,15) donker. Daardoor heeft de vingertop op x3 geen lichte pixel meer en oogt hij stomp/dik omlijnd. In het model is x3 op rij 15,5–16 licht (`b`).
   - Zet (3,14) `.` → `4`; die hoek sluit de bovenrand.
   - Zet (3,15) `4` → `b`.
   - (2,15), (2,16) en (3,16) blijven `1`; (4,16) blijft `4`.
2. **Gloedhand, ondercontour.** Nu loopt de trap (9,57) | (10..12,58) | (13,59) | (14..21,60), dus runs van 1-3-1-8. De losse stap op x13 is een onregelmatig trapje. Het model ligt op x14–15 een halve pixel hoger (zwart op rij 59,5; op rij 60 cyaan).
   - Zet (14,59) en (15,59) `b` → `1`.
   - Zet (14,60) en (15,60) `1` → `e`.
   - Resultaat: runs van 1-3-3-6 en exacter op het model.

Buiten deze 6 pixels moet de diff 0 blijven.
