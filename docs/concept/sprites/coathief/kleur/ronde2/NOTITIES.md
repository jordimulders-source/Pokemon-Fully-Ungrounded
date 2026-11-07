# Coathief: kleursprite ronde 2 (reparaties in vier zones)

Basis: ronde 1 (`../ronde1/`, zie de NOTITIES daar voor de studie, het palet en de checklist). Het palet is ongewijzigd.

## Bestanden
- `coathief.png`: 64×64, mode P, 16 kleuren, index 0 transparant, transparency=0.
- `vel.png`: hetzelfde vel als in ronde 1.
- `r1_vs_r2_kop_poten.png`: kop en voorpoten op 8×, ronde 1 naast ronde 2.
- `uitsnede.png`: kop met poten en de staartkrul op 8×.
- `uitsnede_klauwen.png`: drie varianten voor de grondklauwtjes, op 8× en 1×.
- `bron/`:
  - de reparaties van ronde 2 staan onderaan `reparaties.txt` (blok "ronde 2"); `raster.txt` is ongewijzigd;
  - `diff_r1.py` is de pixeldiff tegen ronde 1, per zone.

## Bewijs
```
controle.py: pixels 1297 | silhouet 1297 | alpha-diff 0 | open randen 0 | losse pixels 0
diff_r1.py:
zone 1 vlekken rond het oog                  11 px
zone 2 verre voorpoot                        24 px
zone 4 klauwtjes verre voorpoot               7 px
zone 3 opgetilde voorpoot (boven klauwen)    10 px
zone 3 verre achterpoot                      26 px
zone 3 nabije achterpoot                     12 px
totaal 90 | buiten de zones: 0
```
Ongewijzigd (0 px):
- lijf, staart, neus en oog (3×3: lid, glans, iris);
- de klauwen van de opgetilde poot (y ≥ 56).

## Per zone
1. **Vlekken** (11 px):
   - de bovenste vlek is een zachte ronde vlek van 7 px boven en achter het oog: (20–21,36), (19–21,37), (20–21,38), met een glanspixel linksboven;
   - de onderste vlek is ook 7 px, onder en achter het oog richting de wang: (21–22,43), (20–22,44), (21–22,45);
   - tussen het oog en de onderste vlek blijft een donkere rij (y 42);
   - boven het oog scheidt het zwarte bovenlid oog en vlek.
   - Op 1× zie je op licht en op donker twee lichte punten in de zwarte muts.
2. **Verre voorpoot** (24 px):
   - de schouder loopt gekarteld over in de poot (y 48–50: b → d/y → m), in plaats van een horizontale grens;
   - daaronder is de poot een cilinder: m-selout links, y als lichtkant, z en m in het midden, k rechts;
   - de elleboog heeft een dubbele lichtstreep (y 52);
   - de pols is een knik in de licht/schaduwgrens (y 56: het licht schuift een kolom op);
   - de voet heeft een lichte bovenkant.
   - Hij blijft in de schaduwtint (geen Y), zodat hij achter de nabije poot ligt.
3. **Andere onderpoten** (48 px):
   - **Opgetilde voorpoot:** lichtkant y, hooglicht Y op de elleboog (y 51) en op de pols/hand (y 54), en schaduw onderaan.
   - **Verre achterpoot:** m-selout links in plaats van k, een lichtkant, en een hak bij y 53 (het licht verspringt), met overloop van bruin (d) naar donker bovenaan.
   - **Nabije achterpoot:** gekartelde overgang van de dij naar het onderbeen (y 51), het scheenhooglicht Y bovenaan, een hak bij y 55–56 (het licht schuift naar rechts, met een Y-bultje) en een hooglicht op de voet (y 58).
4. **Klauwtjes van de verre voorpoot** (7 px), **voor Jordi**:
   - Ik heb haakjes geprobeerd: een donkere teen met crème haakjes (variant A), en met een k-scheiding en een w-punt (variant B). Allebei lazen ze op 4× en 1× nog als losse kruimels.
   - Het silhouet geeft maar 1–2 px onder de voetlijn, zonder ruimte voor omlijning.
   - Daarom de terugval uit de opdracht: die pixels zijn nu deel van de voet (variant C, donker, als naar voren gestrekte tenen).
   - De varianten staan naast elkaar in `uitsnede_klauwen.png`.
   - Wil Jordi daar toch zichtbare klauwtjes, dan moet het silhouet daar 1–2 px groter (zone y 60–62, x 20–26).

## Zelf bekeken (1×, 4× en 8×, licht en donker, naast ronde 1)
- De vlekken lezen nu op 1×.
- De poten hebben volume en lezen niet meer als zwarte palen.
- De lichtkant van de verre voorpoot is een smalle verticale streep, met een knik bij de pols. Het is een cilinder, en zo bouwt Game Freak poten ook op.
- Het gezicht is niet vreemder geworden dan in ronde 1, en het oog is ongewijzigd.

## Lessen
- **Een vlek van 3–5 px leest op 1× niet in een zwart vlak**; 7 px (3 rijen, rond) wel.
- **Donkere poten krijgen volume** met de bivak-lichttint als lichtkant, en een gewricht door het licht een kolom te laten verspringen. Bij een verre poot alleen y, geen Y, zodat hij achter blijft.
- **Klauwtjes van 1–2 px onder de voetlijn** kun je zonder silhouetruimte niet omlijnen. Kies dan donker (voet) en leg het aan Jordi voor, in plaats van kruimels te laten staan.
