# Pinsir-evolutie frontsprite, ronde 6 (verse maker, pitahaya fase 3 / spooktrein-methode)

Jordi bij r3: "ogen niet goed en beetje zelfde probleem als pitahaya fase 3 had", "als in hele sprite blurry".
Jordi bij r4: "oog a is goed, hij is nog steeds super blurry, het ligt aan het feit dat er niet genoeg kleurtinten gebruikt worden en de lijnen te zacht zijn", "en nee dat betekent niet meteen zwarte lijnen doen nu".

Bestanden: `pinsir_evo_r6.png` (64×64, geïndexeerd, index 0 transparant, 16 kleuren incl. transparant), `bouw.py`, `vel.png` (r6 | r5 | model op 8× | segmentkaart; 1× r6, r5, Gen 3 Pinsir/Heracross/Tyranitar/Aggron op wit en donker; 2× op wit). Bouwen: `cd pinsir_evo && python3 sprite_r6/bouw.py [raster|detail]`.

## Methode (geen celreductie + oplappen meer)
1. **Segmentatie op modelresolutie**: zwarte modellijnen (L < 22) verdelen het 1024-model in vlakken; 37 vlakken ≥ 600 modelpx, met de hand benoemd (`VLAKKEN`: kopschild, rug/rugstekels, kop, romp/buiksegmenten, nabije arm, nabij been, dekschild, ver been, verre arm, staart) met een diepte (wat vooraan ligt). Snippers en lijnpixels gaan naar het dichtstbijzijnde grote vlak. Spritepixel = vlak met de meeste niet-lijnpixels in het midden van de cel (smalle delen zoals de onderarm blijven). Eén samenvoeging: nekstrook 60 → nekkraag 55 (anders 1-px strepen tussen twee lijnen).
2. **Lijnen**: alleen grenzen tussen vlakken die in de sprite ≥ 3 px lang zijn, plus lange modellijnen binnen een vlak (≥ 80 modelpx skelet: buiksegment, dij/knie, rugnaad); niet in het dekschild (tekening = textuur) en niet in de kop (bevroren). Lijn komt in het vlak dat ACHTER ligt, zodat voorste delen hun vulling houden; daarna uitgedund tot 1 px (`thin`) en ellebogen weg. Binnenlijnen in de gekleurde lijntint van het onderdeel (lijf 38, schild 40), **geen zwart binnenin**. Lijf tegen de kaak: lijntint. Buitenrand: zwart (model is rondom zwart omlijnd).
3. **Vulling per vlak**: basistint uit de modelmediaan van het vlak (< 45 schaduw, < 72 midden, anders licht); daarbinnen de gladgestreken modeltoon met drempels op de eigen verdeling (−1 / +1 / glans alleen waar het model ≥ 105 is); waar het model binnen een vlak vlak is: sikkel rechtsonder −1, linksboven +1. Verre arm/been −1, nabije arm/been +1 (lichtere platen zoals het model). Dekschild: modeltekening (vlek/midden/licht) per cel. Tintvlekjes < 3 px naar de buurtint.
4. **Bevroren uit r5**: oog A, mond, kaken (kaakpixels + hun zwarte omlijning), silhouet.

## Controle (script)
- Silhouet-diff met r5: **0**. Bevroren zones (oog, mond, kaken) diff: **0**.
- **Zwarte binnenpixels** (zwart met 8 buren in de figuur): **r6 39, r5 215**; alle 39 zitten in het bevroren oog/mond/kaakgebied, **0 daarbuiten**. Zwart totaal 19,1 % (r5 26,7 %), vrijwel alleen buitenrand.
- **Tintvlekjes < 3 px** (vulling, 4-samenhang): **r6 25, r5 43**; met 8-samenhang (schuine 1-px stroken tellen als één): **r6 6, r5 26**. Van de 25: 8 in het bevroren gezicht, de meeste andere zijn de schuine nekstrook (x27–31, y32–35) en losse pixels tegen een lijn.
- Binnenlijnen: 56 vlakgrenzen + lange binnenlijnen, 282 px lijntint.

## Tinten (helderheid (R+G+B)/3; zwart 15)
| groep | tinten | stappen |
|---|---|---|
| lijf | 38 lijn / 65 / 98 / 134 / 178 glans | 27 / 33 / 36 / 44 |
| kaak (bevroren r5) | 41 / 69 / 101 / 143 | 28 / 32 / 42 |
| dekschild | 40 lijn / 65 / 111 / 162 | 25 / 46 / 51 |
Gen 3: Pinsir 68/106/136/169, Heracross 67/101/147/192, Tyranitar 72/120/173/213.
Lijf-palet donkerder dan r5 (schaduw 77 → 65): de romp is in het model bijna zwart; zo leest de romp donker en de platen (kopschild, schouder, knie, onderarm) licht ertegen.

## Afwijkingen van het model
- Kleur lichter en meer contrast dan het model (mag, Jordi 17 nov); nabije ledematen een stap lichter.
- Korte modellijnen, de dekschildnaad langs de rand en de fijne schorslijntjes vervallen (textuur); de schorstekening blijft als vlekken van ≥ 3 px.
- Nekstrook 60 en nekkraag 55 als één vlak.

## Zelf geziene zwakke punten
- Onderlijf links (verre arm, ver been, x15–31, y44–58) blijft een donkere massa met een paar lijnen; dat is het model (donker), maar de verre voet en klauwen lezen op 1× matig.
- Staart: segmentlijnen om de 3 px (zoals het model) geven een licht streeppatroon.
- Nekstrook tussen kaak en borst is een schuine 1-px strook tussen twee lijnen (model: dunne kraagplaatjes).
- Dekschildtekening is kleiner/rustiger dan de brede schorsbalken in het model.
Verse keurder nodig vóór Jordi.
