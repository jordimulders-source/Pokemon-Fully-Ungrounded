# Keuring stap 4, hoofd ronde 5 (6 nov)

Bron: `vel_hoofd.png`, `hoofd_1.png`, `hoofd_2.png`. Referenties: `referenties/hitmontop_anime.webp` (op het vel) en `graphics/pokemon/hitmontop/anim_front.png` (spritekop op het vel). Bekeken op 8× (PIL nearest) en op 1× (het vel), plus een pixeldump van beide PNG's. Coördinaten hieronder zijn binnen de bbox (hoofd_1: x0 = 3, y0 = 21; hoofd_2: x0 = 1, y0 = 23), met kolom eerst en dan rij in absolute y.

## Per eis
| eis | optie 1 | optie 2 |
|---|---|---|
| Kop, haar en punt hetzelfde materiaal en dezelfde kleur, geen streep ertussen | ja | ja |
| Geen kippenpoot (geen vertakte lijnen) | ja | ja (twee D-pixels in de knot, (3–4,30) en (4,29), vormen een kleine plooi maar vertakken niet) |
| Enige streep hoog, als een fade | half: hij staat hoger dan in ronde 4 en de tint loopt uit (D, dan E, dan D). Maar hij is één schuine lijn van linksonder (3,33) naar rechtsboven (14,28), geen V, en het rechteruiteinde **raakt de omtrek** ((14,28) grenst aan de omtrek op (14,27) en (15,28)). Daardoor leest hij als naad of kaprand die de schedel doorsnijdt, niet als een fade. | half, om dezelfde reden |
| Ogen: zwarte rondjes met een wit puntje | ja (4×4 met één wit puntje, zoals Hitmontop) | ja |
| Mond is gewoon een streepje, onder de ogen | **nee**: 5 px als U met opgetrokken uiteinden ((14,43), (15–16,44), (17,43), (18,42)). Dat is een glimlach, geen streepje. Hij zit bovendien tegen de rechteronderrand: het uiteinde (18,42) ligt 1 px van de omtrek, dus hij leest op 1× als een kin- of wangplooi. | **nee**, identiek |
| Kleinere punt zichtbaar | **nee**: knot en punt vormen samen één druppel of uienpunt. Er steekt geen aparte kleine punt uit. | ja, maar het is een sprietje van 1 px breed met een eigen omtrek ((7,23–28)) en leest als antenne of steeltje |
| Haar opgeknot, knot duidelijk | **nee**: leest als Hitmontops spitse kop | **half**: een losse bol links op schedelhoogte die op 1× als oor leest |
| Hoofd tegen de klok in gedraaid | ja (kruin linksboven, rechteroog hoger) | ja |
| Leest rechtop (niet kaal met baard en niet ondersteboven) | ja | ja |
| Simpel, zoals alle Hitmons | ja | ja |
| Gesloten omlijning | ja | ja |
| Geen restpixels | **nee**: een spike van 1 px op (0,28) links bij de knotvoet, en een bult van 1 px in de rechteromtrek op (22,36–37), op ooghoogte (het rechteroog duwt de rand naar buiten) | **nee**: dezelfde bult op (24,36–37) rechts, en een open inham (col 6, rij 26–28) tussen knot en spriet |

## Lijkt op en wijkt af in
- **Lijkt op Hitmontop in:** de ogen, de huidkleur en -tinten, de ene doorlopende omtrek zonder haarlijn, de eenvoud en het rechtop lezen.
- **Wijkt af in:** de mond. Hitmontop (anime) heeft een vlakke of licht dalende lijn, dit is een lieve glimlach, en daardoor leest het gezicht chibi in plaats van stoer. De knot is in optie 1 geen knot en in optie 2 een oor. De fadestreep snijdt tot in de omtrek.

## Opmerkingen (alleen benoemde reparaties)
1. Mond: vervang de U door een recht streepje van 3–4 px, haaks op de gezichtsas (door de draaiing dus licht schuin, met het rechteruiteinde hoger). Leg het midden onder het punt tussen de ogen, minstens 2 px van de omtrek.
2. Fadestreep: laat hem vóór de omtrek ophouden (minstens 1 px J ertussen aan beide kanten). Maak hem korter, zodat hij een boog of flauwe V over het voorhoofd is en niet de hele schedel doorsnijdt. De uiteinden in D zijn goed.
3. Restpixels: haal de spike op (0,28) weg (optie 1) en trek de rechteromtrek op ooghoogte recht (optie 1 rij 36–37 col 22, optie 2 col 24). Schuif zo nodig het rechteroog 1 px naar binnen.
4. Knot: optie 2 is de betere basis. Laat de bol de schedelomtrek overlappen of erop zitten (hoger en meer naar achteren, boven de kruinlijn), zodat hij niet op oorhoogte naast de kop hangt. Geef de punt 2 px voet, zodat hij een kleine Hitmontop-punt is en geen spriet. Optie 1 laat geen aparte knot zien en moet dan vervallen.

Oordeel: FAIL
