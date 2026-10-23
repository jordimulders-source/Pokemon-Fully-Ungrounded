# Nachtaap ronde 8: van nul af aan

Schone lei: geen eerdere nachtaap-sprites of -modeltekeningen bekeken. Vertrekpunt: het concept in woorden (aap met grote ogen, genezer, Nazca-spiraalstaart), de gidsen (SPRITING.md, Dragonfly Cave-gids, FAKEMON_DESIGN.md), het referentieplaatje, Cuyby ronde 3 als niveau, en echte Gen 3-sprites (Jigglypuff, Aipom, Espeon, Abra, Natu, Smoochum; Espurr/Scream Tail alleen voor het oogidee).

## Bestanden
- `anim_front.png`: 64×128, 2 frames, geïndexeerd, 13 kleuren (index 0 transparant).
- `normal.pal`: JASC-palet (16 plaatsen, 13 gebruikt).
- `schetsen.png`: drie ruwe poses (A zittend, B op vier poten, C staand met open hand) en drie oogvarianten (1 amber iris + grote pupil, 2 Jigglypuff-achtig donkerpaars, 3 Espurr-achtige amber ring).
- `compare.png`: naast Jigglypuff, Aipom, Espeon, Abra en Smoochum, op 1× en 3×, met metingen.
- `bron/sprite.py`: de sprite zelf, per lichaamsdeel (kop, staart, lijf) als met de hand ingevuld tekstraster. `bron/frame1.txt`: frame 1 als tekst. `bron/schetsen.py`, `bron/compare.py`.

## Keuzes
- **Pose A** (zittend, handen samen onder de kin) en **oog 1**. Pose A laat de spiraal vrij boven de rug staan (silhouet zoals Aipoms staarthand), en de handen samen zijn het zorgzame gebaar van de genezer. Oog 1 leest het sterkst als nachtdier (grote pupil, amber iris); oog 2 was te donker en oog 3 te starend.
- **De ogen dragen het gezicht.** Twee grote amberogen (dichtbij 10×11, ver 8×11 voor de 3/4-hoek) die bijna tegen elkaar staan, zoals bij Jigglypuff. Per oog: donkere amber bovenin (schaduw van de wenkbrauw), lichte amber onderin als gekleurde reflectie, ronde zwarte pupil, witte glans van 2×2 linksboven. Strak en per oog symmetrisch, zoals het referentieplaatje.
- **Nachtaap-kenmerken, vereenvoudigd:** ronde gezichtsschijf, crème halvemaanvlekken boven de ogen, donkere streep over het voorhoofd tussen de ogen, kleine crème snuit, slanke armen, lichte borst en buik, lange staart. Geen oren (die vallen bij nachtapen weg in de vacht) en geen neus.
- **Spiraalstaart:** een lint dat rechts omhoog loopt, over de top, onderlangs en in het midden omhoog krult tot een ronde punt, met een open spleet. De Nazca-aap heeft zelf een spiraalstaart; meer is niet nodig. Les uit de schets: een amberkleurige punt leest als een derde oog, dus de staart blijft violet. De steel loopt schuin achter de rug langs (vast aan het lijf).
- **Genezer, subtiel:** handen samen onder de kin, met een amber lichtje in de naad tussen de handpalmen (dezelfde amber als de ogen). In frame 2 gloeit het een pixel hoger op.
- **Kleuren (3 hoofdkleuren):** violet (Psychic), crème (gezicht, borst), amber (ogen, het lichtje). Violet in 4 tinten (hooglicht, basis, schaduw, omlijningsbasis), crème en amber elk 3, bijna-zwart, wit.
- **Frame 2:** kop zakt 1 px (ademhaling), spiraal veert 1 px op, lichtje gloeit.

## Checklist SPRITING.md
- [x] Alles met de hand, per lichaamsdeel (kop, staart, lijf apart); geen vormfuncties of automatische schaduw/omlijning. De rasters staan in run-length-vorm of als `x:pixels`, maar elke pixel is gekozen.
- [x] Curven zonder hoekjes: segmentlengtes lopen geleidelijk op of af (kop 4-3-2-1-1-1, dan verticaal), neutrale pixel tussen horizontaal en verticaal.
- [x] Niets gespiegeld: de kop is aan de achterkant voller, het verre oog smaller, armen en benen zijn ongelijk.
- [x] 3/4-pose naar links, licht linksboven: hooglicht linksboven op kop, staart, arm en knie; schaduw rechts en onder; slagschaduw van de kop op de borst.
- [x] Omlijning per kleurgroep: omlijningsbasis (O) en schaduwviolet als lichte omlijning op de belichte bovenkant/links, bijna-zwart (K) aan de schaduwkant. Zwart-aandeel in de buitenrand **0,50** (Gen 3 op het vel: 0,26–0,56).
- [x] Anti-aliasing alleen binnen de lijn; 1 px brede omlijning.
- [x] Ogen: witte glans linksboven en een lichte amber reflectie rechtsonder.
- [x] 64×64, anim_front 64×128 met subtiel tweede frame, ≤ 16 kleuren, index 0 transparant.
- [~] Oppervlak **994 px**: iets boven het doel van 750–900 (Jigglypuff 747, Aipom 856, Abra 906, Espeon 1101). De kop is bewust groot (babyverhoudingen); de staartsteel kost ±70 px.

## Eigen oordeel
- Sterk: de ogen en de kop. Op 1× lees je meteen "grote ogen, aapje", en de crème vlekken en de streep maken er een nachtaap van. Het silhouet (ronde kop plus spiraal) is herkenbaar.
- Zwakker: de onderarmen en handen zijn op 1× klein en vallen een beetje weg; een donkere lijn onder de armen deelt het lijf horizontaal. De rechte schuine staartsteel is wat stijf. Het lichtje tussen de handen is zo subtiel dat je het op 1× nauwelijks ziet (bewust, maar misschien te weinig om "genezer" te lezen).
- Mogelijke volgende stap: steel licht laten buigen, handen een tikje groter, of het lichtje 2 px maken.
