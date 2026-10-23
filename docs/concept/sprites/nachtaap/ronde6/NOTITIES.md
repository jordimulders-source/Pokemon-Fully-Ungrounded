# Nachtaap fase 1, ronde 6 (pixelronde volgens de nieuwe werkwijze)

Modeltekening: **concept B** (`docs/concept/ontwerp/nachtaap/concept_B.png`), door Jordi gekozen. De tekening is niet veranderd.

## Werkwijze
- **Skelet:** Aipom (kop, gezicht, dunne arm met grote hand) en Abra (zithouding, grootte). Formaat en verhoudingen van de modeltekening: bolkop ±56% van de hoogte, klein lijf, tarsierhurk.
- **Palet:** de paarse ramp van `aipom/normal_gba.pal` (213,131,255 / 180,98,230 / 139,57,180 / 82,32,106) met alleen de tint iets naar blauw gedraaid (`rot(..., DH=-0.035)` in `bron/nachtaap.py`), afgerond op GBA-waarden. Eigen indexen per onderdeel: violet (4 tinten), indigo rand, lila gezicht (2), iris (cyaan, gloed, donker), pupil, roze (2), wit, omlijning. 15 van de 16 kleuren in gebruik, index 0 transparant.
- **Pixels met de hand:** elk onderdeel staat als ASCII-raster in `bron/nachtaap.py` (kop, ogen, oren, romp, benen, voeten, arm, hand, spiraal, staart) plus een lijst losse handcorrecties (vachtaccenten, kniehooglichten, gekleurde omlijning aan de lichtkant op met de hand gekozen punten). Geen automatische schaduw of selout.
- **Frame 2:** de geheven hand en de spiraalstaart gaan 1 px omhoog en de ogen gloeien op (de onderste irisrijen lichten op). Subtiel, zoals de Gen 3-animaties.

## Wat er in zit (trouw aan concept B)
Dieper violet met een indigo rand rond een bleke lila gezichtsschijf; korte donkere wig tussen de 'wenkbrauwen'; grote, egaal cyaan gloeiende ogen met één glanspixel en een zwaarder bovenooglid; rond oortje met roze binnenkant; één hand geheven bij de wang, de andere op de knie; dunne ledematen, hoge knieën, voeten met roze kussentjes; Nazca-spiraalstaart. Geen borststeen of andere spullen.

Risico uit de ontwerpronde (armen als tekenfilm): de onderarm is kort en recht omhoog met een grote hand (Aipom), de bovenarm loopt schuin naar de schouder; de elleboog rust op de knie.

## Metingen (keuring_ronde5/scripts/metrics.py, frame 1)
| | oppervlak | b×h | donkere buitenrand | detail | losse pixels / opp. | verzadiging |
|---|---|---|---|---|---|---|
| ronde 6 | 999 | 43×37 | 0,93 | 2,0 | 0,14 | 0,53 |
| ronde 5 | 1230 | 47×42 | 0,54 | 1,7 | 0,10 | 0,34 |
| Aipom | 856 | 32×56 | 0,60 | 2,0 | 0,19 | 0,48 |
| Abra | 906 | 42×40 | 0,56 | 1,93 | 0,18 | 0,72 |

Het oppervlak (999) zit net boven de streefwaarde (±800–950; Treecko 967). De grote bolkop uit het concept kost dat; kleiner maken kan door de kop 1–2 px smaller te tekenen. De buitenrand is nog vrijwel overal donker (de omlijning is nu donkerviolet in plaats van zwart, maar de meting telt die nog als donker).

## Blinde test
`blindtest.png`: de sprite tussen twaalf echte Gen 3-sprites (Treecko, Torchic, Mudkip, Aipom, Abra, Natu, Ralts, Meditite, Spoink, Smoochum, Teddiursa, Skitty). De kandidaat staat op **plek 8**.

**Nog niet onafhankelijk uitgevoerd.** In deze subagent-sessie was geen Agent-tool beschikbaar om een frisse agent zonder context te starten. De hoofdsessie moet de test nog draaien. Gebruik daarvoor alleen `blindtest.png` en de vraag "welke hoort er niet bij en waarom".

Eigen inschatting (niet blind, want ik heb hem zelf getekend): waarschijnlijk wordt hij gevonden. Wat hem verraadt:
1. De pose is frontaal en symmetrisch. Bijna alle Gen 3-sprites staan in 3/4.
2. De omlijning is overal even dik en donker. Gen 3 wisselt dat af met gekleurde lijnen.
3. De vlakken zijn egaal (vooral de gezichtsschijf), met minder losse accentpixels dan Aipom of Abra.
4. De ogen lezen nog wat als een bril door hun dikke zwarte kaders.

Op 1× valt hij minder op dan ronde 5: hij is kleiner, verzadigder en heeft twee duidelijke kleurzones.

## Volgende stap (één laag tegelijk)
Als de blinde test hem aanwijst, volgt eerst een **lijnen- en schaduwronde** (silhouet en vlakken blijven staan): meer gekleurde omlijning, schaduwclusters op de gezichtsschijf en de kop, en dunnere ooglijnen aan de zijkant. Een 3/4-draai is een silhouetkeuze voor Jordi.

Bestanden: `anim_front.png` (64×128, 2 frames), `normal.pal`, `compare.png`, `blindtest.png`, `bron/` (`nachtaap.py` tekent, `vellen.py` maakt de vellen voor beide soorten, `lib.py`). Draaien vanuit de repo-root: `python3 docs/concept/sprites/nachtaap/ronde6/bron/nachtaap.py docs/concept/sprites/nachtaap/ronde6`.
