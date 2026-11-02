# Silhouet v2 ronde 2 (maker-agent, 2 nov)

Basis `ronde1.txt` + reparaties uit `KEURING_ronde1.md`. Bewijs `ronde2.py`: expliciete pixellijsten per zone, met per pixel de dekking in de onderlaag (deel van het 4x4-blok dat niet wit is), en een diff tegen ronde1 én direct. Uitvoer: `ronde2.txt`, `ronde2_1x.png` (1446 px, box 47x62), `vel_ronde2.png`, `zone_ronde2.png` (script `zone_ronde2.py`).

| Zone | px | wat |
|---|---|---|
| 1 verre klauw | 3 | (9,37) aan: eindstuk is een blok van 3x3 (x 8–10, y 35–37), de spleet in de punt wordt kleurwerk. (16,33) en (17,33) uit: pols, steel 2 px (y 33–34, x 8–15) tegen een onderarm van 4–5 px; de oksel (19,32)/(16–19,33) blijft een V. Punt blijft omlaag. |
| 2 buidel/staart | 10 | (39,18) aan (gat onder de knobbel dicht). Staart uit: (53,20), (53,21) (top smaller), (54,23), (54,31)–(54,33) (rechterrand taps), (48,28)–(48,30) (holte onder de haakpunt; de punt x 46–47, y 22–27 hangt als lob over de spleet). Lucht naar de zak 3 px op y 28–30, schacht 6 px. |
| R kop (±1 px) | 3 | (30,8) aan (deuk achterhoofd), (12,14)–(12,15) aan (neus 1 px vooruit). |
| R benen (±1 px) | 3 | (26,50), (38,56), (28,58) aan (trapjes in de beenranden). |

Totaal 19 px tegen ronde1, 0 buiten de zones; 42 px tegen direct, 0 buiten de zones (ronde-1-zones meegeteld).

**Niet gedaan, en waarom:**
- (8–10,38): dekking in de onderlaag 0. Een vierde rij maakt het eindstuk 4 px lang onder een steel van 2 px, en dat leest op 1x als een pootje dat de grond zoekt. Weggelaten.
- **Afwijkingen van de keurder, waar ik de onderlaag volg:**
  - (31,6)–(31,9): dekking 0,44 / 0,06 / 0 / 0; bol achterhoofd staat niet in de render.
  - (14,2) en (30,2): dekking 0,69 / 0,88; de render heeft daar de oorbasis, dus geen ronde hoek.
  - (13,16): dekking 1,0, kin hoort erbij. (13,7): dekking 0,75.
  - (15,21)–(15,25): dekking 0. Een bolle borst staat niet in de render, dat is een pose-/ontwerpvraag (keuring punt 2).
- **Wel tegen de onderlaag in, omdat het een benoemde vormreparatie is (opdracht):** de staartpixels (dekking 0,62–1,0), de pols (16,33)/(17,33) en (39,18) (dekking 0,12).

## Eigen zwakke punten (eerlijk)
- **Kop:** blijft een doos (voorkant x 13 en achterkant x 30 recht over ±10 rijen, platte bovenkant). De keurdersreparaties daarvoor wijken van de onderlaag af en heb ik niet gedaan. Vergroten of omvormen is een vraag aan Jordi.
- **Borst:** de verticale lijn kop–borst blijft. Het silhouet leest rechter dan de render (keuring punt 2, voor Jordi).
- **Staart:** leest op 4x meer als haak dan in ronde 1, maar op 1x nog deels als een knots met een ronde kop. Een echte herdersstaf (punt verder omlaag, lucht eronder) wijkt af van E2 (voor Jordi).
- **Verre klauw:** op 1x een klein haakje omlaag, zonder gespleten punt (die staat nu alleen in de kleur). Dat hij als koevoet en niet als hand leest, hangt van de kleur af. De bocht blijft ±90°.

## Lessen
- Keurdersreparaties eerst per pixel tegen de dekking van de onderlaag leggen; een "ronde hoek" of "bolle achterkant" die niet in de render staat, is een ontwerpwijziging en geen reparatie.
