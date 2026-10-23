# Nachtaap fase 1: ontwerpronde (geen sprite)

Modeltekeningen in vlakke kleuren met een donkere omlijning, opgebouwd uit bollen, peren en buizen (256×256, 3/4-pose). Na de keuring van ronde 5 (`../../sprites/KEURING_RONDE5.md`) blijft het lijfconcept van ronde 3–5 staan: een grote bolkop met tarsierogen, het nachtaapmasker, een klein lijf en een krulstaart (in fase 1 een krulletje; de volle Nazca-spiraal komt in de eindvorm). Wat in alle drie is opgelost:

- **Licht gezicht in een donkere vacht** in plaats van eenkleurig pastel.
- **Egaal gloeiende ogen**: één irisvlak, een kleine pupil, één glanspunt en een zwaarder bovenooglid. Ze kijken mysterieus, niet verveeld. De vorm is die van ronde 2/3: groot en rond.
- **Geen borststeen** en geen andere spullen. Het type zit in de ogen, de gezichtsschijf en de staart.
- **Tarsierhouding** in plaats van een sumohurk: dunne ledematen, hoge knieën tegen het lijf en grote vinger- en teenkussens.
- **Korte wig tussen de wenkbrauwen** in plaats van een streep over de hele schedel (geen helmnaad). De zijstrepen zijn een smalle donkere rand langs de schijf.

| | concept | in één zin |
|---|---|---|
| A | **Nachtaap naar de natuur** (`concept_A.png`) | De kleuren van de echte *Aotus*: grijsbruin-violet met een bleke schijf, een oranje keel en buik en een zwarte staartpunt. Roze gloed, handen onder de kin, wangplukken. |
| B | **Lavendel, maar dieper** (`concept_B.png`) | De goedgekeurde paarse richting, maar verzadigd violet met een indigo rand om een bleke lila schijf. Cyaan gloed, rond oortje, één hand geheven. |
| C | **Twee maansikkels** (`concept_C.png`) | Nachtblauw. De witte wenkbrauwvlekken van de nachtaap zijn twee maansikkels (de maan uit de anatomie). Donker masker, lila gloed, staart hoog met een zilveren punt. |

`vergelijking.png` zet de concepten, verkleind tot spriteformaat (±900–1000 px oppervlak, zoals de keuring vraagt), naast Abra, Aipom, Ralts, Natu en Spoink (Gen 3), op 2× en 1×, met de silhouetten op 1× en een blinde rij.

## Eigen keuring (criteria uit KEURING_RONDE5)
- **Type uit de anatomie, niet uit spullen:** ja, in alle drie. Geen sieraad, kledingstuk of los symbool. De maan in C is een vachttekening.
- **Twee kleurzones en verzadiging:** A en C duidelijk (donkere vacht, bleke schijf, één fel accent). B is het zwakst: het lichte lila schuift weer richting 'knuffel'.
- **Silhouet:** bolkop + krulstaart blijft op 1× het herkenbaarst van alle starters. A krijgt extra randjes door de wangplukken, C door de hoge staart. De drie lijken in silhouet op elkaar; dat is logisch, want het lijfconcept stond vast.
- **Risico's:** C kan door het donkere masker om de ogen richting Dark gaan lezen. Bij alle drie zijn de armen nog wat 'rubberslang' (een tekenfilmaap). In de pixelronde moeten de onderarmen korter en de handen groter, zoals bij Aipom.
- Geen van de drie leest als 'dier met kostuum'. Een eerdere versie van C had een sikkel als hoorns boven de kop; die las als helm en is vervangen door de twee sikkelvormige wenkbrauwen.

## Voorkeur: A
A lost de kern van de keuring het best op: het is het enige concept waarin de echte nachtaap zelf het ontwerp draagt (bleke schijf, oranje keel, zwarte staartpunt). Daardoor leest hij 'mysterieus' in plaats van 'knuffel', zonder één spul. Roze gloed op een crème schijf is Psychic zonder Dark-signalen. De handen onder de kin geven een karakterpose ('ziet iets wat jij niet ziet'). B is de veilige terugval als Jordi het lavendel wil houden. De maansikkels van C kunnen ook op A (witte wenkbrauwvlekken in sikkelvorm). Dat zou de combinatie zijn die ik zou proberen als Jordi tussen A en C twijfelt.

Daarna (volgens de keuring): de gekozen tekening ligt vast als modeltekening, Aipom is het skelet voor kop en gezicht, het palet volgt de rampopbouw van `aipom/normal_gba.pal`, en de schaduw wordt met de hand gezet.

Scripts: `../scripts/` (`nachtaap.py` tekent, `sheets.py` maakt de vellen; draaien met `python3 docs/concept/ontwerp/scripts/sheets.py .` vanuit de repo-root).
