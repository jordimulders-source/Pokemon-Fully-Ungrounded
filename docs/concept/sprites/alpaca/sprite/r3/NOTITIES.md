# Palpaca r3 (19 nov): kleur-/schaduwronde naar Gen 3

Opdracht: `../OPDRACHT_KLEUR.md`. Jordi: "het schaduwwerk over de hele sprite heen is nog niet zo goed he, het is teveel zoals het model" · "dat de kop hoekig leest moet je oplossen met kleurgebruik en schaduwen" · "en als je het linkeroog nog in beeld probeert te brengen, zou dat iets opleveren?" · "met het oog moet je echt goed naar het model kijken" · "kan misschien ook een beetje perspectief met de neus" · "want die loopt in het model iets verder naar binnen".

## Bestanden
- `palpaca.png` (A, zonder verre oog) en `palpaca_B.png` (B, met verre oog): 64×64, geïndexeerd, index 0 transparant, 16 kleuren.
- `normal.pal`, `vel.png` (r3 8× | r2 8× | Mareep | Skitty · 1× en 2× op licht/donker: A, B, r2 · close-up kop 12×: model op spriteraster | A | B | r2).
- `scripts/bouw_r3.py`: het handgemaakte tekstraster (rijen 18–55, kolom 0 = x 14); controleert alfa-diff en rijlengte tegen r2. `scripts/px.py`: modelmeting per spritepixel (zelfde geometrie als r2/bouw.py). `scripts/modelkop.py`: model op het spriteraster, 12×. `scripts/vel.py`: het vel.

## Controle
- **Alfa-diff met r2: 0 px** (A en B). Silhouet, pootstand en lijnen niet verschoven; ook aan de snuit is niets aan het silhouet veranderd (zie Neus).
- A t.o.v. r2: 243 px anders (kop 85, hals 22, lijf + staart 122, poten 14). B t.o.v. A: 2 px.
- Kleurzones per pixel gelijk aan r2 (wol blijft wol, rood blijft rood, enz.; gecontroleerd met script).

## Palet (alleen de wolramp bijgesteld, rest = r2)
| idx | r2 | r3 | rol |
|---|---|---|---|
| 2 | 255 250 236 | = | hooglicht |
| 3 | 242 224 192 | 240 220 184 | basis crème |
| 4 | 210 166 166 | 214 174 158 | schaduw 1 (iets warmer, minder roze) |
| 5 | 152 108 136 | 166 122 136 | schaduw 2 / binnenlijn |
| 6 | 100 66 98 | 112 76 100 | selout lichtkant |
Index 1 blijft de donkere lijn aan de schaduwkant (rechts/onder).

## Per zone
- **Kop**: licht linksboven. Eén rustig hooglichtvlak op de kuif linksboven (2), verder basis. De kuif is nu twee duidelijke krullen boven het gezicht: één golflijn in 4 (geen 5, geen donkere wenkbrauw) met een amplitude van 2 rijen (dalen op y 22, bodems op y 24) en een hooglichtje van 2 px op de bovenkant van elke krul (y 22). De hoekige kop wordt rond door een **sikkel aan de verre (rechter)kant**: 2 px 4 + 1 px 5 langs de rand van y 19 tot 32, onderaan breder, en de rechterbovenhoek van de kuif in 4 (y 18–20), zodat de hoek wegdraait. Losse wanglijn van r2 weg (gaf banding naast de sikkel). Kaak: onderkant in 4/5, kinlijn loopt taps door in 5 (x 21, y 32).
- **Neus/snuit** (perspectief, alleen kleur): snuitrug in 2 (x 18–19, y 28; model 235/241), schaduwkant van de snuit links-onder in 4 (x 18, y 29–30; model gem. 221/210, min 139), neusgat 5 **één pixel naar binnen**: van (18,29) naar (19,29) (model: (19,29) gem. 212, min 104 = donkerste punt; (18,29) min 139). Het silhouet van de snuit hoefde daarvoor niet te veranderen: de modelomtrek ligt op dezelfde plek (x 17, y 28–31). Mondlijn (18–19,31)(21,31) ongewijzigd.
- **Oog (dichtbij)**: ongewijzigd (2×4, glans linksboven).
- **Verre oog (alleen B)**, gemeten in het natieve model (`px.py`, aandeel donker = helderheid < 120):
  | pixel | model gem./min | donker | A | B |
  |---|---|---|---|---|
  | (18,26) | 75 / 16 | 0,78 | 6 (selout) | **1** |
  | (18,27) | 109 / 27 | 0,56 | 6 (selout) | **1** |
  | (19,26) | 162 / 27 | 0,33 (deels kuiflijn) | 3 | 3 |
  | (19,27) | 199 / 27 | 0,11 | 3 | 3 |
  Alleen de twee pixels die het model als oog aantoont. Ze liggen precies op de bevroren omtrek (in het model staat de omtrek 1 px verder links, op x 17, dat is hier transparant). Geen glans: de glans in het model is ±¼ spritepixel.
- **Hals**: slagschaduw van de kin over de hele bovenkant (5/4, y 32–33), daaronder licht links (2) en schaduw rechts (4).
- **Lijf**: één groot hooglichtvlak op rug en borst (y 39–41) met een golvende onderrand (krullen); basis in het midden; schaduwband langs de buik en achterkant (4, buitenste rij 5) met een golvende bovenrand en een krul op de bil (x 38–39, y 41–43). Geen losse vlekjes of dambord. Onder de kraag een schaduw (4/5) in plaats van de zwarte puntjes van r2.
- **Staart**: hooglicht linksboven, twee lobben (scheiding in 4 op y 37), onderkant in 4/5.
- **Poten**: nabije voorpoten licht aan de linkerkant (2), schaduw rechts; dij met eigen hooglicht en sikkel achter; bovenkant van de achterpoot in 4 (slagschaduw van de dij). Verre achterpoot (b/f), handschoenen, manchetten, kraag, oren en kwastjes = r2.

## Zwakke punten
- Verre oog (B) is klein: het valt samen met de omtrek en leest vooral op 2×–8× als een donkerder stukje rand; op 1× nauwelijks. Groter maken kan alleen met pixels die het model niet toont of met een silhouetwijziging (x 17).
- De kop blijft van buiten de r2-omtrek (rechte rechterrand); de ronding komt uit de sikkel en de krullen. Op 1× leest hij ronder dan r2, maar niet zo rond als een omtrekwijziging zou geven.
- Selout aan de lichtkant is 6 (donker mauve); een lichtere selout (5) aan de bovenkant van rug en kop is niet geprobeerd.
- Verre achterpoot heeft nog een zwarte omlijning (1) ook aan de lichtkant (r2, niet aangeraakt).
- Nog niet gekeurd door een onafhankelijke keurder.
