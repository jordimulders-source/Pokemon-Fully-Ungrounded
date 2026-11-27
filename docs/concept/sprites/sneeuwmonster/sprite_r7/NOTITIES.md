# Sneeuwmonster r7
Basis: `sprite_r6/r6_knoop_a.png`. Jordi: "links, de stenen zijn nog steeds te recht en onder de stenen bij de linkerpoot zit een vlak in een effen kleur, fixen".
Ogen, hoofdrand en kuif bevroren. Wijzigingen alleen in de knoopvakken (x23–28/y33–39 en x22–28/y40–45) en zone 2 (x19–34, y41–48); assert in `bouw.py`.

## Stenen (varianten als hele sprites `r7_s1/s2/s3.png`; `sneeuwmonster_r7.png` = s1)
Modelmeting (tweede momenten van de steenpixels in het 1024-model, omgerekend naar spritepx): bovenste knoop midden (26,3; 36,8), 4,8 hoog × 3,8 breed, grote as 118° (iets schuin: boven naar rechts); onderste knoop midden (26,0; 43,1), 4,4 × 4,4, dus rond en niet gekanteld.
Plek per patroon: de verschuiving met de hoogste som (dekking − 0,5) over de patroonpixels.
- **s1:** boven 4×5 schuin ovaal `.XX./.XXX/XXXX/XXXX/.XX.` = Girafarig (26,23) / Mantine (6,24) `_gba` gespiegeld, op (24,34). Onder 5×4 `.XXX./XXXXX/XXXXX/.XXX.` = Horsea (23,20), Kangaskhan, Lairon, Pinsir, Seaking `_gba`, op (24,41). Knopen 14 px, zone 2 14 px.
- **s2:** boven sterker gekanteld `..XX/.XXX/XXXX/XXX./.XX.` op (24,34). Onder 5×5 gekanteld rond `.XXX./XXXXX/XXXXX/XXXX./.XX..` = Charizard (18,48) / Egg (35,26) `_gba`, op (24,41). Knopen 18 px, zone 2 14 px.
- **s3:** beide het rondste en meest voorkomende steentje van ±5 px in `_gba`: `.XXX./XXXXX/XXXXX/.XXX.` (9×: Horsea, Kangaskhan, Lairon, Pinsir, Seaking); boven op (24,35), onder op (24,41). Knopen 15 px, zone 2 14 px.
- Tinten per pixel uit het model (< 40 zwart, < 70 steen donker, < 105 midden, anders licht; een patroonpixel zonder steendekking krijgt de tint van de dichtstbijzijnde pixel met dekking): licht linksboven, donker/zwart rechtsonder.

## Zone 2, effen vlak onder de stenen bij de linkerpoot (14 px)
Sneeuwtint per pixel uit de modelhelderheid (schaduw < 212, midden < 236, licht), ontkorreld binnen de zone. Modelwaarden (L sneeuw, x19–34):
```
41   . 236 241 225 241 243   .   . 243 242 243 243 243 243 243 243
42   . 218 242 240 242   .   .   .   . 242 243 243 240 243 243 235
43   . 205 220 243 243   .   .   .   . 242 243 243 236 243 243 237
44   .   . 202 213 230 240   .   . 212 239 243 243 243 241 231 215
45   .   . 202 201 203 216 200 204 233 243 243 235 215 214 201 208
46   .   .   . 199 201 201 201 201 201 201 201 199 200 201 208 214
47   .   . 233 225 205 201 201 200 200 200 199 200 200 200 204 200
48   . 242 242 241 217 202 200 201 198 198 200 199 200 198 200 200
```
Resultaat: de lichte bolling linksonder (x20–23, y41–43, L 236–243) is weer licht, met midden en schaduw eronder (y44–45, L 202–230) en de lichte plek onder de onderste knoop (x27–30, y45, L 233–243). De r2-verzachting had dit allemaal midden gemaakt.

Eerlijk: de band y46–47 is ook in het model één vlakke schaduw (L 199–201 over x22–33). Daar zit geen toonverdeling in die ik kan overnemen, dus die blijft effen. Bedoelt Jordi juist die band, dan is meer tonen daar een keuze (verzonnen volume), geen overname.
