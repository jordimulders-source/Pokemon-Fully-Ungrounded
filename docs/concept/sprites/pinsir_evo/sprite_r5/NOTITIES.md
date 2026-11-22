# Pinsir-evolutie frontsprite, ronde 5 (basis r4_A, oog A bevroren)

Jordi op r4: "oog a is goed, hij is nog steeds super blurry, het ligt aan het feit dat er niet genoeg kleurtinten gebruikt worden en de lijnen te zacht zijn" · "en nee dat betekent niet meteen zwarte lijnen doen nu".

Bestanden: `pinsir_evo_r5.png` (64×64, geïndexeerd, index 0 transparant, 16 kleuren incl. transparant), `bouw.py`, `onderlijf5.txt` (1 handmatige pixel: de losse zwarte (24,56) → schaduwtint), `vel.png` (r5 | r4A | model op 8×; 1× naast Gen 3 Pinsir/Heracross/Scizor op wit en donker). Bouwen: `cd pinsir_evo && python3 sprite_r5/bouw.py`.

## Controle (script)
- Silhouet-diff met r4A: **0**. Ooggebied (x14–25, y26–28) gelijk aan r4A (alleen paletwaarden anders).
- **Nieuw zwart: 0**; zwart weg: 5 (r4-zwart in het onderlijf zonder modellijn, waaronder de losse pixel (24,56)). Zwart 26,7 % (r4 27,0 %).
- Tintvlekjes < 3 px in de vulling: 43 (r4: 63, r3: 153).
- Buitenrand: zwart, of de lijntint van het onderdeel (lijf/kaak) als gekleurde omlijning; geen middentint meer op de rand, ook niet op de kaakbovenrand. Uitzondering: lichte klauwpunten (y ≥ 53), zoals r3/r4.

## Tinten per kleurgroep (helderheid (R+G+B)/3; zwart 15)
| groep | r4 | r5 | stappen r5 |
|---|---|---|---|
| lijf | 61 / 95 / 131 / 175 (4) | **36** lijn / 77 / 110 / 146 / 190 (5) | 41 / 33 / 36 / 44 |
| kaak | 57 / 91 / 135 (3) | **41** lijn / 69 / 101 / 143 (4) | 28 / 32 / 42 |
| dekschild | 56 / 106 / 157 (3) | **40** donkere rand / 65 / 111 / 162 (4) | 25 / 46 / 51 |
| oog/tand | 221 / 144 | 221 (tandschaduw vervalt → lichte lijftint 146) | |
Gen 3 ter vergelijking: Pinsir 68/106/136/169, Heracross 67/101/147/192, Tyranitar 72/120/173/213 (stappen 30–53).
Gebruik r5: lijf lijn 150 px, schaduw 338, midden 206, licht 137, glans 32; kaak 16/45/59/35; schild 28/93/45/43.

## Wat er gedaan is
1. **Volle palet (16)**: lijf een lijntint erbij (voor gekleurde lijnen) en de schaal gespreid; kaak een lijntint (gekleurde omlijning bovenrand); dekschild een donkere-randtint (schaduwkant langs de zwarte omlijning, rechts/onder).
2. **Lijnen zonder extra zwart**:
   - buitenrand aan de lichtkant: de middentint-selout van r4 is nu de lijntint van het eigen onderdeel (68 px); dunne stekels/klauwen de schaduwtint;
   - lijf direct tegen kaak of dekschild zonder lijn ertussen: lijfpixel → lijntint (20 px);
   - gaten tussen lijnstukken langs de modellijnen (skelet ≥ 7 px in de cel) gedicht in lijntint (6 px).
3. **Onderlijf (y ≥ 36) opnieuw uit het model overgenomen**: per cel de mediane modelhelderheid → 4 tonen (< 40 schaduw, < 62 midden, < 88 licht, ≥ 88 glans; verre ledematen één toon lager); lijnen waar de modellijn door de cel loopt (≥ 9 skeletpixels): zwart als r4 daar zwart had, anders lijntint. Buitenrand en grenzen met kaak/schild ongemoeid.
4. **Kopschild-facetten uit het model**: modeltoon gladgestreken (5×5) en in 3 banden op de eigen toonverdeling (30/75 %): lichte voorste facet linksboven, donkerdere achterste facetten rechts.

## Afwijkingen van het model
- Kleur lichter en meer contrast dan het model (zoals r4).
- Ogen 2 rijen (oog A, bevroren).
- 5 zwarte pixels weg (geen modellijn).

## Zelf geziene zwakke punten
- **Onderlijf blijft druk**: de romp en schenen zijn in het model zeer donker; schaduwtint, lijntint en zwart liggen daar dicht bij elkaar en de vele korte r3/r4-lijnstukjes blijven staan (zwart weghalen alleen waar geen modellijn is). Dit is het punt waar "blurry" nog vandaan kan komen.
- De nieuwe lijntint is vooral aan de buitenrand en bij kaak/schild ingezet; binnenlijnen in het lijf zijn nog grotendeels zwart (r4) met maar 6 gedichte gaten.
- Kopschild-facetten lezen als een licht vlak links en een donker vlak rechts; geen scherpe facetlijn.
Een verse keurder is nodig vóór Jordi.
