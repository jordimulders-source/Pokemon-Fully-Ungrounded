# Bandolingo: proef tintzones (24 nov)
Bron: `olinguito_v2/af/olinguito.png` (niet aangeraakt). Resultaat: `na.png`, vel `voor_na.png` (voor | na | Aipom | Linoone | Furret | Kangaskhan, 6× en 1×). Gemaakt met gerichte pixellijsten in `maak.py`; bewijs met `bewijs.py`.

## Bewijs
- Silhouet (alfamasker): **diff 0**.
- Gezicht en hele kop (x 0–32, y 0–43: masker, oog, snoet, neus, oor, kruin en de lijn eromheen): **diff 0**.
- 29 pixels gewijzigd, 15 kleuren + transparant, mode P 64×64.
- Palet: index 5 (lichtbruin, alleen lijf/staart/poten) 158,111,71 → 170,121,76 (iets meer contrast). Verder geen paletwijziging.

## Per zone
| Zone | px | Wat |
|---|---|---|
| Rughooglicht | 5 | 5 → 4 aan het staarteinde: het licht ligt nu als zone op de bolling linksboven en loopt niet meer als band langs de hele rug |
| Schaduwsikkel rechts | 3 | 3 → 4 bovenaan: de schaduw is dun aan de bovenkant en breed onderaan (sikkel) i.p.v. een even brede rand van 3 px |
| Dijlijn | 2 | bestaande voorlijn van de dij 2 px omhoog doorgetrokken (1 px, tint 3) |
| Schouderlijn | 3 | korte plooilijn (tint 3) van schouderblad naar elleboog, sluit aan op de bestaande binnenlijn |
| Verre voorpoot | 10 | buitenlijn aan de lichtkant 1 → 3 (selout) + lichte streep 4 (cilinder i.p.v. vlak 3) |
| Nabije achterpoot | 6 | lichtstreep 5 doorgetrokken tot de enkel; buitenlijn lichtkant 1 → 3 |

Niet gewijzigd: kop (al selout 9 bovenop en hooglicht linksboven), oor, staart (al selout 3 links, zwart alleen aan de schaduwkant), voeten, klauwen.

## Zwak (eerlijk)
- Het verschil is klein; op 1× nauwelijks te zien. De Gen 3-maatstaf heeft een veel grotere waardesprong (bijna crème hooglicht). Met Jordi's goedgekeurde helderheid ("masker, helderheid en snoet blijven zo") ben ik niet verder gegaan; een sterkere contrastvariant (lichter hooglicht, donkerder 3) is een keuze voor Jordi.
- Zwart bleef aan de lichtkant niet veel over: de bron had al selout op kop, rug en staart; de opmerking "100 % zwart" gold eigenlijk alleen voor de poten.
- De staart is nog 3 banden langs de rand (3-5-4-1) zonder schaduwzone; bij een buis van 3 px vond ik dat Gen 3-achtig genoeg (Aipom), maar het blijft de "band"-look.
- Binnenin nog weinig plooilijnen; meer toevoegen (vachtstreepjes op de rug) leek me te veel richting nieuwe vlekjes.
- Tint 3 en 4 liggen dicht bij elkaar, dus sikkel en plooilijnen lezen zwak.
