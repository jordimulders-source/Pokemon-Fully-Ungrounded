# Lama fase 2: kleur ronde 4c (zelfde maker, 4 nov)

Jordi over 4b (letterlijk): "ik vind het al wat beter worden, maar het lichaam plus nek is nog steeds een beetje een te flakke plank tov de fluffy look van mareep en flaaffy. [...] Het oog ziet er wel un-pokemon like uit, kunnen we het oog nog wat droger en meer lama maken, maar wel pokemon achtig".

Er zijn alleen twee zones aangepast: (1) lijf en hals en (2) het oog. De rest is 0 px anders dan 4b; dat bewijst `bron/controle_uitvoer.txt`. Alles is met de hand getypt in `bron/lama_raster.txt`.

## Studie (op 4×–8×)
- **Mareep en Flaaffy:** het volume komt uit meerdere grote wolbollen die elkaar overlappen. Elke bol heeft zijn licht linksboven en een eigen zachte schaduwrand (middentint) aan de onderkant. De rand van de bol ervoor valt over de lichte top van de bol erachter, en de omtrek bestaat uit ronde bogen. Er zijn geen spikkels en geen banden.
- **Ogen van kalme Gen 3-viervoeters** (Ponyta, Rapidash, Numel, Camerupt, Girafarig, Stantler, Spinda): Pokémon-achtig door een donkere pupil of iris, een duidelijk licht puntje en een omlijnd lid. Kalm of droog door een vlakke lidlijn, een pupil tegen het lid en een lichtje dat laag zit (geen sterretje bovenin). Rapidash en Camerupt maken het lid in huidtint, met de lidlijn als scherpe rand.

## 1. Lijf en hals: vijf wolbollen plus twee op de hals
- **Hals** (blijft kaarsrecht, omtrek ongewijzigd): twee bollen boven elkaar, op y20–23 en y24–27. Elke bol heeft licht `h` linksboven, `l` in het midden en een schaduwrand `b` als boog onderaan; aan de rechterkant loopt een gladde schaduwband (`b`, `s`).
- **Lijf:**
  - A, borst (x12–21): de grootste lichtkoepel, met een schaduwboog rechtsonder.
  - B, schouder (x22–28).
  - C, romp onder de doek (x29–35): de doek werpt schaduw op de top; schaduwboog onderaan.
  - D, achterbuik (x36–42).
  - E, achterwerk (x40–52): lichtkoepel bovenaan, met een schaduwsikkel b→s langs de rechterkant en de onderkant.
  - Elke bol heeft zijn eigen schaduwrand; de rand van de bol vóór valt op de lichte top van de bol erachter.
- **Omtrek in bogen, alleen bij de wol:** de borst bolt uit tot x12 (y35–39), het achterwerk tot x52 (y31–34) en daar weer in naar x50 (y37–39). De hals, de kop, de poten, de doek en de halsband houden hun omtrek. In totaal 35 px afwijking van ronde 6, nergens meer dan 2 px van de 50%-grens van het model (`diff_silhouet.txt`).

## 2. Oog (x19–24, y11–15; 1 px groter dan in 4b)
- y11: een zachte lidplooi (`d`).
- y12: een zwaar, vlak bovenlid in huidtint (`b`/`s`).
- y13: een rechte zwarte lidrand die over de bovenhelft van het oog valt.
- y14–15: een grote donkere iris/pupil (`k`, rand in `n`) met een crème lichtje laag vóór (`h`).
- Twee wimpers achteraan: `k` op (24,12) en (24,13).
- Het resultaat is geen zwart rondje met een wit puntje en geen dicht streepje. Op 1× leest het als een donker, half geloken lama-oog.

## Controles
```
mode P | transparency 0 | 16 kleuren (incl. transparant) | 1180 px
diff t.o.v. 4b: 185 px = oogzone 20 + wolzone 165; daarbuiten 0 px
silhouet t.o.v. ronde 6: +26 / -9 (35 px), wol max. 2 px, rest max. 1 px van het model
open randen 0 (pseudo-omlijning §8: oor van 2 px, nagels van 1 px)
```

## Eerlijk
- Het lijf blijft langer en rechter dan dat van Mareep. Dat is de massa en pose van het model, en die moet blijven. Binnen die vorm leest het nu als overlappende wolbollen en niet meer als een plank.
- De kop op 8× op het vel is uitgesneden op y0–21, net als bij Ponyta en Girafarig.

## Lessen
- Volume in wol komt uit **overlappende bollen met elk een eigen schaduwrand onderaan**, niet uit één schaduwrij. Eén rij afwisselende bollen leest al snel als een band.
- Een lama-oog dat toch Pokémon-achtig is: een lid in huidtint met een zwarte lidrand eronder, en alleen de onderhelft van de iris zichtbaar, met een lichtje. Grijze iriskleur (`n`) als hoofdtint leest "un-Pokémon"; een donkere iris met een licht puntje werkt beter.
- Breid het zonemasker in een controlescript uit met de echte letters van het vorige raster (doek, halsband), niet met een rechthoek: een rechthoek telt de wol ernaast mee als "buiten de zone".

---
# Ronde 4d: alleen de hals (4 nov)
Jordi over 4c (letterlijk): "ik vind het lichaam wel goed nu, misschien de nek nog ietsje meer. Oog vind ik eigenlijk ook wel prima". Lijf en oog zijn bevroren.

- **Hals (x15–27, y20–28):** drie overlappende wolbollen in plaats van twee: y20–22, y23–25 en y26–28.
  - Elke bol heeft licht `h` linksboven, `l` in het midden en een schaduwboog `b` aan de onderkant.
  - Rechts loopt een gladde schaduwband `s`.
  - De voorrand bolt per bol 1 px uit (x15 op y21–22, y24–25 en y27); de achterrand ook (x26 op y22–23 en y25–26). Daardoor bestaat de omtrek uit zachte bogen.
  - De hals blijft kaarsrecht en even dik.
- **Kosten:** 37 px (budget ±40), allemaal in de halszone. **0 px verschil met 4c daarbuiten:** kop, oog, oren, halsband, lijf, doek, staart en poten (zie `bron/controle_uitvoer.txt`).
- **Silhouet:** 9 nieuwe px. Elk ligt 1 px van de 50%-grens van het model, dus binnen de toegestane 2 px (`diff_silhouet.txt`).
- `jordi_4d.png` is opgebouwd zoals `jordi_4c.png`: 4×, kop en hals op 8×, en 1×. Gemaakt met `bron/jordi.py`.
- **Les:** laat de bollen aan de voor- en achterrand verspringen (voor y21–22, achter y22–23), zodat de hals overal even dik blijft en de bogen niet tegenover elkaar liggen als een rups.

---
# Ronde 4e: alleen de hals, onregelmatig (4 nov)
Jordi over 4d (letterlijk): "is nu iets teveel buis achtig". Drie gelijke bollen boven elkaar met verspringende uitbollingen lazen als een rups.

- **Uitgangspunt is de hals van 4c**, niet die van 4d. Wat ik veranderde (x15–27, y20–28):
  - Eén grote, zachte lichtmassa linksboven: `h` op y20–24, naar beneden smaller.
  - Een kleine pluk vóór op y25, met een kort schaduwstreepje `b` op x18 dat alleen aan de linkerkant zit.
  - Een grotere kraagpluk vóór, boven de halsband (y26–28), met `b` eronder op x16–18.
  - De achterkant is rustig: een gladde band `b`/`s` zonder bochten.
  - Er zijn geen gestapelde segmenten en geen randen over de hele breedte.
- **Omtrek:** alleen de voorkant bolt 1 px uit, op x15 y26–27, waar de kraag naar de borst loopt. Beide pixels liggen 1 px van de 50%-grens van het model. De achterkant is ongewijzigd, de hals kaarsrecht en even dik.
- **Kosten:** 29 px t.o.v. 4c (budget ±30), allemaal in de halszone. **0 px verschil buiten de hals**, met zowel 4c als 4d (`bron/controle_uitvoer.txt`).
- **Eigen check op 1× en 8× (`jordi_4e.png`):** het leest niet meer als buis of rups. Je ziet één zachte wolhals met een lichte kant links en een kraagje vóór boven de halsband.
- **Les:** fluffy maak je met ongelijke massa's. Gelijke herhaalde segmenten, ook als ze verspringen, lezen als een geribbelde buis.

---
# Ronde 4f: alleen de hals, iets voller (4 nov)
Jordi over 4e (letterlijk): "klein beetje meer nog".

- **Vanaf 4e, in dezelfde taal:**
  - Meer contrast: de lichtmassa `h` linksboven is breder (y20–23) en de schaduwkant rechts is een tint dieper (`s s` in plaats van `b s`).
  - Eén zachte pluk achter op y22–23 (x26 bolt 1 px uit), hoger dan de kraag en op een andere hoogte, dus niet symmetrisch.
  - De kraagpluk vóór is 1 px voller (x14 op y27–28).
- **Omtrek:** de nieuwe pixels liggen elk 1 px van de 50%-grens van het model (`diff_silhouet.txt`). De hals blijft kaarsrecht en even dik.
- **Kosten:** 22 px t.o.v. 4e (budget ±20, dus 2 px erover), allemaal in de halszone. **0 px verschil buiten de hals** (`bron/controle_uitvoer.txt`).
- **Eigen check op 1× en 8× (`jordi_4f.png`):** één wolhals met een kraag vóór en een pluk achter. Het leest niet als buis of rups.

---
# Ronde 4g: alleen de hals, bolliger (4 nov)
Jordi over 4f (letterlijk): "nee dit ziet er als een gekke uitstulping uit, ik wil het iets bolliger en wolliger en aan de linkerkant ook eentje aan de onderkant".

- **Pluk achter weg:** x26 op y22–23 is verwijderd. De achterrand is weer rustig en recht, zoals in 4e.
- **Drie ronde wolbollen van verschillende maat**, overlappend en niet gestapeld:
  - Bol 1, groot, bovenaan: ronde lichte kern `h` op x17–19 y20–22, met een korte schaduwboog op y24 (x18–20).
  - Bol 2, klein, midden-rechts: lichte kern op x21–23 y24, met een schaduwboog op y26 (x21–23).
  - Bol 3, een ronde borstbol vóór onderaan, vlak boven de halsband (x14–20, y25–28): kern `h` op x15–17 y26–27, schaduwboog `b` op y28. Hij bolt over de voorrand uit tot x14 en vormt samen met de kraag van 4e/4f één geheel.
- **Omtrek:** alleen vóór onderaan uitgebold (x15 y26, x14–15 y27, x14 y28), elk 1 px van de 50%-grens van het model. De hals blijft kaarsrecht.
- **Kosten:** 32 px t.o.v. 4f (budget ±35), allemaal in de halszone. **0 px verschil buiten de hals** (`bron/controle_uitvoer.txt`).
- **Eigen check op 1× en 8× (`jordi_4g.png`):** er is geen uitsteeksel en geen los plukje, en de hals leest niet als buis. Je ziet een wolhals met een grote bol boven en een ronde borstbol vóór onderaan.
- **Les:** een uitbolling van 1–2 px op een rustige rand leest als een "gekke uitstulping" als er geen bol achter zit. Een uitbolling moet de rand zijn van een ronde lichte kern met een schaduwboog.
