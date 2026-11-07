# Evo van Picapau: pose-proef r6pose (eerst de pose, dan pas de sprite)

## Jordi letterlijk (over sprite r4)
**"dit is geen driekwart aanzicht, laten we daar mee beginnen. Zijn mond is gewoon een rode wolk, de kuif staat teveel rechtop, die mag meer naar beneden buigen. Maar het begint met het driekwart aanzicht wat niet klopt en de hele sprite mag wat meer achterover leunen zoals raichu in gen 1"**

## Bestanden
- `picapau_evo_r6pose.py`: kopie van r5 (r5 en r6 zijn niet aangepast). Alleen de oren zijn veranderd: de punt wijst nu naar achteren-opzij en iets omlaag in plaats van rechtop, en de spiraal hangt eronder.
- `maak_pose.py`: de varianten P1–P3, snel gerenderd met `STAP=0.5`, elk passend in 61 px. Draaien: `STAP=0.5 python3.11 maak_pose.py`.
- `vel_pose.png`: P1–P3 op 1×, 4× en als render, naast Taillow, Staraptor, Swellow en Raichu Gen 1 op dezelfde schaal (1× en 4×).

## Wat er aan de pose veranderd is (tegen r5: lijf 35, kop +5, voorover 0)
- **Lijfdraai** naar de kijker: 45–55° (r5: 35°).
  - Borst en buik zie je nu grotendeels van voren.
  - De poten staan naast elkaar in perspectief, met de verre poot hoger en verder naar achteren.
  - De nabije vleugel staat rechts vóór de rug, de verre vleugel piept achter kop en rug uit.
- **Kop** 3/4, met 5–10° extra draai bovenop het lijf.
  - Het oog staat dicht bij de snavelbasis: oog_az 42–48 (r5: 65). Dat is de oplossing voor "het oog helemaal aan de zijkant", zonder de kop in profiel te zetten.
- **Achterover** (vervangt de Talonflame-diagonaal): de romp kantelt 15–30° om de heup naar achteren, zodat borst en buik omhoog en naar voren komen.
  - De kop krijgt een tegenkanteling (kop_kantel ±0,8 × de achteroverhoek), zodat hij rechtop blijft en de snavel niet omhoog wijst.
- **Eerste proef:** lijf 60° met kop +10 (70° totaal) gaf een kop recht van voren met een verkorte snavel. Dat was te ver, dus de varianten liggen lager.

| variant | lijf | kop extra | achterover | oog_az |
|---|---|---|---|---|
| P1 | 45 | +10 | 15 | 48 |
| **P2 (gekozen)** | 50 | +8 | 22 | 45 |
| P3 | 55 | +5 | 30 | 42 |

## Keuze: P2
- **Echt 3/4.** De borst en buik staan naar de kijker, net als bij Taillow en Swellow.
- **Snavel nog lang.** De snavel wijst duidelijk naar links en is lang genoeg om open te lezen. In P3 wordt hij korter en staat de kop bijna van voren.
- **Oog op de goede plek.** Het oog zit vlak boven en achter de snavelbasis, zoals bij Taillow en Staraptor.
- **Achterover genoeg.** De houding helt duidelijk naar achteren, met de kop boven de bolle borst, maar het blijft een vogel.
  - P3 lijkt qua leunen meer op Raichu, maar daar draait de bliksem bijna op zijn kant en wordt de nabije vleugel smaller.
  - P1 leunt te weinig, en daar vallen de oren achter de kop weg.
- **Oren.** De oren buigen naar achteren-opzij met de spiraal aan de punt, niet meer rechtop. De verre vleugel is achter de kop te zien.

## Zwakke punten (voor de sprite)
1. **Bliksem.** Door het achteroverkantelen staat het vlak van de bliksem schuiner. In P2 is hij smaller dan in r5. In de sprite teken ik hem weer breed en vlak naar de kijker (zoals in r3/r4).
2. **Mond.** Die is in de render een donker gat. In de sprite komen er een duidelijke boven- en ondersnavel en een donkere mond, met rood hooguit als kleine tong ("rode wolk").
3. **Oren op 1×.** Ze zijn dun. De spiraal moet in de sprite met de hand leesbaar worden gemaakt, zoals in r3 (1 px-spiraal met gat).
4. **Staartlus.** De lus hangt nu onder het lijf naar beneden en loopt minder om het lijf heen dan bij Raichu Gen 1.

Er is niets gecommit.
