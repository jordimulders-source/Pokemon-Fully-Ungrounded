# Eindkeuring pitahaya-draak fase 1, sprite r5 (16 nov)

r5 = r3 + de 6 MOET-wissels van keuring_r3 + oogvariant B (door Jordi gekozen).
- **Vel:** `vel.png`. Bovenaan r3 | r5 op 1× en 2× (licht en donker). Daaronder het ooggebied op 16×: r3 boven, r5 onder, en naast r5 het natieve model in fase B (1 natieve px lager).
- **Scripts:** `stats.py`, `rand.py`, `vlak.py` en `grens.py` (kopieën voor r5), plus `keuring_r2/klont.py`.

## Oordeel: **FAIL, 1 px** (één tintwissel in de iris; daarna PASS)

### 1. Buiten het ooggebied pixelgelijk aan `keuring_r3/sim_moet.png`
- Er wijken 16 px af van de simulatie, en alle 16 liggen in x 18–36, y 22–27: 0 px erbuiten.
- Het palet is gelijk en het silhouet ook.
- De 16 oogpixels zijn: (18,26), (20,24), (21,25), (22,24), (22,26), (29,26), (31,23), (31,24), (31,25), (31,27), (32,25), (32,27), (34,22), (34,23), (34,26) en (36,23).

### 2. Metingen opnieuw (r5 | sim_moet r3)
| meting | r5 | sim r3 | Gen 3-refs (Bagon / Treecko / Larvitar / Oddish / Cacnea) |
|---|---|---|---|
| zwart van de figuur | 16,7 % | 17,3 % | 6 / 18 / 12 / 12 / 18 |
| zwart binnen de figuur | 7,5 % | 8,1 % | 0,9 / 4,1 / 5,0 / 2,6 / 7,7 |
| losse zwarte pixels | 12 | 8 | 2 / 4 / 1 / 4 / 8 |
| 2×2 zwarte klonten | 6 | 7 | 0 / 1 / 3 / 0 / 16 |
| dambord 2×2 | **4** | 3 | 7 / 11 / 4 / 11 / 14 |
| zwakke tintgrenzen (RGB < 60, helderheidsverschil 32–35) | 15,4 % | 15,5 % | 0,5 / 6,1 / 10,2 / 6,2 / 23,4 |
| buitenlijn: schaduwkant zwart / lichtkant selout / om-en-om | 71/71 · 56/68 · 0 | gelijk | |

- **Losse zwarte pixels: 12.**
  - 4 zitten in het oog: (21,24), (22,25), (30,24) en (29,25). Ze zijn geen echte losse pixels maar diagonale lidlijnen; ze raken hun lijnbuur schuin.
  - 4 zitten in de mond: (21,31), (22,32), (31,31) en (33,30).
  - 4 zijn echte modellijnen van 4–5/9 zwart: (31,10), (44,19), (42,27) en (40,30).
  - Buiten het gezicht zijn het er dus 4, net als in r3.
- **Dambord: 3 diagonale lijnen (zoals in r3) en één nieuwe in de iris:** (33,25)–(34,26) = 12/13 over 13/12. Dat is de MOET hieronder.
- **Tinten en contrast:** ongewijzigd ten opzichte van r3. Roze heeft stappen van 33 / 38 / 35, groen 32 / 33 / 37. Amber 12 → 13 is een stap van 51; dat is een iris, vergelijkbaar met Gen 3-ogen.

### 3. Ooggebied, technisch (het ontwerp is van Jordi; ik toets alleen de techniek)
- **Nabije oog:** de lidlijn is 1 px en loopt schuin en doorlopend: (29,25) → (30,24) → (31–33,23) → (34–35,22), en sluit rechts via (35,23)–(35,25). Glans (31,24) wit linksboven tegen de pupil (32–33,24). Iris donker amber boven, licht amber onder, zoals het model in fase B. De pupil en het lid vormen samen een 2×2-zwart (32,23); dat is gewoon voor Gen 3-ogen.
- **Verre oog:** het lid (19–20,23) en de glans (20,24) staan op de modelplek van de witte pixel; de iris (20–21,25–26) staat eronder. Het oog is smaller dan het nabije, dus het perspectief klopt.
- **Glans:** 1 px per oog, wit, linksboven, past bij de lichtrichting.
- **Trouw:** elke oogpixel komt uit de reductie van het natieve model (fase B); niets is getekend. Op 16× naast het model in fase B kloppen het lid, de glans en de verdeling van de iris.
- **r5 tegenover r3 (1×, 2×):** de ogen lezen scherper. Het nabije lid is een strakke lijn in plaats van een zwarte klont, en het verre oog heeft nu glans. De rest van de sprite is gelijk. **r5 is beter.**

## MOET (1 px)
1. **(34,26) 12 → 13** (dambord in de iris).
   - Model in fase B: 3/9 amber met lum 154, de rest is roze huid en de onderrand; geen zwart.
   - Met 13 wordt de onderste irisrij (30–34,26) één lichte band, en blijft de bovenste rij (30–33,25) donker amber. Dat is precies de verdeling "donker boven, licht onder" van variant B.
   - Het verschil met het model (een kwart pixel amberrand) is kleiner dan 64 px kan tonen.
   - Controle na de wissel: diff met r5 = 1 px en dambord = 3.

## KAN
- Geen nieuwe. De punten van keuring_r3 blijven KAN: tint-3-vlakjes in de schaduwband rechts, (30,13) en de naadfragmenten in de kruin.

## Ter info
- Ooggebied: x 18–36, y 22–27, variant B (Jordi).
- Grootte: 31×49, 1087 px.
