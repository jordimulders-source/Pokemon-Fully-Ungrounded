# Pinsir-evolutie (Bug/Ground) frontsprite, ronde 2

Bestanden: `pinsir_evo_r2.png` (64×64, geïndexeerd, index 0 transparant, 14 kleuren incl. transparant), `kaal.png`, `bouw.py`, `vel.png` (r2 8× | r1 8× | model 8× / close-ups / 1×). Bouwen: `cd pinsir_evo && python3 sprite_r2/bouw.py` (vereist scipy en scikit-image).
Basis = r1-methode (reductie op het 1024-model, meerderheid per cel). **Mond en kaken bevroren** ("de mond en de kaken zijn goed"): kaakpixels van r1 + 1 px eromheen en het gezichtsvak x13–24, y26–36 komen 1-op-1 uit r1 (script-check: diff 0, behalve de benoemde ogenpixels).
r2 wijkt in 276 px af van r1 (per zone t.o.v. r1: zie `zones.py sprite_r1/pinsir_evo_r1.png sprite_r2/pinsir_evo_r2.png`; y40–62: 177 px, y≤24: 42 px, dekschild 18 px + paletwissel).

## 1. Poten en onderlijf (y ≥ 36) — uit de modelplaten
- `model.platen()`: de zwarte modellijnen verdelen het lijf in platen; elke plaat = 1 vlak in de band van zijn **gemeten mediane modelhelderheid** (<50 → 2, <72 → 3, <95 → 4, ≥95 → 5); licht (5) alleen op de **modelglans** (helderheid ≥ max(95, mediaan+20): de knieplaten).
- Lijnen: waar de middellijn (skelet) van een zwarte modellijn door de cel loopt (≥ 9 skeletpixels per cel van 15 px) of het model ≥ 70 % zwart is. Zo worden plaatranden en buiksegmenten doorlopende 1-px lijnen op de modellijnen i.p.v. losse brokken; vlak = grootste niet-zwarte plaatklasse.
- Binnenlijn tussen donkere massa en lichtere plaat (≥ 2 lichtere buren) → donkerste lijftint 2 (Gen 3); tussen twee donkere vlakken blijft zwart (anders verdwijnt het segment).

## 2. Dekschild
- Gemeten binnen het schild (zonder rand): model donker/midden/licht = **51/28/21 %**, r1 = 57/23/20 %, r2 = gelijk aan r1 in verhouding. De donkere tekening was er dus al; ze las niet doordat de vlektint (90,52,26) te dicht bij de middentint lag. **Vlek → modelmediaan (74,42,20), midden → (150,104,64)** (model 77,46,22 / 139,100,69). Vorm: grotere vlakken van r1 (3×3-gemiddeld, geen dambord).

## 3. Zwart
- Gemeten: modelzwart (L<25) = **22,7 %** van de figuur, waarvan 18,9 % echt zwart (L<12): de modellijnen zijn echt zwart, niet donkerbruin. r1 31,4 % → **r2 29,4 %**.
- Zwart weegt 1,0 i.p.v. 1,3; zwarte binnenpixel met < 50 % modelzwart in de cel → donkerste tint (2, of 6/9 in kaak/schild); plaatranden naast lichter lijf → 2 (zie 1).
- Rest: buitenlijn 1 px is op deze schaal relatief dikker dan de modelomlijning (±0,66 spritepx), en de buiksegmenten in de donkere massa blijven zwart.

## 4. Stekels
- Boven y21 telt een cel die direct op de figuur staat mee vanaf 25 % modeldekking (alleen de modelstekels): **5 stekelpunten erbij** (38,13) (26,15) (22,18) (40,18) (15,19) — silhouet t.o.v. r1 alleen daar anders.
- Stekel (loop ≤ 3 px breed, y ≤ 20): achtergrond rechts/punt → zwart, achtergrond links → selout 3, binnenin → 4 (lichte modelflank).

## 5. Ogen (Jordi: "ogen zijn ook gewoon een rij witte pixels")
Model gemeten (8×): boze schuine ogen onder de kopschildrand; links crème (16,27) schuin naar (17,28) met zwart rechtsboven; rechts een klein stukje (21,28) + hoofdstuk (22–23,28), donkere inkeping rechtsonder (pupil), zwarte wenkbrauwband erboven. Opgebouwd zoals de Gen 3-Pinsir (wit, zwarte pupil in een onderhoek, wenkbrauw die aan de binnenkant op het oog drukt). Gezette pixels:
- links: (16,27) wit, **(16,28) wit (nieuw, was gezicht)**, (17,27) zwart wenkbrauw, **(17,28) zwart pupil** (model: klein crème stukje).
- rechts: **(22,27) (23,27) wit** (model: wenkbrauwband; oog 1 rij omhoog zodat het 2×2 wordt en niet met de mondrand y29 versmelt), (22,28) wit, **(23,28) zwart pupil** (model: inkeping), **(21,28) zwart** wenkbrauwpunt (model: klein crème stukje), **(22,26) (23,26) (24,26) zwart** wenkbrauwband 1 rij omhoog mee (was lijf 5).

## Controle
14 kleuren incl. transparant, geen lichte kleur op de buitenrand, geen losse zwarte pixels binnenin. Lijf 4 tinten (2/3/4/5; 4 nog maar 31×).
Let op: het palet in `gereedschap/gemeen.py` is aangepast (9/10); `sprite_r1/bouw.py` opnieuw draaien geeft r1 nu met die tinten.

## Twijfels
- **Poten** lezen beter (buiksegmenten, knieplaten met glans, klauwen), maar zijn donkerder dan in r1: veel platen hebben in het model een mediane helderheid onder 50 (tint 2). Lichter = afwijken van de gemeten middentint.
- **Zwart 29 %**: verder omlaag kan alleen door echt zwarte modellijnen te vervangen (buiksegmenten in de donkere massa) of de buitenlijn deels selout te maken.
- **Linkeroog** blijft smal (1 px wit + zwart ernaast): het verre oog heeft in het model maar ±1 px breedte. Het rechteroog is 2×2 met pupil.
- **Dekschild**: verhouding klopt al met het model; als het nog te licht leest, ligt het aan de vorm (model: lange diagonale strepen) die op 64 px tot vlekken wordt.
