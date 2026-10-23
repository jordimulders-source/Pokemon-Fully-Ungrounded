# Cuyby-evolutie (fase 2), ronde 1: de wandelende hooiberg

Ontwerp: variant A, de **ichu-fontein** (`docs/concept/ontwerp/cuyby_evo/`). De sprite is een pixel-over van die modeltekening en staat helemaal als handgeschreven tekstraster in `bron/cuyby_evo.py`. Elk deel heeft eigen rijen (`(y, x, "pixels")`) en de delen worden van achter naar voor gelegd: achterste sprieten, lijf, zoom, pootjes, buitenste sprieten, kruin, strengen, gezicht. Er zijn geen vormfuncties gebruikt en geen automatische schaduw of omlijning.

## Opbouw
- **Kruin:** elf smalle sprieten van 1 tot 7 px breed die vanuit het gezicht waaieren. Vijf staan achter in de schaduwtint, zes vooraan in de basistint met een hooglichtstreep links. De buitenste twee hellen 45° naar buiten.
  - Elke spriet loopt recht met een vaste helling. Gras is stijf, en gelijke stapjes lezen als een rechte lijn.
  - Rechte, smalle sprieten lezen als gras. Brede, golvende plukken (de eerste opzet) lazen als vlammen of stekels.
- **Lijf:** een pol die naar boven breder wordt.
  - De vacht heeft strengen (s) in de richting van de waaier: links lopen ze van linksboven naar rechtsonder naar het gezicht toe.
  - De grens met het roest is gekarteld.
  - De onderkant is schaduw met donkere streepjes en eindigt in hangende grastipjes, niet in een rechte lijn.
- **Gezicht:** een kleine crème snuit laag in de pol, met een korte pony van één plukje.
  - De ogen zijn klein (2×3) met een witte glans linksboven en een rozebruine weerkaatsing rechtsonder. Daaronder een roze neusje en een mondje.
  - **Cuyby's herkenning:** het zwarte vlak om het linkeroog met een zwart hangoor ernaast, en het roestoranje hangoor rechts, over de wang. De oren hangen naast het gezicht zoals bij een cavia van voren. Ze verschillen in vorm en kleur, dus er is niets gespiegeld.
- **Pootjes:** twee korte roze voorpootjes en twee verre pootjes. De verre pootjes zijn kleiner, staan buiten de voorpootjes en hebben de schaduwtint (n).
- **Frame 2:** de sprieten wiegen in de wind. De bovenste rijen van de kruin (y ≤ 20) schuiven 1 px naar rechts en de rest blijft staan.

## Palet (16 kleuren, index 0 transparant)
- **Stro:** y/Y/s plus omlijningsbasis S (139,98,32). S dient ook als rand van de crème snuit.
- **Roest:** O/q plus omlijningsbasis Q. Dit is het oranje van Cuyby (238,156,74 / 205,115,41 / 148,57,0), zonder lichtere tint, zodat de punten niet als vlam oplichten.
- **Crème:** b/c (Cuyby's crème).
- **Zwart vlak:** g/G (Cuyby's zwart), met de omlijning K als schaduw.
- **Roze:** p en n. n is tegelijk de schaduw van de pootjes en de gekleurde weerkaatsing in de ogen.
- **Glans:** a.

## Checklist SPRITING.md
| Regel | Toegepast |
|---|---|
| 1. Geen vormgereedschap | Ja. De modeltekening is met vormen gemaakt, de sprite is pixel voor pixel als tekst geschreven. Twee correcties zijn als bewerking op het raster gedaan: de bovenste rijen van de sprieten kregen een lichtere rand (zie regel 8) en frame 2 is een verschuiving van de kruin. |
| 2. Per onderdeel | Elf sprieten, het lijf, de zoom, de pootjes, de strengen en het gezicht staan elk apart. Ze zijn na elke stap op 4× en 1× gerenderd. |
| 3. Curven, geen spiegelen | Het lijf heeft een oplopende en aflopende trap (1,1,1,1,1,1,2,3,4,…) zonder hoeken in de ronding. De onderrand is niet meer recht (eerst 28 px recht, nu grastipjes tussen de pootjes). Het zwarte vlak heeft een ronde bovenrand. De sprieten zijn bewust recht: het zijn stijve grashalmen. |
| 4. Palet 3 tinten + omlijning | Stro y/Y/s + S, roest O/q + Q (zonder hooglicht), crème b/c, zwart g/G + K. |
| 5. Licht linksboven | Hooglichtstreep (y) links in elke spriet en linksboven in het lijf. Het roest staat aan de schaduwkant, met q onderaan en rechts. De onderkant van de pol is schaduw. |
| 6. Ogen | Klein, met glans linksboven en een gekleurde weerkaatsing rechtsonder. Het linkeroog heeft een lichte rand (g) in het zwarte vlak, zoals bij Cuyby. |
| 7. Vacht gekarteld | Strengen in de haarrichting, een gekartelde grens tussen stro en roest, en schaduwstreepjes (S) onderaan. |
| 8. Omlijning per kleurgroep | De punten van de sprieten zijn van boven belicht, dus de rechterrand tot y = 18 is S of Q in plaats van K. Daaronder en aan de onderkant is de rand zwart. Overal 1 px. |
| 12. Ledematen en gezicht compleet | 2 oren, 2 ogen, neus, mond, 4 pootjes (2 ver). Alles sluit aan op een doorlopende omlijning. |

## Meting (frame 1; `bron/vel.py`)
| | oppervlak | b×h | donkere buitenrand | waarvan zwart |
|---|---|---|---|---|
| **evolutie** | **1377** | 48×44 | 0,56 | **0,51** |
| Cuyby ronde 3 | 789 | 31×32 | 0,85 | 0,53 |
| Piloswine | 1515 | 42×48 | 0,86 | 0,43 |
| Tangela | 1358 | 46×49 | 0,81 | 0,32 |
| Mareep | 893 | 38×33 | 0,83 | 0,49 |

'Donker' betekent hier luminantie onder 100 en 'zwart' een kanaal-max onder 48. Dat is een andere maat dan in de Cuyby-notities, maar 'waarvan zwart' komt voor Cuyby op hetzelfde getal uit (0,53).
- Het oppervlak is 1,75 × dat van Cuyby, net onder Piloswine.
- Het zwart-aandeel lag eerst op 0,63. Door de belichte sprietpunten in omlijningsbasis te zetten is het nu 0,51, binnen de 0,35–0,6.

## Eigen oordeel
- **Goed:**
  - Op 1× leest het als een pol strogras met een cavia erin. Het zwart om het oog met het zwarte oor en het oranje aan de rechterkant maken direct duidelijk dat dit Cuyby is.
  - Het silhouet (een waaier van halmen) verschilt van Piloswine (een hangende koepel) en van Tangela (krullen).
  - De ogen zijn klein en het gezicht verdwijnt half, zoals gevraagd.
- **Zwak / volgende ronde:**
  - De rechterkant (roest) is een groot vlak met weinig textuur. Daar kunnen een paar strengen (q) bij, in de richting van de waaier.
  - De twee roestsprieten rechts kunnen nog als vlam lezen. Dat moet een blinde test uitwijzen. Zo ja: het roest alleen aan de flank houden en de sprieten daar ook stro maken.
  - De snuit is vrij breed en vlak. Een iets smallere, rondere snuit zou meer 'cavia' zijn.
  - Frame 2 is subtiel (1 px). Of dat in het spel genoeg wiegt, blijkt pas in de emulator.
- **Niet gedaan:** een blinde test (geen budget in deze ronde), de shiny, de achterkant en het icoon.

## Bestanden
- `anim_front.png` (64×128, 2 frames), `normal.pal`, `compare.png` (Cuyby ronde 3, evolutie f1/f2, Piloswine, Tangela, Mareep op 3× en 1×)
- `bron/cuyby_evo.py`: het raster en het palet. Draaien vanuit de repo-root: `python3 docs/concept/sprites/cuyby_evo/ronde1/bron/cuyby_evo.py docs/concept/sprites/cuyby_evo/ronde1`. Het gebruikt `lib.py` uit `nachtaap/ronde7/bron/`.
- `bron/vel.py`: maakt het vergelijkingsvel, de eindrasters `bron/raster_f1.txt`/`raster_f2.txt` en de meting.
