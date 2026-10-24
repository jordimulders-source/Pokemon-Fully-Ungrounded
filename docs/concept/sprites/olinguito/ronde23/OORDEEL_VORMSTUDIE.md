# Olinguito ronde 23: oordeel vanuit de vormstudie (24 okt)

Vel: `oordeel.png`. Ronde 23 naast Poochyena, Growlithe, Vulpix, Zigzagoon, Nickit en Galar-Linoone, op 3× met het kopvak in magenta en op 1×. Maatstaf: `docs/lessen/FAKEMON_CHECKLIST.md` (D1–D4, sjabloon "kleine viervoeter fase 1") en `docs/lessen/vormstudie/metingen.csv`. Er is niets aan de sprite veranderd.

Ik ga er niet mee akkoord. De kop is wel iets te groot, maar niet op de manier die je zou denken. Hij is niet te hoog, hij is te **lang**. Daarnaast ontbreekt de vierde poot en is de sprite als geheel te groot voor een fase 1.

## 1. Kopgrootte
Kopvak = van oortop tot kin, van neuspunt tot achterhoofd (zonder nek of manen), met de hand vastgesteld op een raster. Het kopoppervlak is het aantal spritepixels binnen dat vak; dat telt bij alle soorten op dezelfde manier iets lijf mee.

| Soort | totaal px | kopvak b×h | kophoogte / totale hoogte | kopoppervlak / totaal |
|---|---|---|---|---|
| **Olinguito r23** | 1045 | **29×20** | 56% | **42%** |
| Poochyena | 887 | 18×22 | 55% | 34% |
| Zigzagoon | 1315 | 20×25 | 69% | 32% |
| Growlithe | 1088 | 24×25 | 61% | 41% |
| Vulpix | 1119 | 24×23 | 57% | 38% |
| Galar-Linoone (volwassen) | 1169 | 22×17 | 57% | 25% |
| Eevee / Skitty / Meowth / Shinx / Lillipup / Purrloin | 735–934 | 30–34 breed | 62–70% | 59–79% (frontale kop met grote oren) |
| Nickit | 1095 | 25×36 | 78% | 51% (grote oren) |
| Sentret | 941 | 20×17 | 30% | 27% (staande soort, lange staart) |

Mediaan van alle 13 referenties: kophoogte 62%, kopoppervlak 51%.

- **Kophoogte (56%) is normaal**, eerder aan de lage kant. Een fase 1 heeft een grote kop.
- De eerlijke vergelijking is met de **snuitdieren met een kop in 3/4-profiel en één oog** (Poochyena, Zigzagoon, Growlithe, Vulpix, Galar-Linoone). Hun kopoppervlak ligt op 25–41%, mediaan **34%**. Ronde 23 zit op **42%**: ±8 procentpunt, ±85 px te veel kop voor dit lijf.
- Waar dat in zit: **de kop is 29 px lang.** Bij de snuitdieren is dat 18–24 px. De verhouding breed/hoog is 1,45, tegen 0,8–1,05 bij Poochyena, Zigzagoon, Vulpix en Growlithe (alleen de volwassen Linoone komt aan 1,29). De kop is dus ±5 kolommen (±20%) te lang. Het lijf onder die kop is dun en laag (romp ±607 px, net zoveel als Poochyena), en daardoor oogt de kop "te groot".
- **Zo los je het op zonder het gezicht te hertekenen** (rastercontrole: het masker loopt tot x28 en het verre oor zit direct daarnaast op x29–35, y19–24; een kolomknip door de schedel zou dus het oor of het masker raken): leg de **achterhoofdcontour 2–3 px naar binnen**. Op y25–33 wordt de rand x36–38 (nu `331`) nieuwe omlijning op x33–35, en wat erachter ligt gaat naar de nekrug. Die nekrug loopt dan als één holle curve van het verre oor naar de rug op y32 (±20–25 px handwerk). Neus, masker, oog en beide oren blijven pixel voor pixel gelijk. Het verre oor komt op de achterrand van de schedel te staan, zoals bij Poochyena. Resultaat: schedel ±26 px lang, kopoppervlak ±38–39%, totaal ±1020 px. Lever het als variant naast ronde 23.
- **Niet doen:** het lijf of de poten groter maken. Het totaal (1045) zit al boven de fase-1-band van 700–950 (D1); een groter lijf maakt het een fase 2.

## 2. De vierde poot (verre achterpoot)
Hoe vergelijkbare sprites dat doen (vel `oordeel.png`, en `docs/lessen/vormstudie/vellen/z_c.png`):
- **Mightyena:** de verre achterpoot staat helemaal in beeld **tussen** de verre voorpoot en de nabije achterpoot, ±6×13 px, donkerste tint, voet 3 px hoger dan de nabije achtervoet.
- **Nickit** (zelfde lage marterhouding): de verre achterpoot is ±4–5 px breed en ±8 hoog, onder de buik vóór de dij van de nabije achterpoot. Hij is in de donkere tint, met de voet 1–2 px hoger.
- **Poochyena:** een smalle donkere strook van ±3 px links naast de nabije achterpoot.
- **Galar-Linoone en Zigzagoon** laten hem bijna weg (lage romp, vacht). Een lang, laag dier mag dat dus, maar Jordi wil hem zien; in dit raster past alleen de Poochyena-oplossing (zie hieronder).

**Voorstel voor ronde 23** (rastercontrole: de verre voorpoot met klauwen loopt tot x34, de dij van de nabije achterpoot begint op x37; daartussen is alleen x34–37 op y45 en x35–36 op y46–50 leeg): teken de verre achterpoot als **smalle donkere strook in het vak x34–36, y44–51**, zoals Poochyena. Er is geen ruimte voor een volle Nickit-poot zonder een goedgekeurde poot te verschuiven. De bevroren J-staart (x44–56) blijft onaangeraakt, en het stompje achter de staartkrul blijft staan.
- Aanzet: onder de buikrand (y44, de rij `11111` x33–37), zonder zwarte lijn ertussen, zodat de poot uit de buik komt (les uit ronde 23: vastmaken = geen lijn ertussen).
- Vorm: 3 px breed (x34–36), met x37 als de bestaande omlijning van de nabije dij, die hem overlapt. Op y47–48 schuift hij 1 px naar rechts (hak naar achteren). Voet op y50–51, dus 2 rijen hoger dan de nabije achtervoet (y53–54), met onderaan één klauwpixel in de donkerste klauwtint.
- Tint: binnen schaduwtint 3, links omlijning 2, onderaan 1; geen 4/5. Links houdt de omlijning 1 (x33) hem gescheiden van de verre voorpoot; die kolom is nu al deels 1/3.
- Omvang: ±18–22 px per frame, binnen x33–37, y44–51. Frame 2: zelfde plek.
- Werkt dat op 1× niet (te smal), dan is het alternatief een **variant** waarin de verre voorpoot 2 px naar links schuift (x23–32) voor een Nickit-poot van 5 px. Dat raakt een goedgekeurde poot en mag dus alleen als variant.

## 3. Andere checklistpunten die ronde 23 nog niet haalt
- **D1 formaat:** 1045 px (fase 1: 700–950). Het kortere achterhoofd uit punt 1 helpt; meer is niet nodig, want vorm gaat vóór de grens.
- **D4 breedte:** 48 px, precies op de grens; goed.
- **C2/C6 poten:** na punt 2 vier poten, met voeten op vier hoogtes (nabije voor y53, verre voor y52, nabije achter y54, verre achter y51): de diepte die Mightyena heeft.
- **A3 tegenwicht:** de J-staart komt niet boven de ruglijn uit (top ±y35 tegen rug y32). Dat is een richtlijn (R) en de staart is bevroren, dus laten zo.
- **B5 oren (R):** het verre oor (x29–35) is groter en hoger dan het nabije (x15–21). Bij Poochyena en Teddiursa is het verre oor kleiner of half bedekt. Klein punt; alleen als variant aanpakken, want de kop is goedgekeurd.
- **A6 rechte lijnen:** ruglijn y32 x40–44 is 5 px recht (grens 4); 1 px laten zakken op x43–44 is genoeg.
- **Wel gehaald:** B2 (lange snuit + één oog, neus als meest linkse punt), B1 (kop meer naar de kijker dan het lijf), A2 (J-staart als kenmerk), A5 (asymmetrisch), C4 (hak aan de nabije achterpoot), C7 (één houding).
