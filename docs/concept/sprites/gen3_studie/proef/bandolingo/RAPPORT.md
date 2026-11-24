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

---
# Variant B (`na_B.png`, `maak_B.py`): de echte stap, op lijf, staart en poten
A blijft `na.png`. Vel opnieuw: `voor_na.png` = voor | A | B | Furret | Kangaskhan, op 6× en 1×.

## Bewijs (`bewijs.py`, opnieuw gedraaid; kop nu vergeleken op RGB, dus ook paletwijzigingen tellen)
- A: alfadiff 0, kopdiff 0, 29 px. B: **alfadiff 0, kopdiff 0**, 125 px met een andere index, 15 kleuren + transparant, P 64×64.
- Kopzone (vast): x 0–31 / y 0–38, de snoet en neus tot y 45 (x ≤ 24) en de kaaklijn boven de verre voorpoot.
- Palet B: alleen index 5 (licht) → 186,136,88 (±65 helderheid boven grondtint 4 = 106,70,48; richting Furret-licht).

## Per zone (B)
| Zone | px | Wat |
|---|---|---|
| Lijf: lichtzone | ±45 | één zone op de bolling rug/schouder linksboven, rijen 26–40, harde diagonale grens naar de grondtint; oude rugband en de losse dijvlek weg |
| Lijf: schaduwsikkel | ±25 | één sikkel van 3: dun (1 px) onder de staartbasis, breed (5–6 px) achter de dij en langs de buik (rij 40) |
| Dij | ±12 | contourlijn (3) loopt nu over de bovenkant van de dij door (42,32)→(39,34)→ voorlijn → onderlijn; licht aan de voorkant van de dij, grond, schaduw erachter |
| Vachtlijntjes (3, 1 px) | 7 | rug (40,28)-(41,29); schouder/elleboog (36,38),(35,39); dij (43,35)-(43,36) richting de sikkel |
| Nabije voorpoot | ±20 | 1 px licht aan de voorkant, grond, 2 px schaduw achter (was 2 px licht in banden) |
| Nabije achterpoot | ±14 | 1 px licht aan de voorkant tot de enkel, buitenlijn aan de lichtkant 1 → 3 |
| Verre poten | 0 | stonden al helemaal in de schaduwtint (3/2); zo gelaten |
| Staart | ±25 | selout 3 · 1 px licht · (grond bij 3 px breed) · 3 schaduw · zwarte lijn; de boog bovenaan licht op de bovenkant, schaduw aan de binnenkant |

## Zwak in B (eerlijk)
- **Schaduw is niet donkerder dan voorheen:** tint 3 en 4 kon ik niet uit elkaar zetten, want beide zitten ook in de kop (3 = nekschaduw onder de kruin + 1 lijnpixel bij het oor, 4 = de kruin) en het palet is vol (15). Kop diff 0 en een donkerdere schaduw gaan alleen samen als Jordi een kleine kopkleurwijziging toestaat (bv. 3 → ±62,38,26 kleurt ook ±10 nekschaduwpixels mee) of als er een index vrijkomt.
- De lichtzone is groot en fel naast een kop die donker en grijs blijft; het lijf leest nu lichter dan de kop ("helderheid" was goedgekeurd, dit ligt bij Jordi).
- Het vachtlijntje op de rug (40,28)-(41,29) staat midden in het licht en kan als kras lezen; het dijlijntje gaat op in de sikkel.
- Staart bovenaan (de haak links, rijen 10–12) is 1 px breed gebleven in grondtint, zonder licht.
