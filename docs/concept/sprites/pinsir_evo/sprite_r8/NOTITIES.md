# Pinsir-evolutie frontsprite, ronde 8 (verse maker, basis r7)

Jordi bij r7 (letterlijk): "arm, been zijn veel beter nu, qua kleur en tinten de goede kant op, staart ook beter, vleugel nog niet, hoofd ietsje beter, maar de vorm van het hoofd is niet mooi, de ogen zijn nu weer verdwenen, die moesten puntiger, niet kleiner, en de stekels zijn nergens echt netjes, kijk naar andere stekelige pokemon. Vleugel is ook nog niet gelukt, ik vraag me af of je daar naar andere pokemon hebt gekeken, je mag daar meer van het model afwijken zodat het naar een sprite vertaalt"

Bestanden: `pinsir_evo_r8_<oog>_<schild>.png` (A_A = hoofdvariant, A_B, B_A, B_B; 64×64, geïndexeerd, index 0 transparant, 16 kleuren incl. transparant, palet = r7), `bouw.py`, `kop_raster.txt` (kop/rug als tekstraster), `r7_delen.npy` (delenkaart van r7 uit `sprite_r7/bouw.py`, voor de bevroren delen), `vel.png`.
Bouwen: `cd pinsir_evo && python3 sprite_r8/bouw.py [raster|detail]`.

## Bevroren (script-check in bouw.py, alle varianten)
- Arm, verre arm, been, ver been, staart: **diff 0** met r7. Kaken, mond en romp (rij ≥ 29): **diff 0**. Palet ongewijzigd (tinten van arm/been/staart dus ook).
- Pixels anders dan r7 (met stekels), hoofdvariant: kopschild 115, rug 97, dekschild 177, kop (ogen) 5, nieuw silhouet 85. Silhouet anders: 87 px (kopschild, stekels, schildrand).

## 1. Hoofd (vorm)
- Het kopschild is een expliciet raster (`kop_raster.txt`), gemeten op het model (rooster 30×): zeshoekige plaat met een punt links (x10, rij 22), een rechte schuine bovenrand die naar achter oploopt, een rechte onderrand over het gezicht en een schuine achterrand onder de rug (binnenlijn in lijntint).
- Tinten: bovenband licht (c), vlak midden (b), lichte onderrand (c, zoals het model), glans (d) op de punt. Zwarte onderlijn = wenkbrauw (die zat in r7 ook al zwart).
- Afwijking: de plaat staat 1 rij hoger dan in het model (onderrand rij 24 i.p.v. 26), zodat de ogen 3 rijen krijgen. Kaken en mond zijn niet verschoven.
- De rugbult erachter is donker (a), met een lichte band onder de stekelvoeten.

## 2. Ogen (puntiger, niet kleiner)
- Het oog van Gen 3 Pinsir 1-op-1 (`graphics/pokemon/pinsir/anim_front.png`, nabij oog x30–35 rij 25–27, ver oog x22–27 rij 26–28): een schuin parallellogram van 3 rijen dat met de punt naar het midden wijst. Zwarte binnenhoek; de zwarte onderlijn van het kopschild erboven is de wenkbrauw.
- Grootte: nabij oog 7 witte px + pupil (B: 8; r4-oog A: 5), ver oog 6 + pupil (B: 7; r4 A: 3). Het oog is ook een rij hoger dan r4.
- **A**: met pupil, zoals Pinsir. **B**: zonder pupil, zoals het model (2 pixels verschil: de pupilpixels zijn wit). Andere oogvormen heb ik niet zelf verzonnen (SPRITE_KERN: neem een bestaand Gen 3-oog over).

## 3. Stekels
- Opbouw van Tyranitar en Sandslash (vel 8×): een vin die naar rechts helt. De linkerrand is recht, de rechterrand schuift 1 px per rij op en de punt is 1 px zwart. De linkerflank is licht (d), het midden c en de rechterflank donker (b). De vulling loopt zonder lijn door in de bovenband van het lijf.
- Plekken volgens het model:
  - Kopschild: 4 stekels, van klein naar groot: (15,18), (18,17), (23,15), (26,14). Ze staan 1 rij hoger, net als het kopschild.
  - Rug: (32,13), (38,13) en (44,18).
  - Achterrand van het kopschild: twee kegels, (31,18) en (35,20). Ze hebben een omlijning in de lijntint, zodat er geen extra zwart bij komt.
  - Rugrand naast het schild: 5 doorns. Ze lopen van groot naar klein, net als in het model: (49,21), (51,27), (53,31), (54,36), (56,42).
- De derde kegel van het model (27,20) valt weg: die zou in de voet van de grote kopstekel vallen.
- **Niet gedaan**: de stekels op de staart en de klauwen van de poten. Die horen bij staart en poten, en die zijn bevroren (diff 0). Moeten die ook netter, dan is dat een aparte stap.

## 4. Dekschild (mag afwijken van het model)
- Vorm: de linkerrand blijft zoals in r7 (grens met arm en romp). De rechterrand is een gladde bolle curve, gemeten op het model: x44 (rij 24), x50 (31), x52 (37), x54 (43), punt (52,47). Daarachter ligt de donkere rugrand met de doorns.
- Basis voor beide varianten:
  - lijn in de schildlijntint tegen arm, romp en rug;
  - lichte rand linksboven, 1–2 px (zoals Ledian);
  - okervlak;
  - schaduwsikkel rechtsonder, breder naar de punt.
- **A: aanpak van Mega Pinsir en Ninjask.** Weinig, grote, vlakke contrastvormen direct op de basiskleur, zonder lijntjes. De V-tekens van het model worden drie dikke V's (2 px) die naar de punt wijzen. Langs de bovenkant van elke V loopt een lichte streep, zoals in het model licht naast donker ligt.
- **B: aanpak van Shuckle en Dustox.** Ronde vlekken in een regelmatig patroon. Het zijn zeven schorsknobbels in twee rijen langs de lengteas, elk met een schaduwrand rechtsonder (bultjes zoals bij Shuckle).
- Vel: beide naast hun referenties op 8×, en naast het model.

## Controle
- 16 kleuren incl. transparant, index 0 transparant; zwart 19,1 % (r7 19,4 %).
- Tintvlekjes < 3 px (8-samenhang, vultinten, hele sprite): 37 in A_A. Het grootste deel zit in de bevroren delen (r7) of is bewust:
  - de 1-px lichte flanken van de stekels (glans);
  - de oogpixels (Pinsir 1-op-1).
- Geen lichte kleur op de buitenrand: de doornvulling ligt binnen de zwarte lijn.

## Zelf geziene zwakke punten
- Het kopschild is lichter dan in het model (b/c tegen het donkere model), zodat de plaat los leest van de rug. Kleur mocht afwijken, maar het is een keuze.
- Schild B leest eerder als "koekje met vlekken" dan als dekschild. A ligt dichter bij het model.
- De rugbult tussen kopschild en schild is een groot donker vlak met alleen een lichte band boven. Dat is het model (bijna zwart), maar het is vlak.
- De staartstekels zijn nog de r7-pixels (bevroren, zie punt 3).

Verse keurder nodig vóór Jordi.
