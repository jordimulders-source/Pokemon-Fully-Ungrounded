# Nachtaap fase 1, ronde 5: lijf van ronde 4, ogen in de stijl van ronde 2/3

Opdracht van Jordi: het lichaam van ronde 4 houden en de ogen van ronde 2/3 terugzetten (die vond hij "geinig"). Hij moet mysterieus overkomen, maar niet verveeld of slaperig. De ogen van ronde 4 waren "helemaal verknald".

Bestanden:
- `anim_front.png` (64×128, 2 frames, geïndexeerd, index 0 transparant)
- `normal.pal`: ongewijzigd ten opzichte van ronde 4
- `compare.png`: ronde 3, 4 en 5 naast Abra, Ralts, Natu, Aipom, de Hoenn-starters, Spoink, Meditite, Wynaut en Espurr, op 3× en 1×, met de silhouettest
- `bron/build.py` maakt de sprite uit ronde 4 plus de oograsters. `bron/compose.py` maakt het vergelijkingsvel.

## Wat ik deed
- **Lijf, kop, masker, staart, parel en frame-2-arm** zijn pixel voor pixel ronde 4. Alleen het gezicht (rij 23–30) is opnieuw gezet.
- **Ogen met de hand per pixel**, als in ronde 3 frame 1: grote, donkere nachtogen in nachtblauw (13) met een zwarte rand en zonder pupil, zodat je niet ziet waar hij kijkt.
  - Linksboven zit een **maansikkel** als weerspiegeling: 1 glanspixel (14) en een sikkel van 4 px (11) langs de rand.
  - Rechtsonder zit een **nachtgloed** (12) met een lichte kern (11), zoals het oplichten van nachtdierogen. Die gloed maakt de blik mysterieus. Zonder gloed las hij als "schattige knopogen".
  - **Geen oogleden**, want de halve leden van ronde 2 en 4 lazen slaperig of verveeld. De bovenrand is aan de buitenhoek 2 px dik: een licht schuine lidlijn die het oog amandelvormig maakt zonder het af te sluiten.
- **3/4-aanzicht in de ogen:** het nabije oog is 8 px breed, het verre oog 7 px en staat in de schaduwkant. De neusbrug is 4 px, met de middenstreep van het masker erin. De zijstreep van het masker langs het verre oog is terug (in ronde 4 liep die door het oog).
- **Frame 2:** precies dezelfde ogen, 1 px hoger (de kop komt omhoog). Er is geen ander karakter in frame 2, zoals de keuring vroeg.
- Ik heb drie varianten bekeken: A met een brede neusbrug, B met een smallere brug en dikkere buitenhoeken, en C (gekozen), dat B is met een sterkere nachtgloed.

## check.py (`--stage 1`)
Er is geen FOUT. De cijfers zijn vrijwel gelijk aan ronde 4: 14 kleuren, binnenlijnen zwart 0,072, verschil frame 1-2 0,285. De bekende LET OP blijft: de rand linksboven is 0,21 door de donkere lijn aan de lichtkant (index 4), en er is geen back of icoon.

## Palet (ongewijzigd)
`'nachtaap': {'vacht': [1, 2, 3, 4], 'zilver': [5, 6, 7], 'roze': [8, 9, 10], 'maan': [11, 12, 13], 'wit': [14]}`. Ogen en parel delen de groep "maan", zodat ze in elke variant samen meekleuren.

## Wat ik zelf nog zwak vind
- De ogen zijn groot en glanzend. Dat sluit aan bij wat Jordi geinig vond, maar het blijft iets meer "anime" dan de eenvoudige Gen 3-ogen van Torchic of Mudkip (de keuring van ronde 3 noemde dat). Het mysterie zit nu vooral in de gloed. Wordt het te lief, dan kan de gloed 1 px groter en de sikkel 1 px kleiner.
- De kopvorm zelf is nog steeds rond en symmetrisch (punt uit ronde 4); alleen het gezicht is gedraaid.
- De spiraal raakt de kop nog, en de rand linksboven blijft aan de donkere kant.
- Er is nog geen back, icoon of proefvariant (albino/zwart: kijk dan of de sikkel en de gloed blijven lezen).
