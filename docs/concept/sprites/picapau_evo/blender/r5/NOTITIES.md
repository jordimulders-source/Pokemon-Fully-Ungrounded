# Evo van Picapau, modelronde 5 (r5): imposant, open snavel, spiraaloren, bolle buik

## Jordi letterlijk
- Over r4 V2: **"ja nu komen we ergens! de snavel mag open, dat geeft wat karakter. Vergeet mijn eerdere instructies over de oren, die mogen dunner en wat verder doorkrullen, iets meer zoals de onderkant van de oren van raichu"**
- Op de vraag of de imposant-ronde mocht: **"ja"**.
- Aanvulling: **"ja en in de pose mag de buik echt naar voren, die laten we een beetje op die gen 1 raichu pose lijken"**
  - Coördinator: alleen de houding en de bolle buik overnemen, geen Raichu-lijf. Het blijft een vogel.
- Hiermee vervallen de oude oorgrenzen ("too much", "te wit, te groot").

## Bestanden
- `picapau_evo_r5.py`: model, een eigen kopie van r4. r4 is niet aangepast.
- `maak_r5.py` maakt de uitvoer:
  - `R5_8x.png` en `R5_1x.png`, in de stand van r4 V2 (lijf 35, kop +5, oog_az 65), passend in 61 px (schaal 0,796);
  - `vel_r5.png`: render op 8× en 1×, naast r4 V2, Staraptor, Braviary, Talonflame en Raichu Gen 1;
  - `closeup_r5.png`: kop, snavel en oren op 8× (render en 1×), naast de oren van Raichu Gen 1 en Gen 3.
- Snelle proef: `STAP=0.5`, ±30 s. Volle render: ±4 min.

## Wat ik zie aan de onderkant van Raichu's oren
- **Gen 1:**
  - Onder het rechteroor hangt een losse zwarte spiraal van 1 px dik en ±8–9 px doorsnee, die naar binnen oprolt (±1½ slag).
  - Er zit een duidelijk wit gat in het midden.
  - Hij hangt aan de onderste punt van het oor, rechts naast de kop.
- **Gen 3:**
  - Aan de punt van het rechteroor loopt een dunne donkere lijn (1 px) door.
  - Die buigt omlaag en terug naar binnen: een haakje of open spiraal van ±5 px onder de oorpunt.
- **Gemeen:** het oor eindigt niet in een punt maar loopt over in een dunne lijn die onder de punt omkrult.

## Wat er veranderd is (de rest is r4: kleuren, stippen, vleugelopbouw, staartschacht, vorm van de bliksem)
1. **Imposant.**
   - **Voorover:** het lijf helt meer naar voren, als de diagonaal van Talonflame.
     - De romp-as ligt 17° platter: 18° onder de horizontaal, was 35°. De borst is langgerekt langs die as. De nek staat schuin naar voren, de kop zit voor en boven de borst.
     - Dit zit in de vorm zelf, niet in een rotatie van het hele lijf; dan bleven de kop en de poten op hun plek.
   - **Vleugels:** hoger en breder open. De pols zit hoger en verder naar buiten en de vleugel is 1,32× zo groot (r4: 1,2×).
     - De verre vleugel staat verder naar achteren, zodat de zwarte oorkrullen tegen de lucht staan en niet tegen de donkere vleugel.
   - **Bliksem:** 0,75× zo lang. De breedte krimpt minder, zodat hij op 1× ≥ 2–3 px blijft. Hij staat verder naar links, zodat de buik hem niet bedekt.
   - **Voeten:** grote voeten met dikke loopbenen, 2 tenen naar voren en 2 naar achteren (specht), met donkere klauwen.
     - De verre poot staat 3,5 BU verder naar achteren en 4 BU hoger, dus niet naast de nabije.
2. **Snavel open.**
   - De bovensnavel wijst 5° omhoog, de ondersnavel 9° omlaag en is 0,88× zo lang.
   - Daartussen zit een donkere mondopening: een plaat in het middenvlak van de kop.
   - Op 1×: de bovensnavel is 2–3 px, de ondersnavel ±2 px, met een donkere mond van 1–2 px ertussen.
3. **Oren.**
   - Het blad is dunner (voet ±4 BU, was ±7) en staat nog steeds zwart en achter op de schedel.
   - De punt loopt over in een spiraal van ±410° die onder de punt hangt en naar binnen oprolt. De straal krimpt van 4,6 naar 1,9 BU en de lijn is 2,4 → 1,7 BU dik.
   - Op 1× is dat bij het nabije oor een zwarte ring van 2 px met een gat van ±2 px (zie de close-up). Het verre oor is een haak, net als bij Gen 3.
4. **Bolle buik (Raichu Gen 1-houding).**
   - Er is een grote bol vooraan-onder bij gekomen (straal ±12), die naar voren en iets naar de kijker uitpuilt.
   - De crème buikovaal is meegegroeid en is nu het grootste lichte vlak.
   - De kop zit erboven en het lijf buigt er gedrongen omheen. Nek, vleugels en poten blijven die van een vogel.

## Hoofdvraag: leest het op 1× als een grote vogel met Raichu-motief?
- **Vogel: ja.**
  - De open snavel geeft karakter en leest ook op 1× als twee snaveldelen.
  - Ook de gelaagde vleugels, de nek en de poten met klauwen lezen.
- **Raichu-motief: beter dan r4.**
  - De bolle crème buik vooraan geeft de houding van Gen 1.
  - De oorspiraal leest op 1× als ring met gat.
  - Verder zijn er de staartlus en de bliksem.

## Eerlijke zwakke punten
1. **Silhouet.** Naast Talonflame en Braviary blijft het meer "dikke vogel" dan "roofvogel". Door de bolle buik (Jordi's wens) en de opgerichte vleugels is de vorm vooral een ronde massa met een waaier erachter.
   - Dat past bij "een beetje Raichu", maar de diagonaal van Talonflame is daardoor minder zichtbaar dan in de proef zonder buik.
2. **Bliksem en staartlus.**
   - De bliksem is nu vrij klein en steekt maar half onder de buik uit.
   - De staartlus loopt onder door naar rechts en neemt veel breedte in.
   - Een iets grotere bliksem (0,85×) zou hem beter laten lezen.
3. **Verre vleugel.** Hij staat nu ver naar achteren en is grotendeels verborgen achter de nabije vleugel. Daardoor lijkt het meer op één grote vleugel.
4. **Kleur in de render.** De snavel is licht hoorn en de pootkleur grijs. In de sprite worden die de grijze snavel van Picapau en donkere klauwen.

Deel B (sprite) is nog niet begonnen; dat wacht op de coördinator.
