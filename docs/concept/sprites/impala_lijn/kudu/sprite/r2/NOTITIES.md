# Kudu sprite ronde 2 (maker)
Jordi koos manenvariant A: "A is goed, alleen houd er rekening mee dat gemini die boog had gedaan omdat er een schouder zat, dus die boog hoeft geen boog meer te zijn". Keelfranje blijft zoals in r3b.

## Manen A2 (op modelniveau, `manen_a2.py`)
- **Welke boog:** de gebogen zwarte onderrand van de manen in r3b, die precies de schouderlijn volgt. In r1-A was die met de kopie (+70,+30) mee geschoven en lag hij midden op het lijf. Rood in `boog_viz.png`.
- **Wat ik veranderd heb:** de donkere boogpixels van de kopie (binnen 10 px van de onder- of rechterrand van de kopie, boven het lijf) vallen weg, 2359 modelpx. Daaronder komt het originele model (lijf) terug. Waar de boog onderaan zat, hangen per kolom lokpunten uit het model onder de rand. Twee bronnen:
  - **A2a (gebruikt):** de keelfranjepunten van r3b (x 215-320, y 655-760), 4011 modelpx.
  - **A2b (alternatief):** de lokpunten van r3c, 4561 modelpx. Geeft op het model kleine strookartefacten; in de reductie is het verschil klein (`red_A2a.png` / `red_A2b.png`).
- **Dubbele kamrand weg:** de kopie bevat geen kamlokken meer (bron x>440 en y<530), dus de kam op de schoft is alleen die van r3b.
- **Manen t.o.v. de kale reductie van r3b:** A2a wijkt 96 px af, A2b 98 px, allemaal in de manenzone.
- **Eerlijke kanttekening:** de manen hangen nu recht over de schouder. De rechterrand is een vrijwel verticale haargrens zonder lijn, dus geen boog meer. Of Jordi met "boog" deze onderrand bedoelde of de ronding van de hele haarmassa, weet ik niet zeker.

## Afwerking (`r2.py`, zones in `zones.py`, hoornskelet in `hoorn.py`)
**Basis.** De basis is de kale reductie van model A2a (cel 16, lijn bij ≥25% modellijn). Elke cel krijgt de zone waar de meeste modelpixels in de cel bij horen:
- vacht
- manen (blauwarm haar plus het keelfranjevak)
- staal
- wit
- roze oor
- donker (alleen neus en hoeven)

De tint komt uit de gemiddelde modelhelderheid van die zone in de cel. Er is niets met de hand geschaduwd.

**Palet** (15 kleuren incl. transparant):
- omlijning: #302418
- vacht goud: L #F8D888, M #D8A850, D #A07030
- manen donkerder goud: l #D0A038, m #A87C24, d #6C4C14
- staal (Steelix-tinten): A #4A5A7B (selout en binnenlijn), 3 #7B8FAE, 4 #BCCBDD
- wit: #FFFFFF (slijprand en tekening)
- oor: R #E0A090, r #B06A58
- neus/hoef: K #5C4434

ΔE staal–vacht is 54–71, dus het staal is duidelijk anders dan de vacht.

**Stappen:**
1. **Wit:** uit de witfractie per cel. Lijfstrepen zijn 1 px breed (de cel met de hoogste fractie per reeks). Gezicht (V, wangvlekjes, lip): cellen met ≥30% wit.
2. **Hoorns:** een band langs de middellijn van het model, breedte 4 → 3 → punt, dus nergens alleen 1 px lijn. Binnenin wordt per pixel over de breedte gemeten wat in het model het lichtst is: dat wordt W (≥200) of 4, de donkere kant 3. De oude hoornreductie buiten de band valt weg.
3. **Ontkorrelen:** tintvlakjes kleiner dan 3 px in vacht en manen.
4. **Binnenlijnen:** in de donkerste eigen tint (manen d, vacht D, staal A, oor r). Zo zijn er geen losse zwarte pixels meer tussen de strengen.
5. **Poten (Kirlia):** tint in de lengte, linkerlijn D, verre poot een tintstap donkerder. Hoeven K.
6. **Belijning:** buitenlijn zwart, selout aan de lichtkant (rand die naar boven of linksboven wijst).

## Pixels t.o.v. de kale reductie
Vergeleken met de kale reductie, omgekleurd naar dit palet: 460 van 1327 px wijken af.

| Zone | Pixels |
|---|---|
| vacht | 225 (buitenlijn en selout, strepen, Kirlia-poten, ontkorrelen) |
| staal | 126 (nieuwe hoornband) |
| manen | 89 (binnenlijnen d, ontkorrelen, selout) |
| roze | 11 |
| donker | 8 (hoeven, neus) |
| wit | 1 |

Daarbovenop: de manenzone wijkt 96 px af van de kale reductie van r3b (manen A2a). Per stap staat alles in `telling.txt`, per pixel in `wijzigingen.txt`.

## Oog
Het modeloog (slaperig, half dicht) valt na reductie terug tot een zwart streepje van 3 px op rij 22. Het leest als een gesloten oog, niet als het model. **Gemeld: Gen 3-oog kiezen met Jordi, zoals bij de impala.**

## Eigen zwakke punten
- **Flank:** de strepen staan dicht op elkaar (6 in ±11 kolommen) met tussen de strepen de lichte modeltint L. Dat oogt druk. Het is wel modelmateriaal; ik heb het niet rustiger gemaakt.
- **Hoorns:** smal in verhouding tot het model op 8×. De witte slijprand is maar deels zichtbaar (veel 3 en 4); de spiegelglans kan sterker. De trapjes zijn nog niet per pixel geregeld, zoals bij de impala in r5 (TRAP).
- **Hoeven:** klein (1-2 px K).
- **Kirlia op de poten:** heeft maar 16 px veranderd. Waar het model al een tint had, is die blijven staan.
- **Overgang manen–lijf op de schouder:** heeft geen binnenlijn, alleen tintverschil.
- **Vel:** de rij "1× op licht en donker" toont r2 | r1-A | impala. Het losse blok met vier achtergronden linksonder bevat alleen r2.
