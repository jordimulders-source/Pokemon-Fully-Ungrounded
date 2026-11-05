# Lama fase 3: kleur ronde 3 (5 nov)

**Jordi over 2b (letterlijk):** "de snuit is nog niet goed, maar ik had eerder al gezegd dat je buiten het silhouet mag gaan om de sprite beter te maken. Het lijkt nu alsof die stom staat te lachen, maar het moet juist een hele neutrale lama blik zijn. Dus maak het hoofd maar wat groter dan het silhouet".

Gemaakt vanaf `ronde2b/ronde2b.txt`. De kopzone (y0–21, x10–33: kop, oren, bombín, vlecht, hals tot de bovenrand van de halsband) is helemaal opnieuw met de hand getekend in `bron/kop.txt`. `bron/bouw.py` plaatst en controleert alleen.
- **Buiten de kopzone: 0 px diff met 2b** (lijf, hals onder de halsband, kleding, poten). `bouw.py` controleert dat.
- 222 px gewijzigd, alle binnen de kopzone. Palet ongewijzigd, 15 kleuren, 0 open randen (ook de oren niet meer).

## Pixels buiten het silhouet: +101 (en 5 silhouetpixels niet gevuld)
| zone | aantal | waar |
|---|---|---|
| kop | 37 | voorhoofd en snuit naar links/voren: x12–18, y10–20 |
| bombín | 26 | bol x17–18 en x22–24, y3–7; rand x13–18 y8, x16–18 y9 |
| oren | 17 | hoger en verder uit elkaar: x17–19 en x25–28, y0–4 |
| vlecht | 21 | krullen die achter de kop uitbollen: x27–30, y9–19 |

- **Niet gevuld (−5):** x21/x24 op y1–2 (de oorpunten staan nu verder uit elkaar) en x27 y8 (achter de rand).
- Per pixel in `alpha_diff.txt`. Let op: `bouw.py` telt x27–28 op y3–4 bij "bombin/oren" en "vlecht"; dat zijn pixels van het rechteroor, en zo staan ze in de tabel.

## Wat ik deed
1. **Kop ±1,25×:**
   - Breedte x12–26 (was x15–26) en hoogte y9–20 (was y10–20).
   - Hij groeit naar voren/links en omhoog. Bombín en oren schuiven 1 rij mee omhoog (rand y8, oorpunten y0).
   - De achterkant (x26) en de aansluiting op de hals (y20–21) blijven op hun plek.
   - De snuit is één stompe, ronde vorm, zoals in de onderlaag en foto 1.
2. **Neutrale lama-blik:**
   - De schuine mondlijn uit 2b is weg (die las als een lach). Nu een korte horizontale mondlijn `ddd` (x13–15, y17), zonder opgetrokken mondhoek.
   - Daarboven het neusgat `k` (x14 y15) en de gesplitste bovenlip als kort verticaal lijntje `d` (x14 y16).
   - Daaronder een hangende onderlip als zachte bol (x13–15, y18–19), 1 px teruggezet ten opzichte van de bovenlip.
   - Dan de kin-onderlijn `kkk` (y20) naar de hals.
   - **Oog:** zwaar vlak bovenlid `kkkkk` (x20–24, y13) met de lidmassa `SSSS` erboven (y12). Half gesloten: één rij `dHkkd` (glans laag vóór, donkere iris) en een zacht onderlid `SS`. Geen wenkbrauw en geen opgetrokken lid.
3. **Bombín zoals in de onderlaag:**
   - Bol 8×5 (x17–24, y3–7) met glans `SS`/`S`/`d` linksboven en een rode band `RRrrrrm` (y7).
   - Rand 14 px (x13–26, y8) met glans `dd`. Aan de rechterkant zakt hij naar y9.
   - **Oorpunten zichtbaar:** het linkeroor y0–4 (5 rijen), het rechteroor y0–7 (punt plus buitenkant).
4. **Vlecht als krullen:** vier knotten van 3 rijen langs achterkop en hals (x27–30, y9–20), afwisselend licht (bruin met crème lichtje) en donker. Elke knot bolt in de middelste rij 1 px uit (x30). Hij eindigt in de rode tullma `Rrm` (y21–22), tegen de halsband. Tussen oog en vlecht zitten 2 kolommen kop (x25–26).

## Eerlijke zwakke punten
1. **De snuitvoorkant is 4 rijen recht** (x12, y14–17). De mondlijn breekt hem, maar het blijft een rechte rand van 4 px.
2. **Het zware lid (5 px `k`) met de lidmassa erboven** leest op 1× als een donkere streep. Dat is bedoeld als droge, halfgesloten blik, maar Jordi moet beoordelen of het neutraal oogt of nors.
3. **De vlecht is op 1× een hobbelige donkere rand achter de kop;** de knotten lezen pas vanaf 2×.
4. **De kop is groter, maar de hals eronder niet** (die is bevroren). De overgang kin → hals op y20–21 is daardoor smaller dan in de onderlaag.

## Bestanden
- `ronde3.txt`, `lama3.png`, `normal.pal`, `alpha_diff.txt`.
- `vel_ronde3.png`: zelfde opbouw als 2b; kop 8× met onderlaag | 2b | 3 | foto 1.
- `bron/`: `kop.txt` (het handwerk), `bouw.py`, `vel.py`.

## Lessen
- Een schuine mondlijn die naar achteren omhoog loopt, leest als een glimlach. Een lama-snuit wil een korte horizontale mondlijn met een hangende onderlip.
- Mag de kop groter dan het silhouet, teken dan de hele kopzone als één blok opnieuw (tekstraster van vaste breedte). Pixelreparaties op de oude kop houden de oude verhoudingen vast.
