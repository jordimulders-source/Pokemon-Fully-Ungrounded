# Keuring Dustly r7 (verse eindkeurder, 16 nov)

**Oordeel: FAIL (klein): 6 pixels.** Na deze reparaties PASS; een nieuwe volledige keuring is niet nodig, een pixeldiff (alleen deze 6 pixels gewijzigd) volstaat.

Getoetst: `dustly_r7.png` op 1×, 2×, 8× (licht en donker) naast `gemini/r6_a.png`, de kale reductie (`basis/kaal_64.png`, 11 px omhoog) en Gastly Gen 3. Bewust gevraagde afwijkingen (palet A, minder zwart, kleurrijker, Gastly-belijning/toonstappen, fellere lichtrand, Gastly-tandvorm, kale mondlijn) niet aangerekend.

## Eis 1: trouw aan het model
- Silhouet: alpha-diff **0** met de kale reductie (offset 9,8). Wolkjes rechtsboven, slierten en gaten onderaan op hun modelplek.
- Gezicht: beide ogen pixel voor pixel gelijk aan de modelreductie (ver oog: wit met pupil, rij 27–31; nabij oog: groot wit, pupil (21,30)). Mondlijn volgt de reductie. Tanden op de modelplek.
- Bulten: ronde bult rechts met ring, bultlijn rechtsboven (tonaal), kinlijn links-onder: aanwezig.
- Afwijking: vier restanten van de oude gas-buitenlijn (r2–r5) staan nog als kerntint 3 (L71) midden in licht gas waar het model licht is (gemeten modelblok 148–157). Zie reparaties 1–5.

## Eis 2: Gen 3
- 10 kleuren + transparant. Tonen kern/gas 71 → 113 → 160 → 187 (stappen 42/47/27), lijnen 48 en 26: Gastly-achtig, contrastrijk. **Niet blurry meer**: grote vlakke zones, geen ruis in het gas.
- Lijn alleen om de kern (links-onder pruim-zwart, linksboven rode selout + oranje lichtrand erachter, nooit oranje op de buitenrand). Gas zonder buitenlijn zoals Gastly.
- Leest op 1× en 2× (licht én donker) als wolk met boos gezicht; lichtrand linksboven, schaduw rechtsonder in de kern.
- Kleine clusters < 3 px: alleen lijnstukken (8-verbonden), rand-glans en oog/tand: toegestaan. Uitzondering: de losse donkere spikkels hieronder.

## Reparaties
1. **(38,12): idx3 → idx5.** Donkere spikkel in de tonale bultlijn rechtsboven (lijn = 4,4,4,4,**3**): restant oude buitenlijn; model 157, buren 5/6.
2. **(43,13): idx3 → idx5.** Losse donkere pixel naast de lichte bult rechtsboven; model 157, buren 5/6.
3. **(44,12): idx3 → idx5.** Donkere pixel op de gasrand (gas heeft geen buitenlijn); model licht, buur onder 5.
4. **(46,40): idx3 → idx5.** Donker streepje in de lichte gasrand rechtsonder; model 149, buren 5.
5. **(47,40): idx3 → idx5.** Idem, model 148, aan de gasrand (geen lijn).
6. **(13,34): idx2 → idx1.** Begin van de mondlijn loopt 1,**2**,1,3,1 (zwart/donker om en om op één lijn); in het model heeft (13,34) dezelfde toon als (12,34) (= idx1). Mondvorm verandert niet.

Niet aanraken: (38,11) en de diagonaal (34,15)–(37,12) (tonale bultlijn uit het model), (22,34) (tandvlees boven de Gastly-tand), de onomlijnde gasrand links-onder in idx4 (modelschaduw), de gebroken oranje lichtrand (gekozen in r6b/r7).

Ter info voor Jordi (geen eis): de lichtrand is rood-buiten/oranje-binnen parallel aan de rand; dat is een gekozen rimlight, geen banding-fout.
