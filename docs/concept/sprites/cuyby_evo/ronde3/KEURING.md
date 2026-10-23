# Keuring Cuyby-evolutie ronde 3 (onafhankelijk, 23 okt)

Jordi over ronde 3: "Ziet er goed uit." Kleuren, schaduw, kruinsprieten, pose en vacht zijn goedgekeurd. Deze keuring zoekt dus alleen naar fouten tegen de Dragonfly Cave-regels en §0 van `docs/lessen/SPRITING.md`, niet naar een ander ontwerp.

**Vellen** (`keuring/`):
- `vel_3x.png`: ronde 3 (beide frames) en Cuyby naast 14 echte Gen 3-sprites, op 3× en op 1× (licht en donker).
- `vel_1x.png`: alleen 1×.

**Bronnen:**
- De echte Gen 3-sprites komen uit de git-geschiedenis (`keuring/haal_gen3.py`, commit 358c0d0699). In de huidige `graphics/pokemon/` staan de nieuwere expansion-sprites, en die hebben andere maten.
- De metingen komen uit `keuring/keuring.py`.

Alle coördinaten zijn die van het raster (`bron/raster_f1.txt`, na het knippen).

## Metingen (frame 1)
'Zwart lichtkant' is het aandeel zwart in de randpixels waarvan alleen de linker- of bovenbuur leeg is. 'Zwart schaduwkant' is hetzelfde voor alleen de rechter- of onderbuur.

| sprite | oppervlak | b×h | zwart rand | zwart lichtkant | zwart schaduwkant | kleuren |
|---|---|---|---|---|---|---|
| **evo ronde 3** | 1399 | 49×44 | 0,49 | 0,14 | 0,77 | 15 |
| Cuyby ronde 3 | 789 | 31×32 | 0,53 | 0,51 | 0,49 | 15 |
| Mareep | 893 | 38×33 | 0,49 | 0,12 | 0,84 | 15 |
| Swinub | 482 | 26×22 | 0,37 | 0,00 | 0,72 | 10 |
| Piloswine | 1515 | 42×48 | 0,43 | 0,00 | 0,79 | 13 |
| Linoone | 1357 | 51×60 | 0,56 | 0,41 | 0,62 | 11 |
| Furret | 1191 | 41×50 | 0,43 | 0,10 | 0,76 | 13 |
| Teddiursa | 652 | 28×36 | 0,37 | 0,02 | 0,83 | 13 |
| Ninetales | 2022 | 59×57 | 0,45 | 0,24 | 0,72 | 8 |
| Vulpix | 1119 | 48×40 | 0,45 | 0,05 | 0,85 | 15 |
| Eevee | 748 | 33×44 | 0,41 | 0,08 | 0,78 | 10 |
| Skitty | 934 | 41×40 | 0,38 | 0,09 | 0,66 | 11 |
| Zigzagoon | 1315 | 56×36 | 0,32 | 0,02 | 0,64 | 12 |
| Whismur | 884 | 38×37 | 0,53 | 0,17 | 0,85 | 12 |
| Swablu | 920 | 56×36 | 0,13 | 0,03 | 0,29 | 12 |
| Mawile | 1460 | 55×47 | 0,58 | 0,30 | 0,77 | 14 |

## Wat in orde is
| punt | oordeel | maatstaf |
|---|---|---|
| Omlijning per kleurgroep | **Ok.** Op de lichtkant is 0,14 van de rand zwart, op de schaduwkant 0,77. Dat is precies het Gen 3-patroon: lichtkant 0,00–0,24 (Linoone 0,41 is de uitzondering), schaduwkant 0,62–0,85. Belichte randen hebben r, het wit e, het roze P. | Gids §8; Piloswine, Vulpix, Eevee |
| Licht en schaduw | **Ok.** Het licht komt van linksboven (h links, q rechts), de verre flank is een schaduwband en de evenaar volgt de ronding. De grens tussen de tinten is gekarteld, met streepjes in de haarrichting. | Gids "fur"; Piloswine, Zigzagoon |
| Rechte lijnen | **Ok.** `bouw9` vindt geen randstuk van meer dan 4 px. | §0.3 |
| Kleurgebruik | **Ok.** 15 kleuren, met een stro-ramp van 4 tinten plus omlijning. Mareep en Vulpix zitten ook op 15. Er is geen overshading. | Gids §4 |
| Formaat | **Ok.** 1399 px valt tussen Linoone (1357) en Piloswine (1515), dus op het niveau van een middenevolutie. Ten opzichte van Cuyby is dat ×1,77 (Swinub → Piloswine ×3,1, Zigzagoon → Linoone ×1,03). | §0.6 |
| Pose en diepte | **Ok.** De sprite staat in 3/4: de rug daalt, de zoom stijgt en de verre pootjes staan links en hoger. Dat is hetzelfde skelet als Mareep. | §0.1, §0.7 |
| Familie | **Ok.** De zwarte vlek met het oog, het zwarte oortje met één roze pixel, de witte snuit met het roze neusje, de roze voetjes en de stro-/roesttinten komen van Cuyby. Jordi: "is ook duidelijk een Cuyby-evolutie." | Cuyby ronde 3 |
| Leesbaarheid 1× | **Ok.** Op licht en op donker leest de sprite als een harig dier met het gezicht linksvoor (vergelijkbaar met Piloswine en Swinub). De kruin geeft een onrustig maar herkenbaar silhouet. | §0.5 |

## Bevindingen: nodig
| # | bevinding | regel / voorbeeld | pixels | oplossing |
|---|---|---|---|---|
| N1 | **Open randen in frame 1.** De notities zeiden "bouw9 meldt geen open randen", maar `bouw9` meldt er 19. (a) Bovenkanten van de kruinsprieten zonder omlijning: de linkerspriet en de middelste top hebben h/s/d direct tegen de lucht. (b) Bovenkant van de achterste spriet en een pixel van de pony. (c) Op de schaduwkant d/q/s zonder zwart: twee sprietjes rechtsboven, de onderkant van de lok die naar achteren uitsteekt en vier zoompunten. | Gids §8: omlijning altijd dicht en 1 px, anti-aliasing alleen binnen. Les §19: sprieten in r. Op 1× tegen een donkere achtergrond lekken de lichte pixels uit (vergelijk het vel). | (a) (20,13) (13,16) (15,17) (17,18) (19,19). (b) (34,18) (35,18) (36,18) (32,19) (11,25). (c) (47,25) (50,29) (52–54,42) (48,46) (44,47) (50,47) (38,49) | (a, b) r boven de blote pixel (x20y12, x13y15, x15y16, x17y17, x19y18, x32y18, x34–35y17, x11y24), en (36,18) wordt r. (c) K eronder of erboven (x47y24, x50y28, x54y42, x52–53y43, x48y47, x44y48, x50y48, x38y50). |
| N2 | **Open voet in frame 2.** Als de sprieten 1 px opzij wuiven, ligt de voet open. | Les §18: een stilstaand deel onder een bewegend deel moet zelf dicht zijn. | (15,20) en (31,20) in frame 2 | Een r op y19 (x15, x31) in het deel `kruin_voet`. In frame 1 ligt daar al een r van de spriet. |
| N3 | **Witte snuit plus bles te groot** (ook Jordi's punt 1). Het wit loopt als één wig van (23,32) naar (12,43): 11 rijen hoog en tot 10 px breed (x13–22), tegen een oog van 4×4. Op 1× is het de lichtste en grootste vlek, en dus het eerste wat je ziet ('snavel'). | Les §19: houd het wit bij een snuit en een kleine bles. Teddiursa, Piloswine en Swinub hebben een snuit van 5–7 px breed. | Bles x20–23, y28–36. Snuit x12–22, y36–43. | Bles onder de pony, snuit 2 px smaller (rechterrand x20) en de kin 1 rij hoger (ronde 4). |

## Bevindingen: polijsten
| # | bevinding | regel / voorbeeld | pixels | oplossing |
|---|---|---|---|---|
| P1 | **Zwarte scheidingen midden in de belichte pony.** Zwart binnen het licht leest op 1× als donkere krassen naast het gezicht. | Gids §8: zwart alleen aan de schaduwkant. Les §15: scheidingen bovenaan zacht, alleen bij de zoom zwart. | x12 y31–36, x15–17 y31–34, x19–21 y28–31 | r als scheiding en K alleen onder de punten. Meegenomen in ronde 4, omdat de pony toch opnieuw moest. |
| P2 | **Oog in een bijna-zwart vlak.** De pupil K (41,24,24) ligt in G (49,41,57). Het oog leest alleen door de g-ring en de glans. Op 1× is het een donkere stip met een lichtpuntje. | Gids §6: kraaloog met glans en reflectie (Eevee, Teddiursa). | Oog x25–28, y33–36 | Werkt, en Jordi is tevreden, dus niet veranderd. Optie voor later: de ring 1 tint lichter. |
| P3 | **Veel kleine tintwissels op de nabije flank.** Op 3× oogt dat rommelig, op 1× leest het als haar. | Gids "fur": "don't overdo this". | x30–50, y30–45 | Laten (Jordi: vacht goed). |
| P4 | **Frame 2 beweegt alleen de kruin (1 px).** Gen 3 beweegt vaak meer: Mareep veert met het hele lijf. | — | `kruin_punten` | Laten. Een idee voor later is dat de pony 1 px mee wuift. |

## Oordeel
Ronde 3 is een geslaagde sprite. Omlijning, licht, kleur, formaat, pose en familie zitten binnen de Gen 3-maten. Er zijn twee echte fouten: de open randen (N1, N2) en het te grote wit (N3, dat ook Jordi aanwees). Beide zijn op te lossen zonder het ontwerp te veranderen. Dat gebeurt in ronde 4.
